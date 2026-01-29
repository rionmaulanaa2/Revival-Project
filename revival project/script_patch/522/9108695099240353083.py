# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/ObserveCameraRecover.py
from __future__ import absolute_import
import six
from data.camera_state_const import *
from .ObserveCameraStates import get_prefer_cam_state_pitch_and_yaw
from logic.gutils.CameraHelper import is_posture_inherit_camera_type, get_mecha_camera_type, is_dependent_camera_type

class ObserveCameraRecover(object):

    def get_recover_camera_status(self, target):
        if target and target.is_valid():
            result_cam_states = []
            mecha_state = self.get_in_mecha_state(target)
            if mecha_state:
                result_cam_states.append(mecha_state)
            all_camera_state = global_data.camera_state_pool.CAMERA_STATE_CLASS
            for cam_state, cam_state_class in six.iteritems(all_camera_state):
                if not is_posture_inherit_camera_type(cam_state):
                    if cam_state_class.on_recover_check(cam_state_class, target):
                        result_cam_states.append(cam_state)
                        break

            for cam_state, cam_state_class in six.iteritems(all_camera_state):
                if is_posture_inherit_camera_type(cam_state):
                    if cam_state_class.on_recover_check(cam_state_class, target):
                        if cam_state == FREE_MODEL:
                            result_cam_states.append(cam_state)

            recorded_cam_state = target.ev_g_cam_state()
            if recorded_cam_state:
                if len(result_cam_states) <= 0:
                    result_cam_states.append(recorded_cam_state)
                elif len(result_cam_states) > 0 and recorded_cam_state and recorded_cam_state != result_cam_states[-1]:
                    result_cam_states.append(recorded_cam_state)
            if len(result_cam_states) >= 1:
                last_cam = result_cam_states[-1]
                if is_dependent_camera_type(last_cam):
                    result_cam_states.insert(0, THIRD_PERSON_MODEL)
            if not result_cam_states:
                result_cam_states.append(THIRD_PERSON_MODEL)
            if recorded_cam_state in [THIRD_PERSON_MODEL] and mecha_state:
                result_cam_states.append(mecha_state)
            return result_cam_states
        else:
            return []

    def get_in_mecha_state(self, lplayer):
        if lplayer and lplayer.ev_g_in_mecha():
            control_target = lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                return get_mecha_camera_type(control_target.logic.share_data.ref_mecha_id, control_target.logic.ev_g_mecha_fashion_id())
        return None

    def recover_camera_status(self, target):
        cam_state_list = self.get_recover_camera_status(target)

        def switch_observe_target_camera(to_state):
            global_data.emgr.switch_observe_camera_state_event.emit(to_state)

        recover_func_dict = {AIM_MODE: self.recover_to_aim,
           VEHICLE_MODE: self.recover_to_vehicle,
           PASSENGER_VEHICLE_MODE: self.recover_to_vehicle,
           FREE_MODEL: self.recover_to_free_camera
           }
        for cam_state in cam_state_list:
            if cam_state in recover_func_dict:
                func = recover_func_dict[cam_state]
                func(target)
            else:
                switch_observe_target_camera(cam_state)

        if len(cam_state_list) > 0:
            final_cam_state = cam_state_list[-1]
            f_yaw, f_pitch = get_prefer_cam_state_pitch_and_yaw(final_cam_state, target)
            from logic.gutils.CameraHelper import normalize_angle
            global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(normalize_angle(f_yaw), normalize_angle(f_pitch), True)

    def recover_to_aim(self, target):
        if not (target and target.is_valid()):
            return
        else:
            from logic.gcommon import const
            lens_attachment = target.ev_g_attachment_attr(const.ATTACHEMNT_AIM_POS)
            if lens_attachment is None:
                return
            len_attr_data = lens_attachment.get('cAttr', {})
            aim_magnitude = len_attr_data.get('iLensMagnitude', 2)
            fAimTime = 0.01
            aim_item_id = lens_attachment.get('iType', 0)
            global_data.emgr.switch_to_aim_camera_event.emit(aim_magnitude, fAimTime, item_id=aim_item_id)
            return

    def recover_to_vehicle(self, target):
        if not (target and target.is_valid()):
            return
        control_target = target.ev_g_control_target()
        if control_target and control_target.logic:
            target.send_event('E_UPDATE_VEHICLE_CAMERA', control_target.logic)
        else:
            log_error('control target is not loaded!')

    def recover_to_free_camera(self, target):
        if not (target and target.is_valid()):
            return
        target.send_event('E_FREE_CAMERA_STATE', True)

    def report_outside_error(self, *args):
        import traceback
        stack = traceback.extract_stack()
        import exception_hook
        err_msg = 'Error Recover Camera state!\n' + str(stack) + '\n' + str(args)
        exception_hook.post_error(err_msg)
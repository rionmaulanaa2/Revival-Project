# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataCameraRotate.py
from __future__ import absolute_import
import cython_flag
from logic.gcommon.component.share.ComDataBase import ComDataBase
import math3d
import logic.gcommon.common_utils.bcast_utils as bcast
TYPE_UNCHANGED = 0
TYPE_SIMPLE_ROCKER = 1
MAX_SPEED = 999

class ComDataCameraRotate(ComDataBase):
    BIND_EVENT = {'E_SET_CAM_EX_CAL_FUNC': 'set_cal_func',
       'G_CAM_EX_ROTATION': 'get_angle_params',
       'E_SET_CAM_EX_ROTATION': 'set_cam_ex_rotation',
       'E_SET_CAM_EX_TRANSLATION': 'set_cam_ex_translation',
       'E_SET_CAM_EX_TARGET_OFFSET': 'set_cam_ex_target_offset',
       'E_CLEAR_CAM_EX_ROTATION': 'clear_cam_ex_rotation',
       'E_CLEAR_CAM_EX_TRANSLATION': 'clear_cam_ex_translation',
       'E_CLEAR_CAM_EX_TARGET_OFFSET': 'clear_cam_ex_target_offset',
       'E_SWITCH_CAMERA_STATE_TO_MECHA_TARGET': 'on_switch_camera_state',
       'E_SET_ENABLE_CAM_EX_FUNCTION': 'set_enable_cam_ex_function'
       }

    def __init__(self):
        super(ComDataCameraRotate, self).__init__()
        self.yaw_offset = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_target = 0
        self.pitch_target = 0
        self.roll_target = 0
        self.yaw_duration = 0
        self.yaw_speed = 0
        self.pitch_duration = 0
        self.pitch_speed = 0
        self.roll_duration = 0
        self.roll_speed = 0
        self.dirty = False
        self.use_quaternion = False
        self.translation_target = math3d.vector(0, 0, 0)
        self.translation_offset = math3d.vector(0, 0, 0)
        self.translation_duration = 0
        self.translation_speed = 0
        self.pos_offset_target = math3d.vector(0, 0, 0)
        self.pos_offset_offset = math3d.vector(0, 0, 0)
        self.pos_offset_duration = 0
        self.pos_offset_speed = 0
        self.cam_ex_cal_func = TYPE_SIMPLE_ROCKER
        self.raw_translation_target = math3d.vector(0, 0, 0)
        self.raw_pos_offset_target = math3d.vector(0, 0, 0)
        self.raw_yaw_target = 0
        self.raw_pitch_target = 0
        self.raw_roll_target = 0
        self.is_enable_cam_ex_function = False

    def get_share_data_name(self):
        return 'ref_camera_rotatedata'

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataCameraRotate, self).init_from_dict(unit_obj, bdict)
        self.dirty = False

    def _do_cache(self):
        self.yaw_offset = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_target = 0
        self.pitch_target = 0
        self.roll_target = 0
        self.yaw_duration = 0
        self.yaw_speed = 0
        self.pitch_duration = 0
        self.pitch_speed = 0
        self.roll_duration = 0
        self.roll_speed = 0
        self.dirty = False
        self.use_quaternion = False
        self.translation_target = math3d.vector(0, 0, 0)
        self.translation_offset = math3d.vector(0, 0, 0)
        self.translation_duration = 0
        self.translation_speed = 0
        self.pos_offset_target = math3d.vector(0, 0, 0)
        self.pos_offset_offset = math3d.vector(0, 0, 0)
        self.pos_offset_duration = 0
        self.pos_offset_speed = 0
        self.cam_ex_cal_func = TYPE_SIMPLE_ROCKER
        self.raw_translation_target = math3d.vector(0, 0, 0)
        self.raw_pos_offset_target = math3d.vector(0, 0, 0)
        self.raw_yaw_target = 0
        self.raw_pitch_target = 0
        self.raw_roll_target = 0
        self.is_enable_cam_ex_function = False

    def activate_ecs(self):
        super(ComDataCameraRotate, self).activate_ecs()

    def mark_dirty(self):
        self.dirty = True

    def get_angle_params(self):
        return [
         self.yaw_target, self.yaw_offset, self.pitch_target, self.pitch_offset, self.roll_target, self.roll_offset]

    def set_cam_ex_rotation(self, yaw, pitch, roll, duration, need_sync=True):
        self.is_enable_cam_ex_function = True
        self.yaw_target = yaw
        self.pitch_target = pitch
        self.roll_target = roll
        self.raw_yaw_target = yaw
        self.raw_pitch_target = pitch
        self.raw_roll_target = roll
        self.yaw_duration = duration
        self.pitch_duration = duration
        self.roll_duration = duration
        if duration > 0:
            self.yaw_speed = yaw / float(duration)
            self.pitch_speed = pitch / float(duration)
            self.roll_speed = roll / float(duration)
        else:
            self.yaw_speed = MAX_SPEED
            self.pitch_speed = MAX_SPEED
            self.roll_speed = MAX_SPEED
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SET_CAM_EX_ROTATION, (yaw, pitch, roll, duration, False)], True)

    def set_cam_ex_translation(self, translation, duration, need_sync=True):
        duration = float(duration)
        self.is_enable_cam_ex_function = True
        self.raw_translation_target = math3d.vector(*translation)
        self.translation_duration = duration
        self.translation_speed = MAX_SPEED
        if duration > 0:
            if translation:
                self.translation_speed = self.raw_translation_target.length / duration
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SET_CAM_EX_TRANSLATION, (translation, duration, False)], True)

    def set_cam_ex_target_offset(self, target_offset, duration, need_sync=True):
        duration = float(duration)
        self.is_enable_cam_ex_function = True
        self.raw_pos_offset_target = math3d.vector(*target_offset)
        self.pos_offset_duration = duration
        self.pos_offset_speed = MAX_SPEED
        if duration > 0:
            if target_offset:
                self.pos_offset_speed = self.raw_pos_offset_target.length / duration
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SET_CAM_EX_TRANSLATION, (target_offset, duration, False)], True)

    def clear_cam_ex_rotation(self, duration, need_sync=True):
        duration = float(duration)
        if duration > 0:
            yaw_speed = self.raw_yaw_target / float(duration)
            pitch_speed = self.raw_pitch_target / float(duration)
            roll_speed = self.raw_roll_target / float(duration)
        else:
            yaw_speed = MAX_SPEED
            pitch_speed = MAX_SPEED
            roll_speed = MAX_SPEED
        self.set_cam_ex_rotation(0, 0, 0, duration)
        self.yaw_speed = yaw_speed
        self.pitch_speed = pitch_speed
        self.roll_speed = roll_speed
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CLEAR_CAM_EX_ROTATION, (duration, False)], True)

    def clear_cam_ex_translation(self, duration, need_sync=True):
        translation_speed = MAX_SPEED
        if duration > 0:
            if self.raw_translation_target:
                translation_speed = self.raw_translation_target.length / duration
        self.set_cam_ex_translation((0, 0, 0), duration)
        self.translation_speed = translation_speed
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CLEAR_CAM_EX_TRANSLATION, (duration, False)], True)

    def clear_cam_ex_target_offset(self, duration, need_sync=True):
        _offset_speed = MAX_SPEED
        if duration > 0:
            if self.raw_pos_offset_target:
                _offset_speed = self.raw_pos_offset_target.length / duration
        self.set_cam_ex_target_offset((0, 0, 0), duration)
        self.pos_offset_speed = _offset_speed
        if need_sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CLEAR_CAM_EX_TARGET_OFFSET, (duration, False)], True)

    def set_enable_cam_ex_function(self, enable, duration=0):
        self.is_enable_cam_ex_function = enable

    def set_cal_func(self, func_type):
        self.cam_ex_cal_func = func_type

    def destroy(self):
        scn = global_data.game_mgr.scene
        if scn:
            com_camera = scn.get_com('PartCamera')
            if com_camera:
                com_camera.yaw(-self.yaw_offset)
                com_camera.pitch(-self.pitch_offset)
        global_data.emgr.modify_camera_parameters_event.emit(math3d.vector(0, 0, 0), math3d.vector(0, 0, 0), None)
        scn = global_data.game_mgr.scene
        if scn:
            com_camera = scn.get_com('PartCamera')
            if com_camera:
                com_camera.set_roll(0)
        self.yaw_offset = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.translation_offset = math3d.vector(0, 0, 0)
        self.pos_offset_offset = math3d.vector(0, 0, 0)
        super(ComDataCameraRotate, self).destroy()
        return

    def on_switch_camera_state(self, new_cam_type, old_cam_type, is_finish_switch):
        if not is_finish_switch:
            if self.raw_roll_target != 0 and self.roll_offset == self.roll_target:
                self.roll_offset -= self.roll_speed - 0.0001
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComAimRotation.py
from __future__ import absolute_import
import math3d
from logic.client.const import camera_const
from logic.gcommon.component.UnitCom import UnitCom
FORWARD_VECTOR = math3d.vector(0, 0, 1)
import math

class ComAimRotation(UnitCom):
    BIND_EVENT = {'E_RECORD_CUR_CAM_AIM_DIR': 'on_record_cur_cam_aim_dir',
       'E_ADD_LOCK_AIM_DIR_CAM_MODE': 'on_add_lock_aim_dir_cam_mode',
       'E_ADD_LOCK_AIM_DIR_CAM_MODE_MAP': 'on_add_lock_aim_dir_cam_mode_map',
       'E_NOTIFY_PASSENGER_LEAVE': 'on_passenger_leave',
       'E_ON_DIE': 'on_passenger_leave'
       }

    def __init__(self):
        super(ComAimRotation, self).__init__()
        self._look_at_pos = None
        self.event_registered = False
        self.passenger_leave = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAimRotation, self).init_from_dict(unit_obj, bdict)
        self.lock_aim_dir_cam_modes = set()
        self.lock_aim_dir_cam_mode_map = {}

    def _get_event_func(self):
        if self.lock_aim_dir_cam_modes:
            return self.on_switch_camera_state_for_single_mode
        if self.lock_aim_dir_cam_mode_map:
            return self.on_switch_camera_state_for_pair_of_modes

    def _process_event(self, flag):
        if flag:
            if self.ev_g_is_avatar() and not self.event_registered:
                global_data.emgr.camera_switch_to_state_event += self._get_event_func()
                self.event_registered = True
        elif self.event_registered:
            global_data.emgr.camera_switch_to_state_event -= self._get_event_func()
            self.event_registered = False

    def on_post_init_complete(self, bdict):
        super(ComAimRotation, self).on_post_init_complete(bdict)
        self._process_event(True)

    def reuse(self, share_data):
        self._process_event(True)
        super(ComAimRotation, self).reuse(share_data)

    def cache(self):
        self._process_event(False)
        super(ComAimRotation, self).cache()

    def destroy(self):
        self._process_event(False)
        super(ComAimRotation, self).destroy()

    def get_state_look_at_pos(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        from logic.gcommon.common_const.collision_const import GROUP_CAMERA_INCLUDE, GROUP_ALL_SHOOTUNIT
        CHECK_DIST = 400 * NEOX_UNIT_SCALE
        scn = global_data.game_mgr.scene
        cam = scn.active_camera
        start_pos = cam.world_position
        dir = cam.world_rotation_matrix.forward
        PartCamera = global_data.game_mgr.scene.get_com('PartCamera')
        if PartCamera:
            if PartCamera.cam_manager:
                default_pos = PartCamera.cam_manager.default_pos or math3d.vector(0, 0, 0)
                start_pos += dir * (abs(default_pos.z) + NEOX_UNIT_SCALE * 10)
        if dir.length < 0.0001:
            dir = FORWARD_VECTOR
            log_error('error direction!!!!')
        end_pos = start_pos + dir * CHECK_DIST
        hit, point, normal, fraction, color, obj = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_ALL_SHOOTUNIT, 0)
        if hit:
            look_at_pos = point
        else:
            look_at_pos = end_pos
        return look_at_pos

    def look_at_pos_to_yaw_pitch(self):
        look_at_pos = self._look_at_pos
        if not look_at_pos:
            return
        PartCamera = global_data.game_mgr.scene.get_com('PartCamera')
        PartCtrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not PartCamera or not PartCtrl:
            return
        cam_manager = PartCamera.cam_manager
        if not cam_manager:
            return
        rotate_center = PartCamera.get_rotate_center()
        if not rotate_center:
            return
        scn = global_data.game_mgr.scene
        cam = scn.active_camera
        default_pos = cam_manager.default_pos or math3d.vector(0, 0, 0)
        hypotenuse = look_at_pos - rotate_center
        if hypotenuse.length < 1:
            return
        sin_theta = default_pos.x / hypotenuse.length
        if sin_theta > 1 or sin_theta < -1:
            return
        theta = math.asin(sin_theta)
        if hypotenuse.length > 1:
            look_at_pich = hypotenuse.pitch
            look_at_yaw = hypotenuse.yaw - theta
            old_yaw = cam.world_rotation_matrix.yaw
            old_pitch = cam.world_rotation_matrix.pitch
            diff_yaw = look_at_yaw - old_yaw
            diff_pitch = look_at_pich - old_pitch
            PartCtrl.rotate_camera(diff_yaw, -1 * diff_pitch, True, camera_const.CAM_ROT_INPUT_SRC_LOOK_AT)

    def on_record_cur_cam_aim_dir(self):
        self._look_at_pos = self.get_state_look_at_pos()

    def on_add_lock_aim_dir_cam_mode(self, cam_mode):
        self.lock_aim_dir_cam_modes.add(cam_mode)

    def on_add_lock_aim_dir_cam_mode_map(self, cam_mode_map):
        self.lock_aim_dir_cam_mode_map.update(cam_mode_map)

    def on_switch_camera_state_for_single_mode(self, new_cam_type, old_cam_type, is_finish_switch):
        if self.passenger_leave:
            return
        if not is_finish_switch:
            if new_cam_type in self.lock_aim_dir_cam_modes:
                self.look_at_pos_to_yaw_pitch()
            elif old_cam_type in self.lock_aim_dir_cam_modes:
                self.look_at_pos_to_yaw_pitch()

    def on_switch_camera_state_for_pair_of_modes(self, new_cam_type, old_cam_type, is_finish_switch):
        if self.passenger_leave:
            return
        if not is_finish_switch:
            if new_cam_type == self.lock_aim_dir_cam_mode_map.get(old_cam_type):
                self.look_at_pos_to_yaw_pitch()

    def on_passenger_leave(self, *args):
        self.passenger_leave = True
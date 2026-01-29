# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComFreeSightMode.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.behavior.StateBase import clamp
from ..ComDataRenderRotate import YAW_MODE_LERP_HEAD
from common.utils.timer import CLOCK
from math import acos, fabs, pi, cos
import math3d
MAX_LERP_DURATION = 0.2
MIN_LERP_ANGLE = pi / 180
CIRCLE_ANGLE = pi * 2
MIN_RESET_INTRP_TIMER_INTERVAL = 0.1
NATURALLY_ACTIVE_MECHA_ID_SET = {
 8014, 8016, 8017, 8024, 8028, 8035}

class ComFreeSightMode(UnitCom):
    BIND_EVENT = {'E_ENABLE_MECHA_FREE_SIGHT_MODE': 'enable_mecha_free_sight_mode',
       'E_SET_MECHA_FREE_SIGHT_MODE_MIN_LERP_DURATION': 'set_min_lerp_duration',
       'E_SET_MECHA_FREE_SIGHT_MODE_DEFAULT_ENABLED': 'set_mecha_free_sight_mode_default_enabled',
       'E_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED': 'refresh_mecha_free_sight_mode_enabled',
       'E_DELAY_REFRESH_MECHA_FREE_SIGHT_MODE_ENABLED': 'delay_refresh_mecha_free_sight_mode_enabled',
       'E_SET_FORWARD_IN_FREE_SIGHT_MODE': 'set_model_forward',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_EXIT_FOCUS_CAMERA': ('on_exit_focus_camera', 99)
       }

    def __init__(self):
        super(ComFreeSightMode, self).__init__()
        self.sd.ref_mecha_free_sight_mode_enabled = False
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComFreeSightMode, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_mecha_free_sight_mode_enabled = False
        self.sd.ref_cam_correction_enabled_in_free_sight_mode = True
        self.mecha_id = bdict['mecha_id']
        self.cur_camera_state = None
        self.intrp_forward_timer = None
        self.intrp_set_up_time_stamp = 0.0
        self.delta_yaw = 0.0
        self.cur_lerp_duration = 0.0
        self.default_min_lerp_duration = 0.1
        self.min_lerp_duration = self.default_min_lerp_duration
        self.cur_target_yaw = 0.0
        self.event_registered = False
        self.default_enabled = False
        self.delay_refresh_timer = None
        return

    def destroy(self):
        if self.event_registered:
            self.unregist_event('E_MOVE', self.on_move)
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False
        super(ComFreeSightMode, self).destroy()

    def on_move(self, move_dir, *args):
        if not self.sd.ref_mecha_free_sight_mode_enabled:
            return
        if move_dir and not move_dir.is_zero:
            if self.sd.ref_effective_camera_rot:
                rot = self.sd.ref_effective_camera_rot
            else:
                rot = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)
            forward = rot.rotate_vector(move_dir)
            forward.y = 0
            forward.normalize()
            self.set_model_forward(forward)

    def on_cam_rotate(self, *args):
        if self.sd.ref_cam_correction_enabled_in_free_sight_mode:
            self.on_move(self.sd.ref_rocker_dir)

    def set_model_forward(self, target_forward, max_lerp_duration=MAX_LERP_DURATION, force=False):
        target_yaw = target_forward.yaw
        if target_yaw == self.sd.ref_logic_trans.yaw_target:
            return
        self.sd.ref_logic_trans.yaw_target = target_yaw
        if max_lerp_duration == 0.0:
            self.sd.ref_rotatedata.set_body_link_head()
            return
        yaw = target_yaw - self.sd.ref_rotatedata.yaw_head
        angle = fabs(yaw) % CIRCLE_ANGLE
        if (angle < MIN_LERP_ANGLE or self.sd.ref_rotatedata.yaw_body_mode == YAW_MODE_LERP_HEAD) and not force:
            return
        if angle > pi:
            angle = CIRCLE_ANGLE - angle
        if angle == 0.0:
            return
        cur_lerp_duration = clamp(max_lerp_duration * angle / pi, self.min_lerp_duration, max_lerp_duration)
        self.sd.ref_common_motor.set_yaw_time(cur_lerp_duration)

    def enable_mecha_free_sight_mode(self, flag, max_lerp_duration=MAX_LERP_DURATION):
        if self.sd.ref_mecha_free_sight_mode_enabled == flag:
            return
        else:
            self.sd.ref_mecha_free_sight_mode_enabled = flag
            self.send_event('E_ENABLE_CAMERA_REFERENCE_MOVE', flag)
            self.send_event('E_DISABLE_ROCKER_ANIM_DIR', flag)
            if flag:
                self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
                self.on_move(self.sd.ref_rocker_dir)
            else:
                if self.sd.ref_rocker_dir is not None:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.sd.ref_rocker_dir.x, self.sd.ref_rocker_dir.z)
                else:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
                if self.sd.ref_effective_camera_rot:
                    forward = self.sd.ref_effective_camera_rot.get_forward()
                elif self.ev_g_is_agent():
                    forward = self.ev_g_forward()
                else:
                    forward = math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix).get_forward()
                self.set_model_forward(forward, max_lerp_duration, force=True)
            return

    def set_min_lerp_duration(self, duration=None):
        self.min_lerp_duration = self.default_min_lerp_duration if duration is None else duration
        return

    def set_mecha_free_sight_mode_default_enabled(self, flag):
        self.default_enabled = flag

    def refresh_mecha_free_sight_mode_enabled(self):
        self.enable_mecha_free_sight_mode(self.default_enabled)

    def delay_refresh_func(self):
        self.refresh_mecha_free_sight_mode_enabled()
        self.delay_refresh_timer = None
        return

    def delay_refresh_mecha_free_sight_mode_enabled(self, start_count_down, delay_time=1.0):
        if start_count_down:
            if self.delay_refresh_timer:
                global_data.game_mgr.get_logic_timer().set_interval(self.delay_refresh_timer, delay_time)
            else:
                self.delay_refresh_timer = global_data.game_mgr.register_logic_timer(self.delay_refresh_func, interval=delay_time, times=1, mode=CLOCK)
        elif self.delay_refresh_timer:
            global_data.game_mgr.unregister_logic_timer(self.delay_refresh_timer)
            self.delay_refresh_timer = None
        return

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar():
            self.regist_event('E_MOVE', self.on_move)
            self.regist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = True
            if self.mecha_id not in NATURALLY_ACTIVE_MECHA_ID_SET:
                return
            self.default_enabled = True
            self.enable_mecha_free_sight_mode(True)

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_MOVE', self.on_move)
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.sd.ref_mecha_free_sight_mode_enabled = False
            self.event_registered = False

    def on_exit_focus_camera(self):
        self.set_model_forward(self.scene.active_camera.rotation_matrix.forward, force=True)
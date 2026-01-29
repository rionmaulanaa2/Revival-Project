# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComFreeSight.py
from __future__ import absolute_import
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from common.utils.timer import RELEASE
from ....cdata.mecha_status_config import *
from math import fabs, pi
from logic.client.const.camera_const import FREE_MODEL, OBSERVE_FREE_MODE
from ..ComDataRenderRotate import YAW_MODE_LERP_HEAD
FREE_CAMERA_MODE = {
 FREE_MODEL, OBSERVE_FREE_MODE}
MAX_LERP_DURATION = 0.3
MIN_LERP_ANGLE = pi / 180 * 10
CIRCLE_ANGLE = pi * 2

class ComFreeSight(UnitCom):
    BIND_EVENT = {'E_ENABLE_MECHA_FREE_SIGHT_MODE': 'enable_mecha_free_sight_mode',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_SET_FORWARD_IN_FREE_SIGHT_MODE': 'set_model_forward'
       }

    def __init__(self):
        super(ComFreeSight, self).__init__()
        self.sd.ref_mecha_free_sight_mode_enabled = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComFreeSight, self).init_from_dict(unit_obj, bdict)
        self.cur_camera_state = None
        self.intrp_forward_timer = None
        self.delta_yaw = 0.0
        self.cur_lerp_duration = 0.0
        self.event_registered = False
        self.sd.ref_yaw = 0
        return

    def destroy(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_ROTATE', self.on_rotate)
            self.unregist_event('E_MOVE', self.on_move)
            self.event_registered = False
        super(ComFreeSight, self).destroy()

    def on_rotate(self, delta):
        if not self.sd.ref_mecha_free_sight_mode_enabled:
            return
        cur_states = self.ev_g_get_all_state()
        if MC_MOVE in cur_states or MC_RUN in cur_states or MC_JUMP_1 in cur_states or MC_JUMP_2 in cur_states:
            self.on_move(self.sd.ref_rocker_dir)

    def on_move(self, move_dir, *args):
        if not self.sd.ref_mecha_free_sight_mode_enabled:
            return
        if move_dir and not move_dir.is_zero:
            rot = self.sd.ref_effective_camera_rot or math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)
            forward = rot.rotate_vector(move_dir)
            forward.y = 0
            forward.normalize()
            self.set_model_forward(forward)

    def set_model_forward(self, target_forward, max_lerp_duration=MAX_LERP_DURATION, force=False):
        target_yaw = target_forward.yaw
        if target_yaw == self.sd.ref_logic_trans.yaw_target:
            return
        self.sd.ref_logic_trans.yaw_target = target_yaw
        yaw = target_yaw - self.sd.ref_rotatedata.yaw_head
        angle = fabs(yaw) % CIRCLE_ANGLE
        if angle < MIN_LERP_ANGLE and not force:
            return
        if angle > pi:
            angle = CIRCLE_ANGLE - angle
        if max_lerp_duration == 0.0:
            self.sd.ref_rotatedata.set_body_link_head()
            return
        cur_lerp_duration = max_lerp_duration * angle / pi
        self.sd.ref_common_motor.set_yaw_time(cur_lerp_duration)

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar():
            self.regist_event('E_ROTATE', self.on_rotate)
            self.regist_event('E_MOVE', self.on_move)
            self.event_registered = True
            self.enable_mecha_free_sight_mode(True)

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_ROTATE', self.on_rotate)
            self.unregist_event('E_MOVE', self.on_move)
            self.event_registered = False

    def enable_mecha_free_sight_mode(self, flag, max_lerp_duration=0.3):
        self.sd.ref_mecha_free_sight_mode_enabled = flag
        self.send_event('E_ENABLE_CAMERA_REFERENCE_MOVE', flag)
        self.send_event('E_DISABLE_ROCKER_ANIM_DIR', flag)
        if flag:
            self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 1)
        else:
            if self.sd.ref_rocker_dir is not None:
                self.send_event('E_CHANGE_ANIM_MOVE_DIR', self.sd.ref_rocker_dir.x, self.sd.ref_rocker_dir.z)
            else:
                self.send_event('E_CHANGE_ANIM_MOVE_DIR', 0, 0)
            rot = self.sd.ref_effective_camera_rot or math3d.matrix_to_rotation(self.scene.active_camera.rotation_matrix)
            self.set_model_forward(rot.get_forward(), max_lerp_duration=max_lerp_duration)
        return
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataRenderRotate.py
from __future__ import absolute_import
from __future__ import print_function
import cython_flag
from logic.gcommon.component.share.ComDataBase import ComDataBase
import math3d
import logic.gcommon.common_utils.bcast_utils as bcast
YAW_MODE_UNLINK_HEAD = 0
YAW_MODE_LINK_HEAD = 1
YAW_MODE_LERP_HEAD = 2
C_YAW_MODE_UNLINK_HEAD = YAW_MODE_UNLINK_HEAD
C_YAW_MODE_LINK_HEAD = YAW_MODE_LINK_HEAD
C_YAW_MODE_LERP_HEAD = YAW_MODE_LERP_HEAD
PITCH_MODE_LINK_ZERO = 0
PITCH_MODE_LERP_ZERO = 1
PITCH_MODE_LINK_HEAD = 2
PITCH_MODE_LERP_HEAD = 3
C_PITCH_MODE_LINK_ZERO = PITCH_MODE_LINK_ZERO
C_PITCH_MODE_LERP_ZERO = PITCH_MODE_LERP_ZERO
C_PITCH_MODE_LINK_HEAD = PITCH_MODE_LINK_HEAD
C_PITCH_MODE_LERP_HEAD = PITCH_MODE_LERP_HEAD

class ComDataRenderRotate(ComDataBase):
    BIND_EVENT = {'G_ROTATION': 'get_rot',
       'G_FORWARD': 'get_forward',
       'E_RESET_ROTATION': 'reset_rotation'
       }

    def __init__(self):
        super(ComDataRenderRotate, self).__init__()
        self.yaw_head = 0
        self.yaw_body = 0
        self.yaw_offset = 0
        self.yaw_body_mode = C_YAW_MODE_LINK_HEAD
        self.yaw_duration = 0
        self.yaw_lerp_factor = 0
        self.pitch_head = 0
        self.pitch_body = 0
        self.pitch_body_mode = C_PITCH_MODE_LINK_ZERO
        self.pitch_duration = 0
        self.pitch_lerp_factor = 0
        self.use_pitch_limit = False
        self.dirty = False
        self.force_turn_body = False
        self.use_quaternion = False
        self.rotation_mat = math3d.matrix.make_rotation_y(self.yaw_body + self.yaw_offset)
        self.rotation = math3d.matrix_to_rotation(self.rotation_mat)

    def get_share_data_name(self):
        return 'ref_rotatedata'

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataRenderRotate, self).init_from_dict(unit_obj, bdict)
        self.dirty = False

    def _do_cache(self):
        self.yaw_head = 0
        self.yaw_body = 0
        self.yaw_offset = 0
        self.yaw_body_mode = C_YAW_MODE_LINK_HEAD
        self.yaw_duration = 0
        self.pitch_body = 0
        self.pitch_body_mode = C_PITCH_MODE_LINK_ZERO
        self.use_quaternion = False
        self.dirty = False

    def activate_ecs(self):
        if not self._in_system:
            self.yaw_head = -0.01
        super(ComDataRenderRotate, self).activate_ecs()

    def mark_dirty(self):
        self.dirty = True

    def set_body_link_head(self):
        self.yaw_body_mode = C_YAW_MODE_LINK_HEAD

    def set_body_to_head(self, duration):
        self.yaw_duration = duration
        self.yaw_body_mode = C_YAW_MODE_LERP_HEAD
        self.yaw_lerp_factor = 0

    def set_body_unlink_head(self):
        if self.yaw_body_mode == C_YAW_MODE_LERP_HEAD:
            print('??? not valid?')
            return
        self.yaw_body_mode = C_YAW_MODE_UNLINK_HEAD

    def try_set_body_unlink_head(self):
        if self.yaw_body_mode == C_YAW_MODE_LINK_HEAD:
            self.yaw_body_mode = C_YAW_MODE_UNLINK_HEAD

    def try_set_body_link_head(self):
        if self.yaw_body_mode == C_YAW_MODE_UNLINK_HEAD:
            self.yaw_body_mode = C_YAW_MODE_LINK_HEAD

    def set_body_pitch_to_head(self, duration):
        if self.pitch_body_mode != C_PITCH_MODE_LINK_HEAD:
            self.pitch_body_mode = C_PITCH_MODE_LERP_HEAD
            self.pitch_duration = duration
            self.pitch_lerp_factor = 0

    def set_body_pitch_to_zero(self, duration):
        if self.pitch_body_mode != C_PITCH_MODE_LINK_ZERO:
            self.pitch_body_mode = C_PITCH_MODE_LERP_ZERO
            self.pitch_duration = duration
            self.pitch_lerp_factor = 0

    def set_use_pitch_limit(self, flag):
        self.use_pitch_limit = flag

    def get_rot(self):
        return self.rotation

    def get_forward(self):
        return self.rotation.get_forward()

    def get_yaw(self):
        return self.yaw_head

    def reset_rotation(self, lerp_time=0.2, use_inter_mode=False):
        if self._is_valid:
            self.sd.ref_logic_trans.yaw_offset = 0
            if self.yaw_head == self.yaw_body:
                return
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_RESET_ROTATION, (lerp_time,)], True)
            if lerp_time <= 0:
                self.send_event('E_TWIST_YAW', 0)
                self.set_body_link_head()
                self.send_event('E_ACTION_SYNC_FORCE_YAW', self.sd.ref_logic_trans.yaw_target)
                return
            self.set_body_to_head(lerp_time)
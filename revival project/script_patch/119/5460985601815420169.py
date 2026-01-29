# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataLogicTransform.py
from __future__ import absolute_import
from __future__ import print_function
import cython_flag
from logic.gcommon.component.share.ComDataBase import ComDataBase
import math3d
UNIT_Y = math3d.vector(0, 1, 0)

class ComDataLogicTransform(ComDataBase):
    BIND_EVENT = {'E_FORBID_ROTATION': 'use_quaternion_mode',
       'E_FORWARD': 'on_set_forward',
       'E_ROTATION': 'on_set_quaternion',
       'E_ROTATE_MODEL': 'deprecated_call',
       'E_TRANS_YAW': 'deprecated_call',
       'E_CHARACTER_ATTR': 'change_character_attr'
       }

    def __init__(self):
        super(ComDataLogicTransform, self).__init__()
        self.yaw_target = 0
        self.yaw_offset = 0
        self.pitch_target = 0
        self.pos_target = None
        self.force_turn_body = False
        self.quaternion = None
        self.use_quaternion = False
        self.logic_lod_level = 0
        self.logic_current_tick = 0
        return

    def get_share_data_name(self):
        return 'ref_logic_trans'

    def init_from_dict(self, unit_obj, bdict):
        super(ComDataLogicTransform, self).init_from_dict(unit_obj, bdict)
        keep_pitch = bdict.get('keep_pitch', False)
        self.yaw_target = self.unit_obj.get_value('G_ATTR_GET', 'human_yaw', 0) or 0
        self.pitch_target = self.unit_obj.get_value('G_ATTR_GET', 'head_pitch', 0) if keep_pitch else 0
        position = bdict.get('position', (0, 0, 0)) or (0, 0, 0)
        self.pos_target = math3d.vector(*position)

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            print(('test--ComDataLogicTransform--animator_info--yaw_target =', self.yaw_target, '--use_quaternion =', self.use_quaternion, '--ref_rotatedata.yaw_body =', self.sd.ref_rotatedata.yaw_body, '--ref_rotatedata.yaw_head =', self.sd.ref_rotatedata.yaw_head, '--yaw_offset =', self.yaw_offset, '--pitch_target =', self.pitch_target, '--pos_target =', self.pos_target, '--force_turn_body =', self.force_turn_body, '--id =', self.unit_obj.id, '--self.unit_obj =', self.unit_obj))
            model = self.ev_g_model()
            if not model:
                return
            model_rotation_matrix = model.world_rotation_matrix
            model_rot = math3d.matrix_to_rotation(model_rotation_matrix)
            print('test--ComDataLogicTransform--animator_info--', '--model_rot =', model_rot, '--mat.forward =', model_rotation_matrix.forward, '--model_rotation_matrix.forward =', model_rotation_matrix.forward, '--model_rotation_matrix.yaw =', model_rotation_matrix.yaw, '--self.unit_obj =', self.unit_obj)

    def _do_cache(self):
        self.yaw_target = 0
        self.pitch_target = 0

    def use_quaternion_mode(self, value):
        self.use_quaternion = value
        if not value:
            self.quaternion = None
        return

    def on_set_forward(self, forward, force=False, revert_up=False):
        if type(forward) in (list, tuple):
            forward = math3d.vector(forward[0], forward[1], forward[2])
        if forward.is_zero:
            return
        forward.normalize()
        if revert_up:
            right = forward.cross(-UNIT_Y)
        else:
            right = forward.cross(UNIT_Y)
        if right.is_zero:
            return
        right.normalize()
        up = right.cross(forward)
        up.normalize()
        if up.is_zero:
            return
        mat = math3d.matrix.make_orient(forward, up)
        quat = math3d.matrix_to_rotation(mat)
        self.quaternion = quat

    def on_set_quaternion(self, quat):
        self.quaternion = quat

    def deprecated_call(self, *args, **kwargs):
        pass
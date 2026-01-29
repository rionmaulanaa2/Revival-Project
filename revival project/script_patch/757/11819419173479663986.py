# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVETower.py
from __future__ import absolute_import
from six.moves import range
import world
import collision
import math3d
from common.cfg import confmgr
from SkillBase import SkillBase
from math import radians
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import robot_animation_const
from logic.gcommon.component.client.ComBaseWeaponLogic import ComBaseWeaponLogic
from mobile.common.IdManager import IdManager
from logic.gutils.mecha_utils import get_fire_end_posiiton
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path

class SkillPVETower(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVETower, self).__init__(skill_id, unit_obj, data)
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        self._ext_info = skill_conf.get('ext_info', None)
        if self._ext_info:
            self._throw_item_no = self._ext_info.get('item_type', None)
            self._fire_socket = self._ext_info.get('fire_socket', '')
            fire_yaw = self._ext_info.get('fire_yaw', [180])
            self._fire_yaw_rot = [ math3d.matrix.make_rotation_y(radians(yaw)) for yaw in fire_yaw ]
        return

    def _get_aim_target_id(self):
        target_id = None
        target = self._unit_obj.sd.ref_aim_target
        if target and (target.ev_g_bind_mecha_entity() or target.sd.ref_is_mecha):
            target_id = target.id
        return (target, target_id)

    def remote_do_skill(self, skill_data):
        fire_cnt = skill_data.get('fire_cnt', 1)
        for i in range(fire_cnt):
            model = self._unit_obj.ev_g_model()
            if model.has_socket(self._fire_socket):
                position = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD).translation
            else:
                position = model.position
            forward = self._unit_obj.ev_g_forward()
            yaw_rot = self._fire_yaw_rot[i if i < len(self._fire_yaw_rot) else 0]
            dir = forward * yaw_rot
            throw_item = {'item_itype': self._throw_item_no,
               'uniq_key': ExploderID.gen(global_data.battle_idx),
               'position': (
                          position.x, position.y, position.z),
               'm_position': (
                            position.x, position.y, position.z),
               'dir': (
                     dir.x, dir.y, dir.z),
               'up': (0, 1, 0),
               'use_rot_mat': 1
               }
            self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'do_skill', [self._skill_id, (throw_item, 0)], True)

    def cal_direction(self, forward):
        from math import radians, sin
        up_angle = confmgr.get('grenade_config', str(self._throw_item_no), 'fUpAngle', default=0)
        direction = forward
        if up_angle <= 0:
            return direction
        else:
            up = math3d.vector(0, 1, 0)
            right = direction.cross(up) * -1
            right.normalize()
            if direction.y > sin(radians(90 - up_angle)):
                direction = math3d.vector(0, 1, 0)
            else:
                mat = math3d.matrix.make_rotation(right, -radians(up_angle))
                direction = direction * mat
            return direction
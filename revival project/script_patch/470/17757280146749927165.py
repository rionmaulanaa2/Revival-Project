# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillKnightThrowable.py
from __future__ import absolute_import
import world
import collision
import math3d
from common.cfg import confmgr
from .SkillCd import SkillCd
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import robot_animation_const
from logic.gcommon.component.client.ComBaseWeaponLogic import ComBaseWeaponLogic
from logic.gutils.mecha_utils import get_fire_end_posiiton, get_camera_fire_pos
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path

class SkillKnightThrowable(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillKnightThrowable, self).__init__(skill_id, unit_obj, data)
        self._fSpeed = data.get('fSpeed', None)
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        self._ext_info = skill_conf.get('ext_info', None)
        if self._ext_info:
            self._throw_item_no = self._ext_info.get('item_type', None)
            self._fire_socket = self._ext_info.get('fire_socket', '')
        return

    def do_skill(self, stage, position, forward):
        up = math3d.vector(0, 1, 0)
        model = self._unit_obj.ev_g_model()
        position = get_camera_fire_pos(self._unit_obj.ev_g_position(), position, forward)
        info = confmgr.get('grenade_config', str(self._throw_item_no), 'cCustomParam', default={})
        if self._fire_socket:
            m_position = model.get_socket_matrix(self._fire_socket, world.SPACE_TYPE_WORLD).translation
            position = m_position
            end_pos = get_fire_end_posiiton(self._unit_obj)
            forward = end_pos - position
            if not forward.is_zero:
                forward.normalize()
                forward = self.cal_direction(forward)
        else:
            m_position = model.get_bone_matrix(robot_animation_const.BONE_HEAD_NAME, world.SPACE_TYPE_WORLD).translation
        m_position = m_position + forward * NEOX_UNIT_SCALE * 3
        socket = 'fx_jianqi_0{}'.format(stage)
        if 1 <= stage <= 3 and model.has_socket(socket):
            mat = model.get_socket_matrix(socket, world.SPACE_TYPE_WORLD)
            up = mat.rotation.up
        throw_item = {'item_itype': self._throw_item_no,
           'uniq_key': ExploderID.gen(global_data.battle_idx),
           'position': (
                      position.x, position.y, position.z),
           'm_position': (
                        m_position.x, m_position.y, m_position.z),
           'dir': (
                 forward.x, forward.y, forward.z),
           'up': (
                up.x, up.y, up.z),
           'use_rot_mat': 1,
           'col_width': info.get('energy_width', 6)
           }
        if self._fSpeed is not None and self._fSpeed > 0:
            throw_item['fSpeed'] = self._fSpeed
        if self._unit_obj.sd.ref_is_mecha:
            skin_id, shiny_weapon_id = self._unit_obj.ev_g_mecha_skin_and_shiny_weapon_id()
            if get_mecha_skin_grenade_weapon_sfx_path(skin_id, shiny_weapon_id, self._throw_item_no, 'cRes'):
                throw_item['skin_id'] = skin_id
                if shiny_weapon_id:
                    throw_item['shiny_weapon_id'] = shiny_weapon_id
        return (
         throw_item, stage)

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
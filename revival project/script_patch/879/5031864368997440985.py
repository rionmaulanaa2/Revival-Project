# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillOilBottle.py
from __future__ import absolute_import
import world
import collision
import math3d
import math
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.weapon_const import SHOOT_FROM_MUZZLE
from .SkillBase import SkillBase
from logic.gutils.mecha_utils import get_fire_end_posiiton
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gcommon import time_utility as tutil

class SkillOilBottle(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillOilBottle, self).__init__(skill_id, unit_obj, data)
        self._fSpeed = data.get('fSpeed', None)
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        self._ext_info = skill_conf.get('ext_info', None)
        self._cast_intv = 0
        if self._ext_info:
            self._throw_item_no = self._ext_info.get('item_type', None)
            self._fire_socket = self._ext_info.get('fire_socket', '')
            self._cast_intv = self._ext_info.get('cast_intv', 0)
        return

    def check_skill(self):
        now = tutil.time()
        if now - self._last_cast_time < self._cast_intv:
            return False
        self._last_cast_time = now
        return True

    def on_check_cast_skill(self):
        if not self.can_do_skill_in_water():
            return False
        if self._mp < self._cost_mp:
            return False
        if self._cost_fuel > 0:
            need_fuel = self._cost_fuel + self._cost_fuel_pre if self._cost_fuel_type == 1 else self._cost_fuel_pre
            if self.has_spec_fuel():
                now_fuel = self._unit_obj.ev_g_skill_fuel(self._skill_id)
            else:
                now_fuel = self._unit_obj.ev_g_fuel()
            if not now_fuel or now_fuel <= need_fuel:
                return False
        now = tutil.time()
        if now - self._last_cast_time < self._cast_intv:
            return False
        return True

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

    def do_skill(self, stage, position, cam_forward):
        up = math3d.vector(0, 1, 0)
        model = self._unit_obj.ev_g_model()
        info = confmgr.get('grenade_config', str(self._throw_item_no), 'cCustomParam', default={})
        ignore_fire_pos = confmgr.get('firearm_config', str(self._throw_item_no), 'iIgnoreFirePos')
        m_position = model.get_socket_matrix('fx_kaihuo02', world.SPACE_TYPE_WORLD).translation
        if ignore_fire_pos == SHOOT_FROM_MUZZLE:
            position = m_position
        else:
            position = position + cam_forward * 5 * NEOX_UNIT_SCALE
        end_pos = get_fire_end_posiiton(self._unit_obj)
        forward = end_pos - position
        fire_cam_pitch = math.degrees(cam_forward.pitch)
        first_contact_dis = forward.length
        if not forward.is_zero:
            forward.normalize()
            forward = self.cal_direction(forward)
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
           'bounces': info['bounces'],
           'fire_cam_pitch': fire_cam_pitch,
           'first_contact_dis': first_contact_dis
           }
        if self._unit_obj.sd.ref_is_mecha:
            fashion_id = self._unit_obj.ev_g_mecha_fashion_id()
            if fashion_id is not None:
                throw_item['fashion_id'] = fashion_id
        return (
         throw_item,)
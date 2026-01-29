# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEThrowable.py
from __future__ import absolute_import
import world
import math3d
from SkillBase import SkillBase
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.robot_animation_const import BONE_HEAD_NAME
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path

class SkillPVEThrowable(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEThrowable, self).__init__(skill_id, unit_obj, data)
        ext_info = confmgr.get('skill_conf', str(self._skill_id), 'ext_info', default={})
        self._throw_item_no = ext_info.get('item_type')

    def remote_do_skill(self, skill_data):
        self._unit_obj.send_event('E_DO_SKILL', self._skill_id)

    def do_skill(self):
        if not self._throw_item_no:
            return
        else:
            cam = world.get_active_scene().active_camera
            if not cam:
                return
            forward = cam.rotation_matrix.forward
            position = cam.position + forward * NEOX_UNIT_SCALE * 8
            up = math3d.vector(0, 1, 0)
            model = self._unit_obj.ev_g_model()
            info = confmgr.get('grenade_config', str(self._throw_item_no), 'cCustomParam', default={})
            m_position = self._unit_obj.ev_g_fired_pos()
            if m_position:
                position = m_position
            else:
                m_position = model.get_bone_matrix(BONE_HEAD_NAME, world.SPACE_TYPE_WORLD).translation
                m_position += forward * NEOX_UNIT_SCALE * 3
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
               'use_rot_mat': 1
               }
            if self._unit_obj.sd.ref_is_mecha:
                fashion_id = self._unit_obj.ev_g_mecha_fashion_id()
                if fashion_id is not None:
                    throw_item['fashion_id'] = fashion_id
                skin_id, shiny_weapon_id = self._unit_obj.ev_g_mecha_skin_and_shiny_weapon_id()
                if get_mecha_skin_grenade_weapon_sfx_path(skin_id, shiny_weapon_id, self._throw_item_no, 'cRes'):
                    throw_item['skin_id'] = skin_id
                    if shiny_weapon_id:
                        throw_item['shiny_weapon_id'] = shiny_weapon_id
            return (
             throw_item, 0)
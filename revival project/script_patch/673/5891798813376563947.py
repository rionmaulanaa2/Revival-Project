# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillBuild.py
from __future__ import absolute_import
from .SkillCd import SkillCd
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, WATER_MASK
import math3d
import collision
import world

class SkillBuild(SkillCd):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillBuild, self).__init__(skill_id, unit_obj, data)

    def do_skill(self, *args):
        skill_conf = confmgr.get('skill_conf', str(self._skill_id))
        ext_info = skill_conf.get('ext_info', {})
        building_id, max_distance = ext_info['building_id'], ext_info['max_distance'] * NEOX_UNIT_SCALE
        pos, rot = self.get_building_pos(max_distance)
        ext_param = {'rot': rot
           }
        return (
         building_id, pos, ext_param)

    def get_building_pos(self, max_distance):
        model = self._unit_obj.ev_g_model()
        start_pos = self._unit_obj.ev_g_position()
        end_pos = start_pos + model.rotation_matrix.forward * max_distance
        start_pos = math3d.vector(start_pos.x, start_pos.y + 6 * NEOX_UNIT_SCALE, start_pos.z)
        scene = world.get_active_scene()
        result = scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_CHARACTER_INCLUDE & ~WATER_MASK, collision.INCLUDE_FILTER)
        pos = result[1] or end_pos
        rot = math3d.matrix_to_rotation(model.rotation_matrix)
        return (
         (
          pos.x, pos.y, pos.z), (rot.x, rot.y, rot.z, rot.w))
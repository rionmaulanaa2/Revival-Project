# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillDash8032.py
from .SkillBase import SkillBase
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT, REGION_SCENE_GROUP
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision
import math3d
import world
from mobile.common.EntityManager import EntityManager
VALID_TARGET_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LPuppet', 'LPuppetRobot',
                                            'LMonster', 'LMechaTrans', 'LMotorcycle',
                                            'LPhotonTower', 'LLightShield', 'LExplosiveRobot'))

class SkillDash8032(SkillBase):

    def __init__(self, *args, **kwargs):
        super(SkillDash8032, self).__init__(*args, **kwargs)
        self.box_range = self._data.get('ext_info', {}).get('puncture_box_range', [5, 3, 100])

    def do_skill(self, *args):
        if not self._unit_obj:
            return
        dicts = {}
        state, stab_target = args
        dicts['target_ids'] = {stab_target: 0}
        return (
         state, dicts)

    def end_skill(self, *args):
        super(SkillDash8032, self).end_skill(*args)
        dicts = {}
        state, stab_target = args
        start_pos = self._unit_obj.ev_g_position()
        forward = self._unit_obj.ev_g_forward()
        forward.y = 0
        forward.normalize()
        scn = world.get_active_scene()
        col = collision.col_object(collision.BOX, math3d.vector(self.box_range[0] * NEOX_UNIT_SCALE, self.box_range[1] * NEOX_UNIT_SCALE, self.box_range[2] * NEOX_UNIT_SCALE), GROUP_DYNAMIC_SHOOTUNIT, GROUP_DYNAMIC_SHOOTUNIT)
        col.rotation_matrix = math3d.matrix.make_rotation_y(self._unit_obj.ev_g_yaw())
        col.position = start_pos + forward * (self.box_range[2] * NEOX_UNIT_SCALE) + math3d.vector(0, 50, 0)
        ret = scn.scene_col.static_test(col, -1, GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER) or []
        hit_cid = self._unit_obj.ev_g_human_base_col_id()
        self_cids = [col.cid, hit_cid]
        target_ids = {stab_target: 0}
        for hit_col in ret:
            if hit_col.cid in self_cids:
                continue
            if global_data.emgr.scene_is_shoot_obj.emit(hit_col.cid):
                res = global_data.emgr.scene_find_unit_event.emit(hit_col.cid)
                if res and res[0] and res[0].__class__.__name__ == 'LHouse':
                    continue
                if res and res[0] and res[0] != global_data.player.logic:
                    eid = res[0].id
                    if eid not in target_ids:
                        valid, dist = SkillDash8032.check_valid(eid, start_pos, scn)
                        if valid:
                            target_ids[eid] = dist

        dicts['target_ids'] = target_ids
        return (
         state, dicts)

    @staticmethod
    def check_valid(eid, trigger_pos, scn):
        target = EntityManager.getentity(eid)
        if target and target.logic and target.logic.MASK & VALID_TARGET_TAG_VALUE == 0:
            return (True, 0)
        if target and target.logic:
            pos = target.logic.ev_g_position()
            if not pos:
                return (True, 0)
            target_direction = pos - trigger_pos
            dist = target_direction.length
            start_pos = math3d.vector(pos.x, pos.y + NEOX_UNIT_SCALE, pos.z)
            end_pos = math3d.vector(trigger_pos.x, trigger_pos.y + 5 * NEOX_UNIT_SCALE, trigger_pos.z)
            model = target.logic.ev_g_model()
            if not model or not model.valid:
                return (True, 0)
            check_group = GROUP_STATIC_SHOOTUNIT | REGION_SCENE_GROUP
            result = scn.scene_col.hit_by_ray(start_pos, end_pos, 0, check_group, check_group, collision.INCLUDE_FILTER, True)
            if result[0]:
                for cobj in result[1]:
                    if cobj[4].cid in global_data.war_ignored_shoot_col:
                        continue
                    return (
                     False, 0)

            return (
             True, dist)
        return (True, 0)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVELightSpread.py
from __future__ import absolute_import
from .SkillPVEWeapon import SkillPVEWeapon
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const.idx_const import ExploderID
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.skill_const import SKILL_PVE_LIGHT_ICE_SPREAD
import world
import math3d

class SkillPVELightSpread(SkillPVEWeapon):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVELightSpread, self).__init__(skill_id, unit_obj, data)
        self.sub_index = 0

    def update_skill(self, data, trigger_update_event=True):
        super(SkillPVELightSpread, self).update_skill(data, trigger_update_event)

    def remote_do_skill(self, skill_data):
        print (
         'SkillPVELightSpread remote_do_skill', skill_data)
        if self.fire_cd > 0 and self.fire_cd >= tutil.time() - self.last_fire_end_ts:
            return
        gun_status_inf = self._unit_obj.ev_g_gun_status_inf(self._skill_id)
        if not gun_status_inf:
            return
        if self.fire_socket_follow_wp_pos:
            follow_status_inf = self._unit_obj.ev_g_gun_status_inf(self.fire_socket_follow_wp_pos)
            if follow_status_inf:
                gun_status_inf.set_socket_list([follow_status_inf.get_fired_socket_name()])
        duration = skill_data.get('duration', 0)
        if not self._weapon_pos:
            return
        self.destroy_timer()
        if not self.on_fire(skill_data):
            return
        if duration:
            self.timer_id = global_data.game_mgr.register_logic_timer(func=self.skill_end, times=1, mode=CLOCK, interval=duration)
        else:
            self.skill_end()

    def skill_end(self):
        self.destroy_timer()
        self.sub_index = 0
        if self.fire_cd > 0:
            self.last_fire_end_ts = tutil.time()

    def get_uniq_key(self):
        return ExploderID.gen(global_data.battle_idx)

    def on_fire(self, skill_data):
        if not self._unit_obj:
            return False
        fire_cnt = skill_data.get('fire_cnt', 0)
        from_entity = skill_data.get('from_entity')
        fire_pos = skill_data.get('fire_pos') or [0, -10000, 0]
        start_pos = math3d.vector(*fire_pos)
        if fire_cnt <= 0:
            return False
        target = EntityManager.getentity(from_entity)
        all_monster = []
        if target and target.logic:
            if target.logic.id == self._unit_obj.id:
                start_pos = self._unit_obj.ev_g_fired_pos()
                if not start_pos:
                    return False
                fire_pos = (
                 start_pos.x, start_pos.y, start_pos.z)
            else:
                model = target.logic.ev_g_model()
                if model:
                    mat = model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
                    if mat:
                        start_pos = mat.translation
                        fire_pos = (start_pos.x, start_pos.y, start_pos.z)
            all_monster = global_data.emgr.scene_get_hit_by_ray_enemy_monster_unit.emit(self._unit_obj, target.logic, start_pos)
        if not all_monster:
            return False
        fire_cnt = min(len(all_monster[0][0]), fire_cnt)
        if fire_cnt > 0 and self._skill_id == SKILL_PVE_LIGHT_ICE_SPREAD and target and target.logic:
            global_data.emgr.pve_element_reaction_event.emit(target.logic, 5290507)
        self.sub_index = 0
        for i in range(fire_cnt):
            self.sub_index += 1
            wp_type = self._unit_obj.ev_g_weapon_type(self._weapon_pos)
            wp_conf = confmgr.get('firearm_config', str(wp_type))
            wp_kind = wp_conf.get('iKind')
            direction = all_monster[0][0][i][1] - start_pos
            if not direction.is_zero:
                direction.normalize()
            throw_item = {'uniq_key': self.get_uniq_key(),'item_itype': wp_type,
               'item_kind': wp_kind,
               'position': fire_pos,
               'dir': (
                     direction.x, direction.y, direction.z),
               'sub_idx': self.sub_index,
               'wp_pos': self._weapon_pos,
               'client_extra': {'ignore_cobj_ids': all_monster[0][1]}}
            self._unit_obj.send_event('E_SHOOT_EXPLOSIVE_ITEM', throw_item, True)

        return True
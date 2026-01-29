# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/HuntingBattleData.py
from __future__ import absolute_import
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData, CBornData
import logic.gcommon.time_utility as tutil

class HuntingBattleData(DeathBattleData):

    def init_parameters(self):
        super(HuntingBattleData, self).init_parameters()
        self.is_in_base_part = False
        self.group_top_ui_status_dict = {}
        self.high_damage_entity_ids = []

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def check_pos(self):
        self.is_in_base_part = False

    def save_select_weapon_data(self, weapon_dict, cls_name):
        return False

    def get_last_choose_down_weapon(self):
        return []

    def get_last_choose_weapon(self, cls_name):
        return []

    def show_weapon_tips(self):
        parent_ui = global_data.ui_mgr.get_ui('WeaponBarSelectUI')
        if parent_ui and parent_ui.panel.nd_weapon_2:
            from logic.comsys.common_ui.CommonGuideTipsUI import CommonGuideTipsUI
            tips_ui = CommonGuideTipsUI()
            tips_ui.set_tips(17303)
            wpos = parent_ui.panel.nd_weapon_2.ConvertToWorldSpacePercentage(0, 50)
            wpos.x -= 40
            tips_ui.set_show_parent('WeaponBarSelectUI', wpos, 1.0)
            tips_ui.show_tips()

    def on_update_high_damage_tips(self, entity_ids, is_update):
        old_ids = self.high_damage_entity_ids
        self.high_damage_entity_ids = entity_ids
        if is_update:
            for eid in self.high_damage_entity_ids:
                if eid not in old_ids:
                    from mobile.common.EntityManager import EntityManager
                    ent = EntityManager.getentity(eid)
                    if ent and ent.logic:
                        global_data.game_mgr.show_tip(get_text_by_id(17304, {'name': ent.logic.ev_g_char_name()}))

        self.update_ui_high_damage_ids(entity_ids)

    def update_ui_high_damage_ids(self, entity_ids):
        if not global_data.ui_mgr.get_ui('EntityHeadMarkUI'):
            from logic.comsys.battle.Hunting.EntityHeadMarkUI import EntityHeadMarkUI
            EntityHeadMarkUI()
        ui = global_data.ui_mgr.get_ui('EntityHeadMarkUI')
        if ui:
            ui.update_entity_ids(entity_ids)
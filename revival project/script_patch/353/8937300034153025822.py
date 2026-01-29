# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/HuntingBattle.py
from __future__ import absolute_import
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const import battle_const
from mobile.common.EntityManager import EntityManager
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class HuntingBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        super(HuntingBattle, self).init_from_dict(bdict, is_change_weapon)
        self.mecha_group_id = bdict.get('mecha_group_id', 1)
        self.group_data = bdict.get('group_data', {})

    def is_mecha_group(self, gid):
        return gid == self.mecha_group_id

    @rpc_method(CLIENT_STUB, ())
    def show_fight_tips(self):
        self.on_show_fight_tips()

    def on_show_fight_tips(self):
        from logic.comsys.battle.Hunting.BattleStartHumanInfo import BattleStartHumanInfo, BattleStartMechaInfo
        if not global_data.battle.is_mecha_group(self.get_cur_target_group_id()):
            BattleStartHumanInfo()
        else:
            BattleStartMechaInfo()

    def get_cur_target_group_id(self):
        if global_data.player and global_data.player.logic:
            is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
            if not is_in_spectate:
                return global_data.player.logic.ev_g_group_id()
            if global_data.cam_lplayer:
                return global_data.cam_lplayer.ev_g_group_id()
        return None

    @rpc_method(CLIENT_STUB, (Float('final_prate'),))
    def final_stage(self, final_prate):
        pass

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        pass

    def get_need_preserve_group_sequence(self):
        if global_data.is_judge_ob:
            return True
        else:
            return False

    @rpc_method(CLIENT_STUB, (Dict('group_data'),))
    def show_group_data(self, group_data):
        pass

    def on_show_group_data(self, group_data):
        from logic.comsys.battle.Hunting.HuntingLoadingVsUI import HuntingLoadingVsUI
        ui = HuntingLoadingVsUI()
        ui.show_vs(group_data)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), Dict('selected_combat_weapons'), Dict('group_point_dict')))
    def update_battle_data(self, settle_timestamp, selected_combat_weapons, group_point_dict):
        self.update_settle_timestamp((settle_timestamp,))
        if selected_combat_weapons:
            global_data.death_battle_data.set_select_weapon_data(selected_combat_weapons)
        global_data.death_battle_data and global_data.death_battle_data.update_group_score_data(group_point_dict)

    def is_operable(self):
        battle = global_data.player.get_battle()
        if battle and battle.is_battle_prepare_stage():
            return False
        return True

    def can_move(self):
        return self.is_operable()

    def can_fire(self):
        return self.is_operable()

    def can_roll(self):
        return self.is_operable()

    def can_lens_aim(self):
        return self.is_operable()

    @rpc_method(CLIENT_STUB, (Dict('killer_info'), Float('revive_time')))
    def on_mecha_destroy(self, killer_info, revive_time):
        global_data.emgr.playback_mecha_destroyed.emit(killer_info, revive_time)

    @rpc_method(CLIENT_STUB, (List('entity_ids'), Int('is_update')))
    def high_damage_tips(self, entity_ids, is_update):
        global_data.death_battle_data and global_data.death_battle_data.on_update_high_damage_tips(entity_ids, is_update)

    @rpc_method(CLIENT_STUB, ())
    def weapon_upgrade_tips(self):
        global_data.death_battle_data and global_data.death_battle_data.show_weapon_tips()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ScavengeBattle.py
from __future__ import absolute_import
from logic.entities.DeathBattle import DeathBattle
from logic.entities.Battle import Battle
from logic.gutils import item_utils
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool

class ScavengeBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        self.area_id = bdict.get('area_id')
        super(ScavengeBattle, self).init_from_dict(bdict, is_change_weapon)
        self.init_guide_locate = bdict.get('sp_item_pos_dict', {})

    def can_move(self):
        if self._battle_status == Battle.BATTLE_STATUS_FIGHT:
            return True
        return False

    def can_roll(self):
        if self._battle_status == Battle.BATTLE_STATUS_FIGHT:
            return True
        return False

    @rpc_method(CLIENT_STUB, (Int('item_id'), Uuid('player_eid')))
    def show_weapon_picked(self, item_id, player_eid):
        global_data.emgr.show_weapon_picked.emit(item_id, player_eid)

    @rpc_method(CLIENT_STUB, (Int('item_id'),))
    def show_item_refreshed(self, item_id):
        global_data.emgr.show_item_refreshed.emit(item_id)

    @rpc_method(CLIENT_STUB, (Dict('sp_item_pos_dict'),))
    def server_update_scavenge_sp_item_data(self, sp_item_pos_dict):
        global_data.death_battle_data and global_data.death_battle_data.update_sp_item_data(sp_item_pos_dict)

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.death_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])
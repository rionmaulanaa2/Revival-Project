# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/CrystalBattle.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.entities.DeathBattle import DeathBattle

class CrystalBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        super(CrystalBattle, self).init_from_dict(bdict, is_change_weapon)
        self.crystal_max_hp = bdict.get('crystal_max_hp', 1)
        self.group_mark_dict = bdict.get('group_mark_dict', {})
        self.crystal_cover_dict = bdict.get('crystal_cover_dict', {})
        self.group_round = bdict.get('group_round', {})
        self.group_crystal_points_dict = bdict.get('group_crystal_points_dict', {})

    @rpc_method(CLIENT_STUB, (Dict('group_crystal_damage_dict'),))
    def update_group_crystal_damage(self, group_crystal_damage_dict):
        if not global_data.death_battle_data:
            return
        global_data.death_battle_data.update_group_crystal_damage(group_crystal_damage_dict)

    @rpc_method(CLIENT_STUB, (Dict('group_round'),))
    def update_group_round(self, group_round):
        self.group_round = group_round

    @rpc_method(CLIENT_STUB, (Dict('group_crystal_damage_dict'),))
    def update_group_crystal_points(self, group_crystal_damage_dict):
        self.group_crystal_points_dict = group_crystal_damage_dict
        global_data.emgr.update_crystal_points_event.emit(group_crystal_damage_dict)

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        pass

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        super(CrystalBattle, self).fight_stage(stage_dict)
        self.add_crystal_mark(self.group_mark_dict)

    def add_crystal_mark(self, group_mark_dict):
        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(group_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

    @rpc_method(CLIENT_STUB, ())
    def crystal_hit_hint(self):
        global_data.emgr.show_crystal_hit_hint_event.emit()

    @rpc_method(CLIENT_STUB, (Int('crystal_group_id'),))
    def crystal_destroy_hint(self, crystal_group_id):
        global_data.emgr.show_crystal_destroy_hint_event.emit(crystal_group_id)

    @rpc_method(CLIENT_STUB, (Int('crystal_group_id'), Int('crystal_round')))
    def crystal_die_hint(self, crystal_group_id, crystal_round):
        global_data.emgr.show_crystal_die_hint_event.emit(crystal_group_id, crystal_round)

    def get_crystal_max_hp(self):
        return self.crystal_max_hp

    def get_crystal_cover_dict(self):
        return self.crystal_cover_dict

    def get_group_round(self):
        return self.group_round

    def get_group_crystal_points(self):
        return self.group_crystal_points_dict
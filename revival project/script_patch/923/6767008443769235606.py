# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ControlBattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.entities.DeathBattle import DeathBattle

class ControlBattle(DeathBattle):

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), List('born_point_list'), Dict('group_born_dict'), Dict('control_point_dict'), Dict('group_points_dict'), Dict('selected_combat_weapons')))
    def update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, control_point_dict, group_points_dict, selected_combat_weapons):
        self._update_battle_data(settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons)
        self.update_control_point((control_point_dict,))

    @rpc_method(CLIENT_STUB, (Dict('control_point_dict'),))
    def update_control_point(self, control_point_dict):
        global_data.death_battle_data and global_data.death_battle_data.update_control_point(control_point_dict)

    @rpc_method(CLIENT_STUB, (Dict('group_points_dict'),))
    def update_group_points(self, group_points_dict):
        global_data.death_battle_data and global_data.death_battle_data.update_group_score_data(group_points_dict)

    @rpc_method(CLIENT_STUB, (List('point_pos'), Float('delay_time')))
    def notify_control_point(self, point_pos, delay_time):
        ui = global_data.ui_mgr.show_ui('OccupyBattleTips', 'logic.comsys.battle.Occupy')
        ui.start_move(point_pos, delay_time)
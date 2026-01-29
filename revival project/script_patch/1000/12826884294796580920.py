# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/PointsBattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.entities.Battle import Battle

class PointsBattle(Battle):

    @rpc_method(CLIENT_STUB, (Int('group_points'),))
    def calculate_group_rank(self, group_points):
        ui_obj = global_data.ui_mgr.get_ui('RankBeginUI')
        ui_obj and ui_obj.set_data(group_points)

    @rpc_method(CLIENT_STUB, (Float('next_stage_timestamp'), List('elimination_data'), Int('first_score'), List('rank_data')))
    def update_group_rank(self, next_stage_timestamp, elimination_data, first_score, rank_data):
        if not rank_data:
            return
        if global_data.ui_mgr.get_ui('RankBeginUI'):
            global_data.ui_mgr.close_ui('RankBeginUI')
        ui_obj = global_data.ui_mgr.show_ui('BriefRankUI', 'logic.comsys.battle.Rank')
        ui_obj and ui_obj.refresh_listview(next_stage_timestamp, elimination_data, first_score, rank_data)
        global_data.score_battle_rank_data.set_brief_rank_data(elimination_data, rank_data)

    def request_rank(self, start_rank, end_rank):
        self.call_soul_method('request_rank', (start_rank, end_rank))

    @rpc_method(CLIENT_STUB, (Int('start_rank'), Int('rank_len'), List('rank_data'), List('group_data')))
    def reply_rank(self, start_rank, rank_len, rank_data, group_data):
        ui_obj = global_data.ui_mgr.get_ui('RankListUI')
        if ui_obj:
            data = (
             start_rank, rank_len, rank_data, group_data)
            ui_obj.set_group_data(0, data)

    def request_group_data(self):
        self.call_soul_method('request_group_data')

    @rpc_method(CLIENT_STUB, (Int('group_rank'), Int('group_points'), Int('next_stage_timestamp'), Dict('group_data')))
    def reply_group_data(self, group_rank, group_points, next_stage_timestamp, group_data):
        ui_obj = global_data.ui_mgr.get_ui('RankListUI')
        if ui_obj:
            ui_obj.set_group_data(1, group_data)

    @rpc_method(CLIENT_STUB, (Int('group_num'), Dict('settle_dict'), Dict('team_dict'), Dict('achivement')))
    def settle_stage(self, group_num, settle_dict, team_dict, achivement):
        self.is_settle = True

        def _cb():
            super(PointsBattle, self).settle_stage((group_num, settle_dict, team_dict))

        rank = settle_dict['rank']
        global_data.ui_mgr.close_ui('KnockoutUI')
        if rank > 3:
            ui_obj = global_data.ui_mgr.show_ui('KnockoutUI', 'logic.comsys.battle')
            if ui_obj:
                ui_obj.on_delay_close(_cb)
            else:
                _cb()
        else:
            _cb()

    def request_enemy_data(self):
        self.call_soul_method('request_enemy_data')

    @rpc_method(CLIENT_STUB, (List('enemy_data'),))
    def reply_enemy_data(self, enemy_data):
        import math3d
        pos_lst = []
        for pos in enemy_data:
            x, y, z = pos
            pos_lst.append(math3d.vector(x, y, z))

        global_data.emgr.scene_enemy_mark.emit(pos_lst)
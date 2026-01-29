# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBattleSeason.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gcommon import time_utility as tutil

class impBattleSeason(object):

    def _init_battleseason_from_dict(self, bdict):
        self.battle_season = bdict.get('battle_season', 1)
        self.last_season_report = bdict.get('season_report', {})
        self.season_week_no = bdict.get('season_week_no', 0)
        self.history_season_ids = bdict.get('history_season_ids', [])
        self.kill_rank_cnt = bdict.get('kill_rank_cnt', {})
        self.kill_rank_reward_record = bdict.get('kill_rank_reward_record', [])
        self.rushing_rank_type = bdict.get('rushing_rank_type', None)
        self.season_stat = bdict.get('season_stat', {})
        self.rush_rank_task = bdict.get('rush_rank_task', None)
        return

    def _destroy_battleseason(self):
        global_data.max_season_mem_show_index = None
        return

    def get_battle_season(self):
        return self.battle_season

    def get_cur_season_week_no(self):
        return self.season_week_no

    def get_last_season_report(self):
        return self.last_season_report

    @rpc_method(CLIENT_STUB, (Int('season'), Int('week')))
    def start_new_season(self, season, week):
        self.battle_season = season
        self.season_week_no = week
        self.kill_rank_cnt = {}
        self.kill_rank_reward_record = {}
        self.rushing_rank_type = None
        global_data.emgr.start_new_season_event.emit()
        return

    @rpc_method(CLIENT_STUB, (Int('week'),))
    def start_new_season_week(self, week):
        self.season_week_no = week
        global_data.emgr.start_new_season_week_event.emit()

    @rpc_method(CLIENT_STUB, (List('history_season_ids'),))
    def season_history_id_change(self, history_season_ids):
        self.history_season_ids = history_season_ids

    def receive_rush_rank_reward(self, rank_type):
        if self.receive_rush_rank_reward.get(rank_type):
            return
        self.call_server_method('receive_rush_rank_reward', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'),))
    def receive_rush_rank_reward_ret(self, rank_type):
        self.receive_rush_rank_reward[rank_type] = 1

    def choose_season_rushing_rank_type(self, rushing_rank_type):
        self.call_server_method('choose_season_rush_rank_type', (rushing_rank_type,))
        self.rushing_rank_type = rushing_rank_type

    def choose_season_rush_rank_task(self, task_id):
        self.call_server_method('choose_season_rush_rank_task', (task_id,))
        self.rush_rank_task = task_id

    def get_rushing_rank_type(self):
        return self.rushing_rank_type
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impClanRank.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Int, List, Dict
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_const import rank_const
from logic.gcommon import time_utility as tutil

class impClanRank(object):

    def _init_clanrank_from_dict(self, bdict):
        self.clan_rank_reward_dict = bdict.get('clan_rank_reward_dict', {})

    def request_clan_rank_list(self, rank_type, start_rank, end_rank, include_self=False):
        self.call_server_method('request_clan_rank_list', (rank_type, start_rank, end_rank, include_self))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), List('rank_list_data')))
    def respon_clan_rank_list(self, rank_type, rank_list_data):
        if not rank_list_data:
            none_d = rank_const.RANK_DATA_NONE
            rank_list_data = [0, 0, 0, [], none_d, [none_d, none_d, none_d, none_d, none_d]]
        if len(rank_list_data) == 4:
            start_rank, end_rank, rank_version, rank_list = rank_list_data
            rank = None
            data = None
        else:
            start_rank, end_rank, rank_version, rank_list, rank, data = rank_list_data
        global_data.message_data.set_rank_data(rank_type, start_rank, end_rank, rank_version, rank_list, rank, data)
        global_data.emgr.clan_rank_data.emit(rank_type, start_rank, end_rank, rank_version, rank_list, rank, data)
        return

    def is_offer_clan_rank_reward(self, rank_type):
        if rank_type == rank_const.RANK_TYPE_CLAN_WEEK_POINT:
            reward_idx = tutil.get_rela_week_no() - 1
        elif rank_type == rank_const.RANK_TYPE_CLAN_SEASON_POINT:
            reward_idx = self.get_battle_season() - 1
        else:
            return True
        return reward_idx <= self.clan_rank_reward_dict.get(rank_type, -1)

    def request_offer_clan_rank_reward(self, rank_type):
        if self.clan_rank_reward_dict.get(rank_type, False):
            return
        self.call_server_method('request_offer_clan_rank_reward', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Int('reward_idx')))
    def update_clan_rank_reward(self, rank_type, reward_idx):
        self.clan_rank_reward_dict[rank_type] = reward_idx
        global_data.emgr.clan_rank_reward.emit()

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Int('reward_idx'), Int('rank'), Int('rank_percent'), Dict('reward_dict')))
    def respon_offer_clan_rank_reward(self, rank_type, reward_idx, rank, rank_percent, reward_dict):
        self.clan_rank_reward_dict[rank_type] = reward_idx
        global_data.emgr.clan_rank_reward.emit()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFABattleData.py
from __future__ import absolute_import
import six
from common.framework import Singleton

class FFABattleData(Singleton):
    ALIAS_NAME = 'ffa_battle_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.settle_timestamp = None
        self.rank_data = None
        self.group_rank_data = None
        self.top_group_info = None
        self.spawn_rebirth_dict = {}
        return

    def on_finalize(self):
        self.init_parameters()

    def set_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.emgr.update_battle_timestamp.emit(settle_timestamp)

    def set_group_score_data(self, group_rank_data):
        self.group_rank_data = group_rank_data
        global_data.emgr.update_group_score_data.emit(group_rank_data)

    def get_group_score_data(self):
        return self.group_rank_data

    def set_score_details_data(self, rank_data):
        self.rank_data = rank_data
        global_data.emgr.update_score_details.emit(rank_data)

    def get_score_details_data(self):
        return self.rank_data

    def notify_top_group_info(self, group_id, soul_data):
        self.top_group_info = (
         group_id, soul_data)
        global_data.emgr.update_top_group_info.emit(group_id, soul_data)

    def is_top_1(self, player_eid):
        if self.top_group_info:
            return player_eid in self.top_group_info[1]
        return False

    def update_spawn_rebirth_data(self, data):
        for key in six.iterkeys(data):
            self.spawn_rebirth_dict[key] = data[key]

    def get_spawn_rebirth_data(self, spwan_id):
        return self.spawn_rebirth_dict.get(spwan_id, [0, 0])
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmRace/ArmRaceBattleData.py
from __future__ import absolute_import
from common.framework import Singleton

class ArmRaceBattleData(Singleton):
    ALIAS_NAME = 'armrace_battle_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.settle_timestamp = None
        self.rank_data = None
        self.group_rank_data = None
        self.top_group_info = None
        self.armrace_level = 1
        self.now_level_kill = 0
        return

    def on_finalize(self):
        self.init_parameters()

    def set_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.emgr.update_battle_timestamp.emit(settle_timestamp)

    def set_group_score_data(self, group_rank_data):
        self.group_rank_data = group_rank_data
        global_data.emgr.update_group_score_data.emit(group_rank_data)

    def set_armrace_level(self, level, now_level_kill, level_up):
        self.armrace_level = level
        self.now_level_kill = now_level_kill
        global_data.emgr.update_armrace_level_kill.emit(level, now_level_kill, level_up)

    def get_armrace_level(self):
        return self.armrace_level

    def get_now_level_kill(self):
        return self.now_level_kill

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

    def is_operable(self):
        battle = global_data.player.get_battle()
        if battle and battle.is_battle_prepare_stage():
            return False
        return True
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/RandomDeath/DeathBattleData.py
from __future__ import absolute_import
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
import logic.gcommon.time_utility as tutil

class RandomDeathBattleData(DeathBattleData):

    def init_parameters(self):
        super(RandomDeathBattleData, self).init_parameters()
        self.item_lost_time = 0
        self.random_death_mecha_call = []
        self.random_death_weapon_list = []

    def set_mecha_list(self, mecha_list):
        self.random_death_mecha_call = mecha_list
        global_data.emgr.update_random_mecha_list.emit()

    def get_mecha_is_enable(self, mecha_id):
        return mecha_id in self.random_death_mecha_call

    def get_mecha_list(self):
        return self.random_death_mecha_call

    def get_weapon_list(self):
        return self.random_death_weapon_list

    def set_item_lost_time(self, item_lost_time):
        self.item_lost_time = item_lost_time
        global_data.emgr.update_item_lost_time.emit()

    def get_item_lost_time(self):
        return self.item_lost_time
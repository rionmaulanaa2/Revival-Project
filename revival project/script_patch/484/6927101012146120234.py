# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFABattleData.py
from __future__ import absolute_import
import six
from common.framework import Singleton

class ZombieFFABattleData(Singleton):
    ALIAS_NAME = 'zombieffa_battle_data'

    def init(self):
        self.settle_timestamp = 0
        self.group_rank_data = None
        self.score_details_data = None
        self.top_group_info = None
        self.camp_status = []
        self.spawn_rebirth_dict = {}
        return

    def set_settle_timestamp(self, timestamp):
        self.settle_timestamp = timestamp
        global_data.emgr.update_battle_timestamp.emit(timestamp)

    def set_group_rank_data(self, group_rank_data):
        self.group_rank_data = group_rank_data
        global_data.emgr.update_group_score_data.emit(group_rank_data)

    def get_group_score_data(self):
        return self.group_rank_data

    def set_score_details_data(self, score_details):
        self.score_details_data = score_details
        global_data.emgr.zombieffa_update_socre_details.emit(score_details)

    def get_score_details_data(self):
        return self.score_details_data

    def notify_top_group_info(self, group_id, soul_data):
        self.top_group_info = (
         group_id, soul_data)
        global_data.emgr.update_top_group_info.emit(group_id, soul_data)

    def is_top_1(self, player_eid):
        if self.top_group_info:
            return player_eid in self.top_group_info[1]
        return False

    def update_camp_status(self, camp_status):
        battle = global_data.battle
        player = global_data.player
        if not battle or not player:
            return
        entity_camp_status = []
        for aoi_id, (posx, posz), is_in_mecha in camp_status:
            entity = battle.get_entity_by_aoi_id(aoi_id)
            exclude_uids = (player.uid, player.get_global_spectate_player_uid())
            if entity and entity.uid not in exclude_uids:
                entity_camp_status.append((entity.id, (posx, posz), is_in_mecha))

        self.camp_status = entity_camp_status
        global_data.emgr.zombieffa_update_camp_status.emit()

    def get_camp_status(self):
        return self.camp_status

    def update_spawn_rebirth_data(self, data):
        for key in six.iterkeys(data):
            self.spawn_rebirth_dict[key] = data[key]

    def get_spawn_rebirth_data(self, spwan_id):
        return self.spawn_rebirth_dict.get(spwan_id, [0, 0])
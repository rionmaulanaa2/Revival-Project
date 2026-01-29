# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeData.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from common.cfg import confmgr

class ScavengeData(DeathBattleData):

    def init_parameters(self):
        super(ScavengeData, self).init_parameters()
        self.spawn_info = {}
        self.sp_item_data = {}
        self.hyper_spawn_data = {}

    def update_spawn_rebirth_data(self, data):
        for key in six.iterkeys(data):
            self.spawn_rebirth_dict[key] = data[key]

        global_data.emgr.update_scavenge_item_locate_ui.emit()

    def get_hyper_rebirth_data(self):
        for key, value in six.iteritems(self.spawn_rebirth_dict):
            item_info = self.spawn_info.get(key, {})
            item_id = item_info.get('item_id')
            item_level = confmgr.get('item', str(item_id), 'iQuality')
            self.hyper_spawn_data[key] = value

        return self.hyper_spawn_data

    def save_select_weapon_data(self, weapon_dict, cls_name):
        return False

    def update_sp_item_data(self, sp_item_pos_dict):
        self.sp_item_data = sp_item_pos_dict
        global_data.emgr.update_scavenge_sp_item_guide_ui.emit()

    def on_finalize(self):
        super(ScavengeData, self).on_finalize()
        self.spawn_info = {}
        self.sp_item_data = {}
        self.hyper_spawn_data = {}

    def is_operable(self):
        from logic.gcommon.time_utility import get_server_time_battle
        cur_time = get_server_time_battle()
        if self.round_ready_ts and cur_time < self.round_ready_ts or self.round_end_ts and cur_time > self.round_end_ts:
            return False
        return True
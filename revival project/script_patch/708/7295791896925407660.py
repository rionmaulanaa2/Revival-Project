# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag/FlagBattleData.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
import logic.gcommon.time_utility as tutil

class FlagBattleData(DeathBattleData):

    def init_parameters(self):
        super(FlagBattleData, self).init_parameters()
        self.faction_to_flag_base_id = None
        self.flag_ent_id = None
        self.flag_reset_start_time = None
        self.flag_lock_start_time = None
        self.flag_refresh_time = None
        self.flag_faction = None
        self.picker_id = None
        self.born_range_data = global_data.game_mode.get_cfg_data('born_range_data')
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_flag_recover': self.on_flag_recover,
           'flagsnatch_flag_pick_up': self.on_flag_pick_up
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_flag_recover(self, *args):
        self.flag_faction = None
        self.picker_id = None
        return

    def on_flag_pick_up(self, picker_id, picker_faction, **args):
        self.picker_id = picker_id
        self.flag_faction = picker_faction

    def update_flag_base_info(self, flag_base_info):
        self.faction_to_flag_base_id = flag_base_info

    def set_flag_ent_id(self, eid):
        self.flag_ent_id = eid

    def set_flag_reset_start_time(self, reset_start_time):
        self.flag_reset_start_time = reset_start_time

    def set_flag_lock_start_time(self, flag_lock_time):
        self.flag_lock_start_time = flag_lock_time

    def set_flag_refresh_time(self, refresh_time):
        self.flag_refresh_time = refresh_time

    def set_flag_lock_time(self, lock_time):
        self.flag_lock_time = lock_time

    def set_flag_faciton(self, faction):
        self.flag_faction = faction

    def get_flag_ent(self):
        return global_data.battle.get_entity(self.flag_ent_id)

    def get_flag_base_ent_by_faction(self, faction):
        if not self.faction_to_flag_base_id:
            return None
        else:
            base_id = self.faction_to_flag_base_id.get(faction)
            return global_data.battle.get_entity(base_id)

    def get_flag_faction(self):
        return self.flag_faction

    def get_my_born_data(self):
        my_group_id = self.get_player_group_id()
        if my_group_id in self.born_data:
            return self.born_data[my_group_id]

    def pos_in_base_part(self, pos):
        if global_data.game_mode.mode and global_data.game_mode.mode.game_over:
            return False
        if not (global_data.player and global_data.player.logic):
            return False
        if not pos:
            return False
        born_data_op = global_data.game_mode.get_born_data()
        if self.area_id not in born_data_op:
            return False
        range_ids = born_data_op[self.area_id].get('c_range')
        if not range_ids:
            return False
        for group_id in six.iterkeys(self.born_data):
            born_data = self.born_data[group_id]
            _x, _y, _z, _r, _idx, _ = born_data.data
            tmp_born_range_data = self.born_range_data.get(str(range_ids[_idx]), {})
            y_range = tmp_born_range_data.get('y_range')
            if not y_range:
                return False
            if pos.y < _y + y_range[0] or pos.y > _y + y_range[1]:
                return False
            pos_lst = tmp_born_range_data.get('pos_lst_drop', [])
            if pnpoly(len(pos_lst), pos_lst, (pos.x, pos.z)):
                return True

        return False
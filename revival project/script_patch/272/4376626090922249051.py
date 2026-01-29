# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2BattleData.py
from __future__ import absolute_import
import six
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly

class Flag2BattleData(DeathBattleData):

    def init_parameters(self):
        super(Flag2BattleData, self).init_parameters()
        self.faction_to_flag_base_id = None
        self.flag_ent_id = None
        self.flag_ent_id_dict = None
        self.flag_reset_start_time = {}
        self.flag_lock_start_time = {}
        self.flag_refresh_time = None
        self.flag_drop_refresh_time = None
        self.flag_lock_time = 5
        self.flag_first_lock_time = 15
        self.picker_id_dict = {}
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

    def on_flag_recover(self, holder_id, holder_faction, reason):
        self.picker_id = None
        self.picker_id_dict[holder_faction] = None
        return

    def on_flag_pick_up(self, picker_id, picker_faction, **args):
        self.picker_id_dict[picker_faction] = picker_id

    def update_flag_base_info(self, flag_base_info):
        self.faction_to_flag_base_id = flag_base_info

    def set_flag_ent_id_dict(self, eid_dict):
        self.flag_ent_id_dict = eid_dict

    def set_flag_reset_start_time(self, reset_start_time, faction_id):
        self.flag_reset_start_time[faction_id] = reset_start_time

    def set_flag_lock_start_time(self, flag_lock_time, faction_id):
        self.flag_lock_start_time[faction_id] = flag_lock_time

    def set_flag_refresh_time(self, refresh_time):
        self.flag_refresh_time = refresh_time

    def set_flag_drop_refresh_time(self, refresh_time):
        self.flag_drop_refresh_time = refresh_time

    def set_flag_lock_time(self, lock_time):
        self.flag_lock_time = lock_time

    def set_flag_first_lock_time(self, lock_time):
        self.flag_first_lock_time = lock_time

    def get_flag_base_ent_by_faction(self, faction):
        if not self.faction_to_flag_base_id:
            return None
        else:
            base_id = self.faction_to_flag_base_id.get(faction)
            return global_data.battle.get_entity(base_id)

    def get_flag_ent_by_faction(self, faction):
        if not self.flag_ent_id_dict:
            return None
        else:
            flag_ent_id = self.flag_ent_id_dict[faction]
            return global_data.battle.get_entity(flag_ent_id)

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

    def set_flag_faciton(self, faction):
        self.flag_faction = faction
        self.flag_ent_id = self.flag_ent_id_dict.get(faction, None)
        return

    def get_flag_faction(self):
        return self.flag_faction

    def get_flag_ent(self, group_id=1):
        return global_data.battle.get_entity(self.flag_ent_id_dict.get(group_id, None))
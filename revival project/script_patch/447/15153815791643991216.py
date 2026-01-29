# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathBattleData.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from logic.client.const import game_mode_const
from common.utils import timer
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
from logic.comsys.archive import archive_key_const
from logic.gcommon import const
from collections import defaultdict
SWIM_UI_LIST = [
 'FireRockerUI', 'PostureControlUI', 'BattleControlUIPC', 'ThrowRockerUI', 'BulletReloadUI']

class CBornData(object):

    def __init__(self, group_id):
        self.group_id = group_id
        self.init_parameters()

    def init_parameters(self):
        self.data = None
        group_id = None
        if global_data.player and global_data.player.logic:
            group_id = global_data.player.logic.ev_g_group_id()
        elif global_data.battle:
            group_id = global_data.battle.get_loading_group_id()
        self.side = self.get_side(group_id)
        return

    def set_data(self, data):
        self.data = data

    def get_side(self, compared_group_id):
        if self.group_id:
            side = game_mode_const.MY_SIDE if self.group_id == compared_group_id else game_mode_const.E_ONE_SIDE
        else:
            side = game_mode_const.NONE_SIDE
        return side


class DeathBattleData(Singleton):
    ALIAS_NAME = 'death_battle_data'

    def init(self):
        self.init_parameters()
        self.process_event(True)

    def init_parameters(self):
        self.is_ready_state = True
        self.is_in_base_part = False
        self.check_pos_timer = None
        self.my_born_range_data = {}
        self.born_data = {}
        self.temp_born_point_key = []
        self.weapon_dict = {}
        self.settle_timestamp = None
        self.group_status_dict = {}
        self.show_status_dict = {}
        self.score_details_dict = {}
        self.group_score_dict = {}
        self.area_id = None
        self.spawn_rebirth_dict = {}
        self.rogue_gift_candidates = {}
        self.selected_rogue_gifts = defaultdict(dict)
        self.rogue_distribute_times = []
        self.enable_out_base_rogue = False
        self.refresh_conf_list = None
        self.rogue_refresh_times = defaultdict(int)
        self.max_refresh_time = None
        self.partner_voice_state = {}
        self.partner_text_state = {}
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_scene_observed_player_setted(self, player):
        pass

    def on_finalize(self):
        self.check_pos_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_pos_timer)
        self.init_parameters()
        self.process_event(False)

    def get_is_in_base_part(self):
        return self.is_in_base_part

    def get_player_group_id(self):
        if global_data.player and global_data.player.logic:
            return global_data.player.logic.ev_g_group_id()

    def get_my_born_range_data(self):
        if self.my_born_range_data:
            return self.my_born_range_data
        my_group_id = self.get_player_group_id()
        born_data = global_data.game_mode.get_born_data()
        if self.area_id not in born_data:
            return self.my_born_range_data
        range_ids = born_data[self.area_id].get('c_range')
        born_range_data = global_data.game_mode.get_cfg_data('born_range_data')
        if my_group_id in self.born_data and range_ids:
            born_data = self.born_data[my_group_id]
            _x, _y, _z, _r, _idx, _ = born_data.data
            self.my_born_range_data = born_range_data.get(str(range_ids[_idx]), {})
        return self.my_born_range_data

    def get_my_born_data(self):
        my_group_id = self.get_player_group_id()
        if my_group_id in self.born_data:
            return self.born_data[my_group_id]

    def on_check_base(self):
        if global_data.game_mode.mode and global_data.game_mode.mode.game_over:
            return False
        if not (global_data.player and global_data.player.logic):
            return False
        lpos = global_data.player.logic.ev_g_position()
        if not lpos:
            return False
        born_data = self.get_my_born_data()
        if not born_data:
            return False
        _x, _y, _z, _r, _idx, _ = born_data.data
        my_born_range_data = self.get_my_born_range_data()
        y_range = my_born_range_data.get('y_range')
        if not y_range:
            return False
        if lpos.y < _y + y_range[0] or lpos.y > _y + y_range[1]:
            if self.is_in_base_part:
                self.is_in_base_part = False
                global_data.emgr.death_in_base_part_change.emit()
            return self.is_in_base_part
        pos_lst = my_born_range_data.get('pos_lst', [])
        is_in_base_part = pnpoly(len(pos_lst), pos_lst, (lpos.x, lpos.z))
        if self.is_in_base_part != is_in_base_part:
            self.is_in_base_part = is_in_base_part
            global_data.emgr.death_in_base_part_change.emit()
            if is_in_base_part:
                self.show_swim_ui_list(SWIM_UI_LIST, True)
        return self.is_in_base_part

    def check_pos(self):
        self.my_born_range_data = {}
        self.check_pos_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_pos_timer)
        self.check_pos_timer = global_data.game_mgr.get_logic_timer().register(func=self.on_check_base, mode=timer.CLOCK, interval=1)
        global_data.emgr.death_first_check_in_base.emit()
        in_base = self.on_check_base()
        if not in_base:
            global_data.emgr.death_in_base_part_change.emit()

    def set_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.emgr.update_battle_timestamp.emit(settle_timestamp)

    def update_born_point(self, group_born_dict, born_point_list):
        for key in self.temp_born_point_key:
            del self.born_data[key]

        self.temp_born_point_key = []
        for index, data in enumerate(born_point_list):
            self.born_data[str(index)] = CBornData(str(index))
            self.born_data[str(index)].set_data(data)
            self.temp_born_point_key.append(str(index))

        for group_id, data in six.iteritems(group_born_dict):
            if group_id not in self.born_data:
                self.born_data[group_id] = CBornData(group_id)
            self.born_data[group_id].set_data(data)

        global_data.emgr.update_death_born_point.emit()
        self.check_pos()

    def get_last_choose_weapon(self, cls_name):
        weapon_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('weapon_settings', {})
        death_default_weapon = weapon_settings.get('DeathBattle', {})
        return weapon_settings.get(cls_name, death_default_weapon)

    def get_last_choose_down_weapon(self):
        return global_data.achi_mgr.get_general_archive_data_value(archive_key_const.KEY_LAST_DEATH_CHOOSE_DOWN_WEAPON, [])

    def save_select_weapon_data(self, weapon_dict, cls_name):
        candidate_weapon_list = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        if not candidate_weapon_list:
            return False
        else:
            candidate_weapon_set = set(candidate_weapon_list)
            last_choose_weapon = self.get_last_choose_weapon(cls_name)
            last_choose_weapon.pop(const.PART_WEAPON_POS_MAIN_DF, None)
            new_dict = {}
            illegal_pos = []
            for k, v in six.iteritems(last_choose_weapon):
                if v in candidate_weapon_set:
                    new_dict[int(k)] = v
                    candidate_weapon_set.remove(v)
                else:
                    illegal_pos.append(k)

            for k in illegal_pos:
                if candidate_weapon_set:
                    new_dict[int(k)] = candidate_weapon_set.pop()

            self.set_select_weapon_data(new_dict or weapon_dict)
            return new_dict and new_dict != weapon_dict

    def set_select_weapon_data(self, weapon_dict):
        self.weapon_dict = weapon_dict

    def get_select_weapon_data(self):
        return self.weapon_dict

    def set_area_id(self, area_id):
        self.area_id = area_id
        global_data.emgr.update_death_battle_data_area_id.emit(area_id)

    def update_all_group_status(self, group_status_dict):
        battle = global_data.battle
        self.group_status_dict = group_status_dict
        self.show_status_dict = {}
        if not global_data.player:
            return
        for group_id, entity_list in six.iteritems(group_status_dict):
            self.show_status_dict[group_id] = []
            for data in entity_list:
                aoi_id = data[0]
                entity = battle.get_entity_by_aoi_id(aoi_id)
                if not entity or entity and entity.uid != global_data.player.uid and entity.uid != global_data.player.get_global_spectate_player_uid():
                    self.show_status_dict[group_id].append(data)

        global_data.emgr.update_group_status_event.emit()

    def get_show_group_status(self):
        return self.show_status_dict

    def update_group_score_data(self, data):
        for key in six.iterkeys(data):
            self.group_score_dict[key] = data[key]

        global_data.emgr.update_group_score_data.emit(self.group_score_dict)
        recede = self.get_spawn_recede_rate()
        global_data.emgr.update_spawn_recede.emit(recede)

    def get_spawn_recede_rate(self):
        bat = global_data.player.get_battle()
        if not bat:
            return 0
        total_point = bat.get_settle_point()
        my, other = self.get_group_score()
        score_off = my - other
        recede = int(min(score_off * 1.0 / total_point * 100, 30) + 20.5)
        recede = min(0 if recede < 10 else recede, 50)
        return recede

    def get_group_score_data(self):
        return self.group_score_dict

    def get_group_score(self):
        pre = 0
        next = 0
        for group_id, score in six.iteritems(self.group_score_dict):
            if group_id == self.get_player_group_id():
                pre = score
            else:
                next = score

        return (
         pre, next)

    def update_score_details_data(self, data):
        self.score_details_dict = data
        global_data.emgr.update_score_details.emit(data)

    def get_score_details_data(self):
        return self.score_details_dict

    def show_swim_ui_list(self, ui_list, flag=True):
        if not flag:
            for ui in ui_list:
                ui = global_data.ui_mgr.get_ui(ui)
                if ui:
                    ui.add_hide_count('swim')

        else:
            for ui in ui_list:
                ui = global_data.ui_mgr.get_ui(ui)
                if ui:
                    ui.add_show_count('swim')

    def get_partner_voice_state(self, eid=None):
        if eid is not None:
            return self.partner_voice_state.get(eid, None)
        else:
            return self.partner_voice_state

    def get_partner_text_state(self, eid=None):
        if eid is not None:
            return self.partner_text_state.get(eid, None)
        else:
            return self.partner_text_state

    def set_partner_text_state(self, eid, state):
        if eid is not None and state is not None:
            self.partner_text_state[eid] = state
        return

    def set_partner_voice_state(self, eid, state):
        if eid is not None and state is not None:
            self.partner_voice_state[eid] = state
        return

    def update_spawn_rebirth_data(self, data):
        for key in six.iterkeys(data):
            self.spawn_rebirth_dict[key] = data[key]

    def get_spawn_rebirth_data(self, spwan_id):
        return self.spawn_rebirth_dict.get(spwan_id, [0, 0])

    def get_soul_selected_rogue_gifts(self, soul_id):
        return self.selected_rogue_gifts.get(soul_id, {})

    def get_is_revive(self):
        return False
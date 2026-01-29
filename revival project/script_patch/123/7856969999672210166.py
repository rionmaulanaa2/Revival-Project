# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impStat.py
from __future__ import absolute_import
from logic.gcommon.common_const.statistics_const import CAREER_STATISTICS_ACHIVE_PROP, CAREER_STATISTICS_BATTLE_PROP, TOTAL_CNT, CONTINUOUS_VICTORY, AVG_SETTLE_GRADE, SETTLE_SCORE
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int, List
from logic.client.const import player_battle_info_const as battle_const
import logic.gcommon.time_utility as t_util
import time
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN

class impStat(object):

    def _init_stat_from_dict(self, bdict):
        self._career_stat = bdict.get('career_stat', {})
        self._day_stat = bdict.get('day_stat', {})
        self._history_season_stat_dict = {}
        self._global_achieve = bdict.get('global_achieve', {})
        self._m_gl_achieve = bdict.get('m_gl_achieve', {})
        self._gl_state_data = None
        self._last_request_gl_time = 0
        self._simulate_cache = {}
        self._achieve_choose_record = bdict.get('achieve_choose_record', {})
        return

    @rpc_method(CLIENT_STUB, (Str('prop'), Int('value')))
    def update_career_stat(self, prop, value):
        self._career_stat[prop] = value

    @rpc_method(CLIENT_STUB, (Str('prop'), Str('value')))
    def update_str_career_stat(self, prop, value):
        self._career_stat[prop] = value

    @rpc_method(CLIENT_STUB, (Str('prop'), Int('value')))
    def update_day_stat(self, prop, value):
        self._day_stat[prop] = value
        global_data.emgr.update_day_stat.emit(prop)

    def get_stat(self, prop, default=0):
        return self._career_stat.get(prop, default)

    def get_day_stat(self, prop, default=0):
        return self._day_stat.get(prop, default)

    def is_best_record(self, prop, value):
        if value <= 0:
            return False
        return value >= self.get_stat(prop)

    def get_total_cnt(self):
        cnt = 0
        for battle_type in battle_const.get_chicken_modes():
            prop = CAREER_STATISTICS_BATTLE_PROP(battle_type, TOTAL_CNT)
            cnt += self.get_stat(prop)

        return cnt

    def get_death_total_cnt(self):
        cnt = 0
        for battle_type in battle_const.get_death_modes():
            prop = CAREER_STATISTICS_BATTLE_PROP(battle_type, TOTAL_CNT)
            cnt += self.get_stat(prop)

        return cnt

    def get_avg_settle_score_grade(self, battle_type):
        prop = CAREER_STATISTICS_BATTLE_PROP(battle_type, AVG_SETTLE_GRADE)
        return self._career_stat.get(prop, 'C')

    def request_day_stat(self, prop):
        self.call_server_method('request_day_stat', (prop,))

    def request_player_stat_info(self, uid, season_id):
        if uid == self.uid:
            career_stat = None
            if season_id == self.get_battle_season():
                career_stat = self._career_stat
            else:
                if season_id in self._history_season_stat_dict:
                    career_stat = self._history_season_stat_dict[season_id]
                if career_stat:
                    self.on_player_stat_info((uid, season_id, self._career_stat, self.history_season_ids))
                    return
        self.call_server_method('request_player_stat_info', (uid, season_id))
        return

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('season_id'), Dict('info'), List('history_season_ids')))
    def on_player_stat_info(self, uid, season_id, info, history_season_ids):
        info['season_id'] = season_id
        global_data.message_data.set_player_stat_inf(uid, info, history_season_ids)
        if uid == self.uid and season_id != self.get_battle_season():
            self._history_season_stat_dict[season_id] = info

    def is_best_battle_record(self, battle_type, battle_prop, value):
        prop = CAREER_STATISTICS_BATTLE_PROP(battle_type, battle_prop)
        return self.is_best_record(prop, value)

    def get_battle_stat_prop(self, battle_type, battle_prop, default=0):
        prop = CAREER_STATISTICS_BATTLE_PROP(battle_type, battle_prop)
        return self.get_stat(prop, default)

    def get_battle_continuous_victory(self, play_type, default=0):
        prop = CONTINUOUS_VICTORY + '_' + str(play_type)
        return self.get_stat(prop, default)

    def get_achieve_stat(self, play_type, achieve_id, default=0):
        prop = CAREER_STATISTICS_ACHIVE_PROP(play_type, achieve_id)
        return self.get_stat(prop, default)

    def request_player_history_game_result(self, uid, record_num=30):
        self.call_server_method('request_player_history_game_result', (uid, record_num))

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('info')))
    def on_history_game_result(self, uid, info):
        global_data.message_data.set_history_game_result(uid, info)

    def request_global_stat(self):
        self._last_request_gl_time = time.time()
        self.call_server_method('request_global_stat_data', ())

    @rpc_method(CLIENT_STUB, (Dict('stat_data'),))
    def on_global_stat_data(self, stat_data):
        self._gl_state_data = stat_data
        global_data.emgr.message_update_global_stat.emit(stat_data)

    def request_global_achieve(self):
        self.call_server_method('request_global_achieve', ())

    @rpc_method(CLIENT_STUB, (Dict('achieve_data'),))
    def on_global_achieve_data(self, achieve_data):
        pass

    @rpc_method(CLIENT_STUB, (Dict('achieve_data'),))
    def on_update_global_achieve_data(self, achieve_data):
        self._global_achieve.update(achieve_data)
        global_data.emgr.message_update_global_reward_receive.emit()
        self.request_global_stat()

    def try_get_global_achieve(self, achieve_id, need_check=True):
        if need_check:
            stat = self.get_gl_reward_receive_state(achieve_id)
            if stat != ITEM_UNRECEIVED:
                return
        self.call_server_method('request_try_get_global_achieve', (achieve_id,))

    @rpc_method(CLIENT_STUB, (Int('ret'), Str('achieve_id')))
    def on_get_global_achieve_result(self, ret, achieve_id):
        if ret == 1:
            self._m_gl_achieve[achieve_id] = {'get_time': t_util.time()}
            global_data.emgr.message_update_global_reward_receive.emit()

    def get_gl_reward_receive_state(self, achieve_id):
        if achieve_id in self._m_gl_achieve:
            return ITEM_RECEIVED
        else:
            if achieve_id in self._global_achieve:
                return ITEM_UNRECEIVED
            return ITEM_UNGAIN

    def get_global_stat_data(self):
        if self._gl_state_data is None:
            self.request_global_stat()
            return
        else:
            if time.time() - self._last_request_gl_time >= 5:
                self.request_global_stat()
                return self._gl_state_data
            return self._gl_state_data

    def has_unreceived_gl_reward(self, a_id):
        if a_id in self._global_achieve and a_id not in self._m_gl_achieve:
            return True
        return False

    def set_simulate_cache(self, key, value):
        self._simulate_cache[key] = value

    def get_simulate_cache(self, key):
        return self._simulate_cache.get(key, 0)

    def choose_global_achive(self, parent_achieve_id, achieve_id):
        if str(parent_achieve_id) in self._achieve_choose_record:
            return
        self._achieve_choose_record[str(parent_achieve_id)] = achieve_id
        self.call_server_method('choose_global_achive', (parent_achieve_id, achieve_id))

    def get_chose_sub_of_global_achive(self, parent_achieve_id):
        return self._achieve_choose_record.get(str(parent_achieve_id), None)
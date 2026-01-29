# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PeakWeeklyMatchWidget.py
from __future__ import absolute_import
import time
from common.framework import Singleton
import common.utils.timer as timer
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gutils.spectate_utils import has_live_competitions
from logic.gcommon.cdata.week_competition import data, get_week_competition_conf, get_week_competition_unfinish_conf, get_week_competition_conf_by_date
from logic.gcommon.const import ACTIVITY_PEAK_WEEKEND_MATCH_KEY_NEW

class PeakWeeklyMatchWidget(Singleton):
    ALIAS_NAME = 'peak_match_widget'

    def init(self):
        self.match_status_callback = []
        self.match_begin_but_has_no_live_callback = None
        self.room_status_callback = []
        self.start_peak_match_timer_id = None
        self.start_room_entry_timer_id = None
        self.has_competition_timer_id = 0
        self.has_competition_finished_timer_id = 0
        self.redpoint_status_callback = []
        self.has_redpoint_timer_id = 0
        self.process_event(True)
        self.start_peak_match_check_open()
        self.start_check_room_entry_open()
        self.start_check_redpoint()
        return

    def on_finalize(self):
        self.clear_all_check()
        self.match_status_callback = []
        self.match_begin_but_has_no_live_callback = None
        self.room_status_callback = []
        self.redpoint_status_callback = []
        self.process_event(False)
        return

    def destroy(self):
        self.on_finalize()

    def add_match_status_callback(self, callback):
        self.match_status_callback.append(callback)

    def add_room_status_callback(self, callback):
        self.room_status_callback.append(callback)

    def add_redpoint_status_callback(self, callback):
        self.redpoint_status_callback.append(callback)

    def set_match_begin_but_has_no_live_callback(self, callback):
        self.match_begin_but_has_no_live_callback = callback

    def clear_all_check(self):
        if self.start_room_entry_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.start_room_entry_timer_id)
            self.start_room_entry_timer_id = 0
        if self.start_peak_match_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.start_peak_match_timer_id)
            self.start_peak_match_timer_id = 0
        if self.has_competition_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.has_competition_timer_id)
            self.has_competition_timer_id = 0
        if self.has_competition_finished_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.has_competition_finished_timer_id)
            self.has_competition_finished_timer_id = 0
        if self.has_redpoint_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.has_redpoint_timer_id)
            self.has_redpoint_timer_id = 0

    def check_and_request(self):
        if has_live_competitions():
            has_match = True
        else:
            has_match = False
            global_data.player and global_data.player.request_global_spectate_brief_list(sp_const.SPECTATE_LIST_COMPETITION)
        return has_match

    def check_has_match_live_open(self):
        has_match = self.check_and_request()
        if has_match:
            self.on_has_match()
        elif callable(self.match_begin_but_has_no_live_callback):
            self.match_begin_but_has_no_live_callback()

    def check_has_finish(self):
        has_match = self.check_and_request()
        if not has_match:
            self.on_finish_match()

    def on_has_match(self):
        if not self.has_competition_finished_timer_id:
            self.has_competition_finished_timer_id = global_data.game_mgr.register_logic_timer(self.check_and_request, interval=60, times=-1, mode=timer.CLOCK)
        if self.match_status_callback:
            for cb in self.match_status_callback:
                cb(True)

    def on_finish_match(self):
        if self.match_status_callback:
            for cb in self.match_status_callback:
                cb(False)

        global_data.game_mgr.delay_exec(0.5, self._on_finish_match_clear_and_start)

    def _on_finish_match_clear_and_start(self):
        if self.has_competition_finished_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.has_competition_finished_timer_id)
            self.has_competition_finished_timer_id = 0

    def _has_competitions(self):
        return has_live_competitions()

    def check_peak_match_opent_timer(self):
        self.has_competition_timer_id = global_data.game_mgr.register_logic_timer(self.check_has_match_live_open, interval=30, times=-1, mode=timer.CLOCK)
        self.check_has_match_live_open()

    def start_peak_match_check_open(self):
        if self.start_peak_match_timer_id:
            return
        from logic.gcommon.cdata.week_competition import data, get_week_competition_battle_unfinish_time_list
        time_list = get_week_competition_battle_unfinish_time_list()
        if not time_list:
            return
        near_start_t = min(time_list)
        cur_time = tutil.time()
        t = max(near_start_t - cur_time + 60, 1)

        def callback():
            self.start_peak_match_timer_id = 0
            self.check_peak_match_opent_timer()

        self.start_peak_match_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=t, times=1, mode=timer.CLOCK)

    def start_check_room_entry_open(self):
        if self.start_room_entry_timer_id:
            return
        i, competition_id, start_ts, battle_info, reward_info = get_week_competition_conf()
        cur_time = tutil.time()
        t = start_ts - cur_time + 1
        if t <= 0:
            return

        def callback():
            self.start_room_entry_timer_id = None
            for cb in self.room_status_callback:
                cb()

            self.start_check_room_entry_open()
            return

        self.start_room_entry_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=t, times=1, mode=timer.CLOCK)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {'on_received_global_spectate_brief_list': self.on_received_global_spectate_brief_list,
           'net_login_reconnect_event': self.on_net_reconnect,
           'net_reconnect_event': self.on_net_reconnect,
           'on_activity_mention_per_day_0': self.start_check_redpoint
           }
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def on_received_global_spectate_brief_list(self, list_type):
        if list_type == sp_const.SPECTATE_LIST_COMPETITION:
            has_match = self._has_competitions()
            if has_match:
                self.on_has_match()
            elif self.has_competition_finished_timer_id:
                self.on_finish_match()
            elif self.has_competition_timer_id:
                i, competition_id, start_ts, battle_info, reward_info = get_week_competition_unfinish_conf()
                cur_time = tutil.time()
                battle_start_time = battle_info.get('auto_start_intv', 0) + start_ts
                if i < 0 or battle_start_time + 5 * tutil.ONE_MINUTE_SECONDS < cur_time:
                    self.on_finish_match()
                    if self.has_competition_timer_id:
                        global_data.game_mgr.unregister_logic_timer(self.has_competition_timer_id)
                        self.has_competition_timer_id = 0
                    if self.has_competition_finished_timer_id:
                        global_data.game_mgr.unregister_logic_timer(self.has_competition_finished_timer_id)
                        self.has_competition_finished_timer_id = 0

    def start_check_redpoint(self):
        if self.has_redpoint_timer_id:
            return
        _, competition_id, start_ts, _, _ = get_week_competition_conf_by_date()
        cur_time = int(tutil.get_server_time())
        if not tutil.is_same_day(cur_time, start_ts):
            if self.has_redpoint_timer_id:
                global_data.game_mgr.unregister_logic_timer(self.has_redpoint_timer_id)
                self.has_redpoint_timer_id = 0
            return
        remind_time = start_ts - tutil.ONE_MINUTE_SECONDS * 20
        cache_comp_id_list = global_data.achi_mgr.get_general_archive_data().get_field(ACTIVITY_PEAK_WEEKEND_MATCH_KEY_NEW, [])
        if cur_time < remind_time and str(competition_id) not in cache_comp_id_list:

            def callback():
                self.has_redpoint_timer_id = None
                for cb in self.redpoint_status_callback:
                    cb()

                return

            t = remind_time - cur_time + 1
            print ('---------------register_logic_timer start_check_redpoint----------------- time =', t)
            self.has_redpoint_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=t, times=1, mode=timer.CLOCK)

    def on_net_reconnect(self, *args):
        old_timer_id = self.has_competition_timer_id
        old_finish_timer_id = self.has_competition_finished_timer_id
        self.clear_all_check()
        if old_timer_id:
            self.has_competition_timer_id = global_data.game_mgr.register_logic_timer(self.check_has_match_live_open, interval=30, times=-1, mode=timer.CLOCK)
        if old_finish_timer_id:
            self.has_competition_finished_timer_id = global_data.game_mgr.register_logic_timer(self.check_and_request, interval=60, times=-1, mode=timer.CLOCK)
        self.start_peak_match_check_open()
        self.start_check_room_entry_open()
        self.start_check_redpoint()
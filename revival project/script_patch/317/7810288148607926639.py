# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/SummerPeakMatchWidget.py
from __future__ import absolute_import
import time
from common.framework import Singleton
import common.utils.timer as timer
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gutils.spectate_utils import has_live_competitions
from logic.gcommon.cdata.week_competition import data, get_week_competition_unfinish_conf

class SummerPeakMatchWidget(Singleton):
    ALIAS_NAME = 'summer_peak_match_widget'

    def init(self):
        self.start_summer_match_timer_id = None
        self.finish_summer_match_timer_id = None
        self.repeat_check_timer_id = None
        self.process_event(True)
        self.entry_status_callback = []
        self.check_summer_peak_match_open()
        self.check_cummer_peak_match_close()
        self.check_start_repeat_check()
        return

    def check_summer_peak_match_open(self):
        if self.start_summer_match_timer_id:
            return
        from logic.gcommon.cdata.round_competition import get_nearliest_competition_conf
        comp_id, comp_round, round_conf = get_nearliest_competition_conf()
        if not comp_id:
            return
        start_time = round_conf.get('start_show_time', 0) or round_conf.get('start_time', 0)
        cur_time = tutil.time()
        check_time = start_time - cur_time + 1
        if check_time <= 0:
            return

        def callback():
            for cb in self.entry_status_callback:
                cb()

            self.start_summer_match_timer_id = None
            self.check_cummer_peak_match_close()
            return

        self.start_summer_match_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=check_time, times=1, mode=timer.CLOCK)

    def check_cummer_peak_match_close(self):
        if self.finish_summer_match_timer_id:
            return
        from logic.gcommon.cdata.round_competition import get_nearliest_competition_conf
        comp_id, comp_round, round_conf = get_nearliest_competition_conf()
        if not comp_id:
            return
        battle_start_time = round_conf.get('end_show_time', 0) or round_conf.get('battle_time', 0)
        cur_time = tutil.time()
        check_time = battle_start_time - cur_time + 5
        if check_time <= 0:
            return

        def callback():
            for cb in self.entry_status_callback:
                cb()

            self.finish_summer_match_timer_id = None
            self.check_summer_peak_match_open()
            return

        self.finish_summer_match_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=check_time, times=1, mode=timer.CLOCK)

    def on_finalize(self):
        self.clear_all_check()
        self.entry_status_callback = []

    def destroy(self):
        self.on_finalize()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {'net_login_reconnect_event': self.on_net_reconnect
           }
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def clear_all_check(self):
        if self.start_summer_match_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.start_summer_match_timer_id)
            self.start_summer_match_timer_id = None
        if self.finish_summer_match_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.finish_summer_match_timer_id)
            self.finish_summer_match_timer_id = None
        self.clear_refresh_timer()
        return

    def add_entry_status_callback(self, callback):
        self.entry_status_callback.append(callback)

    def on_net_reconnect(self, *args):
        self.clear_all_check()
        self.check_summer_peak_match_open()
        self.check_cummer_peak_match_close()
        self.check_start_repeat_check()
        global_data.emgr.clean_up_summer_peak_match.emit()

    def check_start_repeat_check(self):
        from logic.gcommon.cdata.round_competition import get_nearliest_competition_open
        if self.need_start_refresh_timer():

            def callback():
                if global_data.player:
                    if not self.need_start_refresh_timer():
                        return
                    comp_id, cur_round, round_conf = get_nearliest_competition_open()
                    if not comp_id:
                        return
                    can_show = global_data.player.is_show_competition_entrance(comp_id, cur_round)
                    if not can_show:
                        global_data.player.clear_camp_show_info()
                        global_data.player.request_comp_show_entrance()

            if global_data.player:
                global_data.player.request_comp_show_entrance()
            self.repeat_check_timer_id = global_data.game_mgr.register_logic_timer(callback, interval=60, times=-1, mode=timer.CLOCK)

    def need_start_refresh_timer(self):
        from logic.gcommon.cdata import dan_data
        from logic.gcommon.cdata.round_competition import get_nearliest_competition_open
        comp_id, cur_round, round_conf = get_nearliest_competition_open()
        if not comp_id:
            return False
        else:
            limit_dan = round_conf.get('limit_dan', 0)
            if not global_data.player:
                return True
            my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
            last_season_dan = global_data.player.get_last_season_dan()
            if my_dan >= limit_dan or last_season_dan >= limit_dan:
                return True
            return False

    def clear_refresh_timer(self):
        if self.repeat_check_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.repeat_check_timer_id)
            self.repeat_check_timer_id = None
        return
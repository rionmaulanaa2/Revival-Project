# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LotterySummerPeakLiveEntryWidget.py
from __future__ import absolute_import
from logic.gutils.spectate_utils import has_live_competitions
from logic.gcommon import time_utility as tutil
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gcommon.common_const.liveshow_const import get_winter_cup_open_time, get_promotion_match_open_time, SUMMER_FINAL_LIVE_RED_POINT

def check_show_entry():
    time_now = tutil.time()
    t_time = get_promotion_match_open_time()
    return t_time[0] < time_now < t_time[1] and global_data.player


def check_is_auditions_match():
    START_HOUR = 68400
    END_HOUR = 79200
    time_now = tutil.time()
    OPEN_TIME = get_winter_cup_open_time()
    day_cnt = (time_now - OPEN_TIME[0]) // 86400
    start_time = OPEN_TIME[0] + day_cnt * 86400 + START_HOUR
    end_time = OPEN_TIME[0] + day_cnt * 86400 + END_HOUR
    is_in_act = OPEN_TIME[0] <= time_now <= OPEN_TIME[1]
    return day_cnt >= 0 and is_in_act and start_time < time_now < end_time and global_data.player


def is_within_time_range(timestamp, t3_start_time, t3_end_time):
    from datetime import datetime, time
    dt = datetime.fromtimestamp(timestamp)
    target_time = dt.time()
    start_time = time(t3_start_time[0], t3_start_time[1], t3_start_time[2])
    end_time = time(t3_end_time[0], t3_end_time[1], t3_end_time[2])
    return start_time <= target_time <= end_time


def check_summer_peak_live_red_point():
    if check_show_entry():
        cur_time = tutil.time()
        last_time = global_data.achi_mgr.get_cur_user_archive_data(SUMMER_FINAL_LIVE_RED_POINT, 0)
        if not last_time:
            return True
        day_start_time = int(tutil.get_day_start_timestamp(cur_time))
        return day_start_time > last_time
    else:
        return False


def save_live_red_point_time():
    cur_time = tutil.time()
    record_time = tutil.get_day_start_timestamp(cur_time)
    global_data.achi_mgr.set_cur_user_archive_data(SUMMER_FINAL_LIVE_RED_POINT, int(record_time))


class LotterySummerPeakLiveEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {'on_open_live_main_ui': 'on_open_live_main_ui_func',
       'net_login_reconnect_event': 'on_net_reconnect',
       'net_reconnect_event': 'on_net_reconnect'
       }

    def __init__(self, parent, panel, widget_id, widget_type):
        self.red_point_timer = None
        super(LotterySummerPeakLiveEntryWidget, self).__init__(parent, panel, widget_id, widget_type)
        return

    @classmethod
    def check_shown(cls, widget_type):
        player = global_data.player
        if not player:
            return False
        if check_show_entry():
            return True
        return False

    def on_init_widget(self):
        super(LotterySummerPeakLiveEntryWidget, self).on_init_widget()
        if check_summer_peak_live_red_point():
            self.panel.btn.red_point.setVisible(True)
        else:
            self.panel.btn.red_point.setVisible(False)
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        self.check_summer_peak_rp()

    def on_finalize_widget(self):
        super(LotterySummerPeakLiveEntryWidget, self).on_finalize_widget()
        self.clear_summer_rp_timer()

    def on_click_btn(self, *args):
        from logic.comsys.live.LiveMainUI import LiveMainUI
        live_main = LiveMainUI()

    def check_summer_peak_rp(self):
        if self.red_point_timer:
            return
        if check_summer_peak_live_red_point():
            return
        cur_time = tutil.time()
        zero_time = tutil.get_day_start_timestamp(tutil.time()) + tutil.ONE_DAY_SECONDS
        if zero_time - cur_time < 0:
            return
        check_time = zero_time - cur_time

        def callback():
            self.red_point_timer = None
            self.panel.btn.red_point.setVisible(True)
            return

        import common.utils.timer as timer
        self.red_point_timer = global_data.game_mgr.register_logic_timer(callback, interval=check_time, times=1, mode=timer.CLOCK)

    def clear_summer_rp_timer(self):
        if self.red_point_timer:
            global_data.game_mgr.unregister_logic_timer(self.red_point_timer)
            self.red_point_timer = None
        return

    def on_open_live_main_ui_func(self):
        if self.panel.btn.red_point.isVisible():
            save_live_red_point_time()
            self.panel.btn.red_point.setVisible(False)
            self.check_summer_peak_rp()

    def on_net_reconnect(self):
        self.clear_summer_rp_timer()
        self.check_summer_peak_rp()
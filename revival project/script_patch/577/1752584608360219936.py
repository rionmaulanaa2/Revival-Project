# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyWeekendActivityEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyWeekendActivityEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {}

    @classmethod
    def check_shown(cls, widget_type):
        from logic.gcommon.time_utility import get_utc8_weekday, get_server_time, get_utc8_hour
        cur_time = get_server_time()
        weekday = get_utc8_weekday(cur_time)
        if weekday not in (5, 6, 7, 1):
            return False
        if weekday == 5:
            hour = get_utc8_hour(cur_time)
            if hour < 5:
                return False
        else:
            if weekday == 1:
                hour = get_utc8_hour(cur_time)
                if hour >= 5:
                    return False
            activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_WEEKEND)
            if activity_list:
                return True
        return False

    def on_init_widget(self):
        super(LobbyWeekendActivityEntryWidget, self).on_init_widget()
        self.panel.PlayAnimation('loop')

        @self.panel.btn.unique_callback()
        def OnClick(*args):
            activity_list = self.get_activity_list()
            if not activity_list:
                global_data.game_mgr.show_tip(607177)
                global_data.emgr.refresh_activity_list.emit()
                return
            global_data.ui_mgr.show_ui('ActivityWeekendMainUI', 'logic.comsys.activity.ActivityWeekend')

    def on_finalize_widget(self):
        super(LobbyWeekendActivityEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(need_red_point)

    def need_show_red_point(self):
        from common.utils.redpoint_check_func import check_lobby_red_point
        if not check_lobby_red_point():
            return False
        activity_list = self.get_activity_list()
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        return count > 0
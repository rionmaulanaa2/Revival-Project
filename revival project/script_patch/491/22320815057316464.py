# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyWinterOutsideLiveEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil

def check_winter_outside_live_show_entry():
    return LobbyWinterOutsideLiveEntryWidget.check_shown('')


class LobbyWinterOutsideLiveEntryWidget(LobbyEntryWidgetBase):
    TIMER_TAG = 220505
    GLOBAL_EVENT = {'on_open_live_main_ui': 'on_open_live_main_ui_func'
       }

    @classmethod
    def check_shown(cls, widget_type):
        player = global_data.player
        if not player:
            return False
        else:
            act_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_WINTER_OUTSIDE_LIVE)
            from logic.gcommon.common_const import liveshow_const as live_sc
            platform_type = live_sc.HUYA_LIVE
            if global_data.player.enable_live(platform_type):
                if act_list:
                    return True
                return False
            return False

    def on_init_widget(self):
        super(LobbyWinterOutsideLiveEntryWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)

    def on_click_btn(self, *args):
        from logic.gcommon.common_const import liveshow_const as live_sc
        self.panel.btn.red_point.setVisible(False)
        from logic.comsys.live.LiveMainUI import LiveMainUI
        live_main = LiveMainUI()
        live_main.change_tab_force(live_sc.HUYA_LIVE)

    def on_finalize_widget(self):
        super(LobbyWinterOutsideLiveEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        if not (self.panel and self.panel.isValid()):
            return
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(True if need_red_point else False)

    def need_show_red_point(self):
        return False
        archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
        ar_key = 'clear_live_red_point'
        if tutil.time() - archive_data.get_field(ar_key, 0) > tutil.ONE_HOUR_SECONS * 4:
            return True
        else:
            return False

    def on_open_live_main_ui_func(self):
        if self.panel.btn.red_point.isVisible():
            archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
            ar_key = 'clear_live_red_point'
            archive_data.set_field(ar_key, tutil.time())
            self.panel.btn.red_point.setVisible(False)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyLotteryActivityEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyLotteryActivityEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {'receive_task_reward_succ_event': 'refresh_red_point',
       'task_prog_changed': 'refresh_red_point',
       'refresh_activity_redpoint': 'refresh_red_point',
       'message_update_global_reward_receive': 'refresh_red_point',
       'buy_good_success': 'refresh_red_point'
       }

    @classmethod
    def check_shown(cls, widget_type):
        activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_LOTTERY_S1)
        if activity_list:
            return True
        return False

    def on_init_widget(self):
        super(LobbyLotteryActivityEntryWidget, self).on_init_widget()
        self.panel.PlayAnimation('loop_activity')
        self.panel.PlayAnimation('show_lighting')

        @global_unique_click(self.panel.btn_activity_3)
        def OnClick(*args):
            self.on_click_button(*args)

    def on_finalize_widget(self):
        super(LobbyLotteryActivityEntryWidget, self).on_finalize_widget()

    def refresh_red_point(self):
        activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_LOTTERY_S1)
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        if self.panel.btn_activity_3.red_point:
            self.panel.btn_activity_3.red_point.setVisible(count > 0)

    def on_click_button(self, *args):
        global_data.ui_mgr.show_ui('LotteryActivityChooseUI', 'logic.comsys.mall_ui')
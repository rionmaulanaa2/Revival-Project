# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyChristmasActivityEntryWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const

class LobbyChristmasActivityEntryWidget(LobbyEntryWidgetBase):
    GLOBAL_EVENT = {'receive_task_reward_succ_event': 'refresh_red_point',
       'task_prog_changed': 'refresh_red_point',
       'refresh_activity_redpoint': 'refresh_red_point',
       'message_update_global_reward_receive': 'refresh_red_point',
       'buy_good_success': 'refresh_red_point'
       }

    def on_init_widget(self):
        super(LobbyChristmasActivityEntryWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        self.panel.PlayAnimation('loop')

    def on_click_btn(self, *args):
        activity_list = self.get_activity_list()
        if not activity_list:
            global_data.game_mgr.show_tip(607177)
            global_data.emgr.refresh_activity_list.emit()
            return
        global_data.ui_mgr.show_ui('ActivityChristmasMainUI', 'logic.comsys.activity')

    def refresh_red_point(self, *args):
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(need_red_point)

    def need_show_red_point(self):
        from common.utils.redpoint_check_func import check_lobby_red_point
        if not check_lobby_red_point():
            return False
        activity_list = activity_utils.get_ordered_activity_list(activity_const.WIDGET_CHRISTMAS)
        count = activity_utils.get_activity_red_point_count_by_activity_list(activity_list)
        return count > 0
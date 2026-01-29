# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyNewReturnEntryWidget.py
from __future__ import absolute_import
from logic.gutils.activity_utils import get_ordered_activity_list, get_activity_red_point_count_by_activity_list
from logic.gcommon.common_const.activity_const import WIDGET_NEW_RETURN
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase

class LobbyNewReturnEntryWidget(LobbyEntryWidgetBase):

    def on_init_widget(self):
        super(LobbyNewReturnEntryWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        self.panel.PlayAnimation('loop')

    def on_click_btn(self, *args):
        global_data.ui_mgr.show_ui('ActivityNewReturnMainUI', 'logic.comsys.activity.ActivityNewReturn')

    def refresh_red_point(self):
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(need_red_point)

    def need_show_red_point(self):
        from common.utils.redpoint_check_func import check_lobby_red_point
        if not check_lobby_red_point():
            return False
        activity_list = self.get_activity_list()
        count = get_activity_red_point_count_by_activity_list(activity_list)
        return count > 0
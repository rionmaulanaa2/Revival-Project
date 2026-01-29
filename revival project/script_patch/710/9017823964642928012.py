# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/ActivityNewReturnMainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_1

class ActivityNewReturnMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202108/comeback_main/comeback_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = ActivityMainUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({})

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_NEW_RETURN
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_NEW_RETURN)

    def refresh_time(self):
        self.panel.nd_time.setVisible(False)
        if not (self.panel and self.panel.lab_time):
            return
        if not self.activity_page_tab_widget:
            return
        cur_page_widget = self.activity_page_tab_widget.get_cur_view_page_widget()
        if not cur_page_widget or not hasattr(cur_page_widget, 'get_left_time'):
            return
        left_time_str = cur_page_widget.get_left_time()
        self.panel.nd_time.setVisible(True)
        self.panel.lab_time.SetString(left_time_str)
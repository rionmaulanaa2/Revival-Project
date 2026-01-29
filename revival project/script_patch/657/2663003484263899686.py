# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerWelfareMainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_1

class ActivitySummerWelfareMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_main_1'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    NEED_HIDE_MAIN_UI = False

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_SUMMER_WELFARE
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_SUMMER_WELFARE)
        self.activity_page_tab_widget.panel.temp_tab_list.setVisible(False)
        self.activity_page_tab_widget.panel.temp_btn_close.setVisible(False)
        self.activity_page_tab_widget.panel.img_title.setVisible(False)
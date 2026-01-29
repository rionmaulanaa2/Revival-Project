# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeekend/ActivityWeekendMainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
import cc

class ActivityWeekendMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202206/weekend_main/weekend_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER

    def on_init_panel(self):
        super(ActivityWeekendMainUI, self).on_init_panel()

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_WEEKEND
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_WEEKEND)

    def on_resolution_changed(self):
        self.activity_page_tab_widget.on_resolution_changed()
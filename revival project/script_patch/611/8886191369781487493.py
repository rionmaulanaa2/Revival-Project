# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerMainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
import cc

class ActivitySummerMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202107/main/activity_main_summer'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    GLOBAL_EVENT = ActivityMainUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({})

    def on_init_panel(self):
        super(ActivitySummerMainUI, self).on_init_panel()
        self.panel.PlayAnimation('in')

    def init_parameters(self):
        super(ActivitySummerMainUI, self).init_parameters()
        self.in_anim_idx = -1

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_SUMMER
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_SUMMER, default_font_size=None)
        return

    def play_in_anim(self):
        self.in_anim_idx += 1
        ui_item = self.panel.temp_tab_list.list_tab.GetItem(self.in_anim_idx)
        ui_item.PlayAnimation('in')

    def on_resolution_changed(self):
        self.activity_page_tab_widget.on_resolution_changed()

    def on_finalize_panel(self):
        self.in_anim_idx = -1
        super(ActivitySummerMainUI, self).on_finalize_panel()
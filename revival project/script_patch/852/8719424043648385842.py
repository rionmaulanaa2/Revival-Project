# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIMainUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase

class ActivityKizunaAIMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202103/kizunaai/activity_main_kizunaai'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = ActivityMainUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({})
    GLOBAL_EVENT = ActivityMainUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({})
    OPEN_SOUND_NAME = 'menu_shop'

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPreviewPageTabWidget import ActivityPreviewPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_KIZUNA_AI
        self.activity_page_tab_widget = ActivityPreviewPageTabWidget(self, WIDGET_KIZUNA_AI)
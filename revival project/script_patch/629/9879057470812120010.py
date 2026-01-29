# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLotteryS6MainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import DIALOG_LAYER_ZORDER

class ActivityLotteryS6MainUI(ActivityMainUIBase):
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'mall/i_lottery_activity/s6/lottery_activity_main_s6'
    UI_ACTION_EVENT = {'btn_lose.OnClick': 'close'
       }

    def on_init_panel(self):
        super(ActivityLotteryS6MainUI, self).on_init_panel()
        self.panel.lab_text.setVisible(False)

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_LOTTERY_S6_ANUBIS
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_LOTTERY_S6_ANUBIS)
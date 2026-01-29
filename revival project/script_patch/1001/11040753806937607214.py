# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloweenLotteryMainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
import cc

class ActivityHalloweenLotteryMainUI(ActivityMainUIBase):
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'mall/i_lottery_activity/halloween/lottery_acticity_main_halloween'
    UI_ACTION_EVENT = {'btn_lose.OnClick': 'close'
       }
    activity_type = 'WIDGET_LOTTERY_HALLOWEEN'

    def on_init_panel(self):
        super(ActivityHalloweenLotteryMainUI, self).on_init_panel()
        self.lab_time_text_id = None
        return

    def play_animation(self):
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('loop')

    def init_parameters(self):
        super(ActivityHalloweenLotteryMainUI, self).init_parameters()

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        self.activity_page_tab_widget = ActivityPageTabWidget(self, self.activity_type)
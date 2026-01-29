# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityS2SecondMainUI.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
import cc

class ActivityS2SecondMainUI(ActivityMainUIBase):
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'mall/i_lottery_activity/lottery_activity_main'
    UI_ACTION_EVENT = {'btn_lose.OnClick': 'close'
       }

    def on_init_panel(self):
        super(ActivityS2SecondMainUI, self).on_init_panel()

    def init_parameters(self):
        super(ActivityS2SecondMainUI, self).init_parameters()
        self.lab_time_text_id = 0

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_LOTTERY_S2_2
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_LOTTERY_S2_2)
        frame_time = 1.0 / 30.0
        tablist = self.panel.temp_tab_list.list_tab
        count = tablist.GetItemCount()
        action_list = []
        for index in range(count):
            one_node = tablist.GetItem(index)
            delay_time = frame_time * index
            action_list.append(cc.DelayTime.create(delay_time))
            action_list.append(cc.CallFunc.create(lambda : one_node.PlayAnimation('appear')))

        self.panel.runAction(cc.Sequence.create(action_list))
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ArtCollection/ActivitySpringFestival2022MainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.const.uiconst import DIALOG_LAYER_ZORDER
import cc

class ActivitySpringFestival2022MainUI(ActivityMainUIBase):
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    NEED_HIDE_MAIN_UI = False
    PANEL_CONFIG_NAME = 'mall/i_lottery_activity/spring/spring_collection/i_activity_collect_main'
    UI_ACTION_EVENT = {'btn_lose.OnClick': 'close'
       }
    activity_type = 'WIDGET_LOTTERY_2022_SPRING'

    def init_parameters(self):
        super(ActivitySpringFestival2022MainUI, self).init_parameters()
        self.lab_time_text_id = 0

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        self.activity_page_tab_widget = ActivityPageTabWidget(self, self.activity_type)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.6),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')),
         cc.DelayTime.create(0.2),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_02'))]))
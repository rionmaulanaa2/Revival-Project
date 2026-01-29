# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIConcertMainUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from logic.gcommon.common_const import activity_const

class ActivityKizunaAIConcertMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/activity_main_kizuna'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = ActivityMainUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'temp_btn_close_1.btn_back.OnClick': 'close'
       })
    GLOBAL_EVENT = ActivityMainUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({})
    OPEN_SOUND_NAME = 'menu_shop'
    SHOW_BALCK_CLOSE_BTN = {
     activity_const.ACTIVITY_KIZUNA_AI_RECRUIT,
     activity_const.ACTIVITY_KIZUNA_AI_ACTIVITY1,
     activity_const.ACTIVITY_KIZUNA_AI_ACTIVITY2,
     activity_const.ACTIVITY_KIZUNA_AI_FETTERS,
     activity_const.ACTIVITY_KIZUNA_AI_EXCHANGE,
     activity_const.ACTIVITY_KIZUNA_WARM_UP}

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPreviewPageTabWidget import ActivityPreviewPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_KIZUNA_AI_CONCERT
        self.activity_page_tab_widget = ActivityPreviewPageTabWidget(self, WIDGET_KIZUNA_AI_CONCERT, select_cb=self._select_widget_cb, default_font_size=None)
        return

    def _select_widget_cb(self, widget):
        is_show_black_btn = widget._activity_type in self.SHOW_BALCK_CLOSE_BTN
        self.panel.temp_btn_close.setVisible(not is_show_black_btn)
        self.panel.temp_btn_close_1.setVisible(is_show_black_btn)
        show_bg = hasattr(widget, 'need_bg') or True if 1 else widget.need_bg()
        self.panel.nd_bg.setVisible(show_bg)
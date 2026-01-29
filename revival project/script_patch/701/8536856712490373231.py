# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnniversaryMainUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from logic.gcommon.common_const import activity_const

class ActivityAnniversaryMainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202201/anniversary_tab/activity_anniversary_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = ActivityMainUIBase.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({})
    GLOBAL_EVENT = ActivityMainUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({})
    OPEN_SOUND_NAME = 'menu_shop'

    def on_init_panel(self):
        super(ActivityAnniversaryMainUI, self).on_init_panel()
        self.change_text_pic()

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPreviewPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_ANNIVERSARY
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_ANNIVERSARY, select_cb=self._select_widget_cb, default_font_size=None)
        return

    def _select_widget_cb(self, widget):
        show_bg = hasattr(widget, 'need_bg') or True if 1 else widget.need_bg()
        self.panel.nd_bg.setVisible(show_bg)

    def try_select_tab(self, activity_type):
        self.activity_page_tab_widget.try_select_tab(activity_type)

    def change_text_pic(self):
        import social
        channel = social.get_channel()
        is_steam_channel = channel and channel.name == 'steam'
        if is_steam_channel:
            self.panel.img_title.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202201/anniversary_tab/txt_anniversary_tab.png')
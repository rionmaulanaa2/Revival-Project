# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520MainUI.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityMainUIBase import ActivityMainUIBase
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc

class Activity520MainUI(ActivityMainUIBase):
    PANEL_CONFIG_NAME = 'activity/activity_202105/520/activity_main_520'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    GLOBAL_EVENT = ActivityMainUIBase.GLOBAL_EVENT.copy()
    GLOBAL_EVENT.update({})

    def on_init_panel(self):
        super(Activity520MainUI, self).on_init_panel()
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('show')

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_520_ACTIVITY
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_520_ACTIVITY, default_font_size=None)
        return

    def on_resolution_changed(self):
        self.activity_page_tab_widget.on_resolution_changed()
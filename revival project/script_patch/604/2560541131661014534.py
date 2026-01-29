# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewAlphaPlan/AlphaPlanMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc

class AlphaPlanMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE
    HOT_KEY_NEED_SCROLL_SUPPORT = True

    def on_init_panel(self):
        self.init_parameters()
        self.create_all_widget()
        self.init_scroll()
        self.panel.PlayAnimation('appear')
        self.hide_main_ui()
        self.try_select_tab(None)
        return

    def on_finalize_panel(self):
        self.show_main_ui()
        self.activity_page_tab_widget and self.activity_page_tab_widget.on_finalize_panel()
        self.activity_page_tab_widget = None
        self.activity_page_widget and self.activity_page_widget.on_finalize_panel()
        self.activity_page_widget = None
        return

    def do_show_panel(self):
        super(AlphaPlanMainUI, self).do_show_panel()
        self._show_times += 1
        if self.activity_page_tab_widget and self._show_times >= 2:
            self.activity_page_tab_widget.refresh_page_widget()

    def init_parameters(self):
        self._show_times = 0
        self.activity_page_tab_widget = None
        self.activity_page_widget = None
        return

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_ALPHA_PLAN
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_ALPHA_PLAN)

    def try_select_tab(self, activity_type):
        self.activity_page_tab_widget.try_select_tab(activity_type)

    def _on_login_reconnected(self, *args):
        self.close()

    def init_scroll(self):
        if global_data.is_pc_mode:
            self.register_mouse_scroll_event()

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        tab_list = self.panel.temp_tab_list.list_tab
        if not tab_list:
            return
        mouse_scroll_utils.sview_scroll_by_mouse_wheel(tab_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)

    def check_can_mouse_scroll(self):
        if global_data.is_pc_mode and self.HOT_KEY_NEED_SCROLL_SUPPORT and global_data.player:
            return True
        return False
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCenterMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc

class ActivityCenterMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_main_2'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected',
       'change_activity_main_close_btn_visibility': 'on_change_activity_main_close_btn_visibility',
       'trigger_activity_main_close_btn': 'on_trigger_activity_main_close_btn'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE
    HOT_KEY_NEED_SCROLL_SUPPORT = True

    def on_init_panel(self):
        self._show_times = 0
        self.hide_main_ui()
        self.init_parameters()
        self.init_widget()
        self.init_scroll()

    def on_finalize_panel(self):
        self.activity_page_tab_widget and self.activity_page_tab_widget.on_finalize_panel()
        self.activity_page_tab_widget = None
        self.activity_page_widget and self.activity_page_widget.on_finalize_panel()
        self.activity_page_widget = None
        self.show_main_ui()
        return

    def do_show_panel(self):
        old_vis = self.panel.isVisible()
        super(ActivityCenterMainUI, self).do_show_panel()
        self._show_times += 1
        if self.activity_page_tab_widget and self._show_times >= 2:
            self.activity_page_tab_widget.refresh_page_widget()
        if self.activity_page_tab_widget and not old_vis:
            self.activity_page_tab_widget.on_main_ui_reshow()

    def do_hide_panel(self):
        super(ActivityCenterMainUI, self).do_hide_panel()
        if self.activity_page_tab_widget:
            self.activity_page_tab_widget.on_main_ui_hide()

    def init_parameters(self):
        self.activity_page_tab_widget = None
        self.activity_page_widget = None
        return

    def init_widget(self):
        self.create_all_widget()
        self.panel.PlayAnimation('appear')

    def create_all_widget(self):
        from logic.comsys.activity.ActivityMainPageTabWidget import ActivityMainPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_MAIN
        self.activity_page_tab_widget = ActivityMainPageTabWidget(self, WIDGET_MAIN, self._select_widget_cb)

    def try_select_tab(self, activity_type):
        self.activity_page_tab_widget.try_select_tab(activity_type)

    def select_tab(self, activity_type):
        self.activity_page_tab_widget.select_tab(activity_type)

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

    def on_change_activity_main_close_btn_visibility(self, widget_type, vis):
        from logic.gcommon.common_const.activity_const import WIDGET_MAIN
        if widget_type == WIDGET_MAIN:
            self.panel.temp_btn_close.setVisible(vis)

    def on_trigger_activity_main_close_btn(self, widget_type):
        from logic.gcommon.common_const.activity_const import WIDGET_MAIN
        if widget_type == WIDGET_MAIN:
            self.close()

    def _select_widget_cb(self, widget):
        show_bg = hasattr(widget, 'need_bg') or True if 1 else widget.need_bg()
        self.panel.nd_bg.setVisible(show_bg)

    def get_page_tab_widget(self):
        return self.activity_page_tab_widget

    def set_close_btn_visible(self, visible):
        self.panel.temp_btn_close.setVisible(visible)

    def set_temp_tab_list_visible(self, visible):
        self.panel.temp_tab_list.setVisible(visible)
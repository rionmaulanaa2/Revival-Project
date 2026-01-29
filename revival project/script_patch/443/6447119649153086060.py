# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMainUIBase.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon import time_utility
from common.cfg import confmgr

class ActivityMainUIBase(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    NEED_HIDE_MAIN_UI = True

    def on_init_panel(self):
        self.regist_main_ui()
        self.init_parameters()
        self.create_all_widget()
        self.init_scroll()
        self.play_animation()
        if self.NEED_HIDE_MAIN_UI:
            self.hide_main_ui()
        self.try_select_tab(None)
        self.register_timer()
        if self.panel and self.panel.lab_time:
            self._timer_cb[0] = lambda : self.refresh_time()
            self.refresh_time()
        return

    def on_finalize_panel(self):
        self.unregist_main_ui()
        self.activity_page_tab_widget and self.activity_page_tab_widget.on_finalize_panel()
        self.activity_page_tab_widget = None
        self.activity_page_widget and self.activity_page_widget.on_finalize_panel()
        self.activity_page_widget = None
        self.unregister_timer()
        if self.NEED_HIDE_MAIN_UI:
            self.show_main_ui()
        return

    def do_show_panel(self):
        old_vis = self.panel.isVisible()
        super(ActivityMainUIBase, self).do_show_panel()
        self._show_times += 1
        if self.activity_page_tab_widget and self._show_times >= 2:
            self.activity_page_tab_widget.refresh_page_widget()
        if self.activity_page_tab_widget and not old_vis:
            self.activity_page_tab_widget.on_main_ui_reshow()

    def do_hide_panel(self):
        super(ActivityMainUIBase, self).do_hide_panel()
        if self.activity_page_tab_widget:
            self.activity_page_tab_widget.on_main_ui_hide()

    def init_parameters(self):
        self.lab_time_text_id = 607014
        self._show_times = 0
        self.activity_page_tab_widget = None
        self.activity_page_widget = None
        self._timer = 0
        self._timer_cb = {}
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_ALPHA_PLAN
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_ALPHA_PLAN)

    def refresh_time(self):
        if not (self.panel and self.panel.lab_time):
            return
        if not self.activity_page_tab_widget:
            return
        activity_type = self.activity_page_tab_widget._cur_selected_activity_type
        if not self.activity_page_tab_widget._cur_selected_activity_type:
            self.panel.lab_time.setVisible(False)
            return
        self.panel.lab_time.setVisible(True)
        conf = confmgr.get('c_activity_config', activity_type)
        end_time = conf.get('cEndTime', 0)
        if end_time:
            server_time = time_utility.get_server_time()
            left_time = end_time - server_time
            if left_time > 0:
                if self.lab_time_text_id:
                    self.panel.lab_time.SetString(get_text_by_id(self.lab_time_text_id).format(time_utility.get_readable_time_2(left_time)))
                else:
                    self.panel.lab_time.SetString(time_utility.get_readable_time_2(left_time))
            else:
                self.panel.lab_time.setVisible(False)

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

    def play_animation(self):
        self.panel.PlayAnimation('appear')
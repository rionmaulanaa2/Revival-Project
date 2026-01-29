# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/OldActivityGranbelmMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import activity_utils
from logic.gcommon.common_const.activity_const import ACTIVITY_GRANBELM_SHARE
from logic.gutils import template_utils
from cocosui import cc, ccui, ccs
from logic.gcommon.common_const.activity_const import WIDGET_GRANBELM

class OldActivityGranbelmMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202004/activity_granbelm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close',
       'nd_close.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self._show_times = 0
        self.hide_main_ui()
        self.init_parameters()
        self.init_widget()

    def on_finalize_panel(self):
        self.show_main_ui()
        self.activity_page_tab_widget and self.activity_page_tab_widget.on_finalize_panel()
        self.activity_page_tab_widget = None
        self.activity_page_widget and self.activity_page_widget.on_finalize_panel()
        self.activity_page_widget = None
        return

    def do_show_panel(self):
        super(OldActivityGranbelmMainUI, self).do_show_panel()
        self._show_times += 1
        if self.activity_page_tab_widget and self._show_times >= 2:
            self.activity_page_tab_widget.refresh_page_widget()
        self.panel.temp_tab_list.PlayAnimation('appear')
        self.panel.temp_tab_list.PlayAnimation('loop')

    def init_parameters(self):
        self.activity_page_tab_widget = None
        self.activity_page_widget = None
        return

    def init_widget(self):
        self.create_all_widget()
        ret_list = activity_utils.get_ordered_activity_list(WIDGET_GRANBELM)
        if ret_list:
            tab_conf = ret_list[0]
            if isinstance(tab_conf, list):
                act_id = tab_conf[0]['activity_type']
            else:
                act_id = tab_conf['activity_type']
            self.select_tab(act_id)
        self.panel.PlayAnimation('appear')

    def create_all_widget(self):
        from logic.comsys.activity.ActivityPageTabWidget import ActivityPageTabWidget
        from logic.gcommon.common_const.activity_const import WIDGET_GRANBELM
        self.activity_page_tab_widget = ActivityPageTabWidget(self, WIDGET_GRANBELM)

    def select_tab(self, activity_type):
        self.activity_page_tab_widget.select_tab(activity_type)

    def _on_login_reconnected(self, *args):
        self.close()
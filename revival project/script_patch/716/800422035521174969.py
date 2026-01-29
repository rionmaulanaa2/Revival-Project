# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMain.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_const.activity_const import *
from .ActivityPhoneBinding import ActivityPhoneBinding
ACTIVITY_INFO = {ACTIVITY_BIND_MOBILE: (
                        ActivityPhoneBinding, '\xe6\x89\x8b\xe6\x9c\xba\xe7\xbb\x91\xe5\xae\x9a')
   }

class ActivityMain(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'pnl_content.btn_close.OnClick': 'on_close'
       }
    UI_EFFECT_LIST = [{'node': 'pnl_content','anim': 'in','time': 0}, {'node': 'tab_bar','anim': 'in','time': 0.6}]
    CONTENT_NODES = ('nd_content', )
    DELAY_TIME = 0.6

    def on_init_panel(self, activity_list):
        self.tab_list = self.panel.tab_bar
        self.tab_panels = []
        self.pages = {}
        self.activity_list = activity_list
        global_data.emgr.show_lobby_common_bg_event.emit(True)
        self.cur_index = None
        tab_list = self.panel.tab_bar.tab_list
        for index, info in enumerate(activity_list):
            panel = tab_list.AddTemplateItem()
            self.add_tab_elem(index, info, panel)

        content_size = tab_list.GetInnerContentSize()
        view_size = tab_list.getContentSize()
        if content_size.height >= view_size.height:
            tab_list.setTouchEnabled(False)
        else:
            tab_list.setTouchEnabled(True)
        self.cur_index = 0
        self.cur_panel = tab_list.GetItem(0)
        self.cur_panel.btn_window_tab.SetSelect(True)
        self.cur_panel.img_hint.setVisible(False)
        self.show_page(activity_list[0])
        self.hide_main_ui()
        return

    def add_tab_elem(self, index, info, panel):
        from logic.gutils.template_utils import init_common_tab_bar_btn
        activity_type, hint = info[0], info[1]
        _, activity_name = ACTIVITY_INFO[activity_type]
        panel.img_hint.setVisible(hint)

        def callback(*args):
            if self.cur_index == index:
                return
            self.cur_panel.btn_window_tab.SetSelect(False)
            self.cur_panel = panel
            self.cur_panel.btn_window_tab.SetSelect(True)
            self.cur_index = index
            self.show_page(info)

        init_common_tab_bar_btn(panel, activity_name, callback)
        self.tab_panels.append(panel)

    def show_page(self, info):
        cur_type = info[0]
        page = self.pages.get(cur_type, None)
        if not page:
            activity_panel, _ = ACTIVITY_INFO[cur_type]
            page = activity_panel()
            self.pages[cur_type] = page
            self.panel.nd_content.AddChild('', page.get_widget())
            page.panel.SetPosition('50%', '50%')
        for ac_type, page in six.iteritems(self.pages):
            page.get_widget().setVisible(cur_type == ac_type)

        global_data.player.read_activity_list(cur_type)
        return

    def on_close(self, *args):
        self.close()

    def on_finalize_panel(self):
        for idx, page in six.iteritems(self.pages):
            page.on_finalize_panel()
            del page

        self.pages = None
        global_data.emgr.show_lobby_common_bg_event.emit(False)
        self.show_main_ui()
        return
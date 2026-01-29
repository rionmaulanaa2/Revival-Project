# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/MainRecruit.py
from __future__ import absolute_import
import six
from six.moves import range
TAB_RECRUIT = 0
TAB_RECRUIT_REWARD = 1
TAB_RECRUIT_LIST = 2
from .AddRecruit import AddRecruit
from .RecruitReward import RecruitReward
from .RecruitList import RecruitList
TAB_MAP = {TAB_RECRUIT: {'tab_name': 10311,'ui_class': AddRecruit},TAB_RECRUIT_REWARD: {'tab_name': 10312,'ui_class': RecruitReward},TAB_RECRUIT_LIST: {'tab_name': 10313,'ui_class': RecruitList}}

class MainRecruit(object):

    def __init__(self, main_panel, **kargs):
        self.main_panel = main_panel
        self.panel = global_data.uisystem.load_template_create('friend/i_friend_invite', parent=self.main_panel)
        self._message_data = global_data.message_data
        self._cur_tab_index = None
        self._tabs = {}
        self._tab_panels = {}
        self.init_tab()
        self.init_data()
        return

    def init_data(self):
        global_data.player.get_recruit_info()
        global_data.player.get_recruit_info_state()
        if global_data.achi_mgr.get_cur_user_archive_data('recruit_red_point'):
            global_data.achi_mgr.set_cur_user_archive_data('recruit_red_point', 0)

    def init_tab(self):
        list_tab = self.panel.nd_friend.nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        for tab_index in range(3):
            tab = list_tab.AddTemplateItem()
            tab.btn_tab.SetText(get_text_by_id(TAB_MAP[tab_index]['tab_name']))
            self.add_touch_tab(tab, tab_index)

    def add_touch_tab(self, tab, tab_index):
        self._tabs[tab_index] = tab
        tab.btn_tab.EnableCustomState(True)

        @tab.btn_tab.callback()
        def OnClick(*_):
            self.touch_tab_by_index(tab_index)

    def touch_tab_by_index(self, tab_index):
        if self._cur_tab_index is not None:
            tab = self._tabs.get(self._cur_tab_index, None)
            tab.btn_tab.SetSelect(False)
            tab.PlayAnimation('unclick')
            tab.img_vx.setVisible(False)
            tab_panel = self._tab_panels.get(self._cur_tab_index, None)
            tab_panel.hide_panel()
        tab = self._tabs.get(tab_index, None)
        tab.btn_tab.SetSelect(True)
        tab.img_vx.setVisible(True)
        tab.PlayAnimation('click')
        tab_panel = self._tab_panels.get(tab_index, None)
        if tab_panel is None:
            tab_panel = TAB_MAP[tab_index]['ui_class'](self.panel.nd_friend.nd_content)
            self._tab_panels[tab_index] = tab_panel
        tab_panel.show_panel()
        self._cur_tab_index = tab_index
        return

    def set_visible(self, visible):
        self.panel.setVisible(visible)
        if visible:
            self.touch_tab_by_index(TAB_RECRUIT)

    def destroy(self):
        self.main_panel = None
        self.panel = None
        self._message_data = None
        self._cur_tab_index = None
        self._tabs.clear()
        for panel in six.itervalues(self._tab_panels):
            panel.destroy()

        self._tab_panels.clear()
        return

    def hide_inputbox(self):
        pass
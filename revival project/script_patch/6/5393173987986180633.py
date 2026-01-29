# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/MainFollow.py
from __future__ import absolute_import
import six
from six.moves import range
TAB_FOLLOW_LIST = 0
TAB_FANS_LIST = 1
TAB_SEARCH_LIST = 2
from .FollowList import FollowList
from .FansList import FansList
from .FollowSearchResult import FollowSearchResult
import logic.comsys.common_ui.InputBox as InputBox
import logic.gcommon.const as const
from logic.gutils.follow_utils import format_popular_num, get_input_box_search_item
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gutils.observe_utils import goto_spectate_player
TAB_MAP = {TAB_FOLLOW_LIST: {'tab_name': 10331,'ui_class': FollowList},TAB_FANS_LIST: {'tab_name': 10332,'ui_class': FansList}}
MaxSearchTextLength = 30

class MainFollow(object):

    def __init__(self, main_panel, **kargs):
        self.main_panel = main_panel
        self.panel = global_data.uisystem.load_template_create('friend/i_follow', parent=self.main_panel)
        self._message_data = global_data.message_data
        self._cur_tab_index = None
        self._tabs = {}
        self._tab_panels = {}
        self._tab_tip_showed = {}
        self.init_tab()
        self.init_data()
        self.init_event()
        return

    def init_data(self):
        if global_data.player:
            global_data.player.request_fans_system_player_info(const.FANS_SYSTEM_INFO_TYPE_FANS, 1)
            global_data.player.request_fans_system_player_info(const.FANS_SYSTEM_INFO_TYPE_FOLLOWS, 1)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_received_global_spectate_list': self.on_received_global_spectate_list,
           'on_update_follow_player_count': self.on_update_follow_player_count,
           'on_update_fans_player_count': self.on_update_fans_player_count
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_received_global_spectate_list(self, list_type, list_info):
        if list_type != sp_const.SPECTATE_LIST_SEARCH:
            return
        if not list_info:
            return
        goto_spectate_player(list_info[0])

    def on_update_follow_player_count(self, follow_count):
        self.refresh_tab_title(TAB_FOLLOW_LIST)

    def on_update_fans_player_count(self, fans_count):
        self.refresh_tab_title(TAB_FANS_LIST)
        if not self._tab_tip_showed.get(TAB_FANS_LIST, False):
            self.refresh_tab_tips(TAB_FANS_LIST)
            self._tab_tip_showed[TAB_FANS_LIST] = True

    def init_tab(self):
        list_tab = self.panel.nd_follow.nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        for tab_index in range(len(TAB_MAP)):
            tab = list_tab.AddTemplateItem()
            self.add_touch_tab(tab, tab_index)
            self.refresh_tab_tips(tab_index)
            self.refresh_tab_title(tab_index)

        self._tab_panels[TAB_SEARCH_LIST] = FollowSearchResult(self.panel.nd_follow)
        self._input_box = InputBox.InputBox(self.panel.temp_search, placeholder=get_text_by_id(19453), clear_btn_cb=self.on_clear_input_box, max_length=MaxSearchTextLength)
        self._input_box.set_rise_widget(self.main_panel)

        @self.panel.btn_search.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_search()

    def refresh_tab_tips(self, tab_index):
        nd_new_fans_vis = False
        tab = self._tabs[tab_index]
        if tab_index == TAB_FANS_LIST:
            latest_add_count = global_data.player.get_latest_add_fans_count()
            if latest_add_count > 0:
                tab.lab_new_fans.setString('+' + format_popular_num(latest_add_count))
                nd_new_fans_vis = True
        tab.nd_new_fans.setVisible(nd_new_fans_vis)

    def refresh_tab_title(self, index):
        num = index == TAB_FOLLOW_LIST and global_data.player.get_follow_player_count() if 1 else global_data.player.get_fans_count()
        text = get_text_by_id(TAB_MAP[index]['tab_name'])
        if num > 0:
            text += ' (' + str(format_popular_num(num)) + ') '
        tab = self._tabs[index]
        tab.btn_tab.SetText(text)

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
        search_panel = self._tab_panels[TAB_SEARCH_LIST]
        if search_panel:
            search_panel.hide_panel()
        self._input_box.set_text('')
        tab = self._tabs.get(tab_index, None)
        tab.btn_tab.SetSelect(True)
        tab.img_vx.setVisible(True)
        tab.PlayAnimation('click')
        tab.nd_new_fans.setVisible(False)
        tab_panel = self._tab_panels.get(tab_index, None)
        if tab_panel is None:
            tab_panel = TAB_MAP[tab_index]['ui_class'](self.panel.nd_follow)
            self._tab_panels[tab_index] = tab_panel
        tab_panel.show_panel()
        self.panel.PlayAnimation('show')
        self._cur_tab_index = tab_index
        return

    def set_visible(self, visible):
        self.panel.setVisible(visible)
        if visible:
            self.touch_tab_by_index(TAB_FOLLOW_LIST)

    def destroy(self):
        self.main_panel = None
        self.panel = None
        self._message_data = None
        self._cur_tab_index = None
        self._tabs.clear()
        self._tab_tip_showed.clear()
        for panel in six.itervalues(self._tab_panels):
            panel.destroy()

        self._tab_panels.clear()
        self.process_event(False)
        if global_data.player:
            global_data.player.clear_fans_system_cached_player_info()
            global_data.player.update_last_fans_count(global_data.player.get_fans_count())
        return

    def hide_inputbox(self):
        pass

    def on_click_btn_search(self):
        search_panel = self._tab_panels[TAB_SEARCH_LIST]
        cur_panel = self._tab_panels[self._cur_tab_index]
        if not search_panel or not cur_panel:
            return
        input_text = self._input_box.get_text() or ''
        input_player_uid, input_player_name = get_input_box_search_item(input_text, MaxSearchTextLength)
        if not input_player_uid and not input_player_name:
            global_data.game_mgr.show_tip(get_text_by_id(2175))
            return
        if self._cur_tab_index == TAB_FOLLOW_LIST:
            info_type = const.FANS_SYSTEM_INFO_TYPE_FOLLOWS if 1 else const.FANS_SYSTEM_INFO_TYPE_FANS
            if input_player_uid:
                G_IS_NA_USER or input_player_uid += global_data.uid_prefix
            global_data.player.search_fans_system_player_info_by_uid(info_type, input_player_uid)
        elif input_player_name:
            global_data.player.search_fans_system_player_info_by_name(info_type, input_player_name)
        if self._cur_tab_index != TAB_SEARCH_LIST:
            cur_panel.hide_panel()
        search_panel.show_panel()

    def on_clear_input_box(self):
        pass

    def get_friend_list(self):
        cur_panel = self._tab_panels.get(self._cur_tab_index)
        if not cur_panel:
            return
        return cur_panel.get_friend_list()

    def get_cur_tab(self):
        return self._tab_panels.get(self._cur_tab_index)
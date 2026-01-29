# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveMainUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
import logic.comsys.common_ui.InputBox as InputBox
from logic.comsys.live.LiveRecommendPageWidget import LiveRecommendPageWidget
from logic.comsys.live.LiveFriendPageWidget import LiveFriendPageWidget
from logic.comsys.live.LiveFollowPageWidget import LiveFollowPageWidget
from logic.comsys.live.LiveSearchPageWidget import LiveSearchPageWidget
from logic.comsys.live.LiveMirrativPageWidget import LiveMirrativPageWidget
from logic.comsys.live.LiveCompetitionPageWidget import LiveCompetitionPageWidget
import logic.gcommon.time_utility as t_util
from logic.gutils.follow_utils import get_input_box_search_item
import common.const.uiconst
from logic.gcommon.common_const.lang_data import LANG_JA
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from common.platform.dctool import interface
from common.utils.time_utils import get_time
from common.utils.timer import CLOCK
from logic.gcommon.common_const import liveshow_const as live_sc
RECOMMEND_PAGE_INDEX = 0
SEARCH_PAGE_INDEX = 3
COMPETITION_PAGE_INDEX = 4
REFRESH_TIME_MIN_INTERVAL = 5
MaxSearchTextLength = 30
TAB_MAP = {RECOMMEND_PAGE_INDEX: {'tab_name': 12069,'ui_class': LiveRecommendPageWidget,'spectate_type': sp_const.SPECTATE_LIST_RECOMMEND,'other_spectate_type': sp_const.SPECTATE_LIST_COMPETITION},1: {'tab_name': 10259,'ui_class': LiveFriendPageWidget,'spectate_type': sp_const.SPECTATE_LIST_FRIEND},2: {'tab_name': 15818,'ui_class': LiveFollowPageWidget,'spectate_type': sp_const.SPECTATE_LIST_FOLLOW},SEARCH_PAGE_INDEX: {'tab_name': 15818,'ui_class': LiveSearchPageWidget,'spectate_type': sp_const.SPECTATE_LIST_SEARCH},4: {'tab_name': 19473,'ui_class': LiveMirrativPageWidget,'spectate_type': sp_const.SPECTATE_LIVE_MIRRATIV,'language': LANG_JA}}

class LiveMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'live/live_main_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {}
    UI_VKB_TYPE = UI_VKB_CLOSE
    CHECK_COMPETITION_INTERVAL = 30
    GLOBAL_EVENT = {'notify_platform_live_list_update_event': 'update_live_show_data',
       'live_platform_inited_event': 'on_platform_inited'
       }

    def on_init_panel(self):
        self._live_widget = None
        self.left_tab_index = 0
        self.init_parameters()
        self.process_event(True)
        self.init_close_node()
        self.init_panel()
        self.init_left_tab_list()
        self.left_tab_list.set_tab_selected(self.left_tab_index)
        self.init_tab_list()
        self.hide_main_ui()
        self.on_click_tab_page(RECOMMEND_PAGE_INDEX)
        self._check_competition_timer = global_data.game_mgr.register_logic_timer(self._check_competition_cb, interval=self.CHECK_COMPETITION_INTERVAL, times=-1, mode=CLOCK)
        self._check_competition_cb()
        global_data.emgr.on_open_live_main_ui.emit()
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.StopTimerAction()
        self.destroy_widget('left_tab_list')
        self.destroy_widget('_live_widget')
        for tab_index, widget in six.iteritems(self._tab_2_widget):
            widget.on_finalize_panel()

        self._tab_2_widget = {}
        self._spectate_type_2_widget = {}
        self._brief_info_ready_set = set()
        self._last_refresh_time = None
        self.get_bg_ui() and self.get_bg_ui().close()
        self.bg_ui = None
        self._tab_panels = {}
        global_data.player and global_data.player.clear_global_spectate_cached()
        self.show_main_ui()
        self._safely_unregist_check_competition_timer()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {'on_received_global_spectate_list': self.on_received_global_spectate_list,
           'on_received_global_spectate_brief_list': self.on_received_global_spectate_brief_list,
           'net_disconnect_event': self.close,
           'on_cancel_loading_spectate': self.on_cancel_loading_spectate
           }
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def _safely_unregist_check_competition_timer(self):
        if self._check_competition_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self._check_competition_timer)
        self._check_competition_timer = None
        return

    def init_close_node(self):

        @self.panel.temp_back.btn_back.callback()
        def OnClick(btn, touch):
            self.close()

    def get_bg_ui(self):
        if self.bg_ui and self.bg_ui.is_valid():
            return self.bg_ui

    def do_hide_panel(self):
        super(LiveMainUI, self).do_hide_panel()
        self.get_bg_ui() and self.get_bg_ui().add_hide_count(self.__class__.__name__)
        self.show_main_ui()

    def do_show_panel(self):
        super(LiveMainUI, self).do_show_panel()
        self.get_bg_ui() and self.get_bg_ui().add_show_count(self.__class__.__name__)
        self.hide_main_ui()

    def init_panel(self):
        self.panel.temp_search.setVisible(False)
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', common.const.uiconst.BG_ZORDER)
        self.bg_ui.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/common/bg/img_live_bg.png')

        @self.panel.btn_refresh.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_refresh()

    def init_parameters(self):
        self._tab_2_widget = {}
        self._tab_panels = {}
        self._cur_tab_index = -1
        self._spectate_type_2_widget = {}
        self._brief_info_ready_set = set()
        self._last_refresh_time = None
        self.bg_ui = None
        self._check_competition_timer = None
        self._prev_competition_check_time = 0
        self.left_tab_list = None
        self.in_require_mainland_live_list = []
        self.valid_mainland_list = []
        self._in_init_left_tab = False
        self._target_live_platform_type = None
        return

    def init_tab_list(self):
        self._tab_panels = {}
        tab_list = self.panel.list_tab_2
        tab_list.DeleteAllSubItem()
        for tab_index in range(len(TAB_MAP)):
            tab_data = TAB_MAP[tab_index]
            language = tab_data.get('language', None)
            if language is not None and get_cur_text_lang() != language:
                continue
            if tab_index == SEARCH_PAGE_INDEX:
                continue
            btn_tab = tab_list.AddTemplateItem()
            btn_tab.btn_tab.SetText(tab_data['tab_name'])
            self._tab_panels[tab_index] = btn_tab
            btn_tab.btn_tab.EnableCustomState(True)

            @btn_tab.btn_tab.unique_callback()
            def OnClick(btn, touch, index=tab_index):
                self.on_click_tab_page(index)

        return

    def init_tab_widget(self, tab_index):
        if tab_index in self._tab_2_widget:
            return
        else:
            if tab_index not in TAB_MAP:
                return
            tab_data = TAB_MAP[tab_index]
            spectate_type = tab_data['spectate_type']
            other_spectate_type = tab_data.get('other_spectate_type', None)
            widget = tab_data['ui_class'](self.panel, spectate_type)
            if other_spectate_type:
                widget.set_other_spectate_type(other_spectate_type)
            widget.init_panel()
            self._tab_2_widget[tab_index] = widget
            self._spectate_type_2_widget[spectate_type] = widget
            return

    def on_click_tab_page(self, tab_index):
        if self._cur_tab_index == tab_index:
            return
        if self._cur_tab_index != tab_index:
            tab_panel = self._tab_panels.get(self._cur_tab_index)
            if tab_panel:
                tab_panel.btn_tab.SetSelect(False)
            cur_page = self._tab_2_widget.get(self._cur_tab_index)
            if cur_page:
                cur_page.hide_panel()
        tab_panel = self._tab_panels.get(tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(True)
        self._cur_tab_index = tab_index
        widget = self._tab_2_widget.get(tab_index)
        if not widget:
            self.init_tab_widget(tab_index)
            widget = self._tab_2_widget.get(tab_index)
        widget.show_panel()
        spectate_type = widget.get_spectate_type()
        if spectate_type not in (sp_const.SPECTATE_LIVE_MIRRATIV,):
            global_data.player and global_data.player.request_global_spectate_brief_list(spectate_type)
        btn_refresh_vis = True
        nd_common_vis = True
        tmp_list_nd_vis = True
        if spectate_type == sp_const.SPECTATE_LIST_FOLLOW:
            btn_refresh_vis = False
            nd_common_vis = False
        elif spectate_type == sp_const.SPECTATE_LIST_FRIEND:
            nd_common_vis = False
        elif spectate_type == sp_const.SPECTATE_LIVE_MIRRATIV:
            nd_common_vis = False
            tmp_list_nd_vis = False
        elif spectate_type == sp_const.SPECTATE_LIST_COMPETITION:
            nd_common_vis = False
        self.panel.temp_list.setVisible(tmp_list_nd_vis)
        self.panel.btn_refresh.setVisible(btn_refresh_vis)
        self.panel.nd_common.setVisible(nd_common_vis)
        self.check_and_show_empty_nd()

    def on_received_global_spectate_brief_list(self, list_type):
        self._brief_info_ready_set.add(list_type)
        cur_page = self._tab_2_widget.get(self._cur_tab_index)
        widget = self._spectate_type_2_widget.get(list_type)
        if widget:
            if widget.get_other_spectate_type() in self._brief_info_ready_set or widget.get_other_spectate_type() is None or widget.get_youtube_data():
                if cur_page and cur_page.get_spectate_type() == list_type and list_type != sp_const.SPECTATE_LIST_SEARCH:
                    need_refresh_ui = True if 1 else False
                    widget.refresh_content_with_brief(refresh_ui=need_refresh_ui)
            if global_data.player.get_global_specate_brief_info(list_type):
                if list_type == sp_const.SPECTATE_LIST_COMPETITION and self._has_competitions():
                    for other_widget in six.itervalues(self._spectate_type_2_widget):
                        if other_widget and other_widget != widget:
                            if other_widget.get_other_spectate_type() == list_type and cur_page and cur_page.get_spectate_type() == list_type and list_type != sp_const.SPECTATE_LIST_SEARCH:
                                need_refresh_ui = True if 1 else False
                                other_widget.refresh_content_with_brief(refresh_ui=need_refresh_ui)

            self.check_and_show_empty_nd()
            if list_type == sp_const.SPECTATE_LIST_COMPETITION and self._has_competitions():
                self._safely_unregist_check_competition_timer()
        return

    def on_received_global_spectate_list(self, list_type, list_info):
        cur_page = self._tab_2_widget.get(self._cur_tab_index)
        widget = self._spectate_type_2_widget.get(list_type)
        if widget and cur_page and cur_page.get_spectate_type() == list_type and list_type == sp_const.SPECTATE_LIST_SEARCH:
            need_refresh_ui = True if 1 else False
            widget.refresh_content_with_details(list_type, list_info, refresh_ui=need_refresh_ui)
        if list_info:
            for other_widget in six.itervalues(self._spectate_type_2_widget):
                if other_widget and other_widget != widget:
                    if other_widget.get_other_spectate_type() == list_type and cur_page and cur_page.get_spectate_type() == list_type and list_type == sp_const.SPECTATE_LIST_SEARCH:
                        need_refresh_ui = True if 1 else False
                        other_widget.refresh_content_with_details(list_type, list_info, refresh_ui=need_refresh_ui)

        self.check_and_show_empty_nd()

    def on_click_btn_refresh(self):
        if self._last_refresh_time and t_util.get_time() - self._last_refresh_time < REFRESH_TIME_MIN_INTERVAL:
            global_data.game_mgr.show_tip(get_text_by_id(15806))
            return
        ls = [
         sp_const.SPECTATE_LIST_COMPETITION, sp_const.SPECTATE_LIST_RECOMMEND]
        for sp_type in ls:
            global_data.player.request_global_spectate_brief_list(sp_type)
            if sp_type in self._brief_info_ready_set:
                self._brief_info_ready_set.remove(sp_type)

        if self._cur_tab_index != RECOMMEND_PAGE_INDEX:
            self.on_click_tab_page(RECOMMEND_PAGE_INDEX)
        self._last_refresh_time = t_util.get_time()
        self.panel.btn_refresh.SetShowEnable(False)
        self.panel.DelayCall(REFRESH_TIME_MIN_INTERVAL, self._tick_refresh)

    def _tick_refresh(self):
        if self._last_refresh_time and t_util.get_time() - self._last_refresh_time >= REFRESH_TIME_MIN_INTERVAL:
            self.panel.btn_refresh.SetShowEnable(True)

    def check_and_show_empty_nd(self):
        cur_widget = self._tab_2_widget.get(self._cur_tab_index)
        if not cur_widget:
            return
        if cur_widget.get_real_content_size() <= 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.lab_empty.setString(cur_widget.get_empty_content_text())
        else:
            self.panel.nd_empty.setVisible(False)

    def on_cancel_loading_spectate(self):
        self.on_click_tab_page(RECOMMEND_PAGE_INDEX)

    def _has_competitions(self):
        from logic.gutils.spectate_utils import has_live_competitions
        return has_live_competitions()

    def _check_competition_cb(self):
        if get_time() - self._prev_competition_check_time < REFRESH_TIME_MIN_INTERVAL:
            return
        self._prev_competition_check_time = get_time()
        global_data.player and global_data.player.request_global_spectate_brief_list(sp_const.SPECTATE_LIST_COMPETITION)

    def init_left_tab_list(self):
        self._in_init_left_tab = True
        self.init_tab_data()
        from logic.gutils.new_template_utils import CommonLeftTabList
        self.left_tab_list = CommonLeftTabList(self.panel.list_tab, self.tab_list, None, self.click_left_tab_btn)
        self._in_init_left_tab = False
        return

    def init_tab_data(self):
        self.tab_list = [{'frame': 'gui/ui_res_2/txt_pic/text_pic_cn/img_live_tab_smc.png'}]
        if interface.is_mainland_package():
            mainland_list = [{'frame': 'gui/ui_res_2/live/img_live_tab_cc.png','live_ty': live_sc.CC_LIVE}, {'frame': 'gui/ui_res_2/live/img_live_tab_kuaishou.png','live_ty': live_sc.KUAISHOU_LIVE}, {'frame': 'gui/ui_res_2/live/img_live_tab_douyu.png','live_ty': live_sc.DOUYU_LIVE}, {'frame': 'gui/ui_res_2/live/img_live_tab_huya.png','live_ty': live_sc.HUYA_LIVE}, {'frame': 'gui/ui_res_2/live/img_live_tab_bilibili.png','live_ty': live_sc.BILIBILI_LIVE}]
            valid_mainland_list = []
            need_require_list = []
            has_data_list = []
            for live_channel in mainland_list:
                live_ty = live_channel.get('live_ty')
                if global_data.player.enable_live(live_ty):
                    valid_mainland_list.append(live_channel)
                    if not self.has_live_platform_data(live_ty):
                        need_require_list.append(live_ty)
                    else:
                        has_data_list.append(live_channel)

            self.valid_mainland_list = valid_mainland_list
            self.in_require_mainland_live_list = list(need_require_list)
            self.tab_list.extend(has_data_list)
            for live_ty in need_require_list:
                self.require_live_platform_page(live_ty)

    def has_live_platform_data(self, live_ty):
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        platform = LivePlatformManager().get_platform_by_type(live_ty)
        if platform:
            start_page = platform.get_start_page()
            new_live_list = platform.get_all_live_list(start_page)
            if not new_live_list:
                return False
            else:
                return True

        return False

    def require_live_platform_page(self, live_ty):
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        platform = LivePlatformManager().get_platform_by_type(live_ty)
        if platform and platform.is_inited():
            start_page = platform.get_start_page()
            platform.request_all_live_list(start_page)

    def click_left_tab_btn(self, index):
        if index == self.left_tab_index:
            return
        self.left_tab_index = index
        if index < len(self.tab_list):
            tab_data = self.tab_list[index]
            ty = tab_data.get('type')
            self.update_show()
        return True

    def update_show(self):
        if self.left_tab_index >= len(self.tab_list):
            return
        tab_data = self.tab_list[self.left_tab_index]
        if self.left_tab_index == 0:
            self.panel.nd_observe.setVisible(True)
            self.panel.nd_live.setVisible(False)
        else:
            self.panel.nd_observe.setVisible(False)
            self.panel.nd_live.setVisible(True)
            live_type = tab_data.get('live_ty')
            if not self._live_widget:
                self.init_live_widget()
            self._live_widget.set_select_platform(live_type)

    def init_live_widget(self):
        from logic.comsys.live.LiveSteamMainUI import LiveSteamMainWidget
        panel = global_data.uisystem.load_template_create('live/i_live_broadcast', self.panel.nd_live, name='nd_content')
        self._live_widget = LiveSteamMainWidget(self, panel)

    def update_live_show_data(self, live_type):
        if self.in_require_mainland_live_list:
            if live_type in self.in_require_mainland_live_list:
                self.in_require_mainland_live_list.remove(live_type)
            if not self.in_require_mainland_live_list:

                def check_in_tab_list(live_channel):
                    target_ty = live_channel.get('live_ty')
                    for i in self.tab_list:
                        if target_ty == i.get('live_ty'):
                            return True

                    return False

                from logic.gutils.new_template_utils import CommonLeftTabList
                have_data_list = []
                for live_channel in self.valid_mainland_list:
                    live_ty = live_channel.get('live_ty')
                    if self.has_live_platform_data(live_ty):
                        have_data_list.append(live_channel)

                for live_channel in have_data_list:
                    if not check_in_tab_list(live_channel):
                        self.tab_list.append(live_channel)

                self.left_tab_list and self.left_tab_list.set_tab_selected(None)
                self.destroy_widget('left_tab_list')
                if not self._in_init_left_tab:
                    self.left_tab_list = CommonLeftTabList(self.panel.list_tab, self.tab_list, None, self.click_left_tab_btn)
                    self.check_update_left_selected_index()
                    self.left_tab_list.set_tab_selected(self.left_tab_index)
                if not self._live_widget:
                    self.init_live_widget()
                    self.update_show()
        return

    def on_platform_inited(self, plat_type):
        if plat_type in self.in_require_mainland_live_list:
            self.require_live_platform_page(plat_type)

    def check_change_tab_force(self):
        from logic.comsys.lobby.EntryWidget.LotterySummerPeakLiveEntryWidget import check_show_entry, check_summer_peak_live_red_point
        if check_show_entry():
            if check_summer_peak_live_red_point():
                self.change_tab_force(live_sc.HUYA_LIVE)

    def change_tab_force(self, platform_type):
        if not self.has_live_platform_data(platform_type):
            self.require_live_platform_page(platform_type)
        if global_data.player.enable_live(platform_type):
            in_tab_list_index = self.get_in_tab_list_index(platform_type)
            if in_tab_list_index is not None:
                self.left_tab_list.select_tab_btn(in_tab_list_index)
            else:
                self._target_live_platform_type = platform_type
        return

    def check_update_left_selected_index(self):
        if self._target_live_platform_type is not None:
            for i, live_channel in enumerate(self.tab_list):
                if live_channel.get('live_ty') == self._target_live_platform_type:
                    self.left_tab_index = i
                    self._target_live_platform_type = None
                    break

        return

    def get_in_tab_list_index(self, platform_type):
        for i, live_data in enumerate(self.tab_list):
            if platform_type == live_data.get('live_ty'):
                return i

        return None
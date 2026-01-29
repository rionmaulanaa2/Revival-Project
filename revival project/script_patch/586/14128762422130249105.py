# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanMainUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER, NORMAL_LAYER_ZORDER_0, UI_VKB_CLOSE
from logic.gutils import clan_utils
from logic.comsys.clan.ClanInActiveConfirm import ClanInActiveConfirm
from logic.gcommon.time_utility import get_rela_month_no

class ClanMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'crew/crew_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'close'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected',
       'clan_task_day_reward': 'refresh_red_point',
       'clan_members_request_list': 'refresh_red_point',
       'clan_task_week_reward': 'refresh_red_point',
       'player_info_update_event': 'refresh_red_point',
       'clan_rank_reward': 'refresh_red_point',
       'receive_task_reward_succ_event': 'refresh_red_point',
       'task_prog_changed': 'refresh_red_point'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.init_tab_type = 0
        self._tab_list = clan_utils.get_created_page_list()
        self.delay_select_timer = None
        self.hide_main_ui()
        global_data.ui_mgr.show_ui('ClanFullScreenBg', 'logic.comsys.clan')
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', BG_ZORDER)
        self.init_parameters()
        self.init_widget()
        if clan_utils.get_permission('audit_permission_titles'):
            global_data.player.request_clan_request()
        self.panel.PlayAnimation('show')
        self.check_is_active_clan()
        return

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('ClanFullScreenBg')
        if self.bg_ui:
            self.bg_ui.close()
            self.bg_ui = None
        self.show_main_ui()
        for index, page_inst in six.iteritems(self._view_page_widgets):
            page_inst.on_finalize_panel()

        self._view_page_widgets = {}
        return

    def do_hide_panel(self):
        super(ClanMainUI, self).do_hide_panel()
        bg_ui = global_data.ui_mgr.get_ui('ClanFullScreenBg')
        if bg_ui:
            bg_ui.do_hide_panel()
        if self.bg_ui:
            self.bg_ui.do_hide_panel()

    def do_show_panel(self):
        super(ClanMainUI, self).do_show_panel()
        self.show_bg()

    def show_bg(self):
        if self._cur_index < 0:
            return
        else:
            if self._cur_index == 0:
                bg_ui = global_data.ui_mgr.get_ui('ClanFullScreenBg')
                if bg_ui:
                    bg_ui.do_show_panel()
                if self.bg_ui:
                    self.bg_ui.do_hide_panel()
            elif self._cur_index == 4:
                bg_ui = global_data.ui_mgr.get_ui('ClanFullScreenBg')
                if bg_ui:
                    bg_ui.do_hide_panel()
                if self.bg_ui:
                    self.bg_ui.do_hide_panel()
                page_inst = self._view_page_widgets.get(self._cur_index, None)
                if page_inst:
                    page_inst.set_show(True)
            else:
                bg_ui = global_data.ui_mgr.get_ui('ClanFullScreenBg')
                if bg_ui:
                    bg_ui.do_hide_panel()
                if self.bg_ui:
                    self.bg_ui.do_show_panel()
            return

    def init_parameters(self):
        self._cur_index = -1
        self._view_page_widgets = {}

    def init_widget(self):
        self.init_page_tab()

    def get_tab_index(self, page_key):
        if not self._tab_list:
            return 0
        for i, info in enumerate(self._tab_list):
            if info['key'] == page_key:
                return i

        return 0

    def select_tab(self, page_key):
        if not self.panel:
            return
        else:
            index = self.get_tab_index(page_key)
            tablist = self.panel.temp_left_tab.tab_list
            item_widget = tablist.GetItem(index)
            item_widget.btn.OnClick(None)
            return

    def _on_login_reconnected(self, *args):
        self.close()

    def refresh_red_point(self, *args):
        tab_list = self._tab_list
        tablist = self.panel.temp_left_tab.tab_list
        for index, info in enumerate(tab_list):
            item_widget = tablist.GetItem(index)
            if info['key'] == clan_utils.CLAN_TASK_LIST:
                item_widget.img_red.setVisible(clan_utils.get_clan_task_redpoint_count() > 0)
            elif info['key'] == clan_utils.CLAN_RANK_BOARD:
                item_widget.img_red.setVisible(clan_utils.get_clan_rank_reward_count() > 0)
            elif info['key'] == clan_utils.CLAN_APPLY_LIST:
                item_widget.img_red.setVisible(clan_utils.get_clan_apply_count() > 0)
            else:
                item_widget.img_red.setVisible(False)

    def on_init_tab_widget(self, item_widget, index, info):
        tablist = self.panel.temp_left_tab.tab_list
        item_widget.lab_main.SetString(info['name'])
        item_widget.lab_main.SetColor('#DD')
        item_widget.btn.EnableCustomState(True)

        @item_widget.btn.unique_callback()
        def OnClick(btn, touch):
            if self._cur_index >= 0:
                last_item_widget = tablist.GetItem(self._cur_index)
                last_item_widget.btn.SetSelect(False)
                last_item_widget.lab_main.SetColor('#DD')
                last_item_widget.StopAnimation('continue')
                last_item_widget.RecoverAnimationNodeState('continue')
            item_widget.btn.SetSelect(True)
            item_widget.lab_main.SetColor('#SW')
            item_widget.PlayAnimation('click')
            item_widget.RecordAnimationNodeState('continue')
            item_widget.PlayAnimation('continue')
            last_page_inst = self._view_page_widgets.get(self._cur_index, None)
            if last_page_inst:
                last_page_inst.set_show(False)
            self._cur_index = index
            page_inst = self._view_page_widgets.get(index, None)
            if not page_inst:
                ui_template = info['template']
                ui_class = clan_utils.get_clan_cls(info['class'])
                unique_nodename = '_sub_page_widget{}'.format(index)
                dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.temp_content, name=unique_nodename)
                page_inst = ui_class(dlg)
                page_inst.on_init_panel()
                self._view_page_widgets[index] = page_inst
            else:
                page_inst.refresh_panel()
            page_inst.set_show(True)
            self.show_bg()
            return

    def init_page_tab(self, refresh_list=False):
        from common.utils import timer
        if refresh_list:
            tab_list = clan_utils.get_created_page_list()
            if len(tab_list) == len(self._tab_list):
                return
            self._tab_list = clan_utils.get_created_page_list()
        tab_list = self._tab_list
        tablist = self.panel.temp_left_tab.tab_list
        tablist.SetInitCount(len(tab_list))
        for index, info in enumerate(tab_list):
            item_widget = tablist.GetItem(index)
            self.on_init_tab_widget(item_widget, index, info)

        self.refresh_red_point()
        if not refresh_list:
            self.delay_select_timer and global_data.game_mgr.get_logic_timer().unregister(self.delay_select_timer)
            self.delay_select_timer = global_data.game_mgr.get_logic_timer().register(func=lambda : self.select_tab(self.init_tab_type), times=1, mode=timer.CLOCK, interval=0.05)

    def check_is_active_clan(self):
        if not global_data.player:
            return False
        else:
            months = global_data.achi_mgr.get_cur_user_archive_data('ignore_clan_inactive_confirm', -1)
            if months == get_rela_month_no():
                return False
            is_quit = global_data.player.is_advise_quit_clan()
            if is_quit:
                have_click_clan = getattr(global_data, 'have_click_clan_btn', None)
                if not have_click_clan:
                    setattr(global_data, 'have_click_clan_btn', True)
                    global_data.ui_mgr.show_ui('ClanInActiveConfirm', 'logic.comsys.clan')
            return
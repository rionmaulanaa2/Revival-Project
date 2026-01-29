# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanJoinMainUI.py
from __future__ import absolute_import
import six
from logic.gutils import clan_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from common.const.uiconst import BG_ZORDER

class ClanJoinMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'crew/crew_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': '_on_click_back'
       }
    GLOBAL_EVENT = {'net_login_reconnect_event': '_on_login_reconnected',
       'create_clan_success': '_on_create_clan_success',
       'create_join_success': '_on_create_clan_success'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.hide_main_ui()
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', BG_ZORDER)
        self.init_parameters()
        self.init_widget()
        self.panel.PlayAnimation('show')

    def on_finalize_panel(self):
        self.show_main_ui()
        for index, page_inst in six.iteritems(self._view_page_widgets):
            page_inst.on_finalize_panel()

        if self.bg_ui and self.bg_ui.is_valid():
            self.bg_ui.close()
        self._view_page_widgets = {}

    def do_show_panel(self):
        super(ClanJoinMainUI, self).do_show_panel()
        self.show_bg()

    def show_bg(self):
        if self._cur_index < 0:
            return
        else:
            if self._cur_index == 2:
                if self.bg_ui:
                    self.bg_ui.do_hide_panel()
                page_inst = self._view_page_widgets.get(self._cur_index, None)
                if page_inst:
                    page_inst.set_show(True)
            elif self.bg_ui:
                self.bg_ui.do_show_panel()
            return

    def init_parameters(self):
        self._cur_index = -1
        self._view_page_widgets = {}
        self._closing = False

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
        index = self.get_tab_index(page_key)
        tablist = self.panel.temp_left_tab.tab_list
        item_widget = tablist.GetItem(index)
        item_widget.btn.OnClick(None)
        return

    def _on_login_reconnected(self, *args):
        self.close()

    def _on_create_clan_success(self):
        self.close()
        global_data.player.request_clan_info(open_ui=True)

    def on_init_tab_widget(self, item_widget, index, info):
        tab_lst = self.panel.temp_left_tab.tab_list
        item_widget.lab_main.SetString(info['name'])
        item_widget.btn.EnableCustomState(True)

        @item_widget.btn.unique_callback()
        def OnClick(btn, touch):
            if self._cur_index >= 0:
                last_item_widget = tab_lst.GetItem(self._cur_index)
                last_item_widget.btn.SetSelect(False)
                last_item_widget.lab_main.SetColor('#DD')
                last_item_widget.StopAnimation('continue')
                last_item_widget.RecoverAnimationNodeState('continue')
            item_widget.btn.SetSelect(True)
            item_widget.PlayAnimation('click')
            item_widget.RecordAnimationNodeState('continue')
            item_widget.PlayAnimation('continue')
            item_widget.lab_main.SetColor('#SW')
            last_page_inst = self._view_page_widgets.get(self._cur_index, None)
            if last_page_inst:
                last_page_inst.set_show(False)
            self._cur_index = index
            page_inst = self._view_page_widgets.get(index, None)
            if not page_inst:
                ui_template = info['template']
                ui_class = clan_utils.get_clan_cls(info['class'])
                unique_node_name = '_sub_page_widget{}'.format(index)
                dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.temp_content, name=unique_node_name)
                page_inst = ui_class(dlg)
                page_inst.on_init_panel()
                self._view_page_widgets[index] = page_inst
            else:
                page_inst.refresh_panel()
            page_inst.set_show(True)
            self.show_bg()
            return

    def init_page_tab(self):
        self._tab_list = clan_utils.get_uncreated_page_list()
        tab_lst = self.panel.temp_left_tab.tab_list
        tab_lst.SetInitCount(len(self._tab_list))
        for index, info in enumerate(self._tab_list):
            item_widget = tab_lst.GetItem(index)
            self.on_init_tab_widget(item_widget, index, info)

        self.select_tab(0)

    def _on_click_back(self, *args):
        if self._closing:
            return
        self._closing = True
        self.close()
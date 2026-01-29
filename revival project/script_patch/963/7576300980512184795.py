# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanRankPage.py
from __future__ import absolute_import
import six
from logic.gutils import clan_utils
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const

class ClanRankPage(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {}
        super(ClanRankPage, self).__init__(dlg)

    def on_init_panel(self):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        super(ClanRankPage, self).on_init_panel()
        self._tab_list = clan_utils.get_clan_rank_page_list()
        self._view_page_widgets = {}
        self._cur_index = -1
        self.init_page_tab()
        self.panel.PlayAnimation('show')

    def set_show(self, show):
        super(ClanRankPage, self).set_show(show)
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.BATTLE_PASS, scene_content_type=scene_const.SCENE_CLAN_RANK)

    def on_finalize_panel(self):
        super(ClanRankPage, self).on_finalize_panel()
        for index, page_inst in six.iteritems(self._view_page_widgets):
            page_inst.on_finalize_panel()

        self._view_page_widgets = {}
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()

    def refresh_panel(self):
        super(ClanRankPage, self).refresh_panel()

    def get_tab_index(self, page_key):
        if not self._tab_list:
            return 0
        for i, info in enumerate(self._tab_list):
            if info['key'] == page_key:
                return i

        return 0

    def select_tab(self, page_key):
        index = self.get_tab_index(page_key)
        tablist = self.panel.pnl_list_top_tab
        item_widget = tablist.GetItem(index)
        item_widget.btn_tab.OnClick(None)
        return

    def on_tab_widget(self, item_widget, index, info):
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
        return

    def init_page_tab(self):
        from logic.gutils import new_template_utils
        tab_list = self._tab_list
        data_list = []
        for index, info in enumerate(tab_list):
            data_list.append({'text': info['name']})

        def callback(item_widget, index):
            self.on_tab_widget(item_widget, index, tab_list[index])

        new_template_utils.init_top_tab_list(self.panel.pnl_list_top_tab, data_list, callback)
        self.select_tab(0)
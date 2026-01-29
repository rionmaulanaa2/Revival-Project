# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TeamHall/TeamHallUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.new_template_utils import CommonLeftTabList

def get_page_cls(cls_name):
    mod = __import__('logic.comsys.lobby.TeamHall.%s' % cls_name, globals(), locals(), [cls_name])
    cls = getattr(mod, cls_name, None)
    return cls


TEAM_LSIT = 0
TEAM_RECRUIT = 1
TAB_LIST = [{'key': TEAM_LSIT,'name': 13126,'template': 'lobby/i_team_hall','class': 'TeamHallList'}, {'key': TEAM_RECRUIT,'name': 13127,'template': 'lobby/i_team_recruit','class': 'TeamRecruitUI'}]

class TeamHallUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/team_up'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn'
       }
    GLOBAL_EVENT = {}

    def on_click_back_btn(self, *args):
        self.close(*args)

    def on_init_panel(self, *args, **kargs):
        self._tab_list = TAB_LIST
        self._view_page_widgets = {}
        self._cur_index = -1
        self.hide_main_ui()
        self.init_page_tab()

    def on_finalize_panel(self):
        for index, page_inst in six.iteritems(self._view_page_widgets):
            page_inst.on_finalize_panel()

        self.show_main_ui()
        self._view_page_widgets = {}

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

    def init_page_tab(self):
        tab_list = self._tab_list
        tablist = self.panel.temp_left_tab.tab_list
        tablist.SetInitCount(len(tab_list))
        for index, info in enumerate(tab_list):
            item_widget = tablist.GetItem(index)
            self.on_init_tab_widget(item_widget, index, info)

        self.refresh_red_point()
        self.select_tab(TEAM_LSIT)

    def on_init_tab_widget(self, item_widget, index, info):
        tablist = self.panel.temp_left_tab.tab_list
        item_widget.btn.SetText(get_text_by_id(info['name']))
        item_widget.btn.EnableCustomState(True)

        @item_widget.btn.unique_callback()
        def OnClick(btn, touch):
            if self._cur_index >= 0:
                last_item_widget = tablist.GetItem(self._cur_index)
                last_item_widget.btn.SetSelect(False)
                last_item_widget.StopAnimation('continue')
                last_item_widget.RecoverAnimationNodeState('continue')
            item_widget.btn.SetSelect(True)
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
                ui_class = get_page_cls(info['class'])
                unique_nodename = '_sub_page_widget{}'.format(index)
                dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.nd_content, name=unique_nodename)
                page_inst = ui_class(dlg)
                page_inst.on_init_panel()
                self._view_page_widgets[index] = page_inst
            else:
                page_inst.refresh_panel()
            page_inst.set_show(True)
            return

    def refresh_red_point(self, *args):
        tab_list = self._tab_list
        tablist = self.panel.temp_left_tab.tab_list
        for index, info in enumerate(tab_list):
            item_widget = tablist.GetItem(index)

    def do_show_panel(self):
        super(TeamHallUI, self).do_show_panel()
        page_inst = self._view_page_widgets.get(self._cur_index, None)
        if page_inst and hasattr(page_inst, 'do_show_panel'):
            page_inst.do_show_panel()
        return

    def do_hide_panel(self):
        super(TeamHallUI, self).do_hide_panel()
        page_inst = self._view_page_widgets.get(self._cur_index, None)
        if page_inst and hasattr(page_inst, 'do_hide_panel'):
            page_inst.do_show_panel()
        return
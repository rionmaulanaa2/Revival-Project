# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/WindowCommonComponent.py
from __future__ import absolute_import
import weakref

class WindowCommonComponent(object):

    def __init__(self, panel):
        self.panel = panel
        self._cur_index = None
        self._on_tab_selected_func = None
        self._before_tab_selected_func = None
        return

    def init_common_panel(self, page_name, on_close=None, extra_info=None):
        from logic.gutils import template_utils
        template_utils.init_common_panel(self.panel, page_name, on_close)

    def jump_to_index(self, index):
        self.panel.list_tab.TopWithNode(self.panel.list_tab.GetItem(index))
        self.on_jump_to_index(index)

    def on_jump_to_index(self, index):
        if self._cur_index == index:
            return
        self._on_tab_selected(index)
        if self._on_tab_selected_func:
            func = self._on_tab_selected_func
            func(index)

    def destroy(self):
        self._on_tab_selected_func = None
        self._before_tab_selected_func = None
        self.panel = None
        return

    def init_tab_list(self, tab_data_list, on_tab_selected_func, before_tab_selected_func=None):
        tab_list = self.panel.list_tab
        self._on_tab_selected_func = on_tab_selected_func
        self._before_tab_selected_func = before_tab_selected_func
        tab_list.SetInitCount(len(tab_data_list))
        all_tab_widgets = tab_list.GetAllItem()
        for index, tab_data in enumerate(tab_data_list):
            text_id = tab_data.get('text_id', '')
            tab_widget = all_tab_widgets[index]
            button = tab_widget.btn_window_tab
            tab_widget.btn_window_tab.SetText(get_text_local_content(text_id))
            button.EnableCustomState(True)

            @button.unique_callback()
            def OnClick(btn, touch, index=index):
                if callable(self._before_tab_selected_func):

                    def resume():
                        self.on_jump_to_index(index)

                    if self._before_tab_selected_func(index, resume):
                        resume()
                else:
                    self.on_jump_to_index(index)

    def _on_tab_selected(self, index):
        if not self.panel:
            return
        else:
            tab_list = self.panel.list_tab
            if self._cur_index is not None:
                cur_tab = tab_list.GetItem(self._cur_index)
                if cur_tab:
                    cur_tab.btn_window_tab.SetSelect(False)
                    cur_tab.StopAnimation('continue')
                    cur_tab.RecoverAnimationNodeState('continue')
            self._cur_index = index
            cur_tab = tab_list.GetItem(index)
            if cur_tab:
                cur_tab.btn_window_tab.SetSelect(True)
                cur_tab.PlayAnimation('click')
                cur_tab.RecordAnimationNodeState('continue')
                cur_tab.PlayAnimation('continue')
            return
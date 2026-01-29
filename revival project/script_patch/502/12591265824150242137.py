# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/DeadSimpleTabList.py
from __future__ import absolute_import
from six.moves import range

class DeadSimpleTabList(object):

    def __init__(self, list_node, tab_node_refresher, on_tab_selected=None, on_tab_unselected=None):
        self._list_node = list_node
        self._tab_node_refresher = tab_node_refresher
        self._on_tab_selected_cb = on_tab_selected
        self._on_tab_unselected_cb = on_tab_unselected
        self._cur_selected_idx = -1

    def destroy(self):
        pass

    def refresh(self, tab_data_list):
        self._list_node.SetInitCount(len(tab_data_list))
        tab_node_list = self._list_node.GetAllItem()
        for idx, tab_data in enumerate(tab_data_list):
            tab_node = tab_node_list[idx]
            if callable(self._tab_node_refresher):
                multi_ret = self._tab_node_refresher(idx, tab_node, tab_data)
                if multi_ret is not None:
                    click_node, on_click = multi_ret
                    if click_node and callable(on_click):

                        def on_click_wrapper(btn, touch, _idx=idx):
                            on_click(btn, touch, _idx)
                            self.selectByIdx(_idx)

                        click_node.BindMethod('OnClick', on_click_wrapper)

        return

    def get_cur_selected_idx(self):
        return self._cur_selected_idx

    def selectByIdx(self, idx):
        if idx == self._cur_selected_idx:
            return
        item_node_cnt = self._list_node.GetItemCount()
        if idx < 0 or idx >= item_node_cnt:
            return
        for i in range(item_node_cnt):
            tab_node = self._list_node.GetItem(i)
            if i == idx:
                self._on_tab_selected(i, tab_node)
            else:
                self._on_tab_unselected(i, tab_node)

        self._cur_selected_idx = idx

    def select_by_user_defined_key(self, key):
        pass

    def _on_tab_selected(self, idx, tab_node):
        if callable(self._on_tab_selected_cb):
            self._on_tab_selected_cb(idx, tab_node)

    def _on_tab_unselected(self, idx, tab_node):
        if callable(self._on_tab_unselected_cb):
            self._on_tab_unselected_cb(idx, tab_node)
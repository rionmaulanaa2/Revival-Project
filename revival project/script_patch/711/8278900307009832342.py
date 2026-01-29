# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/items_book_ui/ItemsBookCommonChooseWidget.py
from __future__ import absolute_import
from logic.gutils import template_utils

class ItemsBookCommonChooseWidget(object):

    def __init__(self, widget, arrow, option_list, default_index, callback=None, max_height=None, close_cb=None, reverse=False, func_btn=None, text_nd=None, arrow_cb=None):
        self.arrow_rotation_cb = arrow_cb
        if func_btn:

            @func_btn.unique_callback()
            def OnClick(btn, touch):
                template_utils.init_common_choose_list_2(widget, arrow, option_list, self.on_choose, max_height, close_cb, reverse, func_btn, self.arrow_rotation_cb)
                func_btn.OnClick(None)
                return

        self._widget = widget
        self._widget.setVisible(False)
        self._arrow = arrow
        self._max_height = max_height
        self._close_cb = close_cb
        self._reverse = reverse
        self._index = None
        self.func_btn = func_btn
        self.text_nd = text_nd
        self.option_list = option_list
        self.callback = callback
        if default_index is not None:
            self.on_choose(default_index)
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'select_item_goods': self.on_select_item_goods
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self._widget = None
        self._arrow = None
        self._close_cb = None
        self.func_btn = None
        self.text_nd = None
        self.option_list = []
        self.name_list = []
        self.callback = None
        self.process_event(False)
        return

    def on_choose(self, index):
        if index >= len(self.option_list):
            return
        else:
            self._index = index
            if self.text_nd:
                self.text_nd.SetString(self.option_list[self._index].get('name', ''))
            elif self.func_btn:
                self.func_btn.SetText(self.option_list[self._index].get('name', ''))
            if self.callback:
                self.callback(self.option_list[self._index].get('index', None))
            return

    def get_choose(self):
        if self._index is not None:
            return self.option_list[self._index].get('index', None)
        else:
            return
            return

    def update_option_list(self, option_list, default_value):
        new_sel_index = 0
        if default_value is None and self._index is not None and self.option_list:
            old_sel_val = self.option_list[self._index]
            if old_sel_val in option_list:
                new_sel_index = option_list.index(old_sel_val)
        elif default_value is not None:
            kind_option_list = [ i.get('index', None) for i in option_list ]
            if default_value in kind_option_list:
                new_sel_index = kind_option_list.index(default_value)
        self.option_list = option_list
        if self.func_btn:

            @self.func_btn.unique_callback()
            def OnClick(btn, touch):
                template_utils.init_common_choose_list_2(self._widget, self._arrow, option_list, self.on_choose, self._max_height, self._close_cb, self._reverse, self.func_btn, self.arrow_rotation_cb)
                self.func_btn.OnClick(None)
                return

        self.on_choose(new_sel_index)
        return

    def on_select_item_goods(self, *args):
        option_list = self._widget.option_list
        option_list_data = self.option_list
        item_count = option_list.GetItemCount()
        for index in range(item_count):
            item_widget = option_list.GetItem(index)
            if not item_widget:
                continue
            if len(option_list_data) >= index + 1:
                option = option_list_data[index]
                if 'item_no' in option and option['item_no']:
                    item_widget.icon_new.setVisible(global_data.lobby_red_point_data.get_skin_rp_by_belong_no(option['item_no']))
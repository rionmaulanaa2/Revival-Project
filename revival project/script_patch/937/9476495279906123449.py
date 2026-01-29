# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayExchangeItemListWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.comsys.mall_ui.MallDisplayItemListWidget import MallDisplayItemListWidget
from common.cfg import confmgr
from logic.gutils import mall_utils

class MallDisplayExchangeItemListWidget(MallDisplayItemListWidget):

    def init_parameters(self):
        super(MallDisplayExchangeItemListWidget, self).init_parameters()
        self._show_not_have = False

    def init_widget(self):
        self.init_show_own()
        self.init_buy_confirm()
        self.init_display()
        self.init_switch_detail()

    def init_show_own(self):

        @self.panel.btn_show_own.unique_callback()
        def OnClick(btn, touch):
            self._show_not_have = not self._show_not_have
            self.panel.btn_show_own.SetSelect(self._show_not_have)
            self.reset_mall_list(is_init=True)

        self.panel.btn_show_own.SetSelect(self._show_not_have)

    def init_sub_tabs(self):
        tab_conf = global_data.lobby_mall_data.get_mall_tag_conf()[self._cur_page_index]
        list_sort = self.panel.list_sort
        count = mall_utils.get_any_sub_page_num(self._cur_page_index)
        list_sort.SetInitCount(count)
        self.panel.img_bar.ResizeAndPosition()
        i = 0
        for sub_tab_key in sorted(six_ex.keys(tab_conf), reverse=False):
            if not sub_tab_key.isdigit():
                continue
            name_id = tab_conf[sub_tab_key]
            sub_tab = list_sort.GetItem(i)
            sub_tab.btn_sort.SetText(int(name_id))
            sub_tab.sub_tab_key = sub_tab_key

            @sub_tab.btn_sort.unique_callback()
            def OnClick(btn, touch, sub_tab_key=sub_tab_key):
                self.set_select_tab(sub_tab_key)

            if i == 0:
                self.set_select_tab(sub_tab_key)
            i += 1

    def jump_to_goods_id(self, goods_id):
        _, stype = mall_utils.get_mall_type_stype(goods_id)
        self.set_select_tab(stype)
        super(MallDisplayExchangeItemListWidget, self).jump_to_goods_id(goods_id)

    def set_select_tab(self, sub_tab_key):
        self._cur_sub_page_index = sub_tab_key
        list_sort = self.panel.list_sort
        for i in range(list_sort.GetItemCount()):
            sub_tab = list_sort.GetItem(i)
            if sub_tab.sub_tab_key == sub_tab_key:
                sub_tab.btn_sort.SetSelect(True)
                self.reset_mall_list(is_init=True)
            else:
                sub_tab.btn_sort.SetSelect(False)

    def init_mall_list(self, page_index, sub_page_index=None):
        self._cur_page_index = page_index
        self.init_sub_tabs()

    def get_mall_items(self):
        from logic.gutils import mall_utils
        items = []
        ret_items = []
        item_page_conf = confmgr.get('mall_page_config', str(self._cur_page_index), default={})
        if self._cur_sub_page_index is not None:
            items = item_page_conf.get(self._cur_sub_page_index, [])
        else:
            for sub_page_conf in six.itervalues(item_page_conf):
                items.extend(sub_page_conf)

        for goods_id in items:
            if not mall_utils.is_good_opened(goods_id):
                continue
            if self._show_not_have:
                if not mall_utils.item_has_owned_by_goods_id(goods_id):
                    ret_items.append(goods_id)
            else:
                ret_items.append(goods_id)

        return ret_items
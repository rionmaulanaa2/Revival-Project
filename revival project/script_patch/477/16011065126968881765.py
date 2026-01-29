# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryScratchShopWidget.py
from __future__ import absolute_import
import six
from .LotteryShopWidget import LotteryShopWidget
from common.cfg import confmgr
from logic.gutils.mall_utils import get_goods_item_no

class LotteryScratchShopWidget(LotteryShopWidget):

    def init_parameters(self):
        super(LotteryScratchShopWidget, self).init_parameters()
        self.is_init = True
        self.special_exchange_goods = confmgr.get('lottery_page_config', str(self.lottery_id), 'special_exchange_goods', default=[])

    def check_is_special_goods(self, goods_id):
        if self.special_exchange_goods and int(goods_id) in self.special_exchange_goods[0]:
            return True
        return False

    def refresh_buy_btn(self, has_owned):
        if self.check_is_special_goods(self.select_goods_id):
            idx = self.special_exchange_goods[0].index(int(self.select_goods_id))
            self.panel.btn_buy_all.SetEnable(False)
            return
        super(LotteryScratchShopWidget, self).refresh_buy_btn(has_owned)

    def _on_click_exchange_item(self, goods_id):
        if self.check_is_special_goods(goods_id):
            return
        super(LotteryScratchShopWidget, self)._on_click_exchange_item(goods_id)

    def _cb_create_item(self, tab_index, index, item_widget):
        super(LotteryScratchShopWidget, self)._cb_create_item(tab_index, index, item_widget)
        goods_item = self._get_goods_items(tab_index)
        if not goods_item or len(goods_item) < index:
            return
        goods_id = goods_item[index]
        if self.check_is_special_goods(goods_id):
            idx = self.special_exchange_goods[0].index(int(goods_id))
            item_widget.lab_exchange_limit.setVisible(False)
            item_widget.temp_price.setVisible(False)
            item_widget.lab_text.setVisible(True)
            item_widget.lab_text.SetString(self.special_exchange_goods[1][idx])

    def _on_click_item_widget(self, index, goods_id, item_widget, tab_index, has_owned):
        if self.select_index != index or self.is_init:
            self.is_init = False
            item_no = get_goods_item_no(goods_id)
            self.on_change_show_reward(item_no)
        self.select_index = index
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = goods_id
        item_widget.setLocalZOrder(2)
        self._seleted_mall_widget = item_widget
        self._seleted_mall_widget.choose.setVisible(True)
        self.refresh_buy_btn(has_owned)
        return

    def _init_exchange_mall_list(self, tab_index, goods_id=None):
        mall_list = self.panel.mall_list_one
        if self._seleted_mall_widget:
            self._seleted_mall_widget.setLocalZOrder(0)
            self._seleted_mall_widget.choose.setVisible(False)
            self._seleted_mall_widget = None
        self.select_goods_id = None
        if goods_id is not None:
            self.select_index = self.get_goods_ui_item_index_by_goods_id(goods_id)
        goods_item = self._get_goods_items(tab_index)
        if not goods_item:
            return
        else:

            @mall_list.unique_callback()
            def OnCreateItem(lv, index, item_widget):
                self._cb_create_item(tab_index, index, item_widget)

            mall_list.SetInitCount(len(goods_item))
            all_items = mall_list.GetAllItem()
            for index, widget in enumerate(all_items):
                if type(widget) in [dict, six.text_type, str]:
                    continue
                self._cb_create_item(tab_index, index, widget)

            mall_list.LocatePosByItem(self.select_index)
            select_widget = mall_list.GetItem(self.select_index)
            if select_widget is None:
                select_widget = mall_list.DoLoadItem(self.select_index)
            select_widget and select_widget.bar.OnClick(None)
            mall_list.scroll_Load()
            return

    def show(self, goods_id=None):
        self.is_init = True
        super(LotteryScratchShopWidget, self).show(goods_id)
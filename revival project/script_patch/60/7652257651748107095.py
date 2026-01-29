# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyBagRecycleUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_desc, init_lobby_bag_item, get_lobby_item_pic_by_item_no, get_recycle_item_price_tips
from common.cfg import confmgr
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from logic.gutils import item_utils
from collections import defaultdict
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class RecyclePriceWidget(object):

    def __init__(self, panel):
        self.panel = panel

    def show_empty_price(self):
        price_dict = {50101002: 0,50101003: 0}
        item_nos = sorted(six_ex.keys(price_dict))
        self.panel.list_get.SetInitCount(len(item_nos))
        all_items = self.panel.list_get.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            item_no = item_nos[idx]
            count = price_dict.get(item_no, 0)
            ui_item.txt_price.SetString(str(count))
            ui_item.price_icon.SetDisplayFrameByPath('', item_utils.get_money_icon(item_no))
            ui_item.btn_add.setVisible(False)

    def set_price(self, item_no_list, item_num_list):
        if len(item_no_list) != len(item_num_list):
            log_error('item_no_list should has a equal num list!', item_no_list, item_num_list)
            return
        if not item_no_list:
            self.show_empty_price()
            return
        price_dict = defaultdict(int)
        for idx, item_no in enumerate(item_no_list):
            item_num = item_num_list[idx]
            price_list = self.get_item_recycle_price(item_no, item_num)
            for price_item in price_list:
                item_no, count = price_item
                if count > 0:
                    price_dict[item_no] += count

        item_nos = sorted(six_ex.keys(price_dict))
        self.panel.list_get.SetInitCount(len(price_dict))
        all_items = self.panel.list_get.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            item_no = item_nos[idx]
            count = price_dict.get(item_no, 0)
            ui_item.txt_price.SetString(str(count))
            ui_item.price_icon.SetDisplayFrameByPath('', item_utils.get_money_icon(item_no))
            ui_item.btn_add.setVisible(False)

        return price_dict

    def destroy(self):
        self.panel = None
        return

    def get_item_recycle_price(self, item_no, item_num):

        def cal_price(recycle_gain_item, _num):
            recycle_get = []
            for item_id, _item_num in recycle_gain_item:
                recycle_get.append([item_id, _item_num * _num])

            return recycle_get

        item_conf = confmgr.get('lobby_item', str(item_no), default={})
        recyle_gain_item = item_conf.get('recyle_gain_item', [])
        return cal_price(recyle_gain_item, item_num)


class LobbyBagRecycleUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'bag/bag_recycle'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'btn_recycle.btn_common.OnClick': 'on_click_recycle_btn'
       }
    TEMPLATE_NODE_NAME = 'temp_bar'

    def on_init_panel(self, *args, **kwargs):
        super(LobbyBagRecycleUI, self).on_init_panel()
        self.item_data = {}
        self._price_dict = {}
        self._cur_sel_num = 0
        self.ItemNumBtnWidget = ItemNumBtnWidget(self.panel.temp_input_quantity)
        self.recyclePriceWidget = RecyclePriceWidget(self.panel)

    def on_finalize_panel(self):
        self.destroy_widget('ItemNumBtnWidget')
        self.destroy_widget('recyclePriceWidget')

    def on_click_close_ui(self, *args):
        self.close()

    def on_click_recycle_btn(self, btn, touch):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            if global_data.player and self.item_data:
                item_id = self.item_data.get('id', None)
                if item_id:
                    global_data.player.recycle_item(item_id, self._cur_sel_num)
                    self.close()
            return

        coin_list_str = get_recycle_item_price_tips(self._price_dict)
        SecondConfirmDlg2().confirm(content=get_text_local_content(80777).format(coin_list=coin_list_str), confirm_callback=confirm_callback)

    def init_recycle_item(self, item_data):
        content_nd = self.panel.nd_content
        item_no = item_data.get('item_no', None)
        quantity = item_data.get('quantity', 1)
        self.item_data = item_data
        init_lobby_bag_item(self.panel.temp_item, item_data)
        content_nd.lab_name.SetString(get_lobby_item_name(item_no))
        content_nd.lab_details.SetString(get_lobby_item_desc(item_no))
        self.ItemNumBtnWidget.init_item(self.item_data, self.on_num_changed)
        self.set_good_num(1)
        return

    def update_recycle_get(self):
        self._price_dict = self.recyclePriceWidget.set_price([self.item_data.get('item_no', None)], [self._cur_sel_num])
        return

    def on_num_changed(self, item_data, num):
        self.set_good_num(num)
        self.update_button_show()

    def set_good_num(self, num):
        self._cur_sel_num = num
        quantity = self.item_data.get('quantity', 1)
        self.panel.temp_input_quantity.lab_num.SetString(str(num) + '/' + str(quantity))
        self.update_recycle_get()

    def update_button_show(self):
        pass

    def on_click_max_btn(self, btn, touch):
        if not self.item_data:
            return
        quantity = self.item_data.get('quantity', 1)
        self.add_sub_widget.set_num(quantity)
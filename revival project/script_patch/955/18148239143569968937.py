# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonBuyListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_type, init_lobby_bag_item, get_recycle_item_price_tips
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from common.cfg import confmgr
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon.item import lobby_item_type
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils
from logic.client.const import mall_const
import logic.gcommon.const as gconst

class BatchBuyItem(object):

    def __init__(self, panel):
        self.panel = panel
        self.item_data = {}
        self.index = None
        self.is_choose = False
        self.num_callback = None
        self.choose_callback = None
        self.price_choice_callback = None
        self.role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        return

    def init_item(self, item_data, is_choose, index, item_num, num_callback, choose_callback, price_choice, price_choice_callback):
        self.item_data = item_data
        self.index = index
        self.set_choose(is_choose)
        self.num_callback = num_callback
        self.choose_callback = choose_callback
        self.price_choice_callback = price_choice_callback
        quantity = self.item_data.get('quantity', 1)
        ui_item = self.panel
        init_lobby_bag_item(self.panel.temp_item, item_data)
        item_no = item_data.get('item_no', None)
        self.panel.lab_name.SetString(get_lobby_item_name(item_no))
        self.update_number_show(ui_item, item_no, item_num, price_choice)
        from logic.gutils import item_utils
        return

    def update_number_show(self, ui_item, item_no, item_num, price_choice):
        from logic.gutils import mall_utils
        skin_data = global_data.player.get_item_by_no(item_no)
        ui_item.temp_price.setVisible(False)
        ui_item.bar_choose_price.setVisible(False)
        if skin_data:
            ui_item.nd_get.setVisible(False)
            ui_item.nd_cant_get.setVisible(False)
            ui_item.temp_price.setVisible(False)
        else:
            ui_item.nd_cant_get.setVisible(False)
            goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
            price = mall_utils.get_mall_item_price(goods_id)
            unowned_open_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(goods_id)
            ui_item.temp_btn_get.btn_common.callback()
            from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, groceries_buy_confirmUI

            @ui_item.temp_btn_get.btn_common.callback()
            def OnClick(btn, touch):
                item_data = global_data.player.get_item_by_no(item_no)
                if item_data is None:
                    goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
                    lobby_i_type = get_lobby_item_type(item_no)
                    price = mall_utils.get_mall_item_price(goods_id)
                    if price:
                        if lobby_i_type == lobby_item_type.L_ITEM_TYPE_ROLE_SKIN:
                            role_or_skin_buy_confirmUI(goods_id)
                        else:
                            groceries_buy_confirmUI(goods_id)
                    else:
                        item_utils.jump_to_ui(item_no)
                else:
                    log_error('item is already owned')
                return

            if price and not unowned_open_item_nos:
                ui_item.nd_get.setVisible(False)
                ui_item.nd_cant_get.setVisible(False)
                prices = mall_utils.get_mall_item_price(goods_id)
                prices = mall_utils.get_mall_item_real_pay_price(prices)
                if len(prices) == 1:
                    ui_item.temp_price.setVisible(True)
                    ui_item.temp_btn_get.setVisible(True)
                    template_utils.splice_price(ui_item.temp_price, prices, color=mall_const.USE_TEMPLATE_COLOR)
                elif len(prices) == 2:
                    ui_item.bar_choose_price.setVisible(True)
                    template_utils.splice_price(ui_item.temp_price_1, [prices[0]], color=mall_const.USE_TEMPLATE_COLOR)
                    template_utils.splice_price(ui_item.temp_price_2, [prices[1]], color=mall_const.USE_TEMPLATE_COLOR)
                    ui_item.btn_choose_1.SetSelect(price_choice == 0)
                    ui_item.btn_choose_2.SetSelect(price_choice == 1)

                    @ui_item.btn_choose_1.callback()
                    def OnClick(btn, touch):
                        if self.price_choice_callback:
                            self.price_choice_callback(self.index, 0)
                            ui_item.btn_choose_1.SetSelect(True)
                            ui_item.btn_choose_2.SetSelect(False)

                    @ui_item.btn_choose_2.callback()
                    def OnClick(btn, touch):
                        if self.price_choice_callback:
                            self.price_choice_callback(self.index, 1)
                            ui_item.btn_choose_1.SetSelect(False)
                            ui_item.btn_choose_2.SetSelect(True)

                ui_item.temp_btn_get.setVisible(False)
            elif unowned_open_item_nos:
                ui_item.nd_get.setVisible(False)
                ui_item.nd_cant_get.setVisible(True)
                ui_item.temp_price.setVisible(False)
                name_text = item_utils.get_lobby_item_name(unowned_open_item_nos[0])
                ui_item.lab_cant_get.SetString(get_text_by_id(81606, {'skin_name': name_text}))
                ui_item.temp_btn_get.setVisible(False)
            elif item_utils.can_jump_to_ui(item_no):
                ui_item.nd_get.setVisible(True)
                ui_item.temp_price.setVisible(False)
                ui_item.nd_cant_get.setVisible(False)
                ui_item.temp_btn_get.btn_common.SetText(2222)
                ui_item.temp_btn_get.setVisible(True)
                ui_item.lab_get.SetString(item_utils.get_item_access(item_no))
            else:
                ui_item.nd_get.setVisible(False)
                ui_item.nd_cant_get.setVisible(True)
                ui_item.temp_price.setVisible(False)
                ui_item.lab_cant_get.SetString(860078)
                ui_item.temp_btn_get.setVisible(False)

        @ui_item.temp_choose.btn.callback()
        def OnClick(btn, touch):
            goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
            price = mall_utils.get_mall_item_price(goods_id)
            unowned_open_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(goods_id)
            if not price or unowned_open_item_nos:
                global_data.game_mgr.show_tip(get_text_by_id(860077))
                return
            if callable(self.choose_callback):
                self.set_choose(not self.is_choose)
                self.choose_callback(self.index, self.is_choose)

    def set_selected_num(self, num):
        pass

    def set_choose(self, is_choose):
        self.is_choose = is_choose
        self.panel.temp_choose.choose.setVisible(is_choose)

    def destroy(self):
        self.num_callback = None
        self.choose_callback = None
        self.price_choice_callback = None
        self.panel = None
        self.item_data = {}
        self.index = None
        return


class CommonBuyListUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/common_buy_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_window'
    UI_ACTION_EVENT = {'temp_btn_buy.btn_common.OnClick': 'on_click_btn_buy'
       }
    GLOBAL_EVENT = {'player_item_update_event': 'on_buy_good_success'
       }

    def on_init_panel(self, *args, **kwargs):
        super(CommonBuyListUI, self).on_init_panel()
        self.item_data_list = []
        self.item_data_num_list = []
        self.item_data_widget_list = []
        self.item_data_choose_list = []
        self.item_price_choice_list = []
        self._item_remove_callback = None
        self._batch_buy_callback = None
        self.init_scroll_view()
        return

    def init_scroll_view(self):

        @self.panel.list_item.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_buy_item_helper(ui_item, idx)

    def set_item_remove_callback(self, callback):
        self._item_remove_callback = callback

    def set_batch_buy_callback(self, callback):
        self._batch_buy_callback = callback

    def init_buy_item_helper(self, ui_item, idx):
        if idx < len(self.item_data_list):
            item_data = self.item_data_list[idx]
            widget = self.item_data_widget_list[idx]
            item_num = self.item_data_num_list[idx]
            is_choose = self.item_data_choose_list[idx]
            price_choice = self.item_price_choice_list[idx]
            if not widget:
                widget = BatchBuyItem(ui_item)
                self.item_data_widget_list[idx] = widget
                widget.init_item(item_data, is_choose, idx, item_num, self.on_num_changed, self.on_choose_changed, price_choice, self.on_price_choice_changed)
        else:
            log_error('idx out of range!!!', idx, len(self.item_data_list))

    def on_num_changed(self, index, num):
        if index < len(self.item_data_num_list):
            if self.item_data_num_list[index] != num:
                self.item_data_num_list[index] = num

    def on_choose_changed(self, index, is_choose):
        if index < len(self.item_data_choose_list):
            self.item_data_choose_list[index] = is_choose
        self.update_price_show()

    def on_price_choice_changed(self, index, price_choice):
        if index < len(self.item_price_choice_list):
            old_choice = self.item_price_choice_list[index]
            if old_choice != price_choice:
                self.item_price_choice_list[index] = price_choice
                self.update_price_show()

    def on_finalize_panel(self):
        for widget in self.item_data_widget_list:
            widget.destroy()

        self._item_remove_callback = None
        self._batch_buy_callback = None
        self.item_data_widget_list = []
        self.item_data_list = []
        self.item_data_num_list = []
        return

    def init_buy_list_item(self, item_data_list):
        if self.item_data_widget_list:
            for widget in self.item_data_widget_list:
                widget.destroy()

            self.item_data_widget_list = []
        if item_data_list:
            self.item_data_list = item_data_list
            self.item_data_num_list = [ 1 for i in item_data_list ]
            self.item_data_widget_list = [ None for i in item_data_list ]
            self.item_data_choose_list = []
            for data in item_data_list:
                item_no = data.get('item_no')
                goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
                price = mall_utils.get_mall_item_price(goods_id)
                unowned_open_item_nos = mall_utils.get_goods_id_unowned_open_item_nos(goods_id)
                if price and not unowned_open_item_nos:
                    self.item_data_choose_list.append(True)
                else:
                    self.item_data_choose_list.append(False)

            self.item_price_choice_list = [ 0 for i in item_data_list ]
            self.item_data_max_num_list = [ item_data.get('quantity', 1) for item_data in item_data_list ]
            self.panel.list_item.SetInitCount(0)
            self.panel.list_item.SetInitCount(len(item_data_list))
            self.panel.list_item.ForceLoadVisibleRangeItem()
        self.update_price_show()
        return

    def on_buy_good_success(self):
        self.check_del_owned_impurchasable_item()
        self.update_price_show()

    def check_del_owned_impurchasable_item(self):
        role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        del_index_list = []
        for idx, item_data in enumerate(self.item_data_list):
            item_no = item_data.get('item_no')
            skin_data = global_data.player.get_item_by_no(item_no)
            if skin_data:
                del_index_list.append(idx)

        if self._item_remove_callback:
            for idx in del_index_list:
                item_data = self.item_data_list[idx]
                item_no = item_data.get('item_no')
                self._item_remove_callback(item_no)

        self.del_items_by_indexes(del_index_list)

    def del_items_by_indexes(self, del_index_list):
        for idx in reversed(del_index_list):
            self.item_data_list.pop(idx)
            self.item_data_max_num_list.pop(idx)
            self.item_data_num_list.pop(idx)
            self.item_data_choose_list.pop(idx)
            self.item_price_choice_list.pop(idx)

        self.refresh_ui()

    def refresh_ui(self):
        for widget in self.item_data_widget_list:
            widget.destroy()

        self.item_data_widget_list = [ None for i in self.item_data_list ]
        self.panel.list_item.SetInitCount(len(self.item_data_list))
        allItem = self.panel.list_item.GetAllItem()
        for idx, ui_item in enumerate(allItem):
            if ui_item:
                self.init_buy_item_helper(ui_item, idx)

        self.panel.nd_empty.setVisible(not bool(self.item_data_list))
        return

    def get_sel_items(self):
        _item_nos = []
        _item_nums = []
        _item_price_choice = []
        for idx, is_choose in enumerate(self.item_data_choose_list):
            if is_choose:
                item_conf = self.item_data_list[idx]
                item_no = item_conf.get('item_no', None)
                if item_no:
                    _item_nos.append(item_no)
                    price_choice = self.item_price_choice_list[idx]
                    _item_price_choice.append(price_choice)
                    num = self.item_data_num_list[idx]
                    _item_nums.append(num)

        return (
         _item_nos, _item_price_choice, _item_nums)

    def get_total_price(self):
        price_list = []
        _item_nos, _item_price_choice, _ = self.get_sel_items()
        if not _item_nos:
            return None
        else:
            for idx, item_no in enumerate(_item_nos):
                item_data = global_data.player.get_item_by_no(item_no)
                if item_data:
                    continue
                goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
                prices = mall_utils.get_mall_item_price(goods_id)
                if prices:
                    price_list.append(prices[_item_price_choice[idx]])

            pay_prices = mall_utils.get_mall_item_real_pay_price(price_list)
            total_price = template_utils.merge_goods_prices(pay_prices)
            return total_price

    def update_price_show(self):
        total_price = self.get_total_price()
        if not total_price:
            self.panel.temp_btn_buy.btn_common.SetShowEnable(False)
            self.panel.temp_price.setVisible(False)
            return
        self.panel.temp_price.setVisible(True)
        template_utils.splice_price(self.panel.temp_price, total_price, is_or=False, color=mall_const.USE_TEMPLATE_COLOR)
        is_can_pay = True
        for price_info in total_price:
            if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                is_can_pay = False

        self.panel.temp_btn_buy.btn_common.SetShowEnable(is_can_pay)

    def on_click_btn_buy(self, btn, touch):
        total_price = self.get_total_price()
        if not total_price:
            global_data.game_mgr.show_tip(get_text_by_id(860112))
            return
        else:
            for price_info in total_price:
                if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                    global_data.game_mgr.show_tip(get_text_by_id(860111))
                    return

            batch_buy_list = []
            _item_nos, _item_price_choice, _ = self.get_sel_items()
            for idx, item_no in enumerate(_item_nos):
                goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
                prices = mall_utils.get_mall_item_price(goods_id)
                if prices:
                    batch_buy_list.append(item_no)
                    payment_price = prices[_item_price_choice[idx]]
                    goods_payment = payment_price.get('goods_payment')
                    if goods_payment is not None:
                        global_data.player.buy_goods(goods_id, 1, goods_payment)

            self.on_batch_buy(batch_buy_list)
            return

    def on_batch_buy(self, buy_item_list):
        if self._batch_buy_callback:
            self._batch_buy_callback(buy_item_list)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineBuyUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_type, init_lobby_bag_item, get_recycle_item_price_tips
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gcommon.item import lobby_item_type
from logic.gutils import dress_utils, item_utils, template_utils, mall_utils
from logic.client.const import mall_const
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.mecha_skin_utils import get_mecha_skin_goods_id

class BatchBuySDItem(object):

    def __init__(self, panel):
        self.panel = panel
        self.item_data = {}
        self.index = None
        self.is_choose = False
        self.num_callback = None
        self.choose_callback = None
        self.price_choice_callback = None
        return

    def init_item(self, item_data, is_choose, index, item_num, num_callback, choose_callback, price_choice, price_choice_callback):
        self.item_data = item_data
        self.index = index
        self.set_choose(is_choose)
        self.num_callback = num_callback
        self.choose_callback = choose_callback
        self.price_choice_callback = price_choice_callback
        ui_item = self.panel
        init_lobby_bag_item(self.panel.temp_item, item_data)
        item_no = item_data.get('item_no', None)
        own = item_data.get('own', 0)
        belong = item_data.get('belong')
        slider_no = item_data.get('slider_no', None)
        if isinstance(slider_no, int):
            self.panel.lab_name.SetString(get_text_by_id(81906) + ' ' + str(slider_no + 1))
        else:
            self.panel.lab_name.SetString(get_lobby_item_name(item_no))
        self.update_number_show(ui_item, item_no, item_num, price_choice, own, belong)
        return

    def update_number_show(self, ui_item, item_no, item_num, price_choice, own, belong):
        ui_item.temp_price.setVisible(False)
        ui_item.bar_choose_price.setVisible(False)
        if own:
            ui_item.nd_get.setVisible(False)
            ui_item.nd_cant_get.setVisible(False)
            ui_item.temp_price.setVisible(False)
        else:
            if belong == 'skin':
                goods_id = get_mecha_skin_goods_id(item_no)
                if goods_id is None:
                    price = None
                else:
                    price = mall_utils.get_mall_item_price(goods_id)
            else:
                goods_id = str(item_no)
                price = mall_utils.get_mall_item_price(goods_id)
            if item_utils.can_jump_to_ui(item_no):
                ui_item.nd_get.setVisible(True)
                ui_item.nd_cant_get.setVisible(False)
                ui_item.temp_price.setVisible(False)
                ui_item.temp_btn_get.btn_common.SetText(2222)
                ui_item.temp_btn_get.setVisible(True)
                ui_item.lab_get.SetString(item_utils.get_item_access(item_no))
            elif price:
                ui_item.nd_get.setVisible(False)
                ui_item.nd_cant_get.setVisible(False)
                prices = mall_utils.get_mall_item_real_pay_price(price)
                if len(prices) == 1:
                    ui_item.temp_price.setVisible(True)
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

            else:
                ui_item.nd_get.setVisible(False)
                ui_item.nd_cant_get.setVisible(True)
                ui_item.temp_price.setVisible(False)
                ui_item.temp_btn_get.setVisible(False)
                ui_item.lab_cant_get.SetString(860078)
        if ui_item.temp_btn_get.isVisible():

            @ui_item.temp_btn_get.btn_common.callback()
            def OnClick(*args):
                goods_id = str(item_no)
                price = mall_utils.get_mall_item_price(goods_id)
                if item_utils.can_jump_to_ui(item_no):
                    item_utils.jump_to_ui(item_no)
                    global_data.ui_mgr.close_ui('SkinDefineBuyUI')
                elif price:
                    if get_lobby_item_type(item_no) == lobby_item_type.L_ITEM_TYPE_MECHA_SKIN:
                        role_or_skin_buy_confirmUI(goods_id)

        @ui_item.temp_choose.btn.callback()
        def OnClick(*args):
            if callable(self.choose_callback):
                self.choose_callback(self, self.index, self.is_choose)

        return

    def set_selected_num(self):
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


class SkinDefineBuyUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/common_buy_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_window'
    UI_ACTION_EVENT = {'temp_btn_buy.btn_common.OnClick': 'on_click_btn_buy'
       }
    GLOBAL_EVENT = {'player_item_update_event': 'on_buy_good_success'
       }

    def on_init_panel(self, *args, **kwargs):
        super(SkinDefineBuyUI, self).on_init_panel()
        self.init_params()
        self.init_scroll_view()

    def init_params(self):
        self.item_data_list = []
        self.item_data_num_list = []
        self.item_data_widget_list = []
        self.item_data_choose_list = []
        self.item_price_choice_list = []
        self._item_remove_callback = None
        self._batch_buy_callback = None
        self.own_skin = True
        self.is_skin_can_buy = True
        return

    def init_scroll_view(self):

        @self.panel.list_item.unique_callback()
        def OnCreateItem(_lv, _idx, _ui_item):
            self.init_buy_item_helper(_ui_item, _idx)

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
                widget = BatchBuySDItem(ui_item)
                self.item_data_widget_list[idx] = widget
                widget.init_item(item_data, is_choose, idx, item_num, self.on_num_changed, self.on_choose_changed, price_choice, self.on_price_choice_changed)
        else:
            log_error('idx out of range!!!', idx, len(self.item_data_list))

    def init_buy_list_item(self, item_data_list):
        if self.item_data_widget_list:
            for widget in self.item_data_widget_list:
                if widget:
                    widget.destroy()

            self.item_data_widget_list = []
        if item_data_list:
            self.item_data_list = item_data_list
            self.item_data_num_list = [ 1 for i in item_data_list ]
            self.item_data_widget_list = [ None for i in item_data_list ]
            self.item_data_choose_list = []
            for data in item_data_list:
                belong = data.get('belong')
                if belong == 'skin':
                    self.own_skin = False
                    item_no = data.get('item_no')
                    goods_id = get_mecha_skin_goods_id(item_no)
                    if goods_id is None:
                        price = None
                    else:
                        price = mall_utils.get_mall_item_price(goods_id)
                    if price:
                        self.is_skin_can_buy = True
                        self.item_data_choose_list.append(True)
                    else:
                        self.is_skin_can_buy = False
                        self.item_data_choose_list.append(False)
                elif belong == 'color':
                    if not self.own_skin:
                        if not self.is_skin_can_buy:
                            self.item_data_choose_list.append(False)
                        else:
                            self.item_data_choose_list.append(True)
                    else:
                        self.item_data_choose_list.append(True)
                else:
                    item_no = data.get('item_no')
                    goods_id = str(item_no)
                    price = mall_utils.get_mall_item_price(goods_id)
                    own = data.get('own')
                    if price or own:
                        self.item_data_choose_list.append(True)
                    else:
                        self.item_data_choose_list.append(False)

            self.item_price_choice_list = [ 0 for i in item_data_list ]
            self.panel.list_item.DeleteAllSubItem()
            self.panel.list_item.SetInitCount(len(item_data_list))
        self.update_price_show()
        return

    def on_num_changed(self):
        pass

    def on_choose_changed(self, widget, index, is_choose):
        if index < len(self.item_data_choose_list):
            belong = self.item_data_list[index].get('belong')
            own = self.item_data_list[index].get('own')
            item_no = self.item_data_list[index].get('item_no')
            if belong == 'skin':
                if not own:
                    goods_id = get_mecha_skin_goods_id(item_no)
                    if goods_id is None:
                        price = None
                    else:
                        price = mall_utils.get_mall_item_price(goods_id)
                    if not price:
                        global_data.game_mgr.show_tip(get_text_by_id(860077))
                        return
                global_data.game_mgr.show_tip(get_text_by_id(81931))
                return
            if belong == 'color':
                if not self.own_skin:
                    if not self.is_skin_can_buy:
                        global_data.game_mgr.show_tip(get_text_by_id(81908))
                        return
                    self.item_data_choose_list[index] = not is_choose
                    widget.set_choose(not is_choose)
                else:
                    self.item_data_choose_list[index] = not is_choose
                    widget.set_choose(not is_choose)
            elif belong == 'decal':
                if not own:
                    goods_id = str(item_no)
                    price = mall_utils.get_mall_item_price(goods_id)
                    if not price:
                        global_data.game_mgr.show_tip(get_text_by_id(860077))
                        return
                self.item_data_choose_list[index] = not is_choose
                widget.set_choose(not is_choose)
            else:
                self.item_data_choose_list[index] = not is_choose
                widget.set_choose(not is_choose)
        self.update_price_show()
        return

    def on_price_choice_changed(self, index, price_choice):
        if index < len(self.item_price_choice_list):
            old_choice = self.item_price_choice_list[index]
            if old_choice != price_choice:
                self.item_price_choice_list[index] = price_choice
                self.update_price_show()

    def on_buy_good_success(self):
        self.close()

    def check_del_owned_impurchaseable_item(self):
        pass

    def del_items_by_indexes(self):
        pass

    def refresh_ui(self):
        pass

    def get_sel_items(self):
        _item_nos = []
        _item_price_choice = []
        _item_nums = []
        _owns = []
        _belongs = []
        _idxs = []
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
                    own = item_conf.get('own', 0)
                    _owns.append(own)
                    belong = item_conf.get('belong', None)
                    _belongs.append(belong)
                    idx = item_conf.get('idx', -1)
                    _idxs.append(idx)

        return (
         _item_nos, _item_price_choice, _item_nums, _owns, _belongs, _idxs)

    def get_total_price(self):
        price_list = []
        is_all_own = True
        _item_nos, _item_price_choice, _, _owns, _belongs, _ = self.get_sel_items()
        if not _item_nos:
            return (None, False)
        else:
            for idx, item_no in enumerate(_item_nos):
                own = _owns[idx]
                if own:
                    continue
                else:
                    is_all_own = False
                belong = _belongs[idx]
                if belong == 'skin':
                    goods_id = get_mecha_skin_goods_id(item_no)
                    if goods_id is None:
                        prices = None
                    else:
                        prices = mall_utils.get_mall_item_price(goods_id)
                else:
                    goods_id = str(item_no)
                    prices = mall_utils.get_mall_item_price(goods_id)
                if prices:
                    price_list.append(prices[_item_price_choice[idx]])

            pay_prices = mall_utils.get_mall_item_real_pay_price(price_list)
            total_price = template_utils.merge_goods_prices(pay_prices)
            return (
             total_price, is_all_own)

    def update_price_show(self):
        total_price, is_all_own = self.get_total_price()
        if not total_price and not is_all_own:
            self.panel.temp_btn_buy.btn_common.SetShowEnable(False)
            self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(81929))
            self.panel.temp_price.setVisible(False)
            return
        if is_all_own:
            self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(860096))
            self.panel.temp_price.setVisible(False)
        else:
            self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(81928))
            self.panel.temp_price.setVisible(True)
        template_utils.splice_price(self.panel.temp_price, total_price, is_or=False, color=mall_const.USE_TEMPLATE_COLOR)
        is_can_pay = True
        for price_info in total_price:
            if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                is_can_pay = False

        self.panel.temp_btn_buy.btn_common.SetShowEnable(is_can_pay)

    def on_click_btn_buy(self, *args):
        total_price, is_all_own = self.get_total_price()
        if not total_price and not is_all_own:
            global_data.game_mgr.show_tip(get_text_by_id(860112))
            return
        else:
            for price_info in total_price:
                if not mall_utils.check_payment(price_info['goods_payment'], price_info['real_price'], pay_tip=False):
                    global_data.game_mgr.show_tip(get_text_by_id(860111))
                    return

            self.panel.temp_btn_buy.btn_common.SetEnable(False)
            batch_buy_list = []
            buy_color_list = []
            own_color_list = []
            buy_decal_list = []
            own_decal_list = []
            _item_nos, _item_price_choice, _, _owns, _belongs, _idxs = self.get_sel_items()
            for idx, item_no in enumerate(_item_nos):
                own = _owns[idx]
                belong = _belongs[idx]
                index = _idxs[idx]
                if own:
                    if belong == 'color':
                        own_color_list.append([item_no, belong, index])
                    elif belong == 'decal':
                        own_decal_list.append([item_no, belong, index])
                elif belong == 'color':
                    buy_color_list.append([item_no, belong, index])
                elif belong == 'decal':
                    buy_decal_list.append([item_no, belong, index])
                goods_id = str(item_no)
                prices = mall_utils.get_mall_item_price(goods_id)
                if prices:
                    batch_buy_list.append(item_no)
                    payment_price = prices[_item_price_choice[idx]]
                    goods_payment = payment_price.get('goods_payment')
                    if goods_payment is not None:
                        if not own:
                            global_data.player.buy_goods(goods_id, 1, goods_payment)

            self.on_batch_buy(batch_buy_list, buy_color_list, own_color_list, buy_decal_list, own_decal_list)
            return

    def on_batch_buy(self, batch_buy_list, buy_color_list, own_color_list, buy_decal_list, own_decal_list):
        if self._batch_buy_callback:
            self._batch_buy_callback(batch_buy_list, buy_color_list, own_color_list, buy_decal_list, own_decal_list)

    def on_finalize_panel(self):
        for widget in self.item_data_widget_list:
            if widget:
                widget.destroy()

        self.init_params()
        super(SkinDefineBuyUI, self).on_finalize_panel()
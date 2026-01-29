# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/ExchangeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel, PVE_MAIN_UI_LIST
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import template_utils
import logic.gcommon.const as gconst
from logic.gutils import mall_utils
from common.cfg import confmgr
from logic.client.const import mall_const
import render
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class ExchangeUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'charge/exchange_diamond'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'

    def on_init_panel(self, from_payment=gconst.SHOP_PAYMENT_YUANBAO, to_payment=gconst.SHOP_PAYMENT_DIAMON, buy_goods_id=mall_const.MALL_DIAMOND_GIFT, keyboard_for_from_payment=True, default_value=0):
        super(ExchangeUI, self).on_init_panel()
        self.hide_main_ui(exceptions=PVE_MAIN_UI_LIST)
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self._from_payment = from_payment
        self._to_payment = to_payment
        self._buy_goods_id = buy_goods_id
        self._keyboard_for_from_payment = keyboard_for_from_payment
        self._default_value = default_value
        self.update_default_value()
        self.init_event()
        self.init_widget()

    def init_event(self):
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.show_main_ui()
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self.update_player_info,
           'buy_good_success': self.on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        item_no = mall_utils.get_payment_item_no(self._to_payment)
        from logic.gutils.item_utils import get_lobby_item_name
        item_name = get_lobby_item_name(item_no)
        template_utils.init_common_panel(self.panel.temp_bg, get_text_by_id(81503, {'item_name': item_name}), None)
        self.show_cur_money(do_init=True)
        self.init_key_board()
        return

    def update_player_info(self):
        self.show_cur_money()
        self.update_default_value()
        self.init_key_board()
        self.check_limit()

    def on_buy_good_success(self, *args):
        self.show_cur_money()
        self.update_default_value()
        self.init_key_board()
        self.check_limit()

    def show_cur_money(self, do_init=False):
        money_types = [self._to_payment, self._from_payment]
        list_money = self.panel.list_price
        if do_init:
            list_money.SetInitCount(len(money_types))
            cost_item_no = mall_utils.get_payment_item_no(self._from_payment)
            from_name = get_lobby_item_name(cost_item_no)
            self.panel.icon_be_exchanged.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(cost_item_no))
            cost_item_no2 = mall_utils.get_payment_item_no(self._to_payment)
            self.panel.icon_exchange.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(cost_item_no2))
            to_name = get_lobby_item_name(cost_item_no2)
            mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
            unit_num = mall_conf.get('num', 1)
            cost_num = self.get_cost_num()
            self.panel.lab_rate.SetString(get_text_by_id(80861, {'cost_num': cost_num,'from_item_name': from_name,'to_item_name': to_name,'num': unit_num}))
        self.check_limit()
        for i, type in enumerate(money_types):
            money_node = list_money.GetItem(i)
            money = mall_utils.get_my_money(type)
            template_utils.init_common_price(money_node, money, type)
            money_node.btn_add.setVisible(False)

    def check_limit(self):
        mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
        max_buy_num_per_day = mall_conf.get('max_buy_num_per_day')
        if max_buy_num_per_day:
            self.panel.lab_limit.setVisible(True)
            _, _, num_info = mall_utils.buy_num_limite_by_day(self._buy_goods_id)
            remain_num, max_num = num_info
            cost_item_no2 = mall_utils.get_payment_item_no(self._to_payment)
            to_name = get_lobby_item_name(cost_item_no2)
            self.panel.lab_limit.SetString(get_text_by_id(860109, {'item_name': to_name,'bought_num': max_num - remain_num,'max_num': max_num}))
            if remain_num <= 0:
                self.panel.lab_limit.SetColor('#SR')
        else:
            self.panel.lab_limit.setVisible(False)

    def get_cost_num(self):
        cost_item_no = mall_utils.get_payment_item_no(self._from_payment)
        mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
        cost_num = 0
        if self._from_payment == gconst.SHOP_PAYMENT_YUANBAO:
            cost_num = mall_conf.get('yuanbao_consumed', 0)
        elif self._from_payment == gconst.SHOP_PAYMENT_DIAMON:
            cost_num = mall_conf.get('diamond_consumed', 0)
        elif self._from_payment == gconst.SHOP_PAYMENT_DIAMON:
            cost_num = mall_conf.get('gold_consumed', 0)
        elif mall_utils.get_payment_type(self._from_payment) == gconst.SHOP_PAYMENT_ITEM:
            item_consumed = mall_conf.get('item_consumed', [])
            if cost_item_no in item_consumed:
                idx = item_consumed.index(cost_item_no)
                cost_num = item_consumed[idx + 1]
        return cost_num

    def update_default_value(self):
        limit_buy, num_info, _ = mall_utils.get_limit_info(self._buy_goods_id)
        if limit_buy:
            can_buy_num, _ = num_info
            self._default_value = min(can_buy_num, self._default_value)

    def init_key_board(self):
        from logic.client.const import mall_const
        mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
        unit_num = mall_conf.get('num', 1)
        max_num = mall_conf.get('num_times', 1)
        mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
        max_buy_num_per_day = mall_conf.get('max_buy_num_per_day')
        if max_buy_num_per_day:
            self.panel.lab_limit.setVisible(True)
            _, _, num_info = mall_utils.buy_num_limite_by_day(self._buy_goods_id)
            remain_num, _ = num_info
            max_num = remain_num
        cost_num = self.get_cost_num()
        cur_yuanbao = mall_utils.get_my_money(self._from_payment)
        cur_exchange_num = [
         self._default_value]

        def on_input(num):
            if self._keyboard_for_from_payment:
                cur_exchange_num[0] = num
                self.panel.lab_ticket_num.SetString(str(num))
                self.panel.lab_diamond_num.SetString(str(int(num / cost_num * unit_num)))
            else:
                cur_exchange_num[0] = int(num / unit_num * cost_num)
                self.panel.lab_ticket_num.SetString(str(cur_exchange_num[0]))
                self.panel.lab_diamond_num.SetString(str(num))
            if cur_exchange_num[0] > cur_yuanbao:
                self.panel.lab_ticket_num.SetColor('#SR')
            else:
                self.panel.lab_ticket_num.SetColor('#SW')
            if cur_exchange_num[0] <= 0:
                self.panel.temp_buy.btn_common_big.SetEnable(False)
            else:
                self.panel.temp_buy.btn_common_big.SetEnable(True)

        template_utils.init_input_num_keyboard(self.panel.temp_keyboard, default_value=cur_exchange_num[0], max_value=max_num, on_input=on_input)
        on_input(self._default_value)

        @self.panel.temp_buy.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            import logic.gutils.item_utils as item_utils
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            prices = mall_utils.get_mall_item_price(self._buy_goods_id, cur_exchange_num[0])
            if not prices:
                return
            if cur_exchange_num[0] > cur_yuanbao:
                if self._from_payment == gconst.SHOP_PAYMENT_YUANBAO:
                    mall_utils.check_yuanbao(cur_exchange_num[0])
                    return
                else:
                    mall_utils.check_payment(self._from_payment, cur_exchange_num[0], pay_tip=True, cb=lambda : self.close())
                    return

            def do_buy():
                price_info = prices[0]
                goods_payment = price_info.get('goods_payment')
                if self._keyboard_for_from_payment:
                    goods_num = cur_exchange_num[0]
                else:
                    goods_num = int(cur_exchange_num[0] / cost_num * unit_num)
                global_data.player.buy_goods(self._buy_goods_id, goods_num, goods_payment)

            mall_conf = confmgr.get('mall_config', self._buy_goods_id, default={})
            unit_num = mall_conf.get('num', 1)
            content = get_text_local_content(12078)
            real_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (item_utils.get_money_icon(self._from_payment), cur_exchange_num[0])
            exchange_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (item_utils.get_money_icon(self._to_payment), int(cur_exchange_num[0] / cost_num * unit_num))
            content = content.format(yuanbao=real_price_txt, diamond=exchange_price_txt)
            SecondConfirmDlg2().confirm(content=content, confirm_callback=do_buy)

    def do_show_panel(self):
        super(ExchangeUI, self).do_show_panel()
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def do_hide_panel(self):
        super(ExchangeUI, self).do_hide_panel()
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
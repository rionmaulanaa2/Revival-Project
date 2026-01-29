# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/RecommendGiftBuyConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from logic.gutils import template_utils
from common.cfg import confmgr
from logic.client.const import mall_const
import logic.gcommon.const as gconst
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class RecommendGiftBuyConfirmUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'mall/buy_gift_confirm'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, goods_id, pick_list=None):
        super(RecommendGiftBuyConfirmUI, self).on_init_panel()
        self.goods_id = goods_id
        self.pick_list = pick_list or []
        self.button_ui_price_nd = None
        self.init_widget()
        self.init_event()
        self.panel.PlayAnimation('appear')
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.on_close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        if self.button_ui_price_nd and self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(True)
        self.process_event(False)

    def init_widget(self):
        self.refresh_info()

    def get_price_info(self, prices, goods_payment):
        for price_info in prices:
            if price_info['goods_payment'] == goods_payment:
                return price_info

        return {}

    def set_buttom_ui_price_nd(self, nd):
        return
        self.button_ui_price_nd = nd
        if self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(False)

    def refresh_info(self):
        goods_id = self.goods_id
        path = mall_utils.get_detail_pic(goods_id)
        self.panel.img_item.SetDisplayFrameByPath('', mall_utils.get_banner_goods_pic_path(goods_id))
        self.panel.lab_name.SetString(mall_utils.get_goods_name(goods_id))
        self.panel.lab_describe.SetString(mall_utils.get_goods_decs(goods_id))
        mall_utils.get_goods_item_show_info(goods_id)
        prices = self.check_limit_open_gold_pay(goods_id)
        count = len(prices)
        all_item = [self.panel.btn_buy_2, self.panel.btn_buy_1]
        for i, btn_price in enumerate(all_item):
            if i == 0:
                price_info = self.get_price_info(prices, gconst.SHOP_PAYMENT_GOLD)
                if not price_info:
                    price_info = self.get_price_info(prices, gconst.SHOP_PAYMENT_DIAMON)
            else:
                price_info = self.get_price_info(prices, gconst.SHOP_PAYMENT_YUANBAO)
            if not price_info:
                btn_price.setVisible(False)
                continue
            btn_price.setVisible(True)
            template_utils.init_price_template(price_info, btn_price.temp_price, color=mall_const.DARK_PRICE_COLOR)
            goods_payment = price_info.get('goods_payment')
            real_price = price_info.get('real_price')

            @btn_price.btn_common_big.unique_callback()
            def OnClick(btn, touch, goods_payment=goods_payment, real_price=real_price):

                def _pay():
                    global_data.player.buy_goods(self.goods_id, 1, goods_payment)

                if not mall_utils.check_payment(goods_payment, real_price, cb=_pay):
                    return
                _pay()

        opening, left_time = mall_utils.get_goods_is_open(goods_id)
        opening and template_utils.show_remain_time_countdown(self.panel.nd_time, self.panel.lab_time, left_time, 80335)

    def check_limit_open_gold_pay(self, goods_id):
        prices = mall_utils.get_mall_item_price(goods_id, pick_list=self.pick_list)
        new_prices = []
        for price_info in prices:
            goods_payment = price_info.get('goods_payment')
            if goods_payment == gconst.SHOP_PAYMENT_GOLD:
                enable, _ = mall_utils.limite_pay_by_goods_payment(gconst.SHOP_PAYMENT_GOLD, goods_id)
                if not enable:
                    continue
            new_prices.append(price_info)

        return new_prices

    def on_close(self, *args):
        self.close()
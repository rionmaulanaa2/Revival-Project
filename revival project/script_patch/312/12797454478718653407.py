# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/DiamondExchangeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, SHOP_PAYMENT_DIAMON
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.client.const import mall_const
from logic.gcommon.item import item_const
from common.const import uiconst
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class DiamondExchangeUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/diamond_exchange'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        pass

    def init_event(self):
        pass

    def on_finalize_panel(self):
        pass

    def init_widget(self, consumed, diamond, pay_tip=True, cb=None):
        needed_diamond = consumed - diamond
        from common.cfg import confmgr
        import math
        goods_id = mall_const.MALL_DIAMOND_GIFT
        mall_item_conf = confmgr.get('mall_config', goods_id, default={})
        count = int(math.ceil(float(needed_diamond) / mall_item_conf['num']))
        price_info = mall_utils.get_mall_item_price(goods_id, count)[0]
        goods_payment = price_info['goods_payment']
        real_price = price_info['real_price']
        from logic.gutils.template_utils import get_money_rich_text
        template_utils.init_price_template(price_info, self.panel.temp_ticket, color=mall_const.DARK_PRICE_COLOR)
        need_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (item_utils.get_money_icon(SHOP_PAYMENT_DIAMON), needed_diamond)
        real_price_txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (item_utils.get_money_icon(SHOP_PAYMENT_YUANBAO), real_price)
        content = get_text_by_id(80797, {'diamond': need_price_txt,'num': real_price_txt})
        self.panel.lab_top.SetString(content)

        @self.panel.temp_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.close()

        @self.panel.temp_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(btn, touch, goods_payment=goods_payment, price=real_price, pay_tip=pay_tip, cb=cb):
            if mall_utils.check_yuanbao(price, pay_tip):
                global_data.player.buy_goods(goods_id, count, goods_payment, need_show=item_const.ITEM_SHOW_TYPE_NONE)
                if cb:
                    cb()
                self.close()

    def on_close(self, *args):
        self.close()
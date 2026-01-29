# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MeowUpgradeConfirmUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.const import uiconst
from logic.gutils import mall_utils
from logic.gutils import template_utils
from common.cfg import confmgr
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.JapanShoppingTips import show_with_japan_shopping_tips

@show_with_japan_shopping_tips
class MeowUpgradeConfirmUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'mall/coin_upgrade_confirm'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_close'
       }

    def on_init_panel(self, goods_id):
        super(MeowUpgradeConfirmUI, self).on_init_panel()
        self.goods_id = goods_id
        conf = confmgr.get('mall_config', goods_id, default={})
        self.goods_type = conf.get('cGoodsInfo', {}).get('goods_type')
        self.init_widget()
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_meow_capacity_lv': self.set_total_price
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)

    def init_widget(self):
        path = mall_utils.get_goods_pic_path(self.goods_id)
        name = mall_utils.get_goods_name(self.goods_id)
        self.panel.temp_coin_before.img_coin.SetDisplayFrameByPath('', path)
        self.panel.temp_coin_after.img_coin.SetDisplayFrameByPath('', path)
        self.panel.temp_coin_max.img_coin.SetDisplayFrameByPath('', path)
        self.panel.lab_detail.setVisible(False)
        self.panel.lab_coin.SetString(name)
        _, self.last_lv, _, _, _, _ = template_utils.get_meow_prices(self.goods_id)
        self.set_total_price()

    def set_total_price(self, *args):
        prices, lv, size, next_lv, next_size, max_lv = template_utils.get_meow_prices(self.goods_id)
        is_max_lv = max_lv <= lv
        if self.last_lv < lv:
            if is_max_lv:
                self.panel.temp_coin_max.PlayAnimation('up')
            else:
                self.panel.temp_coin_before.PlayAnimation('up')
                self.panel.temp_coin_after.PlayAnimation('up')
            self.last_lv = lv
        self.panel.temp_coin_before.setVisible(not is_max_lv)
        self.panel.temp_coin_after.setVisible(not is_max_lv)
        self.panel.temp_coin_max.setVisible(is_max_lv)
        self.panel.temp_price.setVisible(not is_max_lv)
        self.panel.nd_arrow.setVisible(not is_max_lv)
        self.panel.temp_btn_buy.btn_common.SetEnable(not is_max_lv)
        if is_max_lv:
            self.panel.temp_btn_buy.btn_common.SetText(18266)
            self.panel.temp_coin_max.lab_level.SetString('LV.%d' % lv)
            self.panel.temp_coin_max.lab_coin_num.SetString(str(size))
            return
        self.panel.temp_btn_buy.btn_common.SetText('')
        self.panel.temp_coin_before.lab_level.SetString('LV.%d' % lv)
        self.panel.temp_coin_before.lab_coin_num.SetString(str(size))
        self.panel.temp_coin_after.lab_level.SetString('LV.%d' % next_lv)
        self.panel.temp_coin_after.lab_coin_num.SetString(str(next_size))
        if not prices:
            return
        for i, node in enumerate([self.panel.temp_btn_buy]):
            if not node:
                continue
            if i < len(prices):
                node.setVisible(True)
                price_info = prices[i]
                goods_payment = price_info.get('goods_payment')
                real_price = price_info.get('real_price')
                template_utils.init_price_template(price_info, node.temp_price)

                @node.btn_common.unique_callback()
                def OnClick(btn, touch, goods_payment=goods_payment, real_price=real_price):
                    limit = mall_utils.limite_pay(self.goods_id)
                    if limit:
                        return

                    def _pay():
                        if self.goods_type:
                            global_data.player.upgrade_meow_capacity(self.goods_type)
                            global_data.player.sa_log_anniversary_gift_state_buy(self.goods_id)

                    if not mall_utils.check_payment(goods_payment, real_price, cb=_pay):
                        return
                    from logic.gutils.mall_buy_confirm_func import goods_buy_need_confirm
                    if goods_buy_need_confirm(self.goods_id, call_back=_pay):
                        return
                    _pay()
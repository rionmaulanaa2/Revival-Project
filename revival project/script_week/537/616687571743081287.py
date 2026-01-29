# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuySeasonCardUITestBPlus.py
from __future__ import absolute_import
from .BuySeasonCardBaseUI import BuySeasonCardBaseUI
from logic.gutils.template_utils import init_price_template
from logic.gutils.item_utils import buy_season_pass_card_confirm
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L3

class BuySeasonCardUITestBPlus(BuySeasonCardBaseUI):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/card_buy_test_b2'
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn',
       'temp_btn_buy.btn_common_big.OnClick': 'on_click_buy_btn'
       }

    def _init_card_price(self):
        season_pass_type_data = self._season_pass_data.season_pass_type_data
        trial_real_price = season_pass_type_data[SEASON_PASS_L3]['yuanbao_consumed']
        trial_original_price = season_pass_type_data[SEASON_PASS_L3]['orginal_yuanbao']
        real_price = season_pass_type_data[SEASON_PASS_L1]['yuanbao_consumed']
        original_price = season_pass_type_data[SEASON_PASS_L1]['orginal_yuanbao']
        real_price -= trial_real_price
        original_price -= trial_original_price
        discount_price = None if real_price == original_price else real_price
        price_info = {'original_price': original_price,
           'discount_price': discount_price,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        price_node = self.panel.temp_price
        color = ['#SS', '#SR', '#BC']
        init_price_template(price_info, price_node, color=color)
        return

    def on_click_buy_btn(self, btn, *args):
        season_pass_type_data = self._season_pass_data.season_pass_type_data
        trial_real_price = season_pass_type_data[SEASON_PASS_L3]['yuanbao_consumed']
        real_price = season_pass_type_data[SEASON_PASS_L1]['yuanbao_consumed']
        real_price -= trial_real_price
        context = get_text_by_id(81479).format(real_price)
        buy_season_pass_card_confirm(SEASON_PASS_L1, context)
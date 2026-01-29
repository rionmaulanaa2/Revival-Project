# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/CardBuyCheck.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L2, SEASON_CARD
from logic.gutils.item_utils import get_battle_pass_reward_id_list, get_season_pass_reward_lv_id
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.battle_pass_utils import get_season_card_price_info

class CardBuyCheck(WindowMediumBase):
    PANEL_CONFIG_NAME = 'battle_pass/card_buy_check'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_bg.temp_btn_buy.btn_common_big.OnClick': 'on_click_buy_card'
       }

    def on_init_panel(self):
        super(CardBuyCheck, self).on_init_panel()
        self.set_custom_close_func(self.on_click_back_btn)
        self._init_params()
        self.hide_main_ui()
        self._init_card_reward_desc()
        self._init_price()

    def _init_params(self):
        self._disappearing = False
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        self._season_pass_data = get_now_season_pass_data()
        self._active_level = self._season_pass_data.season_pass_type_data.get(str(SEASON_PASS_L2))['activate_lv']
        self._sp_lv, _ = global_data.player.get_battlepass_info()
        season_pass_lv_cap = self._season_pass_data.SEASON_PASS_LV_CAP
        self._can_buy_lv = season_pass_lv_cap if self._sp_lv + self._active_level > season_pass_lv_cap else self._sp_lv + self._active_level
        if global_data.player.has_buy_final_card():
            self._can_buy_lv = self._sp_lv
        self.panel.nd_level.lab_level.SetString(str(self._can_buy_lv))

    def _init_price(self):
        has_buy_card = global_data.player or False if 1 else global_data.player.has_buy_final_card()
        if has_buy_card:
            self.panel.temp_btn_buy.btn_common_big.SetEnable(False)
            self.panel.temp_btn_buy.btn_common_big.SetText(12014)
            self.panel.temp_btn_buy.temp_price.setVisible(False)
        else:
            from logic.gutils.template_utils import init_price_template
            price_info, _, _ = get_season_card_price_info(self._season_pass_data, SEASON_PASS_L2)
            self.panel.temp_btn_buy.btn_common_big.SetEnable(True)
            self.panel.temp_btn_buy.btn_common_big.SetText('')
            self.panel.temp_btn_buy.temp_price.setVisible(True)
            price_node = self.panel.temp_btn_buy.temp_price
            init_price_template(price_info, price_node, color=DARK_PRICE_COLOR)

    def _init_card_reward_desc(self):
        from logic.gutils.item_utils import get_item_rare_degree
        from logic.gcommon.item.item_const import RARE_DEGREE_4
        self._item_dict = {}
        reward_list = []
        start_lv = self._sp_lv + 1 if global_data.player.has_buy_one_kind_season_card() else self._sp_lv
        for lv in range(start_lv, self._can_buy_lv + 1):
            reward_lv = get_battle_pass_reward_id_list(lv, SEASON_CARD)
            reward_list.extend(reward_lv)

        for item_id, num in reward_list:
            item_num = self._item_dict.setdefault(item_id, 0)
            self._item_dict[item_id] = item_num + num

        for item_id, item_num in six_ex.items(self._item_dict):
            rare_degree = get_item_rare_degree(item_id, item_num)
            if rare_degree == RARE_DEGREE_4:
                item = self.panel.list_reward.AddTemplateItem(index=0)
            else:
                item = self.panel.list_reward.AddTemplateItem()
            init_tempate_mall_i_item(item, item_id, item_num, show_rare_degree=True, show_tips=True)

    def on_click_back_btn(self, *args):
        if self._disappearing:
            return
        self._disappearing = True
        self.close()

    def on_click_buy_card(self, *args):
        from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L2
        from logic.gutils.mall_utils import check_yuanbao
        _, yuan_bao_consumed, _ = get_season_card_price_info(self._season_pass_data, SEASON_PASS_L2)
        if check_yuanbao(yuan_bao_consumed, True):
            global_data.player.activate_battlepass_type(SEASON_PASS_L2)

    def on_finalize_panel(self):
        self._season_pass_data = None
        self.set_custom_close_func(None)
        self.show_main_ui()
        return
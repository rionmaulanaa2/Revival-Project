# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuyNewBieCardUI.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battlepass_const import NEWBIE_PASS_TYPE_1, NEWBIE_PASS_L2
from data.newbiepass_data import get_lv_reward, newbiepass_type_data, BUY_CARD_SHOW_LEVEL, NEWBIEPASS_LV_CAP
from logic.gutils import template_utils
EXCEPT_HIDE_UI_LIST = []
from common.const import uiconst

class BuyNewBieCardUI(BasePanel):
    PANEL_CONFIG_NAME = 'new_pass/new_pass_buy'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn',
       'temp_btn_buy_special.btn_common_big.OnClick': 'on_click_buy_btn'
       }

    def on_init_panel(self):
        self.disappearing = False
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self._init_card_price()
        self._init_reward_display()
        self._init_level_reward()
        self.panel.PlayAnimation('appear')

    def _init_level_reward(self):
        for lv in BUY_CARD_SHOW_LEVEL:
            reward_lv = get_lv_reward(str(NEWBIE_PASS_L2), lv)
            reward_conf = confmgr.get('common_reward_data', str(reward_lv))
            reward_list = reward_conf.get('reward_list', [])
            item_no, item_num = reward_list[0]
            item_name = item_utils.get_lobby_item_name(item_no)
            item = self.panel.list_reward_special.AddTemplateItem()
            item.lab_level.SetString('Lv' + str(lv))
            template_utils.init_tempate_mall_i_item(item.temp_reward, item_no)
            item.lab_name.SetString(item_name)

    def _init_reward_display(self):
        reward_id = newbiepass_type_data.get(str(NEWBIE_PASS_TYPE_1)).get('reward_id')
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        self.panel.nd_special_reward.lab_reward_name.SetString(item_name)
        self.panel.nd_special_reward.img_reward.SetDisplayFrameByPath('', pic_path)
        text = get_text_by_id(602015).format(str(NEWBIEPASS_LV_CAP))
        self.panel.nd_special.nd_card_special.lab_tips.SetString(text)

    def _init_card_price(self):
        from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
        from logic.gutils.template_utils import init_price_template
        from logic.client.const.mall_const import DARK_PRICE_COLOR
        self.yuanbao_consume = newbiepass_type_data.get(str(NEWBIE_PASS_TYPE_1)).get('yuanbao_consumed', 100)
        yuanbao_original = newbiepass_type_data.get(str(NEWBIE_PASS_TYPE_1)).get('orginal_yuanbao', self.yuanbao_consume * 2)
        price_node = self.panel.temp_btn_buy_special.temp_price_special
        price_info = {'original_price': yuanbao_original,
           'discount_price': self.yuanbao_consume,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        init_price_template(price_info, price_node, color=DARK_PRICE_COLOR)

    def on_click_buy_btn(self, *args):
        from logic.gutils.mall_utils import check_yuanbao
        if check_yuanbao(self.yuanbao_consume, True):
            global_data.player.activate_newbiepass_type(str(NEWBIE_PASS_TYPE_1))

    def on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()

    def on_finalize_panel(self):
        self.show_main_ui()
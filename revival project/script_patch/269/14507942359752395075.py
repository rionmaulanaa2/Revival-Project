# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/PreviewReward.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_mall_i_item
import logic.gcommon.common_const.battlepass_const as bp_const
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class PreviewReward(WindowMediumBase):
    PANEL_CONFIG_NAME = 'battle_pass/reward_review'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_btn_buy.btn_common_big.OnClick': 'on_click_buy_card'
       }

    def on_init_panel(self):
        super(PreviewReward, self).on_init_panel()
        self.set_custom_close_func(self.on_click_back_btn)
        self.disappearing = False
        self._pass_type = bp_const.SEASON_CARD

    def show_card_reward_desc(self, pass_type):
        from logic.gutils.item_utils import get_item_rare_degree
        from logic.gcommon.item.item_const import RARE_DEGREE_4
        self._pass_type = pass_type
        if pass_type == bp_const.NEWBIE_CARD:
            from data import newbiepass_data
            get_lv_reward_func = newbiepass_data.get_lv_reward
            BUY_CARD_SHOW_LEVEL = newbiepass_data.BUY_CARD_SHOW_LEVEL
            SHOW_REWARD_CARD = bp_const.NEWBIE_PASS_L2
            self.panel.temp_btn_buy.btn_common_big.SetText(80835)
        else:
            from logic.gutils.battle_pass_utils import get_now_season_pass_data
            season_data = get_now_season_pass_data()
            get_lv_reward_func = season_data.get_lv_reward
            BUY_CARD_SHOW_LEVEL = season_data.BUY_CARD_REWARD_SHOW
            SHOW_REWARD_CARD = bp_const.SEASON_PASS_L2
            self.panel.temp_btn_buy.btn_common_big.SetText(81099)
        item_dict = {}
        for lv in BUY_CARD_SHOW_LEVEL:
            reward_lv = get_lv_reward_func(str(SHOW_REWARD_CARD), lv)
            reward_conf = confmgr.get('common_reward_data', str(reward_lv))
            if reward_conf:
                reward_list = reward_conf.get('reward_list', [])
                for item_no, item_num in reward_list:
                    ori_num = item_dict.setdefault(item_no, 0)
                    item_dict[item_no] = ori_num + item_num

        for item_no, item_num in six_ex.items(item_dict):
            rare_degree = get_item_rare_degree(item_no, item_num)
            if rare_degree == RARE_DEGREE_4:
                item = self.panel.list_reward.AddTemplateItem(index=0)
            else:
                item = self.panel.list_reward.AddTemplateItem()
            item.btn_choose.SetNoEventAfterMove(False, '10w')
            item.btn_choose.SetSwallowTouch(False)
            init_tempate_mall_i_item(item, item_no, 1, show_rare_degree=True, show_tips=True)

    def on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.close()

    def on_click_buy_card(self, *args):
        self.close()
        if self._pass_type == bp_const.NEWBIE_CARD:
            global_data.ui_mgr.show_ui('BuyNewBieCardUI', 'logic.comsys.battle_pass')
        else:
            from logic.gutils.battle_pass_utils import get_buy_season_card_ui_name
            global_data.ui_mgr.show_ui(get_buy_season_card_ui_name(), 'logic.comsys.battle_pass')

    def on_finalize_panel(self):
        self.set_custom_close_func(None)
        return
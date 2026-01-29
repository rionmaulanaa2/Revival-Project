# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuyCardConfirmUI.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_CONFIRM, DIALOG_LAYER_ZORDER
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L2
from logic.gutils.item_utils import get_item_rare_degree
from common.const import uiconst

class BuyCardConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/battle_pass_unlock'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'temp_btn_close.btn_common_big.OnClick': 'on_click_back_btn',
       'temp_btn_go.btn_common_big.OnClick': 'on_click_buy_btn'
       }

    def on_init_panel(self, sp_card_type, reward_items, content='', confirm_callback=None, cancel_callback=None):
        self._sp_card_type = sp_card_type
        self._cancel_cb = cancel_callback
        self._confirm_cb = confirm_callback
        self._item_dict = {}
        if len(reward_items):
            self.panel.lab_desc.SetString(content)
            self._init_reward_preview(reward_items)
        else:
            self.panel.lab_desc_2.setVisible(True)
            self.panel.lab_desc.setVisible(False)
            self.panel.nd_reward_list.setVisible(False)
            self.panel.nd_none.setVisible(False)
            self.panel.lab_desc_2.SetString(content)

        def _cb():
            if self.panel and self.panel.isValid():
                self.panel.PlayAnimation('loop')

        self.panel.PlayAnimation('appear')
        max_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.DelayCall(max_time, _cb)

    def _init_reward_preview(self, reward_items):
        need_more = False if len(reward_items) <= 10 else True
        list_award_show = self.panel.list_award_more if need_more else self.panel.list_award
        self.panel.list_award_more.setVisible(need_more)
        self.panel.list_award.setVisible(not need_more)
        for item_id, num in reward_items:
            item_num = self._item_dict.setdefault(item_id, 0)
            self._item_dict[item_id] = item_num + num

        rare_dict = {}
        for item_id, item_num in six_ex.items(self._item_dict):
            rare_degree = get_item_rare_degree(item_id, item_num)
            rare_dict.setdefault(rare_degree, [])
            rare_dict[rare_degree].append((item_id, item_num))

        keys = six_ex.keys(rare_dict)
        keys.sort(reverse=True)
        for rare_key in keys:
            for item_id, item_num in rare_dict[rare_key]:
                item = list_award_show.AddTemplateItem()
                init_tempate_mall_i_item(item, item_id, item_num, show_rare_degree=True, show_tips=True, show_jump=False)

        self.panel.nd_none.setVisible(False)

    def on_click_buy_btn(self, *args):
        if self._confirm_cb and callable(self._confirm_cb):
            self._confirm_cb()

    def on_click_back_btn(self, *args):
        self.close()
        if self._cancel_cb and callable(self._cancel_cb):
            self._cancel_cb()

    def _init_nd_none(self):
        if self._sp_card_type == SEASON_PASS_L1:
            from logic.gutils.battle_pass_utils import get_now_season_pass_data
            sp_data = get_now_season_pass_data()
            extra_reward_id = sp_data.season_pass_type_data.get(SEASON_PASS_L2).get('reward_id')
            if not extra_reward_id:
                return
            reward_conf = confmgr.get('common_reward_data', str(extra_reward_id))
            if not reward_conf:
                return
            reward_list = reward_conf.get('reward_list', [])
            node = [
             self.panel.nd_none.temp_reward_1, self.panel.nd_none.temp_reward_2, self.panel.nd_none.temp_reward_3]
            for idx, reward_info in enumerate(reward_list):
                if idx >= len(node):
                    break
                item_no, item_num = reward_info
                init_tempate_mall_i_item(node[idx], item_no, show_tips=True, show_jump=False)

            self.panel.nd_none.setVisible(True)
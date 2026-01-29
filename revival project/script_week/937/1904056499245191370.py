# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuySeasonCardUI.py
from __future__ import absolute_import
from six.moves import range
import time
from common.cfg import confmgr
from .BuySeasonCardBaseUI import BuySeasonCardBaseUI
from logic.gutils.template_utils import init_price_template, init_tempate_mall_i_item
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L2, SEASON_PASS_L3
from logic.gutils.battle_pass_utils import get_season_card_price_info
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang

class BuySeasonCardUI(BuySeasonCardBaseUI):
    PANEL_CONFIG_NAME = 'battle_pass/s4_s9/card_buy_test_b'
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_ACTION_EVENT = {'temp_btn_back.OnClick': 'on_click_back_btn',
       'temp_btn_buy_special.OnClick': '_on_click_buy_btn',
       'temp_btn_buy_normal.OnClick': '_on_click_buy_btn',
       'temp_btn_buy_common.OnClick': '_on_click_buy_btn'
       }

    def _play_animation(self):
        animation_time = self.panel.GetAnimationMaxRunTime('show')
        now_bp_types = global_data.player or set() if 1 else global_data.player.get_battlepass_types()

        def finished_show--- This code section failed: ---

  45       0  LOAD_CONST            1  ''
           3  STORE_FAST            0  'card_num'

  46       6  SETUP_LOOP           45  'to 54'
           9  LOAD_GLOBAL           0  'SEASON_PASS_L3'
          12  LOAD_GLOBAL           1  'SEASON_PASS_L1'
          15  LOAD_GLOBAL           2  'SEASON_PASS_L2'
          18  BUILD_TUPLE_3         3 
          21  GET_ITER         
          22  FOR_ITER             28  'to 53'
          25  STORE_FAST            1  'season_card'

  47      28  LOAD_FAST             1  'season_card'
          31  LOAD_DEREF            0  'now_bp_types'
          34  COMPARE_OP            6  'in'
          37  POP_JUMP_IF_FALSE    22  'to 22'

  49      40  POP_JUMP_IF_FALSE     2  'to 2'
          43  INPLACE_ADD      
          44  STORE_FAST            0  'card_num'
          47  JUMP_BACK            22  'to 22'
          50  JUMP_BACK            22  'to 22'
          53  POP_BLOCK        
        54_0  COME_FROM                '6'

  54      54  POP_BLOCK        
          55  POP_BLOCK        
          56  POP_BLOCK        
          57  COMPARE_OP            2  '=='
          60  POP_JUMP_IF_FALSE    72  'to 72'

  55      63  LOAD_CONST            3  'light_01'
          66  STORE_FAST            2  'buy_anim_name'
          69  JUMP_FORWARD         36  'to 108'

  56      72  JUMP_FORWARD          2  'to 77'
          75  COMPARE_OP            2  '=='
          78  POP_JUMP_IF_FALSE   102  'to 102'
          81  LOAD_GLOBAL           1  'SEASON_PASS_L1'
          84  LOAD_DEREF            0  'now_bp_types'
          87  COMPARE_OP            7  'not-in'
        90_0  COME_FROM                '78'
          90  POP_JUMP_IF_FALSE   102  'to 102'

  57      93  LOAD_CONST            4  'light_02'
          96  STORE_FAST            2  'buy_anim_name'
          99  JUMP_FORWARD          6  'to 108'

  59     102  LOAD_CONST            5  'light_03'
         105  STORE_FAST            2  'buy_anim_name'
       108_0  COME_FROM                '99'
       108_1  COME_FROM                '69'

  60     108  LOAD_DEREF            1  'self'
         111  LOAD_ATTR             3  'panel'
         114  LOAD_ATTR             4  'PlayAnimation'
         117  LOAD_FAST             2  'buy_anim_name'
         120  CALL_FUNCTION_1       1 
         123  POP_TOP          

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 40

        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.panel.SetTimeOut(1, finished_show)

        def PlayAnim2(*args):
            self.panel.PlayAnimation('light')

        self.panel.SetTimeOut(0.67, PlayAnim2)
        has_card = True if len(now_bp_types) > 0 else False
        self.panel.lab_tip_common.setVisible(not has_card)
        self.panel.lab_tip_normal.setVisible(not has_card)
        if SEASON_PASS_L3 in now_bp_types and SEASON_PASS_L1 not in now_bp_types:
            self.panel.lab_tip_normal2.setVisible(True)
        else:
            self.panel.lab_tip_normal2.setVisible(False)
        self.panel.lab_tip_special.setVisible(has_card)

    def _init_season_time_limited_reward(self):
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_belong_name
        lab_dict = {SEASON_PASS_L1: --- This code section failed: ---

  87       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'lab_rich_driver'
           9  LOAD_ATTR             2  'SetString'
          12  LOAD_GLOBAL           3  'get_text_by_id'
          15  LOAD_CONST            1  83462
          18  BUILD_MAP_1           1 
          21  BUILD_MAP_2           2 
          24  STORE_MAP        
          25  CALL_FUNCTION_2       2 
          28  CALL_FUNCTION_1       1 
          31  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `STORE_MAP' instruction at offset 24
,SEASON_PASS_L2: --- This code section failed: ---

  88       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'lab_rich_mecha'
           9  LOAD_ATTR             2  'SetString'
          12  LOAD_GLOBAL           3  'get_text_by_id'
          15  LOAD_CONST            1  83461
          18  BUILD_MAP_1           1 
          21  BUILD_MAP_2           2 
          24  STORE_MAP        
          25  CALL_FUNCTION_2       2 
          28  CALL_FUNCTION_1       1 
          31  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `STORE_MAP' instruction at offset 24
}
        from logic.gutils.battle_pass_utils import get_now_season_money, get_now_season_pass_data
        season_data = get_now_season_pass_data()
        core_item_list = tuple(season_data.two_core_reward)
        for idx, season_card in enumerate([SEASON_PASS_L1, SEASON_PASS_L2]):
            item_name = get_lobby_item_belong_name(core_item_list[idx])
            lab_dict[season_card](item_name)

    def _init_card_price(self):
        has_discount_func = self._season_pass_data.season_pass_type_data[SEASON_PASS_L2].get('has_discount', None)
        if has_discount_func and callable(has_discount_func) and global_data.player:
            if has_discount_func(global_data.player):
                self.panel.nd_tips.setVisible(True)
        node_dict = {SEASON_PASS_L1: self.panel.temp_btn_buy_normal,SEASON_PASS_L2: self.panel.temp_btn_buy_special,
           SEASON_PASS_L3: self.panel.temp_btn_buy_common
           }
        price_node_dict = {SEASON_PASS_L1: self.panel.temp_price_normal,
           SEASON_PASS_L2: self.panel.temp_price_special,
           SEASON_PASS_L3: self.panel.temp_price_common
           }
        for season_card in (SEASON_PASS_L1, SEASON_PASS_L2, SEASON_PASS_L3):
            card_price_info, _, btn_txt_id = get_season_card_price_info(self._season_pass_data, season_card)
            node = node_dict[season_card]
            price_node = price_node_dict[season_card]
            if not card_price_info:
                node.SetEnable(False)
                price_node.img_price.setVisible(False)
                price_node.lab_price_before.setVisible(False)
                price_node.setVisible(False)
                node.SetText(btn_txt_id)
            else:
                price_node.setVisible(True)
                node.SetText('')
                color_def = ['#SS', '#SR', '#BC']
                init_price_template(card_price_info, price_node, color=color_def)

        self._init_battle_pass_gift_discount()
        return

    def _init_battle_pass_gift_discount(self):
        if not global_data.player:
            return
        battle_pass_gift = global_data.player.get_battle_pass_chance_gift()
        if not battle_pass_gift:
            self.panel.nd_recommend_tips.setVisible(False)
            self.panel.nd_discount_tag.setVisible(False)
            return
        discount = battle_pass_gift.get('discount', 0)
        if discount <= 0:
            return
        from logic.gutils import trigger_gift_utils
        discount_text = trigger_gift_utils.get_gift_discount_text(discount, get_cur_text_lang())
        nodes = [self.nd_discount_tag.tag_01, self.nd_discount_tag.tag_02, self.nd_discount_tag.tag_03]
        for node in nodes:
            discount_text = discount_text.replace('%', '')
            node.lab_num.SetString(get_text_by_id(608311).format(discount_text))

        self.panel.nd_discount_tag.setVisible(True)
        self.panel.nd_recommend_tips.setVisible(True)
        gift_discount_tip_node = global_data.ui_mgr.uis.load_template_create('battle_pass/i_battle_pass_recommend_tips', self.panel.nd_recommend_tips, name='nd_gift_discount')
        expire_time = battle_pass_gift.get('expire_time', 0)
        gift_level = battle_pass_gift.get('gift_level', 0)
        discount_string = get_text_by_id(610040).format(discount_text)
        if gift_level > 0:
            level_string = get_text_by_id(610041).format(str(gift_level))
            gift_discount_tip_node.lab_sp_info.SetString(get_text_by_id(610043).format(discount_string, level_string))
        else:
            gift_discount_tip_node.lab_sp_info.SetString(get_text_by_id(610042).format(discount_string))
        if expire_time > tutil.get_server_time():
            self._gift_discount_left_time_widget = LeftTimeCountDownWidget(gift_discount_tip_node, gift_discount_tip_node.nd_tips.lab_time, lambda timestamp: get_text_by_id(607014).format(tutil.get_readable_time_2(timestamp)))
            self._gift_discount_left_time_widget.begin_count_down_time(expire_time, self._time_up_callback, use_big_interval=True)

    def _time_up_callback(self):
        self.panel.nd_recommend_tips.setVisible(False)
        self._init_card_price()

    def _init_card_reward_desc(self):
        season_pass_card_desc = self._season_pass_data.season_pass_card_desc
        node_list = self.panel.list_reward_special
        node_len = len(season_pass_card_desc)
        self._now_idx = 0

        def async_load():
            load_time_tick = time.time()
            for i in range(self._now_idx, node_len):
                self._now_idx += 1
                card_desc = season_pass_card_desc[i]
                desc_id = card_desc[2]
                func_info = card_desc[3]
                item = node_list.AddTemplateItem()
                item.nd_special.lab_reward.SetString(desc_id)
                item.nd_special.temp_reward_special.setVisible(False)
                func_name = func_info.get('func', None)
                args = func_info.get('args', [])
                if func_name:
                    func = getattr(self, func_name)
                    func and func(item, *args)
                if time.time() - load_time_tick > self._load_time:
                    self.SetTimeOut(self._interval_time, async_load, tag=self.ASYNC_LOAD_TAG)
                    return

            return

        async_load()

    def check_level_up_reward(self, item, *args):
        item.nd_special.btn_check.setVisible(True)

        @item.nd_special.btn_check.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('CardBuyCheck', 'logic.comsys.battle_pass')

    def show_special_reward(self, item, *args):
        season_pass_type_data = self._season_pass_data.season_pass_type_data
        reward_idx = args[0]
        reward_id = season_pass_type_data.get(str(SEASON_PASS_L2)).get('reward_id')
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[reward_idx]
        item.nd_special.temp_reward_special.setVisible(True)
        init_tempate_mall_i_item(item.nd_special.temp_reward_special, item_no, item_num=item_num, show_tips=True)

    def _on_click_buy_btn(self, btn, *args):
        if btn == self.panel.temp_btn_buy_normal:
            card_type = SEASON_PASS_L1
            text_id = 608451
        elif btn == self.panel.temp_btn_buy_common:
            card_type = SEASON_PASS_L3
            text_id = 608450
        else:
            card_type = SEASON_PASS_L2
            text_id = 608452
        from logic.gutils.item_utils import buy_season_pass_card_confirm
        card_price_info, real_price, btn_txt_id = get_season_card_price_info(self._season_pass_data, card_type)
        context = get_text_by_id(text_id).format(real_price)
        buy_season_pass_card_confirm(card_type, context)

    def _on_show_desc(self, *args):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        content_text_id = 608449 if G_IS_NA_PROJECT else 608448
        dlg.set_show_rule(get_text_by_id(608435), get_text_by_id(content_text_id))
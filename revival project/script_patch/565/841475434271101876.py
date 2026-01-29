# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuySeasonCardBaseUI.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.const import uiconst
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L3

class BuySeasonCardBaseUI(BasePanel):
    ASYNC_LOAD_TAG = 50001
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    GLOBAL_EVENT = {'season_pass_update_lv': 'on_update_lv'
       }
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn'
       }

    def show(self):
        self.hide_main_ui()
        self.clear_show_count_dict()
        self._play_animation()

    def on_init_panel--- This code section failed: ---

  41       0  LOAD_GLOBAL           0  'False'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  '_disappearing'

  43       9  LOAD_CONST            1  ''
          12  LOAD_CONST            2  ('get_now_season_pass_data',)
          15  IMPORT_NAME           2  'logic.gutils.battle_pass_utils'
          18  IMPORT_FROM           3  'get_now_season_pass_data'
          21  STORE_FAST            1  'get_now_season_pass_data'
          24  POP_TOP          

  44      25  LOAD_FAST             1  'get_now_season_pass_data'
          28  CALL_FUNCTION_0       0 
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            4  '_season_pass_data'

  46      37  LOAD_CONST            0  ''
          40  LOAD_FAST             0  'self'
          43  STORE_ATTR            6  '_bg_ui'

  48      46  LOAD_CONST            3  0.01
          49  LOAD_FAST             0  'self'
          52  STORE_ATTR            7  '_load_time'

  49      55  LOAD_CONST            4  0.03
          58  LOAD_FAST             0  'self'
          61  STORE_ATTR            8  '_interval_time'

  51      64  LOAD_CONST            1  ''
          67  LOAD_CONST            5  ('SHOP_PAYMENT_YUANBAO',)
          70  IMPORT_NAME           9  'logic.gcommon.const'
          73  IMPORT_FROM          10  'SHOP_PAYMENT_YUANBAO'
          76  STORE_FAST            2  'SHOP_PAYMENT_YUANBAO'
          79  POP_TOP          

  52      80  LOAD_GLOBAL          11  'PriceUIWidget'
          83  LOAD_GLOBAL           6  '_bg_ui'
          86  LOAD_FAST             0  'self'
          89  LOAD_ATTR            12  'panel'
          92  LOAD_ATTR            13  'list_price'
          95  LOAD_CONST            7  'pnl_title'
          98  LOAD_GLOBAL           0  'False'
         101  CALL_FUNCTION_513   513 
         104  LOAD_FAST             0  'self'
         107  STORE_ATTR           14  '_price_top_widget'

  53     110  LOAD_FAST             0  'self'
         113  LOAD_ATTR            14  '_price_top_widget'
         116  LOAD_ATTR            15  'show_money_types'
         119  LOAD_FAST             2  'SHOP_PAYMENT_YUANBAO'
         122  BUILD_LIST_1          1 
         125  CALL_FUNCTION_1       1 
         128  POP_TOP          

  55     129  LOAD_FAST             0  'self'
         132  LOAD_ATTR            16  '_play_animation'
         135  CALL_FUNCTION_0       0 
         138  POP_TOP          

  56     139  LOAD_FAST             0  'self'
         142  LOAD_ATTR            17  '_init_season_time_limited_reward'
         145  CALL_FUNCTION_0       0 
         148  POP_TOP          

  57     149  LOAD_FAST             0  'self'
         152  LOAD_ATTR            18  '_init_card_price'
         155  CALL_FUNCTION_0       0 
         158  POP_TOP          

  58     159  LOAD_FAST             0  'self'
         162  LOAD_ATTR            19  '_init_card_reward_desc'
         165  CALL_FUNCTION_0       0 
         168  POP_TOP          

  59     169  LOAD_FAST             0  'self'
         172  LOAD_ATTR            20  'init_season_exclusive_reward'
         175  CALL_FUNCTION_0       0 
         178  POP_TOP          

  61     179  LOAD_CONST            0  ''
         182  LOAD_FAST             0  'self'
         185  STORE_ATTR           21  'bp_type'

  62     188  LOAD_CONST            0  ''
         191  LOAD_FAST             0  'self'
         194  STORE_ATTR           22  '_gift_discount_left_time_widget'

  63     197  LOAD_GLOBAL           0  'False'
         200  LOAD_FAST             0  'self'
         203  STORE_ATTR           23  '_open_from_battle_pass_gift'

  64     206  LOAD_CONST            0  ''
         209  LOAD_FAST             0  'self'
         212  STORE_ATTR           24  'battle_pass_reward_cb'

  66     215  LOAD_FAST             0  'self'
         218  LOAD_ATTR            25  'hide_main_ui'
         221  CALL_FUNCTION_0       0 
         224  POP_TOP          
         225  LOAD_CONST            0  ''
         228  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_513' instruction at offset 101

    def _play_animation(self):
        self.panel.PlayAnimation('appear')

    def set_level(self, battle_pass_type, old_lv, new_lv):
        self.bp_type = battle_pass_type
        self.old_lv = old_lv
        self.new_lv = new_lv

    def _init_season_time_limited_reward(self):
        pass

    def _init_card_price(self):
        pass

    def _init_card_reward_desc(self):
        pass

    def do_show_panel(self):
        super(BuySeasonCardBaseUI, self).do_show_panel()
        if self._bg_ui is None:
            self._bg_ui = global_data.ui_mgr.show_ui('SeasonPassCardBuyBg', 'logic.comsys.battle_pass')
            self._bg_ui.panel.PlayAnimation('show')
            t = self._bg_ui.panel.GetAnimationMaxRunTime('show')

            def _cb():
                if self._bg_ui:
                    self._bg_ui.panel.PlayAnimation('loop')

            self._bg_ui.SetTimeOut(t, _cb)
        if self._bg_ui:
            self._bg_ui.do_show_panel()
        return

    def do_hide_panel(self):
        super(BuySeasonCardBaseUI, self).do_hide_panel()
        if self._bg_ui:
            self._bg_ui.do_hide_panel()
        if self.bp_type is not None:
            ui = global_data.ui_mgr.show_ui('SeasonPassLevelUp', 'logic.comsys.battle_pass')
            if ui:
                ui.set_level(self.bp_type, self.old_lv, self.new_lv)
            self.bp_type = None
        return

    def init_season_exclusive_reward(self):
        season_pass_type_data = self._season_pass_data.season_pass_type_data
        list_node_dict = {SEASON_PASS_L1: self.panel.list_reward_normal,
           SEASON_PASS_L3: self.panel.list_reward_common
           }
        for season_pass_id, nd_list in six.iteritems(list_node_dict):
            core_reward_id_dict = season_pass_type_data.get(season_pass_id, {}).get('battlepass_core_reward_dict', {})
            if core_reward_id_dict:

                def my_cmp(a, b):
                    rare_a = get_item_rare_degree(a)
                    rare_b = get_item_rare_degree(b)
                    if a == b:
                        return six_ex.compare(a, b)
                    return six_ex.compare(rare_b, rare_a)

                reward_id_list = six_ex.keys(core_reward_id_dict)
                reward_id_list.sort(key=cmp_to_key(my_cmp))

                def on_create_callback(lv, idx, ui_item, reward_lst=reward_id_list, core_reward_info=core_reward_id_dict):
                    reward_id = reward_lst[idx]
                    count = core_reward_info[reward_id]
                    init_tempate_mall_i_item(ui_item, reward_id, item_num=count, show_tips=True)

                nd_list.BindMethod('OnCreateItem', on_create_callback)
                nd_list.DeleteAllSubItem()
                nd_list.SetInitCount(len(core_reward_id_dict))
            else:
                nd_list.setVisible(False)

    def on_update_lv(self, *args):
        if self._disappearing:
            return
        self._disappearing = True
        self.close()

    def on_click_back_btn(self, *args):
        if self._disappearing:
            return
        else:
            if self._open_from_battle_pass_gift:
                global_data.player.try_show_battle_pass_chance_gift(True)
                self._open_from_battle_pass_gift = False
            elif self.battle_pass_reward_cb:
                self.battle_pass_reward_cb()
                self.battle_pass_reward_cb = None
                self.close()
            else:
                self._disappearing = True
                self.close()
            return

    def on_finalize_panel(self):
        self._bg_ui = None
        self._season_pass_data = None
        self.destroy_widget('_price_top_widget')
        global_data.ui_mgr.close_ui('SeasonPassCardBuyBg')
        self.show_main_ui()
        if self.bp_type is not None:
            ui = global_data.ui_mgr.show_ui('SeasonPassLevelUp', 'logic.comsys.battle_pass')
            if ui:
                ui.set_level(self.bp_type, self.old_lv, self.new_lv)
            self.bp_type = None
        if self._gift_discount_left_time_widget:
            self._gift_discount_left_time_widget.destroy()
            self._gift_discount_left_time_widget = None
        return

    def set_from_battle_pass_gift(self, from_gift):
        self._open_from_battle_pass_gift = from_gift

    def set_battle_pass_reward_cb(self, cb):
        self.battle_pass_reward_cb = cb
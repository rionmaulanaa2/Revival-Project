# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLoginRebate.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils, jump_to_ui_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils.mall_utils import is_steam_pay
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_date_str

class ActivityLoginRebate(ActivityBase):
    show_cash_rp = True

    def __init__(self, dlg, activity_type):
        super(ActivityLoginRebate, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.activity_conf = conf
        ui_data = conf.get('cUiData', {})
        self.task_id = conf.get('cTask', '')
        self.children_task_list = task_utils.get_children_task(self.task_id)
        if not is_steam_pay() and not G_IS_NA_USER:
            self.goods_id = ui_data.get('goods_id', '') if 1 else ui_data.get('goods_id_steam', '')
            self.goods_info = None
            self.goods_list_name = ui_data.get('goods_list_name', '')
            return self.goods_list_name or None
        else:
            self.is_pc_global_pay = mall_utils.is_pc_global_pay()
            if global_data.lobby_mall_data and global_data.player:
                self.goods_info = global_data.lobby_mall_data.get_activity_sale_info(self.goods_list_name)
            return

    def on_init_panel(self):
        ActivityLoginRebate.show_cash_rp = False
        self.init_panel()
        self.update_widget()
        self.init_describe()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_widget,
           'task_prog_changed': self.update_widget,
           'buy_good_success': self.update_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        self.panel.lab_rich.SetString(get_text_by_id(634988 if not G_IS_NA_USER and not is_steam_pay() else 83478))

    def init_reward_widget(self):
        unreceived_text = '<outline=2 color = 0xD78400AA>{}</outline>'
        other_text = '<outline=2 color = 0x3894E5AA>{}</outline>'
        list_item = self.panel.list_item
        player = global_data.player
        if not player:
            return
        for i, item in enumerate(list_item.GetAllItem()):
            if i >= len(self.children_task_list):
                return
            item.bar.SetEnable(False)
            task_id = self.children_task_list[i]
            reward_status = player.get_task_reward_status(task_id)
            reward_list = task_utils.get_task_reward_list(task_id)
            task_conf = task_utils.get_task_conf_by_id(task_id)
            title_str = get_text_by_id(610120)
            item.bar_discount.setVisible(not G_IS_NA_USER and not is_steam_pay())
            item.bar_discount.img_mask_discount.setVisible(False)
            if i > 0:
                start_time = task_conf.get('start_time', 0)
                end_time = task_conf.get('end_time', 0)
                start_str = get_date_str('%Y.%m.%d', start_time).split('.', 1)[1]
                end_str = get_date_str('%Y.%m.%d', end_time).split('.', 1)[1]
                title_str = get_text_by_id(83479).format('{}-{}'.format(start_str, end_str))
            for j, (item_no, num) in enumerate(reward_list):
                lab = getattr(item, 'lab_name%d' % j)
                lab.setVisible(True)
                lab.SetString('{}*{}'.format(item_utils.get_lobby_item_name(item_no), num))

            if not self.is_unlock_rebate():
                item.nd_got.setVisible(False)
                item.btn_get.SetText(get_text_by_id(8213))
                item.btn_get.SetEnable(False)
                item.btn_get.SetSelect(False)
                item.bar.SetSelect(False)
                item.lab_title.SetString(other_text.format(title_str))
            elif reward_status == ITEM_RECEIVED:
                item.nd_got.setVisible(True)
                item.btn_get.SetText(get_text_by_id(80866))
                item.btn_get.SetSelect(False)
                item.btn_get.SetEnable(False)
                item.bar.SetSelect(False)
                item.lab_title.SetString(other_text.format(title_str))
                item.bar_discount.img_mask_discount.setVisible(True)
            elif reward_status == ITEM_UNRECEIVED:
                item.nd_got.setVisible(False)
                item.btn_get.SetText(get_text_by_id(80930))
                item.btn_get.SetEnable(True)
                item.btn_get.SetSelect(True)
                item.bar.SetSelect(True)
                item.lab_title.SetString(unreceived_text.format(title_str))

                @item.btn_get.unique_callback()
                def OnClick(btn, touch, _task_id=task_id):
                    self.on_click_receive_btn(_task_id)

            else:
                item.nd_got.setVisible(False)
                item.btn_get.SetText(get_text_by_id(2200))
                item.btn_get.SetEnable(False)
                item.btn_get.SetSelect(False)
                item.bar.SetSelect(False)
                item.lab_title.SetString(other_text.format(title_str))

    def on_click_receive_btn(self, task_id):
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_UNRECEIVED:
            global_data.player.receive_task_reward(task_id)

    def init_describe(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

    def init_btn_get(self):
        self.init_btn_buy()

        @self.panel.nd_content.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if not self.is_unlock_rebate():
                self.on_click_btn_buy()

    def init_btn_buy(self):
        btn_buy = self.panel.nd_content.btn_buy
        if self.is_unlock_rebate():
            btn_buy.SetEnable(False)
            btn_buy.SetText(12014)
            return
        if not self.goods_info:
            btn_buy.SetEnable(False)
            btn_buy.SetText('******')
            return
        if self.is_pc_global_pay or mall_utils.is_steam_pay():
            price_txt = mall_utils.get_pc_charge_price_str(self.goods_info)
        else:
            price_txt = mall_utils.get_charge_price_str(self.goods_info['goodsid'])
        btn_buy.SetEnable(True)
        btn_buy.SetText(mall_utils.adjust_price(str(price_txt)))

    def on_click_btn_buy(self, *args):
        if self.is_pc_global_pay:
            jump_to_ui_utils.jump_to_web_charge()
        elif self.goods_info:
            global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

    def is_unlock_rebate(self):
        player = global_data.player
        if not player:
            return False
        bought_num = player.buy_num_all_dict.get(self.goods_id, 0)
        return bought_num > 0

    def update_widget(self, *args):
        is_unlock = self.is_unlock_rebate()
        self.init_reward_widget()
        self.init_btn_get()
        global_data.emgr.refresh_activity_redpoint.emit()

    @staticmethod
    def show_bought_rp--- This code section failed: ---

 195       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_activity_config'
           9  LOAD_CONST            2  'default'
          12  BUILD_MAP_0           0 
          15  CALL_FUNCTION_258   258 
          18  STORE_FAST            1  'conf'

 196      21  LOAD_FAST             1  'conf'
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            3  'cUiData'
          30  BUILD_MAP_0           0 
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'ui_data'

 197      39  LOAD_GLOBAL           2  'is_steam_pay'
          42  CALL_FUNCTION_0       0 
          45  UNARY_NOT        
          46  POP_JUMP_IF_FALSE    74  'to 74'
          49  LOAD_GLOBAL           3  'G_IS_NA_USER'
          52  UNARY_NOT        
        53_0  COME_FROM                '46'
          53  POP_JUMP_IF_FALSE    74  'to 74'
          56  LOAD_FAST             2  'ui_data'
          59  LOAD_ATTR             1  'get'
          62  LOAD_CONST            4  'goods_id'
          65  LOAD_CONST            5  ''
          68  CALL_FUNCTION_2       2 
          71  JUMP_FORWARD         15  'to 89'
          74  LOAD_FAST             2  'ui_data'
          77  LOAD_ATTR             1  'get'
          80  LOAD_CONST            6  'goods_id_steam'
          83  LOAD_CONST            5  ''
          86  CALL_FUNCTION_2       2 
        89_0  COME_FROM                '71'
          89  STORE_FAST            3  'goods_id'

 199      92  LOAD_GLOBAL           4  'global_data'
          95  LOAD_ATTR             5  'player'
          98  STORE_FAST            4  'player'

 200     101  LOAD_FAST             4  'player'
         104  POP_JUMP_IF_TRUE    111  'to 111'

 201     107  LOAD_GLOBAL           6  'False'
         110  RETURN_END_IF    
       111_0  COME_FROM                '104'

 202     111  LOAD_FAST             4  'player'
         114  LOAD_ATTR             7  'buy_num_all_dict'
         117  LOAD_ATTR             1  'get'
         120  LOAD_FAST             3  'goods_id'
         123  LOAD_CONST            7  ''
         126  CALL_FUNCTION_2       2 
         129  STORE_FAST            5  'bought_num'

 203     132  LOAD_FAST             5  'bought_num'
         135  LOAD_CONST            7  ''
         138  COMPARE_OP            4  '>'
         141  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_258' instruction at offset 15

    @staticmethod
    def show_task_rp--- This code section failed: ---

 207       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_activity_config'
           9  LOAD_CONST            2  'default'
          12  BUILD_MAP_0           0 
          15  CALL_FUNCTION_258   258 
          18  STORE_FAST            1  'conf'

 208      21  LOAD_FAST             1  'conf'
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            3  'cTask'
          30  LOAD_CONST            4  ''
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'task_id'

 209      39  LOAD_GLOBAL           2  'task_utils'
          42  LOAD_ATTR             3  'get_children_task'
          45  LOAD_FAST             2  'task_id'
          48  CALL_FUNCTION_1       1 
          51  STORE_FAST            3  'children_task_list'

 210      54  SETUP_LOOP           52  'to 109'
          57  LOAD_FAST             3  'children_task_list'
          60  GET_ITER         
          61  FOR_ITER             40  'to 104'
          64  STORE_FAST            2  'task_id'

 211      67  LOAD_GLOBAL           4  'global_data'
          70  LOAD_ATTR             5  'player'
          73  LOAD_ATTR             6  'get_task_reward_status'
          76  LOAD_FAST             2  'task_id'
          79  CALL_FUNCTION_1       1 
          82  STORE_FAST            4  'reward_status'

 212      85  LOAD_FAST             4  'reward_status'
          88  LOAD_GLOBAL           7  'ITEM_UNRECEIVED'
          91  COMPARE_OP            2  '=='
          94  POP_JUMP_IF_FALSE    61  'to 61'

 213      97  LOAD_GLOBAL           8  'True'
         100  RETURN_END_IF    
       101_0  COME_FROM                '94'
         101  JUMP_BACK            61  'to 61'
         104  POP_BLOCK        

 216     105  LOAD_GLOBAL           9  'False'
         108  RETURN_VALUE     
       109_0  COME_FROM                '54'

Parse error at or near `CALL_FUNCTION_258' instruction at offset 15

    @staticmethod
    def show_tab_rp(activity_type, *args):
        if not ActivityLoginRebate.show_bought_rp(activity_type):
            if ActivityLoginRebate.show_cash_rp:
                return True
        if ActivityLoginRebate.show_task_rp(activity_type):
            return True
        return False
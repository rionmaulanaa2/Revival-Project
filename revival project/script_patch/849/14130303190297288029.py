# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGenericSkinDiscount.py
from __future__ import absolute_import
import six
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils, jump_to_ui_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils.mall_utils import is_steam_pay

class ActivityGenericSkinDiscount(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGenericSkinDiscount, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.activity_conf = conf
        ui_data = conf.get('cUiData', {})
        self.task_id = conf.get('cTask', '')
        self.children_task_list = task_utils.get_children_task(self.task_id)
        self._timer = 0
        self._timer_cb = {}
        if not is_steam_pay() and not G_IS_NA_USER:
            self.goods_id = ui_data.get('goods_id', '') if 1 else ui_data.get('goods_id_steam', '')
            self.goods_info = None
            self.goods_list_name = ui_data.get('goods_list_name', '')
            return self.goods_list_name or None
        else:
            self.goods_level_icon_path = ui_data.get('goods_level_icon_path', '')
            self.is_pc_global_pay = mall_utils.is_pc_global_pay()
            if global_data.lobby_mall_data and global_data.player:
                self.goods_info = global_data.lobby_mall_data.get_activity_sale_info(self.goods_list_name)
                if self.goods_info:
                    key = self.goods_info['goodsid']
                    goods_id = global_data.player.get_goods_info(key).get('cShopGoodsId')
                    if goods_id:
                        if global_data.is_inner_server and goods_id != self.goods_id:
                            global_data.game_mgr.show_tip('\xe6\xad\xa4\xe6\xb4\xbb\xe5\x8a\xa8goods_id ({}) \xe4\xb8\x8e\xe5\x95\x86\xe5\x93\x81\xe9\x85\x8d\xe7\xbd\xaeid ({}) \xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4, \xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5!'.format(self.goods_id, goods_id))
                        self.goods_id = goods_id
            self.gold_receive_list = {0: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3.png',1: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_1.png',
               2: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_1.png',
               3: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_2.png',
               4: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_2.png',
               5: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_2.png',
               6: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_3.png',
               7: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_3.png',
               8: 'gui/ui_res_2/txt_pic/text_pic_en/activity_202211/skin_discount/txt_skin_discount3_3.png'
               }
            return

    def on_init_panel(self):
        if not self.is_unlock_rebate():
            self.register_timer()
        self.update_widget()
        self.init_btn_goto()
        self.init_describe()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_widget_2,
           'task_prog_changed': self.update_widget_2,
           'buy_good_success': self.update_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def refresh_time(self):
        lab_time = self.panel.nd_content.bar_time.lab_countdown
        left_time = activity_utils.get_left_time(self._activity_type)
        if left_time > 0:
            if left_time > tutil.ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(tutil.get_readable_time(close_left_time))
        if left_time < tutil.ONE_DAY_SECONDS:
            lab_time.SetColor(16776557)
        else:
            lab_time.SetColor(16777215)

    def init_time_widget(self):
        player = global_data.player
        if not player:
            return
        else:
            if self.is_unlock_rebate():
                self.unregister_timer()
                left_count = self.get_left_count()
                today_discount_get = self.if_get_today_discount()
                task_count = len(self.children_task_list) - 1
                if today_discount_get:
                    cur_show = max(task_count - 1 - left_count, 0)
                else:
                    cur_show = task_count - left_count
                print (
                 '????????????????????', task_count, cur_show, left_count)
                today_gold_img_path = self.gold_receive_list.get(cur_show, None)
                if today_gold_img_path:
                    self.panel.nd_content.txt_rebate.SetDisplayFrameByPath('', today_gold_img_path)
                self.set_left_count()
            else:
                self._timer_cb[0] = lambda : self.refresh_time()
                self.refresh_time()
            return

    def init_describe(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

    def init_btn_get(self):
        self.panel.nd_content.lab_price.setVisible(not self.is_unlock_rebate())
        if self.is_unlock_rebate():
            self.init_btn_rebate()
        else:
            self.init_btn_buy()

        @self.panel.nd_content.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if self.is_unlock_rebate():
                self.on_click_btn_rebate()
            else:
                self.on_click_btn_buy()

    def init_btn_buy(self):
        btn_buy = self.panel.nd_content.btn_buy
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

    def init_btn_rebate(self):
        today_discount_get = self.if_get_today_discount()
        if today_discount_get:
            can_receive = False
        else:
            can_receive = True
        if self.get_left_count() <= 0:
            can_receive = False
        btn_rebate = self.panel.nd_content.btn_buy
        btn_rebate.SetEnable(can_receive)
        if can_receive:
            btn_rebate.SetText(604030)
        else:
            btn_rebate.SetText(604029)

    def init_btn_goto(self):
        self.panel.nd_content.bar_name.lab_name.SetString(mall_utils.get_goods_name(self.goods_id))
        self.panel.nd_content.bar_name.temp_level.bar_level.SetDisplayFrameByPath('', self.goods_level_icon_path)

        @self.panel.nd_content.btn_search.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_goto()

    def on_click_btn_buy(self, *args):
        if self.is_pc_global_pay:
            jump_to_ui_utils.jump_to_web_charge()
        elif self.goods_info:
            global_data.player and global_data.player.pay_order(self.goods_info['goodsid'])

    def on_click_btn_rebate(self, *args):
        player = global_data.player
        if not player:
            return
        player.call_server_method('attend_activity', (self._activity_type,))
        self.panel.nd_content.btn_buy.SetEnable(False)
        self.panel.nd_content.btn_buy.SetText(604029)

    def on_click_btn_goto(self, *args):
        jump_to_ui_utils.jump_to_display_detail_by_goods_id(self.goods_id, {'role_info_ui': True})

    def is_unlock_rebate(self):
        player = global_data.player
        if not player:
            return False
        bought_num = player.buy_num_all_dict.get(self.goods_id, 0)
        return bought_num > 0

    def get_left_count(self, *args):
        player = global_data.player
        left_count = 0
        for task_id in self.children_task_list:
            reward_status = player.get_task_reward_status(task_id)
            if reward_status != ITEM_RECEIVED:
                left_count += 1

        return left_count

    def set_left_count(self, *args):
        self.unregister_timer()
        lab_time = self.panel.nd_content.bar_time.lab_countdown
        left_count = self.get_left_count()
        lab_time.SetString(get_text_by_id(609712).format(left_count))

    def update_widget(self, *args):
        is_unlock = self.is_unlock_rebate()
        self.panel.txt_discount.setVisible(not is_unlock)
        self.panel.txt_rebate.setVisible(is_unlock)
        self.init_time_widget()
        self.init_btn_get()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_widget_2(self, *args):
        self.init_btn_get()
        self.set_left_count()
        global_data.emgr.refresh_activity_redpoint.emit()

    def if_get_today_discount(self, *args):
        day_no = tutil.get_rela_day_no(rt=tutil.CYCLE_DATA_REFRESH_TYPE_2)
        last_chid_task_id = self.children_task_list[-1]
        last_day_dict = global_data.player.get_task_content(last_chid_task_id, 'last_day_dict', {})
        last_day = last_day_dict.get(self._activity_type, 0)
        if last_day >= day_no:
            return True
        else:
            return False

    @staticmethod
    def show_bought_rp--- This code section failed: ---

 289       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_activity_config'
           9  LOAD_CONST            2  'default'
          12  BUILD_MAP_0           0 
          15  CALL_FUNCTION_258   258 
          18  STORE_FAST            1  'conf'

 290      21  LOAD_FAST             1  'conf'
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            3  'cUiData'
          30  BUILD_MAP_0           0 
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'ui_data'

 291      39  LOAD_GLOBAL           2  'is_steam_pay'
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

 293      92  LOAD_GLOBAL           4  'global_data'
          95  LOAD_ATTR             5  'player'
          98  STORE_FAST            4  'player'

 294     101  LOAD_FAST             4  'player'
         104  POP_JUMP_IF_TRUE    111  'to 111'

 295     107  LOAD_GLOBAL           6  'False'
         110  RETURN_END_IF    
       111_0  COME_FROM                '104'

 296     111  LOAD_FAST             4  'player'
         114  LOAD_ATTR             7  'buy_num_all_dict'
         117  LOAD_ATTR             1  'get'
         120  LOAD_FAST             3  'goods_id'
         123  LOAD_CONST            7  ''
         126  CALL_FUNCTION_2       2 
         129  STORE_FAST            5  'bought_num'

 297     132  LOAD_FAST             5  'bought_num'
         135  LOAD_CONST            7  ''
         138  COMPARE_OP            4  '>'
         141  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_258' instruction at offset 15

    @staticmethod
    def show_task_rp--- This code section failed: ---

 301       0  LOAD_GLOBAL           0  'confmgr'
           3  LOAD_ATTR             1  'get'
           6  LOAD_CONST            1  'c_activity_config'
           9  LOAD_CONST            2  'default'
          12  BUILD_MAP_0           0 
          15  CALL_FUNCTION_258   258 
          18  STORE_FAST            1  'conf'

 302      21  LOAD_FAST             1  'conf'
          24  LOAD_ATTR             1  'get'
          27  LOAD_CONST            3  'cTask'
          30  LOAD_CONST            4  ''
          33  CALL_FUNCTION_2       2 
          36  STORE_FAST            2  'task_id'

 304      39  LOAD_GLOBAL           2  'task_utils'
          42  LOAD_ATTR             3  'get_children_task'
          45  LOAD_FAST             2  'task_id'
          48  CALL_FUNCTION_1       1 
          51  STORE_FAST            3  'children_task_list'

 305      54  LOAD_GLOBAL           4  'tutil'
          57  LOAD_ATTR             5  'get_rela_day_no'
          60  LOAD_CONST            5  'rt'
          63  LOAD_GLOBAL           4  'tutil'
          66  LOAD_ATTR             6  'CYCLE_DATA_REFRESH_TYPE_2'
          69  CALL_FUNCTION_256   256 
          72  STORE_FAST            4  'day_no'

 306      75  LOAD_FAST             3  'children_task_list'
          78  LOAD_CONST            6  -1
          81  BINARY_SUBSCR    
          82  STORE_FAST            5  'last_chid_task_id'

 307      85  LOAD_GLOBAL           7  'global_data'
          88  LOAD_ATTR             8  'player'
          91  LOAD_ATTR             9  'get_task_content'
          94  LOAD_FAST             5  'last_chid_task_id'
          97  LOAD_CONST            7  'last_day_dict'
         100  BUILD_MAP_0           0 
         103  CALL_FUNCTION_3       3 
         106  STORE_FAST            6  'last_day_dict'

 309     109  LOAD_FAST             1  'conf'
         112  LOAD_ATTR             1  'get'
         115  LOAD_CONST            3  'cTask'
         118  LOAD_CONST            4  ''
         121  CALL_FUNCTION_2       2 
         124  STORE_FAST            2  'task_id'

 310     127  LOAD_FAST             6  'last_day_dict'
         130  LOAD_ATTR             1  'get'
         133  LOAD_ATTR             8  'player'
         136  CALL_FUNCTION_2       2 
         139  STORE_FAST            7  'last_day'

 312     142  LOAD_CONST            8  ''
         145  STORE_FAST            8  'left_count'

 313     148  SETUP_LOOP           57  'to 208'
         151  LOAD_FAST             3  'children_task_list'
         154  GET_ITER         
         155  FOR_ITER             49  'to 207'
         158  STORE_FAST            2  'task_id'

 314     161  LOAD_GLOBAL           7  'global_data'
         164  LOAD_ATTR             8  'player'
         167  LOAD_ATTR            10  'get_task_reward_status'
         170  LOAD_FAST             2  'task_id'
         173  CALL_FUNCTION_1       1 
         176  STORE_FAST            9  'reward_status'

 315     179  LOAD_FAST             9  'reward_status'
         182  LOAD_GLOBAL          11  'ITEM_RECEIVED'
         185  COMPARE_OP            3  '!='
         188  POP_JUMP_IF_FALSE   155  'to 155'

 316     191  LOAD_FAST             8  'left_count'
         194  LOAD_CONST            9  1
         197  INPLACE_ADD      
         198  STORE_FAST            8  'left_count'
         201  JUMP_BACK           155  'to 155'
         204  JUMP_BACK           155  'to 155'
         207  POP_BLOCK        
       208_0  COME_FROM                '148'

 317     208  LOAD_FAST             7  'last_day'
         211  LOAD_FAST             4  'day_no'
         214  COMPARE_OP            0  '<'
         217  POP_JUMP_IF_FALSE   230  'to 230'
         220  LOAD_FAST             8  'left_count'
       223_0  COME_FROM                '217'
         223  POP_JUMP_IF_FALSE   230  'to 230'

 319     226  LOAD_GLOBAL          12  'True'
         229  RETURN_END_IF    
       230_0  COME_FROM                '223'

 322     230  LOAD_GLOBAL          13  'False'
         233  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 15

    @staticmethod
    def show_tab_rp(activity_type):
        if not ActivityGenericSkinDiscount.show_bought_rp(activity_type):
            return False
        if ActivityGenericSkinDiscount.show_task_rp(activity_type):
            return True
        return False
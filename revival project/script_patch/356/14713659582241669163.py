# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityExchange.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import mall_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_DAY_SECONDS, ONE_HOUR_SECONS
from cocosui import cc, ccui, ccs

class ActivityExchange(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityExchange, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}
        self._children_tasks = []

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'buy_good_success': self.buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

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

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        self.panel.lab_tdescribe.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_describe

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn_describe.GetPosition()
            wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]

        def callback--- This code section failed: ---

  96       0  LOAD_GLOBAL           0  'task_utils'
           3  LOAD_ATTR             1  'get_raw_left_open_time'
           6  LOAD_DEREF            0  'parent_task'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'left_time'

  97      15  STORE_FAST            1  'close_left_time'
          18  COMPARE_OP            4  '>'
          21  POP_JUMP_IF_FALSE   122  'to 122'

  98      24  LOAD_FAST             0  'left_time'
          27  LOAD_GLOBAL           2  'ONE_HOUR_SECONS'
          30  COMPARE_OP            4  '>'
          33  POP_JUMP_IF_FALSE    79  'to 79'

  99      36  LOAD_DEREF            1  'self'
          39  LOAD_ATTR             3  'panel'
          42  LOAD_ATTR             4  'lab_time'
          45  LOAD_ATTR             5  'SetString'
          48  LOAD_GLOBAL           6  'get_text_by_id'
          51  LOAD_CONST            2  609203
          54  CALL_FUNCTION_1       1 
          57  LOAD_ATTR             7  'format'
          60  LOAD_GLOBAL           8  'get_readable_time_day_hour_minitue'
          63  LOAD_FAST             0  'left_time'
          66  CALL_FUNCTION_1       1 
          69  CALL_FUNCTION_1       1 
          72  CALL_FUNCTION_1       1 
          75  POP_TOP          
          76  JUMP_ABSOLUTE       193  'to 193'

 101      79  LOAD_DEREF            1  'self'
          82  LOAD_ATTR             3  'panel'
          85  LOAD_ATTR             4  'lab_time'
          88  LOAD_ATTR             5  'SetString'
          91  LOAD_GLOBAL           6  'get_text_by_id'
          94  LOAD_CONST            2  609203
          97  CALL_FUNCTION_1       1 
         100  LOAD_ATTR             7  'format'
         103  LOAD_GLOBAL           9  'get_readable_time'
         106  LOAD_FAST             0  'left_time'
         109  CALL_FUNCTION_1       1 
         112  CALL_FUNCTION_1       1 
         115  CALL_FUNCTION_1       1 
         118  POP_TOP          
         119  JUMP_FORWARD         71  'to 193'

 103     122  LOAD_GLOBAL          10  'ONE_DAY_SECONDS'
         125  LOAD_FAST             0  'left_time'
         128  BINARY_ADD       
         129  STORE_FAST            1  'close_left_time'

 104     132  LOAD_FAST             1  'close_left_time'
         135  LOAD_CONST            1  ''
         138  COMPARE_OP            1  '<='
         141  POP_JUMP_IF_FALSE   153  'to 153'
         144  LOAD_CONST            1  ''
         147  STORE_FAST            1  'close_left_time'
         150  JUMP_FORWARD          0  'to 153'
       153_0  COME_FROM                '150'

 105     153  LOAD_DEREF            1  'self'
         156  LOAD_ATTR             3  'panel'
         159  LOAD_ATTR             4  'lab_time'
         162  LOAD_ATTR             5  'SetString'
         165  LOAD_GLOBAL           6  'get_text_by_id'
         168  LOAD_CONST            3  607130
         171  CALL_FUNCTION_1       1 
         174  LOAD_ATTR             7  'format'
         177  LOAD_GLOBAL           9  'get_readable_time'
         180  LOAD_FAST             1  'close_left_time'
         183  CALL_FUNCTION_1       1 
         186  CALL_FUNCTION_1       1 
         189  CALL_FUNCTION_1       1 
         192  POP_TOP          
       193_0  COME_FROM                '119'

Parse error at or near `STORE_FAST' instruction at offset 15

        self._timer_cb[0] = callback
        callback()
        self.show_list()

    def buy_good_success(self):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            extra_params = task_utils.get_task_arg(task_id_a)
            goods_id_a = str(extra_params.get('goodsid', ''))
            extra_params = task_utils.get_task_arg(task_id_b)
            goods_id_b = str(extra_params.get('goodsid', ''))
            prices = mall_utils.get_mall_item_price(goods_id_a, pick_list='item')
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            cost_item_num_a = price_info.get('real_price')
            cost_item_amount_a = global_data.player.get_item_num_by_no(int(cost_item_no))
            prices = mall_utils.get_mall_item_price(goods_id_b, pick_list='item')
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            cost_item_num_b = price_info.get('real_price')
            cost_item_amount_b = global_data.player.get_item_num_by_no(int(cost_item_no))
            left_num_a, max_num = (1, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id_a)
            if num_info:
                left_num_a, max_num = num_info
            left_num_b, max_num = (1, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id_b)
            if num_info:
                left_num_b, max_num = num_info
            enable_a = left_num_a > 0 and cost_item_amount_a >= cost_item_num_a
            enable_b = left_num_b > 0 and cost_item_amount_b >= cost_item_num_b
            if enable_a != enable_b:
                if enable_a:
                    return -1
                if enable_b:
                    return 1
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.act_list
        sub_act_list.SetTemplate(self.get_task_list_template())
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            extra_params = task_utils.get_task_arg(task_id)
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                continue
            prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
            if not prices:
                continue
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            template_utils.init_tempate_mall_i_item(item_widget.temp_fragment, cost_item_no, show_tips=True)
            template_utils.init_tempate_mall_i_item(item_widget.temp_reward, target_item_no, target_item_num, show_tips=True)
            do_remind = [
             global_data.player.has_exchange_reminder(goods_id)]

            @item_widget.btn_tick.unique_callback()
            def OnClick(btn, touch, do_remind=do_remind, goods_id=goods_id):
                do_remind[0] = not do_remind[0]
                btn.SetSelect(do_remind[0])
                global_data.player.add_exchange_reminder(goods_id, do_remind[0])

            item_widget.btn_tick.SetSelect(do_remind[0])
            if ui_data.get('lab_tips_color'):
                color = int(ui_data.get('lab_tips_color'), 16)
                item_widget.lab_tips.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)

        self.refresh_list()

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                continue
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                continue
            prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
            if not prices:
                continue
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            cost_item_num = price_info.get('real_price')
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                limit_left_num = left_num
                item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
            else:
                item_widget.lab_num.SetString('')
            cost_item_amount = global_data.player.get_item_num_by_no(int(cost_item_no))
            if cost_item_amount >= cost_item_num:
                cost_str = '#DB{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            else:
                cost_str = '#SR{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            item_widget.temp_fragment.lab_quantity.setVisible(True)
            item_widget.temp_fragment.lab_quantity.SetString(cost_str)
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(btn=btn, left_num=left_num, max_num=max_num):
                if limit_left_num <= 0:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                    return
                btn.setVisible(True)
                item_widget.nd_get.setVisible(False)
                enable = left_num > 0 and mall_utils.check_item_money(cost_item_no, cost_item_num, pay_tip=False)
                btn.SetEnable(enable)

            @btn.unique_callback()
            def OnClick(btn, touch, goods_id=goods_id, goods_payment=goods_payment, left_num=left_num):
                from logic.comsys.mall_ui import BuyConfirmUIInterface
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                if left_num > 1:
                    BuyConfirmUIInterface.groceries_buy_confirmUI(goods_id)
                else:
                    global_data.player.buy_goods(goods_id, 1, goods_payment)

            check_btn()

    def get_task_list_template(self):
        return 'activity/i_task_exchange'
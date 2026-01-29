# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmExchange.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
import cc

class ActivityGranbelmExchange(ActivityExchange):

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmExchange, self).__init__(dlg, activity_type)

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_info.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        else:

            @self.panel.btn_details.unique_callback()
            def OnClick(btn, touch):
                jump_to_display_detail_by_item_no(208200216)

            self._timer_cb[0] = lambda : self.refresh_time(None)
            self.refresh_time(None)
            self.show_list()
            return

    def init_parameters(self):
        super(ActivityGranbelmExchange, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def get_task_list_template(self):
        return 'activity/i_task_exchange_new_cell'

    def set_show(self, show, is_init=False):
        super(ActivityGranbelmExchange, self).set_show(show, is_init)
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(1.0),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget and item_widget.lab_name.setVisible(False)
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
            exchange_lv = extra_params.get('exchange_lv', None)
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
            def OnClick(btn, touch, goods_id=goods_id, goods_payment=goods_payment, left_num=left_num, ex_lv=exchange_lv):
                from logic.comsys.mall_ui import BuyConfirmUIInterface
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                else:
                    if ex_lv is not None and global_data.player.get_lv() < ex_lv:
                        item_name = mall_utils.get_goods_name(goods_id)
                        global_data.game_mgr.show_tip(get_text_by_id(608422).format(item=item_name))
                        return
                    if left_num > 1:
                        BuyConfirmUIInterface.groceries_buy_confirmUI(goods_id)
                    else:
                        global_data.player.buy_goods(goods_id, 1, goods_payment)
                    return

            check_btn()

        return

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list
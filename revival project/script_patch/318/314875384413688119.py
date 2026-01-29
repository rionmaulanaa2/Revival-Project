# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncExchangeListWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from functools import cmp_to_key
from .Widget import Widget
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils import mall_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import template_utils, item_utils, task_utils, activity_utils
from logic.gutils.client_utils import post_ui_method
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.template_utils import init_tempate_mall_i_item

class AsyncExchangeListWidget(Widget):

    def __init__(self, panel, activity_type):
        super(AsyncExchangeListWidget, self).__init__(panel, activity_type)
        self._timer = 0

    def on_init_panel(self):
        super(AsyncExchangeListWidget, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        parent_task_id = conf.get('cUiData', {}).get('exchange_task_id', None)
        self._task_list = task_utils.get_children_task(parent_task_id)
        self.__process_event(True)
        if self.panel.act_list.IsAsync():
            self.panel.act_list.BindMethod('OnCreateItem', self._on_create_item(self._create_task_item, conf.get('cUiData', {})))
        self.refresh_panel()
        return

    def on_finalize_panel(self):
        self.__process_event(False)
        super(AsyncExchangeListWidget, self).on_finalize_panel()

    def refresh_panel(self):
        super(AsyncExchangeListWidget, self).refresh_panel()
        if not global_data.player:
            return
        self._refresh_task_list()
        self.__refresh_task_widget()

    def __process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self._on_update_task,
           'receive_task_reward_succ_event': self._on_update_task,
           'receive_task_prog_reward_succ_event': self._on_update_task,
           'buy_good_success': self._on_update_task
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    @post_ui_method
    def _on_update_task(self, *args):
        if global_data.player:
            global_data.player.read_activity_list(self._activity_type)
            self.refresh_panel()

    def _refresh_task_list(self):
        task_list = self._task_list
        if task_list:
            task_list = self._reorder_task_list(task_list)
        self._task_list = task_list

    def _reorder_task_list(self, tasks):

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
            enable_a = left_num_a > 0
            enable_b = left_num_b > 0
            if enable_a != enable_b:
                if enable_a:
                    return -1
                if enable_b:
                    return 1
            if cost_item_num_b != cost_item_num_a:
                return six_ex.compare(cost_item_num_b, cost_item_num_a)
            can_exchange_a = cost_item_amount_a >= cost_item_num_a
            can_exchange_b = cost_item_amount_b >= cost_item_num_b
            if can_exchange_a != can_exchange_b:
                if can_exchange_a:
                    return -1
                if can_exchange_b:
                    return 1
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def __refresh_task_widget(self):
        if self.panel.act_list.IsAsync():
            self.panel.act_list.scroll_reload(len(self._task_list))
            for idx in range(len(self._task_list)):
                ui_item = self.panel.act_list.GetItem(idx)
                if ui_item:
                    self._refresh_task_item(ui_item, idx)

        elif not self.panel.act_list.GetAllItem():
            self.panel.act_list.SetInitCount(len(self._task_list))
            conf = confmgr.get('c_activity_config', self._activity_type)
            for idx in range(len(self._task_list)):
                ui_item = self.panel.act_list.GetItem(idx)
                if ui_item:
                    self._create_task_item(ui_item, idx, conf.get('cUiData', {}))

        else:
            for idx in range(len(self._task_list)):
                ui_item = self.panel.act_list.GetItem(idx)
                if ui_item:
                    self._refresh_task_item(ui_item, idx)

    def _on_create_item(self, inst_cb, ui_data):

        def _on_create_item(list_reward, index, widget_item):
            inst_cb(widget_item, index, ui_data)

        return _on_create_item

    def _create_task_item(self, ui_item, index, ui_data):
        if not global_data.player:
            return
        item_widget = ui_item.temp_common
        task_id = self._task_list[index]
        extra_params = task_utils.get_task_arg(task_id)
        goods_id = str(extra_params.get('goodsid', ''))
        if not goods_id:
            return
        prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
        if not prices:
            return
        price_info = prices[0]
        goods_payment = price_info.get('goods_payment')
        cost_item_no = mall_utils.get_payment_item_no(goods_payment)
        target_item_no = mall_utils.get_goods_item_no(goods_id)
        target_item_num = mall_utils.get_goods_num(goods_id)
        template_utils.init_tempate_mall_i_simple_item(item_widget.nd_1.temp_fragment, cost_item_no, show_tips=True)
        template_utils.init_tempate_mall_i_simple_item(item_widget.nd_1.temp_reward, target_item_no, target_item_num, show_tips=True)
        do_remind = [
         global_data.player.has_exchange_reminder(goods_id)]

        @item_widget.btn_tick.unique_callback()
        def OnClick(btn, touch, do_remind=do_remind, goods_id=goods_id):
            do_remind[0] = not do_remind[0]
            btn.SetSelect(do_remind[0])
            global_data.player.add_exchange_reminder(goods_id, do_remind[0])

        item_widget.btn_tick.SetSelect(do_remind[0])
        self._refresh_task_item(ui_item, index)

    def _refresh_task_item(self, ui_item, index):
        item_widget = ui_item.temp_common
        task_id = self._task_list[index]
        extra_params = task_utils.get_task_arg(task_id)
        if not extra_params:
            return
        else:
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                return
            prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
            if not prices:
                return
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
            item_widget.nd_1.temp_fragment.lab_quantity.setVisible(True)
            item_widget.nd_1.temp_fragment.lab_quantity.SetString(cost_str)
            exchange_lv = extra_params.get('exchange_lv', None)
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(btn=btn, left_num=left_num, max_num=max_num):
                if limit_left_num <= 0:
                    update_task_list_btn(item_widget.nd_task.temp_btn_get, BTN_ST_RECEIVED)
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
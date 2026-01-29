# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKnotCollectAndExchange.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
from cocosui import cc
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
KNOT_ITEM_NO = 50600023
ITEM_ID_LST = [208200125, 20601412, 20602414, 20606409, 50101125, 30100048, 50101126]

class ActivityKnotCollectAndExchange(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKnotCollectAndExchange, self).__init__(dlg, activity_type)
        self._collect_lst_inited = False
        self._exchange_lst_inited = False
        self._collect_task_id = '1411349'
        self._exchange_task_id = '1411356'
        self._collect_children_tasks = []
        self._exchange_children_tasks = []
        self.init_parameters()
        self.init_event()
        self._init_ui_event()
        self.register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}
        self._has_play_appear = False
        conf = confmgr.get('c_activity_config', self._activity_type)
        ui_data = conf.get('cUiData', {})
        self._collect_task_id = ui_data.get('collect_task_id', None)
        self._exchange_task_id = ui_data.get('exchange_task_id', None)
        self.panel.temp_collect.btn_common.SetText(601123)
        self.panel.temp_exchange.btn_common.SetText(601122)
        return

    def init_event(self):
        self.process_event(True)

    def _select_tab_btn(self):
        pass

    def process_event(self, is_bind):
        e_mgr = global_data.emgr
        e_conf = {'receive_task_reward_succ_event': self._on_update_reward,
           'buy_good_success': self._buy_good_success
           }
        if is_bind:
            e_mgr.bind_events(e_conf)
        else:
            e_mgr.unbind_events(e_conf)

    def _buy_good_success(self):
        knot_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(KNOT_ITEM_NO)
        self.panel.lab_num.SetString(str(knot_num))
        global_data.player.read_activity_list(self._activity_type)
        self._init_exchange_list()

    def refresh_panel(self):
        pass

    def set_show(self, show, is_init=False):
        super(ActivityKnotCollectAndExchange, self).set_show(show, is_init)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def _on_update_reward(self, task_id):
        knot_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(KNOT_ITEM_NO)
        self.panel.lab_num.SetString(str(knot_num))
        global_data.player.read_activity_list(self._activity_type)
        self._init_collect_list()
        self._update_btn_get_state()

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
        from logic.gutils.item_utils import get_lobby_item_name
        for idx in range(len(ITEM_ID_LST)):
            name_node = getattr(self.panel, 'lab_name_%s' % idx)
            name_node.SetString(get_lobby_item_name(ITEM_ID_LST[idx], need_part_name=False))
            name_btn = getattr(self.panel, 'btn_click_%s' % idx)

            @name_btn.unique_callback()
            def OnClick(btn, touch, item_id=ITEM_ID_LST[idx]):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
                return

        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(601216))

        if self._collect_task_id and not self._is_invalid(self._collect_task_id):
            self.panel.temp_collect.btn_common.OnClick(None)
        elif self._exchange_task_id and not self._is_invalid(self._exchange_task_id):
            self.panel.temp_collect.btn_common.SetEnable(False)
            self.panel.panel.temp_exchange.btn_common.OnClick(None)
        else:
            self.panel.temp_collect.btn_common.SetEnable(False)
            self.panel.temp_exchange.btn_common.SetEnable(False)
        self._timer_cb[0] = lambda : self._refresh_time()
        self._refresh_time()
        if self.panel.HasAnimation('show') and not self._has_play_appear:
            self._has_play_appear = True
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')
        knot_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(KNOT_ITEM_NO)
        self.panel.lab_num.SetString(str(knot_num))
        self._update_btn_get_state()
        return

    def _reorder_collect_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def _reorder_exchange_task_list(self, tasks):

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

    def _refresh_time(self):
        if not self.panel or not self.panel.lab_time:
            return
        if self.panel.list_collect.isVisible():
            task_id = self._collect_task_id
        else:
            task_id = self._exchange_task_id
        left_time = task_utils.get_raw_left_open_time(task_id)
        if left_time <= 0:
            day_txt = get_text_by_id(607911)
        else:
            is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time)
            if not is_ending:
                day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
            else:
                day_txt = get_text_by_id(left_text)
        self.panel.lab_time.SetString(str(day_txt))

    def _init_collect_list(self):
        if not self._collect_task_id or self._is_invalid(self._collect_task_id):
            self.panel.list_collect.setVisible(False)
            return
        self._collect_lst_inited = True
        children_tasks = task_utils.get_children_task(self._collect_task_id)
        self._collect_children_tasks = self._reorder_collect_task_list(children_tasks)

        def on_create_callback(lv, item_idx, item_widget):
            task_id = self._collect_children_tasks[item_idx]
            reward_id = task_utils.get_task_reward(task_id)
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times > 1:
                item_widget.lab_num.SetString('({0}/{1})'.format(cur_times, total_times))
            else:
                item_widget.lab_num.SetString('')
            btn_get = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)
            has_rewarded = global_data.player.has_receive_reward(task_id)
            if has_rewarded:
                item_widget.nd_get.setVisible(True)
                btn_get.setVisible(False)
            elif cur_times < total_times:
                btn_get.setVisible(True)
                jump_conf = task_utils.get_jump_conf(task_id)
                text_id = jump_conf.get('unreach_text', '')
                if text_id:
                    btn_get.SetText(text_id)
                    btn_get.SetEnable(True)
                else:
                    btn_get.SetEnable(False)
            else:
                btn_get.setVisible(True)
                btn_get.SetEnable(True)

            @btn_get.unique_callback()
            def OnClick(btn, touch, cb_task_id=task_id):
                if self._is_invalid(self._collect_task_id, show_tip=True):
                    return
                _total_times = task_utils.get_total_prog(cb_task_id)
                _cur_times = global_data.player.get_task_prog(cb_task_id)
                jump_conf_info = task_utils.get_jump_conf(cb_task_id)
                if _cur_times < _total_times and jump_conf_info.get('unreach_text', ''):
                    from logic.gutils.item_utils import exec_jump_to_ui_info
                    exec_jump_to_ui_info(jump_conf_info)
                else:
                    global_data.player.receive_task_reward(cb_task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

        sub_act_list = self.panel.list_collect
        sub_act_list.DeleteAllSubItem()
        sub_act_list.BindMethod('OnCreateItem', on_create_callback)
        sub_act_list.SetInitCount(len(self._collect_children_tasks))

    def _init_exchange_list(self):
        if not self._exchange_task_id or self._is_invalid(self._exchange_task_id):
            self.panel.list_collect.setVisible(False)
            return
        self._exchange_lst_inited = True
        children_tasks = task_utils.get_children_task(self._exchange_task_id)
        self._exchange_lst_inited = self._reorder_exchange_task_list(children_tasks)

        def on_create_callback(lv, item_idx, item_widget):
            task_id = self._exchange_lst_inited[item_idx]
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                item_widget.setVisible(False)
                return
            goods_id = str(extra_params.get('goodsid', ''))
            if not goods_id:
                item_widget.setVisible(False)
                return
            prices = mall_utils.get_mall_item_price(goods_id, pick_list='item')
            if not prices:
                item_widget.setVisible(False)
                return
            price_info = prices[0]
            goods_payment = price_info.get('goods_payment')
            cost_item_no = mall_utils.get_payment_item_no(goods_payment)
            target_item_no = mall_utils.get_goods_item_no(goods_id)
            target_item_num = mall_utils.get_goods_num(goods_id)
            template_utils.init_tempate_mall_i_item(item_widget.temp_fragment, cost_item_no, show_tips=True)
            template_utils.init_tempate_mall_i_item(item_widget.temp_reward, target_item_no, target_item_num, show_tips=True)

            @item_widget.btn_tick.unique_callback()
            def OnClick(cb_btn, touch, cb_goods_id=goods_id):
                do_remind = global_data.player.has_exchange_reminder(cb_goods_id)
                cb_btn.SetSelect(not do_remind)
                global_data.player.add_exchange_reminder(goods_id, not do_remind)

            item_widget.btn_tick.SetSelect(global_data.player.has_exchange_reminder(goods_id))
            limit_left_num = 1
            left_num, max_num = (0, 0)
            _, _, num_info = mall_utils.buy_num_limit_by_all(goods_id)
            if num_info:
                left_num, max_num = num_info
                limit_left_num = left_num
                if left_num > 0:
                    item_widget.lab_num.SetString(get_text_by_id(607018).format(left_num, max_num))
                else:
                    item_widget.lab_num.SetString('')
            else:
                left_num = 9999
                item_widget.lab_num.SetString('')
            cost_item_num = price_info.get('real_price')
            cost_item_amount = global_data.player.get_item_num_by_no(int(cost_item_no))
            if cost_item_amount >= cost_item_num:
                cost_str = '#DB{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            else:
                cost_str = '#SR{0}#n/{1}'.format(cost_item_amount, cost_item_num)
            item_widget.temp_fragment.lab_quantity.setVisible(True)
            item_widget.temp_fragment.lab_quantity.SetString(cost_str)
            btn_get = item_widget.temp_btn_get.btn_common
            if limit_left_num <= 0:
                item_widget.nd_get.setVisible(True)
                btn_get.setVisible(False)
            else:
                btn_get.setVisible(True)
                item_widget.nd_get.setVisible(False)
                enable = left_num > 0 and mall_utils.check_item_money(cost_item_no, cost_item_num, pay_tip=False)
                btn_get.SetEnable(enable)

            @btn_get.unique_callback()
            def OnClick(cb_btn, touch, cb_goods_id=goods_id, cb_goods_payment=goods_payment, cb_left_num=left_num):
                from logic.comsys.mall_ui import BuyConfirmUIInterface
                if self._is_invalid(self._exchange_task_id, show_tip=True):
                    return
                if cb_left_num > 1:
                    BuyConfirmUIInterface.groceries_buy_confirmUI(cb_goods_id)
                else:
                    global_data.player.buy_goods(goods_id, 1, cb_goods_payment)

        sub_act_list = self.panel.list_exchange
        sub_act_list.DeleteAllSubItem()
        sub_act_list.BindMethod('OnCreateItem', on_create_callback)
        sub_act_list.SetInitCount(len(self._exchange_lst_inited))

    def _is_invalid(self, task_id, show_tip=False):
        is_invalid = False
        if activity_utils.is_activity_finished(self._activity_type):
            is_invalid = True
        if not task_utils.is_task_open(task_id):
            is_invalid = True
        if show_tip and is_invalid:
            global_data.game_mgr.show_tip(607911)
        return is_invalid

    def _update_btn_get_state(self):
        if self._is_invalid(self._collect_task_id, show_tip=True):
            self.panel.btn_get.btn_common.SetEnable(False)
            return
        if global_data.player.has_unreceived_task_reward(self._collect_task_id):
            self.panel.btn_get.btn_common.SetEnable(True)
        else:
            self.panel.btn_get.btn_common.SetEnable(False)

    def _init_ui_event(self):

        @self.panel.temp_exchange.btn_common.unique_callback()
        def OnClick(btn, touch):
            self.panel.nd_exchange.setVisible(True)
            self.panel.nd_collect.setVisible(False)
            self.panel.temp_exchange.btn_common.SetSelect(True)
            self.panel.temp_collect.btn_common.SetSelect(False)
            self.panel.btn_get.setVisible(False)
            self._refresh_time()
            if not self._exchange_lst_inited:
                self._init_exchange_list()

        @self.panel.temp_collect.btn_common.unique_callback()
        def OnClick(btn, touch):
            self.panel.nd_collect.setVisible(True)
            self.panel.nd_exchange.setVisible(False)
            self.panel.temp_exchange.btn_common.SetSelect(False)
            self.panel.temp_collect.btn_common.SetSelect(True)
            self.panel.btn_get.setVisible(True)
            self._refresh_time()
            if not self._collect_lst_inited:
                self._init_collect_list()

        @self.panel.btn_have.btn_common.unique_callback()
        def OnClick(btn, touch):
            from common.platform import is_win32
            if G_IS_NA_PROJECT and is_win32():
                global_data.game_mgr.show_tip(601226)
            else:
                from logic.gutils.jump_to_ui_utils import jump_to_activity
                from logic.gcommon.common_const.activity_const import ACTIVITY_SPRING_GIFT_KNOT
                jump_to_activity(ACTIVITY_SPRING_GIFT_KNOT)

        @self.panel.btn_get.btn_common.unique_callback()
        def OnClick(btn, touch):
            if self._is_invalid(self._collect_task_id, show_tip=True):
                return
            global_data.player.receive_all_task_reward(self._collect_task_id)
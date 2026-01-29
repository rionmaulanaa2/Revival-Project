# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityKizunaTrainExchange.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gutils import activity_utils, template_utils
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_ACTIVITY1, ACTIVITY_KIZUNA_AI_ACTIVITY2
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_RECEIVED
import cc
ITEM_ID_LST = (208200127, 50101226, 50920102, 50102006, 50101002)

class ActivityKizunaTrainExchange(ActivityExchange):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaTrainExchange, self).__init__(dlg, activity_type)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        self.panel.act_list_common.setVisible(False)
        self.panel.act_list.setVisible(True)
        return

    def on_finalize_panel(self):
        super(ActivityKizunaTrainExchange, self).on_finalize_panel()
        self.sub_widget = None
        return

    def init_items(self):
        for idx, item_id in enumerate(ITEM_ID_LST):
            name_node = getattr(self.panel, 'lab_reward_0%s' % (idx + 1))
            name_node.SetString(item_utils.get_lobby_item_name(item_id, need_part_name=False))
            click_node = getattr(self.panel, 'btn_click_0%s' % (idx + 1))

            @click_node.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
                return

        @self.panel.btn_watch.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no(ITEM_ID_LST[0])

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        else:
            self._timer_cb[0] = lambda : self.refresh_time(None)
            self.refresh_time(None)
            self.show_list()
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

            @self.panel.btn_tips.unique_callback()
            def OnClick(btn, touch, *args):
                desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
                from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
                dlg = GameRuleDescUI()
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

            global_data.player.call_server_method('attend_activity', (self._activity_type,))
            return

    def refresh_time(self, parent_task):
        task_id = confmgr.get('c_activity_config', ACTIVITY_KIZUNA_AI_ACTIVITY1, 'cTask', default='')
        exchange_id = confmgr.get('c_activity_config', ACTIVITY_KIZUNA_AI_ACTIVITY2, 'cTask', default='')
        task_left_time = task_utils.get_raw_left_open_time(task_id)
        exchange_left_time = task_utils.get_raw_left_open_time(exchange_id)
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_act_time.SetString(get_text_by_id(609771).format(get_readable_time_day_hour_minitue(task_left_time)))
            else:
                self.panel.lab_act_time.SetString(get_text_by_id(609771).format(get_readable_time(task_left_time)))
        elif exchange_left_time > 0:
            if exchange_left_time > ONE_HOUR_SECONS:
                self.panel.lab_act_time.SetString(get_text_by_id(609772).format(get_readable_time_day_hour_minitue(exchange_left_time)))
            else:
                self.panel.lab_act_time.SetString(get_text_by_id(609772).format(get_readable_time(exchange_left_time)))
        else:
            close_left_time = 0
            self.panel.lab_act_time.SetString(get_readable_time(close_left_time))

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(ActivityKizunaTrainExchange, self).set_show(show, is_init)
        if self.cur_tab_name_id == self.last_tab_name_id:
            if not self.panel.IsPlayingAnimation('loop'):
                show and self.panel.PlayAnimation('loop')
            return
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        if show:
            self.panel.runAction(cc.Sequence.create([
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
            if self.sub_widget and self.sub_widget.panel:
                self.sub_widget.panel.PlayAnimation('show')

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
            enable_a = left_num_a > 0
            enable_b = left_num_b > 0
            if enable_a != enable_b:
                if enable_a:
                    return -1
                if enable_b:
                    return 1
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

    def transfer_panel_out(self):
        return self.panel

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
        sub_act_list.SetInitCount(len(self._children_tasks))
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
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
            template_utils.init_tempate_mall_i_item(item_widget.nd_1.temp_fragment, cost_item_no, show_tips=True)
            template_utils.init_tempate_mall_i_item(item_widget.nd_1.temp_reward, target_item_no, target_item_num, show_tips=True)
            do_remind = [
             global_data.player.has_exchange_reminder(goods_id)]

            @item_widget.btn_tick.unique_callback()
            def OnClick(btn, touch, do_remind=do_remind, goods_id=goods_id):
                do_remind[0] = not do_remind[0]
                btn.SetSelect(do_remind[0])
                global_data.player.add_exchange_reminder(goods_id, do_remind[0])

            item_widget.btn_tick.SetSelect(do_remind[0])

        self.refresh_list()

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
            extra_params = task_utils.get_task_arg(task_id)
            if not extra_params:
                return
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
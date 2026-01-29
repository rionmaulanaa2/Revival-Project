# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncYuanbaoStrikeTaskListWidget.py
from __future__ import absolute_import
from .AsyncTaskListWidget import AsyncTaskListWidget
from logic.gutils.mall_utils import limite_pay, get_goods_item_task_id
from logic.gutils import task_utils, activity_utils, item_utils
from common.cfg import confmgr
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_INACTIVE, ITEM_UNRECEIVED, BTN_ST_CAN_RECEIVE, BTN_ST_OVERDUE
from functools import cmp_to_key
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.cdata import loop_activity_data
from logic.gcommon import time_utility

class AsyncYuanbaoStrikeTaskListWidget(AsyncTaskListWidget):

    def on_init_panel(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._goods_id = str(ui_data.get('goods_id', ''))
        self._free_tasks = ui_data.get('free_tasks', [])
        self._pay_tasks = ui_data.get('pay_tasks', [])
        self._pay_task_id = get_goods_item_task_id(self._goods_id)
        super(AsyncYuanbaoStrikeTaskListWidget, self).on_init_panel()

    def _create_task_item(self, item_widget, index, ui_data):
        if not global_data.player:
            return
        else:
            ui_item = item_widget
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            task_id = self._task_list[index]
            max_prog = cur_prog = global_data.player.get_task_prog(task_id)
            total_prog = task_utils.get_total_prog(task_id)
            status = global_data.player.get_task_reward_status(task_id)
            task_name = task_utils.get_task_name(task_id, None)
            is_prog_task = False
            item_widget.lab_name.SetString(task_name)
            if total_prog > 1:
                item_widget.lab_num.SetString('{0}/{1}'.format(cur_prog, total_prog))
            else:
                item_widget.lab_num.SetString('')
            percent = 1.0 * max_prog / total_prog * 100
            item_widget.prog.SetPercentage(percent)
            btn = item_widget.temp_btn_get.btn_common
            self._update_receive_btn(task_id, status, ui_item)

            @btn.unique_callback()
            def OnClick(btn, touch, _task_id=task_id, _cur_prog=cur_prog, _total_prog=total_prog, _max_prog=max_prog, _is_prog_task=is_prog_task):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                if _cur_prog < _total_prog:
                    jump_conf = task_utils.get_jump_conf(_task_id)
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    if _is_prog_task:
                        global_data.player.receive_task_prog_reward(_task_id, _total_prog)
                    else:
                        global_data.player.receive_task_reward(_task_id)
                    if _max_prog == _total_prog:
                        btn.SetText(80866)
                        btn.SetEnable(False)

            return

    def _update_receive_btn(self, task_id, status, ui_item):
        if task_id in self._free_tasks:
            strike_type = 'free'
        elif task_id in self._pay_tasks:
            strike_type = 'pay'
        else:
            strike_type = ''
        has_rewarded_pay_task = global_data.player.has_receive_reward(self._pay_task_id)
        btn_receive = ui_item.temp_common.nd_task.temp_btn_get
        if loop_activity_data.is_loop_activity(self._activity_type):
            task_open = loop_activity_data.is_loop_task_open(self._activity_type)
        else:
            task_open = task_utils.is_task_open(self._fixed_task_id)
        if has_rewarded_pay_task or not task_open:
            update_task_list_btn(btn_receive, BTN_ST_OVERDUE, {'btn_text': 601214})
            return
        if strike_type == 'free':
            if status == ITEM_UNRECEIVED:
                update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE, {'btn_text': 635219})
            else:
                super(AsyncYuanbaoStrikeTaskListWidget, self)._update_receive_btn(task_id, status, ui_item)
        elif strike_type == 'pay':
            if limite_pay(self._goods_id):
                if status == ITEM_UNRECEIVED:
                    update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE, {'btn_text': 635219})
                else:
                    super(AsyncYuanbaoStrikeTaskListWidget, self)._update_receive_btn(task_id, status, ui_item)
            else:
                update_task_list_btn(btn_receive, BTN_ST_INACTIVE)
        else:
            log_error('wrong strike type task_id', task_id)

    def _reorder_task_list(self, task_list):
        top_task_id_list = []
        if self._ui_data:
            top_task_id_list = self._ui_data.get('top_task_id_list', None)
        has_bought = limite_pay(self._goods_id)

        def cmp_func(task_id_a, task_id_b):
            if top_task_id_list and task_id_a in top_task_id_list:
                return -1
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            total_times_a = task_utils.get_total_prog(task_id_a)
            cur_times_a = global_data.player.get_task_prog(task_id_a)
            total_times_b = task_utils.get_total_prog(task_id_b)
            cur_times_b = global_data.player.get_task_prog(task_id_b)
            not_finished_a = cur_times_a < total_times_a or task_id_a in self._pay_tasks and not has_bought
            not_finished_b = cur_times_b < total_times_b or task_id_a in self._pay_tasks and not has_bought
            if not_finished_a != not_finished_b:
                if not_finished_a:
                    return 1
                if not_finished_b:
                    return -1
            return 0

        task_list = sorted(task_list, key=cmp_to_key(cmp_func))
        return task_list

    def _refresh_time_widget(self):
        if not self.panel or not self.panel.lab_tips_time:
            return
        if loop_activity_data.is_loop_activity(self._activity_type):
            begin_time, end_time = loop_activity_data.get_loop_task_open_time(self._activity_type)
            task_left_time = end_time - time_utility.time()
        else:
            task_left_time = task_utils.get_raw_left_open_time(self._fixed_task_id)
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_tips_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(task_left_time)))
            else:
                self.panel.lab_tips_time.SetString(get_text_by_id(607014).format(get_readable_time(task_left_time)))
        else:
            close_left_time = 0
            self.panel.lab_tips_time.SetString(601214)
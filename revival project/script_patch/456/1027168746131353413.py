# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCollectNew.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_EXCHANGED, BTN_ST_EXCHANGE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityExchange import ActivityExchange
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityCollectNew(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityCollectNew, self).__init__(dlg, activity_type)
        self.fixed_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.random_task_id = act_data.get('daily_random', None)
        self._children_tasks = []
        self.act_list = None
        return

    def on_init_panel(self):
        self.act_list = self.panel.act_list_common
        self.show_list()

    def on_finalize_panel(self):
        super(ActivityCollectNew, self).on_finalize_panel()
        self._children_tasks = []

    def show_list(self):
        player = global_data.player
        if not player:
            return
        else:
            if not self.act_list:
                log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
                return
            fixed_children_tasks = []
            if self.fixed_task_id:
                fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id) or []
            random_children_tasks = []
            if self.random_task_id:
                random_refresh_type = task_utils.get_task_fresh_type(self.random_task_id)
                random_children_tasks = player.get_random_children_tasks(random_refresh_type, self.random_task_id)
                if random_children_tasks is None:
                    log_error('ActivityExchangeNew no random children tasks!')
                    random_children_tasks = []
            children_tasks = fixed_children_tasks + random_children_tasks
            self._children_tasks = self.reorder_task_list(children_tasks)
            self.act_list.SetInitCount(0)
            self.act_list.SetInitCount(len(self._children_tasks))
            activity_type = self._activity_type
            conf = confmgr.get('c_activity_config', activity_type)
            ui_data = conf.get('cUiData', {})
            for idx, task_id in enumerate(self._children_tasks):
                item_widget = self.act_list.GetItem(idx).temp_common
                item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
                reward_id = task_utils.get_task_reward(task_id)
                template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
                if ui_data.get('lab_name_color'):
                    color = int(ui_data.get('lab_name_color'), 16)
                    item_widget.lab_name.SetColor(color)
                if ui_data.get('lab_num_color'):
                    color = int(ui_data.get('lab_num_color'), 16)
                    item_widget.lab_num.SetColor(color)

            self.init_get_all_btn()
            self.update_get_all_btn()
            self.refresh_list()
            return

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        if not self.act_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        for idx, task_id in enumerate(self._children_tasks):
            item_widget = self.act_list.GetItem(idx).temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            update_task_list_btn(item_widget.nd_task.temp_btn_get, self.get_receive_btn_status(task_id))

            @item_widget.nd_task.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id):
                self.on_click_receive_btn(_task_id)

    def get_receive_btn_status(self, task_id):
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_RECEIVED:
            return BTN_ST_RECEIVED
        if status == ITEM_UNGAIN:
            return BTN_ST_ONGOING
        if status == ITEM_UNRECEIVED:
            return BTN_ST_CAN_RECEIVE

    def on_click_receive_btn(self, task_id):
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                task_utils.try_do_jump(task_id)
            return
        global_data.player.receive_task_reward(task_id)

    def on_click_get_all_btn(self, *args):
        task_ids = []
        if self.fixed_task_id:
            task_ids.append(self.fixed_task_id)
        if self.random_task_id:
            task_ids.append(self.random_task_id)
        if task_ids:
            global_data.player.receive_tasks_reward(task_ids)

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
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
            not_finished_a = cur_times_a < total_times_a
            not_finished_b = cur_times_b < total_times_b
            if not_finished_a != not_finished_b:
                if not_finished_a:
                    return 1
                if not_finished_b:
                    return -1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def init_get_all_btn(self):

        @self.panel.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            self.on_click_get_all_btn()

    def update_get_all_btn(self):
        receivable_task_num = len(self.get_all_receivable_tasks())
        if receivable_task_num >= 1:
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(receivable_task_num))
        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

    def get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self._children_tasks:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task
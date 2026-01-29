# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncTaskListWidget.py
from __future__ import absolute_import
from functools import cmp_to_key
from .Widget import Widget
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_GO
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import template_utils, item_utils, task_utils, activity_utils
from logic.gutils.client_utils import post_ui_method
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.cdata import loop_activity_data
from logic.gcommon import time_utility

class AsyncTaskListWidget(Widget):

    def __init__(self, panel, activity_type):
        super(AsyncTaskListWidget, self).__init__(panel, activity_type)
        self._timer = 0

    def on_init_panel(self):
        super(AsyncTaskListWidget, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._fixed_task_id = conf.get('cTask', '')
        self._random_task_id = conf.get('cUiData', {}).get('daily_random', None)
        self._force_task_list = []
        self._ui_data = conf.get('cUiData', {})
        self.__process_event(True)
        self.__process_timer(True)
        self.panel.act_list.BindMethod('OnCreateItem', self._on_create_item(self._create_task_item, self._ui_data))
        self.refresh_panel()
        return

    def on_finalize_panel(self):
        self.__process_timer(False)
        self.__process_event(False)
        super(AsyncTaskListWidget, self).on_finalize_panel()

    def refresh_panel(self):
        super(AsyncTaskListWidget, self).refresh_panel()
        if not global_data.player:
            return
        self._refresh_task_list()
        self.__refresh_task_widget()
        self.__refresh_get_widget()

    def __process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self._on_update_task,
           'receive_task_reward_succ_event': self._on_update_task,
           'receive_task_prog_reward_succ_event': self._on_update_task
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
        player = global_data.player
        if self._fixed_task_id:
            fixed_task_list = task_utils.get_children_task(self._fixed_task_id)
            if not fixed_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe5\x9b\xba\xe5\xae\x9a\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._fixed_task_id)
                fixed_task_list = [self._fixed_task_id]
        else:
            fixed_task_list = []
        if self._random_task_id:
            random_refresh_type = task_utils.get_task_fresh_type(self._random_task_id)
            random_task_list = player.get_random_children_tasks(random_refresh_type, self._random_task_id)
            if not random_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % self._random_task_id)
                random_task_list = []
            task_list = fixed_task_list + random_task_list
        else:
            task_list = fixed_task_list
        if self._force_task_list:
            task_list += self._force_task_list
        if task_list:
            task_list = self._reorder_task_list(task_list)
        self._task_list = task_list

    def _reorder_task_list(self, task_list):
        top_task_id_list = []
        if self._ui_data:
            top_task_id_list = self._ui_data.get('top_task_id_list', None)

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
            not_finished_a = cur_times_a < total_times_a
            not_finished_b = cur_times_b < total_times_b
            if not_finished_a != not_finished_b:
                if not_finished_a:
                    return 1
                if not_finished_b:
                    return -1
            return 0

        task_list = sorted(task_list, key=cmp_to_key(cmp_func))
        return task_list

    def __refresh_get_widget(self):
        if not self.panel.temp_get_all:
            return
        else:
            player = global_data.player
            can_receive_task = []
            for task_id in self._task_list:
                reward_id = task_utils.get_task_reward(task_id)
                cur_prog = player.get_task_prog(task_id)
                if reward_id is None:
                    prog_rewards = task_utils.get_task_prog_rewards(task_id)
                    max_prog = prog_rewards[-1][0]
                    for prog, reward_id in prog_rewards:
                        if not player.has_receive_prog_reward(task_id, prog):
                            if cur_prog >= prog:
                                can_receive_task.append(task_id)
                            break

                else:
                    status = player.get_task_reward_status(task_id)
                    if status == ITEM_UNRECEIVED:
                        can_receive_task.append(task_id)

            task_num = len(can_receive_task)
            if task_num > 1:
                self.panel.nd_get_all.setVisible(True)
                self.panel.temp_get_all.setVisible(True)
                self.panel.img_num.setVisible(True)
                self.panel.lab_num.SetString(str(task_num))

                @self.panel.temp_get_all.btn_common_big.unique_callback()
                def OnClick(btn, touch):
                    global_data.player.receive_tasks_reward(can_receive_task)

            else:
                self.panel.nd_get_all.setVisible(False)
                self.panel.temp_get_all.setVisible(False)
            return

    def __refresh_task_widget(self):
        self.panel.act_list.scroll_reload(len(self._task_list))

    def _on_create_item(self, inst_cb, ui_data):

        def _on_create_item(list_reward, index, widget_item):
            inst_cb(widget_item, index, ui_data)

        return _on_create_item

    def _create_task_item(self, item_widget, index, ui_data):
        if not global_data.player:
            return
        else:
            ui_item = item_widget
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            task_id = self._task_list[index]
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            is_prog_task = True if reward_id is None else False
            cur_prog = global_data.player.get_task_prog(task_id)
            if is_prog_task:
                prog_rewards = task_utils.get_task_prog_rewards(task_id)
                max_prog = prog_rewards[-1][0]
                for prog, reward_id in prog_rewards:
                    if not global_data.player.has_receive_prog_reward(task_id, prog):
                        if cur_prog >= prog:
                            status = ITEM_UNRECEIVED
                        else:
                            status = ITEM_UNGAIN
                        break
                else:
                    status = ITEM_RECEIVED

                total_prog = prog
                task_parm_dict = {'prog': total_prog}
            else:
                task_parm_dict = None
                max_prog = total_prog = task_utils.get_total_prog(task_id)
                status = global_data.player.get_task_reward_status(task_id)
            task_name = task_utils.get_task_name(task_id, task_parm_dict)
            item_widget.lab_name.SetString(task_name)
            template_utils.quick_init_common_reward_list(item_widget.list_reward, reward_id)
            self.__update_lab_num(item_widget, total_prog, cur_prog)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)
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

    def __update_lab_num(self, item_widget, total_times, cur_times):
        if total_times > 1:
            item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('')

    def _update_receive_btn(self, task_id, status, ui_item):
        if ui_item.temp_common:
            ui_item = ui_item.temp_common
        btn_receive = ui_item.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            jump_conf = task_utils.get_jump_conf(task_id)
            if jump_conf:
                update_task_list_btn(btn_receive, BTN_ST_GO, {'btn_text': jump_conf.get('unreach_text', '')})
            else:
                update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

    def __process_timer(self, is_bind):
        if not self.panel.lab_tips_time:
            return
        if is_bind:
            self._timer = global_data.game_mgr.get_logic_timer().register(func=self._refresh_time_widget, interval=1, mode=CLOCK)
            self._refresh_time_widget()
        elif self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = 0

    def _refresh_time_widget(self):
        if not self.panel or not self.panel.lab_tips_time:
            return
        if loop_activity_data.is_loop_activity(self._activity_type):
            begin_time, end_time = loop_activity_data.get_loop_activity_open_time(self._activity_type)
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
            self.panel.lab_tips_time.SetString(get_readable_time(close_left_time))
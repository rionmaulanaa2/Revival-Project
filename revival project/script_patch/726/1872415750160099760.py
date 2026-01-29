# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityProgressTasks.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityProgressTasks(ActivityBase):
    LAB_TIME_NAME = 'lab_time'
    LAB_LEFT_TIME_NAME = 'lab_left_time'
    LAB_INFO_NAME = 'lab_info'

    def __init__(self, dlg, activity_type):
        super(ActivityProgressTasks, self).__init__(dlg, activity_type)
        self._timer = None
        self._timer_cb = {}
        self._task_id = None
        self._progress_2_reward_dict = {}
        self._left_time_node = None
        return

    def on_init_panel(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._process_event(True)
        self._init_ui_event()
        self._init_activity_time()
        self._left_time_node = getattr(self.panel, self.LAB_LEFT_TIME_NAME) if self.LAB_LEFT_TIME_NAME else None
        if self._left_time_node:
            self._register_timer()
            self._timer_cb[0] = lambda : self._refresh_left_time()
            self._refresh_left_time()
        lab_info_node = getattr(self.panel, self.LAB_INFO_NAME) if self.LAB_INFO_NAME else None
        if lab_info_node:
            lab_info_node.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        if self._task_id:
            self._progress_2_reward_dict = task_utils.get_prog_rewards_in_dict(self._task_id)
        self._show_tasks_list()
        self._custom_init_panel()
        return

    def set_show(self, show, is_init=False):
        super(ActivityProgressTasks, self).set_show(show, is_init)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def _refresh_left_time(self):
        left_time_delta = activity_utils.get_left_time(self._activity_type)
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self._left_time_node.SetString(day_txt)

    def _show_tasks_list(self, *args):
        task_ui_list = self.panel.act_list
        task_ui_list.SetInitCount(0)
        task_ui_list.SetInitCount(len(self._progress_2_reward_dict))
        progress_list = self._reorder_progress_list(six_ex.keys(self._progress_2_reward_dict), self._task_id)
        for idx, progress in enumerate(progress_list):
            task_ui = task_ui_list.GetItem(idx)
            if not task_ui:
                return
            task_ui.lab_name.SetString(task_utils.get_task_name(self._task_id, {'prog': progress}))
            reward_id = self._progress_2_reward_dict.get(progress)
            template_utils.init_common_reward_list(task_ui.list_reward, reward_id)
            if global_data.player:
                task_ui.lab_num.setVisible(True)
                cur_progress = global_data.player.get_task_prog(self._task_id)
                if cur_progress > progress:
                    show_progress = progress if 1 else cur_progress
                    task_ui.lab_num.SetString('{0}/{1}'.format(show_progress, progress))
                else:
                    task_ui.lab_num.setVisible(False)
                btn_receive = task_ui.temp_btn_get.btn_common
                task_ui.nd_get.setVisible(False)

                @btn_receive.unique_callback()
                def OnClick(btn, touch, progress_num=progress):
                    if not activity_utils.is_activity_in_limit_time(self._activity_type) or not global_data.player:
                        return
                    global_data.player.receive_task_prog_reward(self._task_id, progress_num)
                    btn.SetText(80866)
                    btn.SetEnable(False)

                if not global_data.player:
                    is_received = False
                    can_receive = False
                else:
                    is_received = global_data.player.has_receive_prog_reward(self._task_id, progress)
                    can_receive = global_data.player.is_prog_reward_receivable(self._task_id, progress)
                btn_receive.setVisible(not is_received)
                btn_receive.SetEnable(can_receive)
                task_ui.nd_get.setVisible(is_received)

    def _reorder_progress_list(self, progress_lst, parent_task_id):
        if not global_data.player:
            return progress_lst

        def cmp_func(progress_a, progress_b):
            progress_a_receivable = global_data.player.is_prog_reward_receivable(parent_task_id, progress_a)
            progress_b_receivable = global_data.player.is_prog_reward_receivable(parent_task_id, progress_b)
            if progress_a_receivable != progress_b_receivable:
                if progress_a_receivable:
                    return -1
                if progress_b_receivable:
                    return 1
                has_received_a = global_data.player.has_receive_prog_reward(parent_task_id, progress_a)
                has_received_b = global_data.player.has_receive_prog_reward(parent_task_id, progress_b)
                if has_received_a != has_received_b:
                    if has_received_a:
                        return 1
                    if has_received_b:
                        return -1
                else:
                    return 0
            return 0

        return sorted(progress_lst, key=cmp_to_key(cmp_func))

    def _init_ui_event(self):
        pass

    def _init_activity_time(self):
        if self.LAB_TIME_NAME:
            time_node = getattr(self.panel, self.LAB_TIME_NAME)
            start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
            if start_str and end_str and time_node:
                time_node.SetString('{0} - {1}'.format(start_str, end_str))

    def _register_timer(self):
        from common.utils.timer import CLOCK
        self._unregister_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self._second_callback, interval=1, times=-1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def _second_callback(self):
        for timer_key, cb_func in six.iteritems(self._timer_cb):
            cb_func()

    def _process_event(self, is_bind):
        e_conf = {'receive_task_reward_succ_event': self._show_tasks_list,
           'receive_task_prog_reward_succ_event': self._show_tasks_list
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _custom_init_panel(self):
        pass

    def on_finalize_panel(self):
        self._process_event(False)
        self._unregister_timer()
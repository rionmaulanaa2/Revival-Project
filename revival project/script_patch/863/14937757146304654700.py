# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityKizunaWarmUp.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.time_utility import get_readable_time, ONE_HOUR_SECONS, get_readable_time_day_hour_minitue
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.new_template_utils import CommonItemReward
from common.utils.timer import CLOCK
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils import item_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_SHARE, BTN_ST_GO

class ActivityKizunaWarmUp(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaWarmUp, self).__init__(dlg, activity_type)
        self._collect_task = None
        self._concert_task = None
        self._concert_children_tasks = []
        self._collect_progress_rewards = {}
        self._timer = None
        return

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_info and self.panel.lab_info.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')))
        action_list.append(cc.DelayTime.create(0.7))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))
        self.panel.lab_tips.SetString(610008)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)
        self.show_list()

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('show')
        self.panel.stopAllActions()
        self._concert_children_tasks = []
        self._collect_progress_rewards = {}
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = 0

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), default={})
        ui_conf = conf.get('cUiData', {})
        self._collect_task = conf.get('cTask', None)
        self._concert_task = ui_conf.get('concert_parent_task', None)
        self._concert_children_tasks = task_utils.get_children_task(self._concert_task)
        self._concert_children_tasks = self.reorder_task_list(self._concert_children_tasks)
        self._collect_progress_rewards = {}
        self._timer = None
        return

    def refresh_left_time(self):
        left_time = task_utils.get_raw_left_open_time(self._concert_task)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def on_task_update(self, task_id, *args):
        if task_id not in self._concert_children_tasks and task_id != self._collect_task:
            return
        global_data.emgr.refresh_activity_redpoint.emit()
        if task_id == self._collect_task:
            self._refresh_collect_task_list()
        elif task_id in self._concert_children_tasks:
            self._refresh_concert_task_list()
        self._init_get_all()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.on_task_update,
           'receive_task_reward_succ_event': self.on_task_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def show_list(self):
        self._show_collect_task_list()
        self._show_concert_task_list()

    def refresh_list(self):
        self._refresh_collect_task_list()
        self._refresh_concert_task_list()

    def _show_concert_task_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(self._concert_children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(self._concert_children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self._refresh_concert_task_list()

    def _show_collect_task_list(self):
        self.panel.nd_finsh.list_item.DeleteAllSubItem()
        prog_rewards = task_utils.get_prog_rewards(self._collect_task)
        self.panel.nd_finsh.list_item.SetInitCount(len(prog_rewards))
        for i, prog_data in enumerate(prog_rewards):
            prog, reward_id = prog_data
            reward_item = self.panel.nd_finsh.list_item.GetItem(i)
            reward_item.lab_node_num.SetString(str(prog))

            def cb(_prog):
                player = global_data.player
                task_id = self._collect_task
                if not player.has_receive_prog_reward(task_id, _prog) and player.get_task_prog(task_id) >= _prog:
                    player.receive_task_prog_reward(task_id, _prog)

            self._collect_progress_rewards[prog] = CommonItemReward(reward_item.temp_item, reward_id, cb, (prog,), False)

        self._refresh_collect_task_list()

    def _refresh_concert_task_list(self):
        if not global_data.player:
            return
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._concert_children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            item_widget.nd_get.setVisible(False)
            btn = item_widget.temp_btn_get.btn_common

            def check_btn(widget=item_widget):
                btn_receive = widget.temp_btn_get
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
                elif cur_times < total_times:
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        update_task_list_btn(btn_receive, BTN_ST_GO)
                    else:
                        update_task_list_btn(btn_receive, BTN_ST_ONGOING)
                else:
                    update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetEnable(False)

            check_btn()

    def _refresh_collect_task_list(self):
        prog_rewards = task_utils.get_prog_rewards(self._collect_task)
        now_prog = global_data.player.get_task_prog(self._collect_task)
        total_prog = task_utils.get_total_prog(self._collect_task)
        progress = now_prog * 1.0 / total_prog * 100
        self.panel.progress_bar.setTouchEnabled(False)
        self.panel.progress_bg.setVisible(True)
        self.panel.progress_bar.SetPercent(progress)
        self.panel.nd_finsh.lab_finish_task.SetString(get_text_by_id(610009).format(now_prog))
        for i, prog_data in enumerate(prog_rewards):
            prog, reward_id = prog_data
            if prog > now_prog:
                state = ITEM_UNGAIN
            elif global_data.player.has_receive_prog_reward(self._collect_task, prog):
                state = ITEM_RECEIVED
            else:
                state = ITEM_UNRECEIVED
            self._collect_progress_rewards[prog].update_state(state)

    def _set_item_widget_lab_num(self, item_widget, total_times, cur_times):
        if total_times > 1:
            item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
        else:
            item_widget.lab_num.SetString('')

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

    def _init_get_all(self):
        if self._check_has_unreceived_reward():
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

        @self.panel.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            task_list = []
            task_list.extend(self._concert_children_tasks)
            task_list.append(self._collect_task)
            global_data.player.receive_tasks_reward(task_list)

    def _check_has_unreceived_reward(self):
        for task_id in self._concert_children_tasks:
            if global_data.player.has_unreceived_task_reward(task_id):
                return True

        return task_utils.has_unreceived_prog_reward(self._collect_task)
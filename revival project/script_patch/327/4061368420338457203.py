# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityGunTask.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
import cc

class ActivityGunTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityGunTask, self).__init__(dlg, activity_type)
        self.conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.fixed_task_id = self.conf.get('cTask', '')
        ui_data = self.conf.get('cUiData', {})
        self.random_task_id = ui_data.get('daily_random', None)
        self._collect_task = ui_data.get('change_task', '1410655')
        self._gun_item_no = ui_data.get('gun_item_no', '208100409')
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        act_name_id = self.conf.get('cNameTextID', '')
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(self.conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_describe
        if btn_describe:

            @btn_describe.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(self.conf.get('cRuleTextID', '')))
                x, y = btn_describe.GetPosition()
                wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        if not self.conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(self.conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')

    def show_list(self):
        if not global_data.player:
            return
        children_tasks = self.get_all_children_task()
        self._children_tasks = children_tasks
        self._timer_cb[0] = lambda : self.refresh_time(self.fixed_task_id)
        self.refresh_time(self.fixed_task_id)
        sub_act_list = self.panel.act_list
        sub_act_list.DeleteAllSubItem()
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = self.conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
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

        self.refresh_list()
        self._init_gun_progress()
        self._init_get_all()

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            ui_item = sub_act_list.GetItem(i)
            item_widget = ui_item.temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                status = player.get_task_reward_status(task_id)
                self.update_receive_btn(status, ui_item)

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
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()

    def update_receive_btn(self, status, ui_item):
        btn_receive = ui_item.temp_common.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

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

    def _init_gun_progress(self):
        player = global_data.player
        prog_rewards = task_utils.get_prog_rewards(self._collect_task)
        now_prog = global_data.player.get_task_prog(self._collect_task)
        self.panel.list_item.SetInitCount(len(prog_rewards))
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            progress, reward_id = prog_rewards[idx]
            if progress == 1:
                node = getattr(self.panel, 'lab_number_0')
            else:
                node = getattr(self.panel, 'lab_number_%s' % progress)
            node.SetString(str(progress))
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if idx == 0:
                item_no = self._gun_item_no
                item_num = 1
            else:
                item_no, item_num = reward_list[0]
            item_path = get_lobby_item_pic_by_item_no(item_no)
            ui_item.item.SetDisplayFrameByPath('', item_path)
            ui_item.lab_quantity.setVisible(True)
            ui_item.lab_quantity.SetString(str(item_num))
            can_receive = player.is_prog_reward_receivable(self._collect_task, progress) and not player.has_receive_prog_reward(self._collect_task, progress)
            is_received = player.has_receive_prog_reward(self._collect_task, progress)
            if is_received:
                ui_item.nd_get.setVisible(True)
                ui_item.nd_lock.setVisible(True)
                ui_item.btn_choose.SetSelect(False)
            elif can_receive:
                ui_item.btn_choose.SetSelect(True)
            else:
                ui_item.btn_choose.SetSelect(False)

            @ui_item.btn_choose.unique_callback()
            def OnClick(btn, touch, progress=progress, item_no=item_no, item_num=item_num, can_receive=can_receive):
                if can_receive:
                    global_data.player.receive_task_prog_reward(self._collect_task, progress)
                else:
                    x, y = btn.GetPosition()
                    w, h = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    extra_info = {'show_jump': False}
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        self.panel.prog_inside.SetPercentage(now_prog)

        @self.panel.btn_gun_see.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no(self._gun_item_no)

        first_reward_is_received = player.has_receive_prog_reward(self._collect_task, 1)
        last_reward_is_received = player.has_receive_prog_reward(self._collect_task, 100)
        task_left_time = task_utils.get_raw_left_open_time(self.fixed_task_id)
        if last_reward_is_received:
            self.panel.bar_tips_get.setVisible(True)
        elif first_reward_is_received:
            self.panel.bar_tips_count_down.setVisible(True)
            if task_left_time <= 86400:
                action_list = [cc.CallFunc.create(lambda : self.panel.bar_tips_count_down.setVisible(False)),
                 cc.CallFunc.create(lambda : self.panel.bar_tips_riko.setVisible(True)),
                 cc.DelayTime.create(5),
                 cc.CallFunc.create(lambda : self.panel.bar_tips_riko.setVisible(False)),
                 cc.CallFunc.create(lambda : self.panel.bar_tips_count_down.setVisible(True))]
                self.panel.runAction(cc.Sequence.create(action_list))

    def refresh_time(self, parent_task):
        task_left_time = task_utils.get_raw_left_open_time(self.fixed_task_id)
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_tips_time.SetString(get_readable_time_day_hour_minitue(task_left_time))
            else:
                self.panel.lab_tips_time.SetString(get_readable_time(task_left_time))
        else:
            close_left_time = 0
            self.panel.lab_tips_time.SetString(get_readable_time(close_left_time))

    def _init_get_all(self):
        task_num = len(self._get_all_receivable_tasks())
        if task_num >= 1:
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                task_list = []
                task_list.append(self.fixed_task_id)
                task_list.append(self.random_task_id)
                global_data.player.receive_tasks_reward(task_list)

        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

    def _get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self.get_all_children_task():
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task

    def get_all_children_task(self):
        if not global_data.player:
            return []
        player = global_data.player
        fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id)
        random_refresh_type = task_utils.get_task_fresh_type(self.random_task_id)
        random_children_tasks = player.get_random_children_tasks(random_refresh_type, self.random_task_id)
        children_tasks = fixed_children_tasks + random_children_tasks
        children_tasks = self.reorder_task_list(children_tasks)
        return children_tasks
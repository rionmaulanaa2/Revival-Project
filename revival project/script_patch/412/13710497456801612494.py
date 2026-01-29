# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummerVendingTask.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils import mall_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils.jump_to_ui_utils import jump_to_activity
from logic.gcommon.common_const.activity_const import ACTIVITY_SUMMER_VENDING_EXCHANGE, ACTIVITY_SUMMER_VENDING_TASK
from logic.gcommon.item.item_const import ITEM_UNRECEIVED
import cc
SUMMER_VENDING_ITEM_NO = 50101210
ITEM_ID_LST = [(201800171, 694000001), (50101151, 694000002), (50101101, 694000003), (50102006, 694000004), (50101002, 694000005)]

class ActivitySummerVendingTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivitySummerVendingTask, self).__init__(dlg, activity_type)
        self.fixed_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.random_task_id = act_data.get('daily_random', None)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        self.panel.list_task_common.setVisible(True)
        self.panel.act_list.setVisible(False)
        return

    def on_finalize_panel(self):
        super(ActivitySummerVendingTask, self).on_finalize_panel()
        self.sub_widget = None
        return

    def init_items(self):
        from logic.gutils.item_utils import get_lobby_item_name
        for idx in range(len(ITEM_ID_LST)):
            name_node = getattr(self.panel, 'lab_name_%s' % (idx + 1))
            item_id, goods_id = ITEM_ID_LST[idx]
            name_node.SetString(get_lobby_item_name(item_id, need_part_name=False))
            _, _, num_info = mall_utils.buy_num_limit_by_all(str(goods_id))
            left_num = 0
            if num_info:
                left_num, _ = num_info
            if left_num:
                num_text = get_text_by_id(607206).format(left_num)
            else:
                num_text = get_text_by_id(12127)
            num_node = getattr(self.panel, 'lab_num_%s' % (idx + 1))
            num_node.SetString(num_text)
            name_btn = getattr(self.panel, 'btn_click_%s' % (idx + 1))

            @name_btn.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                jump_to_activity(ACTIVITY_SUMMER_VENDING_EXCHANGE)

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.show_list()

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

    def init_parameters(self):
        super(ActivitySummerVendingTask, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def refresh_time(self, parent_task):
        task_id = confmgr.get('c_activity_config', ACTIVITY_SUMMER_VENDING_TASK, 'cTask', default='')
        exchange_id = confmgr.get('c_activity_config', ACTIVITY_SUMMER_VENDING_EXCHANGE, 'cTask', default='')
        task_left_time = task_utils.get_raw_left_open_time(task_id)
        exchange_left_time = task_utils.get_raw_left_open_time(exchange_id)
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(609771).format(get_readable_time_day_hour_minitue(task_left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(609771).format(get_readable_time(task_left_time)))
        elif exchange_left_time > 0:
            if exchange_left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(609772).format(get_readable_time_day_hour_minitue(exchange_left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(609772).format(get_readable_time(exchange_left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(ActivitySummerVendingTask, self).set_show(show, is_init)
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

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not global_data.player:
            return
        player = global_data.player
        fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id)
        random_refresh_type = task_utils.get_task_fresh_type(self.random_task_id)
        random_children_tasks = player.get_random_children_tasks(random_refresh_type, self.random_task_id)
        children_tasks = fixed_children_tasks + random_children_tasks
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        self._timer_cb[0] = lambda : self.refresh_time(self.fixed_task_id)
        self.refresh_time(self.fixed_task_id)
        sub_act_list = self.panel.list_task_common
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
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
        self._init_get_all()

    def refresh_list(self):
        sub_act_list = self.panel.list_task_common
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        btn.SetText(text_id)
                        btn.SetEnable(True)
                    else:
                        btn.SetEnable(False)
                else:
                    btn.setVisible(True)
                    btn.SetEnable(True)

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

    def transfer_panel_out(self):
        return self.panel

    def _init_get_all(self):
        task_num = len(self._get_all_receivable_tasks())
        if task_num >= 2:
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num_red.SetString(str(task_num))
            self.panel.btn_have.setVisible(False)

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                task_list = []
                task_list.append(self.fixed_task_id)
                task_list.append(self.random_task_id)
                global_data.player.receive_tasks_reward(task_list)

        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)
            item_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(SUMMER_VENDING_ITEM_NO)
            self.panel.lab_num.SetString(str(item_num))
            self.panel.btn_have.setVisible(True)

            @self.panel.btn_have.unique_callback()
            def OnClick(btn, touch, *args):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.GetParent().ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(SUMMER_VENDING_ITEM_NO, None, w_pos, extra_info=extra_info)
                return

    def _get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self.get_all_children_task():
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task

    def get_all_children_task(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not global_data.player:
            return []
        player = global_data.player
        fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id)
        random_refresh_type = task_utils.get_task_fresh_type(self.random_task_id)
        random_children_tasks = player.get_random_children_tasks(random_refresh_type, self.random_task_id)
        children_tasks = fixed_children_tasks + random_children_tasks
        children_tasks = self.reorder_task_list(children_tasks)
        return children_tasks
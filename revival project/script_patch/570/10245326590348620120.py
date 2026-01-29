# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMidAutumn/ActivityMidAutumnTask.py
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
from logic.gutils import mall_utils, item_utils, task_utils
from logic.gutils.jump_to_ui_utils import jump_to_activity
from logic.gcommon.common_const.activity_const import ACTIVITY_MID_AUTUMN_TASK, ACTIVITY_MID_AUTUMN_EXCHANGE
from logic.gcommon.item.item_const import ITEM_UNRECEIVED
import cc
EXCHANGE_COIN_ITEM_NO = 50600033
ITEM_ID_LST = [(50920104, 694000034), (30170110, 694000031), (50101105, 694000033), (50101228, 694000032), (50101002, 694000035), (208200219, 694000030)]

class ActivityMidAutumnTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityMidAutumnTask, self).__init__(dlg, activity_type)
        self.fixed_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.random_task_id = act_data.get('daily_random', None)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        self.panel.list_task_common.setVisible(True)
        self.panel.act_list.setVisible(False)
        self.refresh_item_num()
        return

    def on_finalize_panel(self):
        super(ActivityMidAutumnTask, self).on_finalize_panel()
        self.sub_widget = None
        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        global_data.emgr.change_activity_main_close_btn_visibility.emit(widget_type, True)
        return

    def init_items(self):
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
        item_id_list = ITEM_ID_LST
        for idx in range(len(item_id_list)):
            start_node = getattr(self.panel, 'temp_item_%s' % (idx + 1))
            item_id, goods_id = item_id_list[idx]
            self.init_node_item(start_node, item_id, goods_id)

    def init_node_item(self, ui_item, item_id, goods_id):
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
        ui_item.lab_item_name.SetString(get_lobby_item_name(item_id, need_part_name=False))
        _, _, num_info = mall_utils.buy_num_limit_by_all(str(goods_id))
        left_num = 0
        if num_info:
            left_num, _ = num_info
        if left_num:
            num_text = get_text_by_id(907118).format(left_num)
        else:
            num_text = get_text_by_id(12127)
        img_item_node = ui_item.temp_item.item
        item_path = get_lobby_item_pic_by_item_no(item_id)
        img_item_node.SetDisplayFrameByPath('', item_path)
        if ui_item == self.panel.temp_item_5:
            num_node = self.panel.bar_red_tag_di.nd_multilang_1.lab_summer
            num_node.SetString(num_text)
        num_node = ui_item.lab_summer
        num_node.SetString(num_text)
        name_btn = ui_item.temp_item.btn_choose
        item_utils.check_skin_tag(ui_item.temp_s, item_id)

        @name_btn.unique_callback()
        def OnClick(btn, touch, item_id=item_id):
            jump_to_activity(ACTIVITY_MID_AUTUMN_EXCHANGE)

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self.panel.temp_get_all.setVisible(False)
        self.show_list()
        self.panel.SetTimeOut(2.3, lambda : self.panel.PlayAnimation('loop_01'), tag=210825)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        global_data.emgr.change_activity_main_close_btn_visibility.emit(widget_type, False)

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            global_data.emgr.trigger_activity_main_close_btn.emit(widget_type)

    def init_parameters(self):
        super(ActivityMidAutumnTask, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def refresh_time(self, parent_task):
        task_id = confmgr.get('c_activity_config', ACTIVITY_MID_AUTUMN_TASK, 'cTask', default='')
        exchange_id = confmgr.get('c_activity_config', ACTIVITY_MID_AUTUMN_EXCHANGE, 'cTask', default='')
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
        super(ActivityMidAutumnTask, self).set_show(show, is_init)
        show_animation_name = 'show'
        loop_animation_name = 'loop'
        loop01_animation_name = 'loop_01'
        if self.cur_tab_name_id == self.last_tab_name_id:
            if not self.panel.IsPlayingAnimation(loop_animation_name):
                show and self.panel.PlayAnimation(loop_animation_name)
                if show:
                    self._show_action()
            if not self.panel.IsPlayingAnimation(loop01_animation_name):
                show and self.panel.PlayAnimation(loop01_animation_name)
            return
        self.panel.stopAllActions()
        self.panel.StopAnimation(show_animation_name)
        self.panel.StopAnimation(loop_animation_name)
        self.panel.StopAnimation(loop01_animation_name)
        if show:
            self._show_action()

    def _show_action(self):
        show_animation_name = 'show'
        loop_animation_name = 'loop'
        loop01_animation_name = 'loop_01'
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(show_animation_name)),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(loop_animation_name)),
         cc.DelayTime.create(2.3),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(loop01_animation_name))]))
        if self.sub_widget and self.sub_widget.panel:
            self.sub_widget.panel.PlayAnimation(show_animation_name)
        self.panel.temp_item_6.StopAnimation('show')
        self.panel.temp_item_6.StopAnimation('loop')
        self.panel.temp_item_6.StopAnimation('high_show')
        self.panel.temp_item_6.PlayAnimation('show')
        self.panel.temp_item_6.PlayAnimation('loop')
        self.panel.temp_item_6.PlayAnimation('high_show')
        other_list = [
         (
          0.07, self.panel.temp_item_2), (0.1, self.panel.temp_item_4), (0.1, self.panel.temp_item_1),
         (
          0.13, self.panel.temp_item_3), (0.13, self.panel.temp_item_5)]
        self.panel.SetTimeOut(0.13, lambda : self.panel.PlayAnimation('show_01'), tag=210830)
        for idx, item_info in enumerate(other_list):
            delay, item = item_info
            item.setVisible(False)
            item.StopAnimation('show')
            item.StopAnimation('loop')

            def func(item=item, idx=idx):
                item.setVisible(True)
                item.PlayAnimation('show')
                item.PlayAnimation('loop')

            self.panel.SetTimeOut(delay, func, tag=21082502 + idx)

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
        self.refresh_item_num()

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
                    btn.SetText(604029)
                    btn.SetEnable(False)
                    btn.setVisible(True)
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

    def refresh_item_num(self):
        item_num = global_data.player or 0 if 1 else global_data.player.get_item_num_by_no(EXCHANGE_COIN_ITEM_NO)
        self.panel.lab_have.SetString(get_text_by_id(907119, {'num': str(item_num)}))

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
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num_red.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                task_list = []
                task_list.append(self.fixed_task_id)
                task_list.append(self.random_task_id)
                global_data.player.receive_tasks_reward(task_list)

        else:
            self.panel.temp_get_all.setVisible(False)

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
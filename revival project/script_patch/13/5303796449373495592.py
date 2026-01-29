# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityThanksgivingTrainTask.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils import mall_utils
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_const.activity_const import ACTIVITY_HALLOWEEN_ACTIVITY1, ACTIVITY_HALLOWEEN_ACTIVITY2
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED
from logic.gutils.new_template_utils import update_task_list_btn
import cc

class ActivityThanksgivingTrainTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityThanksgivingTrainTask, self).__init__(dlg, activity_type)
        self.fixed_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.random_task_id = act_data.get('daily_random', None)
        self.last_tab_name_id = None
        self.cur_tab_name_id = confmgr.get('c_activity_config', str(activity_type), 'iCatalogID', default='')
        self.sub_widget = None
        self.cur_pumpkin_num = global_data.player.get_item_num_by_no(50600035)
        self.get_gun_first_time = True
        if self.cur_pumpkin_num >= 14:
            self.get_gun_first_time = False
        self.has_gun = False
        if global_data.player.get_item_num_by_no(208105517):
            self.has_gun = True
        return

    def on_finalize_panel(self):
        super(ActivityThanksgivingTrainTask, self).on_finalize_panel()
        global_data.emgr.set_reward_show_blocking_item_no_event.emit([])
        self.sub_widget = None
        return

    def init_items(self):
        pass

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.init_items()
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        if not self.has_gun:
            for index in range(0, min(self.cur_pumpkin_num, 14)):
                self.panel.nd_content.bar_bg.nd_pumpkin.__getattribute__('temp_pumpkin_' + str(index + 1)).PlayAnimation('switch')

        else:
            for index in range(0, 14):
                self.panel.nd_content.bar_bg.nd_pumpkin.__getattribute__('temp_pumpkin_' + str(index + 1)).PlayAnimation('switch')

        global_data.emgr.set_reward_show_blocking_item_no_event.emit([50600035])
        self.show_list()

    def refresh_time(self, parent_task):
        task_id = confmgr.get('c_activity_config', ACTIVITY_HALLOWEEN_ACTIVITY1, 'cTask', default='')
        task_left_time = task_utils.get_raw_left_open_time(task_id)
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.nd_content.img_title_dec.lab_time.SetString(get_text_by_id(610171).format(get_readable_time_day_hour_minitue(task_left_time)))
            else:
                self.panel.nd_content.img_title_dec.lab_time.SetString(get_text_by_id(610171).format(get_readable_time(task_left_time)))
        else:
            close_left_time = 0
            self.panel.nd_content.img_title_dec.lab_time.SetString(get_readable_time(close_left_time))

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget

    def set_show(self, show, is_init=False):
        super(ActivityThanksgivingTrainTask, self).set_show(show, is_init)
        self.panel.stopAllActions()
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        self.panel.RecordAnimationNodeState('loop')
        if show:
            if self.cur_pumpkin_num >= 14 and not self.has_gun:
                self.panel.RecordAnimationNodeState('loop_01')
                self.panel.runAction(cc.Sequence.create([
                 cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
                 cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
                 cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_01'))]))
                if self.sub_widget and self.sub_widget.panel:
                    self.sub_widget.panel.PlayAnimation('show')
            else:
                self.panel.runAction(cc.Sequence.create([
                 cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
                 cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
                 cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
                if self.sub_widget and self.sub_widget.panel:
                    self.sub_widget.panel.PlayAnimation('show')

    def show_get_item_first_time(self):
        self.panel.stopAllActions()
        self.panel.StopAnimation('full_show')
        self.panel.StopAnimation('loop_01')
        self.panel.RecordAnimationNodeState('loop_01')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('full_show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop_01'))]))

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not global_data.player:
            return
        if global_data.player.get_item_num_by_no(208105517):
            self.has_gun = True
        player = global_data.player
        fixed_children_tasks = task_utils.get_children_task(self.fixed_task_id)
        children_tasks = fixed_children_tasks
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        self._timer_cb[0] = lambda : self.refresh_time(self.fixed_task_id)
        self.refresh_time(self.fixed_task_id)
        sub_act_list = self.panel.act_list
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

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            ui_item = sub_act_list.GetItem(i)
            item_widget = ui_item.temp_common
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
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

        nd_content = self.panel.nd_content
        lab_tips = nd_content.lab_tips
        pumpkin_num = global_data.player.get_item_num_by_no(50600035)
        if self.cur_pumpkin_num < pumpkin_num <= 14:
            for index in range(self.cur_pumpkin_num, min(pumpkin_num, 14)):
                self.panel.nd_content.bar_bg.nd_pumpkin.__getattribute__('temp_pumpkin_' + str(index + 1)).PlayAnimation('click')

            self.cur_pumpkin_num = pumpkin_num
        if self.cur_pumpkin_num < 14:
            if not self.has_gun:
                lab_tips.SetString(get_text_by_id(610172).format(14 - self.cur_pumpkin_num))
            else:
                lab_tips.nd_auto_fit.icon_type.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202111/thanksgiving_day/icon_thanksgiving_open.png')
                lab_tips.SetString(12136)
        elif self.cur_pumpkin_num >= 14:
            if self.has_gun:
                lab_tips.nd_auto_fit.icon_type.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202111/thanksgiving_day/icon_thanksgiving_open.png')
                lab_tips.SetString(12136)
            else:
                lab_tips.setVisible(False)
                nd_content.btn_get.setVisible(True)
                if self.get_gun_first_time:
                    self.get_gun_first_time = False
                    self.show_get_item_first_time()

                @self.panel.nd_content.btn_get.unique_callback()
                def OnClick(btn, touch):
                    global_data.player.receive_task_reward('1440404')
                    self.has_gun = True
                    self.panel.nd_content.btn_get.setVisible(False)
                    lab_tips.setVisible(True)
                    lab_tips.nd_auto_fit.icon_type.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202111/thanksgiving_day/icon_thanksgiving_open.png')
                    lab_tips.SetString(12136)
                    self.panel.stopAllActions()
                    self.panel.StopAnimation('loop_01')
                    self.panel.RecoverAnimationNodeState('loop_01')

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

    def transfer_panel_out(self):
        return self.panel
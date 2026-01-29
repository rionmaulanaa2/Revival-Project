# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/TaskListWidget.py
from __future__ import absolute_import
from .ActivityWidgetBase import ActivityWidgetBase
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr

class TaskListWidget(ActivityWidgetBase):
    GLOBAL_EVENT = {'task_prog_changed': 'on_update_reward',
       'receive_task_reward_succ_event': 'on_update_reward'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.refresh_list_content()

    def refresh_panel(self):
        self.refresh_list_content()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self.activity_id)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if task_list:
            parent_task = task_list[0]
            self._children_tasks = task_utils.get_children_task(parent_task)

    def refresh_list_content(self):
        ui_data = confmgr.get('c_activity_config', str(self.activity_id), 'cUiData', default={})
        self._children_tasks = task_utils.reorder_task_list(self._children_tasks)
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(len(self._children_tasks))
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            name_color = ui_data.get('lab_name_color')
            name_color and item_widget.lab_name.SetColor(int(name_color, 16))
            num_color = ui_data.get('lab_num_color')
            num_color and item_widget.lab_num.SetColor(int(num_color, 16))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list_status()

    def refresh_list_status(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            task_id = str(task_id)
            item_widget = sub_act_list.GetItem(i)
            if item_widget.temp_common:
                item_widget = item_widget.temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times > 1:
                item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
            else:
                item_widget.lab_num.SetString('')
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)
            has_rewarded = global_data.player.has_receive_reward(task_id)
            if has_rewarded:
                btn.SetEnable(False)
                btn.SetText(80866)
            elif cur_times < total_times:
                btn.setVisible(True)
                jump_conf = task_utils.get_jump_conf(task_id)
                text_id = jump_conf.get('unreach_text', '')
                if text_id and not global_data.player.is_today_shared() and total_times - cur_times <= 1:
                    btn.SetText(text_id)
                    btn.SetEnable(True)
                else:
                    btn.SetEnable(False)
                    btn.SetText(80930)
            else:
                btn.setVisible(True)
                btn.SetEnable(True)
                btn.SetText(80930)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self.activity_id):
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

    def on_update_reward(self, *args):
        global_data.player.read_activity_list(self.activity_id)
        self.refresh_list_content()
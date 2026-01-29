# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/TaskListWithTagWidget.py
from __future__ import absolute_import
from six.moves import zip
from .TaskListWidget import TaskListWidget
from common.cfg import confmgr
from logic.gutils import activity_utils, task_utils

class TaskListWithTagWidget(TaskListWidget):
    GLOBAL_EVENT = {'task_prog_changed': 'on_update_reward',
       'receive_task_reward_succ_event': 'on_update_reward'
       }

    def on_init_panel(self):
        self._cur_tab_index = -1
        self.init_parameters()
        self.init_tab()
        self.select_tab(0)

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self.activity_id)
        self.task_info = conf['cUiData']['task_info']
        self._children_tasks = self.task_info[self._cur_tab_index]['task_list']

    def init_tab(self):
        self.panel.list_btn.SetInitCount(len(self.task_info))
        for i, info in enumerate(self.task_info):
            tab_item = self.panel.list_btn.GetItem(i)
            tab_item.btn_top.BindMethod('OnClick', lambda b, t, index=i: self.select_tab(index))
            if 'text_id' in info:
                tab_item.btn_top.SetText(info['text_id'])

    def select_tab(self, index):
        if index == self._cur_tab_index:
            return
        self._cur_tab_index = index
        for i, tab_item in enumerate(self.panel.list_btn.GetAllItem()):
            tab_item.btn_top.SetSelect(i == self._cur_tab_index)

        self._children_tasks = self.task_info[self._cur_tab_index]['task_list']
        self.refresh_list_content()

    def refresh_list_content(self):
        super(TaskListWithTagWidget, self).refresh_list_content()
        self.refresh_one_click()
        for tab_item, task_info in zip(self.panel.list_btn.GetAllItem(), self.task_info):
            rp = False
            for task_id in task_info.get('task_list', []):
                if global_data.player.is_task_reward_receivable(str(task_id)):
                    rp = True
                    break

            tab_item.img_red.setVisible(rp)

    def refresh_one_click(self):
        conf = confmgr.get('c_activity_config', self.activity_id)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if not task_list:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        cnt = 0
        for task_id in children_tasks:
            if global_data.player.is_task_reward_receivable(str(task_id)):
                cnt += 1
                if cnt >= 2:
                    break

        visible = cnt >= 2
        self.panel.nd_get_all.setVisible(visible)
        self.panel.temp_get_all.btn_common_big.BindMethod('OnClick', lambda *args: global_data.player.receive_all_task_reward(parent_task))
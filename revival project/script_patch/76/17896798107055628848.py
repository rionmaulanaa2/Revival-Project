# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCarMenLogin.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
import cc

class ActivityCarMenLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityCarMenLogin, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        children_tasks = task_utils.get_children_task(self.task_id)
        self._normal_task = children_tasks[0:-1]
        self._special_task = children_tasks[-1]

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)

        @self.panel.btn_item.unique_callback()
        def OnClick(btn, touch):
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            w_pos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(50101158, None, w_pos, extra_info=extra_info)
            return

        @self.panel.btn_open.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no('101008020')

        @self.panel.btn_open1.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no('101008020')

        children_tasks = task_utils.get_children_task(self.task_id)
        normal_task = self.reorder_task_list(children_tasks[0:-1])
        self._normal_task = normal_task
        self._special_task = children_tasks[-1]
        self.panel.temp_task.lab_name.SetString(task_utils.get_task_name(self._special_task))
        spe_reward = task_utils.get_task_conf_by_id(str(self._special_task)).get('reward', 0)
        template_utils.init_common_reward_list(self.panel.temp_task.list_reward, spe_reward)
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(normal_task))
        for idx, task_id in enumerate(normal_task):
            item_widget = sub_act_list.GetItem(idx).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()
        return

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._normal_task):
            item_widget = sub_act_list.GetItem(i).temp_common
            btn = item_widget.temp_btn_get.btn_common
            status = global_data.player.get_task_reward_status(task_id)
            self.update_receive_btn(status, item_widget)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                global_data.player.receive_task_reward(task_id)
                btn.SetText(80866)
                btn.SetEnable(False)

        status = global_data.player.get_task_reward_status(self._special_task)
        self.update_receive_btn(status, self.panel.temp_task)
        if status == ITEM_RECEIVED:
            self.panel.lab_type.SetString(get_text_by_id(906668))
        else:
            self.panel.lab_type.SetString(get_text_by_id(610101))
        btn_spe = self.panel.temp_task.temp_btn_get.btn_common

        @btn_spe.unique_callback()
        def OnClick(btn, touch, task_id=self._special_task):
            if not activity_utils.is_activity_in_limit_time(self._activity_type):
                return
            global_data.player.receive_task_reward(task_id)
            btn.SetText(80866)
            btn.SetEnable(False)

    def update_receive_btn(self, status, ui_item):
        btn_receive = ui_item.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))
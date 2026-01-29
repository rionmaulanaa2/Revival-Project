# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandShare.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gcommon import time_utility as tutil
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED
from logic.gutils.template_utils import init_common_reward_list
from logic.gutils.new_template_utils import update_task_list_btn

class ActivityFairylandShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityFairylandShare, self).__init__(dlg, activity_type)
        self.parent_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.children_task_list = task_utils.get_children_task(self.parent_task_id)

    def on_init_panel(self):
        self.init_time_widget()
        self.init_reward_list()
        self.process_event(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def on_finalize_panel(self):
        self.process_event(False)
        self.children_task_list = []

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_reward_list,
           'task_prog_changed': self.update_reward_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def init_time_widget(self):
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
        self.panel.nd_activity.nd_task.img_icon_info.lab_info.SetString(int(desc_id))

    def init_reward_list(self):
        player = global_data.player
        if not player:
            return
        ui_list = self.panel.nd_task.act_list
        ui_list.SetInitCount(0)
        ui_list.SetInitCount(len(self.children_task_list))
        ordered_task_list = self.reorder_task_list(self.children_task_list)
        for idx, ui_item in enumerate(ui_list.GetAllItem()):
            task_id = ordered_task_list[idx]
            reward_id = task_utils.get_task_reward(task_id)
            cur_prog = player.get_task_prog(task_id)
            total_prog = task_utils.get_total_prog(task_id)
            task_name = get_text_by_id(906677).format(self.children_task_list.index(task_id) + 1)
            ui_item.temp_common.nd_task.lab_name.SetString(task_name)
            ui_item.temp_common.nd_task.lab_num.SetString('{0}/{1}'.format(min(cur_prog, total_prog), total_prog))
            init_common_reward_list(ui_item.temp_common.nd_task.list_reward, reward_id)
            status = player.get_task_reward_status(task_id)
            self.update_receive_btn(status, ui_item)

            @ui_item.temp_common.nd_task.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id):
                self.on_click_btn_receive(btn, _task_id)

    def update_reward_list(self, *args):
        player = global_data.player
        if not player:
            return
        self.init_reward_list()
        reward_status = player.get_task_reward_status(self.children_task_list[-1])
        lab_tips = self.panel.nd_activity.nd_content.nd_tips.word_tips.nd_auto_fit.lab_tips
        if reward_status != ITEM_UNGAIN:
            lab_tips.SetString(607219)
        else:
            lab_tips.SetString(906639)
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_receive_btn(self, status, ui_item):
        btn_receive = ui_item.temp_common.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

    def on_click_btn_receive(self, btn, task_id):
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        player = global_data.player
        if not player:
            return
        player.receive_task_reward(task_id)

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            player = global_data.player
            can_receive_reward_a = player.is_task_reward_receivable(task_id_a)
            can_receive_reward_b = player.is_task_reward_receivable(task_id_b)
            if can_receive_reward_a != can_receive_reward_b:
                if can_receive_reward_a:
                    return -1
                if can_receive_reward_b:
                    return 1
            has_rewarded_a = player.has_receive_reward(task_id_a)
            has_rewarded_b = player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            not_finished_a = player.is_task_finished(task_id_a)
            not_finished_b = player.is_task_finished(task_id_b)
            if not_finished_a != not_finished_b:
                if not_finished_a:
                    return 1
                if not_finished_b:
                    return -1
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list
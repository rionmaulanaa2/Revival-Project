# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityHalloween/ActivityHalloweenRandomTask.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget import widget
from logic.gutils.task_utils import get_task_prog_rewards, get_task_arg
from logic.gutils.client_utils import post_method

@widget('AsyncTaskListWidget', 'DescribeWidget')
class ActivityHalloweenRandomTask(ActivityBase):

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityHalloweenRandomTask, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityHalloweenRandomTask, self).on_init_panel()
        self.process_event(True)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_prog_reward(self._final_task, self._final_request_point)

        self.conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = self.conf.get('cUiData', {})
        self._final_task = ui_data.get('final_task', '')
        self._final_request_point, self._final_reward = get_task_prog_rewards(self._final_task)[0]
        self._final_reward_item = confmgr.get('common_reward_data', str(self._final_reward), 'reward_list')[0][0]
        task_arg = get_task_arg(self._final_task)
        self.point_item_id = task_arg[0]
        self._on_update_reward()

    def refresh_panel(self):
        super(ActivityHalloweenRandomTask, self).refresh_panel()
        self._on_update_reward()

    @post_method
    def _on_update_reward(self, *args):
        if not global_data.player or not self.panel:
            return
        point_cnt = global_data.player.get_item_num_by_no(self.point_item_id)
        if self._final_request_point and self._final_request_point > 0:
            percent = point_cnt * 100.0 / self._final_request_point
        self.panel.prog.SetPercentage(percent)
        if percent >= 100:
            self.panel.prog.setVisible(False)
            self.panel.bg_prog.setVisible(False)
        else:
            self.panel.prog.setVisible(True)
            self.panel.bg_prog.setVisible(True)
        self.panel.lab_got.SetString('%s%d/%d' % (get_text_by_id(80860), point_cnt, self._final_request_point))
        reward_get = bool(global_data.player.get_item_by_no(self._final_reward_item))
        self.panel.icon_got.setVisible(reward_get)
        can_get = not reward_get and point_cnt >= self._final_request_point
        self.panel.btn_get.SetEnable(can_get)
        self.panel.btn_get.SetText(get_text_by_id(604029) if reward_get else get_text_by_id(604030))
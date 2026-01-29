# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityChristmas/ActivityChristmasMatchTeammate.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityMatchTeammate import ActivityMatchTeammate

class ActivityChristmasMatchTeammate(ActivityMatchTeammate):

    def __init__(self, dlg, activity_type):
        super(ActivityChristmasMatchTeammate, self).__init__(dlg, activity_type)
        self.conf = confmgr.get('c_activity_config', activity_type)
        self.task_id = str(self.conf.get('cTask', 0))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_receive_task_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.process_event(True)
        super(ActivityChristmasMatchTeammate, self).on_init_panel()
        self.panel.lab_info_1.SetString(610295)
        self.panel.lab_info_3.SetString(610296)
        btn = self.panel.btn_sign
        can_receive_task_reward = global_data.player.is_task_finished(self.task_id)
        has_receive_task_reward = global_data.player.has_receive_reward(self.task_id)
        if can_receive_task_reward and not has_receive_task_reward:
            btn.SetEnable(True)
            btn.SetText(604030)
        else:
            btn.SetEnable(False)
            if not can_receive_task_reward:
                btn.SetText(604028)
            elif has_receive_task_reward:
                btn.SetText(604029)
        from logic.gutils.task_utils import get_task_reward
        task_reward_id = get_task_reward(self.task_id)
        reward_list = confmgr.get('common_reward_data', str(task_reward_id), 'reward_list', default=[])
        task_reward = reward_list[0]

        @self.panel.btn_sign.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_reward(self.task_id)

        from logic.gutils.template_utils import init_tempate_reward
        init_tempate_reward(self.panel.temp_item, task_reward[0], task_reward[1], show_tips=True)

    def on_receive_task_reward(self, task_id):
        if str(task_id) == self.task_id:
            self.panel.btn_sign.SetEnable(False)
            self.panel.btn_sign.SetText(604029)

    def on_finalize_panel(self):
        self.process_event(False)
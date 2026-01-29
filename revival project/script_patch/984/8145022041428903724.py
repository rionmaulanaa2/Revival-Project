# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityBoxGift.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import activity_utils
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityBoxGift(ActivityBase):

    def on_init_panel(self):
        self.init_parameters()
        self.init_widget()
        self.init_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_received_task_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            log_error('[ERROR] activity [%s] task [%s] has no chidren task' % (activity_type, conf['cTask']))
            return
        self.parent_task = task_list[0]

    def init_widget(self):
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('loop')
        if global_data.player.has_unreceived_task_reward(self.parent_task):
            self.panel.btn_get.SetText(get_text_by_id(607053))
            self.panel.btn_get.SetEnable(True)
        else:
            self.panel.btn_get.SetText(get_text_by_id(607054))
            self.panel.btn_get.SetEnable(False)
        reward_id = task_utils.get_task_reward(self.parent_task)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        if reward_list:
            self.panel.list_reward.DeleteAllSubItem()
            for item_no, num in reward_list:
                item = self.panel.list_reward.AddTemplateItem()
                from logic.gutils.template_utils import init_tempate_reward
                item.img_frame.SetEnableCascadeOpacityRecursion(False)
                init_tempate_reward(item, item_no, num, show_tips=True)

    def init_event(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_reward(self.parent_task)

    def on_received_task_reward(self, task_id):
        if self.parent_task == task_id:
            self.panel.btn_get.SetText(get_text_by_id(607054))
            self.panel.btn_get.SetEnable(False)
            global_data.player.read_activity_list(self._activity_type)

    def on_finalize_panel(self):
        self.process_event(False)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityUpdatePackage.py
from __future__ import absolute_import
from six.moves import range
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityUpdatePackage(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityUpdatePackage, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self.parent_task = None
        conf = confmgr.get('c_activity_config', self._activity_type)
        if conf['cTask']:
            task_list = activity_utils.parse_task_list(conf['cTask'])
            if len(task_list) <= 0:
                return
            self.parent_task = task_list[0]
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._refresh_btn
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        from logic.gutils import task_utils
        reward_id = ''
        if self.parent_task:
            tmp_reward_id = task_utils.get_task_reward(self.parent_task)
            reward_id = str(tmp_reward_id) if tmp_reward_id else reward_id
        if reward_id:
            template_utils.init_common_reward_list(self.panel.list_reward, reward_id)
            for item in self.panel.list_reward.GetAllItem():
                if global_data.player.has_receive_reward(self.parent_task):
                    item.nd_get.setVisible(True)

        start, end = activity_utils.get_activity_open_time(self._activity_type)
        self.panel.lab_time.SetString(get_text_by_id(604006).format(start, end))
        self._refresh_btn(self.parent_task)

    def on_receive_reward_succ(self, task_id, *args):
        if task_id != self.parent_task:
            return
        for item in self.panel.list_reward.GetAllItem():
            if global_data.player.has_receive_reward(self.parent_task):
                item.nd_get.setVisible(True)

        self._refresh_btn(task_id)

    def _refresh_btn(self, task_id, *args):
        if task_id != self.parent_task:
            return
        btn = self.panel.btn_get
        func_list = confmgr.get('c_activity_config', self._activity_type, 'arrCondition', default=[])
        cur_param_index = 0
        for idx in range(len(func_list)):
            nRet, text_id = self.exec_custom_condition(idx)
            cur_param_index = idx
            if nRet >= 1:
                break

        nRet, text_id = self.exec_custom_condition(cur_param_index)
        app_channel = global_data.channel.get_app_channel()
        forbit_goto = False
        if app_channel not in ('netease', 'app_store'):
            forbit_goto = True

        @btn.unique_callback()
        def OnClick(btn, touch):
            if nRet:
                if cur_param_index == 0 and forbit_goto:
                    return
                self.exec_custom_func(cur_param_index)
            else:
                self.exec_custom_func(cur_param_index + 1)

        if forbit_goto and cur_param_index == 0:
            btn.SetText('')
        else:
            activity_utils.set_btn_text(btn, nRet, text_id)
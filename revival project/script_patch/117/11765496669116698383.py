# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityDailyBenefit.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase

class ActivityDailyBenefit(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityDailyBenefit, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self._task_refresh_reward_cb = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        from logic.gutils import task_utils
        from logic.gcommon.common_utils.local_text import get_text_by_id
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            print('[ERROR] activity [%s] task [%s] has no chidren task' % (activity_type, conf['cTask']))
            return
        parent_task = task_list[0]
        children_task = task_utils.get_children_task(parent_task)
        task_count = len(children_task)
        for i in range(2):
            widget_name = 'nd_reward_%d' % (i + 1)
            if not hasattr(self.panel, widget_name):
                continue
            reward_widget = getattr(self.panel, widget_name)
            if i > task_count - 1:
                reward_widget.setVisible(False)
                continue
            reward_widget.setVisible(True)
            child_task = children_task[i]

            def refresh_reward(task_id, index=i):
                _reward_widget = getattr(self.panel, 'nd_reward_%d' % (index + 1))

                @_reward_widget.btn_get.unique_callback()
                def OnClick(btn, touch):
                    self.exec_custom_func(index)

                nRet, text_id = self.exec_custom_condition(index)
                activity_utils.set_btn_text(_reward_widget.btn_get, nRet, text_id)
                total_times = task_utils.get_total_prog(task_id)
                left_times = total_times - global_data.player.get_task_prog(task_id)
                _reward_widget.lab_times.SetString(get_text_by_id(606034, (left_times, total_times)))

            refresh_reward(child_task)
            self._task_refresh_reward_cb[child_task] = refresh_reward

    def _on_update_reward(self, task_id):
        func = self._task_refresh_reward_cb.get(str(task_id), lambda _: 0)
        func(task_id)
        global_data.player.read_activity_list(self._activity_type)
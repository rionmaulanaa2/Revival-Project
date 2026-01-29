# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPreRegister.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name

class ActivityPreRegister(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityPreRegister, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        self._task_refresh_reward_cb = {}
        self._sub_task_received = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            print('[ERROR] activity [%s] task [%s] has no chidren task' % (activity_type, conf['cTask']))
            return
        parent_task = task_list[0]

        @self.panel.nd_content.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_all_task_reward(parent_task)

        self.init_reward_widget(parent_task)
        self.refresh_btn()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop1')
        self.panel.PlayAnimation('loop2')

    def refresh_btn(self):
        enable = False
        for task_id, received in six.iteritems(self._sub_task_received):
            if not received:
                enable = True
                break

        self.panel.nd_content.btn_get.SetEnable(enable)
        if not enable:
            global_data.player.read_activity_list(self._activity_type)

    def init_reward_widget(self, parent_task):
        children_task = task_utils.get_children_task(parent_task)
        task_count = len(children_task)
        for i in range(task_count - 1):
            reward_widget = getattr(self.panel, 'nd_reward_%d' % (i + 1))
            if i > task_count - 1:
                reward_widget.setVisible(False)
                continue
            reward_widget.setVisible(True)
            child_task = children_task[i]
            reward_id = str(task_utils.get_task_reward(child_task))
            reward_list = confmgr.get('common_reward_data', reward_id, 'reward_list', default=[])
            if len(reward_list) <= 0:
                print('[ERROR] activity [%s] child task [%s] reward_id [%s] has no reward_list' % (self._activity_type, child_task, reward_id))
                continue
            reward_cnt = len(reward_list)
            for reward_idx in range(reward_cnt):
                reward_info = reward_list[reward_idx]
                item_no, item_num = reward_info[0], reward_info[1]
                nd_item = getattr(reward_widget, 'nd_item_%d' % (reward_idx + 1))
                if not nd_item:
                    continue
                template_utils.init_tempate_reward(nd_item.temp_reward, item_no, item_num=item_num, show_tips=True)
                nd_item.lab_reward.SetString(get_lobby_item_name(item_no))
                nd_item.temp_reward.btn_choose.ClearAllFrames()

            self._refresh_common_reward(child_task, i)
            self._task_refresh_reward_cb[child_task] = lambda task_id, index=i: self._refresh_common_reward(task_id, index)

        mecha_reward_task = children_task[-1]
        self._refresh_mecha_reward(mecha_reward_task)
        self._task_refresh_reward_cb[children_task[-1]] = lambda mecha_reward_task: self._refresh_mecha_reward(mecha_reward_task)

    def _refresh_mecha_reward(self, task_id):
        is_finished = global_data.player.is_task_finished(task_id)
        has_unreceived = global_data.player.has_unreceived_task_reward(task_id)
        has_received = is_finished and not has_unreceived
        _reward_widget = getattr(self.panel, 'nd_reward_mech')
        if not _reward_widget:
            return
        self._sub_task_received[task_id] = has_received
        _reward_widget.img_recieved.setVisible(has_received)
        if has_received:
            path = 'gui/ui_res_2/activity/activity_new_domestic/pre_reg/'
            _reward_widget.img_item.SetDisplayFrameByPath('', path + 'pnl_mech_1.png')
            _reward_widget.img_light.SetDisplayFrameByPath('', path + 'img_light_b.png')

    def _refresh_common_reward(self, task_id, index):
        is_finished = global_data.player.is_task_finished(task_id)
        has_unreceived = global_data.player.has_unreceived_task_reward(task_id)
        _reward_widget = getattr(self.panel, 'nd_reward_%d' % (index + 1))
        if not _reward_widget:
            return
        has_received = is_finished and not has_unreceived
        self._sub_task_received[task_id] = has_received
        _reward_widget.nd_recieved.setVisible(has_received)
        if has_received:
            path = 'gui/ui_res_2/activity/activity_new_domestic/pre_reg/'
            _reward_widget.img_reward_bg.SetDisplayFrameByPath('', path + 'pnl_item_1.png')
            _reward_widget.nd_item_1.lab_reward.SetColor(3751577)
            _reward_widget.nd_item_2.lab_reward.SetColor(3751577)
            _reward_widget.nd_num.img_light.SetDisplayFrameByPath('', path + 'img_light_b.png')

    def _on_update_reward(self, task_id):
        func = self._task_refresh_reward_cb.get(str(task_id), lambda _: 0)
        func(task_id)
        self.refresh_btn()
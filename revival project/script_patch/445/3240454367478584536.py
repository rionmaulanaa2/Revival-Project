# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmCollect.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils
from logic.gcommon import time_utility
from logic.gutils import activity_utils
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI

class ActivityGranbelmCollect(ActivityTemplate):
    GLOBAL_EVENT = {'receive_task_reward_succ_event': 'on_task_updated'
       }
    ITEM_IMG_CFG = {201801441: [
                 'img_mech_get', 'show_mech'],
       201001543: [
                 'img_mila_get', 'show_mila'],
       201001644: [
                 'img_lori_get', 'show_lori']
       }

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmCollect, self).__init__(dlg, activity_type)
        self.on_init_panel()
        self.init_ui_event()
        self.on_task_updated(self.collect_task_id)

    def on_init_panel(self):
        self.panel.RecordAnimationNodeState('open')
        self.panel.RecordAnimationNodeState('get_tips')
        self.panel.RecordAnimationNodeState('get_tips_arrow')
        start_str, end_str = activity_utils.get_activity_open_time(self._activity_type)
        if start_str and end_str:
            self.panel.lab_time.SetString('{0} - {1}'.format(start_str, end_str))
        self.panel.PlayAnimation('loop_button')
        self.panel.PlayAnimation('loop_gear')
        collections = global_data.player.get_task_content(self.collect_task_id, 'collections', [])
        for item_no, cfg in six.iteritems(self.ITEM_IMG_CFG):
            get_nd = getattr(self.panel.nd_skin, cfg[0])
            if get_nd:
                if item_no in collections:
                    get_nd.setVisible(True)
                else:
                    get_nd.setVisible(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_task_updated
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        super(ActivityGranbelmCollect, self).init_parameters()
        self.collect_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default=None)
        self.old_collections = set(global_data.player.get_task_content(self.collect_task_id, 'collections', []))
        return

    def init_ui_event(self):

        @self.panel.btn_box.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if player.has_unreceived_task_reward(self.collect_task_id):
                self.panel.StopAnimation('get_tips')
                self.panel.StopAnimation('get_tips_arrow')
                self.panel.RecoverAnimationNodeState('get_tips')
                self.panel.RecoverAnimationNodeState('get_tips_arrow')
                self.panel.PlayAnimation('open')
                player.receive_task_reward(self.collect_task_id)
            elif not player.has_receive_reward(self.collect_task_id):
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                reward_id = task_utils.get_task_reward(self.collect_task_id)
                reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                global_data.emgr.show_reward_preview_event.emit(reward_list, wpos)

    def on_task_updated(self, task_id, *args):
        if task_id != self.collect_task_id:
            return
        self.update_skin()
        self.update_box()
        self.update_btn()

    def update_skin(self):
        collections = set(global_data.player.get_task_content(self.collect_task_id, 'collections', []))
        new_get = collections - self.old_collections
        for item_no in new_get:
            if item_no not in self.ITEM_IMG_CFG:
                continue
            cfg = self.ITEM_IMG_CFG[item_no]
            get_nd = getattr(self.panel.nd_skin, cfg[0])
            anim_name = cfg[1]
            if get_nd:
                if item_no in collections:
                    self.panel.PlayAnimation(anim_name)
                else:
                    self.panel.StopAnimation(anim_name)

        self.old_collections = collections

    def update_box(self):
        player = global_data.player
        if not player:
            return
        nd_box = self.panel.nd_box
        if player.has_receive_reward(self.collect_task_id):
            nd_box.btn_box.setVisible(False)
            nd_box.img_box_get.setVisible(True)
            self.panel.StopAnimation('open')
            self.panel.RecoverAnimationNodeState('open')
            self.panel.PlayAnimation('loop_open')
        else:
            nd_box.btn_box.setVisible(True)
            nd_box.img_box_get.setVisible(False)
            if player.has_unreceived_task_reward(self.collect_task_id):
                self.panel.PlayAnimation('get_tips')
                self.panel.PlayAnimation('get_tips_arrow')

    def update_btn(self):
        cur_param_index = 0
        activity_type = self._activity_type
        func_list = confmgr.get('c_activity_config', activity_type, 'arrCondition', default=[])
        nRet = 0
        text_id = 0
        for idx in range(len(func_list)):
            nRet, text_id = self.exec_custom_condition(idx)
            cur_param_index = idx
            if nRet >= 1:
                break

        btn = self.panel.temp_go.btn_major

        @btn.unique_callback()
        def OnClick(btn, touch):
            if nRet > 0:
                self.exec_custom_func(cur_param_index)
            else:
                self.exec_custom_func(cur_param_index + 1)

        prog = global_data.player.get_task_prog(self.collect_task_id)
        total_prog = task_utils.get_total_prog(self.collect_task_id)
        btn.SetText(get_text_by_id(text_id).format(prog, total_prog))
        global_data.player.read_activity_list(self._activity_type)
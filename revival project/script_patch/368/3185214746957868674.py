# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewComer.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import activity_utils
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_reward
from logic.comsys.lobby import LobbyMatchWidget
from logic.comsys.lobby.MatchMode import MatchMode

class ActivityNewComer(ActivityBase):

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
        self.children_task_list = task_utils.get_children_task(self.parent_task)
        self.btn_list = {}

    def init_widget(self):
        list_task = self.panel.list_task
        list_task.DeleteAllSubItem()
        for index, task_id in enumerate(self.children_task_list):
            reward_id = task_utils.get_task_reward(task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if reward_list:
                item_no = reward_list[0][0]
                num = reward_list[0][1]
                item = list_task.AddTemplateItem()
                if index == len(self.children_task_list) - 1:
                    item.bar_task.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202307/newcomer_welfare/bar_newcomer_welfare_task_3.png')
                else:
                    item.bar_task.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202307/newcomer_welfare/bar_newcomer_welfare_task_2.png')
                item.lab_task.SetString(task_utils.get_task_name(task_id))
                init_tempate_reward(item.temp_item, item_no, num, show_tips=True)
                task_prog = global_data.player.get_task_prog(task_id)
                total_prog = task_utils.get_total_prog(task_id)
                item.lab_prog.SetString('%d/%d' % (task_prog, total_prog))
                btn_click = item.btn_click
                self.btn_list[task_id] = btn_click

                @btn_click.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    self._on_task_click(task_id)

        self._update_btn_state()

    def _on_task_click(self, task_id):
        if not global_data.player:
            return
        else:
            if global_data.player.is_task_finished(task_id):
                if not global_data.player.has_receive_reward(task_id):
                    global_data.player.receive_tasks_reward([task_id])
            else:
                _, sel_battle_type, sel_match_mode, sel_play_type = LobbyMatchWidget.get_battle_infos()
                MatchMode(None, sel_play_type, sel_battle_type, sel_match_mode)
                global_data.ui_mgr.close_ui('ActivityCenterMainUI')
            return

    def _update_btn_state(self):
        for task_id, btn in self.btn_list.items():
            if global_data.player and global_data.player.is_task_finished(task_id):
                if global_data.player and global_data.player.has_receive_reward(task_id):
                    btn.SetEnable(False)
                    btn.SetText(80866)
                else:
                    btn.SetEnable(True)
                    btn.SetText(910007)
            else:
                btn.SetEnable(True)
                btn.SetText(80284)

    def init_event(self):

        @self.panel.btn_show.unique_callback()
        def OnClick(btn, touch):
            mecha_task_id = self.children_task_list[2]
            reward_id = task_utils.get_task_reward(mecha_task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_id, _ = reward_list[0]
            ui = global_data.ui_mgr.show_ui('MultiRewardPreview', 'logic.comsys.reward')
            ui and ui.set_item_id(item_id)

    def on_received_task_reward(self, task_id):
        if self.parent_task == task_id or task_id in self.children_task_list:
            self._update_btn_state()
            global_data.player.read_activity_list(self._activity_type)

    def on_finalize_panel(self):
        self.parent_task = None
        self.children_task_list = None
        self.btn_list = None
        self.process_event(False)
        return
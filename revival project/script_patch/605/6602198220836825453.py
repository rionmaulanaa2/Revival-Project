# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityUnlockByTimeTask.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_INACTIVE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
import cc

class ActivityUnlockByTimeTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityUnlockByTimeTask, self).__init__(dlg, activity_type)
        self.conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = self.conf.get('cUiData', {})
        self.task_list = task_utils.get_children_task(self.conf['cTask'])

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        act_name_id = self.conf.get('cNameTextID', '')
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(self.conf.get('cDescTextID', '')))
        btn_question = self.panel.btn_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(self.conf.get('cRuleTextID', '')))
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
        if self.panel.HasAnimation('loop'):
            self.panel.PlayAnimation('loop')

    def show_list(self):
        if not global_data.player:
            return
        if self.panel.lab_tips_time:
            self._timer_cb[0] = lambda : self.refresh_time(self.conf['cTask'])
            self.refresh_time(self.conf['cTask'])
        sub_act_list = self.panel.act_list
        sub_act_list.DeleteAllSubItem()
        sub_act_list.SetInitCount(len(self.task_list))
        ui_data = self.conf.get('cUiData', {})
        for i, task_id in enumerate(self.task_list):
            item_widget = sub_act_list.GetItem(i).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            if 'lab_name_color' in ui_data:
                color = int(ui_data['lab_name_color'])
                item_widget.lab_name.SetColor(color)
            if 'lab_num_color' in ui_data:
                color = int(ui_data['lab_num_color'])
                item_widget.lab_num.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        player = global_data.player
        if not player:
            return
        else:
            sub_act_list = self.panel.act_list
            for i, task_id in enumerate(self.task_list):
                ui_item = sub_act_list.GetItem(i)
                item_widget = ui_item.temp_common
                total_times = task_utils.get_total_prog(task_id)
                cur_times = global_data.player.get_task_prog(task_id)
                self._set_item_widget_lab_num(item_widget, total_times, cur_times)
                btn = item_widget.temp_btn_get.btn_common
                item_widget.nd_get.setVisible(False)

                @btn.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    if not activity_utils.is_activity_in_limit_time(self._activity_type):
                        return
                    _total_times = task_utils.get_total_prog(task_id)
                    _cur_times = global_data.player.get_task_prog(task_id)
                    jump_conf = task_utils.get_jump_conf(task_id)
                    if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                        item_utils.exec_jump_to_ui_info(jump_conf)
                    else:
                        global_data.player.receive_task_reward(task_id)
                        btn.SetText(80866)
                        btn.SetEnable(False)

                btn_status = None
                extra_args = {}
                if not task_utils.is_task_open(task_id):
                    btn_status = BTN_ST_ONGOING
                    extra_args['btn_text'] = get_text_by_id(611189).format(task_utils.get_task_start_time_str(task_id, format='%m.%d'))
                else:
                    status = player.get_task_reward_status(task_id)
                    if status == ITEM_RECEIVED:
                        btn_status = BTN_ST_RECEIVED
                    elif status == ITEM_UNGAIN:
                        btn_status = BTN_ST_ONGOING
                    elif status == ITEM_UNRECEIVED:
                        btn_status = BTN_ST_CAN_RECEIVE
                update_task_list_btn(item_widget.temp_btn_get, btn_status, extra_args)

            return

    def refresh_time(self, parent_task):
        if not self.panel or not self.panel.lab_tips_time:
            return
        task_left_time = task_utils.get_raw_left_open_time(self.conf['cTask'])
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_tips_time.SetString(get_readable_time_day_hour_minitue(task_left_time))
            else:
                self.panel.lab_tips_time.SetString(get_readable_time(task_left_time))
        else:
            close_left_time = 0
            self.panel.lab_tips_time.SetString(get_readable_time(close_left_time))

    def _init_get_all(self):
        if not self.panel.temp_get_all:
            return
        task_num = len(self._get_all_receivable_tasks())
        if task_num >= 1:
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_tasks_reward(self.conf['cTask'])

        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

    def _get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self.task_list:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task
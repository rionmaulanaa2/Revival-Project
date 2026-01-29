# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmCharge.py
from __future__ import absolute_import
import six
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
import logic.gcommon.const as gconst
import logic.gcommon.time_utility as tutil
from cocosui import cc, ccui, ccs

class ActivityGranbelmCharge(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmCharge, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            log_error('[ERROR] activity [%s] task has no children task', activity_type)
            return
        else:
            self._parent_task_id = task_list[0]
            children_task_list = task_utils.get_children_task(self._parent_task_id)
            arg = task_utils.get_task_arg(self._parent_task_id)
            if not children_task_list or not arg:
                log_error('[ERROR] activity [%s] children_task_list empty or arg empty.', activity_type)
                return
            children_task_list = children_task_list[:-2]
            self._charge_task_list = children_task_list[:len(children_task_list) / 2]
            self._consume_task_list = children_task_list[len(children_task_list) / 2:]
            self._charge_holder_task_id = arg.get('charge_hold_task', None)
            self._consume_holder_task_id = arg.get('consume_hold_task', None)
            if not self._charge_holder_task_id or not self._consume_holder_task_id:
                log_error('[ERROR] activity [%s] has no charge_holder_task_id or consume_holder_task_id.', activity_type)
                return
            self._children_task_2_reward_ui_item = {}
            self._children_task_2_progress_ui_item = {}
            return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def on_init_panel(self):
        self.panel.StopAnimation('show')
        self.panel.RecoverAnimationNodeState('show')
        self.panel.PlayAnimation('show')
        self._children_task_2_reward_ui_item = {}
        for i, task_id in enumerate(self._charge_task_list):
            reward_node = getattr(self.panel, 'temp_charge_%d' % (i + 1))
            if reward_node:
                self._children_task_2_reward_ui_item[task_id] = reward_node
            progress_node = getattr(self.panel, 'progress_charge_%d' % (i + 1))
            if progress_node:
                self._children_task_2_progress_ui_item[task_id] = progress_node

        for i, task_id in enumerate(self._consume_task_list):
            reward_node = getattr(self.panel, 'temp_consume_%d' % (i + 1))
            if reward_node:
                self._children_task_2_reward_ui_item[task_id] = reward_node
            progress_node = getattr(self.panel, 'progress_consume_%d' % (i + 1))
            if progress_node:
                self._children_task_2_progress_ui_item[task_id] = progress_node

        self._children_task_2_reward_ui_item[self._parent_task_id] = self.panel.temp_reward_big
        self._update_current_charge_ui()
        self._update_current_consume_ui()
        for task_id in six.iterkeys(self._children_task_2_reward_ui_item):
            self._update_task_ui(task_id)

        reward_list = self._get_task_reward_list(self._parent_task_id)
        if reward_list:
            first_reward_info = reward_list[0]
            item_no, item_num = first_reward_info[0], first_reward_info[1]
            self.panel.lab_name.SetString(item_utils.get_lobby_item_name(item_no))
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_date = tutil.get_date_str('%Y.%m.%d', conf.get('cBeginTime', 0))
        finish_date = tutil.get_date_str('%Y.%m.%d', conf.get('cEndTime', 0))
        self.panel.lab_time.SetString(get_text_by_id(604006).format(start_date, finish_date))

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(conf.get('cNameTextID', '')), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn.GetPosition()
            wpos = btn.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def _on_update_task_progress(self, task_id):
        global_data.player.read_activity_list(self._activity_type)
        if task_id == self._consume_holder_task_id:
            self._update_current_consume_ui()
        elif task_id == self._charge_holder_task_id:
            self._update_current_charge_ui()
        else:
            self._update_task_ui(task_id)

    def _calc_finished_tasks(self):
        charge_task_finished, consume_task_finished = [], []
        for task_id in self._charge_task_list:
            if global_data.player.is_task_finished(task_id):
                charge_task_finished.append(task_id)

        for task_id in self._consume_task_list:
            if global_data.player.is_task_finished(task_id):
                consume_task_finished.append(task_id)

        return (
         charge_task_finished, consume_task_finished)

    def _update_current_charge_ui(self):
        total_charge = global_data.player.get_task_prog(self._charge_holder_task_id)
        if self.panel.temp_charge.temp_price.GetItemCount() <= 0:
            self.panel.temp_charge.temp_price.AddTemplateItem()
        temp_price_node = self.panel.temp_charge.temp_price.GetItem(0)
        temp_price_node.lab_price.SetString(str(total_charge))

    def _update_current_consume_ui(self):
        total_consume = global_data.player.get_task_prog(self._consume_holder_task_id)
        if self.panel.temp_consume.temp_price.GetItemCount() <= 0:
            self.panel.temp_consume.temp_price.AddTemplateItem()
        temp_price_node = self.panel.temp_consume.temp_price.GetItem(0)
        temp_price_node.lab_price.SetString(str(total_consume))

    def _get_task_reward_list(self, task_id):
        reward_id = str(task_utils.get_task_reward(task_id))
        reward_list = confmgr.get('common_reward_data', reward_id, 'reward_list', default=[])
        if len(reward_list) <= 0:
            log_error('[ERROR] _get_task_reward_list task [%s] reward_id [%s] has no rewards', task_id, reward_id)
            return []
        return reward_list

    def _update_task_ui(self, task_id):
        reward_widget = self._children_task_2_reward_ui_item.get(task_id)
        if not reward_widget:
            return
        progress_node = self._children_task_2_progress_ui_item.get(task_id)
        if progress_node:
            if global_data.player.is_task_finished(task_id):
                percent = 100 if 1 else 0
                if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                    progress_node.SetPercentage(percent)
                else:
                    progress_node.SetPercent(percent)
            reward_list = self._get_task_reward_list(task_id)
            return reward_list or None
        first_reward_info = reward_list[0]
        item_no, item_num = first_reward_info[0], first_reward_info[1]
        template_utils.init_tempate_mall_i_item(reward_widget.temp_reward, item_no, item_num=item_num, show_tips=True)
        receive_state = global_data.player.get_task_reward_status(task_id)
        btn = reward_widget.temp_reward.btn_choose
        if receive_state == ITEM_UNGAIN:
            reward_widget.temp_reward.nd_lock.setVisible(True)
            reward_widget.temp_reward.nd_get_tips.setVisible(False)
            reward_widget.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202004/granbelm_charge/granbelm_charge_item_dec_gray.png')
            reward_widget.StopAnimation('get_tips')
            reward_widget.RecoverAnimationNodeState('get_tips')
        elif receive_state == ITEM_UNRECEIVED:
            reward_widget.temp_reward.nd_lock.setVisible(False)
            reward_widget.temp_reward.nd_get_tips.setVisible(True)
            reward_widget.PlayAnimation('get_tips')
            reward_widget.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202004/granbelm_charge/granbelm_charge_item_dec_red.png')
            btn.BindMethod('OnClick', lambda b, t, tid=task_id: global_data.player.receive_task_reward(tid))
        elif receive_state == ITEM_RECEIVED:
            reward_widget.temp_reward.nd_get.setVisible(True)
            reward_widget.temp_reward.nd_lock.setVisible(False)
            reward_widget.temp_reward.nd_get_tips.setVisible(False)
            reward_widget.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202004/granbelm_charge/granbelm_charge_item_dec_red.png')
            reward_widget.StopAnimation('get_tips')
            reward_widget.RecoverAnimationNodeState('get_tips')
        if task_id != self._parent_task_id:
            total_num = task_utils.get_total_prog(task_id)
            reward_widget.lab_num.SetString(str(total_num))
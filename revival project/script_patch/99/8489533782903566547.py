# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonGlobalKill.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_tempate_reward
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils.activity_utils import get_child_achieves_from_parent, get_left_time
from logic.gcommon.time_utility import get_simply_readable_time
from common.utils.timer import CLOCK
from logic.gutils import task_utils
from common.cfg import confmgr
import six_ex

class ActivityCommonGlobalKill(ActivityBase):

    def on_init_panel(self):
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_update_global_stat': self.update_tick_goal_num,
           'message_update_global_reward_receive': self.on_received_global_archive_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_params(self):
        activity_type = self._activity_type
        self._conf = confmgr.get('c_activity_config', activity_type)
        cUiData = self._conf.get('cUiData')
        self._global_archive_conf = confmgr.get('global_achieve_data')
        self._parent_archive_id = cUiData.get('parent_archive_id')
        child_archive_id_list = get_child_achieves_from_parent(self._parent_archive_id)
        if len(child_archive_id_list) <= 0:
            log_error('[ERROR] activity [%s] parent archive [%s] has no chidren archive' % (activity_type, parent_archive_id))
            return
        else:
            self._children_archive_id_list = child_archive_id_list
            self._reward_item_dict = {}
            self._timer = None
            self._cur_progress = 0
            return

    def init_ui(self):
        self._init_reward_list()
        self._init_time_label()
        self.update_tick_goal_num()
        self.panel.PlayAnimation('show')

    def _init_reward_list(self):
        temp_list = self.panel.temp_list
        temp_list.DeleteAllSubItem()
        temp_list.SetInitCount((len(self._children_archive_id_list) + 1) // 2)
        for index, item in enumerate(temp_list.GetAllItem()):
            if index != temp_list.GetItemCount() - 1:
                item.PlayAnimation('show_common')

        for index, archive_id in enumerate(self._children_archive_id_list):
            item_index = index // 2
            sub_item_index = index % 2
            item_widget = self.panel.temp_list.GetItem(item_index)
            if item_index != 0 and sub_item_index == 0:
                item_widget.progress_bg0.setVisible(False)
            if index == 0:
                sub_item = item_widget.nd_item0
                item_widget.progress_bg0.setVisible(True)
            elif sub_item_index == 0:
                sub_item = item_widget.nd_item0
            else:
                sub_item = item_widget.nd_item1
            is_last_reward = index == len(self._children_archive_id_list) - 1
            if is_last_reward:
                self._init_reward_item(self.panel.temp_item, archive_id)
                item_widget.nd_item1.setVisible(False)
                if len(self._children_archive_id_list) % 2:
                    item_widget.nd_item0.nd_cut.setVisible(False)
                else:
                    item_widget.nd_item0.setVisible(False)
            else:
                self._init_reward_item(sub_item.temp_item, archive_id)

        self._update_reward_state()

    def _init_reward_item(self, item, archive_id):
        reward_id = self._global_archive_conf.get(str(archive_id), {}).get('iRewardID')
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        if reward_list:
            lv_item = item.lv_item
            lv_item.DeleteAllSubItem()
            reward_item = lv_item.AddTemplateItem()
            self._reward_item_dict[archive_id] = reward_item
            item_no = reward_list[0][0]
            num = reward_list[0][1]
            cond_value = self._global_archive_conf.get(str(archive_id), {}).get('iCondValue')
            item.lab_cell_name.SetString(str(cond_value))
            init_tempate_reward(reward_item, item_no, num)

            @reward_item.btn_choose.unique_callback()
            def OnClick(btn, touch):
                if not global_data.player:
                    return
                else:
                    status = global_data.player.get_gl_reward_receive_state(archive_id)
                    if status == ITEM_UNRECEIVED:
                        global_data.player.try_get_global_achieve(archive_id)
                    else:
                        x, y = btn.GetPosition()
                        w, _ = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                    return

    def _update_reward_state(self):
        for archive_id, reward_item in six_ex.items(self._reward_item_dict):
            status = global_data.player.get_gl_reward_receive_state(archive_id) if global_data.player else ITEM_UNGAIN
            if status == ITEM_UNRECEIVED:
                reward_item.PlayAnimation('get_tips')
                reward_item.nd_get.setVisible(False)
                reward_item.nd_get_tips.setVisible(True)
            elif status == ITEM_RECEIVED:
                reward_item.StopAnimation('get_tips')
                reward_item.nd_get.setVisible(True)
                reward_item.nd_get_tips.setVisible(False)
            elif status == ITEM_UNGAIN:
                reward_item.StopAnimation('get_tips')
                reward_item.nd_get.setVisible(False)
                reward_item.nd_get_tips.setVisible(False)

    def _init_time_label(self):
        self._unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self._refresh_left_time, interval=1, mode=CLOCK)
        self._refresh_left_time()

    def _refresh_left_time(self):
        lab_tips_time = self.panel.lab_tips_time
        if not self.panel or not lab_tips_time:
            return
        left_time = get_left_time(self._activity_type)
        if left_time > 0:
            lab_tips_time.SetString(get_text_by_id(635592).format(get_simply_readable_time(left_time)))

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def init_ui_event(self):

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            self.desc_id = self._conf.get('cRuleTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(self.desc_id)))

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_pve_chapter_ui
            jump_to_pve_chapter_ui(1)

    def update_tick_goal_num(self, *args):
        if not global_data.player:
            global_stat_data = None if 1 else global_data.player.get_global_stat_data()
            if global_stat_data is None:
                return
            last_child_archive_conf = self._global_archive_conf.get(str(self._children_archive_id_list[-1]), {})
            return last_child_archive_conf or None
        else:
            archive_name = last_child_archive_conf.get('cGStatName', '')
            self._cur_progress = global_stat_data.get(str(self._parent_archive_id), {}).get(archive_name, 0)
            self.panel.lab_num.SetString(get_text_by_id(635594).format(self._cur_progress))
            max_progress = last_child_archive_conf.get('iCondValue')
            self.panel.lab_info.SetString(get_text_by_id(635595).format(max_progress))
            self._update_progress()
            return

    def _update_progress(self):
        temp_list = self.panel.temp_list
        for index, archive_id in enumerate(self._children_archive_id_list):
            item_index = index // 2
            sub_item_index = index % 2
            item_widget = temp_list.GetItem(item_index)
            if index == 0:
                progress_node = item_widget.progress_bar0
            elif sub_item_index == 0:
                front_item_widget = temp_list.GetItem(item_index - 1)
                progress_node = front_item_widget.nd_item1.nd_cut.progress_bg.progress_bar
            else:
                progress_node = item_widget.nd_item0.nd_cut.progress_bg.progress_bar
            prog = self._global_archive_conf.get(str(archive_id), {}).get('iCondValue')
            if index > 0:
                front_archive_id = self._children_archive_id_list[index - 1]
                front_prog = self._global_archive_conf.get(str(front_archive_id), {}).get('iCondValue')
            else:
                front_prog = 0
            if self._cur_progress >= prog:
                percent = 100
            elif self._cur_progress < front_prog:
                percent = 0
            else:
                percent = 100 * (1 - (prog - self._cur_progress) * 1.0 / (prog - front_prog))
            if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                progress_node.SetPercentage(percent)
            else:
                progress_node.SetPercent(percent)

    def on_received_global_archive_reward(self):
        self._update_reward_state()
        global_data.player.read_activity_list(self._activity_type)

    def on_finalize_panel(self):
        self._unregister_timer()
        self._children_archive_id_list = None
        self._reward_item_dict = None
        self.process_event(False)
        return
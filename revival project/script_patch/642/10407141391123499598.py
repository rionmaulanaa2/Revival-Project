# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityReturnTask.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from logic.gcommon.time_utility import get_readable_time
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.comsys.effect.ui_effect import set_gray
from logic.gutils import activity_utils
from cocosui import cc

class ActivityReturnTask(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityReturnTask, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)
        self.register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.safe_unregister_timer()

    def init_parameters(self):
        self._act_conf = confmgr.get('c_activity_config', self._activity_type)
        self._second_timer = None
        self._combine_task_list = self._act_conf.get('cUiData', {}).get('combine_task_list', [])
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_receive_task_reward_succ,
           'task_prog_changed': self._on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.panel.lab_tdescribe.SetString(get_text_by_id(self._act_conf.get('cDescTextID', '')))

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            parent_task_id = self._get_parent_task_id()
            if parent_task_id is None:
                return
            else:
                reward_id = task_utils.get_task_reward(parent_task_id)
                if reward_id is None:
                    return
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    log_error('reward_id is not exist in common_reward_data', reward_id)
                    return
                reward_list = reward_conf.get('reward_list', [])
                if len(reward_list) <= 0:
                    return
                item_no, item_num = reward_list[0]
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        self._refresh_panel()

    def refresh_panel(self):
        self._refresh_panel()

    def _get_parent_task_id(self):
        if 'cTask' not in self._act_conf:
            return None
        else:
            task_list = activity_utils.parse_task_list(self._act_conf['cTask'])
            if len(task_list) <= 0:
                return None
            return task_list[0]

    def _refresh_panel(self):
        act_name_id = self._act_conf['cNameTextID']
        self._second_timer_cb()
        btn_describe = self.panel.btn_describe

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(self._act_conf.get('cRuleTextID', '')))

        parent_task_id = self._get_parent_task_id()
        if parent_task_id is None:
            children_tasks = []
        else:
            children_tasks = list(task_utils.get_children_task(parent_task_id))
            idx = -1
            for task_id in self._combine_task_list:
                idx += 1
                if not global_data.player.has_receive_reward(task_id):
                    break

        for i in range(0, len(self._combine_task_list)):
            if i != idx:
                children_tasks.remove(self._combine_task_list[i])

        remove_tasks = []
        for task_id in children_tasks:
            if not task_utils.check_task_server_limit(task_id):
                remove_tasks.append(task_id)

        for rm_task_id in remove_tasks:
            children_tasks.remove(rm_task_id)

        if global_data.player.is_task_finished(parent_task_id):
            children_tasks.append(parent_task_id)
        children_tasks.sort(key=cmp_to_key(task_utils.sort_task_func))
        sub_act_list = self.panel.act_list
        offset_before_adjust = sub_act_list.GetContentOffset()
        keep_prev_offset = sub_act_list.GetItemCount() != 0
        sub_act_list.SetInitCount(len(children_tasks))
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times > 1:
                item_widget.lab_num.SetString('{0}/{1}'.format(cur_times, total_times))
            else:
                item_widget.lab_num.SetString('')
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)
            has_rewarded = global_data.player.has_receive_reward(task_id)
            if has_rewarded:
                btn.SetText(80866)
                item_widget.nd_get.setVisible(True)
                btn.setVisible(False)
            elif cur_times < total_times:
                btn.SetText(80930)
                btn.setVisible(True)
                text_id = jump_conf.get('unreach_text', '')
                if text_id:
                    btn.SetText(text_id)
                    btn.SetEnable(True)
                else:
                    btn.SetEnable(False)
            else:
                btn.SetText(80930)
                btn.setVisible(True)
                btn.SetEnable(True)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not global_data.player.has_return_task():
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

        if keep_prev_offset:
            sub_act_list.SetContentOffset(offset_before_adjust)
        else:
            sub_act_list.ScrollToTop()
        self._refresh_ultimate_part()
        return

    def _refresh_ultimate_part(self):
        parent_task_id = self._get_parent_task_id()
        if parent_task_id is None:
            return
        else:
            has_rewarded = global_data.player.has_receive_reward(parent_task_id)
            total_times = task_utils.get_total_prog(parent_task_id)
            cur_times = global_data.player.get_task_prog(parent_task_id)
            self.panel.text_allprogress.SetString(str(cur_times))
            self.panel.text_nub.SetString('/%d' % total_times)
            if has_rewarded:
                text_zi_text_id = 80866
                text_zi_color = '#DC'
                show_get_img = True
                img_role_gray = True
            else:
                text_zi_text_id = 606219
                text_zi_color = '#SW'
                show_get_img = False
                img_role_gray = False
            self.panel.text_zi.SetString(text_zi_text_id)
            self.panel.text_zi.SetColor(text_zi_color)
            self.panel.img_get.setVisible(show_get_img)
            set_gray(self.panel.img_role, img_role_gray)
            return

    def register_timer(self):
        self.safe_unregister_timer()
        from common.utils.timer import CLOCK
        self._second_timer = global_data.game_mgr.register_logic_timer(func=self._second_timer_cb, interval=1, mode=CLOCK)

    def safe_unregister_timer(self):
        if self._second_timer:
            global_data.game_mgr.unregister_logic_timer(self._second_timer)
            self._second_timer = None
        return

    def _second_timer_cb(self):
        left_time = global_data.player.get_return_task_left_time()
        self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))

    def _on_receive_task_reward_succ(self, task_id):
        global_data.player.read_activity_list(self._activity_type)
        self._refresh_panel()

    def _on_update_task_progress(self, task_changes):
        for task_change in task_changes:
            task_id = task_change.task_id
            parent_task_id = self._get_parent_task_id()
            if parent_task_id is None:
                return
            if task_id == parent_task_id:
                self._refresh_panel()
                return

        return
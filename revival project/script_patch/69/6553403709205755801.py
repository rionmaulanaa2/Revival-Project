# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySeasonStar.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils.template_utils import init_template_mall_i_lottery_prog_item
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED
from logic.gutils.activity_utils import get_left_time
from logic.gutils.template_utils import show_left_time
from logic.gutils import task_utils

class ActivitySeasonStar(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivitySeasonStar, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)

    def init_parameters(self):
        self._timer = 0
        self.cUiData = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        task_id = self.cUiData.get('task_id')
        if not task_id:
            return
        self.parent_task_id = task_id
        self.children_tasks = task_utils.get_children_task(task_id)

    def on_init_panel(self):
        super(ActivitySeasonStar, self).on_init_panel()
        self.register_timer()

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        @self.panel.temp_btn_get.btn_major.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_all_task_reward(self.parent_task_id)

        self._refresh_charge_task_progress()

    def set_activity_info(self, last_selected_activity_type, sub_widget):
        self.last_tab_name_id = confmgr.get('c_activity_config', str(last_selected_activity_type), 'iCatalogID', default='')
        self.sub_widget = sub_widget
        if not self.sub_widget:
            return
        self.sub_widget.set_show(self.get_sub_show())

    def get_sub_show(self):
        return False

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)
        self.refresh_left_time()

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def refresh_left_time(self):
        task_id = self.parent_task_id
        if self.children_tasks:
            task_id = self.children_tasks[0]
        left_time_delta = task_utils.get_left_open_time(task_id)
        if left_time_delta > 0:
            show_left_time(self.panel.lab_time_tips, left_time_delta, '')
            self.panel.lab_tips.SetString(633701)
        else:
            left_time_delta = get_left_time(self._activity_type)
            show_left_time(self.panel.lab_time_tips, left_time_delta, '')
            self.panel.lab_tips.SetString(611562)

    def on_finalize_panel(self):
        self.unregister_timer()
        self.process_event(False)
        super(ActivitySeasonStar, self).on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward,
           'task_prog_changed': self.task_prog_changed,
           'receive_task_reward_succ_event': self.receive_task_prog_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def receive_task_prog_reward(self, task_id, prog=None):
        self._refresh_charge_task_progress()
        global_data.emgr.refresh_activity_redpoint.emit()

    def task_prog_changed(self, changes):
        self._refresh_charge_task_progress()
        global_data.emgr.refresh_activity_redpoint.emit()

    def _refresh_charge_task_progress(self):
        if not self.children_tasks:
            return
        if not global_data.player:
            return
        has_receivable_tasks = False
        task_cur_prog = global_data.player.get_task_prog(self.children_tasks[-1])
        for index, task_id in enumerate(self.children_tasks):
            self._update_charge_task_ui(index, task_id)
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                has_receivable_tasks = True

        self.panel.lab_num.SetString(get_text_by_id(611473).format(task_cur_prog))
        self.panel.temp_btn_get.btn_major.SetEnable(has_receivable_tasks)

    def _update_charge_task_ui(self, index, task_id):
        if not global_data.player:
            return
        else:
            temp_item_widget = getattr(self.panel, 'temp_%d' % (index + 1))
            if not temp_item_widget:
                return
            temp_step_widget = getattr(self.panel, 'temp_step_%d' % (index + 1))
            if not temp_step_widget:
                return
            task_conf = task_utils.get_task_conf_by_id(task_id)
            reward_id = task_conf.get('reward')
            prog = task_conf.get('total_prog')
            temp_item_widget.lab_star.SetString(get_text_by_id(611463).format(num=prog))
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if not reward_list:
                return
            is_receivable = False
            show_tips = True
            status = global_data.player.get_task_reward_status(task_id)
            temp_item_widget.btn_choose.UnBindMethod('OnClick')
            has_receive = False
            if status == ITEM_RECEIVED:
                has_receive = True
            elif status == ITEM_UNRECEIVED:
                is_receivable = True
                show_tips = False
                temp_item_widget.btn_choose.BindMethod('OnClick', lambda b, t, task_id=task_id: global_data.player.receive_task_reward(task_id))
            reward_info = reward_list[0]
            item_no, item_num = reward_info[0], reward_info[1]
            show_all_num = True
            init_template_mall_i_lottery_prog_item(temp_item_widget, item_no, item_num=item_num, show_name=False, show_rare_degree=True, show_tips=show_tips, show_all_num=show_all_num, img_frame_path=None)
            temp_item_widget.item.SetColor('#DD' if has_receive else '#SW')
            temp_item_widget.nd_get.setVisible(has_receive)
            temp_item_widget.nd_get_tips.setVisible(is_receivable)
            temp_step_widget.nd_get.setVisible(is_receivable)
            temp_step_widget.btn_step.SetSelect(is_receivable)
            temp_step_widget.bar_normal and temp_step_widget.bar_normal.setVisible(not is_receivable)
            if is_receivable:
                temp_item_widget.PlayAnimation('get_tips')
            else:
                temp_item_widget.StopAnimation('get_tips')
            return
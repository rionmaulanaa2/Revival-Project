# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520Proficiency.py
from __future__ import absolute_import
import six
from six.moves import range
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
from logic.gutils import mall_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.client.const.mall_const import DARK_PRICE_COLOR, DEF_PRICE_COLOR
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.new_template_utils import init_activity_top_tab, TaskListWidget, CommonItemReward
from logic.gutils.template_utils import init_tempate_reward
from common.utils.timer import CLOCK

class Activity520Proficiency(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(Activity520Proficiency, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_widget()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)
        for w in six.itervalues(self._week_task_widget_dict):
            w.destroy()

        self._week_task_widget_dict = {}
        self._collect_prog_rewards = {}
        self._week_task_list = []
        self._all_task_set = set()
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), default={})
        ui_conf = conf.get('cUiData', {})
        self._collect_task = conf.get('cTask', None)
        self._task_list = [ str(tid) for tid in ui_conf.get('task_list', []) ]
        self._week_task_list = []
        self._all_task_set = set()
        for i, parent_task_id in enumerate(self._task_list):
            children_tasks = task_utils.get_children_task(parent_task_id)
            self._all_task_set = self._all_task_set.union(set(children_tasks))
            self._week_task_list.append(list(children_tasks))

        self.begin_time = conf.get('cBeginTime', 0)
        self.end_time = conf.get('cEndTime', 0)
        self._week_task_widget_dict = {}
        self._collect_prog_rewards = {}
        self._second_timer = None
        return

    def init_widget(self):
        tab_info = []
        for i in range(len(self._task_list)):
            tab_info.append({'text': get_text_by_id(602016, (str(i + 1),))})

        init_activity_top_tab(self.panel.list_tab, tab_info, self._onclick_week)
        for i, tab_item in enumerate(self.panel.list_tab.GetAllItem()):
            tab_item.btn_top.lab_unlock.setVisible(not self._is_week_open(i))
            tab_item.btn_top.lab_unlock.SetString(get_text_by_id(608620, (str(i + 1),)))
            tab_item.btn_top.SetText(get_text_by_id(602016, (str(i + 1),)) if self._is_week_open(i) else '')

        self._onclick_week(None, 0)
        self.panel.list_tab.GetItem(0).btn_top.SetSelect(True)
        self.panel.nd_finsh.list_item.DeleteAllSubItem()
        prog_rewards = task_utils.get_prog_rewards(self._collect_task)
        self.panel.nd_finsh.list_item.SetInitCount(len(prog_rewards))
        for i, prog_data in enumerate(prog_rewards):
            prog, reward_id = prog_data
            reward_item = self.panel.nd_finsh.list_item.GetItem(i)
            reward_item.lab_node_num.SetString(str(prog))

            def cb(_prog):
                if not global_data.player.has_receive_prog_reward(self._collect_task, _prog) and global_data.player.get_task_prog(self._collect_task) >= _prog:
                    global_data.player.receive_task_prog_reward(self._collect_task, _prog)

            self._collect_prog_rewards[prog] = CommonItemReward(reward_item.temp_item, reward_id, cb, (prog,), False)

        self.on_task_update(self._collect_task)
        self.refresh_top_red_point()

        @self.panel.temp_get_all.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            if self._check_has_unreceived_reward():
                task_list = list(self._task_list)
                task_list.append(self._collect_task)
                global_data.player.receive_tasks_reward(task_list)

        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')))
        action_list.append(cc.DelayTime.create(0.7))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)
        return

    def refresh_left_time(self):
        left_ts = self.end_time - tutil.time()
        if left_ts > 0:
            self.panel.nd_display.lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_2(left_ts)))
        else:
            self.panel.nd_display.lab_time.SetString('')
            self._timer and global_data.game_mgr.get_logic_timer().unregister(self._timer)

    def on_task_update(self, task_id, *args):
        if task_id not in self._all_task_set and task_id != self._collect_task:
            return
        global_data.emgr.refresh_activity_redpoint.emit()
        if task_id in self._all_task_set:
            self.refresh_top_red_point()
        if task_id == self._collect_task:
            prog_rewards = task_utils.get_prog_rewards(self._collect_task)
            now_prog = global_data.player.get_task_prog(self._collect_task)
            total_prog = task_utils.get_total_prog(self._collect_task)
            progress = now_prog * 1.0 / total_prog * 100
            if progress < 5:
                self.panel.nd_finsh.cut_progress.progress_bar.setVisible(False)
            else:
                self.panel.nd_finsh.cut_progress.progress_bar.setVisible(True)
                self.panel.nd_finsh.cut_progress.progress_bar.SetPercent(progress)
            self.panel.nd_finsh.lab_finish_task.SetString(get_text_by_id(608622, {'num': now_prog}))
            for i, prog_data in enumerate(prog_rewards):
                prog, reward_id = prog_data
                if prog > now_prog:
                    state = ITEM_UNGAIN
                elif global_data.player.has_receive_prog_reward(self._collect_task, prog):
                    state = ITEM_RECEIVED
                else:
                    state = ITEM_UNRECEIVED
                self._collect_prog_rewards[prog].update_state(state)

        if self._check_has_unreceived_reward():
            self.panel.pnl_get_all.setVisible(True)
            self.panel.temp_get_all.setVisible(True)
        else:
            self.panel.pnl_get_all.setVisible(False)
            self.panel.temp_get_all.setVisible(False)

    def _check_has_unreceived_reward(self):
        for task_id in self._task_list:
            if global_data.player.has_unreceived_task_reward(task_id):
                return True

        return task_utils.has_unreceived_prog_reward(self._collect_task)

    def _get_week_task_content(self, week):
        if week == 0:
            return self.panel.task_content.list_task
        nd_name = 'list_task_%s' % week
        if not getattr(self.panel.task_content, nd_name):
            temp_content = self.panel.task_content.list_task
            pos = temp_content.GetPosition()
            week_content = global_data.uisystem.load_template_create('activity/activity_202105/520/i_activity_proficiency_list')
            self.panel.task_content.AddChild(nd_name, week_content)
            week_content.ResizeAndPosition()
            week_content.SetPosition(*pos)
            week_content.setAnchorPoint(temp_content.getAnchorPoint())
        return getattr(self.panel.task_content, nd_name)

    def _onclick_week(self, tab_item, week):
        if not self._is_week_open(week):
            left_time = self.begin_time + week * tutil.ONE_WEEK_SECONDS - tutil.time()
            global_data.game_mgr.show_tip(get_text_by_id(81360).format(tutil.get_readable_time_2(left_time)))
            return False
        if week not in self._week_task_widget_dict:
            children_tasks = self._week_task_list[week]
            task_list_widget = TaskListWidget(self._get_week_task_content(week), children_tasks, self._check_task_open)
            self._week_task_widget_dict[week] = task_list_widget
        for i, wiget in six.iteritems(self._week_task_widget_dict):
            if i != week:
                wiget.setVisible(False)
            else:
                wiget.setVisible(True)

        return True

    def _check_task_open(self, task_id):
        parent_task_id = task_utils.get_parent_task(task_id)
        if parent_task_id not in self._task_list:
            return False
        return self._is_week_open(self._task_list.index(parent_task_id))

    def _is_week_open(self, week):
        return tutil.time() - self.begin_time >= week * tutil.ONE_WEEK_SECONDS

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.on_task_update,
           'receive_task_reward_succ_event': self.on_task_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_top_red_point(self, *args):
        for week, parent_task_id in enumerate(self._task_list):
            if not self._is_week_open(week):
                continue
            if global_data.player.has_unreceived_task_reward(parent_task_id):
                self.panel.list_tab.GetItem(week).img_red.setVisible(True)
            else:
                self.panel.list_tab.GetItem(week).img_red.setVisible(False)

    def refresh_panel(self):
        pass

    def on_init_panel(self):
        pass
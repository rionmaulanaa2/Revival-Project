# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/PVEWeekTaskWidget.py
from __future__ import absolute_import
from .CommonTaskWidget import CommonTaskWidget
from logic.gutils.template_utils import init_tempate_mall_i_item, init_common_reward_list
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.common_const.pve_const import PVE_WEEK_TASK_CACHE_KEY
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import exec_jump_to_ui_info
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from logic.gutils import task_utils
from common.cfg import confmgr
import six_ex

class PVEWeekTaskWidget(CommonTaskWidget):

    def __init__(self, parent, panel, task_type):
        super(PVEWeekTaskWidget, self).__init__(parent, panel, task_type, False)
        temp_content = getattr(self.parent.nd_cut, 'temp_content')
        pos = temp_content.GetPosition()
        self.nd_content = global_data.uisystem.load_template_create('task/i_task_pve_main')
        self.panel.nd_cut.AddChild('pve_week_task', self.nd_content)
        self.nd_content.ResizeAndPosition()
        self.nd_content.SetPosition(*pos)
        self.nd_content.setAnchorPoint(temp_content.getAnchorPoint())
        self._timer = None
        self._remain_time = None
        self._common_reward_data = confmgr.get('common_reward_data')
        self._reward_item_list = {}
        self._pve_week_task_reward_id = None
        self._random_task_list = []
        self._task_item_list = {}
        return

    def init_widget(self, need_hide=True):
        super(PVEWeekTaskWidget, self).init_widget(need_hide)
        self._init_ui_event()
        self._init_title_widget()
        self._init_reward_widget()
        self._init_task_widget()
        self._init_get_all_btn()
        self._write_local_data()

    def _init_ui_event(self):

        @self.nd_content.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(709118, 709119)

    def init_event(self):
        super(PVEWeekTaskWidget, self).init_event()
        global_data.emgr.task_prog_changed += self.on_task_prog_changed
        global_data.emgr.receive_task_prog_reward_succ_event += self.on_receive_task_prog_reward_succ
        global_data.emgr.receive_task_reward_succ_event += self.on_receive_task_reward_succ_event

    def on_task_prog_changed(self, changes):
        for change in changes:
            task_id = change.task_id
            if task_id == self._pve_week_task_reward_id:
                self._update_reward_widget()
            elif task_id in self._random_task_list:
                self._update_task_widget()

        self._update_get_all_btn()

    def on_receive_task_prog_reward_succ(self, task_id, prog):
        if task_id == self._pve_week_task_reward_id:
            self._update_reward_widget()
            self._update_get_all_btn()

    def on_receive_task_reward_succ_event(self, task_id):
        if task_id in self._random_task_list:
            self._update_task_widget()
            self._update_get_all_btn()

    def _init_title_widget(self):
        self._remain_time = int(time_utility.get_next_utc8_monday_time() + 5 * time_utility.ONE_HOUR_SECONS) % time_utility.ONE_WEEK_SECONDS
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_title_timer, interval=1, mode=CLOCK)
        self._update_title_timer()

    def _update_title_timer(self):
        self._remain_time = self._remain_time - 1
        if self._remain_time < 0:
            self._remain_time = time_utility.ONE_WEEK_SECONDS
            self._init_reward_widget()
            self._init_task_widget()
            self._update_get_all_btn()
        time_str = time_utility.get_readable_time(self._remain_time)
        self.nd_content.lab_tips_time.SetString(get_text_by_id(633922).format(time_str))

    def _init_reward_widget(self):
        self._pve_week_task_reward_id = task_utils.get_pve_reward_task_id()
        if not self._pve_week_task_reward_id:
            return
        task_conf = task_utils.get_task_conf_by_id(self._pve_week_task_reward_id)
        prog_rewards = task_conf.get('prog_rewards', [])
        list_reward = self.nd_content.list_reward
        for index, prog_info in enumerate(prog_rewards):
            prog, reward_id = prog_info
            reward_list = self._common_reward_data.get(str(reward_id), {}).get('reward_list')
            item = list_reward.GetItem(index)
            self._reward_item_list[prog] = item
            item.lab_num.setString(str(prog))
            item_id = reward_list[0][0]
            item_num = reward_list[0][1]
            temp_item = item.temp_item
            init_tempate_mall_i_item(temp_item, item_id, item_num, show_tips=False)

            @temp_item.btn_choose.unique_callback()
            def OnClick(btn, touch, prog=prog, item_id=item_id, item_num=item_num):
                if not global_data.player:
                    return
                else:
                    cur_prog = global_data.player.get_task_prog(self._pve_week_task_reward_id)
                    if not global_data.player.has_receive_prog_reward(self._pve_week_task_reward_id, prog) and cur_prog >= prog:
                        global_data.player.receive_task_prog_reward(self._pve_week_task_reward_id, prog)
                    else:
                        x, y = btn.GetPosition()
                        w, _ = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        extra_info = {'show_jump': True}
                        global_data.emgr.show_item_desc_ui_event.emit(item_id, None, wpos, extra_info=extra_info, item_num=item_num)
                    return

        self._update_reward_widget()

    def _update_reward_widget(self):
        cur_prog = global_data.player.get_task_prog(self._pve_week_task_reward_id)
        self.nd_content.lab_score.SetString(str(cur_prog))
        last_prog = 0
        for prog, item in six_ex.items(self._reward_item_list):
            temp_item = item.temp_item
            if not global_data.player.has_receive_prog_reward(self._pve_week_task_reward_id, prog):
                if cur_prog >= prog:
                    temp_item.nd_get.setVisible(False)
                    temp_item.nd_get_tips.setVisible(True)
                    temp_item.PlayAnimation('get_tips')
                else:
                    temp_item.nd_get.setVisible(False)
                    temp_item.nd_get_tips.setVisible(False)
                    temp_item.StopAnimation('get_tips')
            else:
                temp_item.nd_get.setVisible(True)
                temp_item.nd_get_tips.setVisible(False)
                temp_item.StopAnimation('get_tips')
            if cur_prog >= prog:
                item.bar_prog.prog.SetPercentage(100)
            else:
                percentage = float(cur_prog - last_prog) / float(prog - last_prog) * 100
                item.bar_prog.prog.SetPercentage(percentage)
            last_prog = prog

    def _init_task_widget(self):

        def sort_function(task_id):
            status, _, _, _ = task_utils.get_task_status_info(task_id)
            if status == ITEM_UNGAIN:
                return 1
            else:
                if status == ITEM_UNRECEIVED:
                    return 2
                return 0

        self._task_item_list = {}
        self._random_task_parent_list = task_utils.get_pve_random_parent_task_list()
        self._random_task_list = self._get_random_task()
        self._random_task_list.sort(key=lambda x: sort_function(x), reverse=True)
        list_task = self.nd_content.list_task
        list_task.RecycleAllItem()
        for random_task_id in self._random_task_list:
            item = list_task.AddTemplateItem()
            self._task_item_list[random_task_id] = item
            reward_id = task_utils.get_task_reward(random_task_id)
            reward_list = self._common_reward_data.get(str(reward_id), 'reward_list')
            if not reward_list:
                continue
            item.lab_name.SetString(task_utils.get_task_name(random_task_id))
            init_common_reward_list(item.list_reward, reward_id)

            @item.btn_go.unique_callback()
            def OnClick(btn, touch, random_task_id=random_task_id):
                global_data.ui_mgr.close_ui('TaskMainUI')
                jump_conf = task_utils.get_jump_conf(random_task_id)
                exec_jump_to_ui_info(jump_conf)

            @item.btn_get.unique_callback()
            def OnClick(btn, touch, random_task_id=random_task_id, reward_id=reward_id):
                if not global_data.player:
                    return
                else:
                    is_prog_task = True if reward_id is None else False
                    if is_prog_task:
                        _, _, _, total_prog = task_utils.get_task_status_info(random_task_id)
                        global_data.player.receive_task_prog_reward(random_task_id, total_prog)
                    else:
                        global_data.player.receive_task_reward(random_task_id)
                    return

        self._update_task_widget()

    def _update_task_widget(self):
        if not global_data.player:
            return
        for random_task_id, item in six_ex.items(self._task_item_list):
            status, cur_prog, _, total_prog = task_utils.get_task_status_info(random_task_id)
            item.lab_task_progress.setString('{}/{}'.format(cur_prog, total_prog))
            btn_get = item.btn_get
            btn_go = item.btn_go
            nd_got = item.nd_got
            if status == ITEM_RECEIVED:
                btn_get.setVisible(False)
                btn_go.setVisible(False)
                nd_got.setVisible(True)
            elif status == ITEM_UNGAIN:
                btn_get.setVisible(False)
                btn_go.setVisible(True)
                nd_got.setVisible(False)
            elif status == ITEM_UNRECEIVED:
                btn_get.setVisible(True)
                btn_go.setVisible(False)
                nd_got.setVisible(False)

    def _get_random_task(self):
        if not global_data.player:
            return
        all_random_task_list = []
        for random_task_id in self._random_task_parent_list:
            random_refresh_type = task_utils.get_task_fresh_type(random_task_id)
            random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, random_task_id)
            if not random_task_list:
                log_error('\xe8\x8e\xb7\xe5\x8f\x96\xe9\x9a\x8f\xe6\x9c\xba\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe7\x88\xb6\xe4\xbb\xbb\xe5\x8a\xa1id\xef\xbc\x9a%s\xe3\x80\x82\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa561.\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xa1\xa8\xef\xbc\x8c\xe6\x88\x96\xe9\x87\x8d\xe5\x90\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81' % random_task_id)
                continue
            for random_task_id in random_task_list:
                task_conf = task_utils.get_task_conf_by_id(random_task_id)
                if not task_conf:
                    continue
                if not task_utils.is_task_open(random_task_id):
                    continue
                all_random_task_list.append(random_task_id)

        return all_random_task_list

    def _init_get_all_btn(self):
        self._update_get_all_btn()

        @self.nd_content.btn_get_all.unique_callback()
        def OnClick(*args):
            if not global_data.player:
                return
            for random_task_id in self._random_task_parent_list:
                global_data.player.receive_all_task_reward(random_task_id)

            global_data.player.receive_all_task_prog_reward(self._pve_week_task_reward_id)

    def _update_get_all_btn(self):
        self.nd_content.pnl_get_all.setVisible(self.check_task_point())
        self.nd_content.btn_get_all.setVisible(self.check_task_point())

    def _write_local_data(self):
        time_str = time_utility.get_date_str(format='%Y%m%d', timestamp=time_utility.get_server_time())
        global_data.achi_mgr.get_general_archive_data().set_field(PVE_WEEK_TASK_CACHE_KEY, time_str)
        global_data.emgr.refresh_task_main_redpoint.emit()

    @staticmethod
    def check_red_point():
        if PVEWeekTaskWidget.check_task_point() or PVEWeekTaskWidget.check_daily_red_point():
            return True
        return False

    @staticmethod
    def check_task_point():
        from logic.gutils.task_utils import get_random_task_can_receive, get_task_conf_by_id, get_pve_random_parent_task_list, get_pve_reward_task_id
        if not global_data.player:
            return False
        for random_task_id in get_pve_random_parent_task_list():
            if get_random_task_can_receive(random_task_id):
                return True

        pve_week_task_reward_id = get_pve_reward_task_id()
        task_conf = get_task_conf_by_id(pve_week_task_reward_id)
        prog_rewards = task_conf.get('prog_rewards', [])
        cur_prog = global_data.player.get_task_prog(pve_week_task_reward_id)
        for prog_info in prog_rewards:
            prog, _ = prog_info
            if not global_data.player.has_receive_prog_reward(pve_week_task_reward_id, prog) and cur_prog >= prog:
                return True

        return False

    @staticmethod
    def check_daily_red_point():
        return False

    def check_sview(self, *args):
        pass

    def destroy(self):
        super(PVEWeekTaskWidget, self).destroy()
        global_data.emgr.task_prog_changed -= self.on_task_prog_changed
        global_data.emgr.receive_task_prog_reward_succ_event -= self.on_receive_task_prog_reward_succ
        global_data.emgr.receive_task_reward_succ_event -= self.on_receive_task_reward_succ_event
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        global_data.emgr.set_reward_show_blocking_item_no_event.emit([])
        return
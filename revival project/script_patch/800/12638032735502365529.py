# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202404/ActivityPVEScoreRank.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import activity_utils, task_utils
from logic.gutils.item_utils import exec_jump_to_ui_info
from logic.gutils.template_utils import init_tempate_reward, init_common_reward_list
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.rank_pve_activity_const import get_pve_activity_data_by_rank_type
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex
import time
UPDATE_TIME = 60
FINISH_TASK_COLOR = 10331063
UNFINISH_TASK_COLOR = 16777215

class ActivityPVEScoreRank(ActivityBase):

    def on_init_panel(self):
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_event(True)

    def init_params(self):
        self._screen_capture_helper = None
        self._share_content = None
        self._timer = None
        self._conf = confmgr.get('c_activity_config', self._activity_type)
        self._ui_data = self._conf.get('cUiData')
        self._rank_type = self._ui_data.get('rank_type')
        self._my_rank_data = None
        self._my_rank_percent = None
        self._rank_data = get_pve_activity_data_by_rank_type(self._rank_type)
        if not self._rank_data:
            log_error('[ERROR] activity [%s] rank [%s] has no data' % (self._activity_type, self._rank_type))
            return
        else:
            self._rank_task = str(self._rank_data.get('task_id'))
            self._rank_list_reward_data = self._rank_data.get('reward_data')
            self._rank_list_grade_data = self._rank_data.get('grade_percent')
            self._list_rank = self.panel.list_rank
            self._cur_show_index = 0
            self._is_check_sview = False
            self._remain_time = 0
            self._is_finish = False
            self._parent_task = self._conf.get('cTask')
            self._children_task_list = task_utils.get_children_task(self._parent_task)
            self._special_task_item_list = {}
            return

    def init_ui(self):
        self._init_rank()
        self._init_time_label()
        self._init_special_task()

    def init_ui_event(self):
        activity_center_main_ui = global_data.ui_mgr.get_ui('ActivityCenterMainUI')

        def share_cb(*args):
            if not self.panel:
                return
            activity_center_main_ui and activity_center_main_ui.set_temp_tab_list_visible(True)

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            activity_center_main_ui and activity_center_main_ui.set_temp_tab_list_visible(False)
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._screen_capture_helper.take_screen_shot([
             'ActivityCenterMainUI'], self.panel, custom_cb=share_cb, head_nd_name='nd_player_info_1')

        @self.panel.btn_fight.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_pve_chapter_ui
            chapter = self._ui_data.get('chapter', 1)
            jump_to_pve_chapter_ui(int(chapter))

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            global_data.player and global_data.player.request_offer_rank_percent_reward(self._rank_type)

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(self._conf['cNameTextID']), get_text_by_id(self._conf.get('cRuleTextID', '')))

        @self._list_rank.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview is False:
                self._is_check_sview = True
                self._list_rank.SetTimeOut(0.02, self._check_sview)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.on_task_prog_changed,
           'receive_task_reward_succ_event': self.on_received_task_reward,
           'message_on_rank_percent_data': self.message_on_rank_percent_data,
           'receive_rank_percent_reward_success': self.receive_rank_percent_reward_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_task_prog_changed(self, changes):
        for change in changes:
            if self._rank_task == change.task_id:
                self._update_my_rank_score()
                return

    def message_on_rank_percent_data(self, rank_type):
        if rank_type == self._rank_type:
            self._update_rank()
            self._update_btn_state()

    def _init_rank(self):
        self._update_rank()

    def _update_rank(self):
        rank_data = self._get_or_request_rank_data()
        self._update_rank_task(rank_data)
        self._refresh_rank_content(self._rank_type, rank_data)
        self._update_my_rank_score()

    def _get_or_request_rank_data(self):
        rank_data = global_data.message_data.get_rank_percent_data(self._rank_type)
        if not rank_data or time.time() - rank_data['save_time'] > UPDATE_TIME:
            global_data.message_data.clear_rank_percent_data(self._rank_type)
            if global_data.player:
                global_data.player.request_rank_percent_list(self._rank_type, include_self=True, rt_self=True)
            return None
        else:
            self._my_rank_data = rank_data['player_data']
            if rank_data['rank_length'] > 0:
                self._my_rank_percent = rank_data['player_rank'] / rank_data['rank_length']
            else:
                self._my_rank_percent = -1
            return rank_data

    def _refresh_rank_content(self, rank_type, rank_data=None):
        if not rank_data:
            return
        if rank_type != self._rank_type:
            return
        my_rank_index = self._get_my_rank_grade_index()
        if my_rank_index != -1:
            grade = int(self._rank_list_grade_data[my_rank_index][1] * 100)
            self.panel.lab_rank.SetString(get_text_by_id(635665).format(grade))
        else:
            self.panel.lab_rank.SetString(get_text_by_id(635666))

    def _update_my_rank_score(self):
        cur_prog = global_data.player.get_task_prog(self._rank_task) if global_data.player else 0
        self.panel.lab_score.SetString(str(cur_prog))

    def _get_my_rank_grade_index(self):
        rank_data = self._get_or_request_rank_data()
        if not rank_data:
            return -1
        if self._my_rank_percent < 0:
            return -1
        for index, grade_data in enumerate(self._rank_list_grade_data):
            grade_percent = grade_data[1]
            if grade_percent > self._my_rank_percent:
                return index

        return -1

    def _update_rank_task(self, rank_data):
        if not rank_data:
            self.panel.nd_empty.setVisible(True)
            return
        rank_list = rank_data.get('rank_list', [])
        if len(rank_list) < len(self._rank_list_grade_data):
            self.panel.nd_empty.setVisible(True)
            return
        self.panel.nd_empty.setVisible(False)
        self._list_rank.DeleteAllSubItem()
        data_count = len(rank_list)
        index = 0
        all_height = 0
        sview_height = self._list_rank.getContentSize().height
        while all_height < sview_height + 100:
            if data_count - index <= 0:
                break
            data = rank_list[index]
            item = self._add_rank_list_item(data, True, index)
            index += 1

        self._list_rank.ScrollToTop()
        self._list_rank._container._refreshItemPos()
        self._list_rank._refreshItemPos()
        self._cur_show_index = index - 1

    def _check_sview(self):
        rank_data = self._get_or_request_rank_data()
        if not rank_data:
            return
        rank_list = rank_data.get('rank_list', [])
        self._cur_show_index = self._list_rank.AutoAddAndRemoveItem_MulCol(self._cur_show_index, rank_list, len(rank_list), self._add_rank_list_item, 300, 300)
        self._is_check_sview = False

    def _add_rank_list_item(self, rank_data, is_back_item, index=-1):
        if is_back_item:
            item = self._list_rank.AddTemplateItem(bRefresh=True)
        else:
            item = self._list_rank.AddTemplateItem(0, bRefresh=True)
        grade_percent = int(self._rank_list_grade_data[index][1] * 100)
        item.lab_rank.SetString(get_text_by_id(635665).format(grade_percent))
        _, rank_info = rank_data
        item.lab_score.SetString(str(rank_info[0]))
        my_rank_index = self._get_my_rank_grade_index()
        item.img_tag.setVisible(my_rank_index == index)
        reward_id = self._rank_list_reward_data[index][1]
        init_common_reward_list(item.list_reward, reward_id)
        return item

    def _init_time_label(self):
        self._release_timer()
        rank_finish_time = self._rank_data.get('time_data', {}).get('end_time')
        self._remain_time = int(rank_finish_time - time_utility.get_server_time())
        if self._remain_time > 0:
            self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_title_timer, interval=1, mode=CLOCK)
            self._update_title_timer()
        else:
            self.panel.lab_tips_time.SetString(get_text_by_id(634609))
            self._is_finish = True
        self._update_btn_state()

    def _update_title_timer(self):
        self._remain_time = self._remain_time - 1
        if self._remain_time < 0:
            self._release_timer()
            self.panel.lab_tips_time.SetString(get_text_by_id(634609))
            self._is_finish = True
            self._update_btn_state()
            global_data.emgr.refresh_activity_redpoint.emit()
            return
        time_str = time_utility.get_readable_time(self._remain_time)
        self.panel.lab_tips_time.SetString('{}{}'.format(get_text_by_id(81754), time_str))

    def _update_btn_state(self):
        self.panel.btn_fight.setVisible(not self._is_finish)
        btn_get = self.panel.btn_get
        btn_get.setVisible(self._is_finish)
        my_rank_index = self._get_my_rank_grade_index()
        has_receive_reward = bool(global_data.player and global_data.player.is_offer_rank_percent_reward(self._rank_type))
        if self._my_rank_data and my_rank_index != -1 and not has_receive_reward:
            btn_get.SetEnable(True)
        else:
            btn_get.SetEnable(False)

    def _release_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return

    def receive_rank_percent_reward_success(self):
        self._update_btn_state()

    def _init_special_task(self):
        list_task = self.panel.list_task
        list_task.DeleteAllSubItem()
        for index, task_id in enumerate(self._children_task_list):
            reward_id = task_utils.get_task_reward(task_id)
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if reward_list:
                item_no = reward_list[0][0]
                num = reward_list[0][1]
                item = list_task.AddTemplateItem()
                self._special_task_item_list[task_id] = item
                item.lab_task.SetString(task_utils.get_task_name(task_id))
                init_tempate_reward(item.temp_item, item_no, num, show_tips=True)

                @item.btn_get.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    if not global_data.player:
                        return
                    if global_data.player.is_task_finished(task_id) and not global_data.player.has_receive_reward(task_id):
                        global_data.player.receive_tasks_reward([task_id])

                @item.btn_go.unique_callback()
                def OnClick(btn, touch, task_id=task_id):
                    jump_conf = task_utils.get_jump_conf(task_id)
                    exec_jump_to_ui_info(jump_conf)

        self._update_special_task_item_state()

    def _update_special_task_item_state(self):
        for task_id, task_item in self._special_task_item_list.items():
            btn_get = task_item.btn_get
            btn_go = task_item.btn_go
            lab_task = task_item.lab_task
            if global_data.player and global_data.player.is_task_finished(task_id):
                btn_get.setVisible(True)
                btn_go.setVisible(False)
                lab_task.SetColor(FINISH_TASK_COLOR)
                if global_data.player and global_data.player.has_receive_reward(task_id):
                    btn_get.SetEnable(False)
                    btn_get.SetText(80866)
                else:
                    btn_get.SetEnable(True)
                    btn_get.SetText(910007)
            else:
                btn_get.setVisible(False)
                btn_go.setVisible(True)
                lab_task.SetColor(UNFINISH_TASK_COLOR)

    def on_received_task_reward(self, task_id):
        if self._parent_task == task_id or task_id in self._children_task_list:
            self._update_special_task_item_state()
            global_data.player.read_activity_list(self._activity_type)

    @staticmethod
    def check_red_point():
        from logic.gcommon.common_const.activity_const import ACTIVITY_PVE_SCORE_RANK
        return activity_utils.check_pve_rank_score_rp(ACTIVITY_PVE_SCORE_RANK)

    def on_finalize_panel(self):
        self.process_event(False)
        self._release_timer()
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        if self._share_content:
            self._share_content.destroy()
            self._share_content = None
        return
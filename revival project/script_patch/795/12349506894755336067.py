# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerTraining.py
from __future__ import absolute_import
from functools import cmp_to_key
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.item.item_const import ITEM_UNRECEIVED
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.share_utils import check_add_shareui_battle_record_func, check_add_shareui_kv_func, get_share_bg_path, on_share_switch_to_kv
from logic.comsys.share.ShareUI import ShareUI
from logic.comsys.share.ItemInfoShareCreator import ItemInfoShareCreator
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
import cc

class ActivitySummerTraining(ActivityCollect):

    def init_parameters(self):
        super(ActivitySummerTraining, self).init_parameters()
        self._share_content_kv = None
        self._screen_capture_helper = None
        self._cur_mecha_id = 8018
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self.task_id)
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_info.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'task_prog_changed': self._refresh_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _refresh_red_point(self, *args):
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_update_task_progress(self, task_id):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        if task_id not in children_tasks:
            return
        self.show_list()

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        else:
            task_list = activity_utils.parse_task_list(conf['cTask'])
            if len(task_list) <= 0:
                return
            parent_task = task_list[0]
            children_tasks = task_utils.get_children_task(parent_task)
            children_tasks = self.reorder_task_list(children_tasks)
            self._children_tasks = children_tasks
            sub_act_list = self.panel.act_list
            sub_act_list.SetInitCount(0)
            sub_act_list.SetInitCount(len(children_tasks))
            ui_data = conf.get('cUiData', {})
            for i, task_id in enumerate(children_tasks):
                item_widget = sub_act_list.GetItem(i).temp_common
                item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
                if ui_data.get('lab_name_color'):
                    color = int(ui_data.get('lab_name_color'), 16)
                    item_widget.lab_name.SetColor(color)
                if ui_data.get('lab_num_color'):
                    color = int(ui_data.get('lab_num_color'), 16)
                    item_widget.lab_num.SetColor(color)
                reward_id = task_utils.get_task_reward(task_id)
                template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

            self.refresh_list()
            self._init_get_all()
            return

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i).temp_common
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            item_widget.lab_num.setVisible(True)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                PIC0 = 'gui/ui_res_2/common/button/btn_secondary_middle.png'
                PIC1 = 'gui/ui_res_2/common/button/btn_secondary_major.png'
                PIC2 = 'gui/ui_res_2/common/button/btn_secondary_useless.png'
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    btn.SetText(604029)
                    btn.SetEnable(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        btn.SetText(text_id)
                        btn.SetTextColor(2369169, 2369169, 2369169)
                        btn.SetFrames('', [PIC0, PIC0, PIC2], False, None)
                        btn.SetEnable(True)
                    else:
                        btn.SetEnable(False)
                else:
                    btn.setVisible(True)
                    btn.SetEnable(True)
                return

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                show_item_no = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
                if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                    if not self._screen_capture_helper:
                        self._screen_capture_helper = ScreenFrameHelper()

                    def custom_cb(*args):
                        self.show_share_ui()

                    self._screen_capture_helper.take_screen_shot([
                     self.__class__.__name__, 'ActivityFairylandMainUI'], self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1', item_detail_no=show_item_no, item_detail_no_is_get=False, need_share_ui=True)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()

    def show_share_ui(self):
        if not global_data.ui_mgr.get_ui('ShareUI'):
            ui = ShareUI()
            ui.clear_choose_list_func()
        if not self._share_content_kv:
            share_creator = ItemInfoShareCreator()
            share_creator.create()
            self._share_content_kv = share_creator
        if self._share_content_kv:
            lobby_mecha_id = battle_id_to_mecha_lobby_id(int(self._cur_mecha_id))
            kv_path = get_share_bg_path(lobby_mecha_id)
            self._share_content_kv.get_ui_bg_sprite().SetDisplayFrameByPath('', kv_path)
            self._share_content_kv.set_show_record(False)
            self._share_content_kv.show_share_detail(lobby_mecha_id, is_get=False)
        on_share_switch_to_kv(self._share_content_kv, self._screen_capture_helper, True)

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            can_receive_reward_a = global_data.player.is_task_reward_receivable(task_id_a)
            can_receive_reward_b = global_data.player.is_task_reward_receivable(task_id_b)
            if can_receive_reward_a != can_receive_reward_b:
                if can_receive_reward_a:
                    return -1
                if can_receive_reward_b:
                    return 1
            return 0

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def _init_get_all(self):
        task_num = len(self._get_all_receivable_tasks())
        if task_num >= 2:
            self.panel.nd_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_all_task_reward(self.task_id)

        else:
            self.panel.nd_get_all.setVisible(False)
            self.panel.img_num.setVisible(False)

    def _get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self._children_tasks:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_title_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_title_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_title_time.SetString(get_readable_time(close_left_time))
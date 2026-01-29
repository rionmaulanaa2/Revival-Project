# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityKizunaSignShare.py
from __future__ import absolute_import
from six.moves import range
from functools import cmp_to_key
import copy
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS, get_rela_day_no
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_SHARE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.share_utils import check_add_shareui_battle_record_func, check_add_shareui_kv_func, get_share_bg_path, on_share_switch_to_kv
from logic.comsys.share.ShareUI import ShareUI
from logic.comsys.share.ActivityAIConcertCalendarShareCreator import ActivityAIConcertShareCreator
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_CALENDAR
import cc
ITEM_EMOTION_ID = 30601411
ITEM_STICK_ID = 1059969
MAX_SIGN_CNT = 3
MAX_SHARE_CNT = 3

class ActivityKizunaSignShare(ActivityCollect):
    SHARE_CREATOR = ActivityAIConcertShareCreator

    def __init__(self, dlg, activity_type):
        super(ActivityKizunaSignShare, self).__init__(dlg, activity_type)

    def init_parameters(self):
        super(ActivityKizunaSignShare, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        children_tasks = task_utils.get_children_task(self._task_id)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        self.panel.lab_time.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        self.panel.lab_sign_01.SetString(get_text_by_id(907154, ('3', )))
        self.panel.lab_share_01.SetString(get_text_by_id(907155, ('3', )))
        self.panel.lab_sign_03.SetString(item_utils.get_lobby_item_name(ITEM_EMOTION_ID))
        self.panel.lab_emotion.SetString(item_utils.get_lobby_item_name(ITEM_EMOTION_ID))
        self.panel.lab_share_03.SetString(item_utils.get_lobby_item_name(ITEM_STICK_ID))
        self.panel.lab_action.SetString(item_utils.get_lobby_item_name(ITEM_STICK_ID))
        for idx, item_id in enumerate((ITEM_EMOTION_ID, ITEM_STICK_ID)):
            click_node = getattr(self.panel, 'btn_click_0%s' % (idx + 1))

            @click_node.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
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

    def set_widget_done(self, item_widget, is_done):
        item_widget.img_love_01.setVisible(not is_done)
        item_widget.img_love_02.setVisible(is_done)

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)
        children_tasks = self._children_tasks
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        conf = confmgr.get('c_activity_config', self._activity_type)
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
            self._init_spe_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()
        self._init_get_all()
        self._refresh_sign_and_share_state()
        return

    def _init_spe_reward_list(self, nd_list, reward_id, sub_widget='', force_extra_ani=False):
        nd_list.DeleteAllSubItem()
        if reward_id:
            import common.cfg.confmgr as confmgr
            from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            if not reward_conf:
                log_error('reward_id is not exist in common_reward_data', reward_id)
                return
            reward_list = reward_conf.get('reward_list', [])
            reward_list = reward_list[:1]
            reward_count = len(reward_list)
            for idx in range(reward_count):
                item_no, item_num = reward_list[idx]
                reward_item = nd_list.AddTemplateItem()
                if sub_widget:
                    reward_item = getattr(reward_item, sub_widget)
                template_utils.init_tempate_mall_i_item(reward_item, item_no, item_num, show_tips=True, force_extra_ani=force_extra_ani)

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
                btn_receive = item_widget.nd_task.temp_btn_get
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
                elif cur_times < total_times:
                    if self._is_share_task(task_id):
                        if not self._is_can_share_task(task_id):
                            update_task_list_btn(btn_receive, BTN_ST_ONGOING)
                        else:
                            update_task_list_btn(btn_receive, BTN_ST_SHARE)
                    else:
                        update_task_list_btn(btn_receive, BTN_ST_ONGOING)
                else:
                    update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                if _cur_times < _total_times and self._is_share_task(task_id):
                    self._share_activity()
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetEnable(False)

            check_btn()

    def _is_can_share_task(self, task_id):
        if not self._is_share_task(task_id):
            return False
        total_times = task_utils.get_total_prog(task_id)
        cur_times = global_data.player.get_task_prog(task_id)
        last_share_day = global_data.player.get_task_content(task_id, 'last_share_day', 0)
        now_day = get_rela_day_no()
        if last_share_day >= now_day or cur_times < total_times - 1:
            return False
        return True

    def _share_activity(self):
        from logic.comsys.share.ShareUI import ShareUI
        share_ui = ShareUI(parent=self.panel, need_black_bg=False)

        def init_cb():
            if share_ui and share_ui.is_valid():
                share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                def share_inform_func():
                    if global_data.player:
                        global_data.player.share_activity('activity_' + str(ACTIVITY_KIZUNA_AI_CALENDAR))
                        global_data.player.share()

                share_ui.set_share_inform_func(share_inform_func)

        if not getattr(self, '_share_content', None):
            self._share_content = self.SHARE_CREATOR()
            self._share_content.create(parent=None, init_cb=init_cb)
        else:
            init_cb()
        return

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
            is_can_share_task_a = self._is_can_share_task(task_id_a)
            is_can_share_task_b = self._is_can_share_task(task_id_b)
            if is_can_share_task_a != is_can_share_task_b:
                if is_can_share_task_a:
                    return -1
                if is_can_share_task_b:
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
                global_data.player.receive_all_task_reward(self._task_id)

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
        left_time = task_utils.get_raw_left_open_time(self._task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_activity_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_activity_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_activity_time.SetString(get_readable_time(close_left_time))

    def _is_share_task(self, task_id):
        task_conf = task_utils.get_task_conf_by_id(task_id)
        task_temp_id = task_conf.get('template_id', None)
        if task_temp_id == '2004':
            return True
        else:
            return False

    def _refresh_sign_and_share_state(self):
        sign_total_cnt = 0
        sign_done_cnt = 0
        share_total_cnt = 0
        share_done_cnt = 0
        for tid in self._children_tasks:
            if self._is_share_task(tid):
                share_total_cnt += 1
                if global_data.player.has_receive_reward(tid):
                    share_done_cnt += 1
            else:
                sign_total_cnt += 1
                if global_data.player.has_receive_reward(tid):
                    sign_done_cnt += 1

        sign_total_cnt = min(sign_total_cnt, MAX_SIGN_CNT)
        sign_done_cnt = min(sign_done_cnt, MAX_SIGN_CNT)
        share_total_cnt = min(share_total_cnt, MAX_SHARE_CNT)
        share_done_cnt = min(share_done_cnt, MAX_SHARE_CNT)
        if sign_done_cnt >= MAX_SIGN_CNT:
            self.panel.nd_signed_complete.setVisible(True)
            self.panel.nd_signed.setVisible(False)
        else:
            self.panel.nd_signed_complete.setVisible(False)
            self.panel.nd_signed.setVisible(True)
            sub_sign_list = self.panel.list_heart_01
            sub_sign_list.SetInitCount(0)
            sub_sign_list.SetInitCount(sign_total_cnt)
            for i in range(sign_total_cnt):
                item_widget = sub_sign_list.GetItem(i)
                if i < sign_done_cnt:
                    self.set_widget_done(item_widget, True)
                else:
                    self.set_widget_done(item_widget, False)

        if share_done_cnt >= MAX_SHARE_CNT:
            self.panel.nd_shared_complete.setVisible(True)
            self.panel.nd_shared.setVisible(False)
        else:
            self.panel.nd_shared_complete.setVisible(False)
            self.panel.nd_shared.setVisible(True)
            sub_share_list = self.panel.list_heart_02
            sub_share_list.SetInitCount(0)
            sub_share_list.SetInitCount(share_total_cnt)
            for i in range(share_total_cnt):
                item_widget = sub_share_list.GetItem(i)
                if i < share_done_cnt:
                    self.set_widget_done(item_widget, True)
                else:
                    self.set_widget_done(item_widget, False)
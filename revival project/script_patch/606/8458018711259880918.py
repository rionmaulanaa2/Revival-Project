# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/ActivitySpringShoutFriends.py
from __future__ import absolute_import
from six.moves import range
from logic.gutils import activity_utils
from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
from common.cfg import confmgr
from logic.client.const import share_const
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.item_utils import get_lobby_item_name, get_skin_rare_degree_icon, get_lobby_item_pic_by_item_no
from logic.gutils import task_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_SHARE
from logic.comsys.activity.Activity202201.SpringShoutFriendsRedPackagesUI import SpringShoutFriendsRedPackagesUI

class ActivitySpringShoutFriends(ActivityTemplate):
    NORMAL_TASK_COUNT = 4
    NORMAL_TASK_MAX_RECEIVED_COUNT = 2

    def on_init_panel(self):
        super(ActivitySpringShoutFriends, self).on_init_panel()
        global_data.player.query_newyear_hongbao_info()
        global_data.emgr.refresh_activity_redpoint.emit()
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(activity_type, self.__class__.__name__)

        @self.panel.btn_unlock.callback()
        def OnClick(btn, touch):
            SpringShoutFriendsRedPackagesUI()

        @self.panel.btn_preview.callback()
        def OnClick(btn, touch):
            from logic.comsys.activity.Activity202201.SpringShoutFriendsRewardPreviewUI import SpringShoutFriendsRewardPreviewUI
            SpringShoutFriendsRewardPreviewUI()

        @self.panel.btn_binding.callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.UserVerifyCodeUI import UserVerifyCodeUI
            UserVerifyCodeUI()

        self.panel.btn_question.BindMethod('OnClick', self.on_click_btn_question)
        self.refresh_all()

    def on_finalize_panel(self):
        super(ActivitySpringShoutFriends, self).on_finalize_panel()
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def refresh_all(self):
        self.refresh_lucky()
        self.refresh_normal()
        task_info = global_data.player.get_newyear_task_dict()
        user_arch = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
        user_arch.set_field(self.__class__.__name__, task_info)
        global_data.emgr.refresh_activity_list.emit()

    def refresh_normal(self):
        webapp_info = global_data.player.get_webapp_info(self._activity_type)
        task_can_change = webapp_info.get('task_can_change', [])
        normal_task_list = webapp_info.get('normal_task_list', [])
        self.panel.list_item.SetInitCount(self.NORMAL_TASK_COUNT)
        received_task_ids = [ task_id for task_id in normal_task_list if global_data.player.get_task_reward_status(task_id) == ITEM_RECEIVED
                            ]
        is_full = len(received_task_ids) >= self.NORMAL_TASK_MAX_RECEIVED_COUNT
        for idx in range(self.NORMAL_TASK_COUNT):
            if idx < len(normal_task_list):
                task_data = normal_task_list[idx]
            else:
                task_data = None
            task_temp = self.panel.list_item.GetItem(idx)
            if task_temp:
                task_id = task_data
                self.init_task_temp(task_temp, None, task_id, is_full, task_id in task_can_change)

        return

    def refresh_lucky(self):
        webapp_info = global_data.player.get_webapp_info(self._activity_type)
        lucky_task_list = webapp_info.get('lucky_task_list', [])
        task_can_change = webapp_info.get('task_can_change', [])
        lucky_task_id = lucky_task_list or None if 1 else lucky_task_list[0]
        lucky_task_can_change = lucky_task_id in task_can_change
        self.init_task_temp(self.panel.temp_big, None, lucky_task_id, is_full=False, can_change=lucky_task_can_change)
        self.panel.temp_big.bar_level.setVisible(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_web_app_info_update_event': self.on_app_info_update,
           'receive_task_reward_succ_event': self.check_special_task_prog
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def check_special_task_prog(self, task_id):
        webapp_info = global_data.player.get_webapp_info(self._activity_type)
        lucky_task_list = webapp_info.get('lucky_task_list', [])
        normal_task_list = webapp_info.get('normal_task_list', [])
        if task_id in lucky_task_list:
            self.refresh_lucky()
        if task_id in normal_task_list:
            self.refresh_normal()

    def on_app_info_update(self, act_id):
        if str(act_id) != str(self._activity_type):
            return
        self.refresh_all()

    def init_task_temp(self, task_temp, reward_item_no, task_id, is_full, can_change):
        if not reward_item_no and task_id:
            reward_list = task_utils.get_task_reward_list(task_id)
            reward_item_no, _ = reward_list[0]
        if reward_item_no is None:
            task_temp.img_unknow.setVisible(True)
            task_temp.img_item.setVisible(False)
        else:
            task_temp.img_unknow.setVisible(False)
            task_temp.img_item.setVisible(True)
            pic = get_lobby_item_pic_by_item_no(reward_item_no)
            task_temp.img_item.SetDisplayFrameByPath('', pic)

        @task_temp.btn_item.callback()
        def OnClick(btn, touch):
            item_id = reward_item_no
            if not item_id:
                return
            else:
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                global_data.emgr.show_item_desc_ui_event.emit(item_id, None, w_pos, extra_info=extra_info)
                return

        if task_id:
            status = global_data.player.get_task_reward_status(task_id)
        else:
            status = None
        if reward_item_no:
            img_quality = get_skin_rare_degree_icon(reward_item_no)
            task_temp.bar_level.setVisible(True)
            task_temp.img_level.SetDisplayFrameByPath('', img_quality)
            item_name = get_lobby_item_name(reward_item_no)
            task_temp.lab_item_name.SetString(item_name)
            if not can_change:
                total_times = task_utils.get_total_prog(task_id)
                cur_times = global_data.player.get_task_prog(task_id)
                progress_txt = ''.join((get_text_by_id(610300), str('%s/%s' % (cur_times, total_times))))
                task_temp.lab_task_content.SetString(task_utils.get_task_name(task_id))
                task_temp.lab_prog.SetString(progress_txt)
            else:
                task_temp.lab_task_content.SetString(610573)
                task_temp.lab_prog.SetString('')
            self.update_receive_btn(status, task_temp.btn_click, is_full, can_change)
        else:
            task_temp.bar_level.setVisible(False)
            task_temp.lab_item_name.SetString(610566)
            task_temp.lab_task_content.SetString(610575)
            task_temp.btn_click.SetText(80937)
            task_temp.lab_prog.SetString('')

        @task_temp.btn_click.unique_callback()
        def OnClick(btn, touch, task_id=task_id):
            if not activity_utils.is_activity_in_limit_time(self._activity_type):
                return
            if not task_id:
                SpringShoutFriendsRedPackagesUI()
                return
            status = global_data.player.get_task_reward_status(task_id)
            if can_change:
                global_data.player.change_hongbao_task_reard(task_id)
            elif status in [ITEM_RECEIVED, ITEM_UNGAIN] or is_full:
                pass
            elif status == ITEM_UNRECEIVED:
                global_data.player.receive_hongbao_task_reard(task_id)
                btn.SetText(906668)
                btn.SetEnable(False)

        return

    def update_receive_btn(self, status, btn_receive, is_full, can_change):
        btn_receive.EnableCustomState(True)
        if status == ITEM_RECEIVED:
            btn_receive.SetText(906668)
            btn_receive.SetEnable(False)
        elif is_full:
            btn_receive.SetText(610520)
            btn_receive.SetEnable(False)
        elif can_change:
            btn_receive.SetText(610574)
            btn_receive.SetEnable(True)
        elif status == ITEM_UNGAIN:
            btn_receive.SetText(604031)
            btn_receive.SetEnable(True)
        elif status == ITEM_UNRECEIVED:
            btn_receive.SetText(80930)
            btn_receive.SetSelect(True)

    def on_click_btn_question(self, btn, touch):
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))
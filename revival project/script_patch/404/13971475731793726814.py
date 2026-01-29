# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPromare/ActivityPromareLoginShare.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.comsys.activity.widget.GlobalAchievementWidget import GlobalAchievementWidget
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.time_utility import get_simply_time, get_time_string
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog, get_jump_conf, get_raw_left_open_time, get_children_task
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_pic_by_item_no
from logic.gcommon import time_utility

class ActivityPromareLoginShare(ActivityTemplate):

    def on_init_panel(self):
        super(ActivityPromareLoginShare, self).on_init_panel()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default=None)
        self.widget_map = {}
        self._screen_capture_helper = None
        self.refresh_data()
        activity_conf = confmgr.get('c_activity_config', str(self._activity_type), default={})
        self.panel.lab_time.SetString(get_time_string(fmt='%Y.%m.%d', ts=activity_conf['cBeginTime']) + '-' + get_time_string(fmt='%Y.%m.%d', ts=activity_conf['cEndTime']))

        @self.panel.btn_question.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(602039, 611417)

        @self.panel.btn_show.callback()
        def OnClick(btn, touch):
            from logic.gutils.template_utils import get_reward_list_by_reward_id, init_common_reward_list
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            from logic.gutils import item_utils
            ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
            box_id = ui_data.get('target_skin_id', 201802151)
            reward_id = item_utils.get_lobby_item_reward_id(box_id)
            reward_list = get_reward_list_by_reward_id(reward_id)
            ui = global_data.ui_mgr.show_ui('RewardListUI', 'logic.comsys.common_ui')
            ui.set_reward_data(reward_list)

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            self._on_click_btn_share()

        self.init_get_all_btn()
        self.update_share_btn()
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        share_task_list = ui_data['share_task']
        for idx, task in enumerate(share_task_list):
            is_today = self.check_is_todays_task(task)
            if is_today:
                self.panel.list_item.CenterWithNode(self.panel.list_item.GetItem(idx))
                break

        return

    def update_share_btn(self):
        is_shared = global_data.player.is_today_shared()
        self.panel.btn_share.SetEnable(not is_shared)
        self.panel.btn_share.SetText(606046 if is_shared else 3155)

    def init_get_all_btn(self):
        self.update_get_all_btn_visible()

        @self.panel.btn_get.unique_callback()
        def OnClick(*args):
            self.on_click_get_all_btn()

    def update_get_all_btn_visible(self):
        self.panel.btn_get.setVisible(self.check_red_point())

    def check_red_point(self):
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        login_task_list = ui_data['login_task']
        share_task_list = ui_data['share_task']
        for child_task_id in login_task_list:
            has_unreceived_task = global_data.player.has_unreceived_task_reward(child_task_id)
            if task_utils.is_task_open(child_task_id) and has_unreceived_task:
                return True

        for child_task_id in share_task_list:
            has_unreceived_task = global_data.player.has_unreceived_task_reward(child_task_id)
            if has_unreceived_task:
                return True

        return False

    def on_click_get_all_btn(self):
        global_data.player.receive_all_task_reward(self._task_id)

    def on_finalize_panel(self):
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        self.widget_map = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.on_need_refresh_task_show,
           'receive_task_reward_succ_event': self.on_need_refresh_task_show,
           'player_first_success_share_event': self.on_success_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_task_list(self):
        pass

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type, {'completion': True})

    def on_need_refresh_task_show(self, *args):
        self.update_get_all_btn_visible()
        self.refresh_data()

    def refresh_data(self, *args):
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        conf = (
         (
          ui_data['login_task'], 610765, 610765, 15500712),
         (
          ui_data['share_task'], 610766, 610766, 6912718))
        offset = self.panel.list_item.GetContentOffset()
        all_items = self.panel.list_item.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            if ui_item.GetTemplatePath() != 'activity/activity_202203/promare/login/i_promare_login_list':
                self.panel.list_item.DeleteItemIndex(idx)

        self.panel.list_item.RecycleAllItem()
        login_task_list = ui_data['login_task']
        share_task_list = ui_data['share_task']
        for task_id in login_task_list:
            if self.check_is_todays_task(task_id):
                temp = 'activity/activity_202203/promare/login/i_promare_login_list2'
                item = self.panel.list_item.AddControl(global_data.uisystem.load_template_create(temp))
                item.setLocalZOrder(1)
            else:
                temp = 'activity/activity_202203/promare/login/i_promare_login_list'
                item = self.panel.list_item.ReuseItem()
                if not item:
                    item = self.panel.list_item.AddTemplateItem()
                item.setLocalZOrder(0)

        self.panel.list_item.RefreshItemPos()
        self.panel.list_item.SetContentOffset(offset)
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            normal_task = login_task_list[idx]
            share_task = share_task_list[idx]
            self.init_promare_login_item(ui_item, normal_task, share_task)

    def init_promare_login_item(self, ui_item, task_id, second_task_id):
        start_time = self.get_task_start_time(task_id)
        date_time = time_utility.get_utc8_datetime(start_time)
        ui_item.lab_time.SetString(get_text_by_id(81360).format('%s.%s' % (date_time.month, date_time.day)))
        ui_item.list_item.SetInitCount(2)
        self.init_each_promare_task(ui_item.list_item.GetItem(0), task_id, False)
        self.init_each_promare_task(ui_item.list_item.GetItem(1), second_task_id, True)

    def init_each_promare_task(self, ui_item, child_task, is_share_task):
        ui_item.lab_rule.SetString(get_task_name(child_task))
        task_prog = global_data.player.get_task_prog(child_task)
        total_prog = get_total_prog(child_task)
        has_unreceived_task = global_data.player.has_unreceived_task_reward(child_task)
        is_finished = global_data.player.is_task_finished(child_task)
        is_open = task_utils.is_task_open(child_task)
        now = time_utility.get_server_time()
        start_time = self.get_task_start_time(child_task)
        end_time = self.get_task_end_time(child_task) or now + 1
        reward_id = task_utils.get_task_reward(child_task)
        ui_item.img_choose.setVisible(False)
        ui_item.StopAnimation('get_tips')
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        if reward_conf:
            reward_list = reward_conf.get('reward_list', [])
            if reward_list:
                item_no, item_num = reward_list[0]
                item_path = get_lobby_item_pic_by_item_no(item_no)
                ui_item.img_item.SetDisplayFrameByPath('', item_path)
        if not is_share_task:
            if is_finished and not has_unreceived_task:
                ui_item.nd_finish.setVisible(True)
                ui_item.nd_sign.setVisible(False)
                ui_item.nd_miss.setVisible(False)
            elif is_open:
                if self.check_is_todays_task(child_task):
                    ui_item.img_choose.setVisible(True)
                    ui_item.PlayAnimation('get_tips')
                    ui_item.nd_finish.setVisible(False)
                    ui_item.nd_sign.setVisible(False)
                    ui_item.nd_miss.setVisible(False)
                elif self.check_can_resign(child_task):
                    ui_item.nd_finish.setVisible(False)
                    ui_item.nd_sign.setVisible(True)
                    ui_item.nd_miss.setVisible(False)
            elif end_time < now:
                ui_item.nd_finish.setVisible(False)
                ui_item.nd_sign.setVisible(False)
                ui_item.nd_miss.setVisible(True)
            else:
                ui_item.nd_finish.setVisible(False)
                ui_item.nd_sign.setVisible(False)
                ui_item.nd_miss.setVisible(False)
        elif is_finished and not has_unreceived_task:
            ui_item.nd_finish.setVisible(True)
            ui_item.nd_sign.setVisible(False)
            ui_item.nd_miss.setVisible(False)
        elif is_open or has_unreceived_task:
            if has_unreceived_task:
                ui_item.img_choose.setVisible(True)
                ui_item.PlayAnimation('get_tips')
            else:
                ui_item.img_choose.setVisible(False)
                ui_item.StopAnimation('get_tips')
            ui_item.nd_finish.setVisible(False)
            ui_item.nd_sign.setVisible(False)
            ui_item.nd_miss.setVisible(False)
        elif end_time < now:
            ui_item.nd_finish.setVisible(False)
            ui_item.nd_sign.setVisible(False)
            ui_item.nd_miss.setVisible(True)
        else:
            ui_item.nd_finish.setVisible(False)
            ui_item.nd_sign.setVisible(False)
            ui_item.nd_miss.setVisible(False)

        @ui_item.btn_choose.callback()
        def OnClick(btn, touch):
            if not is_share_task:
                is_open = task_utils.is_task_open(child_task)
                if is_open and global_data.player.has_unreceived_task_reward(child_task):
                    global_data.player.receive_task_reward(child_task)
                elif task_prog != total_prog and self.check_is_todays_task(child_task):
                    jump_conf = get_jump_conf(child_task)
                    exec_jump_to_ui_info(jump_conf)
            elif global_data.player.has_unreceived_task_reward(child_task):
                global_data.player.receive_task_reward(child_task)
            elif task_prog != total_prog and self.check_is_todays_task(child_task):
                jump_conf = get_jump_conf(child_task)
                exec_jump_to_ui_info(jump_conf)

    def check_can_resign(self, task):
        if task_utils.is_task_open(task) and not self.check_is_todays_task(task):
            return True
        else:
            return False

    def check_is_todays_task(self, task_id):
        start_time = self.get_task_start_time(task_id)
        now = time_utility.get_server_time()
        if now >= start_time and now - start_time < time_utility.ONE_DAY_SECONDS:
            return True
        else:
            return False

    def get_task_start_time(self, task_id):
        conf = task_utils.get_task_conf_by_id(task_id)
        return conf.get('start_time', 0)

    def get_task_end_time(self, task_id):
        conf = task_utils.get_task_conf_by_id(task_id)
        return conf.get('end_time', 0)

    def _on_click_btn_share(self):
        from logic.gcommon.common_const import activity_const as acconst
        from logic.gutils import jump_to_ui_utils
        if str(self._activity_type) == acconst.ACTIVITY_PROMARE_LOGINSHARE:
            jump_to_ui_utils.jump_to_share_picture('gui/ui_res_2/txt_pic/text_pic_en/share/promare_share.png', None, {'hide_non_pic_content': True})
        else:
            jump_to_ui_utils.jump_to_share()
        return

    def on_success_share(self):
        self.update_share_btn()
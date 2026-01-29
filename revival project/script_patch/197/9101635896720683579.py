# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeixinBinding2.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.client.const import share_const

class ActivityWeixinBinding2(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWeixinBinding2, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.screen_capture_helper = ScreenFrameHelper()

    def on_init_panel(self):
        self.init_reward_widget()
        self.update_reward_widget()
        self.init_all_btns()
        self.update_all_btn_visible()
        self.process_event(True)
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        self.process_event(False)
        if self.screen_capture_helper:
            self.screen_capture_helper.destroy()
            self.screen_capture_helper = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_reward_widget(self):
        reward_id = task_utils.get_task_reward(self.task_id)
        init_common_reward_list(self.panel.list_award, reward_id)

    def init_all_btns(self):

        @self.panel.btn_auto.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_share()

        self.panel.btn_auto.setVisible(True)
        self.panel.btn_manual.setVisible(False)
        self.panel.btn_tips.setVisible(False)
        self.panel.btn_get.setVisible(False)
        self.panel.lab_tips.setVisible(False)

    def update_all_btn_visible(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if reward_status == ITEM_UNGAIN:
            self.panel.btn_auto.SetText(get_text_by_id(611501))
            self.panel.btn_auto.SetEnable(True)
        elif reward_status == ITEM_UNRECEIVED:
            self.panel.btn_auto.SetText(get_text_by_id(606010))
            self.panel.btn_auto.SetEnable(True)
        elif reward_status == ITEM_RECEIVED:
            self.panel.btn_auto.SetText(get_text_by_id(80866))
            self.panel.btn_auto.SetEnable(False)

    def update_reward_widget(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if not (self.panel and self.panel.isValid()):
            return
        all_items = self.panel.list_award.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def on_update_task_progress(self, *args):
        self.update_all_btn_visible()
        self.update_reward_widget()

    def on_click_btn_share(self, *args):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if reward_status == ITEM_RECEIVED:
            return
        if reward_status == ITEM_UNRECEIVED:
            global_data.player.receive_task_reward(self.task_id)
            return
        if reward_status == ITEM_UNGAIN and self.screen_capture_helper:

            def custom_cb(*args):
                share_ui = global_data.ui_mgr.get_ui('ShareUI')
                if not share_ui:
                    return
                share_ui.set_custom_platform_check(self.custom_platform_check_func)
                share_ui.init_platform_list()
                self.on_end_share()

            def share_inform_func():
                if global_data.player:
                    global_data.player.share_activity('activity_166')

            self.on_begin_share()
            self.screen_capture_helper.take_screen_shot(['ActivityCenterMainUI'], self.panel, share_inform_func=share_inform_func, custom_cb=custom_cb)

    def custom_platform_check_func(self, platform_list):
        ret_list = []
        for platform_info in platform_list:
            if isinstance(platform_info, dict) and platform_info.get('share_args', {}).get('platform_enum') == share_const.APP_SHARE_WEIXIN:
                ret_list.append(platform_info)

        return ret_list

    def on_begin_share(self):
        ui = global_data.ui_mgr.get_ui('ActivityCenterMainUI')
        ui and ui.set_close_btn_visible(False)

    def on_end_share(self):
        ui = global_data.ui_mgr.get_ui('ActivityCenterMainUI')
        ui and ui.set_close_btn_visible(True)
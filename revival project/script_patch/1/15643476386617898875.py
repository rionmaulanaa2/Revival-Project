# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityBilibiliFollow.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.platform import is_ios

class ActivityBilibiliFollow(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityBilibiliFollow, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def on_init_panel(self):
        self.init_reward_widget()
        self.init_all_btns()
        self.refresh_reward_widget()
        self.refresh_btns()
        self.process_event(True)
        self.panel.PlayAnimation('appear')

    def on_finalize_panel(self):
        self.process_event(False)

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
        is_finished = global_data.player.is_task_finished(self.task_id)
        self.panel.list_award.setVisible(is_finished)

    def init_all_btns(self):

        @self.panel.btn_follow_riko.unique_callback()
        def OnClick(btn, touch):
            url = 'https://space.bilibili.com/535102427'
            import game3d
            if is_ios():
                game3d.open_url(url)
            elif not game3d.open_url('bilibili://space/535102427'):
                game3d.open_url(url)
            global_data.player and global_data.player.call_server_method('follow_bilibili_riko', ())
            btn.SetEnable(False)
            global_data.achi_mgr.set_cur_user_archive_data('clicked_bilibili_follow_riko_btn', 1)

        @self.panel.btn_follow_smc.unique_callback()
        def OnClick(btn, touch):
            url = 'https://space.bilibili.com/419641453'
            import game3d
            if is_ios():
                game3d.open_url(url)
            elif not game3d.open_url('bilibili://space/419641453'):
                game3d.open_url(url)
            global_data.player and global_data.player.call_server_method('follow_bilibili_smc', ())
            btn.SetEnable(False)
            global_data.achi_mgr.set_cur_user_archive_data('clicked_bilibili_follow_smc_btn', 1)

        @self.panel.btn_get.unique_callback()
        def OnClick(*args):
            global_data.player.receive_task_reward(self.task_id)

        self.panel.btn_follow_riko.SetText(get_text_by_id(606287))
        self.panel.btn_follow_smc.SetText(get_text_by_id(606287))
        is_clicked_riko = global_data.achi_mgr.get_cur_user_archive_data('clicked_bilibili_follow_riko_btn', default=0) == 1
        is_clicked_smc = global_data.achi_mgr.get_cur_user_archive_data('clicked_bilibili_follow_smc_btn', default=0) == 1
        self.panel.btn_follow_riko.SetEnable(not is_clicked_riko)
        self.panel.btn_follow_smc.SetEnable(not is_clicked_smc)

    def on_update_task_progress(self, *args):
        self.refresh_btns()
        self.refresh_reward_widget()
        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_btns(self, *args):
        children_task_id_list = task_utils.get_children_task(self.task_id)
        for task_id in children_task_id_list:
            task_args = task_utils.get_task_arg(task_id)
            follow_type = task_args.get('follow_type')
            is_finished = global_data.player.is_task_finished(task_id)
            if follow_type == 'riko':
                self.panel.btn_follow_riko.SetEnable(not is_finished)
            elif follow_type == 'smc':
                self.panel.btn_follow_smc.SetEnable(not is_finished)

        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if reward_status == ITEM_UNGAIN:
            self.panel.btn_get.SetEnable(False)
            self.panel.btn_get.SetText(606010)
        elif reward_status == ITEM_UNRECEIVED:
            self.panel.btn_get.SetEnable(True)
            self.panel.btn_get.SetText(606010)
        elif reward_status == ITEM_RECEIVED:
            self.panel.btn_get.SetEnable(False)
            self.panel.btn_get.SetText(80866)

    def refresh_reward_widget(self):
        if not (self.panel and self.panel.isValid()):
            return
        is_finished = global_data.player.is_task_finished(self.task_id)
        self.panel.list_award.setVisible(is_finished)
        self.panel.nd_follow_riko.setVisible(not is_finished)
        self.panel.nd_follow_smc.setVisible(not is_finished)
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        all_items = self.panel.list_award.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)
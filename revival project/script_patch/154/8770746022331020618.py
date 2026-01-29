# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWeiboBinding.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
GRAY_BTN_ICON = 'gui/ui_res_2_cn/activity/activity_202012/weibo_btn02.png'

class ActivityWeiboBinding(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWeiboBinding, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')

    def on_init_panel(self):
        self.init_reward_widget()
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

    def update_reward_widget(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if not (self.panel and self.panel.isValid()):
            return
        all_items = self.panel.list_award.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def on_update_task_progress(self, *args):
        self.refresh_btns()
        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_btns(self, *args):
        if not self.task_id:
            return
        else:
            reward_status = global_data.player.get_task_reward_status(self.task_id)
            if reward_status == ITEM_UNGAIN:

                @self.panel.btn_go.unique_callback()
                def OnClick(*args):
                    import game3d
                    if not game3d.open_url('sinaweibo://userinfo?uid=6940968600'):
                        game3d.open_url('https://weibo.com/u/6940968600')
                    global_data.player and global_data.player.call_server_method('bind_weibo_smc', ())

                self.panel.btn_go.SetText(get_text_by_id(606277))
            elif reward_status == ITEM_UNRECEIVED:

                @self.panel.btn_go.unique_callback()
                def OnClick(*args):
                    global_data.player.receive_task_reward(self.task_id)

                self.panel.btn_go.SetText(get_text_by_id(80248))
            elif reward_status == ITEM_RECEIVED:

                @self.panel.btn_go.unique_callback()
                def OnClick(*args):
                    import game3d
                    if not game3d.open_url('sinaweibo://userinfo?uid=6940968600'):
                        game3d.open_url('https://weibo.com/u/6940968600')

                self.panel.btn_go.SetText(get_text_by_id(80866))
                self.panel.btn_go.SetFrames('', [GRAY_BTN_ICON, GRAY_BTN_ICON, GRAY_BTN_ICON], False, None)
            self.update_reward_widget()
            return
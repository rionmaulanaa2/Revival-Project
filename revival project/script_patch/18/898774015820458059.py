# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRedBook.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import activity_utils
from logic.gutils import task_utils
from logic.gutils.template_utils import init_common_reward_list
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN

class ActivityRedBook(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityRedBook, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        task_list = activity_utils.parse_task_list(conf['cTask'])
        self._task_id = task_list[0] if task_list else None
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_btn,
           'receive_task_reward_succ_event': self.refresh_btn
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        self.init_reward_widget()
        self.refresh_btn()
        self.panel.PlayAnimation('appear')

    def init_reward_widget(self):
        reward_id = task_utils.get_task_reward(self._task_id)
        init_common_reward_list(self.panel.list_item, reward_id)

    def update_reward_widget(self):
        reward_status = global_data.player.get_task_reward_status(self._task_id)
        if not (self.panel and self.panel.isValid()):
            return
        all_items = self.panel.list_item.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def refresh_btn(self, *args):
        if not self._task_id:
            return
        btn = self.panel.temp_btn.btn_common_big
        btn.SetEnable(True)
        reward_status = global_data.player.get_task_reward_status(self._task_id)
        if reward_status == ITEM_UNGAIN:
            btn.SetText(609170)

            @btn.callback()
            def OnClick(*args):
                import game3d
                if not game3d.open_url('xhsdiscover://user/64f6f0630000000004027284'):
                    game3d.open_url('https://www.xiaohongshu.com/user/profile/64f6f0630000000004027284')
                global_data.player and global_data.player.call_server_method('bind_redbook_smc', ())

        elif reward_status == ITEM_UNRECEIVED:
            btn.SetText(606010)

            @btn.callback()
            def OnClick(*args):
                global_data.player.receive_task_reward(self._task_id)

        elif reward_status == ITEM_RECEIVED:
            btn.SetText(80866)
            btn.SetEnable(False)

            @btn.callback()
            def OnClick(*args):
                import game3d
                if not game3d.open_url('xhsdiscover://user/64f6f0630000000004027284'):
                    game3d.open_url('https://www.xiaohongshu.com/user/profile/64f6f0630000000004027284')

        self.update_reward_widget()
        global_data.emgr.refresh_activity_redpoint.emit()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGodBinding.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import task_utils
from common.utils.timer import CLOCK
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.template_utils import init_common_reward_list
from logic.comsys.activity.TeachingStepsUI import TeachingStepsUI
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN

class ActivityGodBinding(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityGodBinding, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.update_btn_get_timer = None
        return

    def on_init_panel(self):
        self.init_reward_widget()
        self.init_all_btns()
        self.update_all_btns()
        self.process_event(True)
        self.panel.PlayAnimation('appear')
        global_data.player.call_server_method('req_check_god_bind_state', ())
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        if reward_status == ITEM_UNGAIN:
            self.register_timer()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_update_task_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        self.unregister_timer()
        self.update_btn_get_timer = global_data.game_mgr.register_logic_timer(self.do_update_btn_get, interval=2, mode=CLOCK)

    def unregister_timer(self):
        if self.update_btn_get_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_btn_get_timer)
            self.update_btn_get_timer = None
        return

    def do_update_btn_get(self, *args):
        if self.panel and self.panel.isValid() and self.panel.btn_go.isVisible():
            global_data.player.call_server_method('req_check_god_bind_state', ())
            self.update_all_btns()

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

    def init_all_btns(self):

        @self.panel.btn_go.unique_callback()
        def OnClick(*args):
            self.on_click_bind_btn()

        @self.panel.btn_tips.unique_callback()
        def OnClick(*args):
            self.on_click_tip_btn()

        @self.panel.btn_get.unique_callback()
        def OnClick(*args):
            self.on_click_get_btn()

    def update_all_btns(self):
        reward_status = global_data.player.get_task_reward_status(self.task_id)
        self.panel.btn_go.setVisible(reward_status == ITEM_UNGAIN)
        self.panel.btn_get.setVisible(reward_status != ITEM_UNGAIN)
        self.panel.btn_get.SetEnable(reward_status == ITEM_UNRECEIVED)
        self.panel.btn_go.SetText(80540)
        if reward_status == ITEM_RECEIVED:
            self.panel.btn_get.SetText(80866)
        else:
            self.panel.btn_get.SetText(80248)

    def on_update_task_progress(self, *args):
        self.update_all_btns()
        self.update_reward_widget()

    def on_click_bind_btn(self):
        import game3d
        game3d.open_url('neteasegl://')

    def on_click_get_btn(self):
        global_data.player.receive_task_reward(self.task_id)

    def on_click_tip_btn(self):
        ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        TeachingStepsUI(content_dict=ui_data)
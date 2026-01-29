# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520Teamup.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils, task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN

class Activity520Teamup(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(Activity520Teamup, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self.goods_id = conf.get('goods_id', None)
        return

    def on_init_panel(self):
        self.process_event(True)
        self.init_widgets()

        @self.panel.btn_common.btn_common.unique_callback()
        def OnClick(*args):
            self.on_click_btn_common()

        @self.panel.btn_click.btn_common.unique_callback()
        def OnClick(*args):
            self.on_click_btn_click()

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.update_widgets,
           'receive_task_reward_succ_event': self.update_widgets
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_click_btn_common(self, *args):
        ui = global_data.ui_mgr.show_ui('TeamHallUI', 'logic.comsys.lobby.TeamHall')
        ui and ui.select_tab(1)

    def on_click_btn_click(self, *args):
        player = global_data.player
        if not player:
            return
        global_data.player.receive_task_reward(self.task_id)

    def init_widgets(self):
        reward_id = task_utils.get_task_reward(self.task_id)
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list')
        reward_nd_list = [self.panel.temp_item]
        for idx, (item_no, item_cnt) in enumerate(reward_list):
            template_utils.init_tempate_mall_i_item(reward_nd_list[idx], item_no, 1, show_tips=True)

        self.panel.lab_task.SetString(610960)
        self.panel.btn_common.btn_common.SetText(906601)
        self.panel.lab_title_upper01.SetString(609854)
        self.panel.lab_title_upper.SetString(609855)
        self.update_widgets()

    def update_widgets(self, *args):
        player = global_data.player
        if not player:
            return
        reward_st = player.get_task_reward_status(self.task_id)
        reward_nd_list = [self.panel.temp_item]
        receive_btn = self.panel.btn_click.btn_common
        if reward_st == ITEM_UNGAIN:
            receive_btn.SetText(604031)
            receive_btn.setVisible(False)
            for reward_nd in reward_nd_list:
                reward_nd.nd_get.setVisible(False)
                reward_nd.nd_get_tips.setVisible(False)
                reward_nd.StopAnimation('get_tips')

        elif reward_st == ITEM_UNRECEIVED:
            receive_btn.SetText(606010)
            receive_btn.SetEnable(True)
            receive_btn.setVisible(True)
            for reward_nd in reward_nd_list:
                reward_nd.nd_get.setVisible(False)
                reward_nd.nd_get_tips.setVisible(True)
                reward_nd.PlayAnimation('get_tips')

        elif reward_st == ITEM_RECEIVED:
            receive_btn.SetText(80866)
            receive_btn.SetEnable(False)
            receive_btn.setVisible(True)
            for reward_nd in reward_nd_list:
                reward_nd.nd_get.setVisible(True)
                reward_nd.nd_get_tips.setVisible(False)
                reward_nd.StopAnimation('get_tips')

        if args and reward_st == ITEM_RECEIVED and self.goods_id:
            from logic.comsys.mall_ui.GroceriesUseConfirmUI import GroceriesUseConfirmUI
            global_data.ui_mgr.close_ui('GroceriesUseConfirmUI')
            ui = GroceriesUseConfirmUI(goods_id=self.goods_id, pay_num=1)
            ui and ui.set_title(get_text_by_id(80163))
            ui and ui.set_lab_success('')
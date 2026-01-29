# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommonTeamupNew.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils, task_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.widget import widget
from common.cfg import confmgr
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gutils.client_utils import post_ui_method
from logic.gutils.jump_to_ui_utils import jump_to_pve_main_ui

class ActivityCommonTeamupNew(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommonTeamupNew, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.life_timer = 0

    def on_init_panel(self):
        super(ActivityCommonTeamupNew, self).on_init_panel()
        self.process_event(True)
        self.init_widgets()

        @self.panel.btn_go.unique_callback()
        def OnClick(*args):
            self.on_click_btn_go()

        @self.panel.btn_describe.unique_callback()
        def OnClick(*args):
            rule = confmgr.get('c_activity_config', str(self._activity_type), 'cDescTextID', default='')
            title = confmgr.get('c_activity_config', str(self._activity_type), 'cNameTextID', default='')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()
        super(ActivityCommonTeamupNew, self).on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.update_widgets,
           'receive_task_reward_succ_event': self.update_widgets,
           'receive_task_prog_reward_succ_event': self.update_widgets
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        super(ActivityCommonTeamupNew, self).refresh_panel()
        self.update_widgets()

    def on_click_btn_go(self, *args):
        player = global_data.player
        if not player:
            return
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        if ui_data.get('is_pve'):
            jump_to_pve_main_ui()
            return
        ui = global_data.ui_mgr.show_ui('TeamHallUI', 'logic.comsys.lobby.TeamHall')
        ui and ui.select_tab(1)

    def init_widgets(self):
        prog_rewards = task_utils.get_prog_rewards(self.task_id)
        self.panel.list_item.SetInitCount(len(prog_rewards))
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            progress, reward_id = prog_rewards[idx]
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = reward_list[0]
            item_path = get_lobby_item_pic_by_item_no(item_no)
            reward_name = get_lobby_item_name(item_no)
            ui_item.item.SetDisplayFrameByPath('', item_path)
            ui_item.lab_quantity.setVisible(True)
            ui_item.lab_quantity.SetString(str(item_num))
            ui_item.lab_data.SetString(get_text_by_id(604004).format(idx + 1))
            ui_item.lab_name.SetString(reward_name)
            ui_item._reward_data = (progress, item_no, item_num)

        self.update_widgets()
        self.refresh_time()
        self.register_timer()

    @post_ui_method
    def update_widgets(self, *args):
        player = global_data.player
        if not player:
            return
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            progress, item_no, item_num = ui_item._reward_data
            can_receive = player.is_prog_reward_receivable(self.task_id, progress) and not player.has_receive_prog_reward(self.task_id, progress)
            is_received = player.has_receive_prog_reward(self.task_id, progress)
            if is_received:
                ui_item.nd_get.setVisible(True)
                ui_item.btn_choose.SetSelect(False)
                ui_item.StopAnimation('get_tips')
                ui_item.nd_get_tips.setVisible(False)
                ui_item.img_tips.setVisible(False)
            elif can_receive:
                ui_item.btn_choose.SetSelect(True)
                ui_item.PlayAnimation('get_tips')
                ui_item.nd_get_tips.setVisible(True)
                ui_item.img_tips.setVisible(True)
            else:
                ui_item.btn_choose.SetSelect(False)
                ui_item.StopAnimation('get_tips')
                ui_item.nd_get_tips.setVisible(False)
                ui_item.img_tips.setVisible(False)

            @ui_item.btn_choose.unique_callback()
            def OnClick(btn, touch, progress=progress, item_no=item_no, item_num=item_num, can_receive=can_receive):
                if can_receive:
                    global_data.player.receive_task_prog_reward(self.task_id, progress)
                else:
                    x, y = btn.GetPosition()
                    w, h = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    extra_info = {'show_jump': False}
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        global_data.emgr.refresh_activity_redpoint.emit()

    def refresh_time(self):
        if not self.panel or not self.panel.lab_date:
            return
        lab_time = self.panel.lab_date
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                lab_time.SetString(get_text_by_id(610105).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                lab_time.SetString(get_text_by_id(610105).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            lab_time.SetString(get_readable_time(close_left_time))

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self.life_timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_time, interval=5, mode=CLOCK)

    def unregister_timer(self):
        if self.life_timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self.life_timer)
        self.life_timer = 0
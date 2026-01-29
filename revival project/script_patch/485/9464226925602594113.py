# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNile/ActivityBingoLlkLeftRewardWidget.py
from __future__ import absolute_import
from logic.comsys.activity.widget.ActivityWidgetBase import ActivityWidgetBase
from common.cfg import confmgr
from logic.gcommon.item.lobby_item_type import L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GIFTPACKAGE, L_ITME_TYPE_GUNSKIN
from logic.gutils.item_utils import get_lobby_item_name, exec_jump_to_ui_info, get_lobby_item_type, get_lobby_item_reward_id
from logic.gutils.jump_to_ui_utils import jump_to_item_book_page
from logic.gutils.task_utils import get_task_fresh_type, get_task_name, get_total_prog
from common.uisys.uielment.CCButton import STATE_NORMAL, STATE_SELECTED, STATE_DISABLED
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_UNRECEIVED, ITEM_RECEIVED
from logic.gutils.template_utils import init_tempate_mall_i_item

class ActivityBingoLlkLeftRewardWidget(ActivityWidgetBase):
    GLOBAL_EVENT = {'on_lobby_bag_item_changed_event': 'on_item_changed',
       'receive_task_reward_succ_event': 'receive_task_reward_succ',
       'task_prog_changed': 'on_task_prog_changed',
       'refresh_random_task': 'receive_task_reward_succ'
       }

    def on_init_panel(self):
        self.activity_conf = confmgr.get('c_activity_config', self.activity_id)
        ui_data = self.activity_conf.get('cUiData')
        self.task_card = ui_data.get('task_card', 71600027)
        all_unlock_reward_id = str(ui_data['gift_list'][-1])
        self.ultimate_reward = confmgr.get('common_reward_data', all_unlock_reward_id, 'reward_list')[0][0]
        self.ultimate_reward_task = ui_data.get('final_reward_task', 1451663)
        self.update_final_reward()
        self.update_task_card()
        self.update_left_task_panel()
        chip_item_id = ui_data['chip_item_id']
        init_tempate_mall_i_item(self.panel.nd_content.nd_task.temp_task.nd_vx.temp_item, chip_item_id, 1, show_tips=True, show_rare_degree=False)

        @self.panel.btn_look.callback()
        def OnClick(btn, touch):
            reward_type = get_lobby_item_type(self.ultimate_reward)
            if reward_type == L_ITEM_YTPE_VEHICLE_SKIN:
                jump_to_item_book_page('2', self.ultimate_reward)
            elif reward_type == L_ITME_TYPE_GUNSKIN:
                jump_to_item_book_page('3', self.ultimate_reward)
            elif reward_type == L_ITEM_TYPE_GIFTPACKAGE:
                dlg = global_data.ui_mgr.show_ui('MultiChosenSingleRewardUI', 'logic.comsys.reward')
                dlg and dlg.set_use_params({'id': None,'item_no': self.ultimate_reward,'quantity': 1}, [], [])
                dlg and dlg.set_btn_use_visible(False)
            else:
                from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                jump_to_display_detail_by_item_no(self.ultimate_reward)
            return

    def on_item_changed(self, *args):
        self.update_task_card()

    def receive_task_reward_succ(self, *args):
        self.update_left_task_panel()
        self.update_final_reward()

    def update_task_card(self):
        from logic.gcommon.item import item_utility as iutil
        item_data = iutil.get_lobby_item_data(self.task_card)
        ui_data = self.activity_conf.get('cUiData')
        random_task_id = str(ui_data['random_task_id'])
        reward_num = global_data.player.get_random_task_reward_cnt(random_task_id)
        max_stack_num = item_data.get('max_stack_num', 1)
        self.panel.lab_got.SetString(get_text_by_id(635539, [str(reward_num), str(max_stack_num)]))

    def on_finalize_panel(self):
        super(ActivityBingoLlkLeftRewardWidget, self).on_finalize_panel()
        self.activity_conf = {}

    def update_final_reward(self):
        state = global_data.player.get_task_reward_status(self.ultimate_reward_task)
        can_receive = state == ITEM_UNRECEIVED
        ultimate_reward_gain = can_receive
        self.panel.lab_type.SetString(get_text_by_id(80953 if ultimate_reward_gain else 906662))
        if can_receive:
            self.panel.btn_get.setVisible(True)
            self.panel.btn_get.SetText(610637)
            self.panel.btn_get.SetEnable(True)
        elif state == ITEM_UNGAIN:
            self.panel.btn_get.setVisible(False)
        else:
            self.panel.btn_get.setVisible(True)
            self.panel.btn_get.SetText(80866)
            self.panel.btn_get.SetEnable(False)

        @self.panel.btn_get.callback()
        def OnClick(btn, touch):
            if global_data.player:
                can_receive = global_data.player.get_task_reward_status(self.ultimate_reward_task) == ITEM_UNRECEIVED
                if can_receive:
                    global_data.player.receive_task_reward(self.ultimate_reward_task)
                    self.panel.btn_get.SetText(80866)
                    self.panel.btn_get.SetEnable(False)

        self.update_task_card()

    def update_left_task_panel(self, *args):
        from logic.gutils.task_utils import try_do_jump, get_jump_conf
        ui_data = self.activity_conf.get('cUiData', {})
        random_task_id = str(ui_data['random_task_id'])
        random_refresh_type = get_task_fresh_type(random_task_id)
        random_task_list = global_data.player.get_random_children_tasks(random_refresh_type, random_task_id)
        item = self.panel.nd_content.nd_task.temp_task
        if not random_task_list or global_data.player.get_random_task_reward_cnt(random_task_id) >= 3:
            log_error('ActivityBingoLianliankan has no random children tasks!')
            random_task_list = []
            item.temp_btn.setVisible(False)
            item.temp_btn.btn_common.SetText(634330)
            item.lab_task.SetString(635415)
            item.temp_btn.btn_common.SetEnable(False)
            item.lab_schedule.SetString('')
            return
        else:
            random_task_list.sort()
            child_task = random_task_list[0]
            item.lab_task.SetString(get_task_name(child_task))
            if global_data.player.is_task_finished(child_task):
                prog_text_color = '%s'
            else:
                prog_text_color = '<color=0xf42551FF>%s</color>'
            item.lab_schedule.SetString((prog_text_color + '/%s') % (global_data.player.get_task_prog(child_task), get_total_prog(child_task)))
            text_id_list = (80930, 604027, 906669, 906672)
            task_state = STATE_SELECTED
            if global_data.player.is_task_finished(child_task):
                if global_data.player.has_unreceived_task_reward(child_task):
                    task_state = STATE_NORMAL
                else:
                    task_state = STATE_DISABLED
            text_id = text_id_list[task_state]
            btn_enable = task_state == STATE_NORMAL
            jump_conf = None
            if task_state == STATE_SELECTED:
                jump_conf = get_jump_conf(child_task)
                if jump_conf:
                    text_id = jump_conf.get('unreach_text', None) or text_id_list[-1]
                    btn_enable = True
            item.temp_btn.setVisible(True)
            item.temp_btn.btn_common.SetText(text_id)
            item.temp_btn.btn_common.SetEnable(btn_enable)
            item.temp_btn.btn_common._updateCurState(task_state)

            @item.temp_btn.btn_common.callback()
            def OnClick(btn, touch, child_task=child_task, task_state=task_state, jump_conf=jump_conf):
                if task_state == STATE_NORMAL:
                    global_data.player.receive_task_reward(child_task)
                elif task_state == STATE_SELECTED:
                    exec_jump_to_ui_info(jump_conf)

            return

    def on_task_prog_changed(self, changes):
        for change in changes:
            if str(self.ultimate_reward_task) == str(change.task_id):
                self.update_final_reward()
                break
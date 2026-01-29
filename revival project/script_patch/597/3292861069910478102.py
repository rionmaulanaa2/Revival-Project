# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommunityWelfare.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import init_common_reward_list
UNENABLE_BTN_ICON = 'gui/ui_res_2/common/button/btn_secondary_minor.png'

class ActivityCommunityWelfare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommunityWelfare, self).__init__(dlg, activity_type)
        self.cur_sel_task_btn = None
        self._show_task_ids = []
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        return

    def on_init_panel(self):
        self.init_all_widgets()
        self.process_event(True)
        self.process_init_bind_condition()

    def on_finalize_panel(self):
        self.process_event(False)
        self.cur_sel_task_btn = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_update_task_progress,
           'on_bind_mobile_phone_succ_event': self.on_bind_mobile_phone_succ,
           'realname_state_change': self.on_realname_result
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def process_init_bind_condition(self):
        if global_data.channel:
            bind_type = global_data.channel.get_phone_bind_type()
            if bind_type == 2 or bind_type == 3:
                global_data.player.call_server_method('bind_mobile_phone_in_community', ())
        if global_data.player:
            if global_data.player.is_realname():
                self.on_realname_result()

    def init_all_widgets(self):
        temp_list_task = self.panel.temp_list_task
        temp_list_task.DeleteAllSubItem()
        children_task_id_list = task_utils.get_children_task(self.task_id)
        show_task_ids = []
        cur_channel = global_data.channel.get_name()
        for task_id in children_task_id_list:
            task_args = task_utils.get_task_arg(task_id)
            channel_limits = task_args.get('channel_limit', None)
            if not channel_limits:
                show_task_ids.append(task_id)
            elif cur_channel in channel_limits:
                show_task_ids.append(task_id)

        self._show_task_ids = show_task_ids
        temp_list_task.SetInitCount(len(show_task_ids))
        for idx, task_id in enumerate(show_task_ids):
            ui_item = temp_list_task.GetItem(idx)
            self.init_binding_detail_info(ui_item, task_id)
            self.init_task_reward(ui_item, task_id)
            self.init_list_item_btn(ui_item)
            self.init_receive_and_bind_btn(ui_item, task_id)
            self.update_binding_status(ui_item, task_id)

        return

    def init_binding_detail_info(self, ui_item, task_id):
        task_args = task_utils.get_task_arg(task_id)
        icon_path = task_args.get('icon_path', '')
        title_text_id = task_args.get('title_text_id', '')
        explain_text_id = task_args.get('explain_text_id', '')
        ui_item.lab_binding_icon.SetDisplayFrameByPath('', icon_path)
        ui_item.lab_binding_content.SetString(get_text_by_id(title_text_id))
        ui_item.lab_reward.SetString(get_text_by_id(explain_text_id))

    def update_binding_status(self, ui_item, task_id):
        task_args = task_utils.get_task_arg(task_id)
        update_method_name = task_args.get('update_method', 'empty_click_method')
        update_method = getattr(self, update_method_name)
        if update_method and callable(update_method):
            update_method(ui_item, task_id)
        reward_status = global_data.player.get_task_reward_status(task_id)
        all_items = ui_item.temp_list_reward_item.GetAllItem()
        for item in all_items:
            item.nd_get.setVisible(reward_status == ITEM_RECEIVED)

    def update_mobile_phone_bind_ui_item(self, ui_item, task_id):
        reward_status = global_data.player.get_task_reward_status(task_id)
        ui_item.img_mask.setVisible(False)
        ui_item.img_sevendays_get.setVisible(False)
        ui_item.temp_btn.setVisible(reward_status != ITEM_UNRECEIVED)
        if reward_status == ITEM_RECEIVED:
            ui_item.temp_btn.btn_major.SetText(get_text_by_id(607709))
            ui_item.temp_btn.btn_major.SetFrames('', [UNENABLE_BTN_ICON, UNENABLE_BTN_ICON, UNENABLE_BTN_ICON], False, None)
        else:
            ui_item.temp_btn.btn_major.SetText(get_text_by_id(607705))
        ui_item.temp_btn_2.setVisible(reward_status == ITEM_UNRECEIVED)
        return

    def update_real_name_ui_item(self, ui_item, task_id):
        reward_status = global_data.player.get_task_reward_status(task_id)
        ui_item.img_mask.setVisible(False)
        ui_item.img_sevendays_get.setVisible(False)
        ui_item.temp_btn.setVisible(reward_status == ITEM_UNGAIN)
        ui_item.temp_btn_2.setVisible(reward_status != ITEM_UNGAIN)
        ui_item.temp_btn_2.btn_major.SetEnable(reward_status == ITEM_UNRECEIVED)
        if reward_status == ITEM_UNRECEIVED:
            ui_item.temp_btn_2.btn_major.SetText(get_text_by_id(80248))
        elif reward_status == ITEM_RECEIVED:
            ui_item.temp_btn_2.btn_major.SetText(get_text_by_id(80866))
        elif reward_status == ITEM_UNGAIN:
            pass

    def init_receive_and_bind_btn(self, ui_item, task_id):
        task_args = task_utils.get_task_arg(task_id)
        click_method_name = task_args.get('click_method', 'empty_click_method')
        btn_text_id = task_args.get('btn_text_id')

        @ui_item.temp_btn.btn_major.unique_callback()
        def OnClick(btn, touch):
            click_method = getattr(self, click_method_name)
            click_method()

        @ui_item.temp_btn_2.btn_major.unique_callback()
        def OnClick(btn, touch):
            global_data.player.receive_task_reward(task_id)

        if btn_text_id:
            ui_item.temp_btn.btn_major.SetText(get_text_by_id(btn_text_id))
        ui_item.temp_btn_2.btn_major.SetText(get_text_by_id(10320))

    def init_list_item_btn(self, ui_item):
        ui_item.btn_task.SetSelect(False)
        ui_item.btn_help.setVisible(False)

        @ui_item.btn_task.unique_callback()
        def OnClick(btn, touch):
            self.cur_sel_task_btn and self.cur_sel_task_btn.SetSelect(False)
            self.cur_sel_task_btn = btn
            self.cur_sel_task_btn.SetSelect(True)

    def init_task_reward(self, ui_item, task_id):
        reward_id = task_utils.get_task_reward(task_id)
        init_common_reward_list(ui_item.temp_list_reward_item, reward_id)

    def on_click_bind_mobile_phone_btn(self, *args):
        if not global_data.channel:
            return
        global_data.channel.bind_mobile_phone(1)

    def on_click_real_name_btn(self, *args):
        if not global_data.player:
            return
        if global_data.player.is_realname():
            return
        global_data.player.show_realname_dialog()

    def empty_click_method(self, *args):
        pass

    def on_update_task_progress(self, *args):
        temp_list_task = self.panel.temp_list_task
        children_task_id_list = self._show_task_ids
        for idx, task_id in enumerate(children_task_id_list):
            ui_item = temp_list_task.GetItem(idx)
            self.update_binding_status(ui_item, task_id)

    def on_bind_mobile_phone_succ(self, status):
        if global_data.player and status == 1:
            global_data.player.call_server_method('bind_mobile_phone_in_community', ())

    def on_realname_result(self, *args):
        if global_data.player:
            global_data.player.call_server_method('real_name_in_community', ())
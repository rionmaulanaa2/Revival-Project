# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivDailyGift.py
from __future__ import absolute_import
import six
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from logic.gutils import template_utils
from logic.gutils import task_utils
from logic.gutils import mall_utils
import cc
from logic.gutils import jump_to_ui_utils

class ActivityAnnivDailyGift(ActivityBase):
    TASK_ID_ANNIV_CHARGE = '1411068'
    TASK_ID_ANNIV_7DAY = '1411060'

    def __init__(self, dlg, activity_type):
        super(ActivityAnnivDailyGift, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def init_parameters(self):
        self._timer = 0
        self._parent_task_id = self.TASK_ID_ANNIV_7DAY
        self._children_task_list = task_utils.get_children_task(self._parent_task_id)
        self._task_id_to_reward_ui_dict = {}
        self._task_id_to_day_num = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.on_update_task_progress,
           'anniv_charge_task_finished_event': self.on_anniv_charge_task_finished
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        self.init_reward_widget()
        self.update_time_widget()
        self.update_charge_btn()
        self.update_other_widgets()
        self.panel.PlayAnimation('loop')
        conf = task_utils.get_task_conf_by_id(self.TASK_ID_ANNIV_CHARGE)
        start_time = tutil.get_date_str('%Y.%m.%d', conf.get('start_time', 0))
        end_time = tutil.get_date_str('%Y.%m.%d', conf.get('end_time', 0))
        self.panel.lab_charge_time.SetString(get_text_by_id(609190).format(start_time, end_time))
        self.panel.btn_des.BindMethod('OnClick', self.on_click_btn_desc)

    def on_finalize_panel(self):
        self.process_event(False)

    def init_reward_widget(self):
        reward_node_list_1_6 = self.panel.nd_reward.list_sign_6
        reward_node_7 = self.panel.nd_reward.list_sign_7
        self._task_id_to_reward_ui_dict = {}
        for i, task_id in enumerate(self._children_task_list):
            if i == 6:
                self._task_id_to_reward_ui_dict[task_id] = reward_node_7
                self._task_id_to_day_num[task_id] = 7
            else:
                if i >= reward_node_list_1_6.GetItemCount():
                    log_error('[ERROR] ActivityAnnivDailyGift task count [%s] not match ui count [%s].', i, reward_node_list_1_6.GetItemCount())
                    return
                reward_node = self.panel.nd_reward.list_sign_6.GetItem(i)
                if reward_node:
                    self._task_id_to_reward_ui_dict[task_id] = reward_node
                    self._task_id_to_day_num[task_id] = i + 1

        for task_id in six.iterkeys(self._task_id_to_reward_ui_dict):
            self.update_task_ui(task_id)

    def update_task_ui(self, task_id):
        reward_ui = self._task_id_to_reward_ui_dict.get(task_id)
        if not reward_ui:
            return
        reward_list = task_utils.get_task_reward_list(task_id)
        if not reward_list:
            return
        first_item_info = reward_list[0]
        item_no, item_num = first_item_info[0], first_item_info[1]
        receive_state = global_data.player.get_task_reward_status(task_id)
        if receive_state == ITEM_UNGAIN:
            template_utils.init_tempate_mall_i_item(reward_ui.temp_item, item_no, item_num=item_num, show_tips=True)
            reward_ui.temp_item.nd_get_tips.setVisible(False)
            reward_ui.temp_item.nd_get.setVisible(False)
            reward_ui.temp_item.StopAnimation('get_tips')
        elif receive_state == ITEM_UNRECEIVED:

            def callback():
                global_data.player.receive_task_reward(task_id)

            template_utils.init_tempate_mall_i_item(reward_ui.temp_item, item_no, item_num=item_num, callback=callback)
            reward_ui.temp_item.nd_get_tips.setVisible(True)
            reward_ui.temp_item.PlayAnimation('get_tips')
            reward_ui.temp_item.nd_get.setVisible(False)
        elif receive_state == ITEM_RECEIVED:
            reward_ui.temp_item.StopAnimation('get_tips')
            template_utils.init_tempate_mall_i_item(reward_ui.temp_item, item_no, item_num=item_num, show_tips=True)
            reward_ui.temp_item.nd_get_tips.setVisible(False)
            reward_ui.temp_item.nd_get.setVisible(True)
        reward_ui.lab_name.SetString(mall_utils.get_lobby_item_name(item_no))
        day_num = self._task_id_to_day_num.get(task_id, 0)
        reward_ui.lab_day.SetString(get_text_by_id(604004).format(day_num))

    def on_click_btn_desc(self, btn, touch):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(607353), get_text_by_id(607363))
        x, y = btn.GetPosition()
        wpos = btn.GetParent().ConvertToWorldSpace(x, y)
        dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def on_update_task_progress(self, task_id):
        global_data.player.read_activity_list(self._activity_type)
        self.update_task_ui(task_id)
        self.update_charge_btn()
        self.update_time_widget()
        self.update_other_widgets()

    def on_anniv_charge_task_finished(self):
        self.init_reward_widget()
        self.update_charge_btn()
        self.update_time_widget()
        self.update_other_widgets()

    def update_time_widget(self):
        is_finished = global_data.player.is_task_finished(self.TASK_ID_ANNIV_CHARGE)
        if is_finished:
            end_time = global_data.player.get_anniv_7day_task_end_time()
            start_time = end_time - tutil.ONE_WEEK_SECONDS * 2
            start_date = tutil.get_date_str('%Y.%m.%d', start_time)
            finish_date = tutil.get_date_str('%m.%d', end_time)
            self.panel.lab_get_time_2.SetString(get_text_by_id(609193).format(start_date, finish_date))
            self.panel.lab_get_time_1.setVisible(False)
            self.panel.lab_get_time_2.setVisible(True)
        else:
            conf = task_utils.get_task_conf_by_id(self.TASK_ID_ANNIV_CHARGE)
            start_time = tutil.get_date_str('%Y.%m.%d', conf.get('start_time', 0))
            end_time = conf.get('end_time', 0) + tutil.ONE_WEEK_SECONDS * 2
            end_time = tutil.get_date_str('%Y.%m.%d', end_time)
            self.panel.lab_get_time_1.SetString(get_text_by_id(609193).format(start_time, end_time))
            self.panel.lab_get_time_1.setVisible(True)
            self.panel.lab_get_time_2.setVisible(False)

    def update_charge_btn(self):
        btn_charge = self.panel.btn_get
        is_finished = global_data.player.is_task_finished(self.TASK_ID_ANNIV_CHARGE)
        if not is_finished:

            def on_click_charge(btn, touch):
                if not task_utils.is_task_open(self.TASK_ID_ANNIV_CHARGE):
                    return
                if global_data.is_pc_mode:
                    jump_to_ui_utils.jump_to_charge()
                else:
                    goods_info = global_data.lobby_mall_data.get_activity_sale_info('ANNIV_CHARGE_GOODS')
                    if goods_info:
                        global_data.player and global_data.player.pay_order(goods_info['goodsid'])

            btn_charge.SetEnable(True)
            btn_charge.SetText(get_text_by_id(609191).format(60))
            btn_charge.BindMethod('OnClick', on_click_charge)
        else:
            cur_unreceived_task_list = self.get_cur_unreceived_reward_task_list()
            if len(cur_unreceived_task_list) > 0:

                def on_click_charge(btn, touch):
                    for task_id in cur_unreceived_task_list:
                        global_data.player.receive_task_reward(task_id)

                btn_charge.SetEnable(True)
                btn_charge.SetText(get_text_by_id(80930))
                btn_charge.BindMethod('OnClick', on_click_charge)
            else:
                btn_charge.SetEnable(False)
                btn_charge.SetText(get_text_by_id(80866))

    def update_other_widgets(self):
        is_finished = global_data.player.is_task_finished(self.TASK_ID_ANNIV_CHARGE)
        if is_finished:
            self.panel.lab_get.setVisible(False)
            self.panel.lab_charge_time.setVisible(False)
            self.panel.img_get_bar.setVisible(False)
        else:
            self.panel.lab_get.lab_num.SetString(str(60))
            self.panel.lab_get.setVisible(True)
            self.panel.lab_charge_time.setVisible(True)
            self.panel.img_get_bar.setVisible(True)

    def get_cur_unreceived_reward_task_list(self):
        ret_list = []
        for task_id in self._children_task_list:
            if global_data.player.get_task_reward_status(task_id) == ITEM_UNRECEIVED:
                ret_list.append(task_id)

        return ret_list

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def second_callback(self):
        end_time = global_data.player.get_anniv_7day_task_end_time()
        now = tutil.get_server_time()
        left_time = end_time - now
        if left_time > 0:
            self.panel.lab_get_time_2.SetString(tutil.get_readable_time(left_time))
            self.panel.lab_get_time_2.setVisible(True)
        else:
            self.panel.lab_get_time_2.setVisible(False)
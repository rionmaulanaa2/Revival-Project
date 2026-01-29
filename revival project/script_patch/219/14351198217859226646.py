# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/AsyncChooseRewardTaskListWidget.py
from __future__ import absolute_import
from six.moves import range
from .Widget import Widget
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree
from logic.gutils.mall_utils import is_pc_global_pay, limite_pay, is_steam_pay, get_pc_charge_price_str, get_charge_price_str, adjust_price, get_goods_item_reward_id, get_mall_item_price_list, get_goods_limit_num_all
from logic.gutils.task_utils import get_task_name, get_task_conf_by_id, get_total_prog, get_children_task, get_raw_left_open_time, get_task_temp_id
from logic.gutils.template_utils import init_common_reward_list, init_tempate_mall_i_item, get_reward_list_by_reward_id
from logic.gutils.activity_utils import get_left_time, is_activity_in_limit_time
from logic.gcommon.common_const.task_const import CHARGE_TASK_TEMP_ID
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils.jump_to_ui_utils import jump_to_charge, jump_to_web_charge

class AsyncChooseRewardTaskListWidget(Widget):

    def on_init_panel(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        self.task_id = conf.get('cTask', '')
        self.charge_task_list = get_children_task(self.task_id)
        self.charge_task_count = len(self.charge_task_list)
        self.choose_reward_btn_dict = {}
        self.choose_reward_dict = {}
        self.process_event(True)
        self.init_daliy_charge_list()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_charge_task,
           'buy_good_success': self.update_charge_list,
           'task_prog_changed': self.update_charge_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_daliy_charge_list(self):
        self.panel.act_list.BindMethod('OnCreateItem', self.init_daliy_charge_item)
        self.panel.act_list.DeleteAllSubItem()
        self.panel.act_list.SetInitCount(self.charge_task_count)
        self.panel.act_list.scroll_Load()

    def init_daliy_charge_item(self, lv, idx, item):
        task_id = self.charge_task_list[idx]
        prog = get_total_prog(task_id)
        if G_IS_NA_USER:
            txt = get_text_by_id(633779).format(prog * 10)
        else:
            txt = get_text_by_id(633778).format(prog)
        item.lab_name.SetString(txt)
        select_rewards = get_task_conf_by_id(str(task_id)).get('select_rewards', [])
        if not select_rewards or len(select_rewards) < 2:
            return
        first_reward = get_reward_list_by_reward_id(select_rewards[0])
        item_no, item_num = first_reward[0]
        init_tempate_mall_i_item(item.temp_item, item_no, item_num=item_num, show_tips=False)
        item.temp_item.btn_choose.BindMethod('OnClick', lambda btn, touch, idx=idx, reward=select_rewards[0]: self.on_click_btn_choose(btn, idx, reward))
        second_reward = get_reward_list_by_reward_id(select_rewards[1])
        item_no, item_num = second_reward[0]
        init_tempate_mall_i_item(item.temp_item_2, item_no, item_num=item_num, show_tips=False)
        item.temp_item_2.btn_choose.BindMethod('OnClick', lambda btn, touch, idx=idx, reward=select_rewards[1]: self.on_click_btn_choose(btn, idx, reward))
        item.temp_btn_get.btn_common.BindMethod('OnClick', lambda btn, touch, task_id=task_id, idx=idx: self.on_click_btn_receive(btn, task_id, idx))
        self.update_receive_btn(item.temp_btn_get.btn_common, task_id, idx)
        self.update_choose_btn(task_id, item)
        self.update_task_prog_num(task_id, item)

    def update_charge_list(self, *args):
        for idx in range(len(self.charge_task_list)):
            self.update_charge_task(self.charge_task_list[idx])

    def update_charge_task(self, task_id):
        if task_id in self.charge_task_list:
            idx = self.charge_task_list.index(task_id) if 1 else -1
            if idx == -1:
                return
            item = self.panel.act_list.GetItem(idx)
            return item or None
        self.update_receive_btn(item.temp_btn_get.btn_common, task_id, idx)
        self.update_choose_btn(task_id, item)
        self.update_task_prog_num(task_id, item)
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_receive_btn(self, btn, task_id, idx):
        player = global_data.player
        if not player:
            return
        task_state = player.get_task_reward_status(task_id)
        if task_state == ITEM_UNGAIN:
            btn.SetSelect(False)
            btn.SetEnable(True)
            btn.SetText(80961)
        elif task_state == ITEM_RECEIVED:
            btn.SetEnable(False)
            btn.SetText(80866)
        else:
            if self.choose_reward_btn_dict.get(idx):
                btn.SetText(80930)
            else:
                btn.SetText(634012)
            btn.SetSelect(True)
            btn.SetEnable(True)

    def update_choose_btn(self, task_id, item):
        player = global_data.player
        if not player:
            return
        task_state = player.get_task_reward_status(task_id)
        if task_state == ITEM_RECEIVED:
            reward_id = player.get_task_select_reward_id(task_id)
            select_rewards = get_task_conf_by_id(str(task_id)).get('select_rewards', [])
            btn_list = [item.temp_item, item.temp_item_2]
            for idx in range(len(select_rewards)):
                if reward_id == select_rewards[idx]:
                    btn_list[idx].nd_get.setVisible(True)
                btn_list[idx].nd_lock.setVisible(True)
                btn_list[idx].btn_choose.SetShowEnable(True)

        else:
            item.temp_item.nd_lock.setVisible(False)
            item.temp_item_2.nd_lock.setVisible(False)
            item.temp_item.nd_get.setVisible(False)
            item.temp_item_2.nd_get.setVisible(False)
            item.temp_item.btn_choose.SetShowEnable(True)
            item.temp_item_2.btn_choose.SetShowEnable(True)

    def update_task_prog_num(self, task_id, item):
        player = global_data.player
        if not player:
            return
        now_prog = player.get_task_prog(task_id)
        total_prog = get_total_prog(task_id)
        if G_IS_NA_USER and get_task_temp_id(task_id) == CHARGE_TASK_TEMP_ID:
            now_prog *= 10
            total_prog *= 10
        item.lab_num.SetString('{}/{}'.format(now_prog, total_prog))

    def on_click_btn_choose(self, btn, idx, reward):
        player = global_data.player
        if not player:
            return
        else:
            task_id = self.charge_task_list[idx]
            task_state = player.get_task_reward_status(task_id)

            def show_details():
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': True}
                item_no, item_num = get_reward_list_by_reward_id(reward)[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

            if task_state != ITEM_UNRECEIVED:
                show_details()
                return
            select_btn = self.choose_reward_btn_dict.get(idx, None)
            if select_btn:
                select_btn.SetShowEnable(True)
            if select_btn == btn:
                show_details()
            btn.SetShowEnable(False)
            self.choose_reward_btn_dict[idx] = btn
            self.choose_reward_dict[idx] = reward
            self.update_receive_btn(self.panel.act_list.GetItem(idx).temp_btn_get.btn_common, self.charge_task_list[idx], idx)
            return

    def on_click_btn_receive(self, btn, task_id, idx):
        player = global_data.player
        if not player:
            return
        else:
            task_state = player.get_task_reward_status(task_id)
            if task_state == ITEM_UNGAIN:
                jump_to_charge(tab_idx=0)
            else:
                if task_state == ITEM_RECEIVED:
                    return
                reward_id = self.choose_reward_dict.get(idx, None)
                if not reward_id:
                    global_data.game_mgr.show_tip(get_text_by_id(633795))
                    return
                param = {'reward_id': reward_id}
                global_data.player.receive_task_reward(task_id, param)
            return

    def on_finalize_panel(self):
        self.process_event(False)
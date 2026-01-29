# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturnMechaGift.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollectNew import ActivityCollectNew
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import task_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_INACTIVE, BTN_ST_OVERDUE
from logic.gutils import mall_utils
from logic.gcommon.common_const.activity_const import ACTIVITY_EXCLUSIVE_MECHA
import os
from logic.gcommon.time_utility import get_server_time
import social

class ActivityNewReturnMechaGift(ActivityCollectNew):
    MECHA_DISPLAY_PATH = 'gui/ui_res_2/battle_mech_call_pic'
    UI_ACTION_EVENT = {'panel.nd_content.nd_lock.OnClick': 'choose_mecha',
       'panel.nd_content.nd_lock.btn_choose.OnClick': 'choose_mecha'
       }

    def __init__(self, dlg, activity_type):
        super(ActivityNewReturnMechaGift, self).__init__(dlg, activity_type)
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        act_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.max_prog_promote_count = act_data.get('max_prog_count', 10)
        self.mecha_choose_item_id = act_data.get('mecha_choose_item_id', None)
        self.prog_promote_item_id = act_data.get('prog_promote_item_id', None)
        self.mecha_try_item_id = act_data.get('mecha_try_item_id', None)
        self.fixed_task_id = act_data.get('daily', None)
        self.week_task_id = act_data.get('weekend', None)
        self.prog_task_id = act_data.get('prog', None)
        self.try_mecha_task_id = act_data.get('try_mecha_task', None)
        self.mecha_use_params = confmgr.get('lobby_item', str(self.mecha_choose_item_id), default={})['use_params']
        self.mecha_reward_id_list = self.mecha_use_params['reward_list']
        self.prog_task_config = confmgr.get('task/task_data', self.prog_task_id, 'args', default={})
        self.reward_change_config = self.prog_task_config.get('reward_change_config', {})
        self.time_gap = 86400
        self._close_time = global_data.player.activity_closetime_data.get(self._activity_type, get_server_time())
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.on_task_prog_changed,
           'update_task_content_event': self.on_content_change,
           'on_lobby_bag_item_changed_event': self.on_bag_item_change,
           'receive_task_prog_reward_succ_event': self._on_update_reward,
           'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_bag_item_change(self, *args):
        self.auto_use_reward()
        num = global_data.player.get_item_num_by_no(int(self.prog_promote_item_id))
        self.bar_prog.lab_tips.setString(get_text_by_id(80860) + str(num))
        prog = global_data.player.get_task_prog(self.prog_task_id)
        max_prog = task_utils.get_total_prog(self.prog_task_id)
        if num > 0 and prog < max_prog:
            self.panel.nd_content.nd_unlock.btn_up.SetEnable(True)
        else:
            self.panel.nd_content.nd_unlock.btn_up.SetEnable(False)

    def on_task_prog_changed(self, *args):
        self.auto_recv_reward()
        self.update_prog()

    def on_init_panel(self):
        self.act_list_daily = self.panel.list_item.GetItem(0).act_list_common
        self.act_list_weekend = self.panel.list_item.GetItem(0).act_list_common_2
        self._daily_tasks = self.reorder_task_list(self.get_daily_tasks())
        self._weekend_tasks = self.reorder_task_list(self.get_weekend_tasks())
        self._children_tasks = self.reorder_task_list(self._daily_tasks + self._weekend_tasks)
        self.valid_tasks = self.filter_valid(self._children_tasks)
        self.bar_prog = self.panel.nd_content.nd_unlock.bar_prog
        self.list_reward = self.bar_prog.list_reward
        self.show_list()
        self.init_describe()
        self.init_mecha_choose()
        self.init_ui_event()
        self.update_prog()
        self.panel.list_item.setVisible(True)
        self.auto_actions()
        self._refresh_left_time()

    def _refresh_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self.panel.lab_time.SetString(day_txt)

    def on_content_change(self, *args):
        self.init_mecha_choose()
        self.auto_actions()

    def update_prog_reward(self):
        self.list_reward.SetInitCount(2)
        rewards_dic = task_utils.get_prog_rewards_detail_in_dict(self.prog_task_id)
        keys = six_ex.keys(rewards_dic)
        prog = global_data.player.get_task_prog(self.prog_task_id)
        for i in range(2):
            item_widget = self.list_reward.GetItem(i)
            tmp_target_prog = keys[i]
            reward_status = self.get_reward_status(tmp_target_prog, prog)
            tmp_reward_info = rewards_dic.get(tmp_target_prog)
            self.update_reward_item_state(item_widget, reward_status, tmp_reward_info, tmp_target_prog)
            item_widget.lab_rate.setString(str(tmp_target_prog))

    def get_reward_status(self, target_prog, tmp_prog):
        if tmp_prog < target_prog:
            return ITEM_UNGAIN
        else:
            if global_data.player.has_receive_prog_reward(str(self.prog_task_id), target_prog):
                return ITEM_RECEIVED
            return ITEM_UNRECEIVED

    def update_reward_item_state(self, item_node, receive_state, tmp_reward_info, target_prog):
        reward_id, reward_count = tmp_reward_info[1][0]
        if receive_state == ITEM_UNGAIN:
            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, show_tips=True)
            item_node.nd_get_tips.setVisible(False)
            item_node.nd_get.setVisible(False)
            item_node.StopAnimation('get_tips')
        elif receive_state == ITEM_UNRECEIVED:

            def callback():
                global_data.player.receive_task_prog_reward(str(self.prog_task_id), target_prog)

            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, callback=callback)
            item_node.nd_get_tips.setVisible(True)
            item_node.PlayAnimation('get_tips')
            item_node.nd_get.setVisible(False)
        elif receive_state == ITEM_RECEIVED:
            item_node.StopAnimation('get_tips')
            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, show_tips=True)
            item_node.nd_get_tips.setVisible(False)
            item_node.nd_get.setVisible(True)

    def init_ui_event(self):

        @self.panel.nd_content.nd_unlock.btn_up.unique_callback()
        def OnClick(*args):
            self.promote_prog()

        @self.panel.btn_h5.unique_callback()
        def OnClick(*args):
            from logic.gutils import jump_to_ui_utils
            key = 'v7l90YM95v6pRAVSAseygOAnpT3ObxWw'
            data_id = str(ACTIVITY_EXCLUSIVE_MECHA)
            web_url = 'https://interact2.webapp.163.com/g93jijia'
            inner_web_url = 'https://test-interact2.webapp.163.com/g93jijia'
            jump_to_ui_utils.jump_to_share_website(key, data_id, web_url, inner_web_url)

    def init_mecha_choose(self):
        change_times = global_data.player.get_task_content(self.prog_task_id, 'change_times') or {}
        if change_times.get('1000', 0) == 0:
            channel = social.get_channel()
            is_steam_channel = channel and channel.name == 'steam'
            if G_IS_NA_PROJECT or is_steam_channel:
                self.panel.btn_h5.setVisible(False)
            else:
                self.panel.btn_h5.setVisible(True)
            self.panel.nd_content.nd_lock.setVisible(True)

            @self.panel.nd_content.nd_lock.callback()
            def OnClick(*args):
                self.choose_mecha()

            @self.panel.nd_content.nd_lock.btn_choose.unique_callback()
            def OnClick(*args):
                self.choose_mecha()

        else:
            self.panel.btn_h5.setVisible(False)
            pre_choose_reward = global_data.player.get_task_content(self.prog_task_id, 'pre_choose_reward') or {}
            choose_idx = pre_choose_reward.get('1000', 0)
            reward_conf = confmgr.get('common_reward_data', str(self.mecha_reward_id_list[choose_idx]))
            item_id, item_num = reward_conf['reward_list'][0]
            mecha_dict = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content')
            fashion_id = mecha_dict.get(str(item_id), {}).get('default_fashion', None)
            self.panel.nd_content.nd_lock.setVisible(False)
            nd_unlock = self.panel.nd_unlock
            nd_unlock.setVisible(True)
            nd_unlock.btn_switch.setVisible(False)
            path = os.path.join(self.MECHA_DISPLAY_PATH, str(fashion_id[0]) + '.png')
            if fashion_id[0] == 201802400:
                nd_unlock.img_mecha.SetPosition('50%17', '50%42')
            nd_unlock.img_mecha.SetDisplayFrameByPath('', path)
        return

    def update_prog(self, *args):
        prog = global_data.player.get_task_prog(self.prog_task_id)
        max_prog = task_utils.get_total_prog(self.prog_task_id)
        percent = float(prog) / max_prog
        percent = min(1, percent)
        self.bar_prog.prog.SetPercent(percent * 100)
        self.bar_prog.lab_prog.setString('%s/%s' % (prog, max_prog))
        num = global_data.player.get_item_num_by_no(int(self.prog_promote_item_id))
        if num > 0 and prog < max_prog:
            self.panel.nd_content.nd_unlock.btn_up.SetEnable(True)
        else:
            self.panel.nd_content.nd_unlock.btn_up.SetEnable(False)
        if prog == max_prog:
            self.panel.nd_content.nd_unlock.btn_up.lab_btn.setString(get_text_by_id(80866))
            self.panel.nd_content.nd_unlock.lab_btn_tips.setVisible(False)
        self.bar_prog.lab_tips.setString(get_text_by_id(80860) + str(num))
        self.update_prog_reward()

    def choose_mecha(self):
        ui = global_data.ui_mgr.show_ui('RecallMechaChooseUI', 'logic.comsys.activity')
        ui.config(self.mecha_choose_item_id, self.choose_mecha_callback)

    def choose_mecha_callback(self, item_idx, item_no):
        global_data.player.update_task_extra_info(str(self.prog_task_id), [1000, item_idx])

    def filter_valid(self, tasks):
        valid_tasks = []
        for task in tasks:
            if task_utils.is_task_open_ex(task):
                valid_tasks.append(task)

        return valid_tasks

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.update_prog_reward()
        self.show_list()

    def show_list(self):
        self.show_list_by_node(self.act_list_daily, self._daily_tasks)
        self.show_list_by_node(self.act_list_weekend, self._weekend_tasks)
        self.init_get_all_btn()
        self.update_get_all_btn()

    def get_daily_tasks(self):
        return task_utils.get_children_task(self.fixed_task_id) or []

    def get_weekend_tasks(self):
        return task_utils.get_children_task(self.week_task_id) or []

    def show_list_by_node(self, tmp_list, tasks):
        player = global_data.player
        if not player:
            return
        if not tmp_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        tmp_list.SetInitCount(0)
        tmp_list.SetInitCount(len(tasks))
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        ui_data = conf.get('cUiData', {})
        for idx, task_id in enumerate(tasks):
            item_widget = tmp_list.GetItem(idx).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_num.SetColor(color)

        self.refresh_list_by_node(tmp_list, tasks)

    def refresh_list(self):
        self.refresh_list_by_node(self.act_list_daily, self._daily_tasks)
        self.refresh_list_by_node(self.act_list_weekend, self._weekend_tasks)

    def refresh_list_by_node(self, tmp_list, tasks):
        player = global_data.player
        if not player:
            return
        if not tmp_list:
            log_error('Activity %s dont indicate task list node!', self.__class__.__name__)
            return
        for idx, task_id in enumerate(tasks):
            item_widget = tmp_list.GetItem(idx).temp_common
            total_times = task_utils.get_total_prog(task_id)
            cur_times = player.get_task_prog(task_id)
            self._set_item_widget_lab_num(item_widget, total_times, cur_times)
            update_task_list_btn(item_widget.nd_task.temp_btn_get, self.get_receive_btn_status(task_id))

            @item_widget.nd_task.temp_btn_get.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id):
                self.on_click_receive_btn(_task_id)

    def get_receive_btn_status(self, task_id):
        if not task_utils.is_task_open_ex(task_id):
            if task_utils.get_raw_left_open_time_ex(task_id) > 0:
                return BTN_ST_INACTIVE
            else:
                return BTN_ST_OVERDUE

        status = global_data.player.get_task_reward_status(task_id)
        if status == ITEM_RECEIVED:
            return BTN_ST_RECEIVED
        if status == ITEM_UNGAIN:
            return BTN_ST_ONGOING
        if status == ITEM_UNRECEIVED:
            return BTN_ST_CAN_RECEIVE

    def on_click_get_all_btn(self, *args):
        global_data.player.receive_tasks_reward(self.valid_tasks)

    def on_click_receive_btn(self, task_id):
        super(ActivityNewReturnMechaGift, self).on_click_receive_btn(task_id)

    def init_describe(self):
        btn_describe = self.panel.btn_describe
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        act_name_id = conf.get('iCatalogID', '')

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))

    def get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self.valid_tasks:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task

    def on_finalize_panel(self):
        super(ActivityNewReturnMechaGift, self).on_finalize_panel()
        global_data.ui_mgr.close_ui('RecallMechaChooseUI')
        self.process_event(False)

    def auto_recv_reward(self):
        global_data.player.receive_all_task_reward(str(self.try_mecha_task_id))
        global_data.player.receive_task_prog_reward(str(self.prog_task_id), 1000)

    def auto_use_reward(self):
        pre_choose = global_data.player.get_task_content(str(self.prog_task_id), 'pre_choose_reward') or {}
        pre_choose = pre_choose.get('1000', None)
        if pre_choose is None:
            return
        else:
            item = global_data.player.get_item_by_no(self.mecha_try_item_id)
            if item:
                global_data.player.use_item(item.get_id(), 1, {'selection': [pre_choose]})
            use_params = confmgr.get('lobby_item', str(self.mecha_try_item_id), default={})['use_params']
            reward_id_list = use_params['reward_list']
            reward_id = reward_id_list[pre_choose]
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            for item_id, item_num in reward_conf['reward_list']:
                item = global_data.player.get_item_by_no(item_id)
                if item:
                    global_data.player.use_item(item.get_id(), item_num, {})

            item = global_data.player.get_item_by_no(self.mecha_choose_item_id)
            if item:
                global_data.player.use_item(item.get_id(), 1, {'selection': [pre_choose]})
            return

    def auto_actions(self):
        self.auto_recv_reward()
        self.auto_use_reward()

    def promote_prog(self):
        items = global_data.player.get_items_by_no(self.prog_promote_item_id)
        for item in items:
            item_num = min(item.get_current_stack_num(), self.max_prog_promote_count)
            if item_num > 0:
                global_data.player.use_item(item.get_id(), item_num)
                return
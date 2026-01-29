# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/ActivityNewReturnTrain.py
from __future__ import absolute_import
import six
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gcommon.time_utility import get_readable_time_2
from logic.gcommon.time_utility import get_server_time
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from common.utils.ui_path_utils import ATV_RETURN_TRAIN_BAR
from logic.comsys.effect.ui_effect import set_gray
from common.cfg import confmgr
TASK_VITALITY_ID = '1900130'
TASK_FIGHT_TIMES = '1900131'
STATE_RECEIVED = 0
STATE_RECEIVABLE = 1
STATE_NOT_RECEIVE = 2

class ActivityNewReturnTrain(ActivityBase):
    LAB_LEFT_TIME_NAME = ''

    def __init__(self, dlg, activity_type):
        super(ActivityNewReturnTrain, self).__init__(dlg, activity_type)
        self._timer = None
        self._timer_cb = {}
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self._left_time_node = None
        self._process_widget = None
        self._vitality_pro_reward = []
        self._fight_pro_reward = []
        self._before_init_panel()
        return

    def _before_init_panel(self):
        self._init_task_widget()

    def on_init_panel(self):
        self._close_time = global_data.player.activity_closetime_data.get(self._activity_type, get_server_time())
        self._process_event(True)
        self._init_ui_event()
        self._left_time_node = self.panel.temp_up.lab_time
        if self._left_time_node:
            self._register_timer()
            self._timer_cb[0] = lambda : self._refresh_left_time()
            self._refresh_left_time()
        self._custom_init_panel()

    def set_show(self, show, is_init=False):
        super(ActivityNewReturnTrain, self).set_show(show, is_init)
        if not show:
            return
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

    def _refresh_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self._left_time_node.SetString(day_txt)

    def get_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        if left_time_delta > 0:
            return get_readable_time_2(left_time_delta)
        else:
            return get_text_by_id(607911)

    def _init_task_widget(self, *args):
        self._init_accumulate_vitality()
        self._init_accumulate_fight()
        self._init_various_task()
        self.refresh_get_all_btn()

    def _init_various_task(self):
        from .TrainBattleWidget import ReturnTrainTaskWidget
        self._process_widget = ReturnTrainTaskWidget(self, self.panel.nd_left_mid, None)
        self._process_widget.init_widget()
        return

    def _init_accumulate_fight(self):
        self._fight_pro_reward = task_utils.get_prog_rewards(TASK_FIGHT_TIMES)
        async_lst = self.panel.nd_left.list_right_items

        def on_create_callback(lv, idx, item):
            task_pro, reward_id = self._fight_pro_reward[idx]
            item.data = (task_pro, reward_id)
            item.RecordAnimationNodeState('loop')
            reward_lst = template_utils.get_reward_list_by_reward_id(reward_id)
            if reward_lst:
                item_no, item_num = reward_lst[0]
                template_utils.init_tempate_mall_i_item(item.temp_item, item_no, show_rare_degree=False, item_num=item_num, show_tips=False)

                @item.temp_item.btn_choose.unique_callback()
                def OnClick(btn, touch, task_id=TASK_FIGHT_TIMES, progress_num=task_pro):
                    self._on_click_progress_reward(task_id, progress_num, item_no, item_num, btn)

                item.lab_word.SetString(task_utils.get_task_name(TASK_FIGHT_TIMES, {'prog': task_pro}))
            else:
                log_error('[ActivityNewReturnSign] has no reward list:{0}'.format(reward_id))
            self._refresh_fight_item_state(item)

        task_cur_pro = global_data.player.get_task_prog(TASK_FIGHT_TIMES)
        self.panel.lab_words2.SetString(get_text_by_id(611321).format(n=str(task_cur_pro)))
        async_lst.BindMethod('OnCreateItem', on_create_callback)
        async_lst.DeleteAllSubItem()
        async_lst.SetInitCount(len(self._fight_pro_reward))

    def _refresh_fight_item_state(self, item):
        item.StopAnimation('loop')
        item.RecoverAnimationNodeState('loop')
        item.vx_lizi.setVisible(False)
        item.img_light.setVisible(False)
        task_pro, reward_id = item.data
        if not global_data.player:
            is_received, can_receive = False, False
        else:
            is_received = global_data.player.has_receive_prog_reward(TASK_FIGHT_TIMES, task_pro)
            can_receive = global_data.player.is_prog_reward_receivable(TASK_FIGHT_TIMES, task_pro)
        item.img_check.setVisible(False)
        if is_received:
            item.img_check.setVisible(True)
            set_gray(item.temp_item.item, True)
        elif can_receive:
            item.PlayAnimation('loop')
            item.img_light.setVisible(True)
            item.vx_lizi.setVisible(True)

    def _refresh_all_fight_reward(self):
        async_lst = self.panel.nd_left.list_right_items
        for item in async_lst.GetAllItem():
            if item and type(item) not in (six.text_type, str, dict):
                self._refresh_fight_item_state(item)

        task_cur_pro = global_data.player.get_task_prog(TASK_FIGHT_TIMES)
        self.panel.lab_words2.SetString(get_text_by_id(611321).format(n=str(task_cur_pro)))

    def _init_accumulate_vitality(self):
        self._vitality_pro_reward = task_utils.get_prog_rewards(TASK_VITALITY_ID)
        list_rewards = self.panel.nd_up.temp_up.nd_up.list_rewards
        list_rewards.DeleteAllSubItem()
        list_rewards.SetInitCount(len(self._vitality_pro_reward))
        all_items = list_rewards.GetAllItem()
        for idx, item in enumerate(all_items):
            self._init_accumulate_vitality_item(item, idx)

        task_cur_pro = global_data.player.get_task_prog(TASK_VITALITY_ID)
        total_pro = task_utils.get_total_prog(TASK_VITALITY_ID)
        first_task_pro = task_utils.get_prog_rewards_progs(TASK_VITALITY_ID)[0]
        display_total_pro = total_pro - first_task_pro
        display_pro = task_cur_pro - first_task_pro
        if display_pro <= 0 or display_total_pro:
            cur_percent = 0
        else:
            cur_percent = 1.0 * (task_cur_pro - first_task_pro) / display_total_pro * 100
        if total_pro > 0:
            self.panel.nd_up.temp_up.progress_task.SetPercentage(cur_percent)
            self.panel.nd_up.temp_up.lab_act_num.SetString(str(task_cur_pro))
        else:
            self.panel.nd_up.temp_up.progress_task.SetPercentage(0)

    def _init_accumulate_vitality_item(self, item, idx):
        task_pro, reward_id = self._vitality_pro_reward[idx]
        item.data = (task_pro, reward_id)
        reward_lst = template_utils.get_reward_list_by_reward_id(reward_id)
        if reward_lst:
            item_no, item_num = reward_lst[0]
            item_pic = get_lobby_item_pic_by_item_no(item_no)
            item.item.SetDisplayFrameByPath('', item_pic)
            item.lab_quantity.SetString(str(item_num))
            item.lab_progress.SetString(str(task_pro))

            @item.btn_choose.unique_callback()
            def OnClick(btn, touch, task_id=TASK_VITALITY_ID, progress_num=task_pro):
                self._on_click_progress_reward(task_id, progress_num, item_no, item_num, btn)

        else:
            log_error('[ActivityNewReturnSign] has no reward list:{0}'.format(reward_id))
        self._refresh_vitaliy_item_state(item)

    def _refresh_vitaliy_item_state(self, item):
        task_pro, reward_id = item.data
        if not global_data.player:
            is_received, can_receive = False, False
        else:
            is_received = global_data.player.has_receive_prog_reward(TASK_VITALITY_ID, task_pro)
            can_receive = global_data.player.is_prog_reward_receivable(TASK_VITALITY_ID, task_pro)
        if is_received:
            state = STATE_RECEIVED
        elif can_receive:
            state = STATE_RECEIVABLE
        else:
            state = STATE_NOT_RECEIVE
        if state == STATE_RECEIVABLE:
            item.PlayAnimation('loop')
        else:
            item.StopAnimation('loop')
        item.nd_got.setVisible(state == STATE_RECEIVED)

    def _refresh_all_vitaliy(self):
        list_rewards = self.panel.nd_up.temp_up.nd_up.list_rewards
        for item in list_rewards.GetAllItem():
            self._refresh_vitaliy_item_state(item)

        task_cur_pro = global_data.player.get_task_prog(TASK_VITALITY_ID)
        total_pro = task_utils.get_total_prog(TASK_VITALITY_ID)
        first_task_pro = task_utils.get_prog_rewards_progs(TASK_VITALITY_ID)[0]
        display_total_pro = total_pro - first_task_pro
        display_pro = task_cur_pro - first_task_pro
        if display_pro <= 0 or display_total_pro == 0:
            cur_percent = 0
        else:
            cur_percent = 1.0 * (task_cur_pro - first_task_pro) / display_total_pro * 100
        self.panel.nd_up.temp_up.progress_task.SetPercentage(cur_percent)
        self.panel.nd_up.temp_up.lab_act_num.SetString(str(task_cur_pro))

    def _update_task(self, task_id, *args):
        func_info = {TASK_VITALITY_ID: self._refresh_all_vitaliy,
           TASK_FIGHT_TIMES: self._refresh_all_fight_reward
           }
        deal_func = func_info.get(task_id, None)
        if deal_func and callable(deal_func):
            deal_func()
        global_data.emgr.refresh_activity_redpoint.emit()
        self.refresh_get_all_btn()
        return

    def refresh_get_all_btn(self):
        show = False
        children_tasks = task_utils.get_children_task(self._task_id)
        for task_id in children_tasks:
            if task_utils.get_prog_rewards(task_id):
                if task_utils.has_unreceived_prog_reward(task_id):
                    show = True
                    break
            elif global_data.player.has_unreceived_task_reward(task_id):
                show = True
                break

        self.panel.nd_all.setVisible(show)

    def _on_click_progress_reward(self, task_id, progress_num, item_no, item_num, btn=None):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        if left_time_delta <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(607911))
            return
        else:
            if not global_data.player:
                return
            can_receive = global_data.player.is_prog_reward_receivable(task_id, progress_num)
            if can_receive:
                global_data.player.receive_task_prog_reward(task_id, progress_num)
            elif btn:
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                w_pos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': False}
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, w_pos, extra_info=extra_info, item_num=item_num)
            return

    def _init_ui_event(self):

        @self.panel.temp_btn_go.btn_common.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
            jump_to_mode_choose(PLAY_TYPE_CHICKEN)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            task_list = task_utils.get_children_task(self._task_id)
            global_data.player.receive_tasks_reward(task_list)

    def _register_timer(self):
        from common.utils.timer import CLOCK
        self._unregister_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self._second_callback, interval=1, times=-1, mode=CLOCK)

    def _unregister_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        self._timer_cb = {}
        return

    def _second_callback(self):
        for timer_key, cb_func in six.iteritems(self._timer_cb):
            cb_func()

    def _process_event(self, is_bind):
        e_conf = {'receive_task_prog_reward_succ_event': self._update_task
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _custom_init_panel(self):
        pass

    def on_finalize_panel(self):
        if self._process_widget:
            self._process_widget.destroy()
        self._process_widget = None
        self.panel.Destroy()
        self._process_event(False)
        self._unregister_timer()
        return
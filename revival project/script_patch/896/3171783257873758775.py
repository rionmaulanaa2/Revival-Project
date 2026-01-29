# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewReturn/ActivityNewReturnSign.py
from __future__ import absolute_import
import six
import six_ex
import cc
from common.cfg import confmgr
from common.utils import ui_path_utils
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gcommon.time_utility import get_server_time
from logic.comsys.activity.ActivityTemplate import ActivityBase
SEVENTH_DAY = 7
STATE_RECEIVED = 0
STATE_RECEIVABLE = 1
STATE_NOT_RECEIVE = 2
LAB_TIP_COLOR = {STATE_RECEIVED: 13032680,
   STATE_RECEIVABLE: 14221506,STATE_NOT_RECEIVE: None}

class ActivityNewReturnSign(ActivityBase):
    LAB_TIME_NAME = ''
    LAB_LEFT_TIME_NAME = 'lab_rest_time'
    LAB_INFO_NAME = ''

    def __init__(self, dlg, activity_type):
        super(ActivityNewReturnSign, self).__init__(dlg, activity_type)
        self._timer = None
        self._timer_cb = {}
        self._task_id = None
        self._progress_2_reward_dict = {}
        self._left_time_node = None
        return

    def on_init_panel(self):
        self._close_time = global_data.player.activity_closetime_data.get(self._activity_type, get_server_time())
        self._process_event(True)
        self._init_ui_event()
        self._left_time_node = self.panel.lab_time
        if self._left_time_node:
            self._register_timer()
            self._timer_cb[0] = lambda : self._refresh_left_time()
            self._refresh_left_time()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        if self._task_id:
            self._progress_2_reward_dict = task_utils.get_prog_rewards_in_dict(self._task_id)
        self._init_reward_lst()
        self._custom_init_panel()

    def set_show(self, show, is_init=False):
        super(ActivityNewReturnSign, self).set_show(show, is_init)
        if not show:
            return
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

        def play_day_item_anim(day_lst):
            for num_day in day_lst:
                if num_day == SEVENTH_DAY:
                    tmp_item = self.panel.temp_day7
                else:
                    tmp_item = self.panel.list_items.GetItem(num_day - 1)
                tmp_item.setVisible(True)
                tmp_item.PlayAnimation('show')

        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.17),
         cc.CallFunc.create(lambda : play_day_item_anim([1, 4])),
         cc.DelayTime.create(0.06),
         cc.CallFunc.create(lambda : play_day_item_anim([2, 5])),
         cc.DelayTime.create(0.06),
         cc.CallFunc.create(lambda : play_day_item_anim([3, 6])),
         cc.DelayTime.create(0.06),
         cc.CallFunc.create(lambda : play_day_item_anim([7]))]))

    def _refresh_left_time(self):
        now_time = get_server_time()
        left_time_delta = self._close_time - now_time
        is_ending, left_text, left_time, left_unit = template_utils.get_left_info(left_time_delta)
        if not is_ending:
            day_txt = get_text_by_id(left_text) + str(left_time) + get_text_by_id(left_unit)
        else:
            day_txt = get_text_by_id(left_text)
        self._left_time_node.SetString(day_txt)

    def _init_reward_lst(self, *args):
        day_key_lst = six_ex.keys(self._progress_2_reward_dict)
        day_key_lst.sort()
        for num_day in day_key_lst:
            if num_day == SEVENTH_DAY:
                day_item = self.panel.temp_day7
            else:
                day_item = self.panel.list_items.GetItem(num_day - 1)
            day_item.setVisible(False)
            if num_day != SEVENTH_DAY:
                day_item.lab_num.setVisible(False)
            day_item.RecordAnimationNodeState('loop')
            day_item.lab_time.SetString(get_text_by_id(604004).format(num_day))
            reward_id = self._progress_2_reward_dict.get(num_day)
            reward_lst = template_utils.get_reward_list_by_reward_id(reward_id)
            if reward_lst:
                item_no, item_num = reward_lst[0]
                item_path = get_lobby_item_pic_by_item_no(item_no)
                item_name = get_lobby_item_name(item_no)
                name_txt = '{0}x{1}'.format(item_name, item_num)
                day_item.lab_item_name.SetString(name_txt)
                day_item.img_item.SetDisplayFrameByPath('', item_path)
            else:
                log_error('[ActivityNewReturnSign] has no reward in day:{0} reward:{1}'.format(num_day, reward_id))

            @day_item.btn_1.unique_callback()
            def OnClick(btn, touch, progress_num=num_day):
                now_time = get_server_time()
                left_time_delta = self._close_time - now_time
                if left_time_delta <= 0:
                    global_data.game_mgr.show_tip(get_text_by_id(607911))
                    return
                if not global_data.player or global_data.player.has_receive_prog_reward(self._task_id, progress_num):
                    return
                can_receive = global_data.player.is_prog_reward_receivable(self._task_id, progress_num)
                if can_receive:
                    global_data.player.receive_task_prog_reward(self._task_id, progress_num)

            self._refresh_item_state(day_item, num_day)

    def _refresh_all_item(self, *args):
        day_key_lst = six_ex.keys(self._progress_2_reward_dict)
        for num_day in day_key_lst:
            if num_day == SEVENTH_DAY:
                day_item = self.panel.temp_day7
            else:
                day_item = self.panel.list_items.GetItem(num_day - 1)
            self._refresh_item_state(day_item, num_day)

        global_data.emgr.refresh_activity_redpoint.emit()

    def _refresh_item_state(self, item, day):
        item.StopAnimation('loop')
        item.RecoverAnimationNodeState('loop')
        if not global_data.player:
            is_received = False
            can_receive = False
        else:
            is_received = global_data.player.has_receive_prog_reward(self._task_id, day)
            can_receive = global_data.player.is_prog_reward_receivable(self._task_id, day)
        if is_received:
            state = STATE_RECEIVED
        elif can_receive:
            state = STATE_RECEIVABLE
        else:
            state = STATE_NOT_RECEIVE
        name_color = 16777215
        item.lab_item_name.SetColor(name_color)
        if can_receive:
            item.vx_lizi.setVisible(True)
            item.PlayAnimation('loop')
        else:
            item.vx_lizi.setVisible(False)
        item.bar_tips.setVisible(state == STATE_RECEIVED)
        item.btn_1.SetEnable(can_receive)
        if day != SEVENTH_DAY:
            item.pnl_1.setVisible(state == STATE_RECEIVABLE)
            item.img_get.setVisible(state == STATE_RECEIVABLE)

    def _set_bg_and_font(self, state, item, day):
        if day != SEVENTH_DAY:
            pnl_pic = ui_path_utils.AVT_RETURN_PNL.get(state)
        else:
            pnl_pic = ui_path_utils.AVT_RETURN_SEVEN_PNL.get(state)
        num_font = ui_path_utils.ATV_RETURN_FONT.get(state)
        bar_pic = ui_path_utils.ATV_RETURN_BAR.get(state)
        item.pnl_1.SetDisplayFrameByPath('', pnl_pic)
        item.lab_num.setBMFontFilePath(num_font)
        if bar_pic:
            lab_tip_color = LAB_TIP_COLOR.get(state)
            item.bar_tips.SetDisplayFrameByPath('', bar_pic)
            item.lab_tips.SetColor(lab_tip_color)
        else:
            item.bar_tips.setVisible(False)

    def _init_ui_event(self):
        pass

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
        e_conf = {'task_prog_changed': self._refresh_all_item,
           'receive_task_reward_succ_event': self._refresh_all_item,
           'receive_task_prog_reward_succ_event': self._refresh_all_item
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def _custom_init_panel(self):
        pass

    def on_finalize_panel(self):
        self._process_event(False)
        self._unregister_timer()
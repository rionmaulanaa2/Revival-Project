# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAttendance.py
from __future__ import absolute_import
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Int, List, Bool
import logic.gcommon.time_utility as tutil
from logic.gcommon.common_const.activity_const import SIGN_STATE_WAIT_SIGN, SIGN_STATE_WAIT_REMEDY, SIGN_STATE_GET_REWARD
from logic.gcommon.common_const.activity_const import ALPHA_PLAN_ATTEND_DAYS, NEWBIE_ATTEND_DAY_REWARD_NOT_GOT, NEWBIE_ATTEND_DAY_REWARD_ALREADY_GOT

class impAttendance(object):

    def _init_attendance_from_dict(self, bdict):
        self.history_attend_days = bdict.get('history_attend_days', 0)
        self.attend_reward_status = bdict.get('attend_reward_status', [SIGN_STATE_GET_REWARD] * 7)
        self.attend_week_start_time = bdict.get('attend_week_start_time', 0)
        self.attend_weekday = bdict.get('attend_weekday', 1)
        self._next_query_attend_status_time = 0
        self.calc_today()
        self._newbie_attend_reward_status = bdict.get('newbie_attend_reward_status', [NEWBIE_ATTEND_DAY_REWARD_ALREADY_GOT] * ALPHA_PLAN_ATTEND_DAYS)
        self._new_alpha_plan_enabled = bdict.get('new_alpha_plan_enabled', True)
        self._alpha_train_history_attend_days = bdict.get('alpha_train_history_attend_days', 0)
        self._summer_welfare_rewards = bdict.get('summer_welfare_rewards', {})
        self._summer_welfare_reward_got = bdict.get('summer_welfare_reward_got', False)
        self._weekend_login_period = bdict.get('weekend_login_period', 0)
        self._last_daily_fvictory_time = bdict.get('last_daily_fvictory_time', 0)

    def get_history_attend_days(self):
        return self.history_attend_days

    def attended_any_newbie_day(self):
        for i, status in enumerate(self._newbie_attend_reward_status):
            if status == NEWBIE_ATTEND_DAY_REWARD_ALREADY_GOT:
                return True

        return False

    def is_newbie_day_attended(self, day_no):
        idx = day_no - 1
        if idx < 0 or idx >= len(self._newbie_attend_reward_status):
            return False
        else:
            status = self._newbie_attend_reward_status[idx]
            return status == NEWBIE_ATTEND_DAY_REWARD_ALREADY_GOT

    def get_newibe_lowest_unattended_day_no(self):
        for i, status in enumerate(self._newbie_attend_reward_status):
            day_no = i + 1
            if status == NEWBIE_ATTEND_DAY_REWARD_NOT_GOT:
                return day_no

        return -1

    def has_unattended_day_no(self):
        day_no = self.get_newibe_lowest_unattended_day_no()
        return (
         day_no != -1, day_no)

    def is_day_no_attendable(self, day_no):
        history_attend_days = self.history_attend_days
        if history_attend_days < day_no:
            return False
        else:
            idx = day_no - 1
            if idx < 0 or idx >= len(self._newbie_attend_reward_status):
                return False
            status = self._newbie_attend_reward_status[idx]
            return status == NEWBIE_ATTEND_DAY_REWARD_NOT_GOT

    def has_attendable_day_no(self):
        day_no = self.get_newibe_lowest_unattended_day_no()
        return (
         self.is_day_no_attendable(day_no), day_no)

    def try_get_newbie_attend_reward(self, get_reward=False, day_no=None):
        if day_no is not None:
            sub_day_no = day_no
        else:
            sub_day_no = self.get_newibe_lowest_unattended_day_no()
        attendable = self.is_day_no_attendable(sub_day_no)
        if attendable:
            if get_reward:
                if day_no is not None:
                    self.call_server_method('get_new_role_reward_by_day', (day_no,))
                else:
                    self.call_server_method('get_new_role_reward')
        return attendable

    @rpc_method(CLIENT_STUB, (Int('history_attend_days'), List('newbie_attend_reward_status')))
    def get_newbie_attend_reward(self, history_attend_days, newbie_attend_reward_status):
        self.history_attend_days = history_attend_days
        self._newbie_attend_reward_status = newbie_attend_reward_status
        global_data.emgr.update_newbie_attend_reward.emit()

    @rpc_method(CLIENT_STUB, (Bool('enabled'),))
    def update_new_alpha_plan_enable_state(self, enabled):
        if self._new_alpha_plan_enabled != enabled:
            self._new_alpha_plan_enabled = enabled
            global_data.emgr.refresh_activity_list.emit()

    def check_normal_sign(self):
        self.calc_today()
        state = (SIGN_STATE_WAIT_SIGN, SIGN_STATE_WAIT_REMEDY)
        for i in range(self.attend_weekday):
            if self.attend_reward_status[i] in state:
                return True

        return False

    def get_normal_attend_info(self):
        self.calc_today()
        return (
         self.attend_week_start_time, self.attend_reward_status, self.attend_weekday)

    def calc_today(self):
        now = tutil.get_server_time()
        if now - self.attend_week_start_time > tutil.ONE_WEEK_SECONDS:
            self.query_daily_attend_reward()
            return
        weekday = tutil.get_rela_day_no(now, tutil.CYCLE_DATA_REFRESH_TYPE_1, self.attend_week_start_time)
        if weekday != self.attend_weekday:
            self.query_daily_attend_reward()

    def query_daily_attend_reward(self):
        now = tutil.get_time()
        if now > self._next_query_attend_status_time:
            self._next_query_attend_status_time = now + 10
            self.call_server_method('query_daily_attend_reward')

    def daily_sign(self):
        self.call_server_method('daily_sign')

    def remedy_sign(self, day_no):
        self.call_server_method('remedy_sign', (day_no,))

    def get_daily_attend_reward(self, day_no):
        self.call_server_method('remedy_sign', (day_no,))

    @rpc_method(CLIENT_STUB, (Int('week_start_time'), List('reward_status'), Int('week_day')))
    def refresh_normal_reward_status(self, week_start_time, reward_status, cur_weekday):
        self.attend_week_start_time = week_start_time
        self.attend_reward_status = reward_status
        self.attend_weekday = cur_weekday
        ui = global_data.ui_mgr.get_ui('NormalAttendSignUI')
        if ui:
            ui.refresh_list_reward()

    def is_old_alpha_plan_enabled(self):
        from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_ASSESS_TASK
        return is_sys_unlocked(SYSTEM_ASSESS_TASK)

    def is_new_alpha_plan_enabled(self):
        return self._new_alpha_plan_enabled

    def is_alpha_train_enabled(self):
        return self.is_new_alpha_plan_enabled()

    def get_alpha_train_history_attend_days(self):
        return self._alpha_train_history_attend_days

    @rpc_method(CLIENT_STUB, (Int('days'),))
    def update_alpha_train_days(self, days):
        self._alpha_train_history_attend_days = days

    def get_summer_welfare_reward_dict(self):
        return self._summer_welfare_rewards

    def get_summer_welfare_reward(self):
        self.call_server_method('get_summer_welfare_reward')

    @rpc_method(CLIENT_STUB, (Dict('real_reward_dict'),))
    def on_receive_summer_welfare_reward(self, real_reward_dict):
        global_data.game_mgr.show_tip(get_text_by_id(609723))
        self._summer_welfare_reward_got = True
        global_data.emgr.on_receive_summer_welfare_reward_event.emit()

    def get_can_receive_summer_welfare_reward(self):
        return bool(self._summer_welfare_rewards) and not self._summer_welfare_reward_got

    @rpc_method(CLIENT_STUB, (Int('period_no'),))
    def update_weekend_login_period(self, period_no):
        if period_no == self._weekend_login_period:
            return
        self._weekend_login_period = period_no

    def get_weekend_login_period(self):
        return self._weekend_login_period

    @rpc_method(CLIENT_STUB, (Int('last_daily_fvictory_time'),))
    def update_last_daily_fvictory_time(self, last_daily_fvictory_time):
        self._last_daily_fvictory_time = last_daily_fvictory_time
        global_data.emgr.on_update_first_win_reward_event.emit()

    def can_get_first_win_reward(self):
        return self.get_first_win_reward_left_time() >= 0

    def get_first_win_reward_left_time(self):
        from common.cfg import confmgr
        fv_interval = confmgr.get('daily_first_victory_conf', 'fv_interval', 'Value', default=0)
        cur_time = tutil.time()
        return cur_time - self._last_daily_fvictory_time - fv_interval * tutil.ONE_HOUR_SECONS

    def get_next_first_win_reward_time(self):
        from common.cfg import confmgr
        fv_interval = confmgr.get('daily_first_victory_conf', 'fv_interval', 'Value', default=0)
        return self._last_daily_fvictory_time + fv_interval * tutil.ONE_HOUR_SECONS
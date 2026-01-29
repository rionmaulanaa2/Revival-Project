# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbySummerPeakMatchWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import jump_to_ui_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata import dan_data
from logic.gutils.spectate_utils import has_live_competitions
from logic.gcommon.cdata.week_competition import data, get_week_competition_unfinish_conf
from .LobbyPeakMatchWidget import LobbyPeakMatchWidget
from logic.comsys.lottery.LotteryTurntableSecondComfirm import LotteryTurntableSecondComfirm
from logic.gcommon.cdata.round_competition import get_nearliest_competition_open, get_competition_open_on_show_time
from logic.gcommon.common_const.battle_const import SUMMER_COMP_WHITE_UIDS
from logic.gcommon.common_utils.local_text import get_text_by_id
MAX_MATCH_TIME = 600

class LobbySummerPeakMatchWidget(LobbyPeakMatchWidget):
    GLOBAL_EVENT = {'enter_summer_peak_match_queue': 'hide_btn_lab_time',
       'cancel_summer_peak_match_queue': 'show_btn_lab_time'
       }

    @classmethod
    def check_shown(cls, widget_type):
        player = global_data.player
        if not player:
            return False
        else:
            comp_id, cur_round, round_conf = get_nearliest_competition_open()
            if not comp_id:
                return False
            if player.uid in SUMMER_COMP_WHITE_UIDS:
                return True
            can_show = global_data.player.is_show_competition_entrance(comp_id, cur_round)
            if not can_show:
                global_data.player.request_comp_show_entrance()
                return False
            cur_time = tutil.get_server_time()
            gap_time = 60
            show_time_list = get_competition_open_on_show_time()
            has_competition_start_just_now = False
            for comp_id, cur_round, round_conf in show_time_list:
                battle_time = round_conf.get('battle_time', 0)
                if gap_time > cur_time - battle_time >= 0:
                    has_competition_start_just_now = True
                    break

            if not has_competition_start_just_now:
                player.clear_player_join_state()
            limit_dan = round_conf.get('limit_dan', 0)
            my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
            last_season_dan = global_data.player.get_last_season_dan()
            if my_dan >= limit_dan or last_season_dan >= limit_dan or player.uid in SUMMER_COMP_WHITE_UIDS:
                return True
            return False

    def on_init_widget(self):
        super(LobbyPeakMatchWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        self.lab_timer = None
        self.show_btn_lab_time()
        TIMER_TAG = 230621
        act = self.panel.btn.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.check_start_time_timer),
         cc.CallFunc.create(self.check_hide_register_entry),
         cc.DelayTime.create(2.0),
         cc.DelayTime.create(3.0)])))
        act.setTag(TIMER_TAG)
        return

    def check_hide_register_entry(self):
        if not LobbySummerPeakMatchWidget.check_shown(''):
            self.panel.setVisible(False)
        else:
            self.panel.setVisible(True)

    def check_start_time_timer(self):
        if not global_data.player:
            return
        if global_data.player:
            if global_data.player.get_player_competition_state():
                return
        if self.lab_timer:
            return
        self.show_btn_lab_time()

    def on_click_btn(self, *args):
        self.panel.btn.red_point.setVisible(False)
        player = global_data.player
        if not player:
            return False
        else:
            if self.check_can_enter_summer_peak_match():
                if player.is_matching or player.get_custom_room_id():
                    return
                if global_data.player.get_player_competition_state():
                    self.cancel_summer_peak_match_queue()
                else:
                    comp_id, cur_round, round_conf = get_nearliest_competition_open()
                    ask_ready_tips_id = round_conf.get('ask_ready_tips_id', 931100)
                    LotteryTurntableSecondComfirm(text_id=ask_ready_tips_id, first_click_callback=None, second_click_callback=self.enter_summer_peak_match_queue)
            else:
                self.show_cannot_enter_tips()
            return

    def check_can_enter_summer_peak_match(self):
        comp_id, cur_round, round_conf = get_nearliest_competition_open()
        if not comp_id:
            return False
        limit_dan = round_conf.get('limit_dan', 0)
        my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
        last_season_dan = global_data.player.get_last_season_dan()
        start_ts = round_conf.get('start_time', 0)
        battle_start_time = round_conf.get('battle_time', 0)
        cur_time = tutil.time()
        if battle_start_time > cur_time > start_ts and (my_dan >= limit_dan or last_season_dan >= limit_dan or global_data.player.uid in SUMMER_COMP_WHITE_UIDS):
            return True
        return False

    def show_cannot_enter_tips(self):
        show_time_list = get_competition_open_on_show_time()
        if not show_time_list:
            return ''
        show_time_str_list = []
        near_comp_id, near_cur_round, near_round_conf = get_nearliest_competition_open()
        near_tips_id = near_round_conf.get('tips_id', 0)
        text = get_text_by_id(near_tips_id)
        if text.count('{}') <= 1:
            battle_info = near_round_conf.get('battle_info', {})
            start_ts = near_round_conf.get('start_time', 0)
            register_time_date = tutil.get_utc8_datetime(start_ts)
            register_str = '%02d:%02d' % (register_time_date.hour, register_time_date.minute)
            show_time_str_list.append(register_str)
            tips_txt = get_text_by_id(near_tips_id).format(num=battle_info.get('round', 1), *show_time_str_list)
            global_data.game_mgr.show_tip(tips_txt)
            return
        cur_tips_id = ''
        battle_info = {}
        for comp_id, cur_round, round_conf in show_time_list:
            tips_id = round_conf.get('tips_id', 0)
            start_ts = round_conf.get('start_time', 0)
            battle_info = round_conf.get('battle_info', {})
            register_time_date = tutil.get_utc8_datetime(start_ts)
            register_str = '%02d:%02d' % (register_time_date.hour, register_time_date.minute)
            show_time_str_list.append(register_str)
            cur_tips_id = tips_id

        if cur_tips_id:
            org_txt = get_text_by_id(cur_tips_id)
            if org_txt.count('{') != len(show_time_str_list):
                log_error('open time count is not compatible with battle match', org_txt, show_time_list)
            tips_txt = get_text_by_id(cur_tips_id).format(num=battle_info.get('round', 1), *show_time_str_list)
            global_data.game_mgr.show_tip(tips_txt)

    def enter_summer_peak_match_queue(self):
        if not global_data.player:
            return
        if not self.check_can_enter_summer_peak_match():
            return
        if global_data.player.get_player_competition_state():
            return
        comp_id, cur_round, round_conf = get_nearliest_competition_open()
        if not comp_id:
            return
        global_data.player.req_join_competition(comp_id, cur_round)

    def cancel_summer_peak_match_queue(self):
        if not global_data.player:
            return
        if not self.check_can_enter_summer_peak_match():
            return
        if not global_data.player.get_player_competition_state():
            return
        competition_info = global_data.player.get_competition_info()
        global_data.player.cancel_join_competition(competition_info['comp_id'], competition_info['comp_round'])

    def need_show_red_point(self):
        return False

    def show_btn_lab_time(self, *args, **kwargs):
        if not self.check_can_enter_summer_peak_match():
            self.clean_btn_timer()
            return
        comp_id, comp_round, round_info = get_nearliest_competition_open()
        if not round_info:
            self.clean_btn_timer()
            return
        end_time = round_info.get('battle_time')
        self.panel.lab_time.setVisible(True)

        def update_time(pass_time):
            cur_time = tutil.time()
            left_time = max(end_time - cur_time, 0)
            left_second = int(left_time % 60)
            left_min = int(left_time / 60)
            if left_time <= 0:
                self.clean_btn_timer()
                return
            if left_second < 10:
                left_second = '0' + str(left_second)
            if left_min < 1:
                temp_time = '{}s'.format(left_second)
            else:
                temp_time = '{}m{}s'.format(left_min, left_second)
            text = get_text_by_id(931007).format(temp_time)
            if self.panel.lab_time:
                self.panel.lab_time.SetString(text)

        update_time(0)
        self.panel.lab_time.StopTimerAction()
        self.lab_timer = self.panel.lab_time.TimerAction(update_time, end_time, callback=self.clean_btn_timer, interval=1.0)

    def hide_btn_lab_time(self):
        self.clean_btn_timer()

    def clean_btn_timer(self):
        if self.lab_timer:
            self.lab_timer = None
            self.panel.lab_time.StopTimerAction()
            self.panel.lab_time.setVisible(False)
        return
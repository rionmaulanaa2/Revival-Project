# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/EntryWidget/LobbyPeakMatchWidget.py
from __future__ import absolute_import
import six
from logic.comsys.lobby.EntryWidget.LobbyEntryWidgetBase import LobbyEntryWidgetBase
from logic.gutils import jump_to_ui_utils
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
import cc
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata import dan_data
from logic.gutils.spectate_utils import has_live_competitions
from logic.gcommon.cdata.week_competition import data, get_week_competition_unfinish_conf
MAX_MATCH_TIME = 1200

class LobbyPeakMatchWidget(LobbyEntryWidgetBase):
    TIMER_TAG = 220505
    GLOBAL_EVENT = {'on_received_room_list': 'on_received_room_list',
       'on_open_live_main_ui': 'on_open_live_main_ui_func'
       }

    @classmethod
    def check_shown(cls, widget_type):
        player = global_data.player
        if not player:
            return False
        i, competition_id, start_ts, battle_info, reward_info = get_week_competition_unfinish_conf()
        battle_start_time = battle_info.get('auto_start_intv', 0) + start_ts
        limit_dan = battle_info.get('limit_dan', 0)
        cur_time = tutil.time()
        battle_finish_time = battle_start_time + MAX_MATCH_TIME
        my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
        if my_dan < limit_dan:
            if has_live_competitions():
                return True
            else:
                return False

        elif battle_finish_time > cur_time > start_ts:
            if cur_time > battle_start_time + 600:
                if has_live_competitions():
                    return True
                else:
                    return False

            return True

    def is_time_can_apply_for_week_competition(self):
        i, competition_id, start_ts, battle_info, reward_info = get_week_competition_unfinish_conf()
        if i <= -1:
            return False
        battle_start_time = battle_info.get('auto_start_intv', 0) + start_ts
        limit_dan = battle_info.get('limit_dan', 0)
        cur_time = tutil.time()
        if battle_start_time > cur_time > start_ts:
            return True
        return False

    def on_init_widget(self):
        super(LobbyPeakMatchWidget, self).on_init_widget()
        self.panel.btn.BindMethod('OnClick', self.on_click_btn)
        if self.is_time_can_apply_for_week_competition():
            self.register_timer()
            self.refresh_room_data()
        if global_data.peak_match_widget:
            global_data.peak_match_widget.set_match_begin_but_has_no_live_callback(self.refresh_red_point)

    def on_finalize_widget(self):
        super(LobbyPeakMatchWidget, self).on_finalize_widget()
        if global_data.peak_match_widget:
            global_data.peak_match_widget.set_match_begin_but_has_no_live_callback(None)
        return

    def on_click_btn(self, *args):
        self.panel.btn.red_point.setVisible(False)
        player = global_data.player
        if not player:
            return False
        else:
            i, competition_id, start_ts, battle_info, reward_info = get_week_competition_unfinish_conf()
            if i <= -1:
                return False
            limit_dan = battle_info.get('limit_dan', 0)
            my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
            if self.is_time_can_apply_for_week_competition():
                if global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI'):
                    if global_data.player.get_custom_room_is_of_week_competition():
                        global_data.emgr.room_player_return_from_lobby_event.emit()
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(19328))
                elif my_dan >= limit_dan:
                    com_room_dict = global_data.player.get_cached_week_competition_room_list()
                    if com_room_dict:
                        for t, room_list in six.iteritems(com_room_dict):
                            for r in room_list:
                                if not r.get('is_week_competition'):
                                    continue
                                is_battle = r.get('is_battle', True)
                                if is_battle:
                                    continue
                                room_id = r.get('room_id', None)
                                is_battle = r.get('is_battle', True)
                                battle_type = r.get('battle_type', None)
                                global_data.player.req_enter_room(room_id, battle_type, '')
                                return

                return
            archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
            ar_key = 'clear_live_red_point'
            _recently_has_live = tutil.time() - archive_data.get_field(ar_key, 0) < MAX_MATCH_TIME
            if has_live_competitions() or _recently_has_live:
                from logic.comsys.live.LiveMainUI import LiveMainUI
                LiveMainUI()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(19250))
            return

    def refresh_red_point(self):
        if not (self.panel and self.panel.isValid()):
            return
        need_red_point = self.need_show_red_point()
        self.panel.btn.red_point.setVisible(True if need_red_point else False)

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(60.0),
         cc.CallFunc.create(self.refresh_room_data)]))
        self.panel.btn.runAction(act)
        act.setTag(self.TIMER_TAG)

    def need_show_red_point(self):
        if not global_data.player:
            return False
        from logic.gcommon.cdata.week_competition import data, get_week_competition_unfinish_conf
        i, competition_id, start_ts, battle_info, reward_info = get_week_competition_unfinish_conf()
        if i <= -1:
            return False
        battle_start_time = battle_info.get('auto_start_intv', 0) + start_ts
        limit_dan = battle_info.get('limit_dan', 0)
        cur_time = tutil.time()
        battle_finish_time = battle_start_time + MAX_MATCH_TIME
        if battle_start_time > cur_time:
            my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
            if my_dan >= limit_dan:
                has_seat = self.check_has_empty_competition_seat()
                return has_seat
        else:
            archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
            ar_key = 'clear_live_red_point'
            if tutil.time() - archive_data.get_field(ar_key, 0) > tutil.ONE_HOUR_SECONS:
                return has_live_competitions()
            return False

    def check_has_empty_competition_seat(self):
        if not global_data.player:
            return False
        com_room_dict = global_data.player.get_cached_week_competition_room_list()
        if not com_room_dict:
            return False
        cur_time = tutil.time()
        for t, room_list in six.iteritems(com_room_dict):
            if t < cur_time - tutil.ONE_MINUTE_SECONDS + 5:
                continue
            else:
                for r in room_list:
                    if not r.get('is_week_competition'):
                        continue
                    is_battle = r.get('is_battle', True)
                    if is_battle:
                        continue
                    cur_player_cnt = int(r.get('cur_player_cnt', 0))
                    max_player_cnt = int(r.get('max_player_cnt', 0))
                    if max_player_cnt > cur_player_cnt:
                        return True

                return False

    def refresh_room_data(self):
        if not self.is_time_can_apply_for_week_competition():
            self.panel.btn.stopActionByTag(self.TIMER_TAG)
            self.refresh_red_point()
            return
        if not global_data.ui_mgr.get_ui('RoomListUINew'):
            if global_data.player:
                global_data.player.req_room_list()

    def on_received_room_list(self, page, room_list):
        if page == 0:
            self.refresh_red_point()

    def on_open_live_main_ui_func(self):
        self.panel.btn.red_point.setVisible(False)
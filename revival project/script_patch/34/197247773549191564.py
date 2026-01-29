# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impReport.py
from __future__ import absolute_import
from __future__ import print_function
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB, filter_method
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from mobile.common.FilterMessageBroker import FilterMessageBroker
from logic.gcommon.common_const.log_const import REPORT_CLAN_DAY_LIMIT, REPORT_ROOM_DAY_LIMIT, REPORT_PLAYER_DAY_LIMIT, REPORT_CLASS_CLAN, REPORT_CLASS_ROOM, REPORT_CLASS_NORMAL, REPORT_CLASS_BATTLE, REPORT_ROOM_TIMES, REPORT_CLAN_TIMES, REPORT_PLAYER_TIMES

class impReport(object):

    def _init_report_from_dict(self, bdict):
        report_times_day_limit = bdict.get('report_times_day_limit', {})
        self._report_clan_times_per_day = report_times_day_limit.get(REPORT_CLAN_TIMES, REPORT_CLAN_DAY_LIMIT)
        self._report_room_times_per_day = report_times_day_limit.get(REPORT_ROOM_TIMES, REPORT_ROOM_DAY_LIMIT)
        self._report_player_times_per_day = report_times_day_limit.get(REPORT_PLAYER_TIMES, REPORT_PLAYER_DAY_LIMIT)
        self._tmp_report_player_info = None
        self._need_request_name_dict = True
        return

    def report_someone_in_battle(self, report_type, target_id, reason, other=''):
        report_data = {}
        report_data['target_id'] = target_id
        report_data['reason'] = reason
        report_data['other'] = other
        if self.is_in_global_spectate():
            self.call_server_method('do_global_spectate_report_someone', (report_type, report_data))
        else:
            self.call_soul_method('report_someone_in_battle', (report_type, report_data))

    def report_someone_from_battle_history(self, report_type, target_uid, reason, other=''):
        report_data = {}
        report_data['reason'] = reason
        report_data['other'] = other
        self.call_server_method('report_someone_in_world', (report_type, target_uid, report_data))

    def report_someone_chat(self, report_type, target_uid, chat_content, chat_channel, reason, other=''):
        report_data = {}
        report_data['reason'] = reason
        report_data['other'] = other
        report_data['chat'] = chat_content
        report_data['chat_channel'] = chat_channel
        self.call_server_method('report_someone_in_world', (report_type, target_uid, report_data))

    def report_clan(self, report_type, clan_id, report_data):
        self.call_server_method('report_clan', (report_type, clan_id, report_data))

    def report_custom_room(self, report_type, room_id, report_data):
        self.call_server_method('report_custom_room', (report_type, room_id, report_data))

    def get_report_clan_times(self):
        return self._report_clan_times_per_day

    def get_report_room_times(self):
        return self._report_room_times_per_day

    def get_report_player_times(self):
        return self._report_player_times_per_day

    @rpc_method(CLIENT_STUB, (Int('ret'),))
    def on_report_result(self, ret):
        self.on_process_report_result(ret)

    def on_process_report_result(self, ret):
        from logic.gcommon.common_const.log_const import REPORT_RESULT_OK
        global_data.emgr.on_report_result_event.emit(ret)
        if ret == REPORT_RESULT_OK:
            from logic.gcommon import time_utility as t_util
            global_data._last_report_send_timestamp = t_util.get_server_time()
            global_data.game_mgr.show_tip(get_text_local_content(80893))

    @rpc_method(CLIENT_STUB, (Str('report_type'), Int('times')))
    def on_report_times_change(self, report_type, times):
        if report_type == REPORT_CLAN_TIMES:
            self._report_clan_times_per_day = times
        elif report_type == REPORT_ROOM_TIMES:
            self._report_room_times_per_day = times
        elif report_type == REPORT_PLAYER_TIMES:
            self._report_player_times_per_day = times
        global_data.emgr.on_report_times_change_event.emit(report_type, times)

    @rpc_method(CLIENT_STUB, ())
    def on_reset_report_times(self):
        self._report_room_times_per_day = REPORT_ROOM_DAY_LIMIT
        self._report_clan_times_per_day = REPORT_CLAN_DAY_LIMIT
        self._report_player_times_per_day = REPORT_PLAYER_DAY_LIMIT
        global_data.emgr.on_report_times_change_event.emit(REPORT_CLAN_TIMES, REPORT_CLAN_DAY_LIMIT)
        global_data.emgr.on_report_times_change_event.emit(REPORT_ROOM_TIMES, REPORT_ROOM_DAY_LIMIT)
        global_data.emgr.on_report_times_change_event.emit(REPORT_PLAYER_TIMES, REPORT_PLAYER_DAY_LIMIT)

    def request_report_player_info(self):
        self.call_soul_method('request_report_player_info', (self._need_request_name_dict,))

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def reply_report_player_info(self, data):
        print('test---------------', data)
        self._tmp_report_player_info = data
        global_data.emgr.on_update_report_player_list.emit(data)
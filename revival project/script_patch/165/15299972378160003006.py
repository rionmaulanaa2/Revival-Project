# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impFollow.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, List, Dict, Str, Bool
import logic.gcommon.const as const
from collections import defaultdict

class impFollow(object):

    def _init_follow_from_dict(self, bdict):
        self._follow_list = set()
        self._cached_player_infos = defaultdict(list)
        self._last_fans_count = bdict.get('last_fans_count', 0)
        self._cur_fans_count = self._last_fans_count
        self._cached_player_uids = defaultdict(set)

    def try_follow(self, player_uid):
        if not player_uid or player_uid == self.uid:
            return
        if player_uid not in self._follow_list:
            self.call_server_method('try_follow', (player_uid,))

    def try_unfollow(self, player_uid):
        if not player_uid or player_uid == self.uid:
            return
        if player_uid in self._follow_list:
            self.call_server_method('try_unfollow', (player_uid,))

    @rpc_method(CLIENT_STUB, (List('follow_list'),))
    def on_follow_data(self, follow_list):
        self._follow_list = {int(uid) for uid in follow_list}
        global_data.emgr.on_update_follow_player_count.emit(len(self._follow_list))

    @rpc_method(CLIENT_STUB, (Int('player_uid'),))
    def on_follow(self, player_uid):
        self._follow_list.add(player_uid)
        global_data.emgr.on_follow_result.emit(player_uid)

    @rpc_method(CLIENT_STUB, (Int('player_uid'),))
    def on_unfollow(self, player_uid):
        self._follow_list.discard(player_uid)
        global_data.emgr.on_undo_follow_result.emit(player_uid)

    @rpc_method(CLIENT_STUB, (Int('fans_count'),))
    def on_fans_data(self, fans_count):
        self._cur_fans_count = fans_count
        global_data.emgr.on_update_fans_player_count.emit(self._cur_fans_count)

    @rpc_method(CLIENT_STUB, (Int('player_uid'), Bool('follow_status')))
    def on_query_been_followed_by(self, player_uid, follow_status):
        global_data.emgr.on_response_fans_system_query_follow.emit(player_uid, follow_status)

    def has_follow_player(self, player_uid):
        return player_uid in self._follow_list

    def has_been_followed_by(self, player_uid):
        self.query_been_followed_by(player_uid)
        return False

    def query_been_followed_by(self, player_uid):
        self.call_server_method('query_been_followed_by', (player_uid,))

    def get_follow_player_count(self):
        return len(self._follow_list)

    def get_fans_count(self):
        return self._cur_fans_count

    def get_latest_add_fans_count(self):
        fans_count_now = self.get_fans_count()
        if fans_count_now > self._last_fans_count:
            return fans_count_now - self._last_fans_count
        return 0

    def update_last_fans_count(self, count):
        self._last_fans_count = count

    def request_fans_system_player_info(self, info_type, page_index):
        if page_index <= 0:
            return
        if info_type == const.FANS_SYSTEM_INFO_TYPE_FOLLOWS:
            if page_index > const.FANS_SYSTEM_MAX_FOLLOW_CNT / const.FANS_SYSTEM_PLAYER_INFO_PAGE_SIZE:
                return
        elif page_index > const.FANS_SYSTEM_MAX_FANS_CNT / const.FANS_SYSTEM_PLAYER_INFO_PAGE_SIZE:
            return
        self.call_server_method('get_fans_system_player_info', (info_type, page_index))

    @rpc_method(CLIENT_STUB, (Int('info_type'), Int('page_index'), List('player_infos')))
    def reply_fans_system_player_info(self, info_type, page_index, player_infos):
        if not player_infos:
            return
        else:
            need_notify = False
            for player_info in player_infos:
                uid = player_info.get('uid')
                if uid is None or uid in self._cached_player_uids[info_type]:
                    continue
                self._cached_player_uids[info_type].add(uid)
                self._cached_player_infos[info_type].append(player_info)
                need_notify = True

            if need_notify:
                global_data.emgr.on_received_fans_system_player_info.emit(info_type, page_index)
            return

    def get_fans_system_player_info(self, info_type):
        return self._cached_player_infos[info_type]

    def search_fans_system_player_info_by_uid(self, info_type, player_uid):
        self.call_server_method('fans_system_search_player_infos_by_uid', (info_type, player_uid))

    def search_fans_system_player_info_by_name(self, info_type, player_name):
        self.call_server_method('fans_system_search_player_infos_by_name', (info_type, player_name))

    @rpc_method(CLIENT_STUB, (Int('info_type'), Str('query_input_text'), List('player_infos')))
    def response_fans_system_search_player_infos(self, info_type, query_input_text, player_infos):
        global_data.emgr.on_response_fans_system_search.emit(info_type, query_input_text, player_infos)

    def clear_fans_system_cached_player_info(self):
        self._cached_player_infos.clear()
        self._cached_player_uids.clear()
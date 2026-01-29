# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSummer.py
from __future__ import absolute_import
import six
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Dict, Int, Str, Bool
from logic.gcommon import time_utility
import math
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon.item import item_const

class impSummer(object):

    def _init_summer_from_dict(self, bdict):
        self.locked_coconut_map = list(range(acconst.SUMMER_COCONUT_COLUMN * acconst.SUMMER_COCONUT_COLUMN))
        self.opend_coconut_map = set(bdict.get('opend_coconut_map', []))
        for idx in self.opend_coconut_map:
            self.locked_coconut_map.remove(idx)

        self.coconut_map_reward_dict = bdict.get('coconut_map_reward_dict', {})
        self.last_req_lost_tole_ts = bdict.get('last_req_lost_tole_ts', 0)
        self.send_msg_uids = bdict.get('send_msg_uids', {})
        if not self.send_msg_uids:
            self.send_msg_uids = {'qq_wc': [],'msg': []}
        self.lost_role_team_times = bdict.get('lost_role_team_times', {})
        self.lost_role_red_point = bdict.get('lost_role_red_point', False)
        self.last_summer_share_succ_ts = bdict.get('last_summer_share_succ_ts', 0)
        self._reply_lost_roles = {}
        self.req_lost_roles_timestamp = 0
        self._summer_game_share_url = None
        self.opened_puzzle_data = set(bdict.get('opened_puzzle_data', []))
        return

    def unlock_coconut_map(self, row, column):
        coconut_id = row * acconst.SUMMER_COCONUT_COLUMN + column
        if coconut_id not in self.locked_coconut_map or coconut_id in self.opend_coconut_map:
            return
        self.call_server_method('unlock_coconut_map', (row, column))

    @rpc_method(CLIENT_STUB, (Int('coconut_id'), List('reward_idxs')))
    def on_new_cell_unlocked(self, coconut_id, reward_idxs):
        self.locked_coconut_map.remove(coconut_id)
        self.opend_coconut_map.add(coconut_id)
        for idx in reward_idxs:
            self.coconut_map_reward_dict[str(idx)] = item_const.ITEM_UNRECEIVED

        global_data.emgr.on_new_cell_unlock.emit(coconut_id)

    def receive_coconut_reward(self, reward_idx):
        if self.coconut_map_reward_dict.get(str(reward_idx), item_const.ITEM_UNGAIN) != item_const.ITEM_UNRECEIVED:
            return False
        self.call_server_method('receive_coconut_reward', (reward_idx,))
        return True

    def check_reward_can_receive(self):
        for _, value in six.iteritems(self.coconut_map_reward_dict):
            if value == item_const.ITEM_UNRECEIVED:
                return True

        return False

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('reward_idx')))
    def receive_coconut_reward_ret(self, ret, reward_idx):
        if ret:
            self.coconut_map_reward_dict[str(reward_idx)] = item_const.ITEM_RECEIVED
            global_data.emgr.receive_coconut_reward.emit(reward_idx)

    def req_lost_roles(self):
        cur_time = time_utility.time()
        if cur_time - self.req_lost_roles_timestamp <= 10:
            global_data.game_mgr.show_tip(get_text_by_id(15806))
            return
        self.call_server_method('request_lost_role')
        self.req_lost_roles_timestamp = cur_time

    @rpc_method(CLIENT_STUB, (List('role_infos'),))
    def reply_lost_roles(self, role_infos):
        self._reply_lost_roles = role_infos
        global_data.emgr.reply_lost_roles_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('team_times'),))
    def update_lost_role_team_times(self, team_times):
        self.lost_role_team_times.update(team_times)
        self.lost_role_red_point = True
        global_data.emgr.update_recall_team_times.emit()

    def send_qqorwc_to_lost_role(self, uid, username, share_type):
        self.call_server_method('send_qqorwc_to_lost_role', (uid, username, share_type))
        self.send_msg_uids.setdefault('qq_wc', [])
        if uid not in self.send_msg_uids['qq_wc']:
            self.send_msg_uids['qq_wc'].append(uid)
        global_data.emgr.send_lost_role_recall.emit()

    def send_msg_to_lost_role(self, uid, username):
        self.call_server_method('send_msg_to_lost_role', (uid, username))

    @rpc_method(CLIENT_STUB, (Int('uid'),))
    def send_msg_to_lost_role_succ(self, uid):
        self.send_msg_uids.setdefault('msg', [])
        if uid not in self.send_msg_uids['msg']:
            self.send_msg_uids['msg'].append(uid)
        global_data.emgr.send_lost_role_recall.emit()

    def cancel_lost_role_red_point(self):
        self.lost_role_red_point = False
        self.call_server_method('cancel_lost_role_red_point')

    def on_open_lost_role_widget(self):
        self.call_server_method('on_open_lost_role_widget')

    @rpc_method(CLIENT_STUB, (Int('timestamp'),))
    def update_summer_share_succ_ts(self, timestamp):
        self.last_summer_share_succ_ts = timestamp
        global_data.emgr.update_summer_share_succ_ts.emit()

    def get_last_summer_share_succ_ts(self):
        return self.last_summer_share_succ_ts

    @rpc_method(CLIENT_STUB, (Str('share_url'),))
    def update_summer_game_share_url(self, share_url):
        if share_url:
            self._summer_game_share_url = share_url

    def get_summer_game_share_url(self):
        return self._summer_game_share_url

    @rpc_method(CLIENT_STUB, ())
    def update_summer_game_task(self):
        global_data.emgr.update_summer_game_task_prog.emit()

    def open_puzzle(self, row, column):
        idx = row * acconst.PUZZLE_COLUMN_CNT + column
        if idx >= acconst.PUZZLE_COLUMN_CNT * acconst.PUZZLE_COLUMN_CNT:
            return
        if idx in self.opened_puzzle_data:
            return
        self.call_server_method('open_puzzle', (row, column))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('row'), Int('column')))
    def open_puzzle_ret(self, ret, row, column):
        if ret:
            puzzle_idx = row * acconst.PUZZLE_COLUMN_CNT + column
            self.opened_puzzle_data.add(puzzle_idx)
            global_data.emgr.on_open_puzzle.emit(puzzle_idx)
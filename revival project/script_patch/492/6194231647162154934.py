# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/CustomRoomInfo.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.const import BATTLE_STATE_FIGHTING, BATTLE_STATE_INROOM
from logic.gcommon import const
from common.cfg import confmgr

class CustomRoomInfo(object):

    def __init__(self):
        self.room_id = 0
        self.teams = []

    def init_from_dict(self, room_info):
        self.room_id = room_info.get('room_id', 0)
        self.max_team_size = int(room_info.get('max_team_size', -1))
        self.max_team_cnt = int(room_info.get('max_team_cnt', -1))
        self.battle_type = room_info.get('battle_type', -1)
        self.map_id = room_info.get('map_id', -1)
        self.name = room_info.get('name')
        self.players = room_info.get('players')
        self.team_seat2player = {}
        self.uid2judge_seat = {}
        self.creator = room_info.get('creator')
        self.need_pwd = room_info.get('need_pwd', False)
        self.room_battled_times = room_info.get('room_battled_times', 1)
        self.room_born_idx = room_info.get('born_idx', -1)
        self.can_change_seat = room_info.get('can_change_seat', False)
        self.can_leave_room = room_info.get('can_leave_room', False)
        self.can_chat_in_room = room_info.get('can_chat_in_room', True)
        self.team_names = room_info.get('team_names', {})
        self.customed_battle_dict = room_info.get('customed_battle_dict', {})
        self.is_customed_battle = room_info.get('is_customed_battle', {})
        self.init_data()

    def init_data(self):
        for uid, data in six.iteritems(self.players):
            seat_idx = data.get('seat_index', None)
            if is_in_judge_seat(seat_idx):
                self.uid2judge_seat.update({uid: seat_idx})
            self.team_seat2player[seat_idx] = uid

        return

    def player_enter_room(self, uid, player_data):
        self.players.update({uid: player_data})
        self.player_sit_down(uid, player_data.get('seat_index', None))
        return

    def player_sit_down(self, uid, seat_idx, clear_old_seat=True):
        if is_in_judge_seat(seat_idx):
            self.uid2judge_seat.update({uid: seat_idx})
        elif uid in six_ex.keys(self.uid2judge_seat):
            del self.uid2judge_seat[uid]
        old_seat = self.get_player_seat_idx(uid)
        if uid in self.players:
            self.players[uid].update({'seat_index': seat_idx
               })
        if clear_old_seat:
            if old_seat in self.team_seat2player:
                del self.team_seat2player[old_seat]
        self.team_seat2player[seat_idx] = uid

    def player_leave_room(self, uid):
        old_seat = self.get_player_seat_idx(uid)
        if uid in self.players:
            del self.players[uid]
        if old_seat in self.team_seat2player:
            del self.team_seat2player[old_seat]
        if uid in six_ex.keys(self.uid2judge_seat):
            del self.uid2judge_seat[uid]

    def get_player_seat_idx(self, uid):
        if uid in self.players:
            return self.players[uid].get('seat_index', None)
        else:
            return None

    def get_player_data(self, uid):
        if uid in self.players:
            return self.players[uid]
        else:
            return None
            return None

    def get_team_seat_player_data(self, seat_idx):
        if seat_idx in self.team_seat2player:
            uid = self.team_seat2player[seat_idx]
            return self.get_player_data(uid)
        else:
            return None

    def get_player_num_in_team(self):
        return len(self.players) - len(self.uid2judge_seat)

    def destroy(self):
        self.players = {}
        self.uid2judge_seat = {}
        self.team_seat2player = {}

    def update_roommate_info(self, uid, info):
        player_info = self.players.get(uid, None)
        if player_info is None:
            return
        else:
            player_info.update(info)
            return

    def set_creator(self, new_creator):
        self.creator = new_creator

    def is_two_or_more_team(self):
        pre_team = -1
        team_cnt = 0
        for seat_index, uid in six.iteritems(self.team_seat2player):
            curr_team = seat_index / self.max_team_size
            if curr_team != pre_team:
                team_cnt += 1
                if team_cnt >= 2:
                    break
            pre_team = curr_team

        if team_cnt >= 2:
            return True
        else:
            return False

    def get_team_num(self):
        pre_team = -1
        team_cnt = 0
        for seat_index, uid in six.iteritems(self.team_seat2player):
            curr_team = seat_index / self.max_team_size
            if curr_team != pre_team:
                team_cnt += 1
                if team_cnt >= 2:
                    break
            pre_team = curr_team

        return team_cnt

    def get_players_uid_list(self):
        return six_ex.keys(self.players)

    def update_player_battle_state(self, uid, state):
        if uid not in six_ex.keys(self.players):
            return
        self.players[uid].update({'battle_state': state})

    def set_all_player_battle_state(self, state=BATTLE_STATE_INROOM):
        for uid in six_ex.keys(self.players):
            self.players[uid].update({'battle_state': state})

    def reset_player_seat(self, players_info):
        self.players = {}
        self.team_seat2player = {}
        for uid, data in six.iteritems(players_info):
            self.players[uid] = data
            seat_idx = data.get('seat_index', None)
            self.team_seat2player[seat_idx] = uid

        return

    def is_competition(self, battle_type):
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(str(battle_type))
        if battle_info.get('iRoomNeededItem', None) is None:
            return False
        else:
            return True

    def update_can_change_seat(self, change_seat):
        self.can_change_seat = change_seat

    def update_can_leave_room(self, can_leave_room):
        self.can_leave_room = can_leave_room

    def on_set_competition_team_name(self, team_idx, team_name):
        self.team_names[team_idx] = team_name

    def update_can_chat_in_room(self, can_chat_in_room):
        self.can_chat_in_room = can_chat_in_room


def is_in_judge_seat(seat_index):
    return seat_index is not None and const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END
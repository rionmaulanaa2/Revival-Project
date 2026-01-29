# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCustomRoom.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Dict, Int, Str, Bool, Float
from logic.gcommon import const
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils.search_salog_utils import add_common_search_salog
from logic.gcommon.cdata.dan_data import get_dan_name_id
import logic.gcommon.time_utility as tutil

class RoomInfo(object):

    def __init__(self):
        self.rid = 0
        self._room_info = {}
        self.players = {}
        self.max_team_size = -1
        self.max_team_cnt = -1

    def init_from_dict(self, info):
        import copy
        copy.deepcopy(info)
        self.rid = info.get('room_id', 0)
        self.players = info.get('players', {})
        self.max_team_size = int(info.get('max_team_size', -1))
        self.max_team_cnt = int(info.get('max_team_cnt', -1))
        self._room_info = info
        if 'name' in self._room_info:
            self._room_info['name'] = unpack_text(self._room_info['name'])
        self.room_battled_times = info.get('room_battled_times', 1)

    def player_leave_room(self, uid):
        if uid in self.players:
            del self.players[uid]

    def player_enter_room(self, uid, player_data):
        import copy
        player_data = copy.deepcopy(player_data)
        self.players.update({uid: player_data})

    def on_player_seat_down(self, uid, seat_idx):
        if uid in self.players:
            self.players[uid].update({'seat_index': seat_idx})

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

    def get_player_name(self, uid):
        return self.players.get(uid, {}).get('char_name', '')

    def get_room_info(self):
        import copy
        if self._room_info:
            self._room_info.update({'players': self.players})
        return copy.deepcopy(self._room_info)

    def get_battle_type(self):
        if self._room_info:
            return self._room_info.get('battle_type', -1)
        else:
            return -1

    def clear_room_info(self):
        self.players = {}
        self.rid = 0
        self._room_info = {}

    def destroy(self):
        self.players = {}
        self.rid = 0
        self._room_info = {}

    def update_roommate_info(self, uid, info):
        player_info = self.players.get(uid, None)
        if player_info is None:
            return
        else:
            player_info.update(info)
            return

    def update_room_battled_times(self, room_battled_times):
        self._room_info.update({'room_battled_times': room_battled_times})

    def update_room_born_idx(self, born_idx):
        self._room_info.update({'born_idx': born_idx})

    def set_all_player_in_battle(self, state=const.BATTLE_STATE_FIGHTING):
        for uid in six_ex.keys(self.players):
            self.players[uid].update({'battle_state': state})

    def update_player_battle_state(self, uid, state):
        if uid not in six_ex.keys(self.players):
            return
        self.players[uid].update({'battle_state': state})

    def update_room_info_by_key_value(self, k, v):
        self._room_info.update({k: v})

    def update_player_info_by_uid(self, uid, update_info):
        if uid not in six_ex.keys(self.players):
            return
        self.players[uid].update(update_info)

    def update_team_name_by_idx(self, team_idx, team_name):
        team_names = self._room_info.setdefault('team_names', {})
        team_names[team_idx] = team_name

    def get_team_names(self):
        return self._room_info.get('team_names', {})

    def get_need_pwd(self):
        return self._room_info.get('need_pwd', False)


class impCustomRoom(object):

    def _init_customroom_from_dict(self, bdict):
        self.room_info = RoomInfo()
        self._room_dissolved_in_battle = False
        self._player_kicked_in_battle = False
        self.room_count_down_dict = dict()
        self.room_count_down_timer = None
        self._has_req_week_competition = bdict.get('has_req_week_competition', False)
        self._req_valid_ts = bdict.get('req_valid_ts', 0)
        self._cached_week_competition_room_list = {}
        return

    def req_room_list(self, page=0):
        self.call_server_method('req_room_list', (page,))

    @rpc_method(CLIENT_STUB, (Int('page'), List('room_list')))
    def on_room_list(self, page, room_list):
        new_room_list = []
        for room in room_list:
            if room.get('show_in_client', True):
                new_room_list.append(room)

        ui_inst = global_data.ui_mgr.get_ui('RoomListUINew')
        for room_data in room_list:
            if 'name' in room_data:
                room_data['name'] = unpack_text(room_data['name'])

        if ui_inst:
            ui_inst.refresh_room_list(page, new_room_list)
        self.on_room_list_post(page, new_room_list)

    def on_room_list_post(self, page, room_list):
        if page == 0:
            ls = []
            for r in room_list:
                if r.get('is_week_competition', False):
                    ls.append(r)

            self._cached_week_competition_room_list = {tutil.time(): ls}
        global_data.emgr.on_received_room_list.emit(page, room_list)

    def get_cached_week_competition_room_list(self):
        return self._cached_week_competition_room_list

    def req_create_room(self, room_info):
        self._cache_room_ui(room_info.get('battle_type', None))
        self.call_server_method('req_create_room', (room_info,))
        return

    def req_enter_room(self, room_id, battle_type, pwd):
        self._cache_room_ui(battle_type)
        player_info = {'clan_name': global_data.player.get_clan_name(),
           'clan_lv': global_data.player.get_clan_lv(),
           'clan_badge': global_data.player.get_clan_badge(),
           'battle_state': const.BATTLE_STATE_INROOM,
           'dan_info': global_data.player.get_dan_info()
           }
        self.call_server_method('req_enter_room', (room_id, battle_type, pwd, player_info))

    @rpc_method(CLIENT_STUB, (Dict('player_info'),))
    def on_player_enter_room(self, player_info):
        self.room_info.player_enter_room(player_info.get('uid', None), player_info)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI')
        if room_ui:
            room_ui.on_player_enter_room(player_info)
        return

    @rpc_method(CLIENT_STUB, (Int('ret'), Dict('room_info')))
    def on_enter_room(self, ret, room_info):
        is_week_competition = room_info.get('is_week_competition', False)
        if ret < 0:
            if ret == const.ROOM_ENTER_NOT_EXIST:
                global_data.game_mgr.show_tip(get_text_by_id(19331), True)
            elif ret == const.ROOM_ENTER_PWD_WRONG:
                global_data.game_mgr.show_tip(get_text_by_id(19325), True)
            elif ret == const.ROOM_ENTER_IN_FIGHT:
                if is_week_competition:
                    global_data.game_mgr.show_tip(get_text_by_id(19250), True)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19324), True)
            elif ret == const.ROOM_ENTER_ROOM_FULL:
                if is_week_competition:
                    global_data.game_mgr.show_tip(get_text_by_id(19249), True)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19330), True)
            elif ret == const.ROOM_ENTER_ROOM_INFO_NO_SEATS_FOR_TEAM:
                global_data.game_mgr.show_tip(get_text_by_id(19425), True)
            elif ret == const.ROOM_ENTER_ROOM_LEVEL_NOENGOUGH:
                global_data.game_mgr.show_tip(get_text_by_id(608165), True)
            elif ret == const.ROOM_ENTER_ROOM_COMPETITION_NO_EMULATOR:
                global_data.game_mgr.show_tip(get_text_by_id(609221), True)
            elif ret == const.ROOM_ENTER_ROOM_FORBID:
                global_data.game_mgr.show_tip(get_text_by_id(609223), True)
            elif ret == const.ROOM_ENTER_ROOM_FORBID_COMP:
                forbid_ts = room_info.get('forbid_competition_ts', 0)
                if forbid_ts == -1:
                    global_data.game_mgr.show_tip(get_text_by_id(634074), True)
                else:
                    left_time = forbid_ts - tutil.time()
                    global_data.game_mgr.show_tip(get_text_by_id(634075, {'time': tutil.get_readable_time_hour_minitue_sec(left_time)}), True)
            elif ret == const.ROOM_ENTER_ROOM_DAN_NOENGOUGH:
                if is_week_competition:
                    limit_dan = room_info.get('limit_dan', 6)
                    global_data.game_mgr.show_tip(get_text_by_id(19248).format(dan=get_text_by_id(get_dan_name_id(limit_dan))), True)
            elif ret == const.ROOM_ENTER_ROOM_JOIN_TIME_LIMIT:
                global_data.game_mgr.show_tip(get_text_by_id(19251), True)
            global_data.ui_mgr.close_ui('RoomUI')
            global_data.ui_mgr.close_ui('RoomUINew')
            return
        if ret == const.ROOM_ENTER_REQ_SUCC:
            global_data.game_mgr.show_tip(get_text_by_id(19326), True)
        elif ret == const.ROOM_ENTER_CREATE:
            global_data.game_mgr.show_tip(get_text_by_id(19327), True)
        elif ret == const.ROOM_ENTER_LOST_CREATOR:
            global_data.game_mgr.show_tip(get_text_by_id(608168), True)
        self.room_info.init_from_dict(room_info)
        global_data.ui_mgr.close_ui('RoomCreateUI')
        global_data.ui_mgr.close_ui('RoomCreateUINew')
        global_data.ui_mgr.close_ui('RoomListUINew')
        global_data.emgr.need_show_room_ui_event.emit()

    def req_sit_down(self, uid, seat_index):
        self.call_server_method('req_sit_down', (uid, seat_index))

    def req_leave_seat(self, uid):
        self.call_server_method('req_leave_seat', (uid,))

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('seat_index')))
    def on_player_sit_down(self, uid, seat_index):
        self.room_info.on_player_seat_down(uid, seat_index)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI')
        if room_ui:
            room_ui.on_player_sit_down(uid, seat_index)

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('seat_index'), Bool('clear_old_seat')))
    def on_player_sit_down_with_option(self, uid, seat_index, clear_old_seat):
        self.room_info.on_player_seat_down(uid, seat_index)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_player_sit_down(uid, seat_index, clear_old_seat=clear_old_seat)

    @rpc_method(CLIENT_STUB, (Int('uid'),))
    def on_player_leave_seat(self, uid):
        self.room_info.on_player_seat_down(uid, -1)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI')
        if room_ui:
            room_ui.on_player_leave_to_waiting_area(uid)

    def req_leave_room(self):
        self.call_server_method('req_leave_room', ())

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('reason')))
    def on_player_leave_room(self, uid, reason):
        if uid == global_data.player.uid:
            if reason == const.ROOM_LEAVE_ACTIVE:
                global_data.game_mgr.show_tip(get_text_by_id(19333), True)
            elif reason == const.ROOM_LEAVE_KICK:
                if global_data.player.is_in_battle():
                    self._player_kicked_in_battle = True
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19332), True)
                global_data.emgr.kick_out_from_custom_room.emit()
            elif reason == const.ROOM_LEAVE_START:
                global_data.game_mgr.show_tip(get_text_by_id(19302), True)
            elif reason == const.ROOM_LEAVE_DISSOLVE:
                if global_data.player.is_in_battle():
                    self._room_dissolved_in_battle = True
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19304), True)
                global_data.emgr.kick_out_from_custom_room.emit()
                if global_data.player.get_player_competition_state():
                    global_data.player.reset_join_state_on_dissolve_or_cancel()
        if uid == self.uid:
            self.room_info.clear_room_info()
            global_data.emgr.leave_custom_room.emit()
        else:
            self.room_info.player_leave_room(uid)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI')
        if room_ui:
            room_ui.on_player_leave_room(uid)

    def req_kick_player(self, player_uid):
        self.call_server_method('req_kick_player', (player_uid,))

    def req_dissolve_room(self):
        self.call_server_method('req_dissolve_room', ())

    def req_start(self):
        self.call_server_method('req_start', ())

    def req_share(self, room_info):
        share_dict = room_info.get_share_dict()
        self.call_server_method('req_share', (share_dict,))

    @rpc_method(CLIENT_STUB, (Dict('info'),))
    def start_fail(self, info):
        reason = info['ret']
        if reason == const.ROOM_START_IN_BATTLE:
            in_battle_players = info.get('detail', [])
            players_cnt = len(in_battle_players)
            if players_cnt == 0:
                return
            format_info = []
            for uid in in_battle_players:
                format_info.append(self.room_info.get_player_name(uid) + ', ')

            if len(format_info) >= 4:
                format_info[2] = format_info[2][0:-2]
                format_info[3] = '...'
            else:
                format_info[-1] = format_info[-1][0:-2]
                while len(format_info) < 4:
                    format_info.append('')

            global_data.game_mgr.show_tip(get_text_by_id(19411, format_info), True)
        elif reason == const.ROOM_START_TEAM_NOENOUGH:
            global_data.game_mgr.show_tip(get_text_by_id(608164))
        elif reason == const.ROOM_START_PLAYER_NOENOUGH:
            battle_type = info.get('battle_type', -1)
            if battle_type == -1:
                return
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            if battle_info is None:
                return
            name_text_id = battle_info.get('cNameTID', -1)
            if name_text_id == -1:
                return
            min_player_num = int(battle_info.get('iMinPlayerNum', 0))
            global_data.game_mgr.show_tip(get_text_by_id(608163).format(min_player_num, get_text_by_id(name_text_id)))
        return

    @rpc_method(CLIENT_STUB, (Dict('info'),))
    def start_succ(self, info):
        self.room_info.update_room_battled_times(info.get('room_battled_times', 1))
        self.room_info.set_all_player_in_battle()

    def req_send_room_msg(self, msg):
        self.call_server_method('req_send_room_msg', msg)

    @rpc_method(CLIENT_STUB, (Int('uid'), Str('msg')))
    def on_room_msg(self, uid, msg):
        pass

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('info')))
    def update_roommate_info(self, uid, info):
        self.room_info.update_roommate_info(uid, info)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew') or global_data.ui_mgr.get_ui('RoomUI')
        if room_ui:
            room_ui.update_roommate_info(uid, info)

    def is_in_room(self):
        return self.room_info.rid != 0

    def get_room_type(self, battle_type):
        battle_config = confmgr.get('battle_config')
        return battle_config.get(str(battle_type), {}).get('bSupportCustom', 0)

    def _cache_room_ui(self, battle_type):
        room_type = self.get_room_type(battle_type)
        if room_type == 1:
            if not global_data.ui_mgr.get_ui('RoomUI'):
                from logic.comsys.room.RoomUI import RoomUI
                RoomUI(None, {})
        elif not global_data.ui_mgr.get_ui('RoomUINew'):
            from logic.comsys.room.RoomUINew import RoomUINew
            RoomUINew(None, {})
        return

    def req_transfer_ownership(self, uid):
        self.call_server_method('req_transfer_ownership', (uid,))

    @rpc_method(CLIENT_STUB, (Dict('room_info'),))
    def update_room_info(self, room_info):
        self.room_info.init_from_dict(room_info)

    def req_change_seat_with_someone(self, uid, seat_index):
        self.call_server_method('req_change_seat_with_someone', (uid, seat_index))

    @rpc_method(CLIENT_STUB, (Int('ask_uid'), Bool('succ'), Str('tips')))
    def ask_change_seat_ret(self, ask_uid, succ, tips):
        pass

    def req_change_map_area(self, area_info):
        self.call_server_method('req_change_map_area', (area_info,))

    @rpc_method(CLIENT_STUB, (Int('born_idx'),))
    def on_change_map_area(self, born_idx):
        self.room_info.update_room_born_idx(born_idx)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_change_map_area(born_idx)

    def req_roommate_online_state(self, uid_list):
        self.call_server_method('req_roommate_online_state', (uid_list, False))

    @rpc_method(CLIENT_STUB, (Dict('roommate_state'),))
    def on_roommate_online_state(self, roommate_state):
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.refresh_roommate_online_state(roommate_state)

    def get_room_dissolved_in_battle(self):
        return self._room_dissolved_in_battle

    def set_room_dissolved_in_battle(self, ret):
        self._room_dissolved_in_battle = ret

    def get_player_kicked_in_battle(self):
        return self._player_kicked_in_battle

    def set_player_kicked_in_battle(self, ret):
        self._player_kicked_in_battle = ret

    def req_dissolve_timestamp(self):
        self.call_server_method('req_dissolve_timestamp', ())

    @rpc_method(CLIENT_STUB, (Dict('dissolve_info'),))
    def on_update_dissolve_timestamp(self, dissolve_info):
        global_data.emgr.update_dissolve_timestamp.emit(dissolve_info)

    def req_search_room_list(self, search_str):
        add_common_search_salog(search_str)
        self.call_server_method('req_search_room_list', (search_str,))

    @rpc_method(CLIENT_STUB, (List('room_list'),))
    def on_search_room_list(self, room_list):
        room_list_ui = global_data.ui_mgr.get_ui('RoomListUINew')
        if room_list_ui:
            room_list_ui.on_search_room_list(room_list)

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('state')))
    def on_other_player_quit_battle_state(self, uid, state):
        self.room_info.update_player_battle_state(uid, state)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_other_player_quit_battle_state(uid, state)

    @rpc_method(CLIENT_STUB, (Int('uid'),))
    def on_room_all_player_quit_battle(self, uid):
        self.room_info.set_all_player_in_battle(state=const.BATTLE_STATE_INROOM)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.set_all_player_battle_state()

    def req_change_room_battle_type(self, room_info):
        self.call_server_method('req_change_room_battle_type', (room_info,))

    @rpc_method(CLIENT_STUB, (Dict('room_info'),))
    def on_change_room_battle_type(self, room_info):
        self.room_info.init_from_dict(room_info)
        players_info = room_info.get('players', {})
        self.room_info.players = {}
        for uid, data in six.iteritems(players_info):
            import copy
            player_data = copy.deepcopy(data)
            self.room_info.players[uid] = player_data

        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_change_room_battle_type(room_info)

    def invite_friend_into_room(self, uid):
        room_info = {'curr_player_num': len(self.room_info.players)
           }
        self.call_server_method('invite_friend_into_room', (uid, room_info))

    @rpc_method(CLIENT_STUB, (Int('inviter_uid'), Bool('succ'), Str('tips')))
    def room_invite_ret(self, inviter_uid, succ, tips):
        if tips:
            global_data.game_mgr.show_tip(unpack_text(tips))
        if succ:
            global_data.player.add_room_invite_count_down(inviter_uid, 60)

    def req_room_spectate_obj(self, room_mb, room_id):
        room_info = {'room_mb': room_mb,'room_id': room_id}
        self.call_server_method('req_room_spectate_obj', (room_info,))

    @rpc_method(CLIENT_STUB, (Int('room_id'), Int('spectate_obj')))
    def on_room_spectate_obj(self, room_id, spectate_obj):
        ui_inst = global_data.ui_mgr.get_ui('RoomListUINew')
        if ui_inst:
            ui_inst.on_room_spectate_obj(room_id, spectate_obj)

    def set_can_change_seat(self):
        self.call_server_method('set_can_change_seat', ())

    @rpc_method(CLIENT_STUB, (Bool('change_seat'),))
    def on_set_can_change_seat(self, change_seat):
        if change_seat:
            global_data.game_mgr.show_tip(get_text_by_id(609217), True)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(609218), True)
        self.room_info.update_room_info_by_key_value('can_change_seat', change_seat)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_set_can_change_seat(change_seat)

    def set_can_chat_in_room(self):
        self.call_server_method('set_can_chat_in_room', ())

    @rpc_method(CLIENT_STUB, (Bool('can_chat_in_room'),))
    def on_set_can_chat_in_room(self, can_chat_in_room):
        self.room_info.update_room_info_by_key_value('can_chat_in_room', can_chat_in_room)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        room_ui and room_ui.on_set_can_chat_in_room(can_chat_in_room)

    def set_can_leave_room(self):
        self.call_server_method('set_can_leave_room', ())

    @rpc_method(CLIENT_STUB, (Bool('can_leave_room'),))
    def on_set_can_leave_room(self, can_leave_room):
        self.room_info.update_room_info_by_key_value('can_leave_room', can_leave_room)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_set_can_leave_room(can_leave_room)

    def judgement_before_adjust_seat(self, uid, seat_index):
        self.call_server_method('judgement_before_adjust_seat', (uid, seat_index))

    def judgement_do_adjust_seat(self, uid, seat_index):
        self.call_server_method('judgement_do_adjust_seat', (uid, seat_index))

    def req_set_char_name_in_room(self, uid, char_name_in_room):
        self.call_server_method('set_char_name_in_room', (uid, char_name_in_room))

    @rpc_method(CLIENT_STUB, (Int('uid'), Str('char_name_in_room')))
    def on_set_char_name_in_room(self, uid, char_name_in_room):
        self.room_info.update_player_info_by_uid(uid, {'char_name_in_room': char_name_in_room})
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_set_char_name_in_room(uid, char_name_in_room)

    def set_competition_team_name(self, team_idx, team_name):
        self.call_server_method('set_competition_team_name', (team_idx, str(team_name)))

    @rpc_method(CLIENT_STUB, (Int('team_idx'), Str('team_name')))
    def on_set_competition_team_name(self, team_idx, team_name):
        self.room_info.update_team_name_by_idx(team_idx, team_name)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        room_ui and room_ui.on_set_competition_team_name(team_idx, team_name)

    def request_rejoin_competition_ob(self):
        self.call_server_method('request_rejoin_ob_global_spectate', ())

    def get_room_count_down(self):
        return self.room_count_down_dict

    def update_room_count_down(self):
        end_count_down_id = []
        for player_id in six.iterkeys(self.room_count_down_dict):
            self.room_count_down_dict[player_id] -= 1
            if self.room_count_down_dict[player_id] <= 0:
                end_count_down_id.append(player_id)

        global_data.emgr.room_invite_count_down_event.emit(self.room_count_down_dict)
        for i in end_count_down_id:
            self.room_count_down_dict.pop(i)

        if not self.room_count_down_dict:
            if self.room_count_down_timer:
                global_data.game_mgr.unregister_logic_timer(self.room_count_down_timer)
            self.room_count_down_timer = None
        return

    def add_room_invite_count_down(self, player_id, count_down):
        if player_id in self.room_count_down_dict:
            pass
        self.room_count_down_dict[player_id] = count_down
        if not self.room_count_down_timer:
            self.room_count_down_timer = global_data.game_mgr.register_logic_timer(self.update_room_count_down, interval=1, times=-1, mode=CLOCK)
        global_data.emgr.room_invite_count_down_event.emit(self.room_count_down_dict)

    def req_change_custom_battle_dict(self, customed_battle_dict):
        self.call_server_method('req_change_custom_battle_dict', (customed_battle_dict,))

    @rpc_method(CLIENT_STUB, (Dict('customed_battle_dict'),))
    def on_change_custom_battle_dict(self, customed_battle_dict):
        self.room_info.update_room_info_by_key_value('customed_battle_dict', customed_battle_dict)
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if room_ui:
            room_ui.on_change_custom_battle_dict(customed_battle_dict)

    def test_create_room(self):
        self.req_create_room({'max_team_size': 2,
           'max_team_cnt': 50,
           'battle_type': 7,
           'pwd': '',
           'name': '1234'
           })

    def get_cur_custom_room_info(self):
        return self.room_info.get_room_info()

    def get_custom_room_team_size(self):
        return self.room_info.max_team_size

    def get_custom_room_max_player_num(self):
        return self.room_info.max_team_cnt * self.room_info.max_team_size

    def get_custom_room_id(self):
        if self.room_info:
            return self.room_info.rid
        else:
            return 0

    def get_custom_room_battle_type(self):
        if self.room_info:
            return self.room_info.get_battle_type()
        else:
            return -1

    def is_custom_room_need_pwd(self):
        if self.room_info:
            if self.room_info.get_need_pwd():
                return 1
            return 0
        else:
            return 0

    def get_custom_room_is_of_week_competition(self):
        if self.room_info:
            return self.room_info.get_room_info().get('is_week_competition', False)
        return False

    def req_enter_week_competition(self):
        self.call_server_method('req_enter_week_competition')

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('reason'), Int('req_valid_ts')))
    def req_enter_week_competition_ret(self, ret, reason, req_valid_ts):
        pass

    def has_req_week_competition(self):
        if tutil.time() > self._req_valid_ts:
            self._has_req_week_competition = False
        return self._has_req_week_competition
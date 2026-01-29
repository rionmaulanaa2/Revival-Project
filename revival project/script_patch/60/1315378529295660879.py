# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impTeam.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List, Float
from logic.gcommon.time_utility import get_time, get_server_time
from logic.gcommon.ctypes.Team import Team
from common.utils.timer import CLOCK
import logic.gcommon.const as const
import version
import math
from logic.gcommon.common_const.log_const import TEAM_MODE_RECOMMEND
from logic.gcommon.common_const.team_const import HANG_UP_TIME
from common.platform import is_ios
from logic.gcommon.common_const.battle_const import DEFAULT_PVE_TID
from logic.gcommon.common_const.ui_operation_const import TEAM_ONLY_FRIEND_KEY
NEIGHBOR_CACHE_TIME = 60

class impTeam(object):

    def _init_team_from_dict(self, bdict):
        self._team = None
        self._self_ready = False
        self._ready_battle_type = None
        self._team_idx = None
        self._auto_flag = True
        self._recommend_players = []
        self._pve_recommend_players = []
        self.last_request_time = 0
        self.last_pve_request_time = 0
        self.show_recommend_tips = False
        self._refresh_public_team_ts = 0
        self._refresh_public_pve_team_ts = 0
        self.req_info_valid_time = 0
        self.req_info = None
        self.neighbor_valid_time = 0
        self.neighbor_players = None
        self._pve_battle_info = None
        self.count_down_dict = {}
        self.count_down_timer = None
        self._server_version = version.get_server_version()
        team_cceids = bdict.get('team_cceids', {})
        for uid, team_eid in six.iteritems(team_cceids):
            team_eid and global_data.ccmini_mgr.set_eid_map(team_eid, uid, const.TEAM_SESSION_ID)

        self.hang_up_ts = bdict.get('hangup_ts', 0)
        self.start_hang_up()
        return

    def _destroy_team(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
            self.count_down_timer = None
        self.count_down_dict = {}
        return

    def get_count_down(self):
        return self.count_down_dict

    def update_count_down(self):
        end_count_down_id = []
        for player_id in six.iterkeys(self.count_down_dict):
            self.count_down_dict[player_id] -= 1
            if self.count_down_dict[player_id] <= 0:
                end_count_down_id.append(player_id)

        global_data.emgr.team_invite_count_down_event.emit(self.count_down_dict)
        for i in end_count_down_id:
            self.count_down_dict.pop(i)

        if not self.count_down_dict:
            if self.count_down_timer:
                global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
            self.count_down_timer = None
        return

    def add_invite_count_down(self, player_id, count_down):
        if player_id in self.count_down_dict:
            pass
        self.count_down_dict[player_id] = count_down
        if not self.count_down_timer:
            self.count_down_timer = global_data.game_mgr.register_logic_timer(self.update_count_down, interval=1, times=-1, mode=CLOCK)
        global_data.emgr.team_invite_count_down_event.emit(self.count_down_dict)

    def is_in_team(self):
        return self._team is not None

    def get_team_cur_count(self):
        count = 1
        if self._team:
            mems = self._team.get_members()
            count += len(mems)
        return count

    def get_teammate(self, uid):
        if self._team:
            return self._team.get_teammate(uid)
        else:
            return None

    def get_team_info(self):
        if self._team:
            mems = self._team.get_members()
            return self._team.get_team_dict(mems)
        else:
            return None

    def get_team_size(self):
        if self._team:
            return self._team.get_size()
        return 0

    def is_team_full(self):
        if self._team:
            return self._team.get_size() >= self.get_max_team_size() - 1
        else:
            return False

    def get_self_auto_match(self):
        return self._auto_flag

    def is_all_ready(self):
        if self._team:
            mems = self._team.get_members()
            for uid, teamer in six.iteritems(mems):
                if not teamer.is_ready():
                    return False

        return True

    def get_team_idx(self):
        return self._team_idx

    def save_team_info(self, team_info):
        self._team = Team(team_info['leader'], team_info['team_id'], team_info['battle_type'], team_info['auto_match'], self.get_max_team_size())
        if team_info.get('public_info'):
            self._team.set_public_info(team_info.get('public_info'))
        self._self_ready = team_info.get('self_ready', False)
        self._ready_battle_type = team_info.get('ready_battle_type', None)
        self._team_idx = team_info.get('self_team_idx')
        mems = team_info['members']
        for uid, info in six.iteritems(mems):
            global_data.message_data.set_player_role_head_info({uid: (info.get('head_info_ts', 0), info['head_frame'], info['head_photo'])})
            self._team.add_teammate(uid, info)

        return

    def get_leader_id(self):
        if self._team:
            return self._team.get_leader()
        else:
            return None

    def get_teamate_info(self, uid):
        if self._team:
            return self._team.get_teammate_uinfo(uid)
        else:
            return None

    def is_leader(self, include_solo=True):
        leader_id = self.get_leader_id()
        return leader_id is None and include_solo or leader_id == self.uid

    def is_teammate(self, uid):
        if self._team:
            return uid in self._team.get_members()
        else:
            return False

    def has_someone_afk_punish_time(self):
        if self._team:
            mems = self._team.get_members()
            for uid, teamer in six.iteritems(mems):
                afk_punish_left_time = teamer.get_afk_punish_left_time()
                if afk_punish_left_time and afk_punish_left_time > 0:
                    return (True, teamer.get_char_name())

        return (
         False, '')

    def has_someone_imt_punish_time(self):
        if self._team:
            mems = self._team.get_members()
            for uid, teamer in six.iteritems(mems):
                imt_punish_left_time = teamer.get_imt_punish_left_time()
                if imt_punish_left_time and imt_punish_left_time > 0:
                    return (True, teamer.get_char_name())

        return (
         False, '')

    def has_someone_can_not_allow_match(self):
        if self._team:
            mems = self._team.get_members()
            for uid, teamer in six.iteritems(mems):
                allow_match_left_time = teamer.get_allow_match_left_time()
                if allow_match_left_time > 0:
                    return (False, teamer.get_char_name())

        return (
         True, '')

    def get_self_ready(self):
        return self._self_ready

    def invite_frd(self, frd_id, battle_tid, auto_match, mode):
        team_only_friend = global_data.player.get_setting_2(TEAM_ONLY_FRIEND_KEY)
        if not global_data.message_data.is_friend(frd_id) and team_only_friend:
            global_data.game_mgr.show_tip(635268)
            return
        else:
            if self.is_team_full():
                global_data.player.notify_client_message((get_text_by_id(13068),))
                return
            from logic.gcommon.common_utils import battle_utils
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN, PLAY_TYPE_DEATH
            from common.cfg import confmgr
            battle_info = confmgr.get('battle_config', str(battle_tid))
            play_type = battle_info['play_type']
            cur_team_count = self.get_team_cur_count()
            match_mode = cur_team_count + 1
            battle_type = battle_info['battle_type']
            opened = True
            if play_type == PLAY_TYPE_CHICKEN:
                nxt_battle_tid = battle_utils.get_battle_id_by_player_mode_and_type(play_type, match_mode, battle_type)
                opened = True
            if not opened:
                global_data.game_mgr.show_tip(get_text_by_id(13070))
                return False
            if global_data.player.is_in_room():
                global_data.game_mgr.show_tip(get_text_by_id(13048))
                return False
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if lobby_ui and lobby_ui.team_invite_widget and lobby_ui.team_invite_widget.nd_vis:
                mode = lobby_ui.team_invite_widget.get_cur_invite_mode()
            if global_data.message_data.is_friend(frd_id) and mode != TEAM_MODE_RECOMMEND:
                from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
                mode = TEAM_MODE_FRIEND
                frd_sv = global_data.message_data.get_friend_server_version(frd_id)
                if frd_sv is not None and frd_sv < self._server_version:
                    global_data.game_mgr.show_tip(get_text_by_id(189))
            self.call_server_method('invite_frd', (frd_id, battle_tid, auto_match, mode))
            return True

    @rpc_method(CLIENT_STUB, (Int('invite_uid'), Bool('succ'), Str('tips')))
    def invite_ret(self, invite_uid, succ, tips):
        if tips:
            global_data.game_mgr.show_tip(unpack_text(tips))
        if succ:
            global_data.player.add_invite_count_down(invite_uid, 60)

    @rpc_method(CLIENT_STUB, (Dict('inviter_info'),))
    def be_invited(self, inviter_info):
        ui = global_data.ui_mgr.show_ui('InviteConfirmUI', 'logic.comsys.lobby')
        ui.set_invite_info(inviter_info)

    def agree_invite(self, frd_id):
        self.call_server_method('agree_invite', (frd_id,))

    def req_leave_team(self):
        self.call_server_method('try_leave_team', ())

    def kick_teammate(self, teammate_uid):
        self.call_server_method('kick_teammate', (teammate_uid,))

    @rpc_method(CLIENT_STUB, (Dict('team_info'),))
    def join_team(self, team_info):
        self.save_team_info(team_info)
        global_data.emgr.player_join_team_event.emit(team_info)
        mems = self._team.get_members()
        uid_list = six_ex.keys(mems)
        global_data.emgr.close_simple_inf_ui.emit(uid_list)
        for uid in uid_list:
            if uid in self.count_down_dict:
                self.count_down_dict[uid] = 0

        self._auto_flag = self._team.get_team_dict(mems).get('auto_match', True)
        global_data.ccmini_mgr.create_speaking_list_timer()
        global_data.ccmini_mgr.clean_eid_map()
        info = team_info.get('members', None)
        for uid, tinfo in six.iteritems(info):
            tinfo['team_eid'] and global_data.ccmini_mgr.set_eid_map(tinfo['team_eid'], uid, const.TEAM_SESSION_ID)

        global_data.message_data.request_player_online_state(immediately=True)
        if not self.is_leader():
            self.hang_up_ts = team_info.get('hangup_ts', 0)
            self.start_hang_up()
        battle_info = team_info.get('battle_info')
        if battle_info:
            global_data.emgr.pve_battle_info_change_event.emit(battle_info)
        self.set_init_match_info()
        return

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('uinfo')))
    def update_uinfo(self, uid, uinfo):
        if self._team:
            self._team.update_teamer_info(uid, uinfo)
        uinfo['team_eid'] and global_data.ccmini_mgr.set_eid_map(uinfo['team_eid'], uid, const.TEAM_SESSION_ID)
        if uinfo.get('group_eid'):
            print('group_eid', uinfo.get('group_eid'))
            global_data.ccmini_mgr.set_eid_map(uinfo['group_eid'], uid, const.TEAM_ALL_SESSION_ID)
            if uinfo.get('team_eid'):
                global_data.ccmini_mgr.mute_duplicated_session_eid(uinfo.get('group_eid'), True, const.TEAM_ALL_SESSION_ID)
        if uinfo.get('group_eid') and not uinfo.get('team_eid'):
            global_data.ccmini_mgr.mute_duplicated_session_eid(uid, False, const.TEAM_ALL_SESSION_ID)
        if global_data.is_inner_server:
            print('update_uinfo', uid, uinfo)
        if self._team:
            updated_uinfo = self._team.get_teammate_uinfo(uid)
            global_data.emgr.player_teammate_info_update_event.emit(uid, updated_uinfo)
        global_data.message_data.set_player_role_head_info({uid: (uinfo.get('head_info_ts', 0), uinfo.get('head_frame'), uinfo.get('head_photo'))})

    @rpc_method(CLIENT_STUB, (Dict('teammate_info'), Int('battle_ty pe'), Bool('auto_match')))
    def add_teammate(self, teammate_info, battle_type, auto_match):
        uid = teammate_info['uid']
        global_data.emgr.close_simple_inf_ui.emit(uid)
        if uid in self.count_down_dict:
            self.count_down_dict[uid] = 0
        if self._team:
            self._team.add_teammate(uid, teammate_info)
        global_data.ccmini_mgr.set_eid_map(teammate_info['team_eid'], uid, session_id=const.TEAM_SESSION_ID)
        if self._team:
            global_data.emgr.player_add_teammate_event.emit(teammate_info)
        self.update_match_info_imp(battle_type, auto_match)
        global_data.message_data.request_player_online_state(immediately=True)
        self.set_init_match_info()

    @rpc_method(CLIENT_STUB, (Int('teammate_uid'), Int('leader_uid'), Str('show_msg')))
    def del_teammate(self, teammate_uid, leader_uid, show_msg):
        if not self._team:
            return
        else:
            if show_msg:
                self.show_msg_imp(show_msg)
            old_leader = self._team.get_leader()
            self._team.del_teammate(teammate_uid)
            self._team.set_leader(leader_uid)
            global_data.emgr.player_del_teammate_event.emit(teammate_uid)
            if old_leader != leader_uid:
                global_data.emgr.player_change_leader_event.emit(leader_uid)
            self.set_init_match_info()
            self._pve_battle_info = None
            return

    @rpc_method(CLIENT_STUB, (Int('teammate_uid'),))
    def teammate_offline(self, teammate_uid):
        teammate = self.get_teammate(teammate_uid)
        if teammate:
            self.notify_client_message((pack_text(13071, {'playername': teammate.get_char_name()}),))
        frds_state = {teammate_uid: const.STATE_OFFLINE}
        self.on_one_player_state((frds_state,))

    @rpc_method(CLIENT_STUB, (Int('teammate_uid'),))
    def teammate_online(self, teammate_uid):
        teammate = self.get_teammate(teammate_uid)
        if teammate:
            self.notify_client_message((pack_text(610943, {'playername': teammate.get_char_name()}),))
        frds_state = {teammate_uid: const.STATE_TEAM}
        self.on_one_player_state((frds_state,))

    @rpc_method(CLIENT_STUB, ())
    def leave_team(self):
        self._team = None
        self._team_idx = None
        self._pve_battle_info = None
        self.hang_up_ts = 0
        global_data.emgr.player_leave_team_event.emit()
        global_data.ccmini_mgr.logout_session(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.destroy_speaking_list_timer()
        self.clear_ccmini_team()
        return

    def get_ready(self, is_ready, battle_tid, auto_match):
        if is_ready:
            self.apply_match(battle_tid)
        self.call_server_method('set_ready_state', (is_ready, battle_tid, auto_match))

    def get_ready_battle_type(self):
        return self._ready_battle_type

    def apply_not_ready_match(self, battle_type):
        self.call_server_method('apply_not_ready_match', (battle_type,))

    @rpc_method(CLIENT_STUB, (Int('uid'), Bool('is_ready'), Int('battle_type')))
    def set_ready_state(self, uid, is_ready, battle_type=None):
        if uid == global_data.player.uid:
            self._self_ready = is_ready
            if is_ready:
                self._ready_battle_type = battle_type
        elif self._team and self._team.get_teammate(uid):
            teamer = self._team.get_teammate(uid)
            info = teamer.get_info()
            info['ready'] = is_ready
            info['battle_type'] = battle_type
        global_data.emgr.player_set_ready_event.emit(uid, is_ready, battle_type)

    @rpc_method(CLIENT_STUB, (Int('tip'),))
    def reset_ready_state(self, tip):
        self.show_client_notice((pack_text(tip),))
        self.reset_teammates_ready_state(())

    @rpc_method(CLIENT_STUB, ())
    def reset_teammates_ready_state(self):
        self._self_ready = False
        if self._team:
            teamers = self._team.get_members()
            for uid, member in six.iteritems(teamers):
                info = member.get_info()
                info['ready'] = False
                battle_type = info.get('battle_type', None)
                global_data.emgr.player_set_ready_event.emit(uid, False, battle_type)

            global_data.emgr.player_set_ready_event.emit(self.uid, False, self.get_ready_battle_type())
        return

    def set_init_match_info(self):
        if self._team and self.is_leader():
            ui = global_data.ui_mgr.get_ui('PVELevelWidgetUI')
            chapter, difficulty, pve_player_size = ui.get_match_info() if ui else (None,
                                                                                   None,
                                                                                   None)
            chapter = chapter or self.get_last_pve_chapter()
            difficulty = difficulty or self.get_last_pve_difficulty()
            pve_player_size = pve_player_size or self.get_team_cur_count()
            battle_info = {}
            battle_info['chapter'] = chapter
            battle_info['difficulty'] = difficulty
            battle_info['pve_player_size'] = pve_player_size
            self.call_server_method('init_pve_match_info', (battle_info,))
        return None

    def set_match_info(self, battle_tid, auto_match, battle_info=None):
        self._auto_flag = auto_match
        if battle_info is None:
            battle_info = {}
        self.call_server_method('set_match_info', (battle_tid, auto_match, battle_info))
        return

    @rpc_method(CLIENT_STUB, (Int('battle_type'), Bool('auto_match'), Dict('battle_info')))
    def update_match_info(self, battle_type, auto_match, battle_info):
        self.update_match_info_imp(battle_type, auto_match, battle_info)

    def update_match_info_imp(self, battle_tid, auto_match, battle_info=None):
        if self._team:
            self._team.set_battle_type(battle_tid)
            self._team.set_auto_match(auto_match)
            self._auto_flag = auto_match
            self._pve_battle_info = battle_info
        print('update_match_info_imp', battle_tid, auto_match)
        global_data.emgr.player_match_info_change_event.emit(battle_tid, auto_match)
        if battle_info:
            global_data.emgr.pve_battle_info_change_event.emit(battle_info)

    def get_pve_battle_info(self):
        return self._pve_battle_info

    def apply_join_team(self, target_uid, need_confirm=False, is_public=False):
        self.call_server_method('apply_join_team', (target_uid, need_confirm, is_public))

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('clothing_dict')))
    def teammate_dress_clothing(self, uid, clothing_dict):
        pass

    @rpc_method(CLIENT_STUB, (Int('uid'), List('part_list')))
    def teammate_undress_clothing(self, uid, part_list):
        pass

    def request_recommend_teammates(self, game_type, show_tips=False):
        self.show_recommend_tips = show_tips
        cur_time = get_time()
        if game_type == DEFAULT_PVE_TID:
            off_time = cur_time - self.last_pve_request_time
        else:
            off_time = cur_time - self.last_request_time
        interval_time = 11
        if off_time >= interval_time:
            if game_type == DEFAULT_PVE_TID:
                self.last_pve_request_time = cur_time
            else:
                self.last_request_time = cur_time
            print('request_recommend_team', game_type)
            self.call_server_method('request_recommend_team', (game_type,))
        elif show_tips:
            global_data.player.notify_client_message((get_text_by_id(13081).format(data_time=interval_time - int(off_time)),))

    @rpc_method(CLIENT_STUB, (Int('game_type'), List('recommend_players')))
    def on_get_recommend_teammates_result(self, game_type, recommend_players):
        print('on_get_recommend_teammates_result', game_type, recommend_players)
        if not recommend_players and self.show_recommend_tips:
            global_data.player.notify_client_message((get_text_by_id(13097),))
            return
        from common.const.property_const import U_ID
        import logic.gcommon.const as const
        if global_data.player:
            frds_state = {info[U_ID]:const.STATE_SINGLE for info in recommend_players}
            self.on_one_player_state((frds_state,))
        if game_type == DEFAULT_PVE_TID:
            self._pve_recommend_players = recommend_players
            global_data.emgr.refresh_recommend_teammates.emit(recommend_players)
        else:
            self._recommend_players = recommend_players
            global_data.emgr.refresh_recommend_teammates.emit(recommend_players)

    def get_recommend_players(self):
        return self._recommend_players

    def get_pve_recommend_players(self):
        return self._pve_recommend_players

    def create_public_team(self, public_info):
        self.call_server_method('create_public_team', (public_info,))

    def modify_public_team(self, new_public_info):
        if not self._team:
            return
        public_info = self._team.get_public_info()
        if public_info and public_info.get('leader_uid') == self.uid:
            self.call_server_method('modify_public_team', (new_public_info,))

    def check_can_request_public_teams(self, battle_type):
        now = get_time()
        is_pve = battle_type == DEFAULT_PVE_TID
        if is_pve:
            if self._refresh_public_pve_team_ts > now:
                return False
        elif self._refresh_public_team_ts > now:
            return False
        return True

    def request_public_teams(self, battle_type, start, end, show_tips=True):
        is_pve = battle_type == DEFAULT_PVE_TID
        if self.check_can_request_public_teams(battle_type):
            now = get_time()
            if is_pve:
                self._refresh_public_pve_team_ts = now + 2
            else:
                self._refresh_public_team_ts = now + 2
            self.call_server_method('request_public_teams', (battle_type, start, end))
        else:
            show_tips and global_data.game_mgr.show_tip(get_text_by_id(609400))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('start'), Int('end'), List('data')))
    def on_request_public_teams_result(self, ret, start, end, data):
        if not ret:
            return
        global_data.emgr.refresh_public_teams.emit(start, end, data)

    @rpc_method(CLIENT_STUB, (Str('op_type'), Dict('team_info')))
    def update_public_team_info(self, op_type, team_info):
        if op_type == 'UPDATE':
            if self._team:
                self._team.get_public_info().update(team_info)
            global_data.emgr.refresh_public_single_team.emit(op_type, team_info)
        elif op_type == 'DELETE':
            if self._team:
                self._team.set_public_info({})
            global_data.emgr.refresh_public_single_team.emit(op_type, team_info)

    def auto_join_public_team(self, battle_type):
        from common.audio.ccmini_mgr import LOBBY_TEAM_SPEAKER, LOBBY_TEAM_MIC
        team_voice = global_data.message_data.get_seting_inf(LOBBY_TEAM_SPEAKER)
        team_mic = global_data.message_data.get_seting_inf(LOBBY_TEAM_MIC)
        self.call_server_method('auto_join_public_team', (battle_type, {'has_voice': bool(team_voice and team_mic)}))

    @rpc_method(CLIENT_STUB, (Int('leader_uid'), Bool('need_voice')))
    def auto_join_public_team_ret(self, leader_uid, need_voice):
        if need_voice:
            from common.audio.ccmini_mgr import LOBBY_TEAM_SPEAKER, LOBBY_TEAM_MIC
            global_data.message_data.set_seting_inf(LOBBY_TEAM_SPEAKER, 1)
            global_data.message_data.set_seting_inf(LOBBY_TEAM_MIC, 1)
        global_data.player.apply_join_team(leader_uid, is_public=True)

    def end_hang_up(self):
        self.call_server_method('end_hang_up')
        self.hang_up_ts = 0
        global_data.ui_mgr.close_ui('HangUpUI')

    def start_hang_up(self):
        if self.is_hang_up():
            ui = global_data.ui_mgr.show_ui('HangUpUI', 'logic.comsys.lobby')
            ui.start_hang_up(self.hang_up_ts)
            global_data.emgr.battle_match_status_event.emit(False)

    def is_hang_up(self):
        cur_time = get_server_time()
        return cur_time < self.hang_up_ts

    def reserve_friend(self, frd_uid, msg):
        self.call_server_method('reserve_friend', (frd_uid, msg))

    @rpc_method(CLIENT_STUB, (Int('frd_uid'), Bool('succ'), Str('tips')))
    def reserve_ret(self, frd_uid, succ, tips):
        if tips:
            global_data.game_mgr.show_tip(unpack_text(tips))
        if succ:
            pass

    def confirm_join_if_in_team(self, confirm):
        self.call_server_method('confirm_join_if_in_team', (confirm,))

    @rpc_method(CLIENT_STUB, (Int('frd_uid'), Str('msg')))
    def reserve_friend_ack(self, frd_uid, msg):
        if frd_uid and msg:
            from common.const.property_const import C_NAME, U_LV, CLAN_ID
            friends = global_data.message_data.get_friends()
            if not friends:
                return
            fd_info = friends.get(frd_uid)
            if fd_info:
                chat_name = fd_info.get(C_NAME, '')
                chat_lv = fd_info.get(U_LV, 1)
                frd_cid = fd_info.get(CLAN_ID, -1)
                global_data.message_data.recv_to_friend_msg(frd_uid, chat_name, msg, chat_lv)
                global_data.player.req_friend_msg(frd_uid, chat_lv, frd_cid, msg)

    def try_get_neighbor_player(self):
        cur_time = get_server_time()
        if self.neighbor_players and cur_time <= self.neighbor_valid_time:
            global_data.emgr.message_on_get_neighbor_player.emit(self.neighbor_players)
        elif self.req_info and cur_time <= self.req_info_valid_time:
            self.request_neighbor_player()
        else:
            global_data.emgr.message_on_get_nearby_req_info += self.request_neighbor_player
            global_data.channel.get_nearby_req_info()
        return self.neighbor_players

    def request_neighbor_player(self, req_info=None):
        if req_info is None:
            req_info = self.req_info
        else:
            self.req_info = req_info
            self.req_info_valid_time = get_server_time() + NEIGHBOR_CACHE_TIME
        if 'system' not in req_info or 'location' not in req_info:
            return
        else:
            plat = req_info['system']['platform']
            lat = req_info['location'][plat]['lat']
            log = req_info['location'][plat]['log']
            import json
            self.call_server_method('request_neighbor', (str(lat), str(log), json.dumps(req_info)))
            global_data.emgr.message_on_get_nearby_req_info -= self.request_neighbor_player
            return

    @rpc_method(CLIENT_STUB, (Dict('neighbor_players'),))
    def reply_neighbor_player(self, neighbor_players):
        self.neighbor_valid_time = get_server_time() + NEIGHBOR_CACHE_TIME
        self.neighbor_players = neighbor_players
        global_data.emgr.message_on_get_neighbor_player.emit(self.neighbor_players)

    @rpc_method(CLIENT_STUB, (Bool('is_pve'),))
    def notify_rematch(self, is_pve):
        from logic.gcommon.common_const.team_const import TEAMMATE_MATCH_AGAIN_TYPE_NORMAL, TEAMMATE_MATCH_AGAIN_TYPE_PVE
        print('notify_rematch', is_pve)
        self.teammate_match_again_type = TEAMMATE_MATCH_AGAIN_TYPE_PVE if is_pve else TEAMMATE_MATCH_AGAIN_TYPE_NORMAL
        global_data.emgr.on_notify_rematch.emit(is_pve)
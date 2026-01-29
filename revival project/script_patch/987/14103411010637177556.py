# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLobby.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
LOGIN_TIMESTAMP = {}

class impLobby(object):

    def _init_lobby_from_dict(self, bdict):
        global LOGIN_TIMESTAMP
        self.lobby = None
        self._mecha_open = bdict.get('mecha_open', {})
        lobby_mecha_info = bdict.get('lobby_mecha_info', {})
        self._selected_mecha_item_id = lobby_mecha_info.get('lobby_mecha_id', 101008001)
        self._selected_mecha_id = None
        self._teammate_mecha_dict = {}
        self._lobby_register_for_team = False
        self.register_lobby_team_event()
        if self.uid not in LOGIN_TIMESTAMP:
            LOGIN_TIMESTAMP[self.uid] = global_data.game_time
        self.client_login_time = LOGIN_TIMESTAMP[self.uid]
        return

    def register_lobby_team_event(self):
        if self._lobby_register_for_team:
            return
        self._lobby_register_for_team = True
        global_data.emgr.player_add_teammate_event += self.on_player_add_teammate
        global_data.emgr.player_del_teammate_event += self.on_player_del_teammate
        global_data.emgr.player_teammate_info_update_event += self.on_player_teammate_info_update
        global_data.emgr.player_join_team_event += self.on_player_join_team
        global_data.emgr.player_leave_team_event += self.on_player_leave_team

    def unregister_lobby_team_event(self):
        if self._lobby_register_for_team:
            global_data.emgr.player_add_teammate_event -= self.on_player_add_teammate
            global_data.emgr.player_del_teammate_event -= self.on_player_del_teammate
            global_data.emgr.player_teammate_info_update_event -= self.on_player_teammate_info_update
            global_data.emgr.player_join_team_event -= self.on_player_join_team
            global_data.emgr.player_leave_team_event -= self.on_player_leave_team
        self._lobby_register_for_team = False

    def register_lobby_visit_event(self):
        global_data.emgr.visit_player_add_teammate_event += self.on_player_add_teammate
        global_data.emgr.visit_player_del_teammate_event += self.on_player_del_teammate
        global_data.emgr.visit_player_teammate_info_update_event += self.on_player_teammate_info_update

    def unregister_lobby_visit_event(self):
        global_data.emgr.visit_player_add_teammate_event -= self.on_player_add_teammate
        global_data.emgr.visit_player_del_teammate_event -= self.on_player_del_teammate
        global_data.emgr.visit_player_teammate_info_update_event -= self.on_player_teammate_info_update

    def reset_lobby(self, lobby):
        self.lobby = lobby

    def get_lobby(self):
        return self.lobby

    def read_mecha_open_info(self):
        return self._mecha_open

    def get_battle_mecha_open_list(self, battle_play_type):
        opened_mechas = self._mecha_open['opened_order']
        exclude_play_types = self._mecha_open.get('exclude_play_types', {})
        if not exclude_play_types:
            return opened_mechas
        candidate_mechas = [ mecha_id for mecha_id in opened_mechas if battle_play_type not in exclude_play_types.get(mecha_id, [])
                           ]
        return candidate_mechas

    def get_teammate_mecha_dict(self):
        return self._teammate_mecha_dict

    def get_lobby_selected_mecha_id(self):
        if not self._selected_mecha_id:
            self._selected_mecha_id = mecha_lobby_id_2_battle_id(self._selected_mecha_item_id)
        return self._selected_mecha_id

    def get_lobby_selected_mecha_item_id(self):
        return self._selected_mecha_item_id

    def req_change_lobby_mecha(self, mecha_id):
        if not self._selected_mecha_id:
            self._selected_mecha_id = mecha_lobby_id_2_battle_id(self._selected_mecha_item_id)
        if self._selected_mecha_id == mecha_id:
            return
        mecha_lobby_id = battle_id_to_mecha_lobby_id(mecha_id)
        if not mecha_lobby_id:
            return
        self.call_server_method('lobby_select_mecha', (mecha_lobby_id,))

    @rpc_method(CLIENT_STUB, (Int('new_mecha_id'),))
    def on_lobby_mecha_changed(self, new_mecha_id):
        self._selected_mecha_item_id = new_mecha_id
        self._selected_mecha_id = mecha_lobby_id_2_battle_id(new_mecha_id)
        global_data.emgr.on_lobby_mecha_changed.emit()

    @rpc_method(CLIENT_STUB, (Int('slot'), Int('new_mecha_id')))
    def on_display_mecha_changed(self, slot, new_mecha_id):
        pass

    def req_change_display_mecha(self, slot, mecha_id):
        self.call_server_method('lobby_select_display_mecha', (slot, mecha_id))

    def on_player_join_team(self, team_info):
        members = team_info.get('members', {})
        for uid, teammate_info in six.iteritems(members):
            if uid != self.uid:
                self.on_player_add_teammate(teammate_info)

    def on_player_add_teammate(self, teammate_info):
        uid = teammate_info['uid']
        lobby_mecha_info = teammate_info.get('lobby_mecha_info', {})
        if 'team_idx' in teammate_info:
            lobby_mecha_info['team_idx'] = teammate_info['team_idx']
        self._teammate_mecha_dict[uid] = lobby_mecha_info
        global_data.emgr.player_add_teammate_mech_event.emit(teammate_info)

    def on_player_del_teammate(self, teammate_uid):
        if teammate_uid in self._teammate_mecha_dict:
            del self._teammate_mecha_dict[teammate_uid]
        global_data.emgr.player_del_teammate_mech_event.emit(teammate_uid)

    def on_player_teammate_info_update(self, uid, updated_uinfo):
        if not updated_uinfo:
            return
        else:
            lobby_mecha_info = updated_uinfo.get('lobby_mecha_info', {})
            if not lobby_mecha_info or self._teammate_mecha_dict.get(uid, None) == lobby_mecha_info:
                return
            if 'team_idx' in updated_uinfo:
                lobby_mecha_info['team_idx'] = updated_uinfo['team_idx']
            self._teammate_mecha_dict[uid] = lobby_mecha_info
            global_data.emgr.player_teammate_mech_update_event.emit(uid, updated_uinfo)
            return

    def on_player_leave_team(self):
        self._teammate_mecha_dict = {}
        global_data.emgr.player_teammate_mech_clean_event.emit()

    def enter_lobby_to_visit(self, is_visit_self):
        if is_visit_self:
            return
        self.unregister_lobby_team_event()
        self.register_lobby_visit_event()
        self._teammate_mecha_dict = {}
        members = self.get_visit_team_members()
        if not members:
            return
        for uid, info in six.iteritems(members):
            if uid == self.get_visit_uid():
                continue
            self.on_player_add_teammate(info)

    def leave_lobby_to_visit(self, is_visit_self):
        if is_visit_self:
            return
        self.unregister_lobby_visit_event()
        self.register_lobby_team_event()
        self._teammate_mecha_dict = {}
        team_info = self.get_team_info()
        if not team_info:
            return
        members = team_info.get('members')
        if not members:
            return
        for uid, info in six.iteritems(members):
            if uid == self.uid:
                continue
            self.on_player_add_teammate(info)
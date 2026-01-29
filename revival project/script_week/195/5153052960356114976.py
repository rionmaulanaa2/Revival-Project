# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCCMini.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
import logic.gcommon.const as const
import json

class impCCMini(object):

    def _init_ccmini_from_dict(self, bdict):
        self.cur_ccmini_team_id = None
        global_data.emgr.ccmini_start_capture += self.on_ccmini_start_capture
        global_data.emgr.ccmini_stop_capture += self.on_ccmini_stop_capture
        return

    def _destroy_ccmini(self):
        global_data.emgr.ccmini_start_capture -= self.on_ccmini_start_capture
        global_data.emgr.ccmini_stop_capture -= self.on_ccmini_stop_capture

    def req_team_login_session_data(self):
        team_info = self.get_team_info() or {}
        if self.cur_ccmini_team_id == team_info.get('team_id'):
            global_data.game_mgr.delay_exec(0.2, lambda : global_data.ccmini_mgr.reset_session_state(const.TEAM_SESSION_ID, reset_ignore_voice=True))
            log_error('reset_session_state because of same team', self.cur_ccmini_team_id)
            return
        print ('req_team_login_session_data', team_info.get('team_id'), self.cur_ccmini_team_id)
        self.cur_ccmini_team_id = team_info.get('team_id')
        self.call_server_method('req_team_login_session_data')

    def clear_ccmini_team(self):
        self.cur_ccmini_team_id = None
        return

    def req_near_login_session_data(self):
        self.call_server_method('req_near_login_session_data')

    def req_group_login_session_data(self):
        self.call_server_method('req_group_battle_session_data')

    @rpc_method(CLIENT_STUB, (Dict('login_session_data'),))
    def on_team_login_session_data(self, login_session_data):
        self._on_team_login_session_data(login_session_data)

    def _on_team_login_session_data(self, login_session_data):
        global_data.ccmini_mgr.logout_session(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.set_login_session_info(const.TEAM_SESSION_ID, login_session_data)
        global_data.ccmini_mgr.login_session(const.TEAM_SESSION_ID)

    @rpc_method(CLIENT_STUB, (Dict('login_session_data'),))
    def on_near_login_session_data(self, login_session_data):
        global_data.ccmini_mgr.logout_session(const.NEAR_SESSION_ID)
        global_data.ccmini_mgr.set_login_session_info(const.NEAR_SESSION_ID, login_session_data)
        global_data.ccmini_mgr.login_session(const.NEAR_SESSION_ID)

    @rpc_method(CLIENT_STUB, (Dict('team_eids'),))
    def on_team_eids(self, team_eids):
        pass

    @rpc_method(CLIENT_STUB, (Dict('group_battle_session_data'),))
    def on_group_battle_session_data(self, group_battle_session_data):
        global_data.ccmini_mgr.logout_session(const.TEAM_ALL_SESSION_ID)
        global_data.ccmini_mgr.set_login_session_info(const.TEAM_ALL_SESSION_ID, group_battle_session_data)
        global_data.ccmini_mgr.login_session(const.TEAM_ALL_SESSION_ID)

    def on_ccmini_start_capture(self):
        if self.is_in_battle():
            self.call_soul_method('ccmini_start_capture')

    def on_ccmini_stop_capture(self):
        if self.is_in_battle():
            self.call_soul_method('ccmini_stop_capture')
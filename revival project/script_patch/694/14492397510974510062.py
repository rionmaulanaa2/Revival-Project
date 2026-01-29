# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impConfirm.py
from __future__ import absolute_import
import six
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from logic.gcommon.time_utility import get_server_time
BLOCK_TIME = 300

class impConfirm(object):

    def _init_confirm_from_dict(self, bdict):
        self.block_invite_dict = {int(uid):ts for uid, ts in six.iteritems(bdict.get('block_invite_dict', {}))}
        self.reserve_info = None
        return

    @rpc_method(CLIENT_STUB, (Int('confirm_id'), Str('title'), List('option'), Int('confirm_type'), Dict('extra_info')))
    def confirm(self, confirm_id, title, option, confirm_type, extra_info):
        from logic.gcommon.const import CONFIRM_NORMAL, CONFIRM_TEAM_INVITE, CONFIRM_TEAM_JOIN, CONFIRM_CHANGE_SEAT, CONFIRM_ROOM_INVITE, CONFIRM_TEAM_RESERVE, CONFIRM_MATCH_READY
        from logic.vscene import scene_type
        if confirm_type == CONFIRM_NORMAL:
            if global_data.scene_type == scene_type.SCENE_TYPE_LOBBY:
                ui = global_data.ui_mgr.show_ui('InviteConfirmUI', 'logic.comsys.lobby')
                ui.set_invite_info(confirm_id, title, option, confirm_cb=lambda : global_data.ui_mgr.close_ui('MechaARMainUI1'))
        elif confirm_type in (CONFIRM_TEAM_INVITE, CONFIRM_TEAM_JOIN):
            from_uid = extra_info.get('uid')
            cur_time = get_server_time()
            if cur_time - self.block_invite_dict.get(from_uid, 0) > BLOCK_TIME:
                if global_data.scene_type == scene_type.SCENE_TYPE_LOBBY or global_data.ex_scene_mgr_agent.check_settle_scene_active():
                    ui = global_data.ui_mgr.show_ui('InviteTeamConfirmUI' if confirm_type == CONFIRM_TEAM_INVITE else 'TeamRequestConfirmUI', 'logic.comsys.lobby')
                    ui.set_invite_info(confirm_id, extra_info, confirm_type)
        elif confirm_type == CONFIRM_CHANGE_SEAT:
            if global_data.scene_type == scene_type.SCENE_TYPE_LOBBY:
                ui = global_data.ui_mgr.show_ui('TeamRequestConfirmUI', 'logic.comsys.lobby')
                ui.set_invite_info(confirm_id, extra_info, confirm_type)
        elif confirm_type == CONFIRM_ROOM_INVITE:
            if global_data.scene_type == scene_type.SCENE_TYPE_LOBBY:
                ui = global_data.ui_mgr.show_ui('InviteRoomConfirmUI', 'logic.comsys.lobby')
                ui.set_invite_info(confirm_id, extra_info, confirm_type)
        elif confirm_type == CONFIRM_TEAM_RESERVE:
            from_uid = extra_info.get('uid')
            cur_time = get_server_time()
            if not extra_info.get('join_team_confirm'):
                extra_info['timestamp'] = get_server_time()
                ui = global_data.ui_mgr.get_ui('FightChatUI')
                ui and ui.add_invitation(confirm_id, extra_info)
            elif extra_info.get('join_team_confirm'):
                self.reserve_info = (confirm_id, extra_info, confirm_type)
        elif confirm_type == CONFIRM_MATCH_READY:
            if global_data.scene_type == scene_type.SCENE_TYPE_LOBBY:
                ui = global_data.ui_mgr.show_ui('MatchReadyConfirmUI', 'logic.comsys.lobby')
                ui.set_invite_info(confirm_id, title, option, extra_info, confirm_cb=lambda : global_data.ui_mgr.close_ui('MechaARMainUI1'))

    def req_confirm(self, confirm_id, choice):
        self.call_server_method('confirm', (confirm_id, choice))

    def block_invite(self, uid):
        self.block_invite_dict[uid] = get_server_time()

    def show_reserve_info(self):
        if not self.reserve_info:
            return
        else:
            confirm_id, extra_info, confirm_type = self.reserve_info
            ui = global_data.ui_mgr.show_ui('AppointmentConfirmUI', 'logic.comsys.lobby')
            ui.set_invite_info(confirm_id, extra_info, confirm_type)
            self.reserve_info = None
            return
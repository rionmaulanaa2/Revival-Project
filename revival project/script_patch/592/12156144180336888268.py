# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLive.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Dict, List, Int, Str
from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
from logic.gcommon.common_utils.local_text import get_text_by_id

class impLive(object):

    def _init_live_from_dict(self, bdict):
        self._live_enable_dict = bdict.get('live_enable', {})

    def enable_live(self, kind):
        return self._live_enable_dict.get(kind, False)

    def send_live_dammu(self, msg, channel_id, kind):
        dic = {'channel_id': channel_id,'msg': msg}
        self.call_server_method('send_live_danmu', (kind, dic))

    def follow_anchor(self, kind, anchor_id):
        anchor_id = str(anchor_id)
        self.call_server_method('follow_anchor', (kind, anchor_id))

    def unfollow_anchor(self, kind, anchor_id):
        anchor_id = str(anchor_id)
        self.call_server_method('unfollow_anchor', (kind, anchor_id))

    @rpc_method(CLIENT_STUB, (Bool('succ'), Int('kind'), Str('anchor_id')))
    def follow_anchor_ret(self, succ, kind, anchor_id):
        if succ:
            LivePlatformManager().follow_anchor(kind, anchor_id)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2188))

    @rpc_method(CLIENT_STUB, (Bool('succ'), Int('kind'), Str('anchor_id')))
    def unfollow_anchor_ret(self, succ, kind, anchor_id):
        if succ:
            LivePlatformManager().unfollow_anchor(kind, anchor_id)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(2189))

    def require_follow_anchor_status(self, kind):
        self.call_server_method('get_followed_anchor_status', (kind,))

    @rpc_method(CLIENT_STUB, (Int('kind'), Dict('anchor_list')))
    def reply_followed_anchor_status(self, kind, anchor_list):
        self.on_replay_followed_anchor_status(kind, anchor_list)

    def on_replay_followed_anchor_status(self, kind, anchor_list_dict):
        LivePlatformManager().receive_anchor_live_list(kind, 1, anchor_list_dict)

    def request_live_room_list(self, kind, page):
        self.call_server_method('request_live_room_list', (kind, page))

    @rpc_method(CLIENT_STUB, (Int('kind'), Dict('room_info')))
    def reply_live_room_list(self, kind, room_info):
        self.on_replay_live_room_list(kind, room_info)

    def on_replay_live_room_list(self, kind, room_info):
        room_list = room_info.get('room_list', [])
        page = room_info.get('page', 1)
        fetch_time = room_info.get('fetch_time', 0)
        from logic.gcommon.time_utility import get_server_time
        from logic.gcommon.common_const.liveshow_const import LIVE_LIST_EXPIRE_TIME, PAGE_REQUEST_CD
        if get_server_time() - fetch_time >= LIVE_LIST_EXPIRE_TIME:
            room_info['fetch_time'] = get_server_time() - LIVE_LIST_EXPIRE_TIME + PAGE_REQUEST_CD
        LivePlatformManager().receive_live_data(kind, page, None, room_list, room_info)
        return

    def request_followed_anchor_list(self, kind):
        self.call_server_method('get_followed_anchor_list', (kind,))

    @rpc_method(CLIENT_STUB, (Bool('succ'), Int('kind'), Dict('anchor_list')))
    def reply_followed_anchor_list(self, succ, kind, anchor_list):
        self.on_reply_followed_anchor_list(succ, kind, anchor_list)

    def on_reply_followed_anchor_list(self, succ, kind, anchor_list):
        LivePlatformManager().set_follow_anchor_list(kind, anchor_list)

    def request_live_param(self, kind):
        self.call_server_method('request_live_param', (kind,))

    @rpc_method(CLIENT_STUB, (Int('kind'), Dict('info')))
    def reply_live_param(self, kind, info):
        LivePlatformManager().receive_live_param(kind, info)
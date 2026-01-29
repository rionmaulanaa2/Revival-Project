# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impChat.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB, filter_method
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from mobile.common.FilterMessageBroker import FilterMessageBroker
from logic.gcommon.common_const import chat_const
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon import time_utility as tutil

class impChat(object):

    def _init_chat_from_dict(self, bdict):
        self._chat_background_item_no = bdict.get('chat_background', 0)
        self._check_chat_country = bdict.get('check_chat_country', False)
        self._check_chat_timerange = bdict.get('check_chat_timerange', None)
        FilterMessageBroker.register('on_msg', self.on_msg)
        FilterMessageBroker.register('on_msgs', self.on_msgs)
        return

    def _destroy_chat(self):
        FilterMessageBroker.unregister('on_msg', self.on_msg)
        FilterMessageBroker.unregister('on_msgs', self.on_msgs)

    def sa_log_forbidden_msg(self, channel, msg, code, rerole_id=0, rerole_lv=0, hint=1, input_type='text'):
        self.call_server_method('client_sa_log', ('Chat',
         {'content': msg,
            'hint': hint,
            'channel': chat_const.CHAT_CHANNEL_NAME.get(channel, channel),
            'chat_time': tutil.get_time(),
            'cid': 0,
            'Shield': False,
            'input_type': input_type,
            'rerole_id': rerole_id,
            'rerole_lv': rerole_lv,
            'sdk_code': code
            }))

    def send_msg(self, channel, msg, voice='', extra=None, code=200):
        extra = {} if extra is None else extra
        self.call_server_method('chat_msg', (int(channel), msg, voice, extra, code))
        return

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def on_chat_msg(self, data):
        global_data.message_data.add_msg(data)

    def on_msgs(self, datas):
        for data in datas:
            self.on_msg(data)

    def on_msg(self, data):
        global_data.message_data.add_msg(data)
        if global_data.player:
            if data.get('is_pigoen', False) and data.get('sender_info', {}).get('uid', 0) == global_data.player.uid:
                global_data.player.notify_client_message((get_text_by_id(11053),))

    @rpc_method(CLIENT_STUB, (Dict('info'), Bool('need_confirm')))
    def forbiden_chat_msg(self, info, need_confirm):
        sec = info.get('sec')
        reason = info.get('reason')
        if sec < 0:
            content = get_text_by_id(130, {'reason': get_text_by_id(reason)})
        else:
            unbantime = info.get('time') + sec - tutil.g_stamp_delta
            content = get_text_by_id(129, {'reason': get_text_by_id(reason),'unbantime': tutil.get_time_string('%Y-%m-%d %H:%M:%S', unbantime)})
        if need_confirm:
            NormalConfirmUI2().init_widget(content=content)
        else:
            global_data.game_mgr.show_tip(content, True)

    @rpc_method(CLIENT_STUB, (Dict('info'), Bool('need_confirm')))
    def forbiden_voice_msg(self, info, need_confirm):
        sec = info.get('sec')
        reason = info.get('reason')
        if sec <= 0:
            return
        import logic.gcommon.const as const
        global_data.ccmini_mgr.logout_session(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.logout_session(const.TEAM_ALL_SESSION_ID)
        global_data.ccmini_mgr.logout_session(const.NEAR_SESSION_ID)
        unbantime_date = tutil.get_time_string('%Y-%m-%d %H:%M:%S', info.get('time') + sec - tutil.g_stamp_delta)
        reason = get_text_by_id(reason)
        content = get_text_by_id(179, {'reason': get_text_by_id(reason),'unbantime': unbantime_date})
        if need_confirm:
            NormalConfirmUI2().init_widget(content=content)
        else:
            global_data.game_mgr.show_tip(content, True)

    @rpc_method(CLIENT_STUB, (Int('channel'), Str('tag'), List('history_msg')))
    def on_history_msg(self, channel, tag, history_msg):
        global_data.message_data.set_history_msg(channel, history_msg)

    def req_set_chat_background(self, background_item_no):
        self.call_server_method('req_set_chat_background', (background_item_no,))

    @rpc_method(CLIENT_STUB, (Int('background_item_no'),))
    def on_set_chat_background(self, background_item_no):
        self._chat_background_item_no = background_item_no
        global_data.emgr.message_on_player_chat_background_item.emit(background_item_no)

    def get_chat_frame_item(self):
        return self._chat_background_item_no

    def req_switch_world_chat_lang(self, lang):
        self.call_server_method('switch_world_chat_lang', (lang,))

    def in_moderation_whitelist(self):
        return not self._check_chat_country

    def in_speech_control(self):
        return self._check_chat_timerange and tutil.check_in_time_range(self._check_chat_timerange, tutil.time())
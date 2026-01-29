# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPlayer.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from logic.gcommon import time_utility as tutil

class impPlayer(object):

    def _init_my_player_from_dict(self, bdict):
        pass

    def req_change_sex(self, new_sex):
        if new_sex == self.sex:
            return False
        if tutil.get_server_time() - self.last_set_sex_time < tutil.ONE_DAY_SECONDS:
            global_data.game_mgr.show_tip(10368)
            return False
        self.call_server_method('req_change_sex', (new_sex,))
        return True

    def req_change_name(self, new_name):
        self.call_server_method('req_change_name', (new_name,))

    def get_custom_service_token(self):
        self.call_server_method('get_custom_service_token', (get_cur_text_lang(),))

    def req_guidance_no_show(self, guidance_id):
        self.call_server_method('req_guidance_no_show', (guidance_id,))

    def set_introduction(self, introduction):
        self.call_server_method('client_set_intro', (introduction,))

    def _on_login_player_success(self):
        self.get_custom_service_token()

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def on_change_data(self, data):
        if 'char_name' in data:
            global_data.emgr.player_on_change_name.emit(data['char_name'])
            global_data.emgr.player_change_name_sucess.emit()
            global_data.player.set_name(data['char_name'])
            global_data.channel.on_user_char_name_changed()
        if 'intro' in data:
            global_data.player.set_intro(data['intro'])
            global_data.emgr.player_on_change_intro.emit(data['intro'])
        if 'sex' in data:
            self.set_sex(data['sex'], data.get('sex_time') or tutil.get_server_time())
            global_data.emgr.player_on_change_sex.emit(data['sex'])
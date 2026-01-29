# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBindMobile.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_utils.local_text import get_text_by_id

class impBindMobile(object):

    def _init_bindmobile_from_dict(self, bdict):
        self.cur_bind_phone = bdict.get('last_pn', None)
        return

    def query_cur_bind(self):
        self.call_server_method('query_cur_bind', ())

    @rpc_method(CLIENT_STUB, (Str('cur_phone_num'),))
    def on_cur_bind(self, cur_phone_num):
        self.cur_bind_phone = cur_phone_num
        ui = global_data.ui_mgr.get_ui('PhoneUnBindUI')
        if ui:
            ui.on_get_cur_phone(cur_phone_num)

    def req_send_sms(self, phone_num):
        self.call_server_method('req_send_sms', (str(phone_num),))

    def req_verify_and_bind(self, phone_num, sms_code):
        self.call_server_method('veryfy_and_bind', (str(phone_num), str(sms_code)))

    @rpc_method(CLIENT_STUB, (Bool('ret'),))
    def on_verify_and_bind_result(self, ret):
        if ret:
            global_data.player.notify_client_message((get_text_by_id(2186),))
            global_data.ui_mgr.close_ui('PhoneBindUI')
            global_data.ui_mgr.show_ui('PhoneUnBindUI', 'logic.comsys.activity')
            from logic.gcommon.common_const.activity_const import ACTIVITY_BIND_MOBILE
            global_data.player.del_activity(ACTIVITY_BIND_MOBILE)

    def req_unbind(self, phone_num):
        self.call_server_method('req_unbind', (str(phone_num),))

    @rpc_method(CLIENT_STUB, (Bool('ret'),))
    def on_unbind_result(self, ret):
        if ret:
            global_data.player.notify_client_message((get_text_by_id(2187),))
            self.cur_bind_phone = None
        return

    def get_cur_bind_phone(self):
        return self.cur_bind_phone

    def set_cur_bind_phone(self, phone):
        self.cur_bind_phone = phone
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBindEmail.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class impBindEmail(object):

    def _init_bindemail_from_dict(self, bdict):
        self.cur_bind_email = bdict.get('last_email', None)
        return

    def query_cur_bind_email(self):
        self.call_server_method('query_cur_bind_email', ())

    @rpc_method(CLIENT_STUB, (Str('cur_bind_email'),))
    def on_cur_bind_email(self, cur_bind_email):
        self.cur_bind_email = cur_bind_email
        ui = global_data.ui_mgr.get_ui('EmailUnBindUI')
        if ui:
            ui.on_get_cur_bind_email(cur_bind_email)

    def req_bind_email(self, email):
        func_json = '{"methodId":"uploadEmail", "email":"%s"}' % email
        global_data.channel.extend_func(func_json)
        self.call_server_method('req_bind_email', (str(email),))
        self.cur_bind_email = email

    def req_unbind_email(self, email):
        self.call_server_method('req_unbind_email', (str(email),))

    def get_cur_bind_email(self):
        return self.cur_bind_email

    def set_cur_bind_email(self, email):
        self.cur_bind_email = email
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBindWechat.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict

class impBindWechat(object):

    def _init_bindwechat_from_dict(self, bdict):
        self._bind_code = None
        self._mini_program_type = bdict.get('mini_program_type', '0')
        if global_data.is_inner_server:
            self._mini_program_type = '2'
        return

    @rpc_method(CLIENT_STUB, (Str('bind_code'),))
    def reply_wechat_bind_code(self, bind_code):
        self._bind_code = bind_code
        global_data.emgr.receive_wechat_bind_code_event.emit(bind_code)

    def get_wechat_bind_code(self):
        return self._bind_code

    def get_mini_program_type(self):
        return self._mini_program_type

    @rpc_method(CLIENT_STUB, (Str('mini_program_type'),))
    def update_mini_program_type(self, mini_program_type):
        self._mini_program_type = mini_program_type
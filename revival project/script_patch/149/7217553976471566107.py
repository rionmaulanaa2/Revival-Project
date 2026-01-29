# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNile.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Dict
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class impNile(object):

    def _init_nile_from_dict(self, bdict):
        self._nile_token = None
        return

    def _destroy_nile(self):
        if global_data.nile_sdk:
            global_data.nile_sdk.logout()

    def get_nile_token(self):
        return self._nile_token

    def nile_request_token(self):
        self.call_server_method('nile_request_token', ())

    @rpc_method(CLIENT_STUB, (Str('token'),))
    def notify_nile_token(self, token):
        self.on_notify_nile_token(token)

    def on_notify_nile_token(self, token):
        self._nile_token = token
        global_data.emgr.on_nile_token_update_event.emit()

    def nile_pay_order(self, order_id, market_id, activity_id, cost_id, goods_id):
        privateparam = {'order_id': order_id,
           'market_id': market_id,
           'activity_id': activity_id,
           'cost_id': cost_id,
           'token': self._nile_token
           }
        self.pay_order(goods_id, privateparam)

    def nile_pay_ret(self, ret, privateparam):
        if global_data.nile_sdk:
            global_data.nile_sdk.on_pay_result(ret, privateparam)

    @rpc_method(CLIENT_STUB, (Str('command'),))
    def nile_command_grant(self, command):
        self._notify_command_grant(command)

    def _notify_command_grant(self, command):
        if global_data.nile_sdk:
            global_data.nile_sdk.ForwardServerCommand(command)
        else:
            log_error('notify_command_grant failed: nile_sdk is not initialized')
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impOnlineState.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict, Bool

class impOnlineState(object):

    def _init_onlinestate_from_dict(self, bdict):
        self._enable_invisible = bdict.get('enable_invisible', False)
        self._invisible_times_week_limit = bdict.get('invisible_times_week_limit', 5)

    @rpc_method(CLIENT_STUB, (Int('new_times'),))
    def on_invisible_times_change(self, new_times):
        self._invisible_times_week_limit = new_times
        global_data.emgr.invisible_times_change_event.emit(new_times)

    @rpc_method(CLIENT_STUB, (Bool('enable'), Bool('ret')))
    def on_set_enable_invisible(self, enable, ret):
        self._enable_invisible = enable
        if not ret:
            global_data.emgr.invisibel_state_change_event.emit(enable)

    def set_enable_invisible(self, enable):
        self.call_server_method('set_enable_invisible', (enable,))

    def is_invisible(self):
        return self._enable_invisible

    def get_left_invisible_times(self):
        return self._invisible_times_week_limit
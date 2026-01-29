# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impYuanbaoStrike.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict, Float

class impYuanbaoStrike(object):

    def _init_yuanbaostrike_from_dict(self, bdict):
        self._yuanbao_strike_times = bdict.get('yuanbao_strike_times', 1.0)
        self._loop_yuanbao_strike_times = bdict.get('loop_yuanbao_strike_times', 1.0)

    def get_yuanbao_strike_times(self):
        return self._yuanbao_strike_times

    def get_loop_yuanbao_strike_times(self):
        return self._loop_yuanbao_strike_times

    @rpc_method(CLIENT_STUB, (Float('new_times'), Float('change')))
    def on_yuanbao_strike_times_change(self, new_times, change):
        self._yuanbao_strike_times = new_times
        global_data.emgr.yuanbao_strike_times_change.emit(change)

    @rpc_method(CLIENT_STUB, (Float('new_times'), Float('change')))
    def on_loop_yuanbao_strike_times_change(self, new_times, change):
        self._loop_yuanbao_strike_times = new_times
        global_data.emgr.yuanbao_strike_times_change.emit(change)
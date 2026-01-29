# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impIMT.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gcommon import time_utility
import math

class impIMT(object):

    def _init_imt_from_dict(self, bdict):
        self._imt_punisht_time = bdict.get('imt_punish_time', 0)

    @rpc_method(CLIENT_STUB, (Int('imt_punish_time'),))
    def update_imt_info(self, imt_punish_time):
        self._imt_punisht_time = imt_punish_time
        global_data.emgr.update_allow_match_ts.emit()

    def get_imt_punish_left_time(self):
        return max(int(math.ceil(self._imt_punisht_time - time_utility.time())), 0)
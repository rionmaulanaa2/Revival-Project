# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAFK.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int
from logic.gcommon import time_utility
import math

class impAFK(object):

    def _init_afk_from_dict(self, bdict):
        self._afk_punisht_time = bdict.get('afk_punish_time', 0)

    @rpc_method(CLIENT_STUB, (Int('afk_punish_time'),))
    def update_afk_info(self, afk_punish_time):
        self._afk_punisht_time = afk_punish_time
        global_data.emgr.update_allow_match_ts.emit()

    def get_afk_punish_left_time(self):
        return max(int(math.ceil(self._afk_punisht_time - time_utility.time())), 0)

    def show_afk_confirmUI(self):
        pass
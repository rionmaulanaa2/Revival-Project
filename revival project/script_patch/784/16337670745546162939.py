# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAchievement.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, Dict, Int
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class impAchievement(object):

    def _init_achievement_from_dict(self, bdict):
        pass

    @rpc_method(CLIENT_STUB, (Int('achieve_id'),))
    def add_achieve(self, achieve_id):
        pass

    @rpc_method(CLIENT_STUB, (Int('achieve_id'),))
    def del_achieve(self, achieve_id):
        pass
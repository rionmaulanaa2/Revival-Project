# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impHomeland.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Dict, Str
from logic.gutils import homeland_utils as hm_utils
import json

class impHomeland(object):

    def _init_homeland_from_dict(self, bdict):
        pass

    @rpc_method(CLIENT_STUB, (Str('ret'),))
    def homeland_req_response(self, ret):
        hm_utils.homeland_callback(json.loads(ret), None)
        return
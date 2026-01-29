# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impVerifyCode.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from common.cfg import confmgr
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.common_const import activity_const as acconst
from logic.gutils import task_utils

class impVerifyCode(object):

    def _init_verifycode_from_dict(self, bdict):
        self.verify_code = bdict.get('verify_code', None)
        return

    def get_verifycode(self):
        return self.verify_code
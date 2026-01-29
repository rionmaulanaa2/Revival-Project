# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impFestival.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Dict, List, Str, Bool
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon import time_utility as tutil
import math

class impFestival(object):

    def _init_festival_from_dict(self, bdict):
        self.goods_deduction_info = bdict.get('goods_deduction_info', {'201800637': 0})

    @rpc_method(CLIENT_STUB, (Str('goods_id'), Int('deduction')))
    def update_goods_deduction_info(self, goods_id, deduction):
        self.goods_deduction_info[goods_id] = deduction
        global_data.emgr.update_festival_goods_deduction_info_event.emit()

    def get_festival_goods_deduction_info(self):
        return self.goods_deduction_info
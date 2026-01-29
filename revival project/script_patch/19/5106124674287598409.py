# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impGlobalLottery.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Dict, List, Str, Bool
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon import time_utility as tutil
import math
from logic.gutils import delay
import random

class impGlobalLottery(object):

    def _init_globallottery_from_dict(self, bdict):
        self.global_lottery_record = bdict.get('global_lottery_record', {})

    def attend_global_lottery(self, lottery_key):
        lottery_record = self.global_lottery_record.setdefault(lottery_key, {})
        if lottery_record.get('has_attend', False):
            return
        lottery_record['has_attend'] = True
        delay.call(random.random() * 5 + 0.1, lambda : self.call_server_method('attend_global_lottery', (lottery_key,)))

    def has_attend_global_lottery(self, lottery_key):
        return self.global_lottery_record.get(lottery_key, {}).get('has_attend', False)
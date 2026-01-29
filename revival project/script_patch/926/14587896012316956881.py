# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMultiRank.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.RpcMethodArgs import Str, Int, List, Dict, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_const import rank_const
from logic.gcommon import time_utility as tutil

class impMultiRank(object):

    def _init_multirank_from_dict(self, bdict):
        self.my_rank_mecha_data = {}

    def request_my_multi_rank_service_data(self, rank_type, unique_key):
        self.call_server_method('get_multi_rank_service_data', (rank_type, unique_key))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Str('unique_key'), List('rank_data')))
    def get_multi_rank_service_data_result(self, rank_type, unique_key, rank_data):
        self.my_rank_mecha_data[rank_type] = rank_data
        self.my_rank_mecha_data.setdefault(rank_type, {})
        self.my_rank_mecha_data[rank_type][unique_key] = rank_data
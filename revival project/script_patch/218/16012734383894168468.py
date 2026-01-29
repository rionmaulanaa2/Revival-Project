# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impDuelStat.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int

class impDuelStat(object):

    def _init_duelstat_from_dict(self, bdict):
        self._duel_win_cnt = bdict.get('duel_win_cnt', 0)

    def get_duel_win_cnt(self):
        return self._duel_win_cnt

    @rpc_method(CLIENT_STUB, (Int('win_cnt'),))
    def update_duel_win_cnt(self, win_cnt):
        self._duel_win_cnt = win_cnt
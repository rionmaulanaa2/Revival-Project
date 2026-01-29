# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impShare.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool

class impShare(object):

    def _init_share_from_dict(self, bdict):
        self._today_shared = bdict.get('today_shared', False)

    def _on_share_mention_per_day_0(self):
        if self._today_shared:
            self._today_shared = False

    def share(self):
        self.call_server_method('share_succ', ())

    def share_activity(self, share_type):
        self.call_server_method('share_activity_succ', (share_type,))

    @rpc_method(CLIENT_STUB, (Bool('ret'),))
    def share_ret(self, ret):
        if ret:
            if not self._today_shared:
                self._today_shared = True
                global_data.emgr.player_first_success_share_event.emit()

    def is_today_shared(self):
        return self._today_shared

    def join_social_group(self):
        self.call_server_method('join_social_group', ())
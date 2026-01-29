# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFogFieldSynchronizer.py
from __future__ import absolute_import
from .ComClientSynchronizer import ComClientSynchronizer

class ComFogFieldSynchronizer(ComClientSynchronizer):

    def enable(self, enable):
        if self._enable_sync == enable:
            return
        self._enable_sync = enable
        self.reset()

    def call_sync_method(self, method_name, parameters, immediate=False, include_self=False, broadcast=True, exclude=(), merge=None):
        if self._enable_sync:
            return super(ComFogFieldSynchronizer, self).call_sync_method(method_name, parameters, immediate=immediate, include_self=include_self, broadcast=broadcast, exclude=exclude, merge=merge)

    def call_sync_method_misty(self, method_name, parameters):
        if self._enable_sync:
            return super(ComFogFieldSynchronizer, self).call_sync_method(method_name, parameters)
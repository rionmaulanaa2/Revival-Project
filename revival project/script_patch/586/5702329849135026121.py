# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/uds_sdk/PerfSdkWrapper.py
from __future__ import absolute_import
from common.framework import Singleton
from .RMSdk import RMSdk

def dummyfunc(*args, **kwargs):
    pass


class PerfSdkWrapper(Singleton):
    ALIAS_NAME = 'perf_sdk'
    SDK_LIST = [
     RMSdk]

    def init(self):
        self._agent = None
        for sdk in self.SDK_LIST:
            inst = sdk()
            if inst.setup():
                self._agent = inst
                break

        return

    def __getattr__(self, key):
        if hasattr(self._agent, key):
            self.__dict__[key] = getattr(self._agent, key)
        else:
            self.__dict__[key] = dummyfunc
        return self.__dict__[key]
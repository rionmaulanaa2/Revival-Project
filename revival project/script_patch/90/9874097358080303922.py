# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/wanfa/sub_wanfa/WanfaBase.py
from __future__ import absolute_import
from common.framework import Singleton

class WanfaBase(Singleton):

    def init(self):
        super(WanfaBase, self).init()
        self.on_init_wanfa()

    def on_init_wanfa(self):
        raise NotImplementedError

    def on_destroy_wanfa(self):
        raise NotImplementedError

    def destroy(self):
        self.on_destroy_wanfa()
        self.__class__.finalize()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_mobile_server.py
__author__ = 'lxn3032'
import Timer
from safaia_base import SafaiaBase

class SafaiaMobileServer(SafaiaBase):

    def __init__(self):
        super(SafaiaMobileServer, self).__init__()
        self._timer = None
        return

    def get_engine_name(self):
        return 'mobile server'

    def register_update(self, update_func):
        self._timer = Timer.addRepeatTimer(0.05, update_func)

    def unregister_update(self):
        self._timer.cancel()
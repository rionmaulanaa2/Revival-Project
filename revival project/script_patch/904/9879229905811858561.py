# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_bigworld.py
import BigWorld
from safaia_base import SafaiaBase

class SafaiaBigWorld(SafaiaBase):

    class GlobalTimerObj(BigWorld.Entity):

        def __init__(self):
            super(SafaiaBigWorld.GlobalTimerObj, self).__init__()
            self.timer_callback = None
            self.running = False
            return

        def add_timer_callback(self, func):
            self.timer_callback = func
            self.running = True

        def onTimer(self, timerId, userData):
            if self.timer_callback:
                self.timer_callback()
                if not self.running:
                    self.delTimer(timerId)

    def __init__(self):
        super(SafaiaBigWorld, self).__init__()
        self.timer = self.GlobalTimerObj()

    def get_engine_name(self):
        return 'bigworld'

    def register_update(self, update_func):
        self.timer.add_timer_callback(update_func)
        self.timer.addTimer(0, 0.04)

    def unregister_update(self):
        self.timer.running = False
        self.timer.timer_callback = None
        return

    def get_uid(self):
        return None

    def get_platform(self):
        return 'windows'
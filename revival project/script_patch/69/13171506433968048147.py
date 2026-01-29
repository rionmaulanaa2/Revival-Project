# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSceneTrigger.py
from __future__ import absolute_import
from . import ScenePart
import math3d
import time
from common.utils.timer import CLOCK
UPDATE_INTERVAL = 0.33

class PartSceneTrigger(ScenePart.ScenePart):
    ENTER_EVENT = {'net_reconnect_event': 'on_reconnect',
       'net_login_reconnect_event': 'on_reconnect'
       }

    def __init__(self, scene, name):
        super(PartSceneTrigger, self).__init__(scene, name)
        self._timer = None
        return

    def on_update(self):
        self.scene().set_trigger_position(self.scene().active_camera.world_position)

    def on_enter(self):
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.on_update, interval=UPDATE_INTERVAL, mode=CLOCK, strict=False)

    def on_exit(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return

    def on_reconnect(self, *args):
        if not self._timer:
            return
        self.on_exit()
        self.on_enter()
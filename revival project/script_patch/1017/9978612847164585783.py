# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncEulerSender.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
import math3d
import world
from logic.gutils.sync.TriggerBox import TriggerBox, euler_func_dt

class ComMoveSyncEulerSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_EULER': '_on_sync_euler',
       'E_ACTION_SYNC_CLEAR_EULER': '_on_action_sync_clear_euler'
       }

    def __init__(self):
        super(ComMoveSyncEulerSender, self).__init__(need_update=True)
        self._trigger = TriggerBox(min_itvl=0.1, min_delta=0.1, max_stay=0.5, func_dt=euler_func_dt)
        self._trigger.set_callback(self.on_tri_euler)

    def destroy(self):
        self._trigger.destroy()
        super(ComMoveSyncEulerSender, self).destroy()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncEulerSender, self).init_from_dict(unit_obj, bdict)

    def _on_sync_euler(self, yaw, pitch, roll):
        t = t_util.time()
        data = (yaw, pitch, roll)
        self._trigger.input(t, data)

    def on_tri_euler(self, t, euler3):
        self.send_event('E_CALL_SYNC_METHOD', 'on_sync_euler3', (euler3[0], euler3[1], euler3[2]), True, False)

    def tick(self, dt):
        now = global_data.game_time_wrapped
        self._trigger.check_trigger(now)

    def _on_action_sync_clear_euler(self):
        self._trigger.clear()
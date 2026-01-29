# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveSyncRotSender.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import time_utility as t_util
from ...time_utility import time
import math3d
import world
from logic.gutils.sync.TriggerRot import TriggerRot
from logic.gcommon.common_utils.math3d_utils import normal_v3d_to_tp as v3d_to_tp
V3D_ZERO = math3d.vector(0, 0, 0)

class ComMoveSyncRotSender(UnitCom):
    BIND_EVENT = {'E_ACTION_SYNC_CLEAR_EULER': '_on_action_sync_clear_euler'
       }

    def __init__(self):
        super(ComMoveSyncRotSender, self).__init__(need_update=True)
        self._tg_pos_rot = TriggerRot()
        self._tg_pos_rot.set_callback('agl', self._on_agl_tri)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveSyncRotSender, self).init_from_dict(unit_obj, bdict)

    def on_tri_euler(self, t, euler3):
        self.send_event('E_CALL_SYNC_METHOD', 'on_sync_euler3', (euler3[0], euler3[1], euler3[2]), True, False)

    def _on_agl_tri(self, t, agl_v3d, agl_vel, agl_acc):
        factor = 1
        agl_v3d = v3d_to_tp(agl_v3d * factor)
        agl_vel = v3d_to_tp(agl_vel * factor)
        agl_acc = v3d_to_tp(agl_acc * factor)
        self.send_event('E_CALL_SYNC_METHOD', 'sync_agl', (t, agl_v3d, agl_vel, agl_acc), True)

    def tick(self, dt):
        if not self.unit_obj:
            return
        self._on_pos_rot()
        self._tg_pos_rot.tick(dt)

    def _on_pos_rot(self):
        mat = self.ev_g_rot_matrix()
        agl_spd = self.ev_g_agl_spd()
        if not mat or not agl_spd:
            return
        now = time()
        agl = math3d.rotation_to_euler(math3d.matrix_to_rotation(mat))
        self._tg_pos_rot.input_agl(now, agl, agl_spd, V3D_ZERO)

    def _on_action_sync_clear_euler(self):
        self._trigger.clear()
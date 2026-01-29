# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/camera_controller/lobby_circle_cam_ctrl.py
from __future__ import absolute_import
import math3d
from logic.vscene.parts.camera.camera_controller.lobby_cam_ctrl import LobbyCamCtrl

class LobbyCircleCamCtrl(LobbyCamCtrl):

    def init(self):
        super(LobbyCircleCamCtrl, self).init()
        self._trans_lock_time = -1.0
        self.target_pos = None
        return

    def set_target_pos(self, target_pos):
        self.target_pos = math3d.vector(*target_pos)
        if self.target_pos and not self._has_started:
            self.set_started(True)

    def on_update(self, dt, yaw, pitch):
        if not self.target_pos:
            return
        self.on_update_by_pos(dt, self.target_pos, yaw, pitch)

    def on_update_by_trigger(self, dt, yaw, pitch):
        if not self.target_pos:
            return
        self.on_update_by_pos(dt, self.target_pos, yaw, pitch)

    def on_pause(self, flag):
        pass
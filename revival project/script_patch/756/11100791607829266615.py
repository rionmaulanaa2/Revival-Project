# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLuckyHouseCamera.py
from __future__ import absolute_import
from . import ScenePart
from logic.vscene.parts.camera.camera_controller import lucky_house_cam_ctrl

class PartLuckyHouseCamera(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartLuckyHouseCamera, self).__init__(scene, name, True)
        self._yaw = 0
        self._pitch = 0
        self.camera_ctrl = None
        self.init_camera_ctrl()
        return

    def init_camera_ctrl(self):
        self.camera_ctrl = lucky_house_cam_ctrl.LuckyHouseCamCtrl()

    def on_enter(self):
        pass

    def on_exit(self):
        self.camera_ctrl = None
        return

    def on_pause(self, flag):
        if self.camera_ctrl:
            self.camera_ctrl.on_pause(flag)

    def on_update(self, dt):
        if self.camera_ctrl:
            self.camera_ctrl.on_update(dt, self._yaw, self._pitch)
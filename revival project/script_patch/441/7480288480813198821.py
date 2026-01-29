# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLoginFov.py
from __future__ import absolute_import
from . import ScenePart
import game3d
import math
MAX_ASPECT = 16.0 / 9.0
DEFAULT_FOV = 45
BIAS = 1.2

class PartLoginFov(ScenePart.ScenePart):
    INIT_EVENT = {'resolution_changed': 'on_resolution_changed'
       }

    def __init__(self, scene, name):
        super(PartLoginFov, self).__init__(scene, name)

    def on_resolution_changed(self):
        self.change_cam_config()

    def change_cam_fov_aspect(self):
        scn = self.scene()
        fov = DEFAULT_FOV
        w, h, _, _, _ = game3d.get_window_size()
        current_aspect = w * 1.0 / h
        if current_aspect > MAX_ASPECT:
            current_tan = math.tan(math.radians(DEFAULT_FOV)) * MAX_ASPECT / current_aspect
            ret = math.atan(current_tan)
            fov = math.degrees(ret) - BIAS
        scn.active_camera.fov = fov
        scn.active_camera.aspect = current_aspect

    def change_cam_config(self):
        self.change_cam_fov_aspect()
        scn = self.scene()
        scn.active_camera.transformation = scn.get_preset_camera('cm')

    def on_pre_load(self):
        self.change_cam_config()
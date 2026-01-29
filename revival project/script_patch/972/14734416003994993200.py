# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/ModelThumbRenderer.py
import math
from functools import partial
import game3d
from neox import nxcore, math3d
import world
from .AssetThumbRenderer import AssetThumbRenderer

class ModelThumbRenderer(AssetThumbRenderer):
    CAMERA_DIRECTION = (0, 0, -1)

    def __init__(self):
        super(ModelThumbRenderer, self).__init__()
        from . import TemplateScene, TemplateMaterial
        if TemplateScene:
            self.scene.load(TemplateScene, None, True)
        self.scene.background_color = 4283256141L
        self._camera.near_plane = 0.1
        self._camera.far_plane = 1000
        self._model = None
        return

    def set_up(self, file_path):
        yield True

    def set_up_async(self, file_path):
        self._model = world.model(file_path, self.scene)
        size = self._model.bounding_radius_w
        center = self._model.center_w
        self.ensure_camera_covered(center, size)
        yield nxcore.YieldReturn(True)

    def ensure_camera_covered(self, center, size):
        fov = min(self._camera.fov, self._camera.fov_x)
        distance = size / math.sin(math.radians(fov / 2)) * 1.1
        direction = math3d.Vector3(*self.CAMERA_DIRECTION)
        direction.normalize()
        position = center + direction * distance
        self._camera.position = position

    def clear_up(self):
        if not self._model:
            return
        else:
            self._model.visible = False

            def delayed(model):
                self.scene.remove_object(model)
                model.destroy()

            game3d.delay_exec(0, partial(delayed, self._model))
            self._model = None
            return
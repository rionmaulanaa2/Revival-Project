# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/EffectThumbRenderer.py
import time
import world
import math3d
from neox import nxcore, world2
from neox.world2 import NMaterial
from .DynamicAssetThumbRenderer import DynamicAssetThumbRenderer

class EffectThumbRenderer(DynamicAssetThumbRenderer):

    def __init__(self):
        super(EffectThumbRenderer, self).__init__()
        from . import TemplateScene
        if TemplateScene:
            self.scene.load(TemplateScene, None, True)
        self.scene.background_color = 4283256141L
        self._camera.position = math3d.Vector3(0, 0, -100)
        self._camera.near_plane = 0.1
        self._camera.far_plane = 1000
        self._effect = None
        self._count = 0
        return

    def set_up(self, file_path):
        self._effect = effect = world.particlesystem(file_path)
        self.scene.add_object(effect)
        effect.restart()
        yield True

    def set_up_async(self, file_path):
        self._effect = effect = world.particlesystem(file_path)
        self.scene.add_object(effect)
        effect.restart()
        self._count = 0
        yield nxcore.YieldReturn(True)

    def clear_up(self):
        if self._effect is None:
            return
        else:
            self._effect.destroy()
            self._effect = None
            return

    def tick(self):
        self._count += 1
        return self._count <= 60
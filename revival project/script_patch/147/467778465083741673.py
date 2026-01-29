# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/DynamicAssetThumbRenderer.py
import time
import math
from neox import world, world2, math3d, nxcore
from neox.nxgui import TextureUtility
from .AssetThumbRenderer import AssetThumbRenderer

class DynamicAssetThumbRenderer(AssetThumbRenderer):

    def _render_to_target_coro(self):
        while self._async_setup_queue:
            async_setup_generator, callback, context = self._async_setup_queue.pop(0)
            if async_setup_generator:
                yield nxcore.WaitForUpdate()
                self.scene.update()
                success = yield async_setup_generator
                if success:
                    yield
                    yield nxcore.WaitForRender()
                    self.scene.render(TextureUtility.get_rt_id(self.render_target))
                    complie_end_time = 20 + time.time()
                    while self.scene.has_shader_uncompiled():
                        yield
                        yield nxcore.WaitForRender()
                        self.scene.render(TextureUtility.get_rt_id(self.render_target))
                        if complie_end_time < time.time():
                            complie_end_time = -1
                            break

                    if complie_end_time < 0:
                        continue
                    while True:
                        yield nxcore.WaitForUpdate()
                        finished = not self.tick()
                        self.scene.update()
                        yield nxcore.WaitForRender()
                        self.scene.render(TextureUtility.get_rt_id(self.render_target))
                        callback and callback(self.render_target, self.get_info(), finished)
                        if finished or context.get('canceled'):
                            break

                    self.clear_up()

    def tick(self):
        return False
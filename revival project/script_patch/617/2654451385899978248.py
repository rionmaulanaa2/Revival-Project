# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/AssetThumbRenderer.py
import time
import math
from neox import world, world2, math3d, nxcore
from neox.nxgui import TextureUtility
_THUMB_PREVIEW_SIZE = 256

class AssetThumbRenderer(object):
    _instance = None
    NEED_FORCE_UPDATE = False

    def __init__(self):
        scene = world.scene()
        scene.background_color = 0
        self._scene = scene
        self._scene.name = type(self).__name__
        e = scene.active_section.create_entity('MainCamera')
        self._camera = e.require_component(world2.LegacyCamera)
        self._camera.position = math3d.Vector3(0, 0, -1000)
        self._camera.near_plane = 1
        self._camera.far_plane = 10000
        self._scene.active_camera = self._camera.spaceobject
        self._render_target = TextureUtility.create_render_target(_THUMB_PREVIEW_SIZE, _THUMB_PREVIEW_SIZE)
        self._coroutine_mgr = e.require_component(nxcore.ScriptComponent)
        self._async_setup_queue = []
        self._async_setup_coro = None
        return

    def get_info(self):
        return None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @property
    def render_target(self):
        return self._render_target

    @property
    def camera(self):
        return self._camera

    @property
    def scene(self):
        return self._scene

    @property
    def queue_length(self):
        if self._async_setup_coro and self._async_setup_coro.is_alive():
            return len(self._async_setup_queue) + 1
        return 0

    def set_up(self, file_path):
        yield True

    def set_up_async(self, file_path):
        yield nxcore.YieldReturn(False)

    def clear_up(self):
        pass

    def get_render_target_async(self, file_path, callback):
        async_setup_generator = self.set_up_async(file_path)
        self._async_setup_queue.append((async_setup_generator, callback, {}))
        if not self._async_setup_coro or not self._async_setup_coro.is_alive():
            self._async_setup_coro = self._coroutine_mgr.start_coroutine(self._render_to_target_coro())
        self._cur_file_path = file_path
        return async_setup_generator

    def cancel_get_render_target_async(self, generator):
        for _, _, context in self._async_setup_queue:
            context['canceled'] = True

        for idx, (_generator, _, _) in enumerate(self._async_setup_queue):
            if _generator == generator:
                self._async_setup_queue.pop(idx)
                break

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
                    yield nxcore.WaitForUpdate()
                    self.scene.update()
                    yield nxcore.WaitForRender()
                    self.scene.render(TextureUtility.get_rt_id(self.render_target))
                    callback and callback(self.render_target, self.get_info(), True)
                    self.clear_up()

    def destroy(self):
        self._scene.destroy()
        self._scene = None
        self._render_target = None
        return

    def zoom_to_bounding_box(self, entity, comp):
        min_p = math3d.Vector3(1e+38, 1e+38, 1e+38)
        max_p = math3d.Vector3(-1e+38, -1e+38, -1e+38)
        matrix = entity.matrix
        bounds = comp.calculate_bounding_box(matrix)
        if bounds:
            min_p = math3d.vector3_min(min_p, bounds.min)
            max_p = math3d.vector3_max(max_p, bounds.max)
        else:
            pos = matrix.translation
            min_p = math3d.vector3_min(min_p, pos)
            max_p = math3d.vector3_max(max_p, pos)
        center = (max_p + min_p) * 0.5
        radius = math3d.vector3_length(max_p - center)
        self.zoom_to(center, radius)

    def zoom_to(self, pos, raidus=0.0, rotate=None, anim=True):
        _distance = 10
        if raidus > 0.01:
            t = math.tan(math3d.radians(self._camera.fov * 0.5))
            _distance = raidus / t
        direction = math3d.vector3_rotate(math3d.Vector3(0, 0, -1), self.camera.world_rotation)
        self.camera.position = pos + direction * _distance
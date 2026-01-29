# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/MeshThumbRenderer.py
from neox import nxcore, world2
from neox.world2 import NMaterial
from .AssetThumbRenderer import AssetThumbRenderer

class MeshThumbRenderer(AssetThumbRenderer):

    def __init__(self):
        super(MeshThumbRenderer, self).__init__()
        from . import TemplateScene, TemplateMaterial
        if TemplateScene:
            self.scene.load(TemplateScene, None, True)
        self.scene.background_color = 4283256141L
        self._camera.near_plane = 0.1
        self._camera.far_plane = 1000
        self._mat = NMaterial.load(TemplateMaterial or 'builtin/world2/standard.nmaterial')
        self.e = self.scene.active_section.create_entity('Mesh')
        self.mesh_renderer = self.e.add_component(world2.NMeshRenderer)
        return

    def set_up(self, file_path):
        mesh = world2.Mesh.load(file_path)
        self.mesh_renderer.mesh = mesh
        self.mesh_renderer.material_count = mesh.material_count
        for i in range(0, mesh.material_count):
            self.mesh_renderer.set_material(i, self._mat)

        self.zoom_to_bounding_box(self.e, self.mesh_renderer)
        yield True

    def set_up_async(self, file_path):
        wait_load_res = nxcore.YieldCallback()
        world2.Mesh.load_async(file_path).callback(wait_load_res)
        mesh, = yield wait_load_res
        if mesh:
            self.mesh_renderer.mesh = mesh
            self.mesh_renderer.material_count = mesh.material_count
            for i in range(0, mesh.material_count):
                self.mesh_renderer.set_material(i, self._mat)

            self.zoom_to_bounding_box(self.e, self.mesh_renderer)
            yield nxcore.YieldReturn(True)
        else:
            yield nxcore.YieldReturn(False)
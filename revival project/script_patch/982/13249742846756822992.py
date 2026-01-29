# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/DynamicMaterialThumbRenderer.py
import math
import math3d
from neox import nxgui, world2
from .DynamicAssetThumbRenderer import DynamicAssetThumbRenderer

class DynamicMaterialThumbRenderer(DynamicAssetThumbRenderer):

    def __init__(self):
        super(DynamicMaterialThumbRenderer, self).__init__()
        from . import TemplateScene
        if TemplateScene:
            self.scene.load(TemplateScene, None, True)
        self.scene.background_color = 4283256141
        canvas_e = self.scene.active_section.create_entity('Canvas')
        _canvas = canvas_e.require_component(nxgui.UICanvas)
        _canvas.set_canvas_size(512, 512)
        _canvas.overlay_mode = True
        _canvas.constraint_distance = 100
        self._canvas = _canvas
        self.camera.position = math3d.Vector3(0, 0, -200)
        e = canvas_e.create_child('Mesh')
        t = e.require_component(nxgui.UITransform)
        t.size_delta = math3d.Vector2(512, 512)
        mesh_comp = e.add_component(nxgui.UIMesh)
        from . import TemplateMesh
        if TemplateMesh:
            mesh_comp.mesh = world2.Mesh.load(TemplateMesh)
        mesh_comp.transform.local_scale = math3d.Vector3(13, 13, 13)
        mesh_comp.material_count = 1
        mesh_comp.use_light_probe = True
        mesh_comp.use_reflection_probe = True
        self.mesh_comp = mesh_comp
        return

    @property
    def canvas(self):
        return self._canvas

    def set_up(self, file_path):
        mtl = self.mesh_comp.get_material(0)
        mtl.load_material_template(file_path)
        yield True

    def set_up_async(self, file_path):
        import sys
        sys.jack = self.mesh_comp
        from neox import nxcore
        mtl = self.mesh_comp.get_material(0)
        mtl.load_material_template(file_path)
        self.rotation = 0
        self._canvas.transform.local_rotation = math3d.rotation(0, 0, 0, 1)
        yield
        yield nxcore.YieldReturn(True)

    def tick(self):
        self._canvas.transform.local_rotation = math3d.rotation(0, math.sin(self.rotation), 0, math.cos(self.rotation))
        self.rotation += math.pi / 60
        return self.rotation < math.pi * 2
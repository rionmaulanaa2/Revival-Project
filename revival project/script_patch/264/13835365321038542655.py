# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/Renderers/ImageThumbRenderer.py
import math
import math3d
from neox import nxgui
from neox.nxgui import Sprite, TextureUtility
from .AssetThumbRenderer import AssetThumbRenderer

class ImageThumbRenderer(AssetThumbRenderer):

    def __init__(self):
        super(ImageThumbRenderer, self).__init__()
        self.camera.fov = 60
        canvas_e = self.scene.active_section.create_entity('Canvas')
        _canvas = canvas_e.require_component(nxgui.UICanvas)
        _canvas.set_canvas_size(512, 512)
        _canvas.overlay_mode = True
        _canvas.constraint_distance = 100
        self._canvas = _canvas
        e = canvas_e.create_child('Image')
        t = e.require_component(nxgui.UITransform)
        t.size_delta = math3d.Vector2(512, 512)
        raw_image = e.add_component(nxgui.UIImage)
        self._image = raw_image
        self._image.image_size_mode = nxgui.ImageSizeMode.Stretch

    def get_info(self):
        return self._image.image_size

    @property
    def canvas(self):
        return self._canvas

    @property
    def imgae(self):
        return self._image

    def set_up(self, file_path):
        self.imgae.texture = TextureUtility.load(file_path)
        width, height = self.imgae.texture.dimension
        self.imgae.transform.size_delta = math3d.Vector2(width, height)
        dis = -max(width, height)
        self.camera.position = math3d.Vector3(0, 0, dis / 2 * math.sqrt(3))
        yield True

    def set_up_async(self, file_path):
        from neox import nxcore
        texture = TextureUtility.load(file_path)
        self.imgae.texture = texture
        width, height = self.imgae.texture.dimension
        self.imgae.transform.size_delta = math3d.Vector2(width, height)
        dis = -max(width, height)
        self.camera.position = math3d.Vector3(0, 0, dis / 2 * math.sqrt(3))
        yield nxcore.YieldReturn(True)

    def clear_up(self):
        pass
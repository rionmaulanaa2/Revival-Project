# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/NeoXThumbnailManager.py
import json
import os
from functools import partial
from neox.nxgui import TextureUtility
import game3d
from .NeoXThumbnailWriter import NeoXThumbnailWriter
from .Renderers.ImageThumbRenderer import ImageThumbRenderer
from .Renderers.MeshThumbRenderer import MeshThumbRenderer
from .Renderers.EffectThumbRenderer import EffectThumbRenderer
from .Renderers.MaterialThumbRenderer import MaterialThumbRenderer
from .Renderers.ModelThumbRenderer import ModelThumbRenderer

class NeoXThumbnailManager(object):
    UNSUPPORTED_TYPES = ('cube', 'mtg')

    def __init__(self, resMgr):
        self._resMgr = resMgr
        self.thumbRoot = os.path.join(game3d.get_root_dir(), 'thumb')
        self._renderers = {'Texture': [
                     ImageThumbRenderer()],
           'Mesh': [
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer(),
                  MeshThumbRenderer()],
           'Model': [
                   ModelThumbRenderer()],
           'Particle': [
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer(),
                      EffectThumbRenderer()],
           'Material': [
                      MaterialThumbRenderer()]
           }
        self._renderer = ImageThumbRenderer()
        self._tasks = {}
        self._thumbnailWriter = NeoXThumbnailWriter(self)

    def getThumbnail(self, resPath, width, height, callback):
        print (
         'GetThumbnail', resPath)
        thumbMetaPath = self.getThumbnailMetaPath(resPath, 256, 256)
        if os.path.exists(thumbMetaPath):
            callback(thumbMetaPath)
            return
        else:
            filePath = self._resMgr.getFilePath(resPath)
            fileExt = self._resMgr.getFileExt(filePath)
            fileType = self._resMgr.getFileGroupType(filePath)
            if fileExt == 'gif':
                self._useDirectFile(resPath, callback)
                return
            task = self._tasks.get((resPath, width, height))
            if task is None:
                if fileExt in self.UNSUPPORTED_TYPES:
                    return
                renderer = self.getRenderer(fileType)
                if renderer is not None:
                    task = ThumbnailGettingTask()
                    task.resPath = resPath
                    task.renderer = renderer
                    task.callbacks.append(callback)
                    task.generator = renderer.get_render_target_async(filePath, partial(self._onRenderEnd, resPath, width, height))
                    self._tasks[resPath, width, height] = task
            else:
                task.callbacks.append(callback)
            return

    def getRenderer(self, fileType):
        renderers = self._renderers.get(fileType)
        if renderers is None:
            return
        else:
            return min(renderers, key=lambda renderer: renderer.queue_length)

    def cancelGettingThumbnail(self):
        for task in self._tasks.values():
            renderer = task.renderer
            generator = task.generator
            renderer.cancel_get_render_target_async(generator)

        self._tasks.clear()

    def invalidateThumbnails(self, resPaths):
        for resPath in resPaths:
            thumbMetaPath = self.getThumbnailMetaPath(resPath, 256, 256)
            if not os.path.exists(thumbMetaPath):
                continue
            with open(thumbMetaPath, 'r') as f:
                data = json.load(f)
            files = data.get('files', [])
            thumbMarshaled = data.get('marshaledThumbs', False)
            os.remove(thumbMetaPath)
            if thumbMarshaled:
                for thumbPath in files:
                    if os.path.exists(thumbPath):
                        os.remove(thumbPath)

    def _onRenderEnd(self, resPath, expectedWidth, expectedHeight, renderTarget, renderInfo, isLastOne):
        task = self._tasks.get((resPath, expectedWidth, expectedHeight))
        if task is None:
            return
        else:
            data = TextureUtility.get_texture_pixel_data(renderTarget)
            task.imageDatas.append(data)
            if not isLastOne:
                return
            if len(task.imageDatas) == 0:
                return
            realWidth, realHeight = (256, 256)
            thumbMetaPath = self.getThumbnailMetaPath(resPath, realWidth, realHeight)
            self._resMgr.ensureDirExists(os.path.dirname(thumbMetaPath))

            def cb(resPath, realWidth, realHeight, expectedWidth, expectedHeight):
                task = self._tasks.pop((resPath, expectedWidth, expectedHeight))
                thumbMetaPath = self.getThumbnailMetaPath(resPath, realWidth, realHeight)
                for callback in task.callbacks:
                    callback(thumbMetaPath)

            self._thumbnailWriter.request(resPath, realWidth, realHeight, task.imageDatas, partial(cb, resPath, realWidth, realHeight, expectedWidth, expectedHeight))
            return

    def _useDirectFile(self, resPath, callback):
        realWidth, realHeight = (256, 256)
        thumbMetaPath = self.getThumbnailMetaPath(resPath, realWidth, realHeight)
        self._resMgr.ensureDirExists(os.path.dirname(thumbMetaPath))
        filePath = self._resMgr.getFilePath(resPath)
        thumbMeta = {'width': realWidth,
           'height': realHeight,
           'format': self._resMgr.getFileExt(resPath),
           'files': [
                   filePath],
           'marshaledThumbs': False
           }
        with open(thumbMetaPath, 'w') as f:
            json.dump(thumbMeta, f, indent=2)
        callback(thumbMetaPath)

    def getThumbnailPath(self, resPath, width, height, index=0, count=1):
        if count == 1:
            return os.path.join(self.thumbRoot, '%ix%i' % (width, height), resPath.replace('\\', '_').replace('/', '_')).replace('\\', '/')
        else:
            return os.path.join(self.thumbRoot, '%ix%i' % (width, height), resPath.replace('\\', '_').replace('/', '_') + '__%i__' % index).replace('\\', '/')

    def getThumbnailMetaPath(self, resPath, width, height):
        return os.path.join(self.thumbRoot, '%ix%i' % (width, height), resPath.replace('\\', '_').replace('/', '_') + '.meta.json').replace('\\', '/')


class ThumbnailGettingTask(object):

    def __init__(self):
        self.resPath = None
        self.callbacks = []
        self.renderer = None
        self.generator = None
        self.imageDatas = []
        return
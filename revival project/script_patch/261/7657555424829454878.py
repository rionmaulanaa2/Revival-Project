# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/NeoXThumbnailWriter.py
import json
import os
import threading
import weakref
from SunshineSDK.PlatformAPI.EditAPI import GetEngineEditAPI
from SunshineSDK.SunshineClient import GetSunshineClient

class NeoXThumbnailWriter(object):

    def __init__(self, thumbManager):
        self.ref_thumbManager = weakref.ref(thumbManager)
        self.finishedCallbacks = []
        self._startLoop()

    def _startLoop(self):
        GetSunshineClient().RegisterUpdateCallback(self.tick)

    @property
    def thumbnailManager(self):
        return self.ref_thumbManager()

    def request(self, resPath, realWidth, realHeight, imageDatas, callback):
        thread = threading.Thread(target=self._work, args=(resPath, realWidth, realHeight, imageDatas, callback))
        thread.start()

    def tick(self):
        if not self.finishedCallbacks:
            return
        for callback in self.finishedCallbacks:
            callback()

        self.finishedCallbacks = []

    def _work(self, resPath, realWidth, realHeight, imageDatas, callback):
        files = []
        for i, data in enumerate(imageDatas):
            thumbPath = self.thumbnailManager.getThumbnailPath(resPath, realWidth, realHeight, i, len(imageDatas))
            with open(thumbPath, 'wb') as f:
                f.write(data)
            files.append(os.path.basename(thumbPath))

        thumbMetaPath = self.thumbnailManager.getThumbnailMetaPath(resPath, realWidth, realHeight)
        thumbMeta = {'width': realWidth,
           'height': realHeight,
           'format': 'ARGB32',
           'files': files,
           'fps': 60,
           'marshaledThumbs': True
           }
        with open(thumbMetaPath, 'w') as f:
            json.dump(thumbMeta, f, indent=2)
        self.finishedCallbacks.append(callback)
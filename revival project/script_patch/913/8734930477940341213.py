# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/NeoXRainbowPluginClient.py
import os
from functools import partial
import game3d
from .Asset.NeoXThumbnailManager import NeoXThumbnailManager
from .Asset.NeoXResourceManager import NeoXResourceManager
from ..RainbowPluginClientBase import *

class RainbowPluginImpl(RainbowPluginClientBase):

    def __init__(self):
        super(RainbowPluginImpl, self).__init__()
        self.resMgr = self.createResourceManager()

    def createResourceManager(self):
        from .Asset import Renderers
        Renderers.TemplateScene = self.getThumbnailScene()
        Renderers.TemplateMesh = self.getThumbnailMesh()
        Renderers.TemplateMaterial = self.getThumbnailMaterial()
        return NeoXResourceManager()

    def GetResourceData(self):
        return self.resMgr.getResourceData()

    def GetThumbnail(self, resPath, width, height):
        self.resMgr.getThumbnail(resPath, width, height, partial(self.onThumbnail, resPath, width, height))

    def CancelGettingThumbnail(self):
        self.resMgr.cancelGettingThumbnail()

    def InvalidateThumbnails(self, resPaths):
        self.resMgr.invalidateThumbnails(resPaths)

    def onThumbnail(self, resPath, width, height, thumbMetaPath):
        print 'On THumbnail'
        self.Server.SetThumbnail(resPath, width, height, thumbMetaPath)

    def getThumbnailScene(self):
        return 'builtin/scene/template.scn'

    def getThumbnailMesh(self):
        return 'builtin/nxgui/sphere.uimesh'

    def getThumbnailMaterial(self):
        return 'builtin/world2/standard.nmaterial'
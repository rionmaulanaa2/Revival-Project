# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/LightningPlugin/LightningPluginClient.py
from ..EditorPlugin import EditorPluginClient
from ...SunshineClient import Response
UUID = '3e9b15f0-0227-11e6-9560-a45e60e3528e'

class LightningPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Lighting'

    def SetCameraMode(self, mode):
        raise NotImplementedError

    def SetCameraSpeed(self, speed):
        raise NotImplementedError

    def GetCameraStepSpeed(self):
        return [
         30, 50, 100]

    def GetWindowInfo(self):
        raise NotImplementedError

    def Register(self):
        methodMap = super(LightningPluginClient, self).Register()
        wrapper = _HandlerWrapper(self)
        methodMap.update({(UUID, 'SetCameraMode'): self.SetCameraMode,
           (UUID, 'SetCameraSpeed'): self.SetCameraSpeed,
           (UUID, 'GetWindowInfo'): self.GetWindowInfo,
           (UUID, 'GetCameraStepSpeed'): wrapper.GetCameraStepSpeed,
           (UUID, 'ReconnectSunshine'): self.ReconnectSunshine
           })
        return methodMap

    def ReconnectSunshine(self, port):
        raise NotImplementedError


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin

    def GetCameraStepSpeed(self):
        speedList = self.plugin.GetCameraStepSpeed()
        return Response(UUID, 'SetCameraStepSpeed', speedList)
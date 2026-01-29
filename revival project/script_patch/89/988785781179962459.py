# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/VideoPlugin/VideoPluginClient.py
from ..EditorPlugin import EditorPluginClient
UUID = '24bd0bac-e646-11e7-8b2b-005056c00008'

class VideoPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Video'

    def RecordDone(self):
        raise NotImplementedError

    def Start(self):
        raise NotImplementedError

    def Stop(self):
        raise NotImplementedError

    def Register(self):
        methodMap = super(VideoPluginClient, self).Register()
        methodMap.update({(UUID, 'RecordDone'): self.RecordDone,
           (UUID, 'Start'): self.Start,
           (UUID, 'Stop'): self.Stop
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin
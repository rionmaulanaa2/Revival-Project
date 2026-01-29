# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/AtmospherePlugin/AtmospherePluginClient.py
from ..EditorPlugin import EditorPluginClient
UUID = 'dfdd1bae-ccd7-11e6-b8b4-14dda9de0dd8'

class AtmospherePluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Atmosphere'

    def OnContextMenuActionCallback(self, callbackKey, *args):
        raise NotImplementedError

    def Register(self):
        methodMap = super(AtmospherePluginClient, self).Register()
        methodMap.update({(UUID, 'OnContextMenuActionCallback'): self.OnContextMenuActionCallback,
           (UUID, 'LoadPlugin'): self.LoadPlugin
           })
        return methodMap

    def LoadPlugin(self, pluginName):
        pass
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/ModelLibPlugin/ModelLibPluginClient.py
from ..EditorPlugin import EditorPluginClient
UUID = 'd671cd00-25ad-406a-9de5-596af90d853f'

class ModelLibPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'ModelLib'

    def GetResourceData(self, resItem):
        raise NotImplementedError

    def Register(self):
        methodMap = super(ModelLibPluginClient, self).Register()
        methodMap.update({(UUID, 'GetResourceData'): self.GetResourceData
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin
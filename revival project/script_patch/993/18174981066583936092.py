# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/GalaxyPlugin/GalaxyPluginServer.py
from ..EditorPlugin import EditorPluginServer
from ...Storyline.StorylineConst import NodeVariableSelectorType
UUID = '98efd553-30b6-4efd-862c-9810e0bdf65a'

class GalaxyPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def PushGraphDebugEvent(self, nodeID, eventName, eventArgs):
        raise NotImplementedError

    def ClearGraphDebugEvents(self):
        raise NotImplementedError

    def SetStorylineMetaData(self, filename, eventGraphName, data):
        raise NotImplementedError

    def GetNodeData(self, nodeID):
        raise NotImplementedError

    def SetModifiedNodeData(self, nodeID, data):
        raise NotImplementedError

    def UpdateNodeDynamicMeta(self, nodeID, dynamicMeta):
        raise NotImplementedError

    def GetDocIDByNodeID(self, nodeID):
        raise NotImplementedError

    def GetAllVariablesByDocID(self, docID):
        raise NotImplementedError

    def SetNodeVariableSelectorData(self, nodeID, portName, varSelectorType=NodeVariableSelectorType.INPUT_PORT, data=None):
        raise NotImplementedError
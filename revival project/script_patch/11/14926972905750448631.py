# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/RainbowPluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = '504492a8-6d6d-47a8-83e1-02f0d1c9fadb'

class RainbowPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def AddEntity(self, key, data, dynamicMeta=None, editComponent=None, addUndoState=False, docId=None):
        raise NotImplementedError

    def ClearEntities(self):
        raise NotImplementedError

    def DelEntity(self, key, permanent=False):
        raise NotImplementedError

    def SetEditEntity(self, key):
        raise NotImplementedError

    def ShowMessageBox(self, msg):
        raise NotImplementedError

    def PreCreateEntityInPosition(self, pos, prefabId=None, docId=None):
        raise NotImplementedError

    def SetEditMode(self, mode):
        raise NotImplementedError

    def SetEntityOpMode(self, mode):
        raise NotImplementedError

    def SetSubEditMode(self, mode):
        raise NotImplementedError

    def SetSubEditModeData(self, data):
        raise NotImplementedError

    def SetStatusMessage(self, msg):
        raise NotImplementedError

    def ClearStatusMessage(self):
        raise NotImplementedError

    def UpdateEditEntityProperty(self, key, propertyName, value):
        raise NotImplementedError

    def SetPointSelectionModePosition(self, pos):
        raise NotImplementedError

    def RegisterTypePropertyAttribute(self, typeName, data):
        raise NotImplementedError

    def ExceptionLog(self, log):
        raise NotImplementedError

    def PreDestroyEntity(self, entityID):
        raise NotImplementedError

    def ClearEditorOutputWindow(self):
        raise NotImplementedError

    def CacheEntities(self, cacheName):
        raise NotImplementedError

    def RestoreCache(self, cacheName):
        raise NotImplementedError

    def RequestEntityData(self, entityID):
        raise NotImplementedError

    def GetDocumentInfo(self):
        raise NotImplementedError
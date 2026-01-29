# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/TeldrassilPlugin/TeldrassilPluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = '2aa5b16a-8063-4c46-a2db-2dcb7ddab15e'

class TeldrassilPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def SetAIName(self, uuid, name):
        raise NotImplementedError

    def PushDebugEvent(self, bid, entity, nodeAlias=None, eventName=None, eventArgs=None):
        raise NotImplementedError

    def AIProfileResult(self, aiName, data):
        raise NotImplementedError

    def PushDebugInfo(self, debugInfo):
        raise NotImplementedError

    def PushBatchDebugInfo(self, debugInfoList):
        raise NotImplementedError

    def ClearDebugEvents(self):
        raise NotImplementedError

    def SetBTInfos(self, btInfos):
        raise NotImplementedError

    def CheckBtCodeCallback(self, info):
        raise NotImplementedError

    def SynchronizeState(self, state):
        raise NotImplementedError
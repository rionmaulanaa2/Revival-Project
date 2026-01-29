# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/TeldrassilPlugin/TeldrassilPluginClient.py
from ..EditorPlugin import EditorPluginClient
UUID = '2aa5b16a-8063-4c46-a2db-2dcb7ddab15e'

class TeldrassilPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Teldrassil'

    def GetAIName(self, uuid, gameInfo=None):
        raise NotImplementedError

    def StartAI(self, uuid, aiName, intervalTime, aiContent):
        raise NotImplementedError

    def StopAI(self, uuid):
        raise NotImplementedError

    def StartAIRecording(self, uuid):
        raise NotImplementedError

    def StopAIRecording(self, uuid):
        raise NotImplementedError

    def HotfixAI(self, uuid, aiFileContent, aiName=None):
        raise NotImplementedError

    def HotfixAIBatch(self, allAIFileContent):
        raise NotImplementedError

    def StartTest(self, aiName):
        raise NotImplementedError

    def GetTestResult(self, aiName):
        raise NotImplementedError

    def CheckTreeSyncState(self, uuid, fileContent):
        return NotImplementedError

    def SetAIBBData(self, uuid, bbData):
        return NotImplementedError

    def GetBTNodeMetas(self):
        raise NotImplementedError

    def Register(self):
        methodMap = super(TeldrassilPluginClient, self).Register()
        wrapper = _HandlerWrapper(self)
        methodMap.update({(UUID, 'GetAIName'): self.GetAIName,
           (UUID, 'StartAI'): self.StartAI,
           (UUID, 'StopAI'): self.StopAI,
           (UUID, 'StartAIRecording'): wrapper.StartAIRecording,
           (UUID, 'StopAIRecording'): self.StopAIRecording,
           (UUID, 'HotfixAI'): self.HotfixAI,
           (UUID, 'HotfixAIBatch'): self.HotfixAIBatch,
           (UUID, 'StartTest'): self.StartTest,
           (UUID, 'GetTestResult'): self.GetTestResult,
           (UUID, 'CheckTreeSyncState'): self.CheckTreeSyncState,
           (UUID, 'SetAIBBData'): self.SetAIBBData,
           (UUID, 'GetBTNodeMetas'): self.GetBTNodeMetas
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin

    def StartAIRecording(self, uuid):
        try:
            checkRet = self.plugin.CheckTreeSyncState(uuid)
        except Exception as e:
            checkRet = True

        if not checkRet:
            info = {'WARNNING': '\xe6\xb8\xb8\xe6\x88\x8f\xe5\x86\x85\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91\xe3\x80\x81\xe6\x9c\xac\xe5\x9c\xb0\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4\xef\xbc\x81','MESSAGE_BOX': '\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91\xe4\xb8\xa4\xe8\xbe\xb9\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4\xef\xbc\x8c\xe5\x8f\xaf\xe8\x83\xbd\xe5\x8e\x9f\xe5\x9b\xa0\xef\xbc\x9a\n1\xe3\x80\x81\xe6\x9c\xac\xe5\x9c\xb0\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\xaa\xe6\x9b\xb4\xe6\x96\xb0;\n2\xe3\x80\x81\xe7\x83\xad\xe6\x9b\xb4\xe5\xa4\xb1\xe8\xb4\xa5'
               }
            self.plugin.GetServer().showOutputInfo(info)
        else:
            self.plugin.StartAIRecording(uuid)
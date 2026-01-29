# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Plugins/GalaxyPlugin.py
from __future__ import absolute_import
from sunshine.SunshineSDK.Plugin.GalaxyPlugin import GalaxyPluginClient
from sunshine.SunshineSDK.Storyline import NodeManager, StorylineSystem
import MontageSDK
from .. import Storyline
from ..Storyline import EnumMetaDefines

class GalaxyPlugin(GalaxyPluginClient):

    def __init__(self):
        super(GalaxyPlugin, self).__init__()
        self.runningStoryline = None
        return

    def GetSimulationTypes(self):
        pass

    def SetSimulationType(self, sType):
        pass

    def StartSimulation(self, simulationFile, searchPath):
        from sunshine.SunshineSDK.Storyline import StorylineSystem
        from ..Storyline.StorylineContext import StorylineContext
        StorylineSystem.GetRepositoryMgr().Update()
        context = StorylineContext()
        context.SetDebugMode(True)
        self.runningStoryline = storyline = StorylineSystem.CreateStoryline(context)
        storyline.LoadFromFile(simulationFile)

        def _finishCallback(s, output):
            MontageSDK.Interface.PrintFunc('finished:', s, output)
            s.Release()

        MontageSDK.Montage.PopGraphData()
        storyline.Run(finishCallback=_finishCallback)

    def StopSimulation(self):
        from SunshineManager import S_instance
        if not self.runningStoryline:
            return
        else:
            self.runningStoryline.Destroy()
            self.runningStoryline = None
            MontageSDK.Rainbow.Server.SetEditMode(1)
            lighting = S_instance.editorClient.GetPlugin('Lighting')
            lighting.SetCameraMode(0)
            MontageSDK.Interface.resetCameraFollowMode()
            MontageSDK.Montage.PopGraphData()
            MontageSDK.Montage.Server.loadFileInMontage('')
            return

    def GetGraphNodeMetas(self):
        r = []
        for nodeTypeName in NodeManager.GetAllNodeClasses().keys():
            nodeMeta = StorylineSystem.GetNodeEditorMeta(nodeTypeName)
            r.append(nodeMeta)

        return r

    def GetEntityNodeTypes(self):
        return [
         'Avatar']

    def UpgradeGraphData(self, data):
        if 'groupData' in data:
            del data['groupData']
        return data

    def GetCurrentRunningNode(self):
        if self.runningStoryline is None:
            return
        else:
            return self.runningStoryline.context.GetCurrentRunningNode()
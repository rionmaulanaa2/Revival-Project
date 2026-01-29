# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Plugins/MontagePlugin.py
from __future__ import absolute_import
from sunshine.SunshineSDK.SunshineClient import Response
from sunshine.SunshineSDK.Plugin.EditorPlugin import sunshine_rpc
from MontageSDK.MontagePlugin.MontagePluginClient import MontagePluginClient
import MontageSDK
from MontageSDK.Lib.MontGameInterface import MontEditComponent, EndBehavior, AccelerationMode

class MontagePlugin(MontagePluginClient):

    def __init__(self):
        super(MontagePlugin, self).__init__()

    def ActivateMontage(self):
        MontageSDK.PluginReady = True
        if MontageSDK.RuntimeInitiated:
            self.initEdittimeMontage()

    def initEdittimeMontage(self):
        if MontageSDK.Initiated:
            return
        from MontageImp import MontResourceManagerImp
        if MontageSDK.RuntimeInitiated:
            MontageSDK.Interface.MontageEditorInit(castManager=MontageSDK.Castmanager, resManager=MontResourceManagerImp.getInstance(), montagePlugin=MontageSDK.Montage)

    def GetEngineName(self):
        return 'NeoX2'

    def PauseSceneTime(self, status):
        MontageSDK.Interface.PauseCinematics(status, groupName='EditorPreview')

    def SetSceneTime(self, time, isPause=None):
        MontageSDK.Interface.setCineEpisodeTime(time, isPause, groupName='EditorPreview')

    def PauseMontTime(self, status):
        MontageSDK.Interface.PauseCineEpisodeTime(status, groupName='EditorPreview')

    def SetMontTime(self, time, isPause=None):
        return MontageSDK.Interface.SetMontTime(time, isPause, groupName='EditorPreview')

    def SetEnableDOF(self, enable):
        MontageSDK.Interface.EnableDOF(enable)

    def GetCameraTransform(self):
        return MontageSDK.Interface.GetCameraTransform()

    def GetCineEpisodeState(self):
        return MontageSDK.Interface.GetScenePlayingStatus(groupName='EditorPreview')

    def GetMainPlayerSkeleton(self):
        return MontageSDK.Interface.GetMainPlayerSkeleton()

    def ScreenToGamePos(self, screenpos, dist=100):
        return MontageSDK.Interface.screenToGame(screenpos, dist)

    def CreateIndicatorEntity(self, charkey, screenPos):
        MontageSDK.Interface.CreateIndicatorEntity(charkey, screenPos)

    def Reset(self):
        MontageSDK.Interface.ResetCineStatus()

    def PushGraphData(self, cineFile, startTime, isPause=True):
        MontageSDK.Interface.PreviewCinematics(cineFile, startTime, isPause)

    def PushMontData(self, fileName, startTime, isPause=True, previewCamera='', lastUuid=''):
        if previewCamera != 'PreviewMode':
            MontageSDK.Interface.PlayMont(fileName, startTime, previewCamera, isPause, groupName='EditorPreview', endBehavior=EndBehavior.AUTO)
            if MontageSDK.ExtendPlugin:
                from MontageSDK.Lib.MontPathManager import managers
                if 'CameraActor' in managers:
                    managers['CameraActor'].RefreshCameraPath()
                    managers['DollyTrack'].clear()
                    managers['DollyTrack'].RefreshCameraPath()
        else:
            MontageSDK.Interface.previewResourceByUuid(lastUuid, fileName)

    def IsSupportDiffChange(self):
        return MontageSDK.Interface.accelerationMode == AccelerationMode.DiffChange

    def EditorDataChanged(self, dataChangeInfos):
        for info in dataChangeInfos:
            MontageSDK.Interface.OnEditorDataChange(info)

    def SetPreviewCamera(self, previewCamera):
        MontageSDK.Interface.ChangePreviewCamera(previewCamera)

    def PreviewResource(self, restype, data):
        MontageSDK.Interface.PreviewResource(restype, data)

    def GetEntityBoneTransform(self, entityid, bonename, isWorld=True):
        return MontageSDK.Interface.GetEntityBoneTransform(entityid, bonename, isWorld)

    def PopGraphData(self):
        MontageSDK.Interface.PopGraphData()

    def GetEntityBonesByUuid(self, entityUuid):
        return MontageSDK.Interface.GetEntityBonesByUuid(entityUuid)

    def ScanResources(self, resType, force=True):
        if not MontageSDK.ResManager:
            return
        if resType:
            MontageSDK.ResManager.scanResByType(resType, force=force)
        else:
            MontageSDK.ResManager.scanResource(force=force)
        return True

    def DebugSave(self, filename):
        import os
        if not str.endswith(filename, '.cine'):
            plainName = os.path.splitext(filename)[0]
            filename = plainName + '.cine'
        MontageSDK.Interface.DebugSave(filename)

    def GetEntityData(self, uuid, type=MontEditComponent.EDITTYPE_RECRUITED):
        data = MontageSDK.Interface.GetEntityData(uuid, type)
        return data

    def SetEditEntity(self, selection):
        MontageSDK.Interface.SetEditEntity(selection)

    def FocusEntity(self, uuid):
        MontageSDK.Interface.FocusEntity(uuid)
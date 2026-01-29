# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/MontagePlugin/MontagePluginClient.py
from __future__ import absolute_import
from sunshine.SunshineSDK.Plugin.EditorPlugin import EditorPluginClient
from ..MontagePlugin import UUID

class MontagePluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Montage'

    def Test(self, num):
        raise NotImplementedError

    def PushMontData(self, fileName, startTime, isPause=True, previewCamera='', lastUuid=''):
        pass

    def SetPreviewCamera(self, previewCamera):
        pass

    def Reset(self):
        pass

    def PopGraphData(self):
        pass

    def GetCineEpisodeState(self):
        pass

    def SetSceneTime(self, time, isPause=None):
        pass

    def PauseSceneTime(self, status):
        pass

    def SetMontTime(self, time, isPause):
        pass

    def PauseMontTime(self, status):
        pass

    def GetCameraTransform(self):
        pass

    def GetMainPlayerSkeleton(self):
        pass

    def GetEntityBoneTransform(self, entityid, bonename, isWorld=True):
        pass

    def GetEntityBonesByUuid(self, entityUuid):
        pass

    def ScreenToGamePos(self, screenpos, dist=100):
        pass

    def PreviewResource(self, restype, data):
        pass

    def GetEngineName(self):
        pass

    def ActivateMontage(self):
        pass

    def ScanResources(self, resType, force=True):
        pass

    def DebugSave(self, filename):
        pass

    def GetEntityData(self, uuid, type=None):
        pass

    def SetEditEntity(self, selection):
        pass

    def FocusEntity(self, uuid):
        pass

    def DragEntityResource(self):
        pass

    def CreateIndicatorEntity(self, charkey, screenPos):
        pass

    def IsSupportDiffChange(self):
        return False

    def EditorDataChanged(self, data):
        pass

    def Register(self):
        methodMap = super(MontagePluginClient, self).Register()
        methodMap.update({(UUID, 'Test'): self.Test,
           (UUID, 'PushMontData'): self.PushMontData,
           (UUID, 'SetPreviewCamera'): self.SetPreviewCamera,
           (UUID, 'PopGraphData'): self.PopGraphData,
           (UUID, 'GetCineEpisodeState'): self.GetCineEpisodeState,
           (UUID, 'SetSceneTime'): self.SetSceneTime,
           (UUID, 'PauseSceneTime'): self.PauseSceneTime,
           (UUID, 'SetMontTime'): self.SetMontTime,
           (UUID, 'PauseMontTime'): self.PauseMontTime,
           (UUID, 'GetCameraTransform'): self.GetCameraTransform,
           (UUID, 'GetMainPlayerSkeleton'): self.GetMainPlayerSkeleton,
           (UUID, 'ScreenToGamePos'): self.ScreenToGamePos,
           (UUID, 'GetEntityBoneTransform'): self.GetEntityBoneTransform,
           (UUID, 'GetEntityBonesByUuid'): self.GetEntityBonesByUuid,
           (UUID, 'PreviewResource'): self.PreviewResource,
           (UUID, 'Reset'): self.Reset,
           (UUID, 'GetEngineName'): self.GetEngineName,
           (UUID, 'ActivateMontage'): self.ActivateMontage,
           (UUID, 'ScanResources'): self.ScanResources,
           (UUID, 'DebugSave'): self.DebugSave,
           (UUID, 'GetEntityData'): self.GetEntityData,
           (UUID, 'SetEditEntity'): self.SetEditEntity,
           (UUID, 'FocusEntity'): self.FocusEntity,
           (UUID, 'DragEntityResource'): self.DragEntityResource,
           (UUID, 'CreateIndicatorEntity'): self.CreateIndicatorEntity,
           (UUID, 'IsSupportDiffChange'): self.IsSupportDiffChange,
           (UUID, 'EditorDataChanged'): self.EditorDataChanged
           })
        return methodMap
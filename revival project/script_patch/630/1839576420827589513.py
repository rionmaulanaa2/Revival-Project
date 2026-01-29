# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Plugins/MontageExtendPlugin.py
from __future__ import absolute_import
from sunshine.SunshineSDK.Plugin.EditorPlugin import EditorPluginClient, sunshine_rpc
from MontageSDK.Lib.MontPathManager import managers
from ..MontPath import Manager
import MontageSDK
UUID = '5c04a740-2ee4-11eb-b4e2-b42e99cb346f'

class MontageExtendPlugin(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'MessiahDemo'

    def __init__(self):
        pass

    @sunshine_rpc
    def SetEnableDOF(self, enable):
        import MRender
        MRender.SetRenderOption('EnableDoF', '1' if enable else '0')

    @sunshine_rpc
    def EnablePreviewViewport(self, enable):
        PreviewCameraManager.Instance().ChangePreviewViewportStatus(enable)

    @sunshine_rpc
    def GetEffectGizmoTransform(self):
        from .. import EffectPlacer
        if EffectPlacer.g_EffectPlacer:
            pos, rot, scale = EffectPlacer.g_EffectPlacer.getPlacerLocalTransform()
            return (
             [
              pos.x, pos.y, pos.z], [rot.x, rot.y, rot.z], [scale.x, scale.y, scale.z])

    @sunshine_rpc
    def GetEntityBoneTransform(self, entityid, bonename, isWorld=True):
        return MontageSDK.Interface.GetEntityBoneTransform(entityid, bonename, isWorld)

    @sunshine_rpc
    def addPreviewViewport(self, name, width=1024, height=768, passType=1):
        return PreviewViewportController.getInstance().addViewport(name, width, height, passType)

    @sunshine_rpc
    def removePreviewViewport(self, name):
        return PreviewViewportController.getInstance().removeViewport(name)

    @sunshine_rpc
    def applyCameraFrame(self, name, data):
        PreviewViewportController.getInstance().ApplyCameraFrame(name, data)

    @sunshine_rpc
    def setPreviewCam(self, index, name):
        return PreviewViewportController.getInstance().setPreviewCam(index, name)

    @sunshine_rpc
    def SetCameraPath(self, uuids, callback=True, system='CameraActor'):
        if managers.get(system):
            if uuids == [] and list(managers[system].paths.keys()):
                MontageSDK.Interface.gizmo.set_visible(False)
            managers[system].SetCameraPath(uuids, callback)

    @sunshine_rpc
    def SetCameraPathCurPos(self, time, system='CameraActor'):
        if managers.get(system):
            managers[system].SetCurvePathCurPos(time)

    @sunshine_rpc
    def ClearCameraPath(self, system='CameraActor'):
        if managers.get(system):
            managers[system].clear()

    @sunshine_rpc
    def GetCameraPathCurPosTransform(self, uuid, system='CameraActor'):
        if managers.get(system):
            data = managers[system].getCameraPathCurPosTransform(uuid)
            return data
        else:
            return None
            return None

    @sunshine_rpc
    def UpdateRecordMode(self, recordTrackNum):
        MontageSDK.Interface.UpdateRecordMode(recordTrackNum)

    @sunshine_rpc
    def SwitchToBranch(self, branchName):
        MontageSDK.Interface.SwitchToBranch('EditorPreview', branchName)

    @sunshine_rpc
    def GetCurrentSceneID(self):
        return -1

    @sunshine_rpc
    def DrawSmartCamDebugUI(self, enabled, softzonewidth=0, softzoneheight=0, deadzonewidth=0, deadzoneheight=0, offsetx=0, offsety=0):
        pass

    @sunshine_rpc
    def SetEditorObjectVisible(self, typename, visible):
        if 'CameraActor' not in managers:
            return
        typename2PathType = {'All': ['Camera', 'Entity'],'CameraTracks': ['Camera'],'EntityTracks': ['Entity']}
        if typename in typename2PathType:
            for pathType in typename2PathType[typename]:
                managers['CameraActor'].setShowPath(pathType, visible)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Plugins/LightningPlugin.py
from __future__ import absolute_import
from __future__ import print_function
from sunshine.SunshineSDK.Plugin.LightningPlugin import LightningPluginClient
CAMERA_MODE_NORMAL = 0
CAMERA_MODE_FREEVIEW = 1

class LightningPlugin(LightningPluginClient):

    def __init__(self):
        self.cameraMode = CAMERA_MODE_NORMAL

    @property
    def Actor(self):
        return
        import GlobalData
        return GlobalData.p.model.model.Skeleton

    @property
    def CameraController(self):
        return
        import GlobalData
        return GlobalData.camera.controller

    def SetCameraMode(self, mode):
        return
        import MEngine
        import MObject
        print(('SetCameraMode...............', mode))
        self.cameraMode = mode
        if mode == CAMERA_MODE_NORMAL:
            print('SetCameraMode...............CAMERA_MODE_NORMAL\n\n\n')
            MEngine.GetGameplay().Player.Navigator.CameraController = None
            self.CameraController.ControlledCamera = MEngine.GetGameplay().Player.Camera
            if hasattr(MEngine.GetGameplay().Player, 'GetAffiliatedCamera'):
                camera = MEngine.GetGameplay().Player.GetAffiliatedCamera('CEPreviewCamera')
                if camera:
                    self.CameraController.AffiliatedCamera = camera
            actor = self.Actor
            if actor:
                actor.SetEnableControlCamera(True)
        elif mode == CAMERA_MODE_FREEVIEW:
            print('SetCameraMode...............CAMERA_MODE_FREEVIEW\n\n\n')
            self.CameraController.ControlledCamera = None
            if hasattr(MEngine.GetGameplay().Player, 'GetAffiliatedCamera'):
                camera = MEngine.GetGameplay().Player.GetAffiliatedCamera('CEPreviewCamera')
                if camera:
                    self.CameraController.ControlledCamera = camera
                    self.CameraController.AffiliatedCamera = None
            freeViewController = MObject.CreateObject('FreeviewCameraController')
            freeViewController.KeepRoll = True
            MEngine.GetGameplay().Player.Navigator.CameraController = freeViewController
            actor = self.Actor
            if actor:
                actor.SetEnableControlCamera(False)
        return

    def SetCameraSpeed(self, speed):
        pass

    def GetWindowInfo(self):
        return {}
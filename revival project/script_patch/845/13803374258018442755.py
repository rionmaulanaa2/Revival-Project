# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/VenusPlugin/VenusPluginServer.py
from ..EditorPlugin import EditorPluginServer
UUID = '7260c21e-8e6e-11e7-b0eb-e8b1fc1a5d1e'

class VenusPluginServer(EditorPluginServer):
    SUNSHINE_UUID = UUID

    def SceneLoadedCallback(self, val):
        raise NotImplementedError

    def GetClipNamesByEntityUUIDCallback(self, val):
        raise NotImplementedError

    def GetAvailableEntitiesCallback(self, id_objs):
        raise NotImplementedError

    def GetAnimatorNameByEntityUUIDCallback(self, uuid, name):
        raise NotImplementedError

    def GetAnimatorNodeInfoByUuidParmsCallback(self, info):
        raise NotImplementedError

    def ReloadAnimatorCallback(self, animatorFileName):
        raise NotImplementedError

    def SetAnimatorParamCallback(self, key, data):
        raise NotImplementedError

    def GetAnimatorParamsCallback(self, data):
        raise NotImplementedError

    def PushAnimatorStateCallback(self, data):
        raise NotImplementedError

    def ActivateAnimationTreeCallback(self, val):
        raise NotImplementedError

    def DeactivateAnimationTreeCallback(self, val):
        raise NotImplementedError

    def AddParameterCallback(self, val):
        raise NotImplementedError

    def CopyFromCallback(self, animator):
        raise NotImplementedError

    def CopyNodeCallback(self, animNode):
        raise NotImplementedError

    def CreateNodeCallback(self, val):
        raise NotImplementedError

    def FindCallback(self, val):
        raise NotImplementedError

    def FindParameterCallback(self, paramVal):
        raise NotImplementedError

    def GetAnimatorFileNameCallback(self, fileName):
        raise NotImplementedError

    def GetIntCallback(self, iVal):
        raise NotImplementedError

    def GetNodesCallback(self, nodes):
        raise NotImplementedError

    def GetRootNodeCallback(self, root):
        raise NotImplementedError

    def GetSpeedCallback(self, speed):
        raise NotImplementedError

    def HasAnimationTreeCallback(self, bVal):
        raise NotImplementedError

    def IsAnimationTreeActiveCallback(self, bVal):
        raise NotImplementedError

    def ResetCallback(self, val):
        raise NotImplementedError

    def ResetParameterCallback(self, val):
        raise NotImplementedError

    def ResetTriggerCallback(self, val):
        raise NotImplementedError

    def SetAnimationTreeCallback(self, val):
        raise NotImplementedError

    def SetBoolCallback(self, val):
        raise NotImplementedError

    def SetEmptyTreeCallback(self, val):
        raise NotImplementedError

    def SetFloatCallback(self, val):
        raise NotImplementedError

    def SetIntCallback(self, val):
        raise NotImplementedError

    def SetSpeedCallback(self, val):
        raise NotImplementedError

    def SetStateLeaveCallbackCallback(self, val):
        raise NotImplementedError

    def SetTriggerCallback(self, val):
        raise NotImplementedError

    def ToStringCallback(self, val):
        raise NotImplementedError

    def SetNodePropCallback(self, val):
        raise NotImplementedError
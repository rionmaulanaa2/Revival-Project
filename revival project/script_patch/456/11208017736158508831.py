# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/RainbowEditAPI.py


class RainbowEditAPI(object):

    def CreateEntity(self, uuid, data):
        raise NotImplementedError

    def DestroyEntity(self, entity):
        raise NotImplementedError

    def GetEditComponent(self, entity):
        return None

    def SetEntityVisible(self, entity, visible):
        raise NotImplementedError

    def GetCreateEntityData(self):
        return []

    def GetSystemEntities(self):
        return []

    def GetPrefabData(self):
        return []

    def UpdatePrefabData(self, prefabData):
        raise NotImplementedError
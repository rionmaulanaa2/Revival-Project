# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontCastManagerImp.py
from __future__ import absolute_import
import MontageSDK
from MontageSDK.Lib.MontCastManager import MontCastManagerBase

class MontCastManager(MontCastManagerBase):

    def __init__(self):
        super(MontCastManager, self).__init__()
        self.newDesc = set()

    def getCastEntity(self, key):
        entity = self.castEntities.get(key, None)
        if entity and entity.valid:
            return entity
        else:
            if entity:
                self.castEntities.pop(key)
            return

    def onCastCreate(self, movieGroup):
        from .TrackImp.EntityActor import UEntityActor
        if movieGroup.uuid not in self.newDesc:
            return False
        entity = self.getCastEntity(movieGroup.uuid)
        if not entity:
            return False
        if isinstance(movieGroup, UEntityActor):
            charKey = entity.get_file_path()
            if not movieGroup.sceneObjName and charKey != movieGroup.properties['charKey']:
                entity.destroy()
                self.castEntities.pop(movieGroup.uuid)
                return False
        return entity

    def onCastRemoved(self, movieGroup):
        ret = movieGroup.uuid in self.newDesc
        self.onCastDeleted(movieGroup)
        return ret

    def setNewDesc(self, desc):
        self.newDesc = desc

    def onCastAdded(self, movieGroup):
        from .TrackImp.Dummy import UDummy
        if self.castEntities.get(movieGroup.uuid) is not movieGroup.model:
            if not isinstance(movieGroup, UDummy):
                self.castEntities[movieGroup.uuid] = movieGroup.model
            else:
                self.castEntities[movieGroup.uuid] = movieGroup.dummyObj
        MontageSDK.Interface.InformCastEntityAdd(movieGroup.uuid, movieGroup)
        return True

    def onCastDeleted(self, movieGroup):
        if movieGroup.uuid in self.castEntities:
            if movieGroup.uuid not in self.newDesc:
                self.castEntities.pop(movieGroup.uuid)
            MontageSDK.Interface.InformCastEntityDelete(movieGroup.uuid)
            return True
        return False
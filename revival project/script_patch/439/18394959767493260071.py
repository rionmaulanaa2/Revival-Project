# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/EntityBase.py
from __future__ import absolute_import
from UniCineDriver.Movie.MovieGroupEntityBase import MovieGroupEntityBase
import MontageSDK

class UEntityBase(MovieGroupEntityBase):

    def afterinit(self):
        if MontageSDK.Interface.enableCastCache:
            return MontageSDK.Castmanager.onCastCreate(self)
        else:
            return None

    def afterEditorInit(self):
        if MontageSDK.Interface.enableCastCache:
            MontageSDK.Castmanager.onCastAdded(self)
        elif MontageSDK.Initiated:
            MontageSDK.Interface.InformCastEntityAdd(self.uuid, self)

    def clear_data(self):
        super(UEntityBase, self).clear_data()
        enableCastCache = MontageSDK.Interface.enableCastCache
        if not enableCastCache and MontageSDK.Initiated:
            MontageSDK.Interface.InformCastEntityDelete(self.uuid)
        if enableCastCache:
            ret = MontageSDK.Castmanager.onCastRemoved(self)
            return ret
        return False
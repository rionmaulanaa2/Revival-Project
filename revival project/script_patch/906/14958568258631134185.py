# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontCastManager.py
from __future__ import absolute_import

class MontCastManagerBase(object):

    def __init__(self):
        super(MontCastManagerBase, self).__init__()
        self.castEntities = {}

    def init(self):
        pass

    def getCastEntity(self, key):
        for entity, k in self.castEntities.items():
            if key == k:
                return entity

        return None

    def getCastEntityKey(self, entity):
        return self.castEntities.get(entity)

    def existActorHandler(self, operation, args):
        if operation == 'recruit':
            pass
        elif operation == 'query':
            pass
        elif operation == 'dismiss':
            pass

    def onCastChanged(self, cast):
        pass


def setCastInstance(instance):
    global CastInstance
    CastInstance = instance


def getCastInstance():
    return CastInstance


CastInstance = MontCastManagerBase()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontPathManager.py
from __future__ import absolute_import

class MontPathManagerBase(object):

    def __init__(self):
        super(MontPathManagerBase, self).__init__()
        self.paths = {}

    def _createPath(self, uuid):
        pass

    def SetCurvePath(self, uuid, data=None, callback=True):
        pass

    def RemoveCurvePath(self, uuid):
        pass

    def SetCameraPath(self, uuids, callback=True):
        pass

    def clear(self):
        for uuid in self.paths.keys():
            self.RemoveCurvePath(uuid)

    def SetCurvePathCurPos(self, time):
        pass

    def getCameraPathCurPosTransform(self, uuid):
        pass

    def onMouseLDown(self, x, y):
        pass

    def onMouseMove(self, x, y):
        pass


PathMangerDict = {}

def PathManger(cls):
    if issubclass(cls, MontPathManagerBase) or issubclass(cls, MontPathManagerBase.__subclasses__()):
        PathMangerDict[cls.__name__] = cls
    return cls


managers = {}

def initialize():
    global managers
    for name, cls in PathMangerDict.items():
        if getattr(cls, 'SYSTEM'):
            managers[getattr(cls, 'SYSTEM')] = cls()
        else:
            managers[name] = cls()
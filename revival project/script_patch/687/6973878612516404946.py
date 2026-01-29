# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/UniGameInterfaceBase.py
from .Utils.Matrix import RegisterMatrix

class UniGameInterfaceBase(object):
    _warmUpTracks = []
    _warmUpFinishCallbacks = []
    _warmUpLock = False

    @staticmethod
    def setCameraParams(position, rotation, **kwargs):
        pass

    @classmethod
    def warmUpStart(cls, track):
        if not cls._warmUpLock:
            cls._warmUpTracks.append(track)

    @classmethod
    def warmUpFinish(cls, track):
        if track in cls._warmUpTracks:
            cls._warmUpTracks.remove(track)
            if len(cls._warmUpTracks) == 0:
                cls.onAllWarmUpFinish()
                cls._warmUpLock = True

    @classmethod
    def registerWarmUpFinishCb(cls, cb):
        if cb not in cls._warmUpFinishCallbacks:
            cls._warmUpFinishCallbacks.append(cb)

    @classmethod
    def unRegisterWarmUpFinishCb(cls, cb):
        if cb in cls._warmUpFinishCallbacks:
            cls._warmUpFinishCallbacks.remove(cb)

    @classmethod
    def onAllWarmUpFinish(cls):
        for cb in cls._warmUpFinishCallbacks:
            cb()

    @classmethod
    def needWarmUp(cls):
        return len(cls._warmUpTracks) != 0

    @staticmethod
    def registerMatrix(matrixCls):
        RegisterMatrix(matrixCls)
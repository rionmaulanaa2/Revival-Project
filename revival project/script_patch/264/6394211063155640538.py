# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontResourceManager.py
from __future__ import absolute_import
from ..utils.Algorithm import TopoSort
_ResGetters = {}
_ResDependency = {}
ExclusiveCacheList = []

def ResGetter(restype, dependency=[]):

    def wrapper(fcn):
        global _ResDependency
        global _ResGetters
        _ResGetters[restype] = fcn
        _ResDependency[restype] = dependency
        return fcn

    return wrapper


class MontageRes(object):

    def __init__(self, name, path, type):
        self.name = name
        self.path = path
        self.type = type
        self.thumbnail = ''

    def serialize(self):
        result = {}
        for name, value in vars(self).items():
            result[name] = value

        return result


class AudioRes(MontageRes):

    def __init__(self, name, path, type, filepath, time, event):
        super(AudioRes, self).__init__(name, path, type)
        self.filepath = filepath
        self.time = time
        self.event = event


class EffectRes(MontageRes):

    def __init__(self, name, path):
        super(EffectRes, self).__init__(name, path, 'Particle')


class CueRes(MontageRes):

    def __init__(self, name, path, type, meta, cueid):
        super(CueRes, self).__init__(name, path, type)
        self.meta = meta
        self.cueid = cueid


class CharacterRes(MontageRes):

    def __init__(self, name, path, charkey, skeleton, headBone='', type='Character'):
        super(CharacterRes, self).__init__(name, path, type)
        self.charkey = charkey
        self.skeletonFile = skeleton
        self.headBone = headBone


class SubmodelRes(MontageRes):

    def __init__(self, name, path):
        super(SubmodelRes, self).__init__(name, path, 'Model')


class SkeletonAnimationRes(MontageRes):

    def __init__(self, name, path, res, time, typeName='SkeletonAnimation'):
        super(SkeletonAnimationRes, self).__init__(name, path, typeName)
        self.res = res
        self.time = time


class CameraAnimationRes(MontageRes):

    def __init__(self, name, path, time):
        super(CameraAnimationRes, self).__init__(name, path, 'Default')
        self.time = time


class RepoRes(MontageRes):

    def __init__(self, name, path, type, guid, thumbnail):
        super(RepoRes, self).__init__(name, path, type)
        self.guid = guid
        self.thumbnail = thumbnail


class MontResourceManagerBase(object):

    def __init__(self):
        self.modelResourceData = None
        self.cuedata = None
        self.animationMap = {}
        return

    def tryGetResCache(self):
        return False

    def saveResCache(self, data):
        pass

    def scanResource(self, force=False):
        from .. import _Instances
        if not force:
            cache = self.tryGetResCache()
            if isinstance(cache, dict):
                for resType, resData in cache.items():
                    if resType in _ResGetters:
                        if _Instances.Montage:
                            _Instances.Montage.Server.UpdateResourceData(resType, resData)

                for resType in ExclusiveCacheList:
                    resData = _ResGetters[resType](self)
                    if resData and not isinstance(resData[0], dict):
                        resData = [ res.serialize() for res in resData ]
                    if _Instances.Montage:
                        _Instances.Montage.Server.UpdateResourceData(resType, resData)

                return True
        resCache = {}
        for resType in TopoSort(_ResDependency):
            resGetter = _ResGetters[resType]
            resData = resGetter(self)
            if resData and not isinstance(resData[0], dict):
                resData = [ res.serialize() for res in resData ]
            if resType not in ExclusiveCacheList:
                resCache[resType] = resData
            if _Instances.Montage:
                _Instances.Montage.Server.UpdateResourceData(resType, resData)

        if len(resCache) > 0:
            self.saveResCache(resCache)
        return True

    def scanResByType(self, resType, force=False):
        from .. import _Instances
        cache = self.tryGetResCache()
        if not force:
            if isinstance(cache, dict):
                if resType in cache:
                    _Instances.Montage.Server.UpdateResourceData(resType, cache[resType])
                    return True
                return False
        resDependency = {}

        def getDependencyRecursively(dlist):
            for k in dlist:
                resDependency[k] = _ResDependency[k]
                if _ResDependency[k]:
                    getDependencyRecursively(_ResDependency[k])

        getDependencyRecursively([resType])
        for resType in TopoSort(resDependency):
            resFunc = _ResGetters.get(resType, None)
            if not resFunc:
                continue
            resData = resFunc(self)
            if resData and not isinstance(resData[0], dict):
                resData = [ res.serialize() for res in resData ]
            _Instances.Montage.Server.UpdateResourceData(resType, resData)
            if resType not in ExclusiveCacheList:
                if not isinstance(cache, dict):
                    cache = {}
                cache[resType] = resData
                self.saveResCache(cache)

        return True


def getInstance():
    global ResourceInstance
    return ResourceInstance


def setInstance(instance):
    global ResourceInstance
    ResourceInstance = instance


ResourceInstance = MontResourceManagerBase()
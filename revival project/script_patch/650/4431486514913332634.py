# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontTickHandler.py
from __future__ import absolute_import
from six.moves import range
from .. import _Instances
_TickHandlers = {}

def TickHandler(datatype):

    def wrapper(cls):
        global _TickHandlers
        if not issubclass(cls, MontTickHandler):
            return cls
        _TickHandlers[datatype] = cls
        return cls

    return wrapper


class MontTickHandler(object):

    def __init__(self):
        super(MontTickHandler, self).__init__()
        self.forceUpdate = False

    def init(self):
        pass

    def tick(self, time, currentvalue, dt):
        pass

    def reset(self, groupName):
        self.init()


class MontTickManager(object):

    def __init__(self):
        super(MontTickManager, self).__init__()
        self.lasttime = -999
        self.valueToTick = {}
        self.galaxyTickValue = {}
        self.virtualObjData = {}
        self.forceUpdate = 0
        self.tickHandlers = {}

    def init(self):
        for datatype, cls in _TickHandlers.items():
            self.tickHandlers[datatype] = cls()

    def registerValueToTick(self, datatype, data):
        if '/' in datatype:
            propertypath = datatype.split('/')
            entityid, _ = _Instances.Interface.GetEntityByName(propertypath[0])
            if entityid is not None:
                _Instances.Interface.PrintFunc('entityID')
                self.virtualObjData.setdefault(entityid, {})[tuple(propertypath[1:])] = data
            else:
                _Instances.Interface.PrintFunc('entityID is None')
        elif datatype not in self.tickHandlers:
            return
        self.valueToTick[datatype] = data
        self.tickHandlers[datatype].init()
        if self.tickHandlers[datatype].forceUpdate:
            self.forceUpdate += 1
        return

    def unregisterValueToTick(self, datatype, groupName=None):
        if not groupName:
            groupName = _Instances.Interface.getDefaultGroupName()
            if not groupName:
                return
        if datatype not in self.valueToTick:
            return
        else:
            if self.tickHandlers[datatype].forceUpdate:
                self.forceUpdate -= 1
            self.valueToTick.pop(datatype, None)
            return

    def unregisterVirtualTick(self, paramName, paramValue=None):
        worldId, worldEntity = _Instances.Interface.specialObjects['World']['key'], _Instances.Interface.specialObjects['World']['entity']
        if worldId in self.virtualObjData:
            self.virtualObjData[worldId].pop((paramName,), None)
            self.virtualObjData[worldId].pop((paramName, 'r'), None)
            self.virtualObjData[worldId].pop((paramName, 'g'), None)
            self.virtualObjData[worldId].pop((paramName, 'b'), None)
        return

    def clearRegistration(self, groupName, config):
        if getattr(_Instances.Interface, 'cameraRecordMode', False):
            return
        group = _Instances.Interface.getMontageGroupByName(groupName)
        if not group:
            return
        media = group.media

        def getChildByTrackType(trackType):
            for track in media.sceneRootProxy.getChildren():
                if track.trackType == trackType and track.getProperty('disabled'):
                    return track

            return None

        unreg = []
        for datatype, value in self.valueToTick.items():
            if getChildByTrackType(datatype):
                continue
            unreg.append(datatype)

        for datatype in unreg:
            self.tickHandlers.get(datatype).reset(groupName)
            self.unregisterValueToTick(datatype, groupName)

        self.virtualHandler(0)
        self.virtualObjData.clear()

    def registerGalaxyTick(self, datatype, data):
        self.galaxyTickValue[datatype] = data

    def unregisterGalaxyTick(self, datatype):
        self.galaxyTickValue.pop(datatype, None)
        return

    def virtualHandler(self, currenttime):
        if len(self.virtualObjData) == 0:
            return
        for objid, datapair in self.virtualObjData.items():
            envData = {}
            for pathParts, data in datapair.items():
                value = self.interp(currenttime, data)
                splitList = pathParts[0].split('.')
                key = splitList[0]
                if not envData.get(key):
                    if len(splitList) == 2:
                        envData[key] = {}
                    else:
                        envData[key] = []
                if isinstance(envData[key], dict):
                    envData[key][splitList[1]] = value
                elif isinstance(envData[key], list):
                    envData[key].append(value)

        for k, v in envData.items():
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
                _Instances.Interface.EntityModifyParams(objid, [k], v)
            elif isinstance(v, dict):
                for key, value in v.items():
                    _Instances.Interface.EntityModifyParams(objid, [k, key], value)

    @staticmethod
    def getInterval(time, xpos):
        for i in range(len(xpos) - 1):
            nextpos = xpos[i + 1]
            if time < nextpos:
                return (i, time - xpos[i])

        return (
         len(xpos) - 1, 0)

    @staticmethod
    def interp(time, data):
        if not data or 'xpos' not in data:
            return data
        else:
            frames = data['xpos']
            index, t = MontTickManager.getInterval(time, frames)
            if index == len(frames) - 1:
                return data['lastvalue']
            a, b, c, d = data['params'][index]
            if t <= 0:
                return d
            return a * t ** 3 + b * t ** 2 + c * t + d

    def resetTick(self, groupName):
        self.tick(0)

    def tick(self, dt):
        groupName = _Instances.Interface.getDefaultGroupName()
        montageGroups = _Instances.Interface.getAllMontageGroup()
        for name, group in montageGroups.items():
            if hasattr(group, 'previewGraphID') and group.previewGraphID:
                groupName = name
                break

        if groupName is None:
            return
        else:
            status = _Instances.Interface.GetScenePlayingStatus(groupName)
            if status is None:
                return
            currenttime = status['scenetime']
            if currenttime == self.lasttime and self.forceUpdate == 0:
                return
            self.lasttime = currenttime
            self.virtualHandler(currenttime)
            for datatype, handler in self.tickHandlers.items():
                if datatype in self.valueToTick:
                    value = self.interp(currenttime, self.valueToTick[datatype])
                    handler.tick(currenttime, value, dt)

            return


def setInstance(instance):
    global TickInstance
    TickInstance = instance


def getInstance():
    return TickInstance


TickInstance = MontTickManager()
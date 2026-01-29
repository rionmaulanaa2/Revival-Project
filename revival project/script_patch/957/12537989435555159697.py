# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontEventManager.py
from ..Backend.utils.Event import Event
from .. import _Instances

class MontEventManager(object):
    EVENT_TYPES = [
     'PRE', 'POST', 'PRE_TRANSLATE', 'PRE_ASYNC', 'PAUSE_RESUME', 'POST_POP']
    GLOBAL_EVENT_GROUP_NAME = '_GLOBAL'

    def __init__(self):
        self._CinematicEvents = dict()
        self._AsyncEventCallbacks = dict()

    def isMontageGroupAsync(self, groupName):
        eventMap = self._CinematicEvents.get(groupName, {})
        globalEventMap = self._CinematicEvents.get(self.GLOBAL_EVENT_GROUP_NAME, {})
        eventNum = len(eventMap['PRE_ASYNC'].registerFuncs) if 'PRE_ASYNC' in eventMap else 0
        globalEventNum = len(globalEventMap['PRE_ASYNC'].registerFuncs) if 'PRE_ASYNC' in globalEventMap else 0
        return eventNum + globalEventNum

    def isGroupNameRegistered(self, groupName):
        return groupName in self._CinematicEvents

    def registerCinematicEvent(self, cb, eventType='', groupName=None):
        if not callable(cb):
            _Instances.Interface.PrintFunc('[WARNING]The event you try to register is not callable.')
            return
        else:
            if eventType not in self.EVENT_TYPES:
                _Instances.Interface.PrintFunc('[WARNING]The event type you register is not allowed, please use ', str(self.EVENT_TYPES))
                return
            if groupName == '' or groupName is None:
                groupName = self.GLOBAL_EVENT_GROUP_NAME
            if groupName not in self._CinematicEvents:
                self._CinematicEvents[groupName] = {}
            if eventType not in self._CinematicEvents[groupName]:
                self._CinematicEvents[groupName][eventType] = Event()
            self._CinematicEvents[groupName][eventType] += cb
            return

    def unregisterCinematicEvent(self, cb, eventType, groupName=None):
        if not callable(cb):
            _Instances.Interface.PrintFunc('[WARNING]The event you try to unregister is not callable.')
            return
        else:
            if eventType not in self.EVENT_TYPES:
                _Instances.Interface.PrintFunc('[WARNING]The event type you unregister is not allowed, \t\t\tplease use ', str(self.EVENT_TYPES))
                return
            if groupName == '' or groupName is None:
                groupName = self.GLOBAL_EVENT_GROUP_NAME
            if groupName not in self._CinematicEvents or eventType not in self._CinematicEvents[groupName]:
                _Instances.Interface.PrintFunc('[WARNING]The event has never been registered before!')
                return
            self._CinematicEvents[groupName][eventType] -= cb
            return

    def clearRegisterByEventType(self, eventType, groupName=None):
        if eventType not in self.EVENT_TYPES:
            _Instances.Interface.PrintFunc('[WARNING]The event type you try to clear is not allowed,\t\t\tplease use ', str(self.EVENT_TYPES))
            return
        else:
            if groupName == '' or groupName is None:
                groupName = self.GLOBAL_EVENT_GROUP_NAME
            if groupName not in self._CinematicEvents or eventType not in self._CinematicEvents[groupName]:
                return
            self._CinematicEvents[groupName][eventType].Destroy()
            self._CinematicEvents[groupName].pop(eventType)
            if len(self._CinematicEvents[groupName]) == 0:
                self._CinematicEvents.pop(groupName)
            return

    def TriggerEvent(self, eventtype, groupName, *args):
        if self.GLOBAL_EVENT_GROUP_NAME in self._CinematicEvents and eventtype in self._CinematicEvents[self.GLOBAL_EVENT_GROUP_NAME]:
            event = self._CinematicEvents[self.GLOBAL_EVENT_GROUP_NAME][eventtype]
            event(groupName, *args)
        if groupName in self._CinematicEvents and eventtype in self._CinematicEvents[groupName]:
            event = self._CinematicEvents[groupName][eventtype]
            event(groupName, *args)

    def TriggerEventAsync(self, eventtype, groupName, callback, *args):
        globalAsync = self.GLOBAL_EVENT_GROUP_NAME in self._CinematicEvents and eventtype in self._CinematicEvents[self.GLOBAL_EVENT_GROUP_NAME]
        if globalAsync:
            event = self._CinematicEvents[self.GLOBAL_EVENT_GROUP_NAME][eventtype]
            event(groupName, callback, *args)
        groupAsync = groupName in self._CinematicEvents and eventtype in self._CinematicEvents[groupName]
        if groupAsync:
            event = self._CinematicEvents[groupName][eventtype]
            event(groupName, callback, *args)
        return globalAsync or groupAsync

    def AsyncCallbackReceived(self, groupName, config):
        if groupName not in self._AsyncEventCallbacks:
            self._AsyncEventCallbacks[groupName] = 1
        else:
            self._AsyncEventCallbacks[groupName] += 1
        if self._AsyncEventCallbacks[groupName] == self.isMontageGroupAsync(groupName):
            self._AsyncEventCallbacks[groupName] = 0
            _Instances.Interface.AsyncTasksFinishedCallback(groupName, config)

    def PreCinematicPlay(self):
        if 'PRE' not in self._CinematicEvents:
            return
        event = self._CinematicEvents['PRE']
        event()

    def PostCinematicPlay(self):
        if 'POST' not in self._CinematicEvents:
            return
        event = self._CinematicEvents['POST']
        event()


def getMontEventMgrInstance():
    global MontEventMgrInstance
    return MontEventMgrInstance


MontEventMgrInstance = MontEventManager()
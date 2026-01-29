# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/Node.py
__author__ = 'gzhuangwei@corp.netease.com'
import time
from .NodePort import TriggerOutPort, TriggerInPort

class Node(object):
    NODE_META_TYPE = None
    NODE_FLAGS = 0
    INPUT_PORTS = []
    OUTPUT_PORTS = []
    INPUT_PORT_MAP = None
    OUTPUT_PORT_MAP = None
    OUTPUT_TRIGGER_NUM = None
    EXCEPTION_HANDLE_TYPE = None

    def __init__(self):
        super(Node, self).__init__()
        cls = self.__class__
        cls.INPUT_PORT_MAP = dict(((p.GetName(), p) for p in self.INPUT_PORTS))
        cls.OUTPUT_PORT_MAP = dict(((p.GetName(), p) for p in self.OUTPUT_PORTS))
        if cls.OUTPUT_TRIGGER_NUM is None:
            num = 0
            for port in self.OUTPUT_PORTS:
                if port.IsTrigger():
                    num += 1

            cls.OUTPUT_TRIGGER_NUM = num
        self.graph = None
        self.nodeID = None
        self.varData = None
        self.inputPortData = None
        self._canStartTimes = -1
        self._haveStartedTimes = 0
        self._interruptTimes = -1
        self._firstRunTime = 0
        self._runTimesIn1s = 0
        return

    def GetInputPortList(self):
        return self.INPUT_PORTS

    def GetOutputPortList(self):
        return self.OUTPUT_PORTS

    def GetOutputTriggerNum(self):
        return self.OUTPUT_TRIGGER_NUM

    def GetInputPortByName(self, name):
        return self.INPUT_PORT_MAP.get(name, None)

    def GetOutputPortByName(self, name):
        return self.OUTPUT_PORT_MAP.get(name, None)

    def FindInputPort(self, connectPort, name=None):
        if name is not None:
            p = self.GetInputPortByName(name)
            if p is not None and p.CanConnectFrom(connectPort):
                return p
        else:
            for p in self.GetInputPortList():
                if p.CanConnectFrom(connectPort):
                    return p

        return

    def FindOutputPort(self, name=None):
        outputPortList = self.GetOutputPortList()
        if name is None:
            if len(outputPortList) > 0:
                return outputPortList[0]
        else:
            for p in outputPortList:
                if p.GetName() == name:
                    return p

        return

    def HasPortData(self, name):
        return hasattr(self, name)

    def GetPortData(self, name):
        return getattr(self, name)

    def SetPortData(self, name, value):
        setattr(self, name, value)

    def SetProperty(self, name, value):
        setattr(self, name, value)

    def SetSpecialData(self, name, value):
        pass

    def SetTriggerData(self, triggerData):
        pass

    def GetDebugData(self, stage='start'):
        return {'nodeType': self.__class__.__name__,'stage': stage}

    def HasInputTriggerPort(self):
        for port in self.GetInputPortList():
            if port.IsTrigger():
                return True

        return False

    def HasOutputTriggerPort(self):
        for port in self.GetOutputPortList():
            if port.IsTrigger():
                return True

        return False

    def InitDone(self, data, context):
        pass

    def Check(self, context):
        return ''

    def Start(self, context):
        raise NotImplementedError

    def Pause(self, context, status=True):
        pass

    def Release(self, context):
        pass

    def GetAutoStartPriority(self):
        return None

    def CanStart(self, context):
        if self._canStartTimes >= 0:
            if self._runTimesIn1s >= self._canStartTimes:
                self.DoStartWarning(context)
            elif self._haveStartedTimes >= self._canStartTimes:
                if self._interruptTimes >= 0 and self._haveStartedTimes < self._interruptTimes:
                    self.DoStartWarning(context)
        return True

    def AddStartTimes(self, times=1):
        self._haveStartedTimes += times
        if self._canStartTimes >= 0:
            timeNow = time.time()
            if timeNow - self._firstRunTime > 1:
                self._firstRunTime = timeNow
                self._runTimesIn1s = 1
            else:
                self._runTimesIn1s += 1

    def DoStartWarning(self, context):
        pass

    def EditorOnlyModifyNodeData(self, propertyStr, value):
        parts = propertyStr.split('/')
        opt = parts.pop(0)
        from ..Meta.TypeMeta import AddEntityProperty, DelEntityProperty, ModifyEntityProperty
        from ..Meta import ClassMetaManager
        nodeType = self.__class__.__name__
        meta = ClassMetaManager.GetClassMeta(nodeType)
        if opt == 'add':
            if isinstance(value, dict):
                for key in value:
                    AddEntityProperty(self, meta, parts, value[key], key, True)

            elif isinstance(value, (tuple, list)):
                for val in value:
                    if isinstance(val, (tuple, list)):
                        AddEntityProperty(self, meta, parts, val[1], val[0])
                    else:
                        AddEntityProperty(self, meta, parts, val)

            else:
                AddEntityProperty(self, meta, parts, value)
        elif opt == 'del':
            DelEntityProperty(self, meta, parts)
        elif opt == 'mod':
            ModifyEntityProperty(self, meta, parts, value)


class ActionNode(Node):
    NODE_META_TYPE = 'Action'
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort()]


class EventNode(Node):
    NODE_META_TYPE = 'Event'
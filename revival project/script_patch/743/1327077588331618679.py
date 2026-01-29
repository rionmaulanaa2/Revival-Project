# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/NodeGraph.py
from .StorylineConst import NodeFlags
from ..SunshineRpc.Event import Event
from .. import iteritems

class ObservedDict(dict):

    def __init__(self):
        super(ObservedDict, self).__init__()
        self.itemChangedEvent = Event()

    def __setitem__(self, key, val):
        triggerEvent = False
        if key not in self or self.__getitem__(key) != val:
            triggerEvent = True
        super(ObservedDict, self).__setitem__(key, val)
        if triggerEvent:
            self.itemChangedEvent(key)


class NodeGraph(object):

    def __init__(self, context, nodeBuffer, externalData, outputParameterNodeIDList, nodeKeyList, finishCallback=None, exceptionCallback=None):
        self.graphID = self.GenID()
        self.context = context
        self.nodeBuffer = nodeBuffer
        self.outputParameterNodeIDList = outputParameterNodeIDList
        self.finishCallback = finishCallback
        self.finishCallbacks = []
        self.exceptionCallback = exceptionCallback
        self.nodeKeyList = nodeKeyList
        self.pauseBuffer = None
        self.parentNode = None
        self.externalData = externalData
        self.validExecNodes = set()
        self.variables = ObservedDict()
        if externalData and 'Variables' in externalData:
            for k in externalData['Variables']:
                self.variables[k] = externalData['Variables'][k]['defaultValue']

        self.autoStartList = []
        self.nodeStartTimesMap = {}
        signalReceiverNodeList = []
        for runtimeNode in self.nodeBuffer:
            node = runtimeNode.node
            if node.__class__.__name__ == 'SignalReceiverNode':
                signalReceiverNodeList.append(node.nodeID)
            node.graph = self
            autoStartPriority = node.GetAutoStartPriority()
            if autoStartPriority is not None:
                self.autoStartList.append((autoStartPriority, node.nodeID))

        for _, nodeID in self.autoStartList:
            self.CollectValidExecNodes(nodeID)

        for nodeID in signalReceiverNodeList:
            self.CollectValidExecNodes(nodeID)

        self.isReleased = False
        return

    CURRENT_ID = 1

    @staticmethod
    def GenID():
        id = NodeGraph.CURRENT_ID
        NodeGraph.CURRENT_ID += 1
        return id

    def CollectValidExecNodes(self, nodeID):
        self.validExecNodes.add(nodeID)
        nodeRuntime = self.nodeBuffer[nodeID]
        for portName, connections in iteritems(nodeRuntime.connectToMap):
            outputPort = nodeRuntime.node.GetOutputPortByName(portName)
            if not outputPort.IsTrigger():
                continue
            for connection in connections:
                if connection.dstNodeID in self.validExecNodes:
                    continue
                self.CollectValidExecNodes(connection.dstNodeID)

    def InitStartEntities(self):
        entities = self.GetExternalData('Entity')
        if not entities:
            return
        for entityKey, entityData in iteritems(entities):
            isStartEntity = self.context.IsStartEntity(entityKey)
            parentEntityKey = self.context.GetParentEntityKey(entityKey)
            while parentEntityKey:
                if self.context.IsStartEntity(parentEntityKey):
                    isStartEntity = True
                    break
                parentEntityKey = self.context.GetParentEntityKey(parentEntityKey)

            if isStartEntity:
                self.context.CreateEntity(entityKey, entityData)

    def Run(self, initStartEntity=True):
        if self.context.isDebugging and not self.CheckBeforeRun():
            return
        self.context.BindNodeGraph(self)
        if initStartEntity:
            self.InitStartEntities()
        self.autoStartList.sort(reverse=True)
        for _, nodeID in self.autoStartList:
            self.StartNode(nodeID)

    def CheckBeforeRun(self):
        checkResult = True
        for runtimeNode in self.nodeBuffer:
            node = runtimeNode.node
            self.context.SetCurrentNode(node)
            errorMessage = node.Check(self.context)
            if errorMessage:
                self.context.DebugError('\xe8\xbf\x90\xe8\xa1\x8c\xe5\x89\x8d\xe6\xa3\x80\xe6\x9f\xa5\xe5\x87\xba\xe9\x94\x99 %s' % errorMessage)
                checkResult = False

        return checkResult

    def StartNode(self, nodeID, triggerData=None):
        if self.nodeBuffer is None:
            return
        else:
            from .Storyline import StorylineStage
            if self.context.IsStageReach(StorylineStage.TERMINATE):
                return
            nodeRuntime = self.nodeBuffer[nodeID]
            for portName, connections in iteritems(nodeRuntime.connectInMap):
                inputPort = nodeRuntime.node.GetInputPortByName(portName)
                for connect in connections:
                    if inputPort.IsTrigger():
                        if connect.srcNodeID not in self.validExecNodes:
                            invalidNode = self.nodeBuffer[connect.srcNodeID].node
                            self.context.SetCurrentNode(invalidNode)
                            self.context.DebugWarning('\xe5\x9b\xa0\xe4\xb8\xba\xe6\xad\xa4\xe8\x8a\x82\xe7\x82\xb9\xe6\x9c\xaa\xe6\x89\xa7\xe8\xa1\x8c\xef\xbc\x8c\xe5\x90\x8e\xe7\xbb\xad\xe8\xbf\x9e\xe6\x8e\xa5\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae\xe7\xab\xaf\xe5\x8f\xa3\xe5\xb0\x86\xe4\xb8\x8d\xe4\xbc\x9a\xe4\xbb\x8e\xe6\xad\xa4\xe8\x8a\x82\xe7\x82\xb9\xe8\xbf\x9b\xe8\xa1\x8c\xe8\xb5\x8b\xe5\x80\xbc')
                        continue
                    srcNodeID = connect.srcNodeID
                    srcNode = self.nodeBuffer[srcNodeID].node
                    if not srcNode.HasInputTriggerPort() and not srcNode.HasOutputTriggerPort():
                        hasTriggerPort = False
                    else:
                        hasTriggerPort = True
                    if not hasTriggerPort and nodeRuntime.node.GetAutoStartPriority() is None:
                        self.StartNode(srcNodeID)

            self.context.SetCurrentNode(nodeRuntime.node)
            node = nodeRuntime.node
            if not node.CanStart(self.context):
                raise RuntimeWarning('node[%s] start too many times. please check your logic.' % node.__class__.__name__)
            if not self.context.isDebugging and node.__class__.NODE_FLAGS & NodeFlags.NODE_DEVELOPMENT_ONLY:
                self.FinishNode(nodeID, {})
                return
            if node.varData and 'input' in node.varData:
                dstNode = node
                for dstPortName in node.varData['input']:
                    dstPort = dstNode.GetInputPortByName(dstPortName)
                    if len(nodeRuntime.connectInMap[dstPortName]) > 0:
                        continue
                    variableKeys = node.varData['input'][dstPortName]
                    for index, variableKey in enumerate(variableKeys):
                        value = self.variables.get(variableKey, variableKey)
                        if dstPortName.startswith('__') and dstPortName.endswith('__'):
                            dstNode.SetSpecialData(dstPortName, value)
                        else:
                            oldData = dstNode.GetPortData(dstPortName)
                            newData = dstPort.InputData(oldData, '__Variables__', value, -1)
                            dstNode.SetPortData(dstPortName, newData)

            if node.varData and 'property' in node.varData:
                for propertyName in node.varData['property']:
                    variableKeys = node.varData['property'][propertyName]
                    for index, variableKey in enumerate(variableKeys):
                        value = self.variables.get(variableKey, variableKey)
                        node.SetProperty(propertyName, value)

            node.AddStartTimes()
            node.SetTriggerData(triggerData)
            self.context.DebugEnter()
            try:
                r = node.Start(self.context)
                battle = self.context.GetBattle()
                if battle:
                    pass
            except Exception as e:
                import traceback
                import sys
                exc_type, exc_value, exc_traceback = sys.exc_info()
                message = '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                self.context.DebugError(message + '\n' + str(e))
                battle = self.context.GetBattle()
                if battle:
                    battle.logger.error('[Storyline %s-%s]start node error, battle_id: %s', node.nodeID, node.__class__.__name__, battle.id)
                if node.EXCEPTION_HANDLE_TYPE is None:
                    raise
                elif node.EXCEPTION_HANDLE_TYPE == 'pass':
                    r = {}
                elif node.EXCEPTION_HANDLE_TYPE == 'end':
                    self.FinishGraph(exceptionOccurred=True)
                    return

            if isinstance(r, dict):
                self.FinishNode(nodeID, r)
            return

    def FinishNode(self, nodeID, outputs=None):
        if self.nodeBuffer is None:
            return
        else:
            from .Storyline import StorylineStage
            if self.context.IsStageReach(StorylineStage.TERMINATE):
                return
            if self.pauseBuffer is not None:
                self.pauseBuffer.append((nodeID, outputs))
                return
            outputs = outputs or {}
            nodeRuntime = self.nodeBuffer[nodeID]
            node = nodeRuntime.node
            self.context.SetCurrentNode(node)
            nextNodeIDList = []
            nextTriggerIDList = []
            if node.GetOutputTriggerNum() > 0:
                triggerList = outputs.pop('__out__', [])
                not_add_out = outputs.pop('not_add_out', False)
                if not triggerList and '__out__' in nodeRuntime.connectToMap:
                    if not not_add_out:
                        triggerList = [
                         '__out__']
                if isinstance(triggerList, str):
                    triggerList = [
                     triggerList]
                for triggerPortName in triggerList:
                    for connect in nodeRuntime.connectToMap[triggerPortName]:
                        dstPortName = connect.dstPortName
                        dstNode = self.nodeBuffer[connect.dstNodeID].node
                        if dstNode.__class__.__name__ == 'LevelTargetNode':
                            nextTriggerIDList.insert(0, (connect.dstNodeID, triggerPortName, dstPortName))
                        elif dstNode.__class__.__name__ == 'CreateDynamicDoorNode':
                            nextTriggerIDList.insert(0, (connect.dstNodeID, triggerPortName, dstPortName))
                        else:
                            nextTriggerIDList.append((connect.dstNodeID, triggerPortName, dstPortName))

            for srcPortName, value in iteritems(outputs):
                srcPort = node.GetOutputPortByName(srcPortName)
                isSrcTrigger = srcPort and srcPort.IsTrigger()
                if node.varData and 'output' in node.varData and srcPortName in node.varData['output']:
                    for variableKey in node.varData['output'][srcPortName]:
                        self.variables[variableKey] = value

                for connect in nodeRuntime.connectToMap.get(srcPortName, []):
                    dstNodeRuntime = self.nodeBuffer[connect.dstNodeID]
                    dstPortName = connect.dstPortName
                    dstNode = dstNodeRuntime.node
                    dstPort = dstNode.GetInputPortByName(dstPortName)
                    if dstPortName.startswith('__') and dstPortName.endswith('__'):
                        dstNode.SetSpecialData(dstPortName, value)
                    else:
                        oldData = dstNode.GetPortData(dstPortName)
                        indegree = len(dstNodeRuntime.connectInMap[dstPortName])
                        newData = dstPort.InputData(oldData, srcPort, value, indegree)
                        dstNode.SetPortData(dstPortName, newData)
                    if dstPort.IsTrigger():
                        nextNodeIDList.append((connect.dstNodeID, srcPortName, dstPortName))

            self.context.DebugFinish(outputs)
            nextNodeIDList.extend(nextTriggerIDList)
            for nextNodeID, fromPortName, dstPortName in nextNodeIDList:
                if self.isReleased:
                    break
                self.context.SetCurrentNode(node)
                self.context.DebugExecute(nodeID, fromPortName, nextNodeID, dstPortName)
                triggerData = (
                 nodeID, fromPortName, dstPortName)
                self.StartNode(nextNodeID, triggerData)

            self.context.SetCurrentNode(node)
            self.context.DebugLeave()
            return len(nextNodeIDList)

    def GetNodeByID(self, nodeID):
        if self.nodeBuffer is None:
            return
        else:
            return self.nodeBuffer[nodeID].node

    def _GatherOutput(self):
        output = {}
        for i in self.outputParameterNodeIDList:
            self.StartNode(i)
            node = self.nodeBuffer[i].node
            output[node.GetOutputName()] = node.GetValue()

        return output

    def FinishGraph(self, exceptionOccurred=False):
        if self.nodeBuffer is None:
            return
        else:
            self._running = False
            output = self._GatherOutput()
            if exceptionOccurred and callable(self.exceptionCallback):
                self.exceptionCallback(self.context.GetStoryline())
            else:
                if callable(self.finishCallback):
                    self.finishCallback(self.context.GetStoryline(), output)
                for cb in self.finishCallbacks:
                    cb()

            return output

    def Pause(self, status=True):
        if self.nodeBuffer is None:
            return
        else:
            oldStatus = self.pauseBuffer is not None
            if oldStatus == status:
                return status
            node = self.nodeBuffer[self.context.currentNodeID].node
            node.Pause(self.context, status)
            if status:
                self.pauseBuffer = []
            else:
                pauseBuffer = self.pauseBuffer
                self.pauseBuffer = None
                for nodeID, outputs in pauseBuffer:
                    self.FinishNode(nodeID, outputs)

            return oldStatus

    def Release(self):
        if self.isReleased:
            return
        else:
            for node in self.nodeBuffer:
                node.Release(self.context)

            self.nodeBuffer = None
            self.outputParameterNodeIDList = None
            self.finishCallback = None
            self.exceptionCallback = None
            self.pauseBuffer = None
            self.nodeKeyList = []
            self.isReleased = True
            return

    def IsReleased(self):
        return self.isReleased

    def NodeIdxToKey(self, nodeID):
        return self.nodeKeyList[nodeID]

    def GetNodeMetaType(self, nodeID):
        return self.nodeBuffer[nodeID].node.NODE_META_TYPE

    def GetExternalData(self, key):
        return self.externalData.get(key)

    def AddFinishCallback(self, cb):
        if cb not in self.finishCallbacks:
            self.finishCallbacks.append(cb)

    def SetParentNode(self, parentNode):
        self.parentNode = parentNode


class MacroNodeGraph(NodeGraph):

    def __init__(self, context, nodeBuffer, externalData, outputParameterNodeIDList, nodeKeyList, finishCallback=None, exceptionCallback=None):
        super(MacroNodeGraph, self).__init__(context, nodeBuffer, externalData, outputParameterNodeIDList, nodeKeyList, finishCallback, exceptionCallback)
        self.macroInputNode = None
        self.macroOutputNode = None
        self.parentNodeGraph = None
        for runtimeNode in nodeBuffer:
            node = runtimeNode.node
            nodeType = node.__class__.__name__
            if nodeType == 'MacroInputNode':
                self.macroInputNode = node
            elif nodeType == 'MacroOutputNode':
                self.macroOutputNode = node

        return

    def SetInputData(self, portData):
        for k in portData:
            self.macroInputNode.SetPortData(k, portData[k])

    def InitStartEntities(self):
        pass

    def Run(self, initStartEntity=True):
        super(MacroNodeGraph, self).Run(initStartEntity)

    def _GatherOutput(self):
        return self.macroOutputNode.GetOutput()

    def Release(self):
        super(MacroNodeGraph, self).Release()
        self.macroInputNode = None
        self.macroOutputNode = None
        self._runTimes = 0
        return

    def CheckBeforeRun(self):
        result = super(MacroNodeGraph, self).CheckBeforeRun()
        if not result:
            graph = self
            while graph.parentNode:
                parentNode = graph.parentNode
                self.context.SetCurrentNode(parentNode)
                self.context.DebugError('\xe5\x86\x85\xe9\x83\xa8\xe8\x8a\x82\xe7\x82\xb9\xe8\xbf\x90\xe8\xa1\x8c\xe5\x89\x8d\xe6\xa3\x80\xe6\x9f\xa5\xe5\x87\xba\xe9\x94\x99')
                graph = parentNode.graph

        return result
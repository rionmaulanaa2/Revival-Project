# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/Storyline.py
import json
import os
import re
from .NodeGraph import NodeGraph, MacroNodeGraph
from .CommonNodes import InputParameterNode
from ..Meta.ClassMetaManager import GetClassMeta
from .. import iteritems
from . import BaseNode

class StorylineStage(object):
    NEW, INITED, RUNNING, TERMINATE, RELEASING, RELEASED, DESTROY = range(7)


class ChildGraphType(object):
    CHILD_GRAPH, MACRO = range(2)


class StorylineContextBase(object):
    DEBUGGING_FILE_LIST = []

    def __init__(self):
        self.storyline = None
        self.nodeGraph = None
        self.activeNodeGraphs = {}
        self.currentNodeID = None
        self.isDebugMode = False
        self.enterDebugEvent = []
        self.activeSignals = []
        self.shouldRunStartNode = True
        return

    def setActiveSignals(self, signals):
        self.activeSignals = signals

    def setShouldRunStartNode(self, shouldRunStartNode):
        self.shouldRunStartNode = shouldRunStartNode

    def IsStageReach(self, st):
        return self.storyline.IsStageReach(st)

    def IsStartEntity(self, entityKey):
        raise NotImplementedError

    def CreateEntity(self, entityKey, entityData):
        raise NotImplementedError

    def DestroyEntity(self, entityKey):
        raise NotImplementedError

    def GetEntity(self, entityKey):
        raise NotImplementedError

    def CreateStoryline(self, context, storylineNo):
        raise NotImplementedError

    def GetMacroData(self, macroID):
        from .StorylineSystem import GetRepositoryMgr
        mgr = GetRepositoryMgr()
        data = mgr.GetMacroData(macroID)
        return data

    def RunGraph(self, nodeGraph, finishCallback=None, exceptionCallback=None, releaseWhenFinished=True):
        prevNodeGraph = self.nodeGraph
        self.activeNodeGraphs[nodeGraph.graphID] = nodeGraph

        def callback(_, output):
            self.nodeGraph = prevNodeGraph
            self.activeNodeGraphs.pop(nodeGraph.graphID)
            if releaseWhenFinished:
                nodeGraph.Release()
            if finishCallback:
                finishCallback(output)

        def _exceptionCallback(_):
            self.nodeGraph = prevNodeGraph
            self.activeNodeGraphs.pop(nodeGraph.graphID)
            if releaseWhenFinished:
                nodeGraph.Release()
            if exceptionCallback:
                exceptionCallback()

        nodeGraph.finishCallback = callback
        nodeGraph.exceptionCallback = _exceptionCallback
        nodeGraph.Run(False)
        if not nodeGraph.IsReleased():
            return nodeGraph

    def OnDebugEvent(self, nodeID, eventName, eventArgs):
        raise NotImplementedError

    def Release(self):
        raise NotImplementedError

    def GetEntityData(self, entityKey):
        entityData = self.nodeGraph.GetExternalData('Entity')
        if entityData:
            return entityData.get(entityKey)
        else:
            return None

    def GetParentEntityKey(self, entityKey):
        entityData = self.nodeGraph.GetExternalData('Entity')
        if entityData:
            return entityData[entityKey].get('Edit', {}).get('parent', '')
        return ''

    def GetChildEntityKeyList(self, entityKey):
        entityData = self.nodeGraph.GetExternalData('Entity')
        if entityData:
            return [ _key for _key, _data in entityData.items() if self.GetParentEntityKey(_key) == entityKey ]
        return []

    def PreProcess(self, data):
        return data

    @classmethod
    def SetDebugFileList(self, fileList):
        self.DEBUGGING_FILE_LIST = fileList
        print ('DebugFileList', self.DEBUGGING_FILE_LIST)

    def SetDebugMode(self, debugMode):
        self.isDebugMode = debugMode

    @property
    def isDebugging(self):
        return self.isDebugMode or self.storyline.GetFileName() in self.DEBUGGING_FILE_LIST

    def BindNodeGraph(self, nodeGraph):
        self.nodeGraph = nodeGraph
        self.activeNodeGraphs[nodeGraph.graphID] = nodeGraph

    def StartNewGraph(self, nodeGraphBuilder, finishCallback=None, exceptionCallback=None, releaseWhenFinished=True, inputData=None, graphType=ChildGraphType.CHILD_GRAPH, parentNode=None):
        nodeGraphCls = MacroNodeGraph if graphType == ChildGraphType.MACRO else NodeGraph
        externalData = None if graphType == ChildGraphType.MACRO else self.nodeGraph.externalData
        nodeGraph = nodeGraphCls(self, nodeGraphBuilder.nodeBuffer, externalData, nodeGraphBuilder.outputParameterNodeIDList, nodeGraphBuilder.nodeKeyList)
        if inputData:
            nodeGraph.SetInputData(inputData)
        if parentNode:
            nodeGraph.SetParentNode(parentNode)
        return self.RunGraph(nodeGraph, finishCallback, exceptionCallback, releaseWhenFinished)

    def SetCurrentNode(self, node):
        self.nodeGraph = node.graph
        if self.nodeGraph not in self.activeNodeGraphs:
            self.activeNodeGraphs[self.nodeGraph.graphID] = self.nodeGraph
        self.currentNodeID = node.nodeID

    def FinishNode(self, node, outputs=None):
        self.SetCurrentNode(node)
        self.nodeGraph.FinishNode(self.currentNodeID, outputs)

    def FinishGraph(self, graph=None):
        if graph is None:
            graph = self.nodeGraph
        if graph is self.storyline.nodeGraph:
            self.storyline.stage = StorylineStage.TERMINATE
        graph.FinishGraph()
        return

    def DebugEnter(self):
        if self.isDebugging:
            node = self.nodeGraph.GetNodeByID(self.currentNodeID)
            inputs = {}
            for port in node.GetInputPortList():
                name = port.GetName()
                if port.IsTrigger():
                    continue
                if node.HasPortData(name):
                    inputs[name] = node.GetPortData(name)

            meta = GetClassMeta(node.__class__.__name__)
            self.FireDebugEvent(self.currentNodeID, 'Enter', {'input': inputs,
               'properties': meta.SerializeData(node) if meta else {},
               'exData': node.GetDebugData('enter')
               })

    def DebugFinish(self, output):
        if self.isDebugging:
            node = self.nodeGraph.GetNodeByID(self.currentNodeID)
            self.FireDebugEvent(self.currentNodeID, 'Finish', {'output': output,
               'exData': node.GetDebugData('finish'),
               'variables': self.nodeGraph.variables
               })

    def DebugLeave(self):
        if self.isDebugging:
            self.FireDebugEvent(self.currentNodeID, 'Leave')

    def DebugExecute(self, fromNodeID, fromPortName, toNodeID, toPortName):
        if self.isDebugging:
            args = {'fromPortName': fromPortName,'nextNodeID': self.nodeGraph.NodeIdxToKey(toNodeID),
               'toPortName': toPortName
               }
            self.FireDebugEvent(fromNodeID, 'Execute', args)

    def DebugError(self, message):
        if self.isDebugging:
            self.FireDebugEvent(self.currentNodeID, 'Error', {'message': message
               })

    def DebugWarning(self, message):
        if self.isDebugging:
            self.FireDebugEvent(self.currentNodeID, 'Warning', {'message': message
               })

    def FireDebugEvent(self, nodeID, eventName, eventArgs=None):
        if self.nodeGraph.IsReleased() or self.nodeGraph.GetNodeMetaType(nodeID) in ('Entity',
                                                                                     'Decorator'):
            return
        else:
            nodeKey = self.nodeGraph.NodeIdxToKey(nodeID)
            if eventArgs is None:
                eventArgs = {}
            eventArgs['filename'] = self.storyline.GetFileName()
            self.OnDebugEvent(nodeKey, eventName, eventArgs)
            if eventName == 'Enter':
                self.enterDebugEvent.append(nodeKey)
            elif eventName == 'Leave':
                try:
                    self.enterDebugEvent.remove(nodeKey)
                except ValueError:
                    pass

            return

    def Destroy(self):
        self.enterDebugEvent = []
        self.Release()
        self.storyline = None
        self.nodeGraph = None
        self.activeNodeGraphs = {}
        return

    def Clone(self):
        return self.__class__()

    def GetStoryline(self):
        return self.storyline

    def GetNodeByID(self, nodeID, graphID=None):
        graph = self.activeNodeGraphs.get(graphID, self.nodeGraph)
        return graph.GetNodeByID(nodeID)


class Storyline(object):

    def __init__(self, context):
        self.context = context
        self.context.storyline = self
        self.graphBuilder = None
        self.nodeGraph = None
        self.retCode = 0
        self.stage = StorylineStage.NEW
        self._filename = None
        return

    def IsStageReach(self, st):
        return self.stage >= st

    def LoadFromFile(self, filename):
        with open(filename, 'rb') as f:
            data = json.load(f)
        if 'NodeBuffer' not in data['Storyline']:
            directory, name = os.path.split(filename)
            baseFilename = os.path.splitext(name)[0]
            extension = os.path.splitext(name)[1]

            def _mergeSubGraph(_path, _data):
                with open(_path) as fp:
                    subData = json.load(fp)
                    _data['Entities'].update(subData['Entities'])
                    _data['Signals'].update(subData['Signals'])
                    _data['Variables'].update(subData['Variables'])
                    _data['Storyline']['nodeData'].update(subData['Storyline']['nodeData'])
                    _data['Storyline']['lineData'].extend(subData['Storyline']['lineData'])

            if 'SubGraphNames' in data:
                for subGraphName in data['SubGraphNames']:
                    _subGraphFilePath = os.path.join(directory, '%s.%s.%s' % (baseFilename, subGraphName, extension[1:]))
                    if not os.path.exists(_subGraphFilePath):
                        continue
                    _mergeSubGraph(_subGraphFilePath, data)

            else:
                for f in os.listdir(directory):
                    _subGraphFilePath = os.path.join(directory, f)
                    if os.path.isfile(_subGraphFilePath):
                        match = re.match('%s\\.(.+)\\.%s' % (re.escape(baseFilename), extension[1:]), f)
                        if match:
                            _mergeSubGraph(_subGraphFilePath, data)

        self.LoadFromDict(data)
        name = os.path.basename(filename)
        name = os.path.splitext(name)[0]
        self._filename = name

    def LoadFromName(self, name):
        from .StorylineSystem import GetRepositoryMgr
        workspace = GetRepositoryMgr().GetWorkspace()
        filename = os.path.join(workspace, name)
        self.LoadFromFile(filename)

    def LoadFromDict(self, data):
        from .NodeGraphBuilder import NodeGraphBuilder
        graphBuilder = NodeGraphBuilder.CreateFromDict(data, self.context)
        self.SetGraphBuilder(graphBuilder)
        self.stage = StorylineStage.INITED

    def GetFileName(self):
        return self._filename

    def SetFileName(self, filename):
        self._filename = filename

    def SetGraphBuilder(self, graphBuilder):
        self.graphBuilder = graphBuilder

    def Run(self, finishCallback=None, exceptionCallback=None):
        self.nodeGraph = NodeGraph(self.context, self.graphBuilder.nodeBuffer, self.graphBuilder.externalData, self.graphBuilder.outputParameterNodeIDList, self.graphBuilder.nodeKeyList, finishCallback, exceptionCallback)
        self.stage = StorylineStage.RUNNING
        self.nodeGraph.Run()

    def Pause(self):
        if self.nodeGraph:
            self.nodeGraph.Pause(True)

    def Resume(self):
        if self.nodeGraph:
            self.nodeGraph.Pause(False)

    def _HasVariable(self, key):
        return key in self.graphBuilder.externalData['Variables'] and self.graphBuilder.externalData['Variables'][key]['exposed']

    def HasParameter(self, key):
        return self._HasVariable(key) or key in self.graphBuilder.inputParameterNodeMap

    def GetParameter(self, key):
        if self._HasVariable(key):
            return self.graphBuilder.externalData['Variables'][key]['defaultValue']
        else:
            inputParameterNode = self.graphBuilder.inputParameterNodeMap.get(key)
            if inputParameterNode:
                return inputParameterNode.GetValue()
            return None

    def SetParameter(self, key, value):
        if self._HasVariable(key):
            self.graphBuilder.externalData['Variables'][key]['defaultValue'] = value
            return
        inputParameterNode = self.graphBuilder.inputParameterNodeMap.get(key)
        if isinstance(inputParameterNode, InputParameterNode):
            inputParameterNode.SetValue(value)

    def SetParameters(self, parameters):
        for k in parameters:
            self.SetParameter(k, parameters[k])

    def GetVariableKeyByName(self, name):
        variables = self.graphBuilder.externalData['Variables']
        for key, variableData in iteritems(variables):
            if variableData['name'] == name:
                return key

    def GetContext(self):
        return self.context

    def Release(self):
        self.stage = StorylineStage.RELEASING
        if self.nodeGraph:
            self.nodeGraph.Release()
            self.nodeGraph = None
        return

    def Destroy(self):
        self.Release()
        self.stage = StorylineStage.RELEASED
        self.context.Destroy()
        self.stage = StorylineStage.DESTROY
        self.context = None
        return

    def ExportToDict(self):
        return self.graphBuilder.ExportToDict()

    def Export(self, filename):
        with open(filename, 'wb') as f:
            data = self.ExportToDict()
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))
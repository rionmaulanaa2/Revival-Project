# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/CommonNodes.py
__author__ = 'gzhuangwei@corp.netease.com'
from .Node import Node, EventNode, ActionNode
from .NodePort import NodePort, TriggerOutPort, TriggerInPort, EntityPort, EntitiesPort, FloatNodePort, IntNodePort, BoolNodePort, StrNodePort, Vector3NodePort, AnyNodePort, GetParamPortByType
from .NodeManager import storyline_node, storyline_input_parameter_node, storyline_output_parameter_node
from .NodeMetaManager import storyline_node_meta
from .NodeMeta import NodeMeta
from . import StorylineMeta
from .. import iteritems
from ..Meta.TypeMeta import PFloat, PInt, PArray, PCustom

@storyline_node
class StartEvent(EventNode):
    OUTPUT_PORTS = [
     TriggerOutPort()]

    def Start(self, context):
        return {}

    def GetAutoStartPriority(self):
        context = self.graph.context
        if context.isDebugging and not context.shouldRunStartNode:
            return None
        else:
            return 1


@storyline_node_meta
class StartEventMeta(NodeMeta):
    CLASS_NAME = 'StartEvent'
    NODE_TEXT = '\xe5\xbc\x80\xe5\xa7\x8b\xe8\x8a\x82\xe7\x82\xb9'
    NODE_CATEGORY = 'EventNode'


@storyline_node
class EndEvent(EventNode):
    INPUT_PORTS = [
     TriggerInPort()]

    def Start(self, context):
        context.FinishGraph(self.graph)


@storyline_node_meta
class EndEventMeta(NodeMeta):
    CLASS_NAME = 'EndEvent'
    NODE_TEXT = '\xe7\xbb\x93\xe6\x9d\x9f\xe8\x8a\x82\xe7\x82\xb9'
    NODE_CATEGORY = 'EventNode'


@storyline_node
class EndEventEx(EventNode):
    INPUT_PORTS = [
     TriggerInPort()]

    def __init__(self):
        super(EndEventEx, self).__init__()
        self.retCode = 0

    def Start(self, context):
        context.storyline.retCode = self.retCode
        context.FinishGraph(self.graph)


@storyline_node_meta
class EndEventExMeta(NodeMeta):
    CLASS_NAME = 'EndEventEx'
    NODE_TEXT = '\xe7\xbb\x93\xe6\x9d\x9f\xe8\x8a\x82\xe7\x82\xb9Ex'
    NODE_CATEGORY = 'EventNode'
    PROPERTIES = {'retCode': PInt(text='retCode', sort=1)
       }


class EntityNode(Node):
    NODE_META_TYPE = 'Entity'
    OUTPUT_PORTS = [
     EntityPort('__out__')]

    def __init__(self, entityKey):
        super(EntityNode, self).__init__()
        self.entityKey = entityKey

    def Start(self, context):
        return {'__out__': self.entityKey}

    def GetAutoStartPriority(self):
        return 1000


class GraphNode(Node):
    NODE_META_TYPE = 'Graph'
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort()]

    def __init__(self):
        super(GraphNode, self).__init__()
        self.graphBuilder = None
        self.nodeGraph = None
        return

    def Start(self, context):
        self.context = context
        self.nodeGraph = self.context.StartNewGraph(self.graphBuilder, self.OnGraphFinished)

    def OnGraphFinished(self, *args):
        if self.nodeGraph:
            self.nodeGraph = None
        self.context.FinishNode(self, {})
        return

    def Release(self, context):
        if self.nodeGraph:
            self.nodeGraph.Release()
            self.nodeGraph = None
        self.context = None
        super(GraphNode, self).Release(context)
        return


class MacroNode(Node):
    NODE_META_TYPE = 'Macro'
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort()]

    def __init__(self, macroID, nodeGraphBuilder):
        super(MacroNode, self).__init__()
        self.macroID = macroID
        self.graphBuilder = nodeGraphBuilder
        self.context = None
        self.nodeGraph = None
        self.isGraphReleased = False
        self.triggerLogicPortName = ''
        macroInputNode, macroOutputNode = (None, None)
        for runtimeNode in nodeGraphBuilder.nodeBuffer:
            node = runtimeNode.node
            nodeType = node.__class__.__name__
            if nodeType == 'MacroInputNode':
                macroInputNode = node
            elif nodeType == 'MacroOutputNode':
                macroOutputNode = node

        self.inputPortList = [] + self.INPUT_PORTS
        for port in macroInputNode.GetOutputPortList():
            if port.GetName() == '__out__':
                continue
            newPort = port.__class__(port.GetName())
            self.inputPortList.append(newPort)

        self.outputPortList = list(self.OUTPUT_PORTS)
        for port in macroOutputNode.GetInputPortList():
            if port.GetName() == '__in__':
                continue
            newPort = port.__class__(port.GetName())
            self.outputPortList.append(newPort)

        self.inputPortMap = dict(((p.GetName(), p) for p in self.inputPortList))
        self.outputPortMap = dict(((p.GetName(), p) for p in self.outputPortList))
        self.portData = {}
        for port in self.GetInputPortList():
            if not port.IsTrigger():
                self.portData[port.GetName()] = port.GetDefault()

        return

    def HasPortData(self, name):
        return name in self.inputPortMap and not self.inputPortMap[name].IsTrigger()

    def GetPortData(self, name):
        return self.portData.get(name, None)

    def SetPortData(self, name, value):
        self.portData[name] = value

    def SetTriggerData(self, triggerData):
        nodeID, fromPortName, dstPortName = triggerData
        self.triggerLogicPortName = dstPortName

    def GetTriggerLogicPortName(self):
        return self.triggerLogicPortName

    def Start(self, context):
        from .Storyline import ChildGraphType
        self.context = context
        if self.isGraphReleased:
            macroData = context.GetMacroData(self.macroID)
            if not macroData:
                raise RuntimeError('Macro data is empty! macroID=%s' % self.macroID)
            from .NodeGraphBuilder import NodeGraphBuilder
            childBuilder = NodeGraphBuilder.CreateFromDict(macroData, context)
            self.graphBuilder = childBuilder
            self.isGraphReleased = False
        self.nodeGraph = self.context.StartNewGraph(self.graphBuilder, self._OnGraphFinished, inputData=self.portData, graphType=ChildGraphType.MACRO, parentNode=self)

    def Pause(self, context, status=True):
        self.nodeGraph.Pause(status)

    def GetInputPortList(self):
        return self.inputPortList

    def GetInputPortByName(self, name):
        return self.inputPortMap.get(name, None)

    def GetOutputPortList(self):
        return self.outputPortList

    def GetOutputPortByName(self, name):
        return self.outputPortMap.get(name, None)

    def _OnGraphFinished(self, *args):
        self.isGraphReleased = True
        self.nodeGraph = None
        self.context.FinishNode(self, args[0])
        return

    def Release(self, context):
        self.context = None
        self.portData = {}
        if self.nodeGraph:
            self.nodeGraph.Release()
            self.nodeGraph = None
        super(MacroNode, self).Release(context)
        return


class AbstractMacroNode(Node):
    NODE_META_TYPE = 'Macro'
    IS_INPUT = True

    def __init__(self, parameters):
        super(AbstractMacroNode, self).__init__()
        self.portList = [] + self.OUTPUT_PORTS if self.IS_INPUT else self.INPUT_PORTS
        self.portData = {}
        for p in parameters:
            portName = p['portName']
            if p['type'] == 'Logic':
                if self.IS_INPUT:
                    cls = TriggerOutPort if 1 else TriggerInPort
                else:
                    cls = GetParamPortByType(p['type'])
                    self.portData[portName] = None
                self.portList.append(cls(portName))

        self.portMap = dict(((p.GetName(), p) for p in self.portList))
        return

    def HasPortData(self, name):
        return name in self.portMap and not self.portMap[name].IsTrigger()

    def SetPortData(self, name, value):
        self.portData[name] = value

    def GetPortData(self, name):
        return self.portData.get(name, None)

    def Start(self, context):
        raise NotImplementedError


class MacroInputNode(AbstractMacroNode):
    OUTPUT_PORTS = [
     TriggerOutPort()]
    IS_INPUT = True

    def GetOutputPortList(self):
        return self.portList

    def GetOutputPortByName(self, name):
        return self.portMap.get(name, None)

    def Start(self, context):
        parentNode = self.graph.parentNode
        portName = parentNode.GetTriggerLogicPortName()
        ret = self.portData.copy()
        if portName != '__in__':
            ret['__out__'] = [
             portName]
        return ret

    def GetAutoStartPriority(self):
        return 1


class MacroOutputNode(AbstractMacroNode):
    INPUT_PORTS = [
     TriggerInPort()]
    IS_INPUT = False

    def __init__(self, parameters):
        super(MacroOutputNode, self).__init__(parameters)
        self.triggerLogicPortName = '__out__'

    def GetInputPortList(self):
        return self.portList

    def GetInputPortByName(self, name):
        return self.portMap.get(name, None)

    def Start(self, context):
        context.FinishGraph()

    def SetTriggerData(self, triggerData):
        nodeID, fromPortName, dstPortName = triggerData
        self.triggerLogicPortName = dstPortName

    def GetOutput(self):
        output = self.portData.copy()
        if self.triggerLogicPortName != '__in__':
            output['__out__'] = [
             self.triggerLogicPortName]
        return output


class InputParameterNode(Node):
    NODE_META_TYPE = 'Parameter'
    PARAMETER_NAME = 'UnknownParameter'

    def __init__(self, outputPort, inputName, value):
        super(InputParameterNode, self).__init__()
        self.outputPort = outputPort
        self.inputName = inputName
        self.value = value
        self.outputPortList = [outputPort]

    def GetOutputPortList(self):
        return self.outputPortList

    def GetOutputPortByName(self, name):
        if name == self.outputPort.GetName():
            return self.outputPort
        else:
            return None
            return None

    def Start(self, context):
        return {self.outputPort.GetName(): self.value}

    def GetInputName(self):
        return self.inputName

    def SetValue(self, value):
        self.value = value

    def GetValue(self):
        return self.value

    @staticmethod
    def CreateByNameType(portType, inputName, value):
        outputPort = NodePort(StorylineMeta.NodePort('__out__', None, False, portType))
        return InputParameterNode(outputPort, inputName, value)


@storyline_input_parameter_node
class FloatInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'FloatParameter'

    def __init__(self, inputName, value):
        super(FloatInputParameterNode, self).__init__(FloatNodePort('__out__'), inputName, value)


@storyline_input_parameter_node
class IntInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'IntParameter'

    def __init__(self, inputName, value):
        super(IntInputParameterNode, self).__init__(IntNodePort('__out__'), inputName, value)


@storyline_input_parameter_node
class BoolInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'BoolParameter'

    def __init__(self, inputName, value):
        super(BoolInputParameterNode, self).__init__(BoolNodePort('__out__'), inputName, value)


@storyline_input_parameter_node
class StrInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'StrParameter'

    def __init__(self, inputName, value):
        super(StrInputParameterNode, self).__init__(StrNodePort('__out__'), inputName, value)


@storyline_input_parameter_node
class Vector3InputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'Vector3Parameter'

    def __init__(self, inputName, value):
        super(Vector3InputParameterNode, self).__init__(Vector3NodePort(name='__out__'), inputName, value)


@storyline_input_parameter_node
class EntityInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'EntityParameter'

    def __init__(self, inputName, value):
        super(EntityInputParameterNode, self).__init__(EntityPort(name='__out__'), inputName, value)


@storyline_input_parameter_node
class EntityArrayInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'EntityArrayParameter'

    def __init__(self, inputName, value):
        super(EntityArrayInputParameterNode, self).__init__(EntitiesPort(name='__out__'), inputName, value)


@storyline_input_parameter_node
class AnyInputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'AnyParameter'

    def __init__(self, inputName, value):
        super(AnyInputParameterNode, self).__init__(AnyNodePort(name='__out__'), inputName, value)


class OutputParameterNode(Node):
    NODE_META_TYPE = 'Parameter'
    PARAMETER_NAME = 'UnknownParameter'

    def __init__(self, inputPort, outputName, value):
        super(OutputParameterNode, self).__init__()
        self.inputPort = inputPort
        self.outputName = outputName
        self.value = value
        self.inputPortList = [inputPort]

    def GetInputPortList(self):
        return self.inputPortList

    def GetInputPortByName(self, name):
        if name == self.inputPort.GetName():
            return self.inputPort
        else:
            return None
            return None

    def SetSpecialData(self, name, value):
        if name == '__in__':
            self.value = value

    def Start(self, context):
        pass

    def GetOutputName(self):
        return self.outputName

    def GetValue(self):
        return self.value

    @staticmethod
    def CreateByNameType(portType, outputName, value):
        inputPort = NodePort(StorylineMeta.NodePort('__in__', None, False, portType))
        return OutputParameterNode(inputPort, outputName, value)


@storyline_output_parameter_node
class FloatOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'FloatParameter'

    def __init__(self, outputName, value):
        super(FloatOutputParameterNode, self).__init__(FloatNodePort('__in__'), outputName, value)


@storyline_output_parameter_node
class IntOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'IntParameter'

    def __init__(self, outputName, value):
        super(IntOutputParameterNode, self).__init__(IntNodePort('__in__'), outputName, value)


@storyline_output_parameter_node
class BoolOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'BoolParameter'

    def __init__(self, outputName, value):
        super(BoolOutputParameterNode, self).__init__(BoolNodePort('__in__'), outputName, value)


@storyline_output_parameter_node
class StrOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'StrParameter'

    def __init__(self, outputName, value):
        super(StrOutputParameterNode, self).__init__(StrNodePort('__in__'), outputName, value)


@storyline_output_parameter_node
class Vector3OutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'Vector3Parameter'

    def __init__(self, outputName, value):
        super(Vector3OutputParameterNode, self).__init__(Vector3NodePort(name='__in__'), outputName, value)


@storyline_output_parameter_node
class EntityOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'EntityParameter'

    def __init__(self, outputName, value):
        super(EntityOutputParameterNode, self).__init__(EntityPort(name='__in__'), outputName, value)


@storyline_output_parameter_node
class EntityArrayOutputParameterNode(InputParameterNode):
    PARAMETER_NAME = 'EntityArrayParameter'

    def __init__(self, outputName, value):
        super(EntityArrayOutputParameterNode, self).__init__(EntitiesPort(name='__in__'), outputName, value)


@storyline_output_parameter_node
class AnyOutputParameterNode(OutputParameterNode):
    PARAMETER_NAME = 'AnyParameter'

    def __init__(self, outputName, value):
        super(AnyOutputParameterNode, self).__init__(AnyNodePort(name='__in__'), outputName, value)


class CallStoryline(ActionNode):

    def __init__(self, storyline):
        super(CallStoryline, self).__init__()
        self.storyline = storyline
        inputTypes, outputTypes = storyline.graphBuilder.GetInputOutputParameterTypes()
        self.inputPortList = self.INPUT_PORTS + list((NodePort(StorylineMeta.NodePort(name, name, portType=typeName)) for name, typeName in iteritems(inputTypes)))
        self.outputPortList = self.OUTPUT_PORTS + list((NodePort(StorylineMeta.NodePort(name, name, portType=typeName)) for name, typeName in iteritems(outputTypes)))
        self.inputPortMap = dict(((p.GetName(), p) for p in self.inputPortList))
        self.outputPortMap = dict(((p.GetName(), p) for p in self.outputPortList))
        num = 0
        for port in self.outputPortList:
            if port.IsTrigger():
                num += 1

        self.outputTriggerNum = num

    def GetInputPortList(self):
        return self.inputPortList

    def GetOutputPortList(self):
        return self.outputPortList

    def GetInputPortByName(self, name):
        return self.inputPortMap.get(name, None)

    def GetOutputPortByName(self, name):
        return self.outputPortMap.get(name, None)

    def GetOutputTriggerNum(self):
        return self.outputTriggerNum

    def HasPortData(self, name):
        return self.storyline.HasParameter(name)

    def GetPortData(self, name):
        return self.storyline.GetParameter(name)

    def SetPortData(self, name, value):
        self.storyline.SetParameter(name, value)

    def Start(self, context):

        def _Finished(storyline, output):
            context.FinishNode(self, output)

        self.storyline.Run(_Finished)

    def Release(self, context):
        if self.storyline:
            self.storyline.Release()
            self.storyline = None
        return


class MakeEntityArrayDecorator(Node):
    NODE_META_TYPE = 'Decorator'
    INPUT_PORTS = [
     EntitiesPort(name='__decorator_in__', isTrigger=True)]
    OUTPUT_PORTS = [EntitiesPort(name='__decorator_out__')]

    def __init__(self):
        super(MakeEntityArrayDecorator, self).__init__()
        self.entityKey = []

    def SetSpecialData(self, name, value):
        if name == '__decorator_in__':
            if not isinstance(value, list):
                value = [
                 value]
            for v in value:
                if v not in self.entityKey:
                    self.entityKey.append(v)

    def _HasVarInput(self):
        return self.varData and 'input' in self.varData and bool(self.varData['input'])

    def GetAutoStartPriority(self):
        if self._HasVarInput():
            return 1
        else:
            return None

    def Start(self, context):
        return {'__decorator_out__': self.entityKey}


@storyline_node
class TimeConditionPass(ActionNode):

    def __init__(self):
        super(TimeConditionPass, self).__init__()
        self.passTime = 0
        self.interval = 0

    def Start(self, context):
        import time
        timeNow = time.time()
        if self.passTime == 0 or self.interval > 0 and timeNow - self.passTime > self.interval:
            self.passTime = timeNow
            return {}


@storyline_node_meta
class TimeConditionPassNodeMeta(NodeMeta):
    CLASS_NAME = 'TimeConditionPass'
    NODE_TEXT = '\xe6\x97\xb6\xe9\x97\xb4\xe6\x9d\xa1\xe4\xbb\xb6\xe9\x80\x9a\xe8\xbf\x87'
    NODE_CATEGORY = 'GraphNode'
    PROPERTIES = {'interval': PFloat(text='\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4(0\xe8\xa1\xa8\xe7\xa4\xba\xe5\x8f\xaa\xe9\x80\x9a\xe8\xbf\x87\xe4\xb8\x80\xe6\xac\xa1)', min=0, max=999999, sort=2)
       }


class DynamicNode(ActionNode):

    def __init__(self):
        super(DynamicNode, self).__init__()
        self.inputParams = []
        self.outputParams = []
        self.inputPorts = []
        self.outputPorts = []
        self.portData = {}

    def initPorts(self):
        plist = []
        for param in self.inputParams:
            plist.append(self.CreatePort(param, True))

        self.inputPorts = self.INPUT_PORTS + plist
        plist = []
        for param in self.outputParams:
            plist.append(self.CreatePort(param, False))

        self.outputPorts = self.OUTPUT_PORTS + plist

    def _getInputPortMap(self):
        return dict(((p.GetName(), p) for p in self.GetInputPortList()))

    def _getOutputPortMap(self):
        return dict(((p.GetName(), p) for p in self.GetOutputPortList()))

    def HasPortData(self, name):
        inputPortMap = self._getInputPortMap()
        return name in inputPortMap and not inputPortMap[name].IsTrigger()

    def GetPortData(self, name):
        if hasattr(self, name):
            data = getattr(self, name)
        else:
            data = self.portData.get(name, None)
        return data

    def SetPortData(self, name, value):
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            self.portData[name] = value

    def GetInputPortList(self):
        return self.inputPorts

    def GetInputPortByName(self, name):
        return self._getInputPortMap().get(name, None)

    def GetOutputPortList(self):
        return self.outputPorts

    def GetOutputPortByName(self, name):
        return self._getOutputPortMap().get(name, None)

    def CreatePort(self, data, isInput):
        if data['type'] == 'Logic':
            if isInput:
                return TriggerInPort(data['portName'])
            else:
                self.OUTPUT_TRIGGER_NUM += 1
                return TriggerOutPort(data['portName'])

        portCls = GetParamPortByType(data['type'])
        return portCls(data['portName'])


class DynamicNodeMeta(NodeMeta):
    EDITOR_NODE_CLS = 'StorylineDynamicParamProxyNode'
    PROPERTIES = {'inputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=True, default={'portName': None,'paramName': 'Param','type': 'Int'})),
       'outputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=True, default={'portName': None,'paramName': 'Param','type': 'Int'}))
       }


class _SignalNodeBase(EventNode):
    IS_SENDER = True

    def __init__(self, data):
        super(_SignalNodeBase, self).__init__()
        self.signalKey = data['key']
        self.portList = [] + self.INPUT_PORTS if self.IS_SENDER else self.OUTPUT_PORTS
        self.portData = {}
        for p in data['parameters']:
            portName = p['key']
            cls = GetParamPortByType(p['type'])
            self.portList.append(cls(portName))
            self.portData[portName] = None

        self.portMap = dict(((p.GetName(), p) for p in self.portList))
        return

    def HasPortData(self, name):
        return name in self.portMap and not self.portMap[name].IsTrigger()

    def SetPortData(self, name, value):
        self.portData[name] = value

    def GetPortData(self, name):
        return self.portData.get(name, None)

    def Start(self, context):
        raise NotImplementedError


class SignalSenderNode(_SignalNodeBase):
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort()]
    IS_SENDER = True

    def GetInputPortList(self):
        return self.portList

    def GetInputPortByName(self, name):
        return self.portMap.get(name, None)

    def Start(self, context):
        nodeGraph = context.nodeGraph
        for nodeID, runtimeNode in enumerate(nodeGraph.nodeBuffer):
            node = runtimeNode.node
            if isinstance(node, SignalReceiverNode) and node.signalKey == self.signalKey:
                node.portData.clear()
                node.portData.update(self.portData)
                context.nodeGraph.StartNode(nodeID)

        output = self.portData.copy()
        return output


class SignalReceiverNode(_SignalNodeBase):
    OUTPUT_PORTS = [
     TriggerOutPort()]
    IS_SENDER = False

    def GetOutputPortList(self):
        return self.portList

    def GetOutputPortByName(self, name):
        return self.portMap.get(name, None)

    def Start(self, context):
        return self.portData.copy()

    def GetAutoStartPriority(self):
        context = self.graph.context
        if context.isDebugging and self.signalKey in context.activeSignals:
            return 1000
        else:
            return None


class _VariableNodeBase(ActionNode):

    def __init__(self, variableData, value):
        super(_VariableNodeBase, self).__init__()
        self.variableKey = variableData['key']
        self.value = value
        self.portList = [] + self.INPUT_PORTS
        portName = variableData['key']
        cls = GetParamPortByType(variableData['type'])
        self.portList.append(cls(portName))

    def GetInputPortList(self):
        return self.portList

    def GetInputPortByName(self, name):
        if name == self.variableKey:
            return self.portList[-1]
        return super(_VariableNodeBase, self).GetInputPortByName(name)

    def HasPortData(self, name):
        return name == self.variableKey

    def SetPortData(self, name, value):
        self.value = value

    def SetProperty(self, name, value):
        self.value = value

    def GetPortData(self, name):
        if name == self.variableKey:
            return self.value
        else:
            return None
            return None

    def Start(self, context):
        raise NotImplementedError


class StorylineVariableSetterNode(_VariableNodeBase):
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort()]

    def Start(self, context):
        nodeGraph = context.nodeGraph
        nodeGraph.variables[self.variableKey] = self.value
        return {}


class StorylineVariableCompareNode(_VariableNodeBase):
    INPUT_PORTS = [
     TriggerInPort()]
    OUTPUT_PORTS = [
     TriggerOutPort(name='true'),
     TriggerOutPort(name='false')]

    def Start(self, context):
        nodeGraph = context.nodeGraph
        result = nodeGraph.variables[self.variableKey] > self.value
        return {'__out__': 'true' if result else 'false'}
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/LogicMathNodes.py
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..NodePort import BoolNodePort, TriggerOutPort, TriggerPortMeta
from ..CommonNodes import DynamicNode, DynamicNodeMeta
from ..NodeMeta import NodeMeta
from ..Node import ActionNode
from ..StorylineMeta import BoolPort
from ...Meta.TypeMeta import PArray, PCustom, PInt

class LogicBaseMeta(DynamicNodeMeta):
    NODE_CATEGORY = 'BaseNode|LogicNode'
    INPUT_PORT_TEXT_MAP = {'a': '\xe5\xb8\x83\xe5\xb0\x94A',
       'b': '\xe5\xb8\x83\xe5\xb0\x94B'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'a': BoolPort(text='\xe5\xb8\x83\xe5\xb0\x94A'),
       'b': BoolPort(text='\xe5\xb8\x83\xe5\xb0\x94B')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'true': TriggerPortMeta(text='true'),
       'false': TriggerPortMeta(text='false')
       }
    PROPERTIES = {'inputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[
                     'Bool'], hasExec=False, default={'portName': None,'paramName': '\xe5\xb8\x83\xe5\xb0\x94','type': 'Bool'})),
       'outputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, visible=False, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=True, default={'portName': None,'paramName': 'Param','type': 'Int'}))
       }


class LogicBaseNode(DynamicNode):
    INPUT_PORTS = DynamicNode.INPUT_PORTS + [
     BoolNodePort('a'),
     BoolNodePort('b')]
    OUTPUT_PORTS = [
     TriggerOutPort('true'),
     TriggerOutPort('false')]

    def __init__(self):
        super(LogicBaseNode, self).__init__()
        self.a = False
        self.b = False


@storyline_node_meta
class LogicAndBooleanMeta(LogicBaseMeta):
    CLASS_NAME = 'LogicAndBooleanNode'
    NODE_TEXT = '\xe9\x80\xbb\xe8\xbe\x91\xe4\xb8\x8e'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#logic-and-node'
    NODE_TIPS = '\xe5\xb0\x86\xe8\xbe\x93\xe5\x85\xa5\xe7\x9a\x84\xe5\xb8\x83\xe5\xb0\x94\xe5\x80\xbc\xe4\xb8\x8e\xe4\xb8\x80\xe4\xb8\x8b'


@storyline_node
class LogicAndBooleanNode(LogicBaseNode):

    def Start(self, context):
        result = {'__out__': ['true' if self._calcLogicAnd() else 'false']}
        return result

    def _calcLogicAnd(self):
        res = self.a and self.b
        for var in self.inputParams:
            value = self.GetPortData(var['portName'])
            res = res and value

        return res


@storyline_node_meta
class LogicOrBooleanMeta(LogicBaseMeta):
    CLASS_NAME = 'LogicOrBooleanNode'
    NODE_TEXT = '\xe9\x80\xbb\xe8\xbe\x91\xe6\x88\x96'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#logic-or-node'
    NODE_TIPS = '\xe5\xb0\x86\xe8\xbe\x93\xe5\x85\xa5\xe7\x9a\x84\xe5\xb8\x83\xe5\xb0\x94\xe5\x80\xbc\xe6\x88\x96\xe4\xb8\x80\xe4\xb8\x8b'
    OUTPUT_PORT_TEXT_MAP = {'equal': '=',
       'notEqual': '!='
       }


@storyline_node
class LogicOrBooleanNode(LogicBaseNode):

    def Start(self, context):
        result = {'__out__': ['true' if self._calcLogicOr() else 'false']}
        return result

    def _calcLogicOr(self):
        res = self.a or self.b
        for var in self.inputParams:
            value = self.GetPortData(var['portName'])
            res = res or value

        return res


@storyline_node_meta
class LogicNegationBooleanMeta(NodeMeta):
    CLASS_NAME = 'LogicNegationBooleanNode'
    NODE_TEXT = '\xe9\x80\xbb\xe8\xbe\x91\xe9\x9d\x9e'
    NODE_CATEGORY = 'BaseNode|LogicNode'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#logic-not-node'
    NODE_TIPS = '\xe5\xb0\x86\xe8\xbe\x93\xe5\x85\xa5\xe7\x9a\x84\xe5\xb8\x83\xe5\xb0\x94\xe5\x80\xbc\xe5\x8f\x96\xe5\x8f\x8d'
    INPUT_PORT_TEXT_MAP = {'a': '\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'true': 'true',
       'false': 'false'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'a': BoolPort(text='\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'true': TriggerPortMeta(text='true'),
       'false': TriggerPortMeta(text='false')
       }


@storyline_node
class LogicNegationBooleanNode(ActionNode):
    INPUT_PORTS = DynamicNode.INPUT_PORTS + [
     BoolNodePort('a')]
    OUTPUT_PORTS = [
     TriggerOutPort('true'),
     TriggerOutPort('false')]

    def __init__(self):
        super(LogicNegationBooleanNode, self).__init__()
        self.a = False

    def Start(self, context):
        if self.a:
            return {'__out__': 'false'}
        else:
            return {'__out__': 'true'}


@storyline_node_meta
class TestMultipleBoolMeta(LogicBaseMeta):
    CLASS_NAME = 'TestMultipleBoolNode'
    NODE_TEXT = '\xe5\xb8\x83\xe5\xb0\x94\xe8\xae\xa1\xe6\x95\xb0'
    SEMANTICS = '{{nodeText}}\n\xe6\x95\xb0\xe9\x87\x8f{{property.count}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#test-multi-bool-node'
    NODE_TIPS = '\xe5\xbd\x93\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x98\xe9\x87\x8f\xe9\x87\x8c\xe5\xb8\x83\xe5\xb0\x94\xe4\xb8\xba\xe7\x9c\x9f\xe7\x9a\x84\xe4\xb8\xaa\xe6\x95\xb0\xe5\xa4\xa7\xe4\xba\x8e\xe7\xad\x89\xe4\xba\x8ecount\xe6\x97\xb6\xef\xbc\x8c\xe8\xa7\xa6\xe5\x8f\x91>=\xe7\xab\xaf\xe5\x8f\xa3\xef\xbc\x8c\xe5\xb0\x8f\xe4\xba\x8e\xe6\x97\xb6\xef\xbc\x8c\xe8\xa7\xa6\xe5\x8f\x91<\xe7\xab\xaf\xe5\x8f\xa3'
    OUTPUT_PORT_TEXT_MAP = {'largerOrEqual': '>=',
       'lessThan': '<'
       }
    OUTPUT_PORTS = {'largerOrEqual': TriggerPortMeta(text='>='),
       'lessThan': TriggerPortMeta(text='<')
       }
    PROPERTIES = {'count': PInt(sort=2, text='\xe6\x95\xb0\xe9\x87\x8f', default=0, tip='\xe8\xbe\x93\xe5\x85\xa5\xe4\xb8\xad\xe4\xb8\xba\xe7\x9c\x9f\xe7\x9a\x84\xe4\xb8\xaa\xe6\x95\xb0'),
       'inputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[
                     'Bool'], hasExec=False, default={'portName': None,'paramName': '\xe5\xb8\x83\xe5\xb0\x94','type': 'Bool'})),
       'outputParams': PArray(sort=3, text='\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x82\xe6\x95\xb0', maxSize=50, visible=False, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=True, default={'portName': None,'paramName': 'Param','type': 'Int'}))
       }


@storyline_node
class TestMultipleBoolNode(LogicBaseNode):
    OUTPUT_PORTS = [
     TriggerOutPort('largerOrEqual'),
     TriggerOutPort('lessThan')]

    def Start(self, context):
        result = {'__out__': ['largerOrEqual' if self._calcTrueCount() >= self.count else 'lessThan']}
        return result

    def _calcTrueCount(self):
        trueCount = 0
        if self.a:
            trueCount += 1
        if self.b:
            trueCount += 1
        for var in self.inputParams:
            value = self.GetPortData(var['portName'])
            if value:
                trueCount += 1

        return trueCount
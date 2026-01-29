# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/AdvancedMathNodes.py
import random
import math
from .BaseMathNodes import BaseNumbersMeta, BaseNumbersNode
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..Node import ActionNode
from ..NodePort import IntNodePort, FloatNodePort, EntitiesPort, TriggerPortMeta
from ..NodeMeta import NodeMeta
from ..StorylineMeta import IntPort, EntitiesPort as EntitiesPortMeta, FloatPort
from ...Meta.TypeMeta import OrderedProperties, PInt, PFloat, PBool

@storyline_node_meta
class ModuloNumbersMeta(BaseNumbersMeta):
    NODE_CATEGORY = 'BaseNode|AdvancedMath'
    CLASS_NAME = 'ModuloNumbersNode'
    NODE_TEXT = '\xe4\xbd\x99\xe6\x95\xb0'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#modulo-node'
    NODE_TIPS = '\xe5\x8f\x98\xe9\x87\x8fA\xe5\x92\x8c\xe5\x8f\x98\xe9\x87\x8fB\xe5\x8f\x96\xe4\xbd\x99\xef\xbc\x8c\xe7\xbb\x93\xe6\x9e\x9c\xe8\xbe\x93\xe5\x87\xba\xe5\x88\xb0\xe4\xbd\x99\xe6\x95\xb0\xe5\x92\x8c\xe5\x95\x86\xe6\x95\xb0\xe9\x87\x8c'
    OUTPUT_PORT_TEXT_MAP = {'modulo': '\xe4\xbd\x99\xe6\x95\xb0',
       'quotient': '\xe5\x95\x86\xe6\x95\xb0'
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'modulo': IntPort(text='\xe4\xbd\x99\xe6\x95\xb0'),
       'quotient': IntPort(text='\xe5\x95\x86\xe6\x95\xb0')
       }


@storyline_node
class ModuloNumbersNode(BaseNumbersNode):
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     IntNodePort('modulo'),
     IntNodePort('quotient')]

    def Start(self, context):
        modulo = self.eax % self.ebx
        quotient = self.eax // self.ebx
        return {'modulo': modulo,'quotient': quotient}


@storyline_node_meta
class RandomIntMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|AdvancedMath'
    CLASS_NAME = 'RandomIntNode'
    NODE_TEXT = '\xe9\x9a\x8f\xe6\x9c\xba\xe6\x95\xb4\xe6\x95\xb0'
    SEMANTICS = '{{nodeText}}\n\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc{{property.min}}\n\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc{{property.max}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#random-int-node'
    OUTPUT_PORT_TEXT_MAP = {'result': '\xe7\xbb\x93\xe6\x9e\x9c'
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'result': IntPort(text='\xe7\xbb\x93\xe6\x9e\x9c')
       }
    PROPERTIES = OrderedProperties([
     (
      'min', PInt(text='\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc', default=0)),
     (
      'max', PInt(text='\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc', default=100))])


@storyline_node
class RandomIntNode(ActionNode):
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     IntNodePort('result')]

    def __init__(self):
        super(RandomIntNode, self).__init__()
        self.min = 0
        self.max = 100

    def Start(self, context):
        result = random.randint(self.min, self.max)
        return {'result': result}


@storyline_node_meta
class RandomFloatMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|AdvancedMath'
    CLASS_NAME = 'RandomFloatNode'
    NODE_TEXT = '\xe9\x9a\x8f\xe6\x9c\xba\xe6\xb5\xae\xe7\x82\xb9\xe6\x95\xb0'
    SEMANTICS = '{{nodeText}}\n\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc{{property.min}}\n\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc{{property.max}}\n\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\x96\xe6\x95\xb4{{property.isRounded}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#random-float-node'
    OUTPUT_PORT_TEXT_MAP = {'result': '\xe7\xbb\x93\xe6\x9e\x9c'
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'result': FloatPort(text='\xe7\xbb\x93\xe6\x9e\x9c')
       }
    PROPERTIES = OrderedProperties([
     (
      'min', PFloat(text='\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc', default=0.0)),
     (
      'max', PFloat(text='\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc', default=100.0)),
     (
      'isRounded', PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\x96\xe6\x95\xb4', default=False))])


@storyline_node
class RandomFloatNode(ActionNode):
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     FloatNodePort('result')]

    def __init__(self):
        super(RandomFloatNode, self).__init__()
        self.min = 0.0
        self.max = 100.0

    def Start(self, context):
        result = random.uniform(self.min, self.max)
        if self.isRounded:
            result = math.floor(result)
        return {'result': result}


@storyline_node_meta
class GetEntitiesCountMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|AdvancedMath'
    CLASS_NAME = 'GetEntitiesCountNode'
    NODE_TEXT = '\xe8\x8e\xb7\xe5\x8f\x96Entities\xe6\x95\xb0\xe9\x87\x8f'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#get-entities-num-node'
    INPUT_PORT_TEXT_MAP = {'entities': '\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84'
       }
    OUTPUT_PORT_TEXT_MAP = {'count': '\xe6\x95\xb0\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'entities': EntitiesPortMeta(text='\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'count': IntPort(text='\xe6\x95\xb0\xe9\x87\x8f')
       }


@storyline_node
class GetEntitiesCountNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     EntitiesPort('entities')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     IntNodePort('count')]

    def __init__(self):
        super(GetEntitiesCountNode, self).__init__()
        self.entities = []

    def Start(self, context):
        count = len(self.entities)
        return {'count': count}
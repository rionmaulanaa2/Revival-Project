# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/BaseMathNodes.py
from ..NodeMeta import NodeMeta
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..Node import ActionNode
from ..StorylineMeta import MultiTypesPort, IntPort
from ..NodePort import MultiTypesNodePort, TriggerPortMeta, IntNodePort
from ...Meta.TypeMeta import PInt

class BaseNumbersMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|BaseMath'
    INPUT_PORT_TEXT_MAP = {'eax': '\xe5\x8f\x98\xe9\x87\x8fA',
       'ebx': '\xe5\x8f\x98\xe9\x87\x8fB'
       }
    OUTPUT_PORT_TEXT_MAP = {'dst': '\xe7\xbb\x93\xe6\x9e\x9c'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'eax': MultiTypesPort(text='\xe5\x8f\x98\xe9\x87\x8fA', supportedTypes=['Int', 'Float']),
       'ebx': MultiTypesPort(text='\xe5\x8f\x98\xe9\x87\x8fB', supportedTypes=['Int', 'Float'])
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'dst': MultiTypesPort(text='\xe7\xbb\x93\xe6\x9e\x9c', supportedTypes=['Int', 'Float'])
       }


class BaseNumbersNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     MultiTypesNodePort('eax', supportedTypes=['Int', 'Float']),
     MultiTypesNodePort('ebx', supportedTypes=['Int', 'Float'])]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     MultiTypesNodePort('dst', supportedTypes=['Int', 'Float'])]

    def __init__(self):
        super(BaseNumbersNode, self).__init__()
        self.eax = 0
        self.ebx = 0


@storyline_node_meta
class AddNumbersMeta(BaseNumbersMeta):
    CLASS_NAME = 'AddNumbersNode'
    NODE_TEXT = '\xe5\x8f\x98\xe9\x87\x8f\xe7\x9b\xb8\xe5\x8a\xa0'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#add-node'


@storyline_node
class AddNumbersNode(BaseNumbersNode):

    def Start(self, context):
        dst = self.eax + self.ebx
        return {'dst': dst}


@storyline_node_meta
class SubtractNumbersMeta(BaseNumbersMeta):
    CLASS_NAME = 'SubtractNumbersNode'
    NODE_TEXT = '\xe5\x8f\x98\xe9\x87\x8f\xe7\x9b\xb8\xe5\x87\x8f'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#subtract-node'


@storyline_node
class SubtractNumbersNode(BaseNumbersNode):

    def Start(self, context):
        dst = self.eax - self.ebx
        return {'dst': dst}


@storyline_node_meta
class MultiplyNumbersMeta(BaseNumbersMeta):
    CLASS_NAME = 'MultiplyNumbersNode'
    NODE_TEXT = '\xe5\x8f\x98\xe9\x87\x8f\xe7\x9b\xb8\xe4\xb9\x98'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#multi-node'


@storyline_node
class MultiplyNumbersNode(BaseNumbersNode):

    def Start(self, context):
        dst = self.eax * self.ebx
        return {'dst': dst}


@storyline_node_meta
class DivideNumbersMeta(BaseNumbersMeta):
    CLASS_NAME = 'DivideNumbersNode'
    NODE_TEXT = '\xe5\x8f\x98\xe9\x87\x8f\xe7\x9b\xb8\xe9\x99\xa4'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#divide-node'


@storyline_node
class DivideNumbersNode(BaseNumbersNode):

    def Start(self, context):
        dst = self.eax / self.ebx
        return {'dst': dst}


@storyline_node_meta
class MinMeta(BaseNumbersMeta):
    CLASS_NAME = 'MinNode'
    NODE_TEXT = '\xe5\x8f\x96\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#min-node'


@storyline_node
class MinNode(BaseNumbersNode):

    def Start(self, context):
        dst = min(self.eax, self.ebx)
        return {'dst': dst}


@storyline_node_meta
class MaxMeta(BaseNumbersMeta):
    CLASS_NAME = 'MaxNode'
    NODE_TEXT = '\xe5\x8f\x96\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#max-node'


@storyline_node
class MaxNode(BaseNumbersNode):

    def Start(self, context):
        dst = max(self.eax, self.ebx)
        return {'dst': dst}


class BaseIntNodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|BaseMath'
    INPUT_PORT_TEXT_MAP = {'eax': '\xe6\x95\xb4\xe6\x95\xb0A'
       }
    OUTPUT_PORT_TEXT_MAP = {'dst': '\xe7\xbb\x93\xe6\x9e\x9c'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'eax': IntPort(text='\xe6\x95\xb4\xe6\x95\xb0A')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'dst': IntPort(text='\xe7\xbb\x93\xe6\x9e\x9c')
       }
    PROPERTIES = {'ebx': PInt(sort=2, text='\xe6\x95\xb4\xe6\x95\xb0B', min=-50000, max=50000)
       }


class BaseIntNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     IntNodePort('eax')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     IntNodePort('dst')]

    def __init__(self):
        super(BaseIntNode, self).__init__()
        self.eax = 0
        self.ebx = 0


@storyline_node_meta
class BaseIntAddNodeMeta(BaseIntNodeMeta):
    CLASS_NAME = 'BaseIntAddNode'
    NODE_TEXT = '\xe6\x95\xb4\xe6\x95\xb0\xe5\x8a\xa0\xe6\xb3\x95'
    SEMANTICS = '{{nodeText}}\n\xe6\x95\xb4\xe6\x95\xb0A:{{input.eax}}\n\xe6\x95\xb4\xe6\x95\xb0B:{{property.ebx}}\n\xe7\xbb\x93\xe6\x9e\x9c:{{local.dst}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#int-add-node'


@storyline_node
class BaseIntAddNode(BaseIntNode):

    def Start(self, context):
        dst = self.eax + self.ebx
        return {'dst': dst}


@storyline_node_meta
class BaseIntSubtractNodeMeta(BaseIntNodeMeta):
    CLASS_NAME = 'BaseIntSubtractNode'
    NODE_TEXT = '\xe6\x95\xb4\xe6\x95\xb0\xe5\x87\x8f\xe6\xb3\x95'
    SEMANTICS = '{{nodeText}}\n\xe6\x95\xb4\xe6\x95\xb0A:{{input.eax}}\n\xe6\x95\xb4\xe6\x95\xb0B:{{property.ebx}}\n\xe7\xbb\x93\xe6\x9e\x9c:{{local.dst}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#int-substract-node'


@storyline_node
class BaseIntSubtractNode(BaseIntNode):

    def Start(self, context):
        dst = self.eax - self.ebx
        return {'dst': dst}


@storyline_node_meta
class BaseIntMultiNodeMeta(BaseIntNodeMeta):
    CLASS_NAME = 'BaseIntMultiNode'
    NODE_TEXT = '\xe6\x95\xb4\xe6\x95\xb0\xe4\xb9\x98\xe6\xb3\x95'
    SEMANTICS = '{{nodeText}}\n\xe6\x95\xb4\xe6\x95\xb0A:{{input.eax}}\n\xe6\x95\xb4\xe6\x95\xb0B:{{property.ebx}}\n\xe7\xbb\x93\xe6\x9e\x9c:{{local.dst}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#int-multi-node'


@storyline_node
class BaseIntMultiNode(BaseIntNode):

    def Start(self, context):
        dst = self.eax * self.ebx
        return {'dst': dst}


@storyline_node_meta
class BaseIntDivideNodeMeta(BaseIntNodeMeta):
    CLASS_NAME = 'BaseIntDivideNode'
    NODE_TEXT = '\xe6\x95\xb4\xe6\x95\xb0\xe9\x99\xa4\xe6\xb3\x95'
    SEMANTICS = '{{nodeText}}\n\xe6\x95\xb4\xe6\x95\xb0A:{{input.eax}}\n\xe6\x95\xb4\xe6\x95\xb0B:{{property.ebx}}\n\xe7\xbb\x93\xe6\x9e\x9c:{{local.dst}}'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#int-divide-node'


@storyline_node
class BaseIntDivideNode(BaseIntNode):

    def Start(self, context):
        dst = self.eax / self.ebx
        return {'dst': dst}
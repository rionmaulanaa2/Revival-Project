# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/CopyVariableNodes.py
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..Node import ActionNode
from ..NodePort import IntNodePort, FloatNodePort, TriggerPortMeta, BoolNodePort, Vector3NodePort, StrNodePort
from ..NodeMeta import NodeMeta
from ..StorylineMeta import IntPort, FloatPort, BoolPort, Vector3Port, StrPort

@storyline_node_meta
class CopyIntNodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CopyNode'
    CLASS_NAME = 'CopyIntNode'
    NODE_TEXT = '\xe5\xa4\x8d\xe5\x88\xb6\xe6\x95\xb4\xe6\x95\xb0'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#copy-int-node'
    INPUT_PORT_TEXT_MAP = {'source': '\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'target': '\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'source': IntPort(text='\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'target': IntPort(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f')
       }
    SEMANTICS = '{{nodeText}}\n{{input.source}}->{{local.target}}'


@storyline_node
class CopyIntNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     IntNodePort('source')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     IntNodePort('target')]

    def __init__(self):
        super(CopyIntNode, self).__init__()
        self.source = 0

    def Start(self, context):
        self.target = self.source
        return {'target': self.target}


@storyline_node_meta
class CopyBoolNodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CopyNode'
    CLASS_NAME = 'CopyBoolNode'
    NODE_TEXT = '\xe5\xa4\x8d\xe5\x88\xb6\xe5\xb8\x83\xe5\xb0\x94'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#copy-bool-node'
    NODE_TIPS = '\xe6\x8a\x8a\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x98\xe9\x87\x8f\xe7\x9a\x84\xe5\x80\xbc\xef\xbc\x8c\xe5\xa4\x8d\xe5\x88\xb6\xe7\xbb\x99\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x98\xe9\x87\x8f'
    INPUT_PORT_TEXT_MAP = {'source': '\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'target': '\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'source': BoolPort(text='\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'target': BoolPort(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f')
       }
    SEMANTICS = '{{nodeText}}\n{{input.source}}->{{local.target}}'


@storyline_node
class CopyBoolNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     BoolNodePort('source')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     BoolNodePort('target')]

    def __init__(self):
        super(CopyBoolNode, self).__init__()
        self.source = False

    def Start(self, context):
        self.target = self.source
        return {'target': self.target}


@storyline_node_meta
class CopyVector3NodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CopyNode'
    CLASS_NAME = 'CopyVector3Node'
    NODE_TEXT = '\xe5\xa4\x8d\xe5\x88\xb6\xe5\x90\x91\xe9\x87\x8f'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#copy-vector-node'
    NODE_TIPS = '\xe6\x8a\x8a\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x98\xe9\x87\x8f\xe7\x9a\x84\xe5\x80\xbc\xef\xbc\x8c\xe5\xa4\x8d\xe5\x88\xb6\xe7\xbb\x99\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x98\xe9\x87\x8f'
    INPUT_PORT_TEXT_MAP = {'source': '\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'target': '\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'source': Vector3Port(text='\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'target': Vector3Port(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f')
       }
    SEMANTICS = '{{nodeText}}\n{{input.source}}->{{local.target}}'


@storyline_node
class CopyVector3Node(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     Vector3NodePort('source')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     Vector3NodePort('target')]

    def __init__(self):
        super(CopyVector3Node, self).__init__()
        self.source = 0

    def Start(self, context):
        self.target = self.source
        return {'target': self.target}


@storyline_node_meta
class CopyFloatNodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CopyNode'
    CLASS_NAME = 'CopyFloatNode'
    NODE_TEXT = '\xe5\xa4\x8d\xe5\x88\xb6\xe6\xb5\xae\xe7\x82\xb9\xe6\x95\xb0'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#copy-float-node'
    NODE_TIPS = '\xe6\x8a\x8a\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x98\xe9\x87\x8f\xe7\x9a\x84\xe5\x80\xbc\xef\xbc\x8c\xe5\xa4\x8d\xe5\x88\xb6\xe7\xbb\x99\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x98\xe9\x87\x8f'
    INPUT_PORT_TEXT_MAP = {'source': '\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'target': '\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'source': FloatPort(text='\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'target': FloatPort(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f')
       }
    SEMANTICS = '{{nodeText}}\n{{input.source}}->{{local.target}}'


@storyline_node
class CopyFloatNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     FloatNodePort('source')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     FloatNodePort('target')]

    def __init__(self):
        super(CopyFloatNode, self).__init__()
        self.source = 0

    def Start(self, context):
        self.target = self.source
        return {'target': self.target}


@storyline_node_meta
class CopyStrNodeMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CopyNode'
    CLASS_NAME = 'CopyStrNode'
    NODE_TEXT = '\xe5\xa4\x8d\xe5\x88\xb6\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#copy-str-node'
    NODE_TIPS = '\xe6\x8a\x8a\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x98\xe9\x87\x8f\xe7\x9a\x84\xe5\x80\xbc\xef\xbc\x8c\xe5\xa4\x8d\xe5\x88\xb6\xe7\xbb\x99\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\x98\xe9\x87\x8f'
    INPUT_PORT_TEXT_MAP = {'source': '\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f'
       }
    OUTPUT_PORT_TEXT_MAP = {'target': '\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'source': StrPort(text='\xe6\xba\x90\xe5\x8f\x98\xe9\x87\x8f')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out'),
       'target': StrPort(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x8f\x98\xe9\x87\x8f')
       }
    SEMANTICS = '{{nodeText}}\n{{input.source}}->{{local.target}}'


@storyline_node
class CopyStrNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     StrNodePort('source')]
    OUTPUT_PORTS = ActionNode.OUTPUT_PORTS + [
     StrNodePort('target')]

    def __init__(self):
        super(CopyStrNode, self).__init__()
        self.source = 0

    def Start(self, context):
        self.target = self.source
        return {'target': self.target}
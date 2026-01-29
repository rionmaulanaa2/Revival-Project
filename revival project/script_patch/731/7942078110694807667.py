# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/CompareNodes.py
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..Node import ActionNode
from ..NodePort import BoolNodePort, EntitiesPort, TriggerOutPort, TriggerPortMeta, MultiTypesNodePort
from ..NodeMeta import NodeMeta
from ..StorylineMeta import MultiTypesPort
from ..StorylineMeta import BoolPort, EntitiesPort as EntitiesPortMeta
from ...Meta.TypeMeta import OrderedProperties, PEnum, DefEnum

@storyline_node_meta
class NumberCompareMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CompareNode'
    CLASS_NAME = 'NumberCompareNode'
    NODE_TEXT = '\xe6\x95\xb0\xe5\xad\x97\xe6\xaf\x94\xe8\xbe\x83'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#num-compare-node'
    NODE_TIPS = '\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\xa4\xe4\xb8\xaa\xe8\xbe\x93\xe5\x85\xa5\xe7\x9a\x84\xe5\xa4\xa7\xe5\xb0\x8f\xef\xbc\x8c\xe8\xa7\xa6\xe5\x8f\x91\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\xa3\xe7\x9a\x84\xe5\x86\x85\xe5\xae\xb9'
    INPUT_PORT_TEXT_MAP = {'eax': '\xe6\x95\xb0\xe5\xad\x97A',
       'ebx': '\xe6\x95\xb0\xe5\xad\x97B'
       }
    OUTPUT_PORT_TEXT_MAP = {'lessThan': '<',
       'equal': '=',
       'largerThan': '>'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In', tip='\xe8\xbe\x93\xe5\x85\xa5\xe7\xab\xaf\xe5\x8f\xa3'),
       'eax': MultiTypesPort(text='\xe6\x95\xb0\xe5\xad\x97A', supportedTypes=['Int', 'Float'], tip='\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x98\xafint/float'),
       'ebx': MultiTypesPort(text='\xe6\x95\xb0\xe5\xad\x97B', supportedTypes=['Int', 'Float'], tip='\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x98\xafint/float')
       }
    OUTPUT_PORTS = {'lessThan': TriggerPortMeta(text='<', tip='\xe5\xb0\x8f\xe4\xba\x8e'),
       'equal': TriggerPortMeta(text='=', tip='\xe7\xad\x89\xe4\xba\x8e'),
       'largerThan': TriggerPortMeta(text='>', tip='\xe5\xa4\xa7\xe4\xba\x8e')
       }


@storyline_node
class NumberCompareNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     MultiTypesNodePort('eax', supportedTypes=['Int', 'Float']),
     MultiTypesNodePort('ebx', supportedTypes=['Int', 'Float'])]
    OUTPUT_PORTS = [
     TriggerOutPort('lessThan'),
     TriggerOutPort('equal'),
     TriggerOutPort('largerThan')]

    def __init__(self):
        super(NumberCompareNode, self).__init__()
        self.eax = 0
        self.ebx = 0

    @staticmethod
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def Start(self, context):
        result = {'__out__': []}
        if self.isclose(self.eax, self.ebx):
            result['__out__'] = [
             'equal']
        elif self.eax > self.ebx:
            result['__out__'] = [
             'largerThan']
        else:
            result['__out__'] = [
             'lessThan']
        return result


@storyline_node_meta
class BoolCompareMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CompareNode'
    CLASS_NAME = 'BoolCompareNode'
    NODE_TEXT = '\xe5\xb8\x83\xe5\xb0\x94\xe5\x80\xbc\xe6\xaf\x94\xe8\xbe\x83'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#bool-compare-node'
    NODE_TIPS = '\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\xa4\xe4\xb8\xaa\xe5\xb8\x83\xe5\xb0\x94\xe5\x80\xbc\xe6\x98\xaf\xe5\x90\xa6\xe7\x9b\xb8\xe7\xad\x89'
    INPUT_PORT_TEXT_MAP = {'a': '\xe5\xb8\x83\xe5\xb0\x94A',
       'b': '\xe5\xb8\x83\xe5\xb0\x94B'
       }
    OUTPUT_PORT_TEXT_MAP = {'equal': '=',
       'notEqual': '!='
       }
    INPUT_PORTS = {'a': BoolPort(text='\xe5\xb8\x83\xe5\xb0\x94A'),
       'b': BoolPort(text='\xe5\xb8\x83\xe5\xb0\x94B')
       }
    OUTPUT_PORTS = {'equal': TriggerPortMeta(text='='),
       'notEqual': TriggerPortMeta(text='!=')
       }


@storyline_node
class BoolCompareNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     BoolNodePort('a'),
     BoolNodePort('b')]
    OUTPUT_PORTS = [
     TriggerOutPort('equal'),
     TriggerOutPort('notEqual')]

    def __init__(self):
        super(BoolCompareNode, self).__init__()
        self.a = True
        self.b = False

    def Start(self, context):
        result = {'__out__': []}
        if self.a == self.b:
            result['__out__'] = [
             'equal']
        else:
            result['__out__'] = [
             'notEqual']
        return result


DefEnum('BoolValue', {0: 'False',
   1: 'True'
   })

@storyline_node_meta
class TestBoolMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CompareNode'
    CLASS_NAME = 'TestBoolNode'
    NODE_TEXT = '\xe5\xb8\x83\xe5\xb0\x94\xe5\x88\xa4\xe6\x96\xad'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#test-bool-node'
    NODE_TIPS = '\xe6\xb5\x8b\xe8\xaf\x95\xe5\xb8\x83\xe5\xb0\x94\xe5\x8f\x98\xe9\x87\x8f\xe5\xbd\x93\xe5\x89\x8d\xe7\x9a\x84\xe5\x80\xbc'
    SEMANTICS = '{{nodeText}}\n\xe5\x80\xbc{{property.value}}'
    INPUT_PORT_TEXT_MAP = {'a': '\xe5\xb8\x83\xe5\xb0\x94'
       }
    OUTPUT_PORT_TEXT_MAP = {'equal': 'True',
       'notEqual': 'False'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'a': BoolPort(text='\xe5\xb8\x83\xe5\xb0\x94')
       }
    OUTPUT_PORTS = {'equal': TriggerPortMeta(text='True'),
       'notEqual': TriggerPortMeta(text='False')
       }
    PROPERTIES = OrderedProperties([
     (
      'value', PEnum(text='\xe5\x80\xbc', enumType='BoolValue', default=0))])


@storyline_node
class TestBoolNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     BoolNodePort('a')]
    OUTPUT_PORTS = [
     TriggerOutPort('equal'),
     TriggerOutPort('notEqual')]

    def __init__(self):
        super(TestBoolNode, self).__init__()
        self.a = True
        self.value = 0

    def Start(self, context):
        result = {'__out__': []}
        if self.a == self.value:
            result['__out__'] = [
             'equal']
        else:
            result['__out__'] = [
             'notEqual']
        return result


@storyline_node_meta
class EntitiesCompareMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|CompareNode'
    CLASS_NAME = 'EntitiesCompareNode'
    NODE_TEXT = 'Entities\xe6\xaf\x94\xe8\xbe\x83'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#entities-compare-node'
    NODE_TIPS = '\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\xa4\xe4\xb8\xaaEntities\xe6\x98\xaf\xe5\x90\xa6\xe7\x9b\xb8\xe7\xad\x89'
    INPUT_PORT_TEXT_MAP = {'a': '\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84A',
       'b': '\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84B'
       }
    OUTPUT_PORT_TEXT_MAP = {'equal': '=',
       'notEqual': '!='
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'a': EntitiesPortMeta(text='\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84A'),
       'b': EntitiesPortMeta(text='\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xbb\x84B', entityType='')
       }
    OUTPUT_PORTS = {'equal': TriggerPortMeta(text='='),
       'notEqual': TriggerPortMeta(text='!=')
       }


@storyline_node
class EntitiesCompareNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     EntitiesPort('a', entityType=''),
     EntitiesPort('b', entityType='')]
    OUTPUT_PORTS = [
     TriggerOutPort('equal'),
     TriggerOutPort('notEqual')]

    def __init__(self):
        super(EntitiesCompareNode, self).__init__()
        self.a = []
        self.b = []

    def Start(self, context):
        result = {'__out__': []}
        if list(set(self.a)) == list(set(self.b)):
            result['__out__'] = [
             'equal']
        else:
            result['__out__'] = [
             'notEqual']
        return result
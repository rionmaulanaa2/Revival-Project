# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/ListenerNodes.py
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..Node import ActionNode
from ..NodePort import AnyNodePort, TriggerPortMeta
from ..NodeMeta import NodeMeta
from ..StorylineMeta import AnyPort

@storyline_node_meta
class OnVariableValueChangedMeta(NodeMeta):
    NODE_CATEGORY = 'BaseNode|ListenerNode'
    CLASS_NAME = 'OnVariableValueChangedNode'
    NODE_TEXT = '\xe5\x8f\x98\xe9\x87\x8f\xe5\x80\xbc\xe6\x94\xb9\xe5\x8f\x98\xe6\x97\xb6'
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#variable-listener-node'
    NODE_TIPS = '\xe7\x9b\x91\xe5\x90\xac\xe5\x8f\x98\xe9\x87\x8f\xe7\x9a\x84\xe5\x80\xbc\xe5\x8f\x98\xe5\x8c\x96\xef\xbc\x8c\xe5\x8f\x98\xe5\x8c\x96\xe6\x97\xb6\xe8\xa7\xa6\xe5\x8f\x91\xe5\x90\x8e\xe9\x9d\xa2\xe7\x9a\x84\xe8\x8a\x82\xe7\x82\xb9'
    INPUT_PORT_TEXT_MAP = {'variable': '\xe5\x8f\x98\xe9\x87\x8f'
       }
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In'),
       'variable': AnyPort(text='\xe5\x8f\x98\xe9\x87\x8f')
       }


@storyline_node
class OnVariableValueChangedNode(ActionNode):
    INPUT_PORTS = ActionNode.INPUT_PORTS + [
     AnyNodePort('variable')]

    def __init__(self):
        super(OnVariableValueChangedNode, self).__init__()
        self.variable = None
        return

    def Start(self, context):

        def onVariableChanged(key):
            self.key = self.varData['input']['variable'][0]
            if self.key == key:
                context.FinishNode(self)

        context.nodeGraph.variables.itemChangedEvent += onVariableChanged
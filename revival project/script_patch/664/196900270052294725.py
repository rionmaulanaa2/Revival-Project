# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/NodeMeta.py
from . import StorylineConst
from ..Meta import ClassMetaManager
from ..Meta.EditorMeta import EditorMeta
from ..Meta.TypeMeta import ClassMeta, InitObject
from .StorylineMeta import ActionNodeMeta, EventNodeMeta, ParameterNodeMeta
from .NodePort import TriggerPortMeta

class NodeMeta(ClassMeta):
    NODE_TEXT = ''
    NODE_CATEGORY = ''
    INPUT_PORT_TEXT_MAP = {}
    OUTPUT_PORT_TEXT_MAP = {}
    SEMANTICS = ''
    NODE_META_TYPE = 'Action'
    INPUT_PORTS = {'__in__': TriggerPortMeta(text='In')
       }
    OUTPUT_PORTS = {'__out__': TriggerPortMeta(text='Out')
       }
    NODE_USE_RANGE = 'common'
    NODE_USE_RANGE_TEXT_MAP = {'common': '',
       'server': '\xef\xbc\x88\xe6\x9c\x8d\xef\xbc\x89',
       'client': '\xef\xbc\x88\xe5\xae\xa2\xef\xbc\x89'
       }
    NODE_SUPPORTED_CONNECT_RANGE = {'common': [],'server': [
                'common', 'server'],
       'client': [
                'common', 'client']
       }
    NODE_COMMENT = ''
    NODE_TIPS = ''
    NODE_DOC = ''
    EDITOR_NODE_CLS = None
    NORMAL_STATE_COLOR = StorylineConst.S_NODE_NORMAL_TYPE_COLOR
    NODE_META_CREATOR_MAP = {'Action': ActionNodeMeta,
       'Event': EventNodeMeta,
       'Parameter': ParameterNodeMeta
       }
    REPLACE_NODE_TYPES = []
    NODE_FLAGS = 0

    def GetNodeEditorMeta(self, nodeCls):
        inputPortDataList = []
        for port in nodeCls.INPUT_PORTS:
            name = port.GetName()
            if self.INPUT_PORTS and name in self.INPUT_PORTS:
                portMeta = self.INPUT_PORTS[name]
                portData = portMeta.ConvertToDict()
                portData['name'] = name
                portData['tip'] = portData['tip'] or port.GetPortMeta().tip
                portData['canConnectNodeTypes'] = portData['canConnectNodeTypes'] or port.GetPortMeta().canConnectNodeTypes
                if portData['limitedConnectCount'] == -1:
                    portData['limitedConnectCount'] = port.GetPortMeta().limitedConnectCount
            else:
                text = self.INPUT_PORT_TEXT_MAP.get(name, None)
                portMeta = port.GetPortMeta()
                portData = portMeta.ConvertToDict()
                if text is not None:
                    portData['text'] = text
            inputPortDataList.append(portData)

        outputPortDataList = []
        for port in nodeCls.OUTPUT_PORTS:
            name = port.GetName()
            if self.OUTPUT_PORTS and name in self.OUTPUT_PORTS:
                portMeta = self.OUTPUT_PORTS[name]
                portData = portMeta.ConvertToDict()
                portData['name'] = name
                portData['tip'] = portData['tip'] or port.GetPortMeta().tip
                portData['canConnectNodeTypes'] = portData['canConnectNodeTypes'] or port.GetPortMeta().canConnectNodeTypes
                if portData['limitedConnectCount'] == -1:
                    portData['limitedConnectCount'] = port.GetPortMeta().limitedConnectCount
            else:
                text = self.OUTPUT_PORT_TEXT_MAP.get(port.GetName(), None)
                portMeta = port.GetPortMeta()
                portData = portMeta.ConvertToDict()
                if text is not None:
                    portData['text'] = text
            outputPortDataList.append(portData)

        nodeTypeName = nodeCls.__name__
        nodeClassMeta = ClassMetaManager.GetClassMeta(nodeTypeName)
        node = nodeCls()
        initData = nodeClassMeta.SerializeData(node)
        InitObject(node, nodeClassMeta, initData)
        data = nodeClassMeta.SerializeData(node)
        data['Type'] = nodeTypeName
        editorMeta = nodeClassMeta.GetEditorMeta()
        editorMeta.children['Type'] = EditorMeta(text='\xe7\xb1\xbb\xe5\x9e\x8b', editable=False)
        NodeMetaCreator = self.NODE_META_CREATOR_MAP[nodeCls.NODE_META_TYPE]
        m = NodeMetaCreator(nodeType=nodeTypeName, nodeText=self.NODE_TEXT + self.NODE_USE_RANGE_TEXT_MAP[self.NODE_USE_RANGE], nodeUseRange=self.NODE_USE_RANGE, nodeConnectRange=self.NODE_SUPPORTED_CONNECT_RANGE.get(self.NODE_USE_RANGE, []), nodeTips=self.NODE_TIPS, nodeDoc=self.NODE_DOC, inputPortDataList=inputPortDataList, outputPortDataList=outputPortDataList, nodeEditorMeta=editorMeta, defaultNodeData=data, normalStateColor=self.NORMAL_STATE_COLOR, comment=self.NODE_COMMENT, semantics=self.SEMANTICS, editorNodeCls=self.EDITOR_NODE_CLS, nodeFlags=nodeCls.NODE_FLAGS, replaceNodeTypes=self.REPLACE_NODE_TYPES)
        if self.NODE_CATEGORY is not None:
            m.category = self.NODE_CATEGORY
        return m

    def GetSelfEditorMeta(self):
        inputPortDataList = []
        for name, portMeta in self.INPUT_PORTS.items():
            portMeta.name = name
            inputPortDataList.append(portMeta.ConvertToDict())

        outputPortDataList = []
        for name, portMeta in self.OUTPUT_PORTS.items():
            portMeta.name = name
            outputPortDataList.append(portMeta.ConvertToDict())

        nodeTypeName = self.CLASS_NAME
        nodeClassMeta = ClassMetaManager.GetClassMeta(nodeTypeName)
        data = nodeClassMeta.SerializeDataOnlyMeta()
        data['Type'] = nodeTypeName
        editorMeta = nodeClassMeta.GetEditorMeta()
        editorMeta.children['Type'] = EditorMeta(text='\xe7\xb1\xbb\xe5\x9e\x8b', editable=False)
        NodeMetaCreator = self.NODE_META_CREATOR_MAP[self.NODE_META_TYPE]
        m = NodeMetaCreator(nodeType=nodeTypeName, nodeText=self.NODE_TEXT + self.NODE_USE_RANGE_TEXT_MAP[self.NODE_USE_RANGE], nodeUseRange=self.NODE_USE_RANGE, nodeConnectRange=self.NODE_SUPPORTED_CONNECT_RANGE.get(self.NODE_USE_RANGE, []), nodeTips=self.NODE_TIPS, nodeDoc=self.NODE_DOC, inputPortDataList=inputPortDataList, outputPortDataList=outputPortDataList, nodeEditorMeta=editorMeta, defaultNodeData=data, comment=self.NODE_COMMENT, semantics=self.SEMANTICS, editorNodeCls=self.EDITOR_NODE_CLS, nodeFlags=self.NODE_FLAGS, replaceNodeTypes=self.REPLACE_NODE_TYPES)
        if self.NODE_CATEGORY is not None:
            m.category = self.NODE_CATEGORY
        return m

    def SerializeDataOnlyMeta(self):
        props = {}
        props.update(self.GetAllProperties())
        props.update(self.EDITOR_ATTRIBUTES)
        r = {}
        for key, value in props.items():
            o = value.GetDefault()
            n = value
            r[key] = n.SerializeData(o)

        r['Type'] = self.className
        return r
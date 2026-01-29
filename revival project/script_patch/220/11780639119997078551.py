# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/StorylineMeta.py
from . import StorylineConst

class DisplayPolicy(object):
    NEVER = 0
    CONNECT = 1
    ALWAYS = 2


class NodePort(object):
    PORT_TYPE = 'Unknown'
    DISPLAY_POLICY = 0

    def __init__(self, name='NodePort', text='unknown', optional=False, portType=None, policy=None, extAttrs=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(NodePort, self).__init__()
        self.portType = portType or self.PORT_TYPE
        self.name = name
        self.text = text
        self.tip = tip
        self.limitedConnectCount = limitedConnectCount
        self.canConnectNodeTypes = canConnectNodeTypes
        self.optional = optional
        self.policy = policy or self.DISPLAY_POLICY
        self.extAttrs = extAttrs or {}

    def ConvertToDict(self):
        r = {'portType': self.portType,
           'name': self.name,
           'text': self.text,
           'tip': self.tip,
           'limitedConnectCount': self.limitedConnectCount,
           'canConnectNodeTypes': self.canConnectNodeTypes,
           'optional': self.optional,
           'policy': self.policy,
           'extAttrs': self.extAttrs
           }
        return r


class EntityPort(NodePort):
    PORT_TYPE = 'Entity'

    def __init__(self, name='EntityPort', text='entity', entityType=None, optional=False, allowedComponents=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(EntityPort, self).__init__(name, text, optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes)
        self.entityType = entityType
        self.allowedComponents = allowedComponents

    def ConvertToDict(self):
        r = super(EntityPort, self).ConvertToDict()
        r['entityType'] = self.entityType
        r['allowedComponents'] = self.allowedComponents
        return r


class EntitiesPort(EntityPort):
    PORT_TYPE = 'EntityArray'


class FloatPort(NodePort):
    PORT_TYPE = 'Float'


class IntPort(NodePort):
    PORT_TYPE = 'Int'


class BoolPort(NodePort):
    PORT_TYPE = 'Bool'


class StrPort(NodePort):
    PORT_TYPE = 'Str'


class Vector3Port(NodePort):
    PORT_TYPE = 'Vector3'


class AnyPort(NodePort):
    PORT_TYPE = 'Any'


class MultiTypesPort(NodePort):
    PORT_TYPE = 'MultiTypes'

    def __init__(self, name='NodePort', text='unknown', optional=False, supportedTypes=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(MultiTypesPort, self).__init__(name, text, optional=optional, extAttrs={'supportedTypes': supportedTypes}, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes)


class StorylineNodeMeta(object):
    META_TYPE = 'Unknown'
    CATEGORY = 'ActionNode'

    def __init__(self, nodeType, nodeText, nodeUseRange, nodeConnectRange, nodeTips, nodeDoc, inputPortDataList, outputPortDataList, nodeEditorMeta, defaultNodeData, normalStateColor=StorylineConst.S_NODE_NORMAL_TYPE_COLOR, comment='', semantics='', editorNodeCls=None, nodeFlags=0, replaceNodeTypes=None):
        super(StorylineNodeMeta, self).__init__()
        self.nodeType = nodeType
        self.nodeText = nodeText
        self.nodeUseRange = nodeUseRange
        self.nodeConnectRange = nodeConnectRange
        self.nodeTips = nodeTips
        self.nodeDoc = nodeDoc
        self.inputPortDataList = inputPortDataList
        self.outputPortDataList = outputPortDataList
        self.nodeEditorMeta = nodeEditorMeta
        self.defaultNodeData = defaultNodeData
        self.category = self.CATEGORY
        self.normalStateColor = normalStateColor
        self.comment = comment
        self.semantics = semantics
        self.editorNodeCls = editorNodeCls
        self.nodeFlags = nodeFlags
        self.replaceNodeTypes = replaceNodeTypes

    def ConvertToDict(self):
        r = {'metaType': self.META_TYPE,
           'category': self.category,
           'nodeType': self.nodeType,
           'nodeName': self.nodeText,
           'nodeUseRange': self.nodeUseRange,
           'nodeConnectRange': self.nodeConnectRange,
           'tips': self.nodeTips,
           'doc': self.nodeDoc,
           'inputs': self.inputPortDataList,
           'outputs': self.outputPortDataList,
           'default': self.defaultNodeData,
           'normalStateColor': self.normalStateColor,
           'comment': self.comment,
           'semantics': self.semantics,
           'editorNodeCls': self.editorNodeCls,
           'nodeFlags': self.nodeFlags,
           'replaceNodeTypes': self.replaceNodeTypes
           }
        if type(self.nodeEditorMeta) is dict:
            r['data'] = self.nodeEditorMeta
        else:
            r['data'] = self.nodeEditorMeta.ConvertToDict()
        return r


class ActionNodeMeta(StorylineNodeMeta):
    META_TYPE = 'Action'
    CATEGORY = 'ActionNode'


class EventNodeMeta(StorylineNodeMeta):
    META_TYPE = 'Event'
    CATEGORY = 'EventNode'


class ParameterNodeMeta(StorylineNodeMeta):
    META_TYPE = 'Parameter'
    CATEGORY = 'ParameterNode'
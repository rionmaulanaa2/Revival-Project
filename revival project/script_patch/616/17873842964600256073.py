# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/GalaxyPlugin/GalaxyHelper.py
from ... import iteritems
from ...Meta import ClassMetaManager, TypeMeta
from ...Storyline import NodeManager

class GraphUpdaterBase(object):
    REPLACE_NODE_TYPE = {}
    UPDATE_NODE_FUNCS = {}

    def RefreshNodeData(self, data):
        nodeType = data['Type']
        node = NodeManager.CreateNode(nodeType)
        nodeClassMeta = ClassMetaManager.GetClassMeta(nodeType)
        if not nodeClassMeta:
            return data
        TypeMeta.InitObject(node, nodeClassMeta, data)
        data = nodeClassMeta.SerializeData(node)
        return data

    def UpdateNodeData(self, nodeData):
        nodeType = nodeData['Type']
        if nodeType in ('GraphNode', 'CollapsedGraphNode'):
            nodeData['Data'] = self.UpgradeGraphData(nodeData['Data'])
        elif nodeType in self.REPLACE_NODE_TYPE:
            nodeData['Type'] = nodeData['Data']['Type'] = self.REPLACE_NODE_TYPE[nodeType]
        elif nodeType in self.UPDATE_NODE_FUNCS:
            func = self.UPDATE_NODE_FUNCS[nodeType]
            if isinstance(func, str):
                func = getattr(self, func)
            nodeData = func(nodeData)
        data = nodeData.get('Data', None)
        if data and 'Type' in data:
            nodeData['Data'] = self.RefreshNodeData(data)
        return nodeData

    def UpgradeGraphData(self, graphData):
        if not graphData:
            return graphData
        nodeData = graphData.get('nodeData', {})
        for nodeID, node in iteritems(nodeData):
            newData = self.UpdateNodeData(node)
            if newData:
                nodeData[nodeID] = newData

        if 'groupData' in graphData and isinstance(graphData['groupData'], list):
            graphData['groupData'] = {}
        return graphData
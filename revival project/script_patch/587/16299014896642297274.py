# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/GalaxyPlugin/GalaxyPluginClient.py
from ..EditorPlugin import EditorPluginClient
from ...Meta import ClassMetaManager
from ...Meta.TypeMeta import UpdateObject, AddEntityProperty, DelEntityProperty, ModifyEntityProperty
from ...Storyline import NodeManager
from ...Storyline.StorylineConst import NodeVariableSelectorType
from ...SunshineClient import Response
UUID = '98efd553-30b6-4efd-862c-9810e0bdf65a'

class GalaxyPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Galaxy'
    API_VERSION = '2.6.38'

    def StartSimulation(self, simulationFile, searchPath, exData=None):
        raise NotImplementedError

    def StartSimulationMultiFiles(self, filenames, workspace, simulationTempPath, exData=None):
        raise NotImplementedError

    def StopSimulation(self):
        raise NotImplementedError

    def SendSignals(self, signals):
        raise NotImplementedError

    def GetSimulationTypes(self):
        raise NotImplementedError

    def SetSimulationType(self, sType):
        raise NotImplementedError

    def GetGraphNodeMetas(self):
        raise NotImplementedError

    def GetEntityNodeTypes(self):
        raise NotImplementedError

    def GetGraphUpdater(self):
        from .GalaxyHelper import GraphUpdaterBase
        return GraphUpdaterBase()

    def GetCategoryNameMap(self):
        return {}

    def UpdateNodesDynamicMeta(self, nodes):
        dynamicMetas = {}
        for nodeID, nodeData in nodes.items():
            nodeType = nodeData.get('Type', None)
            node = NodeManager.CreateNode(nodeType)
            meta = ClassMetaManager.GetClassMeta(nodeType)
            if meta is None or node is None:
                continue
            UpdateObject(node, meta, nodeData)
            dynamicMeta = meta.GetDynamicEditorMeta(node)
            if dynamicMeta is None:
                dynamicMeta = {}
            dynamicMetas[nodeID] = dynamicMeta

        self.GetServer().UpdateNodesDynamicMeta(dynamicMetas)
        return

    def GetStorylineMetaData(self, filename, eventGraphName='Graph', exData=None):
        return None

    def ModifyStorylineMetaData(self, filename, eventGraphName, data, propertyStr, value, exData=None):
        cls = self.GetStorylineMetaDataCls(filename, eventGraphName, exData)
        if not cls:
            return data
        obj = cls(data)
        meta = ClassMetaManager.GetClassMeta(cls.__name__)
        parts = propertyStr.split('/')
        opt = parts.pop(0)
        if opt == 'add':
            if isinstance(value, dict):
                for key in value:
                    AddEntityProperty(obj, meta, parts, value[key], key, True)

            elif isinstance(value, (tuple, list)):
                for val in value:
                    if isinstance(val, (tuple, list)):
                        AddEntityProperty(obj, meta, parts, val[1], val[0])
                    else:
                        AddEntityProperty(obj, meta, parts, val)

            else:
                AddEntityProperty(obj, meta, parts, value)
        elif opt == 'del':
            DelEntityProperty(obj, meta, parts)
        elif opt == 'mod':
            ModifyEntityProperty(obj, meta, parts, value)
        return obj.Serialize()

    def UpdateStorylineMetaDataDynamicMeta(self, filename, eventGraphName, data, exData):
        cls = self.GetStorylineMetaDataCls(filename, eventGraphName, exData)
        if cls:
            obj = cls(data)
            return obj.GetDynamicEditorMeta()
        else:
            return None
            return None

    def GetStorylineMetaDataCls(self, filename, eventGraphName='Graph', exData=None):
        return None

    def ModifyNodeData(self, nodeData, propertyStr, value):
        parts = propertyStr.split('/')
        opt = parts.pop(0)
        if opt != 'add':
            return
        else:
            nodeType = nodeData.get('Type', None)
            node = NodeManager.CreateNode(nodeType)
            meta = ClassMetaManager.GetClassMeta(nodeType)
            if meta is None or node is None:
                return nodeData
            UpdateObject(node, meta, nodeData)
            node.EditorOnlyModifyNodeData(propertyStr, value)
            return meta.SerializeData(node)

    def ModifyNodeVariableSelectorData(self, nodeID, portName, varSelectorType=NodeVariableSelectorType.INPUT_PORT, data=None):
        pass

    def OnOptionalPortVisibilityChanged(self, isVisible, nodeID, portName, isInput, exData):
        pass

    def PressNodeButton(self, nodeID, propertyStr, value):
        pass

    def OnNodeOperation(self, op, nodeID):
        pass

    def GetNodeDataCallback(self, nodeID, nodeData):
        pass

    def GetStorylineMetaDataCallback(self, filename, eventGraphName, metaData):
        pass

    def GetDocIDByNodeIDCallback(self, nodeID, docID):
        pass

    def GetAllVariablesByDocIDCallback(self, docID, variables):
        pass

    def OnLineOperation(self, op, lineData):
        pass

    def GetGraphColor(self):
        return {}

    def GetGameMenu(self):
        data = {}
        return data

    def onGameMenuCommand(self, command):
        return ''

    def SetDebugFileList(self, fileList):
        from ...Storyline.Storyline import StorylineContextBase
        StorylineContextBase.SetDebugFileList(fileList)

    def PostProcessFileData(self, filename, fileData):
        return (
         filename, fileData, '')

    def Export(self, srcFile, dstFile):
        import os
        import re
        import json
        from ...Storyline.Storyline import StorylineContextBase
        from ...Storyline import StorylineSystem
        import six
        srcFile = six.ensure_str(srcFile)
        dstFile = six.ensure_str(dstFile)
        with open(srcFile, 'r') as f:
            data = json.loads(f.read())
            directory, name = os.path.split(srcFile)
            nameWithoutPostfix = name[:-4] if name.endswith('.ets') else name

            def _mergeSubGraph(_path, _data):
                with open(_path) as fp:
                    subData = json.load(fp)
                    _data['Storyline']['nodeData'].update(subData['Storyline']['nodeData'])
                    _data['Storyline']['groupData'].update(subData['Storyline']['groupData'])
                    _data['Storyline']['lineData'].extend(subData['Storyline']['lineData'])
                    _data['Variables'].update(subData.get('Variables', {}))
                    _data['Signals'].update(subData.get('Signals', {}))
                    _data['Entities'].update(subData.get('Entities', {}))

            if 'SubGraphNames' in data:
                for subGraphName in data['SubGraphNames']:
                    _subGraphFilePath = os.path.join(directory, '%s.%s.%s' % (nameWithoutPostfix, subGraphName, 'ets'))
                    if not os.path.exists(_subGraphFilePath):
                        continue
                    _mergeSubGraph(_subGraphFilePath, data)

            else:
                for file in os.listdir(directory):
                    filename = os.path.join(directory, file)
                    if os.path.isfile(filename):
                        match = re.match('%s\\.(.+)\\.ets' % re.escape(nameWithoutPostfix), file)
                        if match:
                            _mergeSubGraph(filename, data)

            data['Storyline'] = self.GetGraphUpdater().UpgradeGraphData(data.get('Storyline', {}))
            context = StorylineContextBase()
            storyline = StorylineSystem.CreateStoryline(context)
            storyline.LoadFromDict(data)
            exportData = storyline.ExportToDict()
            with open(dstFile, 'w') as w:
                w.write(json.dumps(exportData, sort_keys=True, indent=4, separators=(',',
                                                                                     ':')))

    def MoveEntitiesAroundScreenPos(self, entities, screenPos):
        pass

    def Register(self):
        methodMap = super(GalaxyPluginClient, self).Register()
        wrapper = _HandlerWrapper(self)
        methodMap.update({(UUID, 'StartSimulation'): self.StartSimulation,
           (UUID, 'StartSimulationMultiFiles'): self.StartSimulationMultiFiles,
           (UUID, 'StopSimulation'): wrapper.StopSimulation,
           (UUID, 'SendSignals'): self.SendSignals,
           (UUID, 'GetSimulationTypes'): wrapper.GetSimulationTypes,
           (UUID, 'SetSimulationType'): self.SetSimulationType,
           (UUID, 'GetGraphNodeMetas'): wrapper.GetGraphNodeMetas,
           (UUID, 'GetEntityNodeTypes'): wrapper.GetEntityNodeTypes,
           (UUID, 'GetCategoryNameMap'): wrapper.GetCategoryNameMap,
           (UUID, 'UpgradeGraphData'): wrapper.UpgradeGraphData,
           (UUID, 'UpdateNodesDynamicMeta'): self.UpdateNodesDynamicMeta,
           (UUID, 'GetStorylineMetaData'): wrapper.GetStorylineMetaData,
           (UUID, 'ModifyStorylineMetaData'): wrapper.ModifyStorylineMetaData,
           (UUID, 'UpdateStorylineMetaDataDynamicMeta'): wrapper.UpdateStorylineMetaDataDynamicMeta,
           (UUID, 'ModifyNodeData'): wrapper.ModifyNodeData,
           (UUID, 'GetDocIDByNodeIDCallback'): self.GetDocIDByNodeIDCallback,
           (UUID, 'GetAllVariablesByDocIDCallback'): self.GetAllVariablesByDocIDCallback,
           (UUID, 'OnLineOperation'): self.OnLineOperation,
           (UUID, 'ModifyNodeVariableSelectorData'): self.ModifyNodeVariableSelectorData,
           (UUID, 'OnOptionalPortVisibilityChanged'): self.OnOptionalPortVisibilityChanged,
           (UUID, 'PressNodeButton'): self.PressNodeButton,
           (UUID, 'OnNodeOperation'): self.OnNodeOperation,
           (UUID, 'GetNodeDataCallback'): self.GetNodeDataCallback,
           (UUID, 'GetStorylineMetaDataCallback'): self.GetStorylineMetaDataCallback,
           (UUID, 'SetWorkspace'): wrapper.SetWorkspace,
           (UUID, 'SetDebugFileList'): self.SetDebugFileList,
           (UUID, 'GetGraphColor'): wrapper.GetGraphColor,
           (UUID, 'GetGameMenu'): wrapper.GetGameMenu,
           (UUID, 'onGameMenuCommand'): self.onGameMenuCommand,
           (UUID, 'PostProcessFileData'): wrapper.PostProcessFileData,
           (UUID, 'Export'): self.Export,
           (UUID, 'MoveEntitiesAroundScreenPos'): self.MoveEntitiesAroundScreenPos
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin

    def StopSimulation(self):
        self.plugin.StopSimulation()

    def GetSimulationTypes(self):
        data = self.plugin.GetSimulationTypes()
        if data:
            return Response(UUID, 'SetSimulationTypes', data)

    def GetGraphNodeMetas(self):
        data = self.plugin.GetGraphNodeMetas()
        if type(data) is list:
            data = dict(((a.nodeType, a.ConvertToDict()) for a in data))
        return Response(UUID, 'SetGraphNodeMetas', data)

    def GetStorylineMetaData(self, filename, eventGraphName='Graph', exData=None):
        data = self.plugin.GetStorylineMetaData(filename, eventGraphName, exData)
        return Response(UUID, 'SetStorylineMetaData', filename, eventGraphName, data)

    def ModifyStorylineMetaData(self, filename, eventGraphName, data, propertyStr, value, exData=None):
        newData = self.plugin.ModifyStorylineMetaData(filename, eventGraphName, data, propertyStr, value, exData)
        if newData and data != newData:
            return Response(UUID, 'SetModifiedStorylineMetaData', filename, eventGraphName, newData)

    def UpdateStorylineMetaDataDynamicMeta(self, filename, eventGraphName, data, exData):
        dynamicMeta = self.plugin.UpdateStorylineMetaDataDynamicMeta(filename, eventGraphName, data, exData)
        return Response(UUID, 'UpdateStorylineMetaDataDynamicMeta', filename, eventGraphName, dynamicMeta)

    def GetEntityNodeTypes(self):
        data = self.plugin.GetEntityNodeTypes()
        return Response(UUID, 'SetEntityNodeType', data)

    def GetCategoryNameMap(self):
        data = self.plugin.GetCategoryNameMap()
        return Response(UUID, 'SetCategoryNameMap', data)

    def UpgradeGraphData(self, data):
        data = self.plugin.GetGraphUpdater().UpgradeGraphData(data)
        return Response(UUID, 'SetUpgradeGraphData', data)

    def ModifyNodeData(self, nodeID, data, propertyStr, value, version=''):
        newData = self.plugin.ModifyNodeData(data, propertyStr, value)
        if newData and data != newData:
            return Response(UUID, 'SetModifiedNodeData', nodeID, newData, version)

    @staticmethod
    def SetWorkspace(workspace):
        from ...Storyline.StorylineSystem import GetRepositoryMgr
        GetRepositoryMgr().SetWorkspace(workspace)

    def GetGraphColor(self):
        data = self.plugin.GetGraphColor()
        return Response(UUID, 'SetGraphColor', data)

    def GetGameMenu(self):
        data = self.plugin.GetGameMenu()
        return Response(UUID, 'SetGameMenu', data)

    def PostProcessFileData(self, filename, fileData):
        result = self.plugin.PostProcessFileData(filename, fileData)
        return {'filename': result[0],'fileData': result[1],'error': result[2] if len(result) >= 3 else ''}
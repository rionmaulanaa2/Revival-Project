# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/RainbowPluginClient.py
from collections import OrderedDict
from ..EditorPlugin import EditorPluginClient
from ...SunshineClient import Response
from ...Meta.MetaUtils import iteritems
from ...Meta.ClassMetaManager import GetClassMeta
import json
UUID = '504492a8-6d6d-47a8-83e1-02f0d1c9fadb'

class RainbowPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Rainbow'
    API_VERSION = '2.5.3'

    def SetEditMode(self, modeId):
        raise NotImplementedError

    def GetSubEditModeData(self):
        return []

    def SetSubEditMode(self, mode):
        raise NotImplementedError

    def SetEntityOpMode(self, modeID):
        raise NotImplementedError

    def SetGizmoMode(self, mode):
        raise NotImplementedError

    def GetResourceData(self):
        raise NotImplementedError

    def GetEditCategories(self):
        raise NotImplementedError

    def GetEntityTypeName(self, key):
        raise NotImplementedError

    def GetCreateEntityData(self):
        raise NotImplementedError

    def GetEntityData(self, key):
        raise NotImplementedError

    def GetEntityDynamicEditorMeta(self, key):
        pass

    def GetEntityEditComponent(self, key):
        raise NotImplementedError

    def GetAvailableEntities(self):
        raise NotImplementedError

    def ModifyEntityProperty(self, key, pathParts, val):
        raise NotImplementedError

    def PreviewEntityProperty(self, key, pathParts, val, status):
        self.ModifyEntityProperty(key, pathParts, val)

    def SetEntityParent(self, key, parentKey):
        pass

    def AddEntityProperty(self, key, pathParts, vals):
        raise NotImplementedError

    def DelEntityProperty(self, key, pathParts):
        pass

    def MoveEntityProperty(self, key, srcPathParts, dstPathParts):
        pass

    def OperateEntityProperty(self, key, pathParts, args=None):
        raise NotImplementedError

    def CreateEntity(self, key, data, position=None, exData=None):
        raise NotImplementedError

    def UpdateEntity(self, key, data):
        raise NotImplementedError

    def SetEditEntity(self, key):
        raise NotImplementedError

    def FocusEntity(self, key):
        raise NotImplementedError

    def FocusPosition(self, position):
        raise NotImplementedError

    def ClickEntityProperty(self, key, propertyStr):
        pass

    def DestroyEntity(self, key):
        raise NotImplementedError

    def UpdateEditData(self, data):
        raise NotImplementedError

    def SetEntityData(self, key, data):
        raise NotImplementedError

    def EnterPointSelectionMode(self):
        raise NotImplementedError

    def GetPrefabData(self):
        raise NotImplementedError

    def MovePrefabToDirectory(self, prefabIds, targetDir):
        raise NotImplementedError

    def CreatePrefabDirectory(self, dirName, path):
        raise NotImplementedError

    def UpdatePrefabData(self, pyExpr, operation='modify'):
        raise NotImplementedError

    def GetExportTemplates(self):
        raise NotImplementedError

    def GetAllTypeEditorMetas(self):
        return {}

    def ReLoadAllTypeEditorMetas(self):
        pass

    def SetDocumentInfo(self, info):
        pass

    def ModifyEnum(self, enumKey, enumData):
        pass

    def AddEnum(self, enumKey, enumData):
        pass

    def DelEnum(self, enumKey):
        pass

    def GetCreateEmptyEntityData(self):
        pass

    def isEntityTransformPath(self, path):
        pass

    def UpdateEntityTransform(self, entityID, path):
        pass

    def GetScriptableObjectMetaConfig(self):
        pass

    def ScriptableObjectGenCode(self, dataPath, codePath, hotFix=False):
        pass

    def GetThumbnail(self, resPath, width, height):
        pass

    def CancelGettingThumbnail(self):
        pass

    def InvalidateThumbnails(self, resPaths):
        pass

    def Register(self):
        methodMap = super(RainbowPluginClient, self).Register()
        wrapper = _HandlerWrapper(self)
        methodMap.update({(UUID, 'SetEditMode'): self.SetEditMode,
           (UUID, 'SetEntityOpMode'): self.SetEntityOpMode,
           (UUID, 'SetGizmoMode'): self.SetGizmoMode,
           (UUID, 'GetSubEditModeData'): wrapper.GetSubEditModeData,
           (UUID, 'SetSubEditMode'): self.SetSubEditMode,
           (UUID, 'GetAllTypePropertyAttributes'): wrapper.GetAllTypeEditorMetas,
           (UUID, 'GetCreateEntityData'): wrapper.GetCreateEntityData,
           (UUID, 'GetEditEnums'): wrapper.GetEditEnums,
           (UUID, 'GetComponentMetas'): wrapper.GetComponentMetas,
           (UUID, 'GetEditCategories'): wrapper.GetEditCategories,
           (UUID, 'GetEntityData'): wrapper.GetEntityData,
           (UUID, 'GetAvailableEntities'): wrapper.GetAvailableEntities,
           (UUID, 'ModifyEditEntity'): wrapper.ModifyEditEntity,
           (UUID, 'PreviewEntityProperty'): self.PreviewEntityProperty,
           (UUID, 'OperateEditEntity'): wrapper.OperateEditEntity,
           (UUID, 'SetEditEntity'): self.SetEditEntity,
           (UUID, 'FocusEntity'): self.FocusEntity,
           (UUID, 'FocusPosition'): self.FocusPosition,
           (UUID, 'ClickEntityProperty'): self.ClickEntityProperty,
           (UUID, 'CreateEntity'): self.CreateEntity,
           (UUID, 'CreateEntities'): wrapper.CreateEntities,
           (UUID, 'DestroyEntity'): wrapper.DestroyEntity,
           (UUID, 'DestroyEntities'): wrapper.DestroyEntities,
           (UUID, 'UpdateEntity'): wrapper.UpdateEntity,
           (UUID, 'UpdateEntities'): wrapper.UpdateEntities,
           (UUID, 'GetResourceData'): wrapper.GetResourceData,
           (UUID, 'GetPrefabData'): wrapper.GetPrefabData,
           (UUID, 'EnterPointSelectionMode'): self.EnterPointSelectionMode,
           (UUID, 'UpdatePrefabData'): self.UpdatePrefabData,
           (UUID, 'GetExportTemplates'): wrapper.GetExportTemplates,
           (UUID, 'UpdateEditData'): self.UpdateEditData,
           (UUID, 'SetEntityData'): self.SetEntityData,
           (UUID, 'SetEntityParent'): self.SetEntityParent,
           (UUID, 'SetDocumentInfo'): self.SetDocumentInfo,
           (UUID, 'AddEnum'): wrapper.AddEnum,
           (UUID, 'DelEnum'): wrapper.DelEnum,
           (UUID, 'ModifyEnum'): wrapper.ModifyEnum,
           (UUID, 'GetBlackboardAssets'): wrapper.GetBlackboardAssets,
           (UUID, 'CallbackEntityProperty'): wrapper.CallbackEntityProperty,
           (UUID, 'GetCreateEmptyEntityData'): wrapper.GetCreateEmptyEntityData,
           (UUID, 'GetScriptableObjectMetaConfig'): wrapper.GetScriptableObjectMetaConfig,
           (UUID, 'ScriptableObjectGenCode'): self.ScriptableObjectGenCode,
           (UUID, 'GetThumbnail'): self.GetThumbnail,
           (UUID, 'CancelGettingThumbnail'): self.CancelGettingThumbnail,
           (UUID, 'InvalidateThumbnails'): self.InvalidateThumbnails,
           (UUID, 'MovePrefabToDirectory'): wrapper.MovePrefabToDirectory,
           (UUID, 'CreatePrefabDirectory'): self.CreatePrefabDirectory
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._cachedDynamicMeta = {}

    def GetSubEditModeData(self):
        data = [ {'Mode': m,'ActionName': n,'Text': t} for m, n, t in self.plugin.GetSubEditModeData() ]
        if data:
            return Response(UUID, 'SetSubEditModeData', data)

    def GetAllTypeEditorMetas(self):
        self.plugin.ReLoadAllTypeEditorMetas()
        from ...Meta import ClassMetaManager
        r = []
        metas = ClassMetaManager.GetAllClassMetas()
        for typeName, clsMeta in iteritems(metas):
            meta = clsMeta.GetEditorMeta()
            if hasattr(meta, 'ConvertToDict'):
                meta = meta.ConvertToDict()
            r.append(Response(UUID, 'RegisterTypePropertyAttribute', typeName, meta))

        data = self.plugin.GetAllTypeEditorMetas()
        for typeName, meta in iteritems(data):
            if hasattr(meta, 'ConvertToDict'):
                meta = meta.ConvertToDict()
            r.append(Response(UUID, 'RegisterTypePropertyAttribute', typeName, meta))

        return r

    def GetCreateEntityData(self):
        data = [ {'ActionName': n,'EntityType': et,'Text': t,'PrefabData': p,'EditGroup': eg} for n, et, t, p, eg in self.plugin.GetCreateEntityData()
               ]
        if data:
            for item in data:
                pass

            return Response(UUID, 'SetCreateEntityData', data)

    def GetEntityData(self, key, seqID=None):
        data = self.plugin.GetEntityData(key)
        if not data:
            return
        else:
            if not isinstance(data.get('Type', None), str):
                typeName = self.plugin.GetEntityTypeName(key)
                if typeName is None:
                    typeName = '(Dynamic)'
                data['Type'] = typeName
            if 'Edit' not in data:
                editComponent = self.plugin.GetEntityEditComponent(key)
                if editComponent is not None:
                    data['Edit'] = editComponent.ConvertToDict()
            if '__dynamic_meta__' not in data:
                dynamicMeta = self.plugin.GetEntityDynamicEditorMeta(key)
                if dynamicMeta != self._cachedDynamicMeta.get(key):
                    self._cachedDynamicMeta[key] = dynamicMeta
                    data['__dynamic_meta__'] = dynamicMeta
            if '__exData__' in data:
                data.pop('__exData__')
            return Response(UUID, 'UpdateEntityData', key, data, seqID)

    def GetAvailableEntities(self):
        keys = self.plugin.GetAvailableEntities()
        if not keys:
            return
        else:
            r = []
            for key in keys:
                data = self.plugin.GetEntityData(key)
                typeName = self.plugin.GetEntityTypeName(key)
                data['Type'] = typeName
                if 'Edit' not in data:
                    editComponent = self.plugin.GetEntityEditComponent(key)
                    if editComponent is not None:
                        data['Edit'] = editComponent.ConvertToDict()
                if typeName is None:
                    typeName = '(Dynamic)'
                    data['Type'] = typeName
                if '__dynamic_meta__' not in data:
                    dynamicMeta = self.plugin.GetEntityDynamicEditorMeta(key)
                    self._cachedDynamicMeta[key] = dynamicMeta
                    data['__dynamic_meta__'] = dynamicMeta
                r.append(Response(UUID, 'AddEntity', key, data))

            return r

    def GetEditEnums(self):
        from ...Meta.EnumMeta import EnumMetas
        data = OrderedDict(((k, v.Serialize()) for k, v in iteritems(EnumMetas)))
        return Response(UUID, 'SetEditEnums', data)

    def GetComponentMetas(self):
        from ...Meta.ComponentMeta import ComponentMetas
        data = OrderedDict(((k, v.Serialize()) for k, v in iteritems(ComponentMetas)))
        return Response(UUID, 'SetComponentMetas', data)

    def ModifyEditEntity(self, key, path, val):
        parts = list(filter(None, path.split('/')))
        opt = parts.pop(0)
        if opt == 'mod':
            propertyStr = '/'.join(parts)
            if parts[0] == 'Edit':
                editComponent = self.plugin.GetEntityEditComponent(key)
                if editComponent:
                    editComponent.ModifyProperty(parts[1], val)
                    if self.plugin.isEntityTransformPath(propertyStr) or propertyStr == 'Edit/parent':
                        self.plugin.UpdateEntityTransform(key, propertyStr)
                    return Response(UUID, 'ModifyEntityOver')
            self.plugin.ModifyEntityProperty(key, parts, val)
            if self.plugin.isEntityTransformPath(propertyStr) or propertyStr == 'Edit/parent':
                self.plugin.UpdateEntityTransform(key, propertyStr)
        elif opt == 'add':
            self.plugin.AddEntityProperty(key, parts, val)
        elif opt == 'del':
            self.plugin.DelEntityProperty(key, parts)
        elif opt == 'move':
            srcPathParts, dstPathParts = list(filter(None, val[0].split('/'))), list(filter(None, val[1].split('/')))
            self.plugin.MoveEntityProperty(key, srcPathParts, dstPathParts)
        return Response(UUID, 'ModifyEntityOver')

    def OperateEditEntity(self, key, path, args):
        parts = path.split('/')
        self.plugin.OperateEntityProperty(key, parts, args)

    def CreateEntities(self, key2Data, key2Pos=None, key2exData=None):
        if key2exData is None:
            key2exData = {}
        if key2Pos is None:
            key2Pos = {}
        for key, data in key2Data.items():
            self.plugin.CreateEntity(key, data, key2Pos.get(key, None), key2exData.get(key, None))

        return

    def DestroyEntities(self, keys):
        for key in keys:
            self.DestroyEntity(key)

    def DestroyEntity(self, key):
        if self.plugin.DestroyEntity(key):
            self.plugin.GetServer().DelEntity(key)

    def UpdateEntities(self, entities):
        for key, data in iteritems(entities):
            self.plugin.UpdateEntity(key, data)
            self.plugin.UpdateEntityTransform(key, '')

        return Response(UUID, 'ModifyEntityOver')

    def UpdateEntity(self, key, data):
        self.plugin.UpdateEntity(key, data)
        self.plugin.UpdateEntityTransform(key, '')
        return Response(UUID, 'ModifyEntityOver')

    def GetResourceData(self):
        resDict = self.plugin.GetResourceData()
        if not resDict:
            return
        r = []
        for resType, resList in iteritems(resDict):
            r.append(Response(UUID, 'SetResourceData', resType, ';'.join(resList)))

        return r

    def GetPrefabData(self):
        prefabData = self.plugin.GetPrefabData()
        return Response(UUID, 'SetPrefabData', prefabData)

    def MovePrefabToDirectory(self, prefabIds, targetDir):
        succeed = self.plugin.MovePrefabToDirectory(prefabIds, targetDir)
        if succeed:
            return Response(UUID, 'MovePrefabToDirectory', prefabIds, targetDir)

    def GetEditCategories(self):
        data = self.plugin.GetEditCategories()
        if data:
            return Response(UUID, 'SetEditCategories', data)

    def GetExportTemplates(self):
        data = self.plugin.GetExportTemplates()
        if data:
            jsonStr = json.dumps(data, sort_keys=True, indent=4)
            return Response(UUID, 'SetExportTemplates', jsonStr)

    def AddEnum(self, enumKey, enumData):
        from ...Meta.EnumMeta import GetEnumMetaByKey, LoadEnum
        LoadEnum(enumKey, enumData)
        self.plugin.AddEnum(enumKey, enumData)
        enum = GetEnumMetaByKey(enumKey)
        if enum:
            return Response(UUID, 'SetEditEnums', {enumKey: enum.Serialize()})

    def ModifyEnum(self, enumKey, enumData):
        from ...Meta.EnumMeta import GetEnumMetaByKey, LoadEnum
        LoadEnum(enumKey, enumData)
        self.plugin.ModifyEnum(enumKey, enumData)
        return Response(UUID, 'SetEditEnums', {enumKey: GetEnumMetaByKey(enumKey).Serialize()})

    def DelEnum(self, enumKey):
        from ...Meta.EnumMeta import DelEnum
        DelEnum(enumKey)
        self.plugin.DelEnum(enumKey)

    def GetBlackboardAssets(self):
        pass

    def CallbackEntityProperty(self, propertyStr, data):
        classMeta = GetClassMeta(self.plugin.GetEntityTypeName(data['uuidList'][0]))
        metaProperty = classMeta.PROPERTIES
        for _propertyStr in propertyStr.split('/'):
            metaProperty = metaProperty[_propertyStr]

        metaPropertyFunc = metaProperty.editorMeta.get(data['callbackType'], '')
        if metaPropertyFunc:
            getattr(classMeta, metaPropertyFunc)(data)

    def GetCreateEmptyEntityData(self):
        data = self.plugin.GetCreateEmptyEntityData()
        if data:
            return Response(UUID, 'SetCreateEmptyEntityData', data)

    def GetScriptableObjectMetaConfig(self):
        config = self.plugin.GetScriptableObjectMetaConfig()
        if config is not None:
            return Response(UUID, 'RegisterScriptableObjectMetaConfig', config)
        else:
            return
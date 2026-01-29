# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/Messiah/MessiahRainbowPluginClient.py
from __future__ import print_function
import math
import sys
import inspect
try:
    from typing import Optional, Dict
except ImportError:
    Optional, Dict = (
     None, None)

import MResource
import MEngine
import MRender
import MType
import MObject
from .....PlatformAPI.Platforms.Messiah import Input
from .....PlatformAPI.Platforms.Messiah import Globals
from .....PlatformAPI.Platforms.Messiah import MessiahUtils
from .....PlatformAPI.EditAPI import GetEngineEditAPI
from .....SunshineRpc.Event import Event
from .....Meta.ClassMetaManager import GetClassMeta
from .....Meta.TypeMeta import UpdateObject, ModifyEntityProperty, AddEntityProperty, DelEntityProperty, MoveEntityProperty, GetObjectMetaByPath, TraverseObjectByPath, BaseClassMeta, PObject
from ....EditorPlugin import sunshine_rpc
from ..RainbowPluginClientBase import *
from ..RainbowEditAPI import RainbowEditAPI
from ..RainbowEntityEditComponent import GetEditComponentClass, RainbowEntityEditComponent
from ..EntityMgr import EntityMgr
from .EntityUtils import GetIEntity, GetEntityTransformName

class RainbowPluginImpl(RainbowPluginClientBase):

    def __init__(self):
        super(RainbowPluginImpl, self).__init__()
        self.entityMgr = EntityMgr()
        self.editAPI = None
        self.selectEntityUUID = None
        self.selectedEntities = set()
        self.customSelectEntities = {}
        self.selectSetting = False
        self.InitEditorTouch()
        self.modeHandlers = {EDITOR_MODE_GAME: GameMode(self),
           EDITOR_MODE_EDIT: EditMode(self)
           }
        self.mode = EDITOR_MODE_GAME
        self.inMoveMode = False
        self.moveTimer = None
        self.inSpecialEditMode = False
        self.specialMode = None
        self.ctrlDown = False
        self.gizmoInfo = 'EntityTranslator'
        self.gizmoMode = 0
        self.createModeMovePt = None
        self.editComponents = {}
        self.editCategories = [
         'Monster', 'NPC', 'Radar', 'Editor', 'Others']
        self.editEntities = {}
        self.entityidToUuid = {}
        self.EventEditEntityChanged = Event()
        self.enableEventEntityCreated = True
        self.enableEventEntityPreDestroy = True
        self._shouldSentInitialEntities = False
        self.entityCache = []
        self._cacheTransforms = {}
        GetEngineEditAPI().RegisterKeyboardListener(self)
        GetEngineEditAPI().RegisterMouseListener(self)
        GetEngineEditAPI().RegisterPlayerAvatarReadyCallback(self._OnPlayerAvatarReady)
        GetEngineEditAPI().RegisterBeforeChangeSceneCallback(self._BeforeSpaceChange)
        GetEngineEditAPI().RegisterSceneChangedCallback(self._OnSpaceChanged)
        return

    def InitSelectionSetting(self):
        mp = MEngine.GetGameplay().Player.Manipulator
        mp.BindEvent('TargetTransformChanged', self._onManipulatorTargetTransformChanged)
        import MConfig
        if MConfig.Platform == 'windows':
            mp.BindEvent('TargetFinishEditTransform', self._onFinishTransform)
        mp.SelectGizmo(self.gizmoInfo)
        for gizmo in ['EntityTranslator', 'EntityRotator', 'EntityScaler']:
            if gizmo in mp.Gizmos:
                mp.Gizmos[gizmo].Size = 0.15

        MRender.SetSelectedColor(0)
        self.selectSetting = True

    def _onManipulatorTargetTransformChanged(self, *_):
        self._onTransformChanged(True, False)

    def _onFinishTransform(self, *_):
        self._onTransformChanged(True, True)

    def _onTransformChanged(self, updateServer=False, undo=False):
        for UUID in self.selectedEntities:
            entity = self.entityMgr.GetEntity(UUID)
            if not entity:
                continue
            transformKey = 'position'
            if self.gizmoInfo == 'EntityTranslator':
                transformKey = 'position'
            elif self.gizmoInfo == 'EntityScaler':
                transformKey = 'scale'
            else:
                transformKey = 'direction'
            if hasattr(entity, transformKey):
                transformValue = getattr(entity, transformKey)
                player = GetEngineEditAPI().GetPlayerAvatar()
                if entity is player:
                    player.server['GM'].GMCommand('#teleport %f %f %f' % transformValue)
                elif not undo:
                    self.UpdateEntityTransform(UUID, transformKey, updateServer, undo)
                else:
                    cacheValues = self._cacheTransforms.get(transformKey, {})
                    if UUID not in cacheValues or cacheValues[UUID] != transformValue:
                        initialValues = None
                        if UUID in cacheValues:
                            initialValues = {UUID: cacheValues[UUID]}
                        self.UpdateEntityTransform(UUID, transformKey, updateServer, undo, initialValues)
                        cacheValues[UUID] = transformValue
                        self._cacheTransforms[transformKey] = cacheValues

        return

    @sunshine_rpc
    def GetServerVar(self, key):

        def _on_resp(v):
            print('>>>get response from game server:', v)

        self.GameServer.GetServerVar(key).on_result(_on_resp)

    @property
    def selectEntity(self):
        return self.entityMgr.GetEntity(self.selectEntityUUID)

    def SetEntityOpMode(self, modeID):
        gizmoInfo = {0: 'EntityTranslator',
           1: 'EntityRotator',
           2: 'EntityScaler'
           }
        if modeID not in gizmoInfo:
            return
        self.gizmoInfo = gizmoInfo[modeID]
        mp = MEngine.GetGameplay().Player.Manipulator
        mp.BindEvent('TargetTransformChanged', self._onManipulatorTargetTransformChanged)
        if GetEngineEditAPI().IsGizmoVisible():
            mp.SelectGizmo(self.gizmoInfo)
        else:
            mp.SelectGizmo('')

    def SetGizmoMode(self, mode):
        if mode != self.gizmoMode:
            mp = MEngine.GetGameplay().Player.Manipulator
            gizmo = mp.Gizmos.get('EntityTranslator', None)
            if hasattr(gizmo, 'SwitchMode'):
                gizmo.SwitchMode()
                self.gizmoMode = mode
        return

    def HasEditEntity(self, entityID):
        if entityID in self.entityidToUuid:
            return self.entityMgr.HasEntity(self.entityidToUuid[entityID])
        else:
            return False

    @sunshine_rpc
    def ShowEntity(self, uuid):
        ent = self.entityMgr.GetEntity(uuid)
        if ent:
            self.editAPI.SetEntityVisible(ent, True)

    @sunshine_rpc
    def HideEntity(self, uuid):
        entity = self.entityMgr.GetEntity(uuid)
        if entity:
            self.editAPI.SetEntityVisible(entity, False)

    def InitEditorTouch(self):
        self.gesture = GetEngineEditAPI().InitEditorTouch(self)

    def EnableEditorTouch--- This code section failed: ---

 217       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'gesture'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    43  'to 43'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'gesture'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    43  'to 43'

 218      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'gesture'
          27  LOAD_ATTR             2  'EnableTrack'
          30  LOAD_FAST             1  'enable'
          33  LOAD_GLOBAL           3  'False'
          36  CALL_FUNCTION_2       2 
          39  POP_TOP          
          40  JUMP_FORWARD          0  'to 43'
        43_0  COME_FROM                '40'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def SetEditMode(self, mode):
        if self.mode == mode:
            return
        if self.mode:
            self.modeHandlers[self.mode].OnExit()
        self.mode = mode
        self.modeHandlers[mode].OnEnter()

    def SetEditModeGame(self):
        self.SetEditMode(EDITOR_MODE_GAME)

    def SetEditModeEdit(self):
        self.SetEditMode(EDITOR_MODE_EDIT)

    def SetEditEntity(self, uuid):
        if isinstance(uuid, (tuple, list)):
            if not all((self.entityMgr.HasEntity(e) for e in uuid)):
                return
            uuidList = uuid
        elif uuid:
            if not self.entityMgr.HasEntity(uuid):
                return
            uuidList = [
             uuid]
        else:
            uuidList = []
        self.SetSelectEntityInternal(None)
        self.ctrlDown = True
        for key in uuidList[::-1]:
            self.SetSelectEntityInternal(key)

        self.ctrlDown = False
        return

    def DestroyEntity(self, uuid):
        if self.selectEntityUUID and uuid == self.selectEntityUUID:
            self.SetSelectEntity(None)
            self.ClearStatusMessage()
        entity = self.entityMgr.GetEntity(uuid)
        if not entity:
            return False
        else:
            if entity is GetEngineEditAPI().GetPlayerAvatar():
                return False
            self.editAPI.DestroyEntity(entity)
            doc = self.entityMgr.GetEntityDocument(uuid)
            doc.DeleteEntity(uuid)
            if uuid in self.selectedEntities:
                self.selectedEntities.remove(uuid)
            for entityid in self.entityidToUuid:
                if self.entityidToUuid[entityid] == uuid:
                    self.entityidToUuid.pop(entityid)
                    break

            self.GetServer().DelEntity(uuid)
            return True

    def GetEntityTypeName(self, uuid):
        entity = self.entityMgr.GetEntity(uuid)
        if entity:
            return entity.__class__.__name__
        else:
            return None
            return None

    def GetEntityData(self, uuid):
        entity = self.entityMgr.GetEntity(uuid)
        if not entity:
            raise KeyError('Unable to find entity %s' % uuid)
        return self._SerializeEntity(entity)

    def GetEntityEditComponent(self, uuid):
        return self.editComponents.get(uuid)

    def UpdateEntity(self, key, data):
        entity = self.entityMgr.GetEntity(key)
        if not entity:
            return
        else:
            classMeta = GetClassMeta(entity.__class__.__name__)
            editData = data.get('Edit', None)
            UpdateObject(entity, classMeta, data)
            if editData is not None:
                editComponent = self.editComponents.get(key)
                if editComponent:
                    for k in editData:
                        editComponent.ModifyProperty(k, editData[k])

            return

    def GetResourceData(self):
        if Globals.PLATFORM[0] == 'windows':
            r = {}
            for resType in xrange(19):
                resList = MResource.QueryResourceByType(resType).split(';')
                resTypeStr = Globals.RES_TYPE_STRING_TABLE.get(resType, 'None')
                if resList:
                    r[resTypeStr] = resList

            return r
        else:
            return MessiahUtils.LoadJson(MessiahUtils.GetResourceFilePath('GameConfig/Editor/ClientResourceData.json'))

    def GetEditCategories(self):
        return self.editCategories

    def GetPrefabData(self):
        return self.editAPI.GetPrefabData()

    def CreateEntity(self, uuid, data, position=None, exData=None):
        if position:
            self.ShowDebugPoint(None)
            if len(position) == 2:
                position = MessiahUtils.RaycastObstacle(position, EDITOR_RAYCAST_DISTANCE)
                if position:
                    data['position'] = position
        if not GetEngineEditAPI().IsGameReady():
            self.entityCache.append((uuid, data, exData))
            return
        else:
            entity = self.editAPI.CreateEntity(uuid, data)
            if not entity:
                print('Fail to create entity, uuid=%s, data=%s, exData=%s' % (uuid, data, exData))
                return
            if exData and 'docID' in exData:
                docID = exData['docID']
            else:
                docID = self.entityMgr.DefaultDocumentID
            if not self.editAPI.GetEditComponent(entity):
                editComponent = self._CreateEditComponent(entity, data.get('Edit'))
                editComponent.editable = True
                self.editComponents[uuid] = editComponent
            if entity and GetIEntity(entity).CharCtrl:
                GetIEntity(entity).CharCtrl.PassiveMode = True
            if entity and GetIEntity(entity).Filter:
                GetIEntity(entity).Filter.ApplyMotion = False
            if hasattr(entity, 'id'):
                self.entityidToUuid[entity.id] = uuid
            self._AddEntity(uuid, entity, False, docID)
            return

    def _DelayCreateEntities(self):
        for uuid, data, exData in self.entityCache:
            self.CreateEntity(uuid, data, exData=exData)

        self.entityCache = []

    def _CreateEditComponent(self, entity, data=None):
        for clz in inspect.getmro(entity.__class__):
            editComponentClass = GetEditComponentClass(clz.__name__)
            if editComponentClass:
                break
        else:
            return

        editComponent = editComponentClass(data)
        editComponent.Bind(entity)
        editComponent.PostInit(data)
        return editComponent

    def GetAvailableEntities(self):
        if GetEngineEditAPI().IsGameReady():
            entities = []
            for key, _ in self.entityMgr.DefaultDocument.IterEntities():
                entities.append(key)

            return entities
        else:
            self._shouldSentInitialEntities = True
            return []

    def ModifyEntityProperty(self, key, pathParts, val):
        print('ModifyEntityProperty, key=%s, path=%s, val=%s' % (key, pathParts, val))
        entity = self.entityMgr.GetEntity(key)
        if len(pathParts) > 0 and pathParts[0] == 'Edit':
            editComponent = self.editComponents.get(key)
            if editComponent is not None:
                editComponent.ModifyProperty(pathParts[1], val)
                return
        if self.isEntityTransformPath('/'.join(pathParts)):
            prop = pathParts[len(pathParts) - 1]
            self._cacheTransforms.get(prop, {})[key] = val
        objMeta = GetClassMeta(entity.__class__.__name__)
        objList, metaList = [], []
        for obj, meta in TraverseObjectByPath(entity, objMeta, pathParts, len(pathParts) - 1):
            if obj is None or meta is None:
                return
            objList.append(obj)
            metaList.append(meta)

        for i in range(len(metaList) - 1, -1, -1):
            if isinstance(metaList[i], BaseClassMeta):
                o, m = objList[i], metaList[i]
                relPath = pathParts[i:]
                ModifyEntityProperty(o, m, relPath, val)
                if hasattr(m, 'OnPropertyChanged'):
                    m.OnPropertyChanged(o, '/'.join(relPath))
                return

        ModifyEntityProperty(entity, objMeta, pathParts, val)
        return

    def AddEntityProperty(self, key, pathParts, vals):
        print('AddEntityProperty, key=%s, path=%s, vals=%s' % (key, pathParts, vals))
        entity = self.entityMgr.GetEntity(key)
        objMeta = GetClassMeta(entity.__class__.__name__)
        if isinstance(vals, dict):
            for k in vals:
                AddEntityProperty(entity, objMeta, pathParts, vals[k], k, True)

        else:
            for v in vals:
                AddEntityProperty(entity, objMeta, pathParts, v)
                if hasattr(objMeta, 'OnPropertyChanged'):
                    objMeta.OnPropertyChanged(entity, '/'.join(pathParts))

    def DelEntityProperty(self, key, pathParts):
        print('DelEntityProperty, key=%s, path=%s' % (key, pathParts))
        entity = self.entityMgr.GetEntity(key)
        if not entity:
            print('DelEntityProperty, entity %s was not found!' % key, file=sys.stderr)
        objMeta = GetClassMeta(entity.__class__.__name__)
        DelEntityProperty(entity, objMeta, pathParts)
        if hasattr(objMeta, 'OnPropertyChanged'):
            objMeta.OnPropertyChanged(entity, '/'.join(pathParts))

    def MoveEntityProperty(self, key, srcPathParts, dstPathParts):
        entity = self.entityMgr.GetEntity(key)
        if not entity:
            return
        objMeta = GetClassMeta(entity.__class__.__name__)
        if not objMeta:
            return
        MoveEntityProperty(entity, objMeta, srcPathParts, dstPathParts)

    def OperateEntityProperty(self, key, pathParts, args=None):
        print('OperateEntityProperty, key=%s, path=%s, args=%s' % (key, pathParts, args))
        entity = self.entityMgr.GetEntity(key)
        if not entity:
            return
        else:
            dataMeta = GetClassMeta(entity.__class__.__name__)
            if not dataMeta:
                return
            targetObj, targetMeta = GetObjectMetaByPath(entity, dataMeta, pathParts, len(pathParts) - 1)
            if targetObj is None:
                sys.stderr.write('invalid path\n')
                return
            if isinstance(targetMeta, PObject):
                targetMeta = targetMeta._GetObjectClassMeta(targetObj)
            funcName = pathParts[-1]
            if targetMeta is None:
                func = getattr(targetObj, funcName, None)
            elif hasattr(targetMeta, funcName):
                func = getattr(targetMeta, funcName)
                args = list(args) if args else []
                args.insert(0, targetObj)
            else:
                func = targetMeta.GetChildObject(targetObj, funcName)
            if func is not None:
                if args is None:
                    func()
                else:
                    func(*args)
            return

    def ClickEntityProperty(self, key, propertyStr):
        print('You just clicked %s' % propertyStr)

    def GetEntityDynamicEditorMeta(self, key):
        entity = self.entityMgr.GetEntity(key)
        if not entity:
            return
        classMeta = GetClassMeta(entity.__class__.__name__)
        if not classMeta:
            return
        return classMeta.GetDynamicEditorMeta(entity)

    def OnFingerOut(self, state, x, y):
        mode = self.inSpecialEditMode or self.modeHandlers[self.mode] if 1 else self.specialMode
        mode.OnMouseLDown(state, x, y)
        return mode.CaptureTouch()

    def OnKeyUp(self, state, key):
        if key in (Input.KEY_LCTRL, Input.KEY_RCTRL):
            self.ctrlDown = False
        elif key in (Input.KEY_LEFTARROW, Input.KEY_RIGHTARROW, Input.KEY_UPARROW, Input.KEY_DOWNARROW):
            self.OnMoveEnd()
        elif key == Input.KEY_F:
            self.OnFocusEntity()
        elif key == Input.KEY_B:
            self.FixCurrentEntityPos()

    def OnKeyDown(self, state, key):
        if key in (Input.KEY_LCTRL, Input.KEY_RCTRL):
            self.ctrlDown = True
        elif key in (Input.KEY_LEFTARROW, Input.KEY_RIGHTARROW, Input.KEY_UPARROW, Input.KEY_DOWNARROW):
            self.OnMoveEntity(state, key)
        elif key == Input.KEY_DELETE:
            self.OnDeleteEntity(state, key)

    def OnMouseLDown(self, state, x, y):
        mode = self.inSpecialEditMode or self.modeHandlers[self.mode] if 1 else self.specialMode
        mode.OnMouseLDown(state, x, y)

    def OnMouseRDown(self, state, x, y):
        mode = self.inSpecialEditMode or self.modeHandlers[self.mode] if 1 else self.specialMode
        mode.OnMouseRDown(state, x, y)

    def OnMouseMove(self, state, x, y):
        self.modeHandlers[self.mode].OnMouseMove(state, x, y)

    def OnMouseWheelDown(self, state=None):
        pass

    def OnMouseWheelUp(self, state=None):
        pass

    def OnDeleteEntity(self, state, key):
        for ent in self.selectedEntities:
            edit = self.editComponents.get(ent)
            if edit.IsEditable():
                self.GetServer().PreDestroyEntity(ent)

    def OnMoveEntity(self, state, key):
        if not self.selectEntityUUID or not self.entityMgr.HasEntity(self.selectEntityUUID):
            return
        self._MoveEntity(key)
        if self.moveTimer:
            self.moveTimer.Cancel()
        self.moveTimer = GetEngineEditAPI().GetPlayerAvatar().Timer.AddRepeatTimer(0.1, self._MoveEntity, key, 0.4)

    def _MoveEntity(self, key, dis=0.2):
        if not self.selectEntityUUID or not self.entityMgr.HasEntity(self.selectEntityUUID):
            return
        entity = self.entityMgr.GetEntity(self.selectEntityUUID)
        if not entity:
            return
        pos = entity.position
        theta = entity.direction
        if key == Input.KEY_LEFTARROW:
            newPos = (pos[0] + dis * math.cos(theta), pos[1], pos[2] - dis * math.sin(theta))
        elif key == Input.KEY_RIGHTARROW:
            newPos = (pos[0] - dis * math.cos(theta), pos[1], pos[2] + dis * math.sin(theta))
        elif key == Input.KEY_UPARROW:
            newPos = (pos[0] + dis * math.sin(theta), pos[1], pos[2] + dis * math.cos(theta))
        elif key == Input.KEY_DOWNARROW:
            newPos = (pos[0] - dis * math.sin(theta), pos[1], pos[2] - dis * math.cos(theta))
        else:
            raise Exception
        rPos = MessiahUtils.GetMapHeightByRaycast(newPos)
        entity.position = rPos or newPos

    def OnMoveEnd(self):
        if self.moveTimer:
            self.moveTimer.Cancel()
            self.moveTimer = None
        return

    def EnableEventEntityCreated(self, enable):
        self.enableEventEntityCreated = enable

    def EnableEventEntityPreDestroy(self, enable):
        self.enableEventEntityPreDestroy = enable

    def SetSelectEntityInternal(self, uuid):
        if not self.selectSetting:
            self.InitSelectionSetting()
        if not self.ctrlDown:
            for entityID in self.selectedEntities:
                editComponent = self.editComponents.get(entityID)
                if editComponent:
                    editComponent.LeaveSelectedState()

            self.selectedEntities = set()
            self.selectEntityUUID = uuid
            if self.selectEntityUUID:
                self.selectedEntities.add(self.selectEntityUUID)
                editComponent = self.editComponents.get(self.selectEntityUUID)
                if editComponent:
                    editComponent.EnterSelectedState()
        elif uuid:
            if uuid not in self.selectedEntities:
                self.selectedEntities.add(uuid)
                self.selectEntityUUID = uuid
                editComponent = self.editComponents.get(uuid)
                if editComponent:
                    editComponent.EnterSelectedState()
            else:
                self.selectedEntities.remove(uuid)
                editComponent = self.editComponentsget(uuid)
                if editComponent:
                    editComponent.LeaveSelectedState()
                if self.selectEntityUUID is uuid:
                    self.selectEntityUUID = None
        else:
            self.selectEntityUUID = None
        self.EventEditEntityChanged(self.selectEntityUUID)
        return

    def IsGameReady(self):
        return GetEngineEditAPI().IsGameReady()

    def SetSelectEntity(self, uuid):
        if uuid == self.selectEntityUUID:
            return
        self.SetSelectEntityInternal(uuid)
        self.GetServer().SetEditEntity(list(self.selectedEntities))

    def OnEditModeClick(self, state, x, y):
        if not self.inMoveMode:
            self.OnClickSelectEntity(x, y)
        else:
            self.OnMoveSelectEntity(x, y)

    def OnEditModeRightClick(self, state, x, y):
        if self.inMoveMode and self.selectEntityUUID:
            editComponent = self.editComponents.get(self.selectEntityUUID)
            editComponent.OnCancelMove()
            self.SetSelectEntity(None)
            self.ClearStatusMessage()
        self.inMoveMode = False
        return

    def OnEditModeMouseMove(self, _, x, y):
        if not self.selectedEntities or not self.inMoveMode:
            return
        player = GetEngineEditAPI().GetPlayerAvatar()
        for uuid in self.selectedEntities:
            entity = self.entityMgr.GetEntity(uuid)
            if entity is not player:
                self.editComponents[uuid].OnPickMove(x, y)

    def OnClickSelectEntity(self, x, y):
        selectEntityUUID = None
        engineEntity = MessiahUtils.RaycastEntity((x, y), EDITOR_RAYCAST_DISTANCE)
        if engineEntity:
            for key, entity in self.entityMgr.IterAllEntities():
                if GetIEntity(entity) == engineEntity:
                    selectEntityUUID = key
                    break

        if not selectEntityUUID:
            for key in self.editComponents:
                if self.editComponents[key].CheckIfSelected(x, y):
                    selectEntityUUID = key
                    break

        self.SetSelectEntity(selectEntityUUID)
        self._ShowSelectEntityInfo(x, y)
        return

    def _ShowSelectEntityInfo(self, x, y):
        pos = None
        if self.selectEntityUUID:
            entity = self.entityMgr.GetEntity(self.selectEntityUUID)
            msg = 'Entity Selected. '
            if hasattr(entity, 'position'):
                pos = [ round(x, 2) for x in entity.position ]
                msg += 'Position: ' + str(pos) + ', '
            if hasattr(entity, 'direction'):
                msg += 'Direction: ' + str(round(entity.direction, 2)) + '. '
        else:
            msg = 'None Selected. '
            position = MessiahUtils.RaycastObstacle((x, y), EDITOR_RAYCAST_DISTANCE)
            if position:
                pos = [ round(x, 2) for x in position ]
                msg += 'Terrain Position: ' + str(pos) + '. '
        player = GetEngineEditAPI().GetPlayerAvatar()
        if pos and player:
            playerPos = player.position
            dis = math.sqrt(math.pow(pos[0] - playerPos[0], 2) + math.pow(pos[1] - playerPos[1], 2))
            height = playerPos[1] - pos[1]
            msg += 'Horizontal distance: ' + str(round(dis, 2)) + ', '
            msg += 'Height distance: ' + str(round(height, 2)) + '. '
        self.SetStatusMessage(msg)
        return

    def OnMoveSelectEntity(self, x, y):
        if not self.inMoveMode:
            return
        else:
            if not self.selectEntityUUID:
                self.inMoveMode = False
                return
            player = GetEngineEditAPI().GetPlayerAvatar()
            entity = self.entityMgr.GetEntity(self.selectEntityUUID)
            if entity is player:
                position = MessiahUtils.RaycastObstacle((x, y), EDITOR_RAYCAST_DISTANCE)
                if not position:
                    import MCamera
                    cf = MCamera.CaptureFrame()
                    position = (cf.Position.x, cf.Position.y, cf.Position.z)
                GetEngineEditAPI().GetPlayerAvatar().server['GM'].GMCommand('#teleport %f %f %f' % position)
            else:
                self.GetServer().UpdateEditEntityProperty(self.selectEntity.UUID, 'position', entity.position)
            self.SetSelectEntity(None)
            self.ClearStatusMessage()
            self.inMoveMode = False
            return

    def SetStatusMessage(self, msg):
        self.GetServer().SetStatusMessage(msg)

    def ClearStatusMessage(self):
        self.GetServer().ClearStatusMessage()

    def ShowDebugPoint(self, pt):
        if self.createModeMovePt:
            GetEngineEditAPI().GetPlayerAvatar().VisualDebug.DestroyObject(self.createModeMovePt)
        if pt is None:
            return
        else:
            position = MessiahUtils.RaycastObstacle(pt, EDITOR_RAYCAST_DISTANCE)
            if not position:
                return
            self.createModeMovePt = GetEngineEditAPI().GetPlayerAvatar().VisualDebug.CreateSphere(position, 0.5, posType=Globals.VISUAL_DEBUG_POS_TYPE_WORLD)
            return

    def EnterPointSelectionMode(self):
        self.inSpecialEditMode = True
        self.specialMode = EditorModePointSelection(self)

    def OnPointSelectionModeClick(self, state, x, y):
        self.ShowDebugPoint(None)
        pos = MessiahUtils.RaycastObstacle((x, y), EDITOR_RAYCAST_DISTANCE)
        self.ExitSpecialMode()
        self.GetServer().SetPointSelectionModePosition(pos)
        return

    def ExitSpecialMode(self):
        self.inSpecialEditMode = False
        self.specialMode = None
        return

    def _AddEntity(self, uuid, entity, select, docID=None):
        if entity is None:
            return
        else:
            if docID:
                doc = self.entityMgr.GetDocument(docID)
                if not doc:
                    docID = self.entityMgr.CreateDocument(docID)
                    doc = self.entityMgr.GetDocument(docID)
            else:
                doc = self.entityMgr.DefaultDocument
            doc.AddEntity(uuid, entity)
            edit = None
            editComp = self.editComponents.get(uuid)
            if editComp:
                edit = editComp.ConvertToDict()
            self.GetServer().AddEntity(uuid, self.GetEntityData(uuid), self.GetEntityDynamicEditorMeta(uuid), edit, False, docID)
            transformNames = GetEntityTransformName(GetEngineEditAPI().GetPlayerAvatar())
            for prop in transformNames:
                if hasattr(entity, prop):
                    entities = self._cacheTransforms.setdefault(prop, {})
                    entities[uuid] = getattr(entity, prop)

            if select:
                self.SetSelectEntity(uuid)
            return

    def _OnPlayerAvatarReady(self):
        self._DelayCreateEntities()
        if not self._shouldSentInitialEntities:
            return
        player = GetEngineEditAPI().GetPlayerAvatar()
        if player:
            self.entityMgr.DefaultDocument.AddEntity(player.id, player)
        for entity in self.editAPI.GetSystemEntities():
            if hasattr(entity, 'id'):
                entityID = entity.id
            else:
                entityID = str(id(entity))
            self.entityMgr.DefaultDocument.AddEntity(entityID, entity)

        if self._shouldSentInitialEntities:
            self._shouldSentInitialEntities = False
            for key, entity in self.entityMgr.DefaultDocument.IterEntities():
                self._AddEntity(key, entity, False)

    def UpdatePrefabData(self, pyExpr, operation='modify'):
        prefabData = eval(pyExpr)
        self.editAPI.UpdatePrefabData(prefabData)

    def GetCreateEntityData(self):
        return self.editAPI.GetCreateEntityData()

    def GetExportTemplates(self):
        return []

    def _InitExceptionCatcher(self):
        import linecache

        def logCallBack(t, value, tb):
            output = [
             '\n>>>>>>>>>> TRACEBACK BEGIN >>>>>>>>>>']
            try:
                while tb:
                    f = tb.tb_frame
                    c = f.f_code
                    linecache.checkcache(c.co_filename)
                    line = linecache.getline(c.co_filename, f.f_lineno, f.f_globals)
                    output.append('\tFile "%s", in %s' % (c.co_filename, c.co_name))
                    output.append('\t> %d: %s' % (f.f_lineno, line.strip() if line else None))
                    tb = tb.tb_next

            except Exception as e:
                output.append(str(e))

            output.append('\t%s %s' % (t.__name__, value))
            output.append('<<<<<<<<<< TRACEBACK END <<<<<<<<<<')
            logStr = '\n'.join(output)
            self.GetServer().ExceptionLog(logStr)
            return

        MEngine.SetExceptionCallback(logCallBack)

    def RefreshEntitiesToEditor(self):
        for key, entity in self.entityMgr.IterAllEntities():
            self.GetServer().AddEntity(key, self._SerializeEntity(entity))

    def _SerializeEntity(self, entity):
        classMeta = GetClassMeta(entity.__class__.__name__)
        if not classMeta:
            sys.stderr.write('unable to find class meta for entity: %s' % entity)
            return
        return classMeta.SerializeData(entity)

    def _BeforeSpaceChange(self):
        if self.mode == EDITOR_MODE_EDIT:
            self.SetEditMode(EDITOR_MODE_GAME)
            self.GetServer().SetEditMode(EDITOR_MODE_GAME)
        hasEditEntity = False
        for _, doc in self.entityMgr.IterAllDocuments():
            if doc is self.entityMgr.DefaultDocument:
                continue
            if doc.EntityCount() > 0:
                hasEditEntity = True
                break

        if hasEditEntity:
            self.GetServer().CacheEntities(GetEngineEditAPI().GetSpaceNo())

    def _OnSpaceChanged(self):
        if not GetEngineEditAPI().IsGameReady():
            return
        self.GetServer().RestoreCache(GetEngineEditAPI().GetSpaceNo())

    def EnterEditMode(self):
        GetEngineEditAPI().TriggerFreeview()
        GetEngineEditAPI().HideAllGui()
        if GetEngineEditAPI().GetPlayerAvatar() and hasattr(GetEngineEditAPI().GetPlayerAvatar(), 'Selection'):
            GetEngineEditAPI().GetPlayerAvatar().Selection.TryUnSelectEntity(None)
        return

    def ExitEditMode(self):
        GetEngineEditAPI().CloseFreeview()
        GetEngineEditAPI().RestoreGui()
        if self.selectEntityUUID:
            editComponent = self.editComponents.get(self.selectEntityUUID)
            editComponent.LeaveSelectedState()
            self.selectEntityUUID = None
        for entityID in self.selectedEntities:
            editComponent = self.editComponents.get(entityID)
            if editComponent:
                editComponent.LeaveSelectedState()

        self.selectedEntities = set()
        return

    def OnFocusEntity(self):
        if not self.selectEntityUUID:
            return
        centerPos, radius = self.GetSelectEntityTransformInfo()
        self._OnCameraFocus(centerPos, radius)

    def _OnCameraFocus(self, pos, radius):
        c = MEngine.GetGameplay().Player.Camera
        mat = c.Transform
        mat.translation = pos + 2 * radius * mat.z_axis
        c.Transform = mat
        nav = MEngine.GetGameplay().Player.Navigator
        nav.Target = pos

    def GetSelectEntityTransformInfo(self):
        if not self.selectedEntities:
            if not self.selectEntityUUID:
                return
            return self._GetEntityTransformInfo([self.selectEntityUUID])
        else:
            return self._GetEntityTransformInfo(self.selectedEntities)

    def _GetEntityTransformInfo(self, entityIDList):
        radius = 5.0
        entities = filter(lambda x: x, map(lambda x: self.entityMgr.GetEntity(x), entityIDList))
        posList = map(lambda x: GetIEntity(x.entity).Transform.translation, entities)
        centerPos = sum(posList, MType.Vector3(0, 0, 0)) * (1.0 / len(posList))
        radius = max(max(map(lambda p: (p - centerPos).length * 2, posList)), radius)
        return (
         centerPos, radius)

    def FixCurrentEntityPos(self):
        if self.selectEntity and self.selectEntity.Edit.editable:
            self._FixEntityPos(self.selectEntity.entity)
        for entityID in self.selectedEntities:
            entity = self.entityMgr.GetEntity(entityID)
            if entity:
                self._FixEntityPos(entity.entity)

    def _FixEntityPos(self, entity):
        pos = entity.position
        height = GetEngineEditAPI().GetPlayerAvatar().Space.GetMapHeight(pos)
        if height:
            pos = (
             pos[0], height, pos[2])
            entity.position = pos
        pos = GetEngineEditAPI().GetPlayerAvatar().Space.GetMapHeightForFixPos(pos)
        if pos:
            entity.position = pos

    def isEntityTransformPath(self, path):
        return path in GetEntityTransformName(GetEngineEditAPI().GetPlayerAvatar()) or path in ('Edit/localPosition',
                                                                                                'Edit/localDirection',
                                                                                                'Edit/localScale')

    def UpdateEntityTransform(self, entityID, path, updateServer=False, undo=False, initialValue=None):

        def _rotate(_pos, _roll, _pitch, _yaw, reverse):
            if not reverse:
                _matrix = MType.Matrix4x3()
                _matrix.set_pitch_yaw_roll(_pitch, _yaw, _roll)
                _newPos = _matrix.transform_v(_pos)
            else:
                _matrix = MType.Matrix4x3()
                _matrix.yaw = _yaw
                _newPos = _matrix.transform_v(_pos)
                _matrix = MType.Matrix4x3()
                _matrix.pitch = _pitch
                _newPos = _matrix.transform_v(_newPos)
                _matrix = MType.Matrix4x3()
                _matrix.roll = _roll
                _newPos = _matrix.transform_v(_newPos)
            return _newPos

        entity = self.entityMgr.GetEntity(entityID)
        iEntity = GetIEntity(entity)
        editComponent = self.GetEntityEditComponent(entityID)
        parentID = editComponent.parent if editComponent else ''
        if parentID:
            serverTransformList = []
            transform = iEntity.Transform
            transformName = GetEntityTransformName(entity)
            pEntity = self.entityMgr.GetEntity(parentID)
            pIEntity = GetIEntity(pEntity)
            pTransform = pIEntity.Transform
            pRoll, pPitch, pYaw = pTransform.roll, pTransform.pitch, pTransform.yaw
            pPosition, pScale = pTransform.translation, pTransform.scale
            if path in ('', 'Edit/parent') or path in transformName:
                position = transform.translation
                localPosition = position - pPosition
                localPosition = _rotate(localPosition, -pRoll, -pPitch, -pYaw, True)
                localPosition = [localPosition.x, localPosition.y, localPosition.z]
                if editComponent.localPosition != localPosition:
                    editComponent.localPosition = localPosition
                    serverTransformList.append(('Edit/localPosition', localPosition))
                localDirection = [transform.roll - pTransform.roll, transform.pitch - pTransform.pitch, transform.yaw - pTransform.yaw]
                if editComponent.localDirection != localDirection:
                    editComponent.localDirection = localDirection
                    serverTransformList.append(('Edit/localDirection', localDirection))
                scale = iEntity.Transform.scale
                localScale = [scale.x / pScale.x, scale.y / pScale.y, scale.z / pScale.z]
                if editComponent.localScale != localScale:
                    editComponent.localScale = localScale
                    serverTransformList.append(('Edit/localScale', localScale))
            elif path in ('Edit/localPosition', 'Edit/localDirection', 'Edit/localScale'):
                localPos = editComponent.localPosition
                newPos = _rotate(MType.Vector3(*localPos), pRoll, pPitch, pYaw, False)
                newPos = newPos + pPosition
                if transform.translation != newPos:
                    transform.translation = newPos
                    serverTransformList.append((transformName[0], [newPos.x, newPos.y, newPos.z]))
                localRot = editComponent.localDirection
                newRoll, newPitch, newYaw = localRot[0] + pTransform.roll, localRot[1] + pTransform.pitch, localRot[2] + pTransform.yaw
                if transform.roll != newRoll or transform.pitch != newPitch or transform.yaw != newYaw:
                    transform.roll, transform.pitch, transform.yaw = newRoll, newPitch, newYaw
                    if iEntity.Skeleton:
                        iEntity.Skeleton.SetVariableF(0, 'G_YAW', transform.yaw)
                    serverTransformList.append((transformName[1], transform.yaw))
                localScale = editComponent.localScale
                newScale = MType.Vector3(localScale[0] * pScale.x, localScale[1] * pScale.y, localScale[2] * pScale.z)
                if transform.scale != newScale:
                    transform.scale = newScale
                    serverTransformList.append((transformName[2], transform.scale.x))
                iEntity.Transform = transform
            if updateServer:
                for _path, _value in serverTransformList:
                    if _path:
                        self.GetServer().UpdateEditEntityProperty(entityID, _path, _value, undo, initialValue)

        elif updateServer:
            self.GetServer().UpdateEditEntityProperty(entityID, path, getattr(entity, path), undo, initialValue)
        for _key, _entity in self.entityMgr.IterAllEntities():
            _editComponent = self.GetEntityEditComponent(_key)
            if _editComponent and _editComponent.parent == entityID:
                self.UpdateEntityTransform(_key, 'Edit/localPosition', updateServer)

    def GetCreateEmptyEntityData(self):
        return {'Type': 'EmptyEntity','name': '\xe7\xa9\xba\xe5\xaf\xb9\xe8\xb1\xa1'}

    def FocusEntity(self, key):
        if self.entityMgr.GetEntity(key) is None:
            return
        else:
            centerPos, radius = self._GetEntityTransformInfo(key)
            self._OnCameraFocus(centerPos, radius)
            return

    def FocusPosition(self, position):
        self._OnCameraFocus(MType.Vector3(*position), 5)


class EditorMode(object):
    text = ''
    mode = 0

    def __init__(self, parent):
        self.parent = parent

    def OnEnter(self):
        pass

    def OnExit(self):
        pass

    def OnMouseLDown(self, state, x, y):
        pass

    def OnMouseRDown(self, state, x, y):
        pass

    def OnMouseMove(self, state, x, y):
        pass

    def CaptureTouch(self):
        return False


class GameMode(EditorMode):
    text = '\xe6\xb8\xb8\xe6\x88\x8f\xe6\xa8\xa1\xe5\xbc\x8f'
    mode = EDITOR_MODE_GAME


class EditMode(EditorMode):
    text = '\xe7\xbc\x96\xe8\xbe\x91\xe6\xa8\xa1\xe5\xbc\x8f'
    mode = EDITOR_MODE_EDIT

    def OnEnter(self):
        self.parent.EnterEditMode()

    def OnExit(self):
        self.parent.ExitEditMode()

    def OnMouseMove(self, state, x, y):
        self.parent.OnEditModeMouseMove(state, x, y)

    def OnMouseLDown(self, state, x, y):
        self.parent.OnEditModeClick(state, x, y)

    def OnMouseRDown(self, state, x, y):
        self.parent.OnEditModeRightClick(state, x, y)

    def CaptureTouch(self):
        return True


class EditorModePointSelection(EditorMode):

    def OnEnter(self):
        self.parent.EnterEditMode()

    def OnExit(self):
        self.parent.ExitEditMode()

    def OnMouseLDown(self, state, x, y):
        self.parent.OnPointSelectionModeClick(state, x, y)

    def OnMouseRDown(self, state, x, y):
        self.parent.ShowDebugPoint((x, y))

    def CaptureTouch(self):
        return True
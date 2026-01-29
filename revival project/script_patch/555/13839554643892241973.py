# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Plugins/RainbowPlugin.py
from __future__ import absolute_import
from __future__ import print_function
import MontageSDK
from sunshine.SunshineSDK.Plugin.RainbowPlugin import RainbowPluginClient
from MontageSDK.Backend.utils.ShortUUID import uuid
EDITOR_MODE_GAME = 0
EDITOR_MODE_EDIT = 1

class RainbowPlugin(RainbowPluginClient):

    def __init__(self):
        super(RainbowPlugin, self).__init__()
        self.mode = None
        self.gizmoMode = None
        self.pointSelMode = False
        self.selectedEntityIDlist = []
        self.editCategories = ['PlayerAvatar', 'Monster', 'InteractSceneEntity', 'Npc']
        self.entities = {}
        self.ctrlDown = False
        return

    def SetEditMode(self, mode):
        if self.mode == mode:
            return
        self.mode = mode

    def SetEntityOpMode(self, modeID):
        MontageSDK.Interface.setGizmoType(modeID)

    def SetGizmoMode(self, mode):
        if self.gizmoMode == mode:
            return
        if mode == 0:
            print('\xe5\xb7\xb2\xe5\x88\x87\xe6\x8d\xa2\xe5\x88\xb0\xe4\xb8\x96\xe7\x95\x8c\xe5\x9d\x90\xe6\xa0\x87\xe7\xb3\xbb\xef\xbc\x88neox\xe5\x85\xac\xe7\x89\x88\xe6\x9c\xaa\xe5\xae\x9e\xe7\x8e\xb0\xef\xbc\x89')
        else:
            print('\xe5\xb7\xb2\xe5\x88\x87\xe6\x8d\xa2\xe5\x88\xb0\xe5\xb1\x80\xe9\x83\xa8\xe5\x9d\x90\xe6\xa0\x87\xe7\xb3\xbb\xef\xbc\x88neox\xe5\x85\xac\xe7\x89\x88\xe6\x9c\xaa\xe5\xae\x9e\xe7\x8e\xb0\xef\xbc\x89')
        self.gizmoMode = mode

    def GetEditCategories(self):
        return self.editCategories

    def GetResourceData(self):
        pass

    def GetPrefabData(self):
        prefabData = [
         {'Type': 'Monster',
            'charid': 'G609',
            'name': '\xe5\xa4\xa9\xe6\x9c\xba\xe8\x90\xa5',
            'PrefabID': 'M90003105',
            'Conf': {'baseSpeed': 6.5,'charid': 'G609','charName': '\xe5\xa4\xa9\xe6\x9c\xba\xe8\x90\xa5'}}]
        return prefabData

    def DestroyEntity(self, key):
        self.ClearSelections()
        entity = self.entities.pop(key, None)
        entity.LeaveArea()
        return True

    def FocusEntity(self, key):
        return
        import MType
        import MEngine
        entity = self.getEntitybyKey(key[0])
        if entity is None:
            MontageSDK.Interface.PrintFunc('Entity not found: %s' % key)
            return
        else:
            maxV3 = MType.Vector3()
            for prim in entity.Primitives:
                for axis in ['x', 'y']:
                    if getattr(maxV3, axis, 0) < getattr(prim.LocalBound.max, axis, 0):
                        setattr(maxV3, axis, getattr(prim.LocalBound.max, axis, 0))

            lookOffset = MType.Vector3(0, 1, 0)
            lookAt = 2 * maxV3 + MType.Vector3(0, 0, 3)
            t = MType.Matrix4x3()
            t.translation = entity.Transform.translation + lookAt + lookOffset
            t.pitch = lookAt.pitch
            t.yaw = lookAt.yaw
            MEngine.GetGameplay().Player.Camera.Transform = t
            return

    def CreateEntity(self, key, data, position=None):
        if data['Type'] == 'Monster':
            import MHelper
            import MType
            import Model
            entity = MHelper.CreateEntity('model', (('Char/tj/1005b/tj_hair_1005', ''), ('Char/tj/1005b/tj_ub_1005', ''),
             ('Char/tj/1005b/tj_lb_1005', '')), 'Char/1003/base.skeleton', '')
            gamepos = MontageSDK.Interface.screenToGame(position)
            t = MType.Matrix4x3()
            t.translation = MType.Vector3(gamepos['X'], gamepos['Y'], gamepos['Z'])
            t.roll = 0
            t.pitch = 0
            t.yaw = 0
            t.scale = MType.Vector3(1, 1, 1)
            entity.Transform = t
            actor = entity.Skeleton
            model = Model.SimpleModel()
            model.model = entity
            actor.BindEvent('SignalNotify', model.signalNotifyCallback)
            MontageSDK.Helper.CreateMedia(str(id(actor)))
            MontageSDK.Helper.media[str(id(actor))].engine = 0
            self.entities[key] = entity
            data = {'position': [
                          gamepos['X'], gamepos['Y'], gamepos['Z']],
               'scale': 1,
               'direction': 0.0,
               'name': '\xe5\xa4\xa9\xe6\x9c\xba\xe8\x90\xa5',
               'Type': 'Monster',
               'Edit': {'editName': '\xe5\xa4\xa9\xe6\x9c\xba\xe8\x90\xa5',
                        'editable': True,
                        'editCategory': 'Monster',
                        'typeCategory': 'Client',
                        'isStartEntity': None,
                        'Type': 'EditComponent'
                        }
               }
            self.GetServer().AddEntity(key, data, None, None, True)
        if data['Type'] != 'Model':
            return
        else:
            gamepos = MontageSDK.Interface.screenToGame(position)
            createDesc = {'CreateMode': 'Diy',
               'CreateInfo': [
                            {'name': data['name'],
                               'resType': 'model',
                               'skeleton': '',
                               'graph': '',
                               'models': (
                                        (
                                         data['respath'], ''),),
                               'clothes': [],'clothcolshape': ''
                               }],
               'InitValue': {'Transform': gamepos + (0, 0, 0, 1)
                             }
               }
            MontageSDK.Montage.Server.CreateActor(gamepos, createDesc)
            return

    def GetEntityTypeName(self, key):
        return 'Entity'

    def GetEntityEditComponent(self, key):
        return None

    def GetEntityDynamicEditorMeta(self, key):
        return None

    def getEntityUUID(self, entity):
        for key, e in MontageSDK.Interface.entities.items():
            if e is entity:
                return key

        return MontageSDK.Castmanager.castEntities.get(entity)

    def registerMouseUpCallback(self):
        pass

    def registerEditKeyUpCallback(self):
        pass

    def registerGameKeyUpCallback(self):
        keys = [
         Input.KEY_1,
         Input.KEY_2,
         Input.KEY_3,
         Input.KEY_4,
         Input.KEY_SPACE]
        Input().listenKeyUp(self.onGameKeyUp, *keys)

    def unregisterGameKeyUpCallback(self):
        keys = [
         Input.KEY_1,
         Input.KEY_2,
         Input.KEY_3,
         Input.KEY_4,
         Input.KEY_SPACE]
        for key in keys:
            Input().listenersKeyUp.pop(key)

    def onMouseUp(self, key, *args):
        if self.pointSelMode:
            pos = MontageSDK.Interface.screenToGame(args)
            self.pointSelMode = False
            self.Server.SetPointSelectionModePosition(pos)
        else:
            body = MontageSDK.Interface.RaycastRigidBody(args)
            selectedid = None
            self.ClearSelections()
            if body is not None:
                entity = body.Parent
                if entity is not None:
                    selectedid = key = self.getEntityUUID(entity)
                    if key is None:
                        selectedid = key = uuid()
                        self.entities[key] = entity
                    self.SetEditEntity([key])
            MontageSDK.Interface.PrintFunc(selectedid)
            self.Server.SetEditEntity(selectedid)
        return

    def onMouseDown(self, state, x, y):
        MontageSDK.CurvePathManager.onMouseLDown(x, y)

    def onMouseMove(self, state, x, y):
        MontageSDK.CurvePathManager.onMouseMove(x, y)

    def onEditKeyUp(self, _, key):
        if self.mode != EDITOR_MODE_EDIT:
            return
        if key == Input.KEY_K:
            print('K pressed')
            MontageSDK.Montage.Server.onKeyUp(key)
        elif key == Input.KEY_D:
            print('D pressed')
        elif key == Input.KEY_J:
            MontageSDK.Interface.SkipCurrentshot()
        elif key in (Input.KEY_LCTRL, Input.KEY_RCTRL):
            print('Ctrl up!!!!')
            self.ctrlDown = False

    def onEditKeyDown(self, _, key):
        if key in (Input.KEY_RCTRL, Input.KEY_LCTRL):
            print('Ctrl down!!!')
            self.ctrlDown = True

    def onGameKeyUp(self, _, key):
        if self.mode != EDITOR_MODE_GAME:
            return
        currentNode = MontageSDK.Galaxy.GetCurrentRunningNode()
        from ..Storyline.StorylineNode import ScriptDialogNode
        if not currentNode or not isinstance(currentNode, ScriptDialogNode):
            return
        if key == Input.KEY_1:
            currentNode.FinishDialog(output=0)
        elif key == Input.KEY_2:
            currentNode.FinishDialog(output=1)
        elif key == Input.KEY_3:
            currentNode.FinishDialog(output=2)
        elif key == Input.KEY_4:
            currentNode.FinishDialog(output=3)
        self.unregisterGameKeyUpCallback()

    def InitSelectionSetting(self):
        import MEngine
        mp = MEngine.GetGameplay().Player.Manipulator
        mp.SelectGizmo('EntityTranslator')

    def ClearSelections(self):
        for selectedid in self.selectedEntityIDlist:
            selectedentity = self.getEntitybyKey(selectedid)
            if selectedentity is None:
                continue
            selectedentity.IsSelected = False

        self.selectedEntityIDlist = []
        return

    def SetEditEntity(self, keys):
        return
        self.ClearSelections()
        self.InitSelectionSetting()
        for k in keys:
            entity = self.getEntitybyKey(k)
            if entity is None:
                continue
            entity.IsSelected = True
            self.selectedEntityIDlist.append(k)

        return

    def getEntitybyKey(self, key):
        return self.entities.get(key, None)

    def EnterPointSelectionMode(self):
        self.pointSelMode = True

    def ModifyEntityProperty(self, key, pathParts, val):
        import MType
        entity = self.getEntitybyKey(key)
        if entity is None:
            return
        else:
            if hasattr(entity, 'ModifyParams'):
                MontageSDK.Interface.PrintFunc('modifyparams')
                entity.ModifyParams(pathParts, val)
                return
            if pathParts[0] == 'translation':
                transform = entity.Transform
                transform.translation = MType.Vector3(*val)
                entity.Transform = transform
            elif pathParts[0] == 'scale':
                transform = entity.Transform
                transform.scale = MType.Vector3(*val)
                entity.Transform = transform
            elif pathParts[0] == 'rotation':
                transform = entity.Transform
                transform.set_pitch_yaw_roll(val[1], val[2], val[0])
                entity.Transform = transform
            elif pathParts[0] == 'name':
                entity.SetName(val)
            return

    def GetEntityData(self, key):
        category = 'CineActors'
        entity = MontageSDK.Castmanager.getCastEntity(key)
        if entity is None:
            category = 'Original'
            entity = MontageSDK.Interface.entities.get(key)
            if entity is None:
                return
        return self.serializeEntity(entity, category)

    def GetAvailableEntities(self):
        return
        import GlobalData
        if GlobalData.p.space.loadFinished:
            self._GetAvailableEntities()
        else:
            GlobalData.p.space.addResourceLoadedCallback(self._GetAvailableEntities)

    def _GetAvailableEntities(self):
        import MHelper
        self.entities.clear()
        world = MHelper.GetActiveWorld()
        levels = world.Levels
        for l in levels.values():
            for e in l.RootArea.Entities:
                shortID = uuid()
                self.entities[shortID] = e
                self.Server.AddEntity(shortID, self.serializeEntity(e))

    def serializeEntity(self, entity, category='Original'):
        from MontageSDK.Lib.VirtualObj import BaseVirtualObj
        if isinstance(entity, BaseVirtualObj):
            return entity.Serialize()
        t = entity.Transform
        name = entity.GetName() if entity.GetName() != '' else 'MainPlayer'
        data = {'name': name,
           'Type': 'Entity',
           'translation': (
                         round(t.translation.x, 3), round(t.translation.y, 3), round(t.translation.z, 3)),
           'rotation': (
                      round(t.roll, 3), round(t.pitch, 3), round(t.yaw, 3)),
           'scale': (
                   round(t.scale.x, 3), round(t.scale.y, 3), round(t.scale.z, 3))
           }
        editData = {'editCategory': category}
        if MontageSDK.PluginReady:
            from MontageImp.MontEditComponent import MontEditComponentImp
            editComp = MontEditComponentImp(entity)
            if category == 'Original':
                editComp.SetEditType(editComp.EDITTYPE_EXIST)
            elif category == 'CineActors':
                editComp.SetEditType(editComp.EDITTYPE_RECRUITED)
            editData.update(editComp.ConvertToDict())
        if 'Edit' not in data:
            data['Edit'] = editData
        else:
            data.update({'Edit': editData})
        return data

    def GetExportTemplates(self):
        pass

    def GetCreateEntityData(self):
        return []

    def EnterEditMode(self):
        from SunshineManager import S_instance
        S_instance.lightningPlugin.SetCameraMode(1)

    def ExitEditMode(self):
        from SunshineManager import S_instance
        S_instance.lightningPlugin.SetCameraMode(1)
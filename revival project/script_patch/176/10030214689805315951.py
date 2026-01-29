# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontGameInterfaceImp.py
from __future__ import absolute_import
import math3d
import math
from MontageSDK.Backend.utils.Event import Event
import game
import game3d
import world
import MontageSDK
from MontageSDK.Lib.MontGameInterface import MontGameInterfaceBase, MontEditComponent, EndBehavior, ResPreview, AccelerationMode
from MontageSDK.Lib.MontCastManager import MontCastManagerBase
from MontageSDK.Lib import MontGameInterface as MGI
from . import TrackImp
from MontageSDK.Lib import MontPathManager
from MontageSDK.Backend.utils.ShortUUID import uuid
from .TrackImp.UniHelper import get_active_scene
from .TrackImp.UniGameInterface import set_cur_camera_params, UniGameInterface, NeoxMatrix
from .TrackImp.EffectFx import UEffectEntity
from .MontCameraBlendHelper import MontCameraBlendHelper
from .MontRecordManager import MontRecordManager
from .Gizmo import Gizmo
EPSILON = 0.0001

def rotation_matrix_to_euler_angle(m4_rotation):
    pitch = math.degrees(m4_rotation.pitch)
    yaw = math.degrees(m4_rotation.yaw)
    roll = math.degrees(m4_rotation.roll)
    return math3d.vector(pitch, yaw, roll)


def get_ray_to_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal, distance):
    d = ray_direction.dot(plane_normal)
    if abs(d) < EPSILON:
        t = distance
    else:
        t = (plane_point - ray_origin).dot(plane_normal) / d
        if t < EPSILON:
            t = distance
        if t > distance:
            t = distance
    return ray_direction * t + ray_origin


def get_active_camera():
    cur_scn = get_active_scene()
    camera = cur_scn.active_camera
    return camera


def screen_to_world_point(screen_x, screen_y, plane_normal, plane_point, distance):
    camera = get_active_camera()
    ray_origin, ray_direction = camera.screen_to_world(screen_x, screen_y)
    ray_direction.normalize()
    return get_ray_to_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal, distance)


def get_cur_camera_params():
    camera = get_active_camera()
    v3_pos = camera.world_position
    v3_rot = rotation_matrix_to_euler_angle(camera.rotation_matrix)
    n_fov = camera.fov
    return (
     v3_pos, v3_rot, n_fov)


def pick_model_by_touch(x, y):
    scene = world.get_active_scene()
    return scene.pick(x, y)[0]


class MontGameInterface(MontGameInterfaceBase):

    def __init__(self):
        super(MontGameInterface, self).__init__()
        self.cachedata = None
        self.gizmo = Gizmo()
        self.sceneEntities = []
        self.recruitedSceneEntities = []
        self.sceneEntity2UUID = {}
        self.UUID2sceneEntity = {}
        self.sceneAnimationMap = {}
        self.sceneEffects = []
        self.selectedEntityUuid = ''
        self.cineEpisodeTimeChanged = Event()
        self.timelineman.registerInterface(UniGameInterface)
        self.timelineman.interface.registerMatrix(NeoxMatrix)
        self.accelerationMode = AccelerationMode.DiffChange
        self.enableCastCache = False
        self.resetflag = False
        self.blendHelper = MontCameraBlendHelper()
        self.recordMgr = MontRecordManager()
        self.ctrlDown = False
        self.shortcut_info_dict = {}
        return

    def RuntimeInit(self, montCastManager=None):
        if MontageSDK.RuntimeInitiated:
            return
        super(MontGameInterface, self).RuntimeInit(montCastManager)
        self.timelineman.movie_finish_callback = self.CineFinishedHandler

    def MontageEditorInit(self, castManager=None, resManager=None, pathManager=None, cuedata=None, montagePlugin=None, extendPlugin=None):
        if MontageSDK.Initiated:
            return
        from MontageSDK.Backend.Transaction.TrackMeta.TrackMetaBase import registerSceneRootMeta, registerMontageRootMeta, TRootBase, registerRootMeta
        from .Meta.sceneTrack import TSceneRoot
        from .Meta.montageTrack import TMontageRoot
        registerSceneRootMeta(TSceneRoot)
        registerMontageRootMeta(TMontageRoot)
        registerRootMeta(TRootBase)
        super(MontGameInterface, self).MontageEditorInit(castManager, resManager, pathManager, cuedata, montagePlugin, extendPlugin)
        self.gizmo.scn = get_active_scene()
        if self.gizmo.scn:
            self.gizmo.scn.gizmo_init()
        self.gizmo.set_visible(False)
        global_data.montage_editor.add_editor_update_func(self.gizmo.update)
        global_data.montage_editor.add_mousemsg_listener(self.on_mouse_msg)
        self.registerPrePostCinematicEvent(groupName='EditorPreview')
        MontPathManager.initialize()
        self.gizmo.add_gizmo_dragging_listener(self.on_gizmo_drag)
        self.GetAvailableEntities()
        if self.CastManagerCls is not MontCastManagerBase:
            self.enableCastCache = self.accelerationMode == AccelerationMode.CastCache
        app.level.rainbowPlugin.GetServer().SetEditMode(1)
        self.registerEditorKeyHandle()

    def on_gizmo_drag(self, obj):
        if 'CameraActor' not in MontPathManager.managers:
            return
        if obj is MontPathManager.managers['CameraActor'].virtual_node and MontPathManager.managers['CameraActor'].transformProxy.isValid() and not MontPathManager.managers['CameraActor'].transformProxy.getProperty('locked', default=False):
            MontPathManager.managers['CameraActor'].RefreshCameraPathByEdit()
        else:
            dollyTrackPath = MontPathManager.managers['DollyTrack']
            if dollyTrackPath and obj in [ node.model for node in dollyTrackPath.wayNodes ]:
                dollyTrackPath.UpdateNodePos(obj)

    def setGizmoType(self, typecode):
        self.gizmo.switch_gizmo(typecode)

    def on_mouse_msg(self, msg, key):
        x, y = game.mouse_x, game.mouse_y
        if msg == game.MSG_MOUSE_DOWN:
            if not self.gizmo.is_dragging() and self.gizmo.snap_test(x, y):
                self.gizmo.start_dragging(x, y)
        elif msg == game.MSG_MOUSE_UP:
            if self.gizmo.is_dragging():
                self.gizmo.end_dragging()
                pathMgr = MontPathManager.managers['CameraActor']
                if pathMgr.virtual_node is not self.gizmo.object:
                    for key, entity in self.entities.items():
                        if entity.model is self.gizmo.object:
                            self.recordMgr.updateRecordFrame(entity)

                elif 'CameraActor' in MontPathManager.managers:
                    transform = MontPathManager.managers['CameraActor'].transformProxy
                    if transform.isValid() and not transform.getProperty('locked', default=False):
                        pathMgr.UpdateNodeEditToGame()
                dollyTrackPath = MontPathManager.managers['DollyTrack']
                nodes = [ node.model for node in dollyTrackPath.wayNodes ]
                if dollyTrackPath and self.gizmo.object in nodes:
                    nodeIndex = nodes.index(self.gizmo.object)
                    dollyTrackPath.SetWaypointToEditor(nodeIndex)
            else:
                model = pick_model_by_touch(x, y)
                self.SelectEntityByModel(model)

    def screenToGame(self, pos, distance=100):
        distance *= 10
        normal = math3d.vector(0, 1, 0)
        point = math3d.vector(0, 35, 0)
        if not pos:
            width, height, _, _, _ = game3d.get_window_size()
            pos = (width * 0.5, height * 0.5)
        pos = screen_to_world_point(pos[0], pos[1], normal, point, distance)
        return {'X': pos.x,'Y': pos.y,'Z': pos.z}

    def GetCameraTransform(self):
        params = get_cur_camera_params()
        data = {'Translation': {'X': round(params[0].x, 3),
                           'Y': round(params[0].y, 3),
                           'Z': round(params[0].z, 3)
                           },
           'Rotation': {'Roll': round(params[1].z, 3),
                        'Pitch': round(params[1].x, 3),
                        'Yaw': round(params[1].y, 3)
                        }
           }
        return data

    @property
    def timelineman(self):
        return global_data.sunshine_uniman

    def ResetCineStatus(self):
        super(MontGameInterface, self).ResetCineStatus()
        self.resetflag = True

    def RegisterRootMetaForMedia(self):
        from MontageSDK.Backend.Transaction.TrackMeta.TrackMetaBase import TRootBase
        from .Meta.sceneTrack import TSceneRoot
        from .Meta.montageTrack import TMontageRoot
        self.engine = 0
        return True

    def registerPrePostCinematicEvent(self, groupName=None):
        from MontageSDK.Lib.MontEventManager import getMontEventMgrInstance as MontEventMgr
        super(MontGameInterface, self).registerPrePostCinematicEvent(groupName)
        MontEventMgr().registerCinematicEvent(self.cineFinishedCallback, 'POST', groupName=groupName)
        MontEventMgr().registerCinematicEvent(self.freeCameraController, 'PRE', groupName=groupName)

    def CineFinishedHandler(self, groupName, eventType='POST'):
        from MontageSDK.Lib.MontEventManager import getMontEventMgrInstance as MontEventMgr
        MontEventMgr().TriggerEvent(eventType, groupName)

    def cineFinishedCallback(self, groupName):
        self.PrintFunc('Cine Finished Triggered! Movie key is: %s' % str(groupName))

    def freeCameraController(self, groupName, config):
        pass

    def DebugSave(self, filename):
        import json
        with open(filename, 'w') as fp:
            json.dump(self.cachedata, fp, indent=2)

    def ModifyPlayRate(self, groupName, playRate):
        self.timelineman.setPlayRate(moviekey=groupName, playRate=playRate)

    def TranslateMediaToCinematic(self, media, previewCamera='', isPauseEnd=EndBehavior.AUTO):
        media.setProperty('previewCamera', previewCamera)
        media.setProperty('endBehavior', isPauseEnd)
        return media._model()

    def PreviewCinematics(self, data, time, isPaused, groupName=None):
        if not groupName:
            groupName = self.getDefaultGroupName()
            if groupName is None:
                return False
        if groupName == 'EditorPreview' and self.enableCastCache:
            if self.resetflag is False:
                castDesc = set([ t.uuid for t in self.getEdittimeMedia().getAllEntityTracks() ])
                MontageSDK.Castmanager.setNewDesc(castDesc)
            else:
                MontageSDK.Castmanager.setNewDesc(set())
                self.resetflag = False

        def playCine():
            self.timelineman.pause(isPaused, groupName)
            self.timelineman.sceneGoto(time, groupName)
            if groupName == 'EditorPreview':
                playSpeed = data.properties.setdefault('globalSettings', {}).setdefault('playSettings', {}).get('playSpeed', 1.0)
                self.timelineman.setPlayRate(groupName, playSpeed)

        self.timelineman.stop_playing(groupName)
        if data:
            self.timelineman.play(data, groupName)
            if self.timelineman.interface.needWarmUp():
                self.timelineman.interface.registerWarmUpFinishCb(playCine)
            else:
                playCine()
        return True

    def PopCinematics(self, groupName):
        self.timelineman.stop_playing(groupName)
        return True

    def StopMont(self, groupName=None, ignoreLoop=True):
        if groupName is None:
            groupName = self.getDefaultGroupName()
            if groupName is None:
                return False
        media = self.getMontageGroupByName(groupName).media
        if media.endBehavior in (EndBehavior.LOOP, EndBehavior.PAUSE_AT_END) and not ignoreLoop:
            return False
        else:
            if groupName == 'EditorPreview':
                return False
            self.PopGraphData(groupName)
            return True

    def GetCineEpisodeState(self):
        return self.GetScenePlayingStatus()

    def PauseCinematics(self, status, groupName=None):
        super(MontGameInterface, self).PauseCinematics(status, groupName)
        self.PauseCineEpisodeTime(status, groupName)

    def PauseCineEpisodeTime(self, status, groupName=None):
        if groupName is None:
            groupName = self.getDefaultGroupName()
        self.timelineman.pause(status, groupName)
        return

    def setCineEpisodeTime(self, time, isPaused=None, groupName=None):
        if groupName is None:
            groupName = self.getDefaultGroupName()
        self.timelineman.sceneGoto(time, groupName)
        if isPaused is not None:
            self.timelineman.pause(isPaused, groupName)
        self.cineEpisodeTimeChanged(time, isPaused, groupName)
        return

    def GetMontTime(self, groupName=None):
        return self.timelineman.getMontTime(groupName)

    def SetMontTime(self, time, isPaused=None, groupName=None):
        if groupName is None:
            groupName = self.getDefaultGroupName()
        self.timelineman.goto(time, moviekey=groupName)
        if isPaused is not None:
            self.timelineman.pause(isPaused, moviekey=groupName)
        return self.timelineman.getSceneTime(groupName)

    def GetScenePlayingStatus(self, groupName='EditorPreview'):
        group = self.getMontageGroupByName(groupName)
        if not group:
            return None
        else:
            media = group.media
            montTime = self.timelineman.getMontTime(groupName)
            sceneTime = self.timelineman.getSceneTime(groupName)
            if groupName == 'EditorPreview' and media.endBehavior == EndBehavior.LOOP:
                montTime = min(montTime, media.montageRootProxy.getProperty('endTime') - 0.033)
                sceneTime = min(sceneTime, media.sceneRootProxy.getProperty('endTime') - 0.033)
            return {'montagetime': montTime,
               'scenetime': sceneTime,
               'isPaused': self.timelineman.isPaused(groupName)
               }

    def SelectEntityByModel(self, model):

        def showGizmo():
            self.gizmo.set_visible(True)
            self.gizmo.bind_object(model)

        self.gizmo.set_visible(False)
        if model is None:
            MontageSDK.Montage and MontageSDK.Montage.Server.SetEditEntities([])
            self.selectedEntityUuid = ''
            return
        else:
            for uid, m in self.entities.items():
                if m.model and m.model is model:
                    showGizmo()
                    if m.model in self.sceneEntity2UUID:
                        uid = self.sceneEntity2UUID[m.model] if 1 else uid
                        self.selectedEntityUuid = uid
                        MontageSDK.Montage and MontageSDK.Montage.Server.SetEditEntities([uid])
                        return

            from MontageSDK.Lib.MontPathManager import managers
            if 'CameraActor' in managers:
                virtualNode = managers['CameraActor'].virtual_node
                if model is virtualNode:
                    return showGizmo()
            if 'DollyTrack' in managers:
                wayNodes = [ node.model for node in managers['DollyTrack'].wayNodes ]
                wayNodes.append(managers['DollyTrack'].virtual_node)
                if model in wayNodes:
                    return showGizmo()
            return

    def SetEditEntity(self, selection):
        self.gizmo.set_visible(False)
        if selection:
            for sel in selection:
                if sel in self.entities:
                    self.gizmo.set_visible(True)
                    self.gizmo.bind_object(self.entities[sel].model)
                elif sel in self.recruitedSceneEntities and sel in self.UUID2sceneEntity:
                    model = self.UUID2sceneEntity[sel]
                    self.gizmo.set_visible(True)
                    self.gizmo.bind_object(model)

    def registerEditorKeyHandle(self):

        def _onKeyboardMsg(msg, keyCode):
            if msg == game.MSG_KEY_DOWN:
                if keyCode == game.VK_CTRL:
                    app.level.camera_controller.allow_move = False
                    self.ctrlDown = True
            elif msg == game.MSG_KEY_UP:
                if keyCode == game.VK_CTRL:
                    app.level.camera_controller.allow_move = app.level.edit_mode == 1
                    self.ctrlDown = False
                elif keyCode == game.VK_K:
                    MontageSDK.Montage.Server.addKeysByGame(self.selectedEntityUuid)
                    self.ctrlDown = False
                elif keyCode == game.VK_DELETE:
                    if self.selectedEntityUuid:
                        MontageSDK.ExtendPlugin.Server.deleteEntities([self.selectedEntityUuid])
                        self.ctrlDown = False
                elif keyCode == game.VK_S or keyCode == game.VK_Z:
                    if self.ctrlDown:
                        key_info = self.shortcut_info_dict.get(keyCode, {})
                        cmd = key_info.get('cmd', '')
                        if cmd:
                            MontageSDK.ExtendPlugin.Server.useEditorShortcuts(cmd)
                            self.ctrlDown = False

        game.add_key_handler(None, None, _onKeyboardMsg)
        return

    def FocusEntity(self, uuid):
        if uuid in self.UUID2sceneEntity:
            model = self.UUID2sceneEntity[uuid]
        else:
            entity = self.entities.get(uuid, None)
            if entity is None:
                MontageSDK.Interface.PrintFunc('Entity not found: %s' % uuid)
                return
            if not hasattr(entity, 'model'):
                return
            model = entity.model
        if not model:
            return
        else:
            if hasattr(world, 'model') and isinstance(model, world.model):
                maxV3 = math3d.vector(0, 0, 0)
                for axis in ['x', 'y']:
                    if getattr(maxV3, axis, 0) < getattr(model.bounding_box, axis, 0):
                        setattr(maxV3, axis, getattr(model.bounding_box, axis, 0))

                lookOffset = math3d.vector(0, 5, 0)
                lookAt = maxV3 * 4 + math3d.vector(0, 0, 15)
                pos = model.transformation.translation + lookAt + lookOffset
                rot = math3d.vector(math.degrees(-lookAt.pitch), 180 + math.degrees(lookAt.yaw), 0)
            else:
                maxV3 = math3d.vector(2, 2, 0)
                lookOffset = math3d.vector(0, 5, 0)
                lookAt = maxV3 * 4 + math3d.vector(0, 0, 15)
                pos = model.world_position + lookAt + lookOffset
                rot = math3d.vector(math.degrees(-lookAt.pitch), 180 + math.degrees(lookAt.yaw), 0)
            set_cur_camera_params(v3_pos=pos, v3_rot=rot)
            return

    def GetEntityData(self, uuid, type=MontEditComponent.EDITTYPE_RECRUITED):
        entity = self.entities.get(uuid, None)
        if not entity:
            model = self.UUID2sceneEntity.get(uuid, None)
            director = self.timelineman.movies.get('EditorPreview').m_movieGroupDirector
            result = {'ret': None}

            def filterModelCb--- This code section failed: ---

 510       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'model'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    41  'to 41'
          12  LOAD_FAST             0  'g'
          15  LOAD_ATTR             1  'model'
          18  LOAD_DEREF            0  'model'
          21  COMPARE_OP            8  'is'
        24_0  COME_FROM                '9'
          24  POP_JUMP_IF_FALSE    41  'to 41'

 511      27  LOAD_FAST             0  'g'
          30  LOAD_DEREF            1  'result'
          33  LOAD_CONST            2  'ret'
          36  STORE_SUBSCR     

 512      37  LOAD_GLOBAL           2  'True'
          40  RETURN_END_IF    
        41_0  COME_FROM                '24'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

            director.traverseGroup(filterModelCb)
            entity = result['ret']
        data = {}
        if entity:
            if MontageSDK.PluginReady:
                from MontageImp.MontEditComponent import MontEditComponentImp
                editComp = MontEditComponentImp(entity)
                editComp.SetEditType(type)
                data.update(editComp.ConvertToDict()['MontageInfo'])
        return data

    def CreateIndicatorEntity(self, charkey, screenPos):
        self.indicatorCharKey = charkey
        translation = self.screenToGame(screenPos)
        MontageSDK.ExtendPlugin.Server.createEntityTrack(self.indicatorCharKey, translation)

    def UpdateEntityData(self, key, entity):
        if MontageSDK.PluginReady:
            data = self.GetEntityData(key)
            if hasattr(entity, 'model') and entity.model in self.sceneEntity2UUID:
                uuid = self.sceneEntity2UUID[entity.model]
            else:
                uuid = key
            MontageSDK.Montage.Server.UpdateEntityData(uuid, data)

    def InformCastEntityAdd(self, key, entity):
        self.entities[key] = entity
        data = self.GetEntityData(key)
        if hasattr(entity, 'model') and entity.model in self.sceneEntity2UUID:
            uuid = self.sceneEntity2UUID[entity.model]
            self.recruitedSceneEntities.append(uuid)
        else:
            uuid = key
        if MontageSDK.Montage:
            MontageSDK.Montage.Server.UpdateEntityData(uuid, data)

    def InformCastEntityDelete(self, key):
        entity = self.entities.pop(key, None)
        if entity is None or not MontageSDK.Montage:
            return
        else:
            if hasattr(entity, 'model') and entity.model in self.sceneEntity2UUID:
                key = self.sceneEntity2UUID[entity.model]
                self.recruitedSceneEntities.remove(key)
                if self.gizmo.object == entity.model:
                    self.gizmo.set_visible(False)
                data = self.GetEntityData(key, 'SceneEffect' if isinstance(entity, UEffectEntity) else 'SceneEntity')
                MontageSDK.Montage.Server.UpdateEntityData(key, data)
            else:
                MontageSDK.Montage.Server.DelEntity(key)
            return

    def getEntityModelByName(self, name, groupName=None):
        group = self.getMovieGroupByName(name, groupName)
        if group:
            return group.model
        else:
            return None

    def getMovieGroupByName(self, name, groupName=None):
        if not groupName:
            groupName = self.getDefaultGroupName()
        movie = self.timelineman.movies.get(groupName)
        if not movie:
            return
        else:
            director = movie.m_movieGroupDirector
            target = {name: None}

            def filterNameCb(g):
                if g.name == name:
                    target[name] = g
                    return True

            director.traverseGroup(filterNameCb)
            return target[name]

    def _CineOffset(self, groupName):
        group = self.getMontageGroupByName(groupName)
        offsetTranslation = group.cineOffsetTransform.get('Position', (0, 0, 0))
        offsetRotation = group.cineOffsetTransform.get('Rotation', (0, 0, 0))
        if offsetTranslation == (0, 0, 0) and offsetRotation == (0, 0, 0):
            return
        media = group.media
        sceneRootProxy = media.sceneRootProxy
        dummyTransform = {'Translation': {'X': 0,'Y': 0,'Z': 0},'Rotation': {'Roll': 0,'Pitch': 0,'Yaw': 0}}
        dummyTrack = sceneRootProxy.addChild('Dummy', '_cineOffsetDummy')
        dummyTrack['Transform'].replaceFrame(dummyTransform, 0)
        for child in sceneRootProxy.getChildren():
            if child.name == '_cineOffsetDummy' or child.trackType == 'Director':
                continue
            media.reParent(child.uuid, dummyTrack.uuid, 0)

        dummyOffsetTransform = {'Translation': {'X': offsetTranslation[0],'Y': offsetTranslation[1],'Z': offsetTranslation[2]},'Rotation': {'Roll': math.degrees(offsetRotation[0]),
                        'Pitch': math.degrees(offsetRotation[1]),
                        'Yaw': math.degrees(offsetRotation[2])
                        }
           }
        dummyTrack['Transform'].replaceFrame(dummyOffsetTransform, 0)

    def GetAvailableEntities(self):
        if not MontageSDK.PluginReady:
            return

        class DummyMovieGroup(object):

            def __init__(self, model):
                self.model = model
                self.name = model.name

        from .MontEditComponent import MontEditComponentImp
        self.sceneEntities = get_active_scene().get_models()
        self.sceneEntity2UUID = {}
        self.UUID2sceneEntity = {}
        for model in self.sceneEntities:
            model.pickable = True
            editComp = MontEditComponentImp(DummyMovieGroup(model))
            editComp.SetEditType('SceneEntity')
            data = editComp.ConvertToDict()
            shortID = uuid()
            self.sceneEntity2UUID[model] = shortID
            self.UUID2sceneEntity[shortID] = model
            MontageSDK.Montage.Server.UpdateEntityData(shortID, data['MontageInfo'])

        sfx_list = get_active_scene().get_sfxes()
        pse_list = []
        self.sceneEffects = sfx_list + pse_list
        for effect in self.sceneEffects:
            editComp = MontEditComponentImp(DummyMovieGroup(effect))
            editComp.SetEditType('SceneEffect')
            data = editComp.ConvertToDict()
            shortID = uuid()
            self.sceneEntity2UUID[effect] = shortID
            self.UUID2sceneEntity[shortID] = effect
            MontageSDK.Montage.Server.UpdateEntityData(shortID, data['MontageInfo'])

    def UpdateAnimationMap(self, name, animMap):
        if MontageSDK.PluginReady:
            if name in self.sceneAnimationMap:
                return
            self.sceneAnimationMap[name] = animMap
            MontageSDK.ExtendPlugin.Server.UpdateAnimationMap(name, animMap)

    def UpdateRecordMode(self, recordTrackNum):
        self.recordMgr.updateRecordMode(recordTrackNum)

    def SetMontTracksEnabled(self, groupName, enabletracks, disabletracks):
        self.timelineman.setTracksEnabled(groupName, enabletracks, disabletracks)

    @staticmethod
    @ResPreview('SkeletonAnimationFrame')
    def previewSkeletonAnimation(data):
        media = MontageSDK.Interface.getEdittimeMedia()
        frameUuid = data.get('uuid', None)
        anim = data.get('animation')
        if not media or not uuid or not anim:
            return
        else:
            frameProxy = media.getProxy(frameUuid)
            if not frameProxy:
                return
            entityProxy = frameProxy.getEntityAncestor()
            entity = MontageSDK.Interface.entities.get(entityProxy.uuid)
            entity.model.play_animation(str(anim), -1, 0, 0, 1, 1)
            return

    @staticmethod
    @ResPreview('Effect')
    def previewEffect(data):
        from .TrackImp.UniGameInterface import recruitFx
        from .TrackImp import UniHelper
        entityUuid = data.get('uuid', None)
        entity = MontageSDK.Interface.entities.get(entityUuid)

        def callback(sfx, user_data, task):
            if entity.m_model:
                entity.m_model.destroy()
                entity.m_model = None
            if sfx is None:
                return
            else:
                entity.m_model = sfx
                sfx.loop = True
                sfx.frame_rate = 1
                UniHelper.get_active_scene().add_object(sfx)
                sfx.restart()
                entity.updateEffectTransform()
                return

        if entity:
            recruitFx(data, callback)
        return

    def OnEditorDataChange(self, dataChangeInfo):
        op = dataChangeInfo.get('op', None)
        if not op:
            return
        else:
            rootDirector = MontageSDK.Interface.timelineman.movies.get('EditorPreview')
            oldValue = dataChangeInfo.get('oldValue', None)
            newValue = dataChangeInfo.get('newValue', None)
            if op == 'DEL':
                self._OnEditorDel(oldValue)
            elif op == 'ADD':
                proxyType = dataChangeInfo.get('proxyType', None)
                parentUuid = dataChangeInfo.get('parentUuid', None)
                self._OnEditorAdd(newValue, proxyType, parentUuid)
            elif op == 'MOD':
                proxyUuid = dataChangeInfo.get('parentUuid', None)
                propertyDir = dataChangeInfo.get('propertyDir', None)
                self._OnEditorMod(newValue, proxyUuid, propertyDir)
            rootDirector.update(0, force=True)
            rootDirector.setCameraByPreviewInfo()
            return

    def _GetDirectorByRootProxy(self, rootProxy):
        rootDirector = MontageSDK.Interface.timelineman.movies.get('EditorPreview')
        if rootProxy.trackType == 'SceneTrackRoot':
            director = rootDirector.m_movieGroupDirector
        elif rootProxy.trackType == 'MontageTrackRoot':
            director = rootDirector.m_movieGroupMont
        else:
            raise TypeError('[Montage] root track type error')
        return director

    def _OnEditorDel(self, oldValue):
        from MontageSDK.Backend.Transaction.MontageProxy import MontageTrackProxy, MontageFrameProxy
        media = MontageSDK.Interface.getEdittimeMedia()
        proxy = media.getProxy(oldValue)
        parentProxy = proxy.getParent()
        director = self._GetDirectorByRootProxy(parentProxy.getRootProxy())
        if isinstance(proxy, MontageTrackProxy):
            director.DeleteTrackByUuid(proxy.uuid)
            parentProxy.deleteChild(proxy)
        elif isinstance(proxy, MontageFrameProxy):
            track = director.GetActionByUuid(parentProxy.uuid)
            if track:
                track.DeleteFrameByUuid(proxy.uuid)

    def _OnEditorAdd(self, newValue, proxyType, parentUuid):
        from MontageSDK.Backend.Model.MontageTrack import MontageTrack
        from MontageSDK.Backend.Transaction.MontageProxy import MontageTrackProxy, MontageFrameProxy
        media = MontageSDK.Interface.getEdittimeMedia()
        modelUuid = newValue.get('uuid', None)
        if not modelUuid:
            return
        else:
            parentProxy = media.getProxy(parentUuid)
            rootProxy = parentProxy.getRootProxy()
            director = self._GetDirectorByRootProxy(rootProxy)
            if proxyType == 'Track':
                trackProxy = media.getProxy(modelUuid)
                if trackProxy is not None:
                    parentProxy.revertTrack(modelUuid, newValue)
                    trackModel = trackProxy._model()
                else:
                    trackModel = MontageTrack(modelUuid)
                    trackModel.deserialize(newValue)
                    trackProxy = MontageTrackProxy(trackModel)
                    parentProxy._model().addChild(trackModel)
                if parentProxy is rootProxy:
                    director.AddMontChild(trackModel)
                else:
                    director.AddGroupChild(parentUuid, trackModel)
            elif proxyType == 'Frame':
                frameModel = parentProxy._model().createFrame(modelUuid)
                frameModel.deserialize(newValue)
                frameProxy = MontageFrameProxy(frameModel)
                parentProxy._model().frames.sort(key=lambda k: k.time)
                action = director.GetActionByUuid(parentUuid)
                if action:
                    action.AddFrameByModel(frameModel)
            return

    def _OnEditorMod(self, newValue, proxyUuid, propertyDir):
        from MontageSDK.Backend.Transaction.MontageProxy import MontageTrackProxy, MontageFrameProxy
        media = MontageSDK.Interface.getEdittimeMedia()
        rootDirector = MontageSDK.Interface.timelineman.movies.get('EditorPreview')
        if not proxyUuid or not propertyDir:
            return
        proxy = media.getProxy(proxyUuid)
        if proxy is media:
            if propertyDir[-1] == 'previewCamera':
                media.setProperty('previewCamera', newValue)
                rootDirector.previewCamera = newValue
                rootDirector.setCameraByPreviewInfo()
                rootDirector.update(0)
                rootDirector.setCameraByPreviewInfo()
            return
        if isinstance(proxy, MontageFrameProxy):
            director = self._GetDirectorByRootProxy(proxy.getParent().getRootProxy())
            parentUuid = proxy.getParent().uuid
            parentMovieAction = director.GetActionByUuid(parentUuid)
            if parentMovieAction:
                parentMovieAction.SetFrameValue(proxyUuid, propertyDir[-1], newValue)
                if propertyDir[-1] == 'time':
                    proxy.setTime(newValue)
                elif propertyDir[-1] == 'duration':
                    proxy.setDuration(newValue)
                else:
                    proxy.setProperty(propertyDir[-1], newValue)
        elif isinstance(proxy, MontageTrackProxy):
            director = self._GetDirectorByRootProxy(proxy.getRootProxy())
            proxy.setProperty(propertyDir[-1], newValue)
            director.SetTrackProperty(proxy.uuid, propertyDir[-1], newValue)


def setGameInterface(interface_instance):
    MGI.setGameInterface(interface_instance)


def getGameInterface():
    return MGI.getGameInterface()


MGI.setGameInterface(MontGameInterface())
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/EntityActor.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from UniCineDriver.Movie.MovieObject import MovieGroupCls, MovieTrackCls
from .EntityBase import UEntityBase
from UniCineDriver.Movie.MovieActionSpan import MovieActionSpan
from UniCineDriver.Movie.MovieActionKeyframe import MovieActionTriggerKeyframe
import MontageSDK
from .UniGameInterface import recruitEntity, recruitExistModel, UniGameInterface, recruitModelWithID
from .UniHelper import euler_angle_to_rotation_matrix, rotation_matrix_to_euler_angle, get_active_scene
import math3d
import world
PROPERTY_STORAGE = [
 'cast_shadow', 'receive_shadow', 'position', 'scale', 'world_rotation_matrix']
PROPERTY_HANDLERS = {}

class PropertyHandler(object):

    def __init__(self, propertyName):
        self.propertyName = propertyName

    def __call__(self, func):
        PROPERTY_HANDLERS[self.propertyName] = func
        return func


@MovieGroupCls('EntityActor')
class UEntityActor(UEntityBase):

    def __init__(self, data, blackboard):
        super(UEntityActor, self).__init__(data, blackboard)
        self.m_model = None
        self.m_bIsRemoved = False
        self._pauseFlag = False
        self.asyncTask = None
        self.warmup = self.properties.get('warmUp', False)
        self._updatePending = False
        self.bind_model = None
        self.isModelBind = False
        self.currentBind = None
        self.lastBindInfo = {}
        self.sceneObjName = self.properties.get('sceneActorName', '')
        self.isSceneBound = False
        self.storylineID = self.properties.get('storylineID', None)
        self.isNPC = False
        self.start_matrix = None
        self.castShadow = 0
        self.receiveShadow = 0
        return

    def pause(self, flag):
        super(UEntityActor, self).pause(flag)
        self._pauseFlag = flag

    def isPaused(self):
        return self._pauseFlag

    @property
    def model(self):
        if self.m_model and self.m_model.valid:
            return self.m_model
        else:
            return None

    @PropertyHandler('isDynamicShadow')
    def setCastShadow(self):
        if self.castShadow != self.properties.get('isDynamicShadow', 0):
            self.castShadow = self.properties.get('isDynamicShadow', 0)
            if self.model and self.castShadow != 0:
                self.model.cast_shadow = self.castShadow == 1

    @PropertyHandler('receiveShadow')
    def setReceiveShadow(self):
        if self.receiveShadow != self.properties.get('receiveShadow', 0):
            self.receiveShadow = self.properties.get('receiveShadow', 0)
            if self.model and self.receiveShadow != 0:
                self.model.receive_shadow = self.receiveShadow == 1

    def afterinit(self):
        model = super(UEntityActor, self).afterinit()
        if model:
            if not self.sceneObjName:
                self.create_model_callback(model)
            else:
                self.recruit_scene_callback(model)
            return
        if not self.sceneObjName:
            if self.storylineID and recruitModelWithID(self.storylineID, self.recruit_scene_callback):
                self.isNPC = True
            else:
                self.asyncTask = recruitEntity(self.properties, self.create_model_callback)
                if self.warmup:
                    UniGameInterface.warmUpStart(self)
        else:
            recruitExistModel(self.sceneObjName, self.recruit_scene_callback)

    def clear_data(self):
        if self.sceneObjName:
            self.restoreEntityState()
        ret = super(UEntityActor, self).clear_data()
        if ret:
            self.m_model = None
            return
        else:
            if not self.sceneObjName and not self.isNPC:
                if self.m_model is not None and self.m_model.valid:
                    self.m_model.destroy()
                elif self.asyncTask and self.asyncTask.valid:
                    self.asyncTask.cancel()
            self.m_model = None
            return

    def init_model(self):
        if self.m_model is None:
            return
        else:
            if get_active_scene().get_model(self.m_model.name) is not self.m_model:
                get_active_scene().add_object(self.m_model)
            return

    def updateEntityTransform(self):
        if not self.m_model:
            self._updatePending = True
            return
        if self.currentBind:
            return
        self.m_model.position = math3d.vector(*self.transform.translate())
        self.m_model.scale = math3d.vector(*self.transform.scale())
        v3_rot = math3d.vector(self.transform.pitch(), self.transform.yaw(), self.transform.roll())
        m4_rotation = euler_angle_to_rotation_matrix(v3_rot)
        if self.m_model and self.m_model.valid:
            self.m_model.world_rotation_matrix = m4_rotation

    def create_model_callback(self, obj, *args, **kwargs):
        if obj is None or self.m_bIsRemoved:
            return
        else:
            self.m_model = obj
            obj.pickable = True
            obj.name = str(self.properties['name'])
            self.afterEditorInit()
            self.init_model()
            self.check_submodels_created()
            for track in self.tracks:
                if isinstance(track, UEntityActorAnimation) and track.properties['disabled'] is False:
                    cur_time = self.blackBoard.get('_lasttime', 0.0)
                    pause = MontageSDK.Interface.timelineman.isPaused('EditorPreview')
                    curspan = track.getCurrentFirstSpan()
                    track.resumeAnim(cur_time, needplay=True)
                    if curspan and pause:
                        track.pauseAtNext = 2

            if self._updatePending:
                self.updateEntityTransform()
            if self.warmup:
                UniGameInterface.warmUpFinish(self)
            return

    def recruit_scene_callback(self, obj):
        self.m_model = obj
        obj.pickable = True
        self.isSceneBound = True
        self.afterEditorInit()
        self.saveEntityState()
        self.check_submodels_created()

    def afterEditorInit(self):
        super(UEntityActor, self).afterEditorInit()
        if MontageSDK.Initiated:
            animMap = {sz_anim_name:self.m_model.get_anim_length(sz_anim_name) / 1000 for sz_anim_name in self.m_model.get_anim_names()}
            MontageSDK.Interface.UpdateAnimationMap(self.name, animMap)

    def applyCustomData(self, data):
        super(UEntityActor, self).applyCustomData(data)
        if self.model:
            for propertyName, setFunc in PROPERTY_HANDLERS.items():
                if hasattr(self, setFunc.__name__):
                    boundFunc = getattr(self, setFunc.__name__)
                    boundFunc()

        bindInfo = data.get('dynamicBind', {})
        if not bindInfo:
            if self.currentBind:
                self.undo_binding(self.lastBindInfo)
            else:
                return
        else:
            bindMovieGroup = MontageSDK.Interface.getMovieGroupByName(bindInfo['entityGroupName'], self.blackBoard['_moviekey'])
            if not bindMovieGroup:
                return
            if not self.model or not bindMovieGroup.model:
                return
            if bindMovieGroup.model == self.currentBind and bindInfo['socket'] == self.lastBindInfo['socket']:
                return
            self.lastBindInfo = bindInfo
            self.currentBind = bindMovieGroup.model
            self.do_binding(bindInfo)

    def saveEntityState--- This code section failed: ---

 221       0  SETUP_LOOP           84  'to 87'
           3  LOAD_GLOBAL           0  'PROPERTY_STORAGE'
           6  GET_ITER         
           7  FOR_ITER             76  'to 86'
          10  STORE_FAST            1  'propertyName'

 222      13  LOAD_GLOBAL           1  'hasattr'
          16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             2  'model'
          22  LOAD_FAST             1  'propertyName'
          25  CALL_FUNCTION_2       2 
          28  POP_JUMP_IF_FALSE    67  'to 67'

 223      31  LOAD_GLOBAL           3  'setattr'
          34  LOAD_GLOBAL           1  'hasattr'
          37  LOAD_FAST             1  'propertyName'
          40  BINARY_ADD       
          41  LOAD_CONST            2  'Storage'
          44  BINARY_ADD       
          45  LOAD_GLOBAL           4  'getattr'
          48  LOAD_FAST             0  'self'
          51  LOAD_ATTR             2  'model'
          54  LOAD_FAST             1  'propertyName'
          57  CALL_FUNCTION_2       2 
          60  CALL_FUNCTION_3       3 
          63  POP_TOP          
          64  JUMP_BACK             7  'to 7'

 225      67  LOAD_GLOBAL           5  'MontageSDK'
          70  LOAD_ATTR             6  'Interface'
          73  LOAD_ATTR             7  'PrintFunc'
          76  LOAD_CONST            3  'Failed to save entity state'
          79  CALL_FUNCTION_1       1 
          82  POP_TOP          
          83  JUMP_BACK             7  'to 7'
          86  POP_BLOCK        
        87_0  COME_FROM                '0'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 60

    def restoreEntityState(self):
        for propertyName in PROPERTY_STORAGE:
            propertyStorage = '_' + propertyName + 'Storage'
            if hasattr(self, propertyStorage):
                setattr(self.model, propertyName, getattr(self, propertyStorage))
                delattr(self, propertyStorage)
            else:
                MontageSDK.Interface.PrintFunc('Failed to restore entity state')

    def check_submodels_created(self):
        bindInfo = self.customData.get('bindInfo', {})
        if bindInfo:
            modelPath = bindInfo['modelPath']
            socketName = bindInfo['socket']
            bindType = bindInfo.get('bindType', 0)
            if self.bind_model:
                self.model.unbind(self.bind_model)
            self.bind_model = world.model(str(modelPath), get_active_scene())
            if self.model and not self.isModelBind:
                indirectObjs = []
                allObjects = self.model.get_all_objects_on_sockets()
                for obj in allObjects:
                    for indirect in obj.get_all_objects_on_sockets():
                        indirectObjs.append(indirect)

                for obj in allObjects:
                    if obj not in indirectObjs:
                        self.model.unbind(obj)

                self.bind_model.remove_from_parent()
                if bindType == 0:
                    self.model.bind(str(socketName), self.bind_model, world.BIND_TYPE_TRANSLATE | world.BIND_TYPE_ROTATE)
                elif bindType == 1:
                    self.model.bind_bone(str(socketName), self.bind_model, bind_type=world.BIND_TYPE_TRANSLATE | world.BIND_TYPE_ROTATE)
                self.isModelBind = True
        else:
            if self.model:
                indirectObjs = []
                allObjects = self.model.get_all_objects_on_sockets()
                for obj in allObjects:
                    for indirect in obj.get_all_objects_on_sockets():
                        indirectObjs.append(indirect)

                for obj in allObjects:
                    if obj not in indirectObjs:
                        self.model.unbind(obj)

            self.bind_model = None
            self.isModelBind = False
        return

    def do_binding(self, bind_info):
        target = self.currentBind
        if not target:
            return
        self.model.remove_from_parent()
        posOffset = bind_info['offset']['position']
        rotOffset = bind_info['offset']['rotation']
        self.model.position = math3d.vector(*posOffset)
        self.model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(rotOffset[1], rotOffset[2], rotOffset[0]))
        print('Bind target.bind ======================')
        bindType = bind_info['bindType']
        if bindType == 0:
            target.bind(bind_info['socket'], self.model, world.BIND_TYPE_TRANSLATE | world.BIND_TYPE_ROTATE)
        elif bindType == 1:
            target.bind_bone(bind_info['socket'], self.model, bind_type=world.BIND_TYPE_TRANSLATE | world.BIND_TYPE_ROTATE)

    def undo_binding(self, bind_info):
        if not self.currentBind:
            return
        else:
            bindType = bind_info['bindType']
            if bindType == 0:
                self.currentBind.unbind(self.model)
            else:
                if bindType == 1:
                    self.currentBind.unbind_bone(self.model)
                get_active_scene().add_object(self.model)
                if not self.blackBoard:
                    return
                entityGroup = MontageSDK.Interface.getMovieGroupByName(bind_info['entityGroupName'], self.blackBoard['_moviekey'])
                if not entityGroup:
                    return
            target = entityGroup.model
            socket_matrix = None
            if bindType == 0:
                socket_index = self.currentBind.get_socket_index(bind_info['socket'])
                socket_matrix = target.get_socket_matrix(socket_index)
            else:
                if bindType == 1:
                    skeletonComponent = self.currentBind.get_skeleton_component()
                    socket_index = skeletonComponent.get_joint_index(bind_info['socket'])
                    socket_matrix = skeletonComponent.get_joint_original_matrix_in_node_space(socket_index, world.NodeSpace.Root)
                if socket_matrix is None:
                    return
            v3_rot = rotation_matrix_to_euler_angle(socket_matrix)
            translation = self.transform.translate()
            scale = self.transform.scale()
            self.transform.createfromDegrees([v3_rot.z, v3_rot.x, v3_rot.y])
            self.transform.setTranslate(translation)
            self.transform.setScale(scale)
            self.currentBind = None
            self.updateEntityTransform()
            return

    def goto(self, n_cur_time, n_interval_time):
        super(UEntityActor, self).goto(n_cur_time, n_interval_time)
        if 'Transform' in self.customData:
            self.updateEntityTransform()

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEntityActor, self).update(n_cur_time, n_interval_time, force=force)
        if n_interval_time != 0 or force:
            if 'Transform' in self.customData:
                self.updateEntityTransform()


@MovieTrackCls('Animation', 'EntityActor')
class UEntityActorAnimation(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(UEntityActorAnimation, self).__init__(model, parent_movie_group)
        self.playRate = 1.0
        self._lasttime = 0.0
        self.activeFrameID = ''
        self.pauseAtNext = 0
        self.frameDrive = self.m_parentMovieGroup().blackBoard['_frameDrive']
        self.cur_span_duration = -1
        self.cur_anim_time = -1
        self.anim_rate = -1
        self.montFPS = self.m_parentMovieGroup().blackBoard['_montFPS']
        self.frame_time = 1 / float(self.montFPS) * 1000
        self.smooth_freq = 4
        self.smooth_count = 0

    @property
    def pauseFlag(self):
        return self.m_parentMovieGroup().isPaused()

    def updatePlayRate(self, rate):
        if rate != self.playRate:
            self.playRate = rate
            curspan = self.getCurrentFirstSpan()
            if self.model and curspan:
                self.model.anim_rate = curspan.properties.get('PlaybackSpeed', 1.0) * rate

    def onSpanFrameEnter(self, frame):
        self.activeFrameID = frame.uuid
        self.playAnim(frame, frame.properties.get('StartTime', 0.0))
        if self.frameDrive:
            self.cur_span_duration = frame.duration / float(self.montFPS) * 1000

    def onSpanFrameLeave(self, frame):
        if not self.model:
            return
        if frame.uuid == self.activeFrameID:
            self.model.stop_animation()

    def change_disabled(self, status):
        if status:
            if self.model:
                self.model.stop_animation()
            self.activeFrameID = ''
        super(UEntityActorAnimation, self).change_disabled(status)

    def playAnim(self, frame, starttime=0.0):
        if not frame:
            return
        if not self.model or not self.model.valid:
            return
        prop = frame.properties
        animaspeed = float(prop.get('PlaybackSpeed', 1.0)) * self.playRate
        self.model.play_animation(str(prop['name']), prop.get('overlap', 0) * 1000, prop['TransitType'], starttime * 1000, int(prop.get('Loop', 1)) and not int(prop.get('PauseEnd', False)), 1.0)
        self.model.anim_rate = animaspeed
        if self.frameDrive:
            self.cur_anim_time = self.model.anim_time
            self.anim_rate = self.model.anim_rate

    def getCurrentFirstSpan(self):
        if len(self._curspans) > 0:
            return self._curspans[0]
        else:
            return None

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEntityActorAnimation, self).update(n_cur_time, n_interval_time, force=False)
        self._lasttime = n_cur_time
        if self.model and self.pauseAtNext > 0:
            self.pauseAtNext -= 1
            if self.pauseAtNext == 0:
                self.model.stop_animation()
        if self.frameDrive:
            if not self.model or self.cur_anim_time < 0 or self.cur_anim_time >= self.cur_span_duration:
                return
            if self.cur_anim_time != self.model.anim_time and self.smooth_count == 0:
                span_time_left = self.cur_span_duration - self.cur_anim_time
                anim_time_left = self.cur_span_duration - self.model.anim_time
                self.model.anim_rate = anim_time_left * self.anim_rate / span_time_left
            self.smooth_count = (self.smooth_count + 1) % self.smooth_freq
            self.cur_anim_time += self.frame_time * n_interval_time

    def pause(self, flag):
        if flag:
            if self.model:
                self.model.stop_animation()
        else:
            self.pauseAtNext = 0
            self.resumeAnim(self._lasttime)

    def resumeAnim(self, n_cur_time, needplay=True):
        if not self.model:
            return
        curspan = self.getCurrentFirstSpan()
        if not curspan:
            return self.model.stop_animation()
        prop = curspan.properties
        starttime = curspan.time
        self._lasttime = n_cur_time
        playedtime = round(n_cur_time, 3) - starttime + prop.get('StartTime', 0.0)
        animaspeed = float(prop.get('PlaybackSpeed', 1.0)) * self.playRate
        anim_length = prop.get('Oridur', 1) * self.montFPS
        if anim_length == 0:
            playedtime = 0.0
        elif animaspeed == 0:
            playedtime = prop.get('StartTime', 0.0)
        else:
            playedtime = playedtime * animaspeed % anim_length
        if needplay:
            self.model.play_animation(str(prop['name']), prop.get('overlap', 0) * 1000, prop['TransitType'], playedtime * 1000, int(prop.get('Loop', 1)) and not int(prop.get('PauseEnd', False)), 1.0)
        else:
            self.model.anim_time = playedtime / float(self.montFPS) * 1000
        self.model.anim_rate = animaspeed
        if self.frameDrive:
            self.cur_anim_time = self.model.anim_time
            self.anim_rate = self.model.anim_rate

    @property
    def model(self):
        return self.m_parentMovieGroup().model

    def goto(self, n_cur_time, n_interval_time):
        lastspan = self.getCurrentFirstSpan()
        self.update(n_cur_time, n_interval_time)
        curspan = self.getCurrentFirstSpan()
        if lastspan is curspan:
            self.resumeAnim(n_cur_time, needplay=False)
        else:
            if curspan:
                self.activeFrameID = curspan.uuid
            self.resumeAnim(n_cur_time)
            if self.pauseFlag:
                self.pauseAtNext = 1

    def loadFromModel(self, model):
        super(UEntityActorAnimation, self).loadFromModel(model)
        count = len(self.frames)
        if count < 2:
            return
        for i in range(1, count):
            cur_frame = self.frames[i]
            left_frame = self.frames[i - 1]
            overlap = left_frame.time + left_frame.duration - cur_frame.time
            if overlap > 0:
                cur_frame.properties['overlap'] = overlap
            else:
                cur_frame.properties['TransitType'] = 0


@MovieTrackCls('AnimationGraph', 'EntityActor')
class UEntityActorAnimationGraph(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(UEntityActorAnimationGraph, self).__init__(model, parent_movie_group)

    def onSpanFrameEnter(self, frame):
        from .AnimGraphStr import LayerBlendGraph
        animation0 = frame.properties.get('Animation0', None)
        animation1 = frame.properties.get('Animation1', None)
        bone0 = frame.properties.get('BoneSelector0', None)
        bone1 = frame.properties.get('BoneSelector1', None)
        if not (animation0 and animation1 and bone0 and bone1):
            return
        else:
            animation0 = animation0.split('/')[-1]
            animation1 = animation1.split('/')[-1]
            graphStr = LayerBlendGraph.format(Animation0=animation0, Animation1=animation1, Bone0=bone0, Bone1=bone1)
            from neox import nxanimation
            animGraph = nxanimation.AnimationGraph.load(graphStr)
            if animGraph:
                animationComponent = self.model.get_animation_component()
                animationBundle = self.model.get_default_animation_bundle()
                animationComponent.play_animation_graph(animGraph, animationBundle)
            return

    def onSpanFrameLeave(self, frame):
        self.model.stop_animation()

    @property
    def model(self):
        return self.m_parentMovieGroup().model


@MovieTrackCls('Bind', 'EntityActor')
class UEntityActorBind(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(UEntityActorBind, self).__init__(model, parent_movie_group)
        self._initParentBindInfo(model.properties)
        self.posOffset = None
        self.rotOffset = None
        self.activeFrameID = ''
        return

    def _initParentBindInfo(self, properties):
        if properties['bindObject'] != 'EMPTY' and properties['bindSocket'] != 'None':
            bindType = properties.get('bindType', 0)
            self.m_parentMovieGroup().setCustomData(['bindInfo'], {'modelPath': str(properties['bindObject']),
               'socket': str(properties['bindSocket']),
               'bindType': bindType
               })
        else:
            self.m_parentMovieGroup().setCustomData(['bindInfo'], {})

    def onSpanFrameLeave(self, frame):
        if frame.uuid == self.activeFrameID:
            self.m_parentMovieGroup().setCustomData(['dynamicBind'], {})
            self.posOffset = None
            self.rotOffset = None
        return

    def onSpanFrameEnter(self, frame):
        self.m_parentMovieGroup().setCustomData(['dynamicBind'], {})
        prop = frame.properties
        if prop['BindNPCName'] != 'None' and prop['SocketName'] != 'None':
            self.activeFrameID = frame.uuid
            bind_data = {'entityGroupName': str(prop['BindNPCName']),
               'socket': str(prop['SocketName']),
               'bindType': prop.get('BindType', 0),
               'offset': {'position': prop['BindingOffset'],'rotation': prop['RotationOffset']}}
            self.posOffset = prop['BindingOffset']
            self.rotOffset = prop['RotationOffset']
            self.m_parentMovieGroup().setCustomData(['dynamicBind'], bind_data)

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEntityActorBind, self).update(n_cur_time, n_interval_time, force=force)
        if self.posOffset:
            if self.m_parentMovieGroup().model:
                self.m_parentMovieGroup().model.position = math3d.vector(*self.posOffset)
        if self.rotOffset:
            if self.m_parentMovieGroup().model:
                self.m_parentMovieGroup().model.rotation_matrix = math3d.euler_to_matrix(math3d.vector(self.rotOffset[1], self.rotOffset[2], self.rotOffset[0]))

    def SetProperty(self, key, value):
        super(UEntityActorBind, self).SetProperty(key, value)
        if key == 'bindSocket' or key == 'bindObject':
            self._initParentBindInfo(self.properties)
            self.m_parentMovieGroup().isModelBind = False
            self.m_parentMovieGroup().check_submodels_created()

    def clear_data(self):
        if self.m_parentMovieGroup().bind_model:
            self.m_parentMovieGroup().model.unbind(self.m_parentMovieGroup().bind_model)
        if self.m_parentMovieGroup().currentBind:
            self.m_parentMovieGroup().undo_binding(self.m_parentMovieGroup().lastBindInfo)
            self.m_parentMovieGroup().setCustomData(['dynamicBind'], {})
        super(UEntityActorBind, self).clear_data()


@MovieTrackCls('Hidden', 'EntityActor')
class UEntityActorHidden(MovieActionTriggerKeyframe):

    def __init__(self, model, parent_movie_group):
        super(UEntityActorHidden, self).__init__(model, parent_movie_group)
        self._needUpdate = False
        self.visibleCondition = True

    @property
    def model(self):
        return self.m_parentMovieGroup().model

    def trigger(self, data):
        value = not data.get('value', False)
        if self.model:
            self.model.visible = value
            self._needUpdate = False
        else:
            self._needUpdate = True
            self.visibleCondition = value

    def reset(self):
        if self.model:
            self.model.visible = True
            self._needUpdate = False
        else:
            self.visibleCondition = True
            self._needUpdate = True

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEntityActorHidden, self).update(n_cur_time, n_interval_time, force=force)
        if self._needUpdate and self.model:
            self.model.visible = self.visibleCondition
            self._needUpdate = False
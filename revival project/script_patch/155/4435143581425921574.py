# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/EffectFx.py
from __future__ import absolute_import
from UniCineDriver.Movie.MovieActionSpan import MovieActionSpan
from UniCineDriver.Movie.MovieActionKeyframe import MovieActionTriggerKeyframe
from UniCineDriver.Movie.MovieObject import MovieGroupCls, MovieTrackCls
from UniCineDriver.Movie.MovieGroupEntityBase import MovieGroupEntityBase
from .UniGameInterface import recruitFx, recruitExistFx, get_socket_matrix_by_name
from . import UniHelper
import math3d
import world
from .UniHelper import euler_angle_to_rotation_matrix, rotation_matrix_to_euler_angle
import MontageSDK

@MovieGroupCls('EffectEntity')
class UEffectEntity(MovieGroupEntityBase):

    def __init__(self, data, blackboard):
        super(UEffectEntity, self).__init__(data, blackboard)
        self.m_model = None
        self.m_bIsRemoved = False
        self._updatePending = False
        self.isActivate = False
        self.asyncTask = None
        self.loop = False
        self.endPos = None
        self._origin_end_pos = math3d.vector(0, 0, 0)
        self.playRate = 1.0
        self.pauseFlag = False
        self.sceneSfxName = self.properties.get('sceneActorName', '')
        self.visible = True
        return

    def isTaskPending(self):
        return self.asyncTask and self.asyncTask.valid

    def _updateCurPosAndRot(self):
        self.cur_pos = self.model.world_position
        rot_mat = self.model.world_rotation_matrix
        euler = rotation_matrix_to_euler_angle(rot_mat)
        self.cur_rot = [euler.z, euler.x, euler.y]

    @property
    def model(self):
        if self.m_model and self.m_model.valid:
            return self.m_model
        else:
            return None

    def pause(self, flag):
        self.pauseFlag = flag

    def clear_data(self):
        super(UEffectEntity, self).clear_data()
        MontageSDK.Interface.InformCastEntityDelete(self.uuid)
        if not self.sceneSfxName:
            if self.m_model and self.m_model.valid:
                self.m_model.destroy()
        self.m_model = None
        if self.isTaskPending():
            asyncTask = self.asyncTask
            asyncTask.cancel()
        self.asyncTask = None
        self.isActivate = False
        return

    def afterinit(self):
        if not self.sceneSfxName:
            if self.properties['effect'] == 'EMPTY':
                if self.m_model:
                    self.clear_data()
            MontageSDK.Interface.InformCastEntityAdd(self.uuid, self)
        else:
            recruitExistFx(self.properties, self.recruit_fx_callback)

    def activate_fx(self):
        if self.model or self.isActivate or self.isTaskPending():
            return
        self.asyncTask = recruitFx(self.properties, self.create_fx_callback)

    def deactivate_fx(self):
        asyncTask = self.asyncTask
        if asyncTask and asyncTask.valid:
            asyncTask.cancel()
        self.asyncTask = None
        if not self.isActivate:
            return
        else:
            if self.model and self.model.valid:
                self.m_model.destroy()
            self.m_model = None
            self.isActivate = False
            MontageSDK.Interface.UpdateEntityData(self.uuid, self)
            return

    def create_fx_callback(self, sfx, user_data, task):
        if sfx is None:
            return
        else:
            self.isActivate = True
            sfx.name = str(self.properties['name'])
            self.m_model = sfx
            self.m_model.loop = self.loop
            self.m_model.frame_rate = self.playRate
            UniHelper.get_active_scene().add_object(sfx)
            sfx.restart()
            self.updateEffectTransform()
            MontageSDK.Interface.UpdateEntityData(self.uuid, self)
            return

    def recruit_fx_callback(self, sfx):
        self.m_model = sfx
        self.m_model.visible = self.visible
        if 'Transform' in self.customData:
            self.updateEffectTransform()
        MontageSDK.Interface.InformCastEntityAdd(self.uuid, self)

    def goto(self, n_cur_time, n_interval_time):
        super(UEffectEntity, self).goto(n_cur_time, n_interval_time)
        self.updateEffectTransform()

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEffectEntity, self).update(n_cur_time, n_interval_time, force=force)
        if n_interval_time != 0 or force:
            self.updateEffectTransform()

    def updateEffectTransform(self):
        if not self.model:
            self._updatePending = True
            return
        if not self.transform:
            return
        self.model.world_position = math3d.vector(*self.transform.translate())
        if self.endPos:
            self.model.end_pos = self.endPos
        else:
            self.model.end_pos = self._origin_end_pos
        self.model.scale = math3d.vector(*self.transform.scale())
        v3_rot = math3d.vector(self.transform.pitch(), self.transform.yaw(), self.transform.roll())
        m4_rotation = euler_angle_to_rotation_matrix(v3_rot)
        if self.model:
            self.model.world_rotation_matrix = m4_rotation

    def applyCustomData(self, data):
        super(UEffectEntity, self).applyCustomData(data)
        bind = data.get('bind', {})
        if not bind:
            self.endPos = None
            return
        else:
            startInfo = bind.get('start', {})
            endInfo = bind.get('end', {})
            positionOffset = bind.get('position', [])
            rotationOffset = bind.get('rotation', [])
            if rotationOffset:
                rot = [self.transform.roll() + rotationOffset[0],
                 self.transform.pitch() + rotationOffset[1],
                 self.transform.yaw() + rotationOffset[2]]
                self.transform.createfromDegrees(rot)
            if startInfo:
                position = startInfo.translation
                self.transform.setTranslate([position.x, position.y, position.z])
            if endInfo:
                position = endInfo.translation
                self.endPos = position
            if positionOffset:
                origin_pos = self.transform.translate()
                self.transform.setTranslate([
                 origin_pos[0] + positionOffset[0],
                 origin_pos[1] + positionOffset[1],
                 origin_pos[2] + positionOffset[2]])
            return

    def change_sfx_loop(self, status):
        if self.loop == status:
            return
        if self.model:
            self.model.loop = status
        self.loop = status

    def change_fx_visible(self, status):
        if self.visible == status:
            return
        if self.model:
            self.model.visible = status
        self.visible = status

    def updatePlayRate(self, rate):
        super(UEffectEntity, self).updatePlayRate(rate)
        self.playRate = rate
        if self.model:
            self.model.frame_rate = rate


@MovieTrackCls('Activate', 'EffectEntity')
class UActivateEffect(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(UActivateEffect, self).__init__(model, parent_movie_group)
        self.activeFrameID = ''
        self.pauseLater = False
        self.pauseTime = 0

    @property
    def fxModel(self):
        return self.m_parentMovieGroup().model

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UActivateEffect, self).update(n_cur_time, n_interval_time, force=force)
        if not self.fxModel:
            return
        pauseFlag = self.m_parentMovieGroup().pauseFlag
        fxPauseFlag = self.fxModel.get_state() == world.FX_STATE_INACTIVE or self.fxModel.frame_rate == 0
        if not pauseFlag and fxPauseFlag:
            self.fxResume()
        elif pauseFlag and not fxPauseFlag:
            if self.pauseLater:
                if self.fxModel.loop:
                    self.pauseTime %= self.fxModel.life_span
                self.fxModel.set_curtime_directly(self.pauseTime)
                self.pauseLater = False
            self.fxPause()

    def goto(self, n_cur_time, n_interval_time):
        super(UActivateEffect, self).goto(n_cur_time, n_interval_time)
        currSpan = self.getCurrentFirstSpan()
        if currSpan:
            if not self.fxModel:
                self.m_parentMovieGroup().activate_fx()
                self.pauseTime = n_cur_time - currSpan.time
                self.pauseLater = True
            else:
                playTime = n_cur_time - currSpan.time
                if self.fxModel.loop:
                    playTime %= self.fxModel.life_span
                if abs(playTime - self.fxModel.cur_time) > 0.001:
                    self.fxModel.set_curtime_directly(playTime)
                    self.pauseTime = playTime
                self.fxPause()

    def getCurrentFirstSpan(self):
        if len(self._curspans) > 0:
            return self._curspans[0]
        else:
            return None

    def fxPause(self):
        if not self.fxModel:
            return
        if hasattr(world, 'particlesystem') and isinstance(self.fxModel, world.particlesystem):
            self.fxModel.pause()
        elif isinstance(self.fxModel, world.sfx):
            self.fxModel.frame_rate = 0

    def fxResume(self):
        if not self.fxModel:
            return
        if hasattr(world, 'particlesystem') and isinstance(self.fxModel, world.particlesystem):
            self.fxModel.resume()
        elif isinstance(self.fxModel, world.sfx):
            self.fxModel.frame_rate = self.m_parentMovieGroup().playRate

    def onSpanFrameEnter(self, frame):
        self.activeFrameID = frame.uuid
        if frame.properties['value']:
            self.m_parentMovieGroup().activate_fx()

    def onSpanFrameLeave(self, frame):
        if self.activeFrameID == frame.uuid:
            if frame.properties['value']:
                self.m_parentMovieGroup().deactivate_fx()


@MovieTrackCls('Loop', 'EffectEntity')
class UEffectLoop(MovieActionTriggerKeyframe):

    def trigger(self, data):
        self.m_parentMovieGroup().change_sfx_loop(data['value'])

    def reset(self):
        self.m_parentMovieGroup().change_sfx_loop(False)


@MovieTrackCls('Bind', 'EffectEntity')
class UEffectBind(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(UEffectBind, self).__init__(model, parent_movie_group)
        self.isBinding = False
        self.start_entity_name = ''
        self.end_entity_name = ''
        self.positionOffset = None
        self.rotationOffset = None
        self.activeFrameId = ''
        return

    def onSpanFrameEnter(self, frame):
        if frame.properties['BindNPCName'] == 'None':
            return
        self.activeFrameId = frame.uuid
        self.start_entity_name = frame.properties['BindNPCName']
        self.end_entity_name = frame.properties['EndNPCName']
        self.positionOffset = frame.properties['PositionOffset']
        self.rotationOffset = frame.properties['RotationOffset']
        self.isBinding = True

    def onSpanFrameLeave(self, frame):
        if frame.uuid == self.activeFrameId:
            self.isBinding = False
            self.m_parentMovieGroup().setCustomData(['bind'], {})
            self.start_entity_name = self.end_entity_name = ''
            self.rotationOffset = self.positionOffset = None
        return

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UEffectBind, self).update(n_cur_time, n_interval_time, force=force)
        parent = self.m_parentMovieGroup()
        start_entity_model = MontageSDK.Interface.getEntityModelByName(self.start_entity_name, self.m_parentMovieGroup().blackBoard['_moviekey'])
        end_entity_model = MontageSDK.Interface.getEntityModelByName(self.end_entity_name, self.m_parentMovieGroup().blackBoard['_moviekey'])
        if self.isBinding and start_entity_model:
            span = self._curspans[0]
            start_matrix = get_socket_matrix_by_name(span.properties['SocketName'], start_entity_model)
            end_matrix = get_socket_matrix_by_name(span.properties['EndSocketName'], end_entity_model)
            customData = {'position': self.positionOffset,'rotation': self.rotationOffset}
            if start_matrix:
                customData.update({'start': start_matrix})
            if end_matrix:
                customData.update({'end': end_matrix})
            parent.setCustomData(['bind'], customData)


@MovieTrackCls('Hidden', 'EffectEntity')
class UEffectVisible(MovieActionTriggerKeyframe):

    def trigger(self, data):
        self.m_parentMovieGroup().change_fx_visible(not data['value'])

    def reset(self):
        self.m_parentMovieGroup().change_fx_visible(True)
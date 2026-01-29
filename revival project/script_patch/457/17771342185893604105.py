# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/sceneTrack.py
from __future__ import absolute_import
from six.moves import range
from . import PInt, PStr, PBool, PFloat, PColor, PButton, PRes, PVector3, PEnum, PDict, PArray, OrderedProperties, PCustom, PFile, PVector2
from . import TrackMetaBase, TrackMeta, TResource, GetTrackMetaCls, TSceneRootBase, TFloat, TBool, EditorTrackColorType, MontageTrackProxy, TRootBase
from .CustomTrack import CustomEntityTracks, CustomSceneTracks, TSpanCue
from . import translate, DefEnum
from .CueConsts import CueID
from copy import deepcopy
import json
import os
DefEnum('IncarnationType', {0: 'None',1: 'actor0'})
DefEnum('CameraShakeType', {0: 'Custom',
   1: 'Bump',
   2: 'Explosion',
   3: 'Earthquake',
   4: 'BadTrip',
   5: 'HandheldCamera',
   6: 'Vibration',
   7: 'RoughDriving'
   })
DefEnum('CameraType', {0: 'PhysicCamera',
   1: 'GameCamera'
   })
DefEnum('SocketList', {'None': 'None'})
DefEnum('SocketListOther', {'None': 'None'})
DefEnum('CurrentNPCList', {'None': 'None'
   })
DefEnum('PlayAnimTransitType', {1: 'TT_IMM',
   2: 'TT_DELAY',
   3: 'TYPE_CROSS',
   4: 'TYPE_MORPH'
   })
DefEnum('UnBindType', {0: '\xe5\x8e\x9f\xe5\x9c\xb0\xe4\xb8\x8d\xe5\x8a\xa8',
   1: '\xe5\x9c\xb0\xe4\xb8\x8a',
   2: '\xe4\xb8\x8e\xe4\xbe\x9d\xe9\x99\x84\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x90\x8c\xe9\xab\x98'
   })
DefEnum('BindType', {0: 'Socket',
   1: '\xe9\xaa\xa8\xe9\xaa\xbc'
   })
DefEnum('DynamicShadowType', {0: '',
   1: 'True',
   2: 'False'
   })

@TrackMeta
class TRoot(TRootBase):
    CUSTOM_SETTINGS = {'sceneID': PInt(text=translate('Test', '\xe5\x89\xa7\xe6\x83\x85\xe6\x89\x80\xe5\x9c\xa8\xe5\x9c\xba\xe6\x99\xafID'), default=None, editable=False),
       'FitHor': PBool(text=translate('Montage', '\xe6\xa8\xaa\xe5\x90\x91\xe9\x80\x82\xe9\x85\x8d'), default=True),
       'Aspect': PFloat(text=translate('Montage', '\xe5\xb1\x8f\xe5\xb9\x95\xe6\xaf\x94\xe4\xbe\x8b'), default=16.0 / 9)
       }


@TrackMeta
class TCue(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Cue
    RESOURCE_TRACK = True
    FRAME_PROPERTIES = {'CueID': PInt(editable=False),
       'Data': PStr(),
       'Name': PRes(default='', resSet='Cue'),
       'Oneshot': PBool(text='\xe5\x8f\xaa\xe8\xa7\xa6\xe5\x8f\x91\xe4\xb8\x80\xe6\xac\xa1'),
       'Insure': PBool(text='\xe4\xbf\x9d\xe8\xaf\x81\xe8\xa7\xa6\xe5\x8f\x91')
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TCue, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
        except ImportError:
            return

        resManager = Sunshine.Services.GetService('MontageService').getResourceManager()
        ps = path[0]
        if ps == 'Name':
            if data:
                cueId = resManager.getResByKey('Cue', 'name', data)['cueid']
                frame.properties['CueID'] = cueId
            else:
                frame.properties['CueID'] = 0

    @classmethod
    def Serialize(cls, model):
        import json
        return json.dumps(model.serialize())

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TCue, self).UpdateMeta(proxy, dynamicmeta)
        entityAncestor = proxy.getEntityAncestor()
        if entityAncestor is not None:
            dynamicmeta.update({'Name': {'resType': 'EntityCue'}})
        elif proxy.getParent().trackType == 'SceneTrackRoot' or proxy.getParent().getParent().trackType == 'SceneTrackRoot':
            dynamicmeta.update({'Name': {'resType': 'GlobalCue'}})
        return

    def getIntersectedValue(self, track, time):
        return ''


@TrackMeta
class TAnimationRes(TResource):
    ALLOW_SAMENAME = True
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Animation
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'BoneFilter': PStr(text='\xe9\xaa\xa8\xe9\xaa\xbc\xe8\xbf\x87\xe6\xbb\xa4', default={'filterStr': ''}, visible=False)
       }
    FRAME_PROPERTIES = {'Oridur': PFloat(editable=False, default=1.0),
       'PauseEnd': PBool(text='\xe5\x8f\xaa\xe6\x92\xad\xe4\xb8\x80\xe6\xac\xa1'),
       'RemoveMotion': PBool(text='\xe7\xa7\xbb\xe9\x99\xa4\xe4\xbd\x8d\xe7\xa7\xbb'),
       'PlaybackSpeed': PFloat(text='\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87', default=1.0),
       'MirrorType': PBool(text='\xe5\x8a\xa8\xe7\x94\xbb\xe9\x95\x9c\xe5\x83\x8f', default=False),
       'DeactPausePlay': PBool(text='\xe6\x9a\x82\xe5\x81\x9c\xe6\x92\xad\xe6\x94\xbe\xe8\xbf\x9b\xe5\xba\xa6', default=False),
       'DeactStopMotion': PBool(text='\xe5\x81\x9c\xe6\xad\xa2\xe8\xbe\x93\xe5\x87\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe4\xbd\x8d\xe7\xa7\xbb', default=False),
       'MotionToEntity': PBool(text='\xe4\xbd\x8d\xe7\xa7\xbb\xe9\xa9\xb1\xe5\x8a\xa8', default=False),
       'MotionScale': PVector3(text='\xe4\xbd\x8d\xe7\xa7\xbb\xe7\xbc\xa9\xe6\x94\xbe', default=[1.0, 1.0, 1.0], editCondition="obj['MotionToEntity']"),
       'IgnoreGravity': PBool(text='\xe5\xbf\xbd\xe7\x95\xa5\xe9\x87\x8d\xe5\x8a\x9b\xe5\xbd\xb1\xe5\x93\x8d', default=False, editCondition="obj['MotionToEntity']"),
       'BlendIn': PFloat(text='\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4', default=0.1, min=0.0, max=1.0),
       'BlendOut': PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4', default=0.0, min=0.0, max=1.0),
       'StartTime': PFloat(text='\xe5\x8a\xa8\xe7\x94\xbb\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', precision=3),
       'EndTime': PFloat(text='\xe5\x8a\xa8\xe7\x94\xbb\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', default=1.0, precision=3),
       'RefTime': PFloat(text='\xe5\x8f\xa0\xe5\x8a\xa0\xe4\xba\x8e\xe5\x9f\xba\xe5\x87\x86\xe5\xb8\xa7', default=0.0, min=0.0, max=1.0),
       'extract': PButton(text='\xe6\x8f\x90\xe5\x8f\x96Transform', buttonText='\xe6\x8f\x90\xe5\x8f\x96'),
       'TransitType': PEnum(text='\xe6\x92\xad\xe6\x94\xbe\xe7\xb1\xbb\xe5\x9e\x8b', enumType='PlayAnimTransitType', default=3)
       }

    def initFrameData(self, frame):
        super(TAnimationRes, self).initFrameData(frame)
        frame.properties['extract'] = None
        return

    def extract(self, proxy):
        try:
            from MontageExtend.ExtController.AnimExtractController import AnimExtractController
            import Sunshine.Services
            from PyQt5.QtWidgets import QMessageBox
        except ImportError:
            return

        playbackspeed = proxy.getProperty('PlaybackSpeed')
        if playbackspeed <= 0:
            QMessageBox.warning(None, '\xe8\xad\xa6\xe5\x91\x8a', '\xe6\x9a\x82\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81\xe9\x9d\x9e\xe6\xad\xa3\xe6\x95\xb0\xe7\x9a\x84\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87')
            return
        else:
            entityproxy = proxy.getEntityAncestor()
            if not entityproxy or not entityproxy['Transform']:
                return
            animname = proxy.getProperty('name')
            if not animname:
                return
            anim = self.getAnimRes(entityproxy, animname)
            if not anim:
                return
            animpath = '/'.join(anim['path'].split('/')[:-2]) + anim['res']
            param = {'animpath': animpath,
               'starttime': proxy.getTime(),
               'duration': proxy.getDuration(),
               'oridur': proxy.getProperty('Oridur'),
               'playrate': proxy.getProperty('PlaybackSpeed')
               }
            c = AnimExtractController(param)
            transformProxy = entityproxy['Transform']
            media = Sunshine.Services.GetService('MontageService').getTransaction()
            for child in entityproxy.getChildren():
                if child.trackType == 'Transform' and media.branchHelper._getBranchOfProxy(child) == media.branchHelper.currentBranch:
                    transformProxy = child
                    break

            result = c.Extract(transformProxy)
            if result:
                proxy.setProperty('RemoveMotion', True)
            return

    @staticmethod
    def getAnimRes(entityAncestor, animname):
        try:
            import Sunshine.Services
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        resManager = mService.getResourceManager()
        if not entityAncestor.DynamicEntity:
            skeletonFile = resManager.getResByKey('Character', 'charkey', entityAncestor.getProperty('charKey'))['skeletonFile']
            animRes = resManager.getResByKey('SkeletonAnimation', 'path', '/'.join([skeletonFile, animname]))
            if animRes:
                return animRes
            skeletonFile = '_'.join(['scene_animations', entityAncestor.name])
        else:
            skeletonFile = '_'.join(['scene_animations', entityAncestor.getProperty('sceneActorName')])
        return resManager.getResByKey('SkeletonAnimation', 'path', '/'.join([skeletonFile, animname]))

    def setFrameDataByPath(self, frame, path, data):
        try:
            import Sunshine.Services
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        media = mService.getTransaction()
        frameProxy = media.getProxy(frame.uuid)
        ps = path[0]
        if ps == 'PlaybackSpeed':
            oldSpeed = frame.properties['PlaybackSpeed']
            newSpeed = data
            ratio = abs(oldSpeed / newSpeed) if newSpeed != 0 and oldSpeed != 0 else 1
            newDuration = frame.duration * ratio
            frameProxy.setDuration(newDuration)
        super(TAnimationRes, self).setFrameDataByPath(frame, path, data)
        entityAncestor = frameProxy.getEntityAncestor()
        if ps == 'name':
            anim = self.getAnimRes(entityAncestor, data)
            if anim:
                duration = float(anim['time']) / 1000.0
                frame.properties['Oridur'] = duration
                frame.properties['EndTime'] = duration
                frameProxy.setDuration(duration)

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        children = deepcopy(self.getFrameProperties())
        children['name'] = PRes(sort=35, text='\xe8\xb5\x84\xe6\xba\x90', default='', resSet='SkeletonAnimation', resType='SkeletonAnimation')
        montageService = Sunshine.Services.GetService('MontageService')
        montageService.registerTrackMeta('FRAME', self, children)

    def getIntersectedValue(self, track, time):
        hit_frames = []
        for frame in track.frames:
            startime = frame.time
            if startime <= time <= startime + frame.duration:
                hit_frames.append(frame)

        if len(hit_frames) == 0:
            return ''
        else:
            if len(hit_frames) == 1:
                return hit_frames[0].properties['name']
            return '...'

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TAnimationRes, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
        except ImportError:
            return

        resmgr = Sunshine.Services.GetService('MontageService').getResourceManager()

        def updateAnimDuration(file):
            anim = resmgr.getResByKey('SkeletonAnimation', 'path', file)
            if anim:
                duration = float(anim['time']) / 1000.0
                dynamicmeta['StartTime'] = {'min': 0.0,'max': duration}
                dynamicmeta['EndTime'] = {'min': 0.0,'max': duration}

        if not proxy.getEntityAncestor().DynamicEntity:
            charKey = proxy.getEntityAncestor().getProperty('charKey')
            res = resmgr.getResByKey('Character', 'charkey', charKey)
            if res:
                animRes = resmgr.resourceSets['SkeletonAnimation'].getResources(res['skeletonFile'])[1]
                if animRes:
                    skeletonFile = res['skeletonFile']
                    dynamicmeta['name'] = {'subDir': skeletonFile}
                else:
                    skeletonFile = '_'.join(['scene_animations', proxy.getEntityAncestor().name])
                    dynamicmeta['name'] = {'subDir': skeletonFile}
            else:
                return
        else:
            sceneObjName = proxy.getEntityAncestor().getProperty('sceneActorName')
            if sceneObjName:
                skeletonFile = '_'.join(['scene_animations', sceneObjName])
                dynamicmeta['name'] = {'subDir': skeletonFile}
            else:
                return
        filename = '/'.join([skeletonFile, proxy.getProperty('name')])
        updateAnimDuration(filename)

    def getBlendInTime(self, proxy):
        return proxy.getProperty('BlendIn', 0)

    def getBlendOutTime(self, proxy):
        return proxy.getProperty('BlendOut', 0)

    def getBlendKey(self, isBlendIn):
        if isBlendIn:
            return 'BlendIn'
        return 'BlendOut'

    def getMaxBlendTime(self, proxy):
        return 1


@TrackMeta
class TAnimationGraph(TrackMetaBase):
    ALLOW_SAMENAME = True
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Animation
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)
       }
    FRAME_PROPERTIES = {'Animation0': PRes(text='\xe5\x8a\xa8\xe7\x94\xbb0', default='', resSet='SkeletonAnimation', resType='SkeletonAnimation'),
       'BoneSelector0': PCustom(text='\xe9\x80\x89\xe6\x8b\xa9\xe9\xaa\xa8\xe9\xaa\xbc0', editAttribute='BoneSelector', default='', bonesInfo={}),
       'Animation1': PRes(text='\xe5\x8a\xa8\xe7\x94\xbb1', default='', resSet='SkeletonAnimation', resType='SkeletonAnimation'),
       'BoneSelector1': PCustom(text='\xe9\x80\x89\xe6\x8b\xa9\xe9\xaa\xa8\xe9\xaa\xbc1', editAttribute='BoneSelector', default='', bonesInfo={})
       }

    def getIntersectedValue(self, track, time):
        return ''

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TAnimationGraph, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
        except ImportError:
            return

        mService = Sunshine.Service.GetService('MontageService')
        skeletonFile = '_'.join(['scene_animations', proxy.getEntityAncestor().name])
        dynamicmeta['Animation0'] = {'subDir': skeletonFile}
        dynamicmeta['Animation1'] = {'subDir': skeletonFile}
        entityCtrl = mService.getController().entityCtrl
        entityName = proxy.getEntityAncestor().name
        entityUuid = entityCtrl.getEntityUuidByName(entityName)
        entityData = entityCtrl.getEntityData(entityUuid)
        if not entityData:
            return
        bones = entityData.get('bones', [])
        boneParentIDs = entityData.get('boneParentIDs', [])
        if bones and boneParentIDs:
            dynamicmeta.update({'BoneSelector0': {'bonesInfo': {'bones': bones,
                                               'boneParentIDs': boneParentIDs
                                               }
                                 },
               'BoneSelector1': {'bonesInfo': {'bones': bones,
                                               'boneParentIDs': boneParentIDs
                                               }
                                 }
               })


@TrackMeta
class TFacialAnimationRes(TAnimationRes):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'BoneFilter': PStr(text='\xe9\xaa\xa8\xe9\xaa\xbc\xe8\xbf\x87\xe6\xbb\xa4', default={'filterStr': ''}, visible=False)
       }

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        children = deepcopy(self.getFrameProperties())
        children['name'] = PRes(sort=35, text='\xe8\xb5\x84\xe6\xba\x90', default='', resSet='SkeletonAnimation', resType='SkeletonAnimation-Expression')
        montageService = Sunshine.Services.GetService('MontageService')
        montageService.registerTrackMeta('FRAME', self, children)


@TrackMeta
class TCamAnimationRes(TResource):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Animation
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)
       }
    FRAME_PROPERTIES = {'Oridur': PFloat(editable=False, default=1.0),
       'PauseEnd': PBool(text='\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe5\x81\x9c\xe6\xad\xa2'),
       'BeginTime': PFloat(text=translate('Montage', '\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'), default=0.0, min=0, precision=3)
       }

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        children = deepcopy(self.getFrameProperties())
        children['name'] = PRes(sort=35, text='\xe8\xb5\x84\xe6\xba\x90', default='', resSet='CameraAnimation')
        montageService = Sunshine.Services.GetService('MontageService')
        montageService.registerTrackMeta('FRAME', self, children)

    def getIntersectedValue(self, track, time):
        hit_frames = []
        for frame in track.frames:
            startime = frame.time
            if startime <= time <= startime + frame.duration:
                hit_frames.append(frame)

        if len(hit_frames) == 0:
            return ''
        else:
            if len(hit_frames) == 1:
                return hit_frames[0].properties['name']
            return '...'

    def setFrameDataByPath(self, frame, path, data):
        super(TCamAnimationRes, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        resManager = mService.getResourceManager()
        media = mService.getTransaction()
        frameProxy = media.getProxy(frame.uuid)
        ps = path[0]
        if ps == 'name':
            anim = resManager.getResByKey('CameraAnimation', 'path', data)
            if anim:
                duration = float(anim['time']) / 1000.0
                frame.properties['Oridur'] = duration
                frameProxy.setDuration(duration)


@TrackMeta
class TShakeBase(TrackMetaBase):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)}
    FRAME_PROPERTIES = {'posInfluence': PVector3(text='\xe5\xbd\xb1\xe5\x93\x8d\xe4\xbd\x8d\xe7\xbd\xae', default=(0.25, 0.25,
                                                                           0.25)),
       'rotInfluence': PVector3(text='\xe5\xbd\xb1\xe5\x93\x8d\xe8\xa7\x92\xe5\xba\xa6', default=(1.0, 1.0,
                                                                           1.0)),
       'magnitude': PFloat(text='\xe5\xbc\xba\xe5\xba\xa6', min=0, default=1.0),
       'roughness': PFloat(text='\xe9\xa2\x91\xe5\xba\xa6', min=0, default=1.0),
       'fadeIn': PFloat(text='\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4', min=0, default=0),
       'fadeOut': PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4', min=0, default=0),
       'followDirection': PBool(text='\xe6\xa0\xb9\xe6\x8d\xae\xe5\xbd\x93\xe5\x89\x8d\xe9\x95\x9c\xe5\xa4\xb4\xe6\x96\xb9\xe5\x90\x91\xe6\x8c\xaf\xe5\x8a\xa8', default=True)
       }


@TrackMeta
class TCameraShake(TShakeBase):
    s_ShakeData = [
     {'m_v3PosInfluence': (0.25, 0.25, 0.25),
        'm_v3RotInfluence': (1.0, 1.0, 1.0),
        'm_nMagnitude': 1.0,
        'm_nRoughness': 1.0,
        'm_nFadeInTime': 0.0,
        'm_nFadeOutTime': 0.0
        },
     {'m_v3PosInfluence': (0.15, 0.15, 0.15),
        'm_v3RotInfluence': (1.0, 1.0, 1.0),
        'm_nMagnitude': 2.5,
        'm_nRoughness': 4.0,
        'm_nFadeInTime': 0.1,
        'm_nFadeOutTime': 0.75
        },
     {'m_v3PosInfluence': (0.25, 0.25, 0.25),
        'm_v3RotInfluence': (4.0, 1.0, 1.0),
        'm_nMagnitude': 5.0,
        'm_nRoughness': 10.0,
        'm_nFadeInTime': 0.0,
        'm_nFadeOutTime': 1.5
        },
     {'m_v3PosInfluence': (0.25, 0.25, 0.25),
        'm_v3RotInfluence': (1.0, 1.0, 4.0),
        'm_nMagnitude': 0.6,
        'm_nRoughness': 3.5,
        'm_nFadeInTime': 2.0,
        'm_nFadeOutTime': 2.0
        },
     {'m_v3PosInfluence': (0.0, 0.0, 0.15),
        'm_v3RotInfluence': (2.0, 1.0, 4.0),
        'm_nMagnitude': 1.0,
        'm_nRoughness': 0.15,
        'm_nFadeInTime': 5.0,
        'm_nFadeOutTime': 1.0
        },
     {'m_v3PosInfluence': (0.0, 0.0, 0.0),
        'm_v3RotInfluence': (1.0, 0.5, 0.5),
        'm_nMagnitude': 1.0,
        'm_nRoughness': 0.25,
        'm_nFadeInTime': 1.0,
        'm_nFadeOutTime': 1.0
        },
     {'m_v3PosInfluence': (0.0, 0.15, 0.0),
        'm_v3RotInfluence': (1.25, 1.0, 4.0),
        'm_nMagnitude': 0.0,
        'm_nRoughness': 20.0,
        'm_nFadeInTime': 2.0,
        'm_nFadeOutTime': 2.0
        },
     {'m_v3PosInfluence': (0.0, 0.0, 0.0),
        'm_v3RotInfluence': (1.0, 1.0, 1.0),
        'm_nMagnitude': 1.0,
        'm_nRoughness': 2.0,
        'm_nFadeInTime': 1.0,
        'm_nFadeOutTime': 1.0
        }]
    s_ShakeTypes = {'0': 'Custom',
       '1': 'Bump',
       '2': 'Explosion',
       '3': 'Earthquake',
       '4': 'BadTrip',
       '5': 'HandheldCamera',
       '6': 'Vibration',
       '7': 'RoughDriving'
       }
    FRAME_PROPERTIES = {'name': PStr(visble=False, default=s_ShakeTypes['0']),
       'shakeType': PEnum(text='\xe6\x8c\xaf\xe5\x8a\xa8\xe7\xb1\xbb\xe5\x9e\x8b', enumType='CameraShakeType', default=0)
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TCameraShake, self).setFrameDataByPath(frame, path, data)
        if path[0] == 'shakeType':
            try:
                import Sunshine.Services
            except ImportError:
                return

            shakeName = self.s_ShakeTypes[str(data)]
            montage = Sunshine.Services.GetService('MontageService')
            frameProxy = montage.getTransaction().getProxy(frame.uuid)
            shakeDefault = self.s_ShakeData[data]
            frameProxy.setProperty('posInfluence', shakeDefault['m_v3PosInfluence'])
            frameProxy.setProperty('rotInfluence', shakeDefault['m_v3RotInfluence'])
            frameProxy.setProperty('magnitude', shakeDefault['m_nMagnitude'])
            frameProxy.setProperty('roughness', shakeDefault['m_nRoughness'])
            frameProxy.setProperty('fadeIn', shakeDefault['m_nFadeInTime'])
            frameProxy.setProperty('fadeOut', shakeDefault['m_nFadeOutTime'])
            frameProxy.setProperty('name', shakeName, systemname='Inspector')


@TrackMeta
class TAudioRes(TCue):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Audio
    FRAME_PROPERTIES = {'CueID': PInt(default=1, editable=False),
       'Name': PRes(sort=35, default='\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88\xe4\xba\x8b\xe4\xbb\xb6'),
       'FilePath': PStr(default='', visible=False),
       'Break': PBool(text='\xe4\xb8\xad\xe6\x96\xad\xe5\x81\x9c\xe6\xad\xa2', editable=True),
       'Follow': PBool(text='\xe8\xb7\x9f\xe9\x9a\x8f\xe8\xa7\x92\xe8\x89\xb2', editable=True),
       'Principle': PBool(text='\xe5\xbc\xba\xe5\x88\xb6\xe4\xb8\xbb\xe8\xa7\x92\xe9\x9f\xb3\xe6\x95\x88', editable=True),
       'BlendOutTime': PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4', default=0.0, editable=True, min=0, precision=3),
       'BlendOutType': PEnum(text='\xe6\xb7\xa1\xe5\x87\xba\xe7\xb1\xbb\xe5\x9e\x8b', enumType='BlendOutType', sort=1),
       'Res': PStr(default='', visible=False, editable=False),
       'Event': PStr(default='', visible=False, editable=False)
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TCue, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
        except ImportError:
            return

        resManager = Sunshine.Services.GetService('MontageService').getResourceManager()
        ps = path[0]
        if ps == 'Name':
            if data:
                audio = resManager.getResByKey('Music', 'path', data)
                frame.properties['Res'] = audio['filepath']
                frame.properties['Name'] = audio['event']
            else:
                frame.properties['Res'] = ''

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        children = deepcopy(self.getFrameProperties())
        children['Name'] = PRes(sort=35, default='\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88\xe4\xba\x8b\xe4\xbb\xb6', resSet='Music')
        montageService = Sunshine.Services.GetService('MontageService')
        montageService.registerTrackMeta('FRAME', self, children)

    @classmethod
    def Serialize(cls, model):
        p = model.properties
        res = p['Res']
        if not res:
            return ''
        _filePath = res
        _event = p['Name']
        _break = 1 if p['Break'] else 0
        _follow = 1 if p['Follow'] else 0
        _blendOutTime = p['BlendOutTime']
        _blendOutType = p['BlendOutType']
        _principle = 1 if p['Principle'] else 0
        value = '%s;%s;%d;%d;%.2f;%d;%d' % (_filePath, _event, _break, _follow, _blendOutTime, _blendOutType, _principle)
        return str(value)

    def getIntersectedValue(self, track, time):
        return ''

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TCue, self).UpdateMeta(proxy, dynamicmeta)


@TrackMeta
class TEffectRes(TCue):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Effect
    FRAME_PROPERTIES = {'CueID': PInt(default=32765, editable=False),
       'Name': PRes(sort=35, default='Effect'),
       'AttachBone': PEnum(text=translate('Montage', '\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc'), enumType='CharacterBones', default='Scene Root', multiSelection=False),
       'Duration': PFloat(text=translate('Montage', '\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88-1\xef\xbc\x9a\xe4\xb8\x8d\xe7\xbb\x93\xe6\x9d\x9f\xef\xbc\x89'), default=-1),
       'CoordinateBase': PEnum(text=translate('Montage', '\xe5\x8f\x98\xe6\x8d\xa2\xe5\x9d\x90\xe6\xa0\x87\xe7\xb3\xbb'), enumType='CoordinateBase', default=0),
       'Follow': PBool(text=translate('Montage', '\xe8\xb7\x9f\xe9\x9a\x8f\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe7\xa7\xbb\xe5\x8a\xa8'), default=True),
       'Drop': PBool(text=translate('Montage', '\xe6\x8e\x89\xe8\x90\xbd\xe5\x9c\xb0\xe9\x9d\xa2'), default=False),
       'PositionOffset': PVector3(text=translate('Montage', '\xe4\xbd\x8d\xe7\xbd\xae\xe5\x81\x8f\xe7\xa7\xbb'), default=[0.0, 0.0, 0.0]),
       'RotationOffset': PVector3(text=translate('Montage', '\xe8\xa7\x92\xe5\xba\xa6\xe5\x81\x8f\xe7\xa7\xbb'), default=[0.0, 0.0, 0.0]),
       'ScaleChange': PVector3(text=translate('Montage', '\xe7\xbc\xa9\xe6\x94\xbe\xe8\xae\xbe\xe7\xbd\xae'), default=[1.0, 1.0, 1.0], min=0.01),
       'ToTarget': PBool(text=translate('Montage', '\xe4\xbd\x9c\xe7\x94\xa8\xe4\xba\x8e\xe7\x9b\xae\xe6\xa0\x87'), default=False),
       'HardDetach': PBool(text=translate('Montage', '\xe7\xab\x8b\xe5\x8d\xb3\xe5\x8d\xb8\xe8\xbd\xbd'), default=True),
       'ActionEndDetach': PBool(text=translate('Montage', '\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8d\xb8\xe8\xbd\xbd'), default=True),
       'ScaleFree': PBool(text=translate('Montage', '\xe7\xbc\xa9\xe6\x94\xbe\xe8\x87\xaa\xe7\x94\xb1'), default=False),
       'MirrorX': PBool(text=translate('Montage', '\xe5\x85\xb3\xe4\xba\x8eX\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0'), default=False),
       'MirrorY': PBool(text=translate('Montage', '\xe5\x85\xb3\xe4\xba\x8eY\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0'), default=False),
       'MirrorZ': PBool(text=translate('Montage', '\xe5\x85\xb3\xe4\xba\x8eZ\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0'), default=False),
       'Visible': PBool(text=translate('Montage', '\xe4\xbf\x9d\xe6\x8c\x81\xe5\x8f\xaf\xe8\xa7\x81'), default=True),
       'Oneshot': PBool(text=translate('Montage', '\xe5\x8f\xaa\xe8\xa7\xa6\xe5\x8f\x91\xe4\xb8\x80\xe6\xac\xa1'), default=True),
       'Insure': PBool(text=translate('Montage', '\xe4\xbf\x9d\xe8\xaf\x81\xe8\xa7\xa6\xe5\x8f\x91'), default=True),
       'Color': PColor(text=translate('Montage', '\xe7\x89\xb9\xe6\x95\x88\xe9\xa2\x9c\xe8\x89\xb2'), default=[255, 255, 255, 255], showAlphaChannel=True),
       'Apply': PButton(text='\xe6\x93\x8d\xe4\xbd\x9c', buttonText='\xe5\xba\x94\xe7\x94\xa8\xe5\x81\x8f\xe7\xa7\xbb')
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TCue, self).setFrameDataByPath(frame, path, data)

    def addEditorMeta(self, attrs):
        try:
            import Sunshine.Services
        except ImportError:
            print "Don't call addEditorMeta at your game, use it only at Montage Editor."
            return

        children = deepcopy(self.getFrameProperties())
        children['Name'] = PRes(sort=35, default='Effect', resSet='Effect')
        montageService = Sunshine.Services.GetService('MontageService')
        montageService.registerTrackMeta('FRAME', self, children)

    def UpdateMeta(self, proxy, dynamicmeta):
        self.addEditorMeta(self.attrs)
        try:
            import Sunshine.Services
            from Montage.Backend.Transaction.MontageProxy import MontageFrameProxy
        except ImportError:
            print "Don't call addEditorMeta at your game, use it only at Montage Editor."
            return

        try:
            from ..Utils.EffectUtil import UpdateEntityBonesEnums
        except ImportError:
            print "To use Effect track's AttachBone property, make sure you update MontageImp and MontageExtend plugin!"
            return

        if isinstance(proxy, MontageFrameProxy):
            entityAncestor = proxy.getEntityAncestor()
            if entityAncestor is None:
                return
            UpdateEntityBonesEnums(entityAncestor.uuid)
        return

    @classmethod
    def Serialize(cls, model):
        p = model.properties
        fxName = p['Name']
        node = ''
        boneList = p['AttachBone']
        if not isinstance(boneList, list):
            boneList = [
             boneList]
        for k in range(len(boneList)):
            node = node + boneList[k]
            if k != len(boneList) - 1:
                node += ';'

        mode = str(p['CoordinateBase'])
        follow = '1'
        drop = '0'
        if not p['Follow']:
            follow = '0'
            if p['Drop']:
                drop = '1'
        toTarget = p['ToTarget'] or '0' if 1 else '1'
        hardDetach = p['HardDetach'] or '0' if 1 else '1'
        actionEndDetach = p['ActionEndDetach'] or '0' if 1 else '1'
        scaleFree = p['ScaleFree'] or '0' if 1 else '1'
        keepVisible = p['Visible'] or '0' if 1 else '1'
        dur = str(p['Duration'])
        data = fxName + ':' + node + ':' + dur + ':' + mode + follow + drop + toTarget + hardDetach + actionEndDetach + scaleFree + keepVisible
        minValue = 0.0005
        positionOffset = p['PositionOffset']
        pos = (positionOffset[0], positionOffset[1], positionOffset[2])
        r = 3.141592653589793 / 180
        rotationOffset = p['RotationOffset']
        rot = (rotationOffset[0] * r, rotationOffset[1] * r, rotationOffset[2] * r)
        scaleChange = p['ScaleChange']
        scale = [scaleChange[0], scaleChange[1], scaleChange[2]]
        mirrorX = p['MirrorX']
        mirrorY = p['MirrorY']
        mirrorZ = p['MirrorZ']
        if mirrorX:
            scale[0] = -scale[0]
        if mirrorY:
            scale[1] = -scale[1]
        if mirrorZ:
            scale[2] = -scale[2]
        if abs(rot[0]) > minValue or abs(rot[1]) > minValue or abs(rot[2]) > minValue:
            data += ':' + 'r%.2f,%.2f,%.2f' % (rot[0], rot[1], rot[2])
        if abs(pos[0]) > minValue or abs(pos[1]) > minValue or abs(pos[2]) > minValue:
            data += ':' + 'p%.2f,%.2f,%.2f' % (pos[0], pos[1], pos[2])
        if abs(scale[0] - 1) > minValue or abs(scale[1] - 1) > minValue or abs(scale[2] - 1) > minValue:
            data += ':' + 's%.2f,%.2f,%.2f' % (scale[0], scale[1], scale[2])
        r, g, b, a = p.get('Color')
        if r != 255 or g != 255 or b != 255 or a != 255:
            c = (r << 24) + (g << 16) + (b << 8) + a
            data += ':#' + str(c)
        return data

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback

    def Apply(self, proxy):
        if self.__class__.APPLY_CALLBACK:
            self.__class__.APPLY_CALLBACK(proxy)


@TrackMeta
class TEffectRoot(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Effect
    EDIT_TYPE = 'NO_FRAME'
    TRACK_PROPERTIES = {'Name': PStr(default='Effect', visible=False, editable=False)
       }
    _VALID_CHILDREN = [
     (
      'EffectEx', 'TEffectEx', {'allowDuplicate': True,'frametype': 1}), ('EffectFolder', 'TEffectFolder', {'allowDuplicate': True})]


@TrackMeta
class TEffectEx(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Effect
    APPLY_CALLBACK = None
    TRACK_PROPERTIES = {'CueID': PInt(default=32765, editable=False),
       'name': PStr(default='Effect', visible=True, editable=True),
       'res': PStr(default='Effect', visible=False, editable=False),
       'AttachBone': PEnum(text='\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc', enumType='CharacterBones', default='Scene Root', multiSelection=False),
       'CoordinateBase': PEnum(text='\xe5\x8f\x98\xe6\x8d\xa2\xe5\x9d\x90\xe6\xa0\x87\xe7\xb3\xbb', enumType='CoordinateBase', default=0),
       'Follow': PBool(text='\xe8\xb7\x9f\xe9\x9a\x8f\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe7\xa7\xbb\xe5\x8a\xa8', default=True),
       'Drop': PBool(text='\xe6\x8e\x89\xe8\x90\xbd\xe5\x9c\xb0\xe9\x9d\xa2', default=False),
       'ToTarget': PBool(text='\xe4\xbd\x9c\xe7\x94\xa8\xe4\xba\x8e\xe7\x9b\xae\xe6\xa0\x87', default=False),
       'HardDetach': PBool(text='\xe7\xab\x8b\xe5\x8d\xb3\xe5\x8d\xb8\xe8\xbd\xbd', default=True),
       'ActionEndDetach': PBool(text='\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xbb\x93\xe6\x9d\x9f\xe5\x8d\xb8\xe8\xbd\xbd', default=True),
       'ScaleFree': PBool(text='\xe7\xbc\xa9\xe6\x94\xbe\xe8\x87\xaa\xe7\x94\xb1', default=False),
       'MirrorX': PBool(text='\xe5\x85\xb3\xe4\xba\x8eX\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0', default=False),
       'MirrorY': PBool(text='\xe5\x85\xb3\xe4\xba\x8eY\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0', default=False),
       'MirrorZ': PBool(text='\xe5\x85\xb3\xe4\xba\x8eZ\xe8\xbd\xb4\xe5\xaf\xb9\xe7\xa7\xb0', default=False),
       'Visible': PBool(text='\xe4\xbf\x9d\xe6\x8c\x81\xe5\x8f\xaf\xe8\xa7\x81', default=True),
       'Oneshot': PBool(text='\xe5\x8f\xaa\xe8\xa7\xa6\xe5\x8f\x91\xe4\xb8\x80\xe6\xac\xa1', default=True),
       'Insure': PBool(text='\xe4\xbf\x9d\xe8\xaf\x81\xe8\xa7\xa6\xe5\x8f\x91', default=True)
       }
    FRAME_PROPERTIES = {'PositionOffset': PVector3(text='\xe6\x8c\x82\xe6\x8e\xa5\xe5\x81\x8f\xe7\xa7\xbb', default=[0.0, 0.0, 0.0]),
       'RotationOffset': PVector3(text='\xe6\x8c\x82\xe6\x8e\xa5\xe6\x97\x8b\xe8\xbd\xac', default=[0.0, 0.0, 0.0]),
       'ScaleChange': PVector3(text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\xbc\xa9\xe6\x94\xbe', default=[1.0, 1.0, 1.0], min=0.01),
       'Color': PColor(text='\xe7\x89\xb9\xe6\x95\x88\xe9\xa2\x9c\xe8\x89\xb2', default=[255, 255, 255, 255], showAlphaChannel=True),
       'Apply': PButton(text='\xe6\x93\x8d\xe4\xbd\x9c', buttonText='\xe5\xba\x94\xe7\x94\xa8\xe5\x81\x8f\xe7\xa7\xbb')
       }

    def Apply(self, proxy):
        if self.__class__.APPLY_CALLBACK:
            self.__class__.APPLY_CALLBACK(proxy)

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback

    def previewEffect(self, uuid, resstr=''):
        cb = self.__class__.getPreviewCallback('Name')
        if callable(cb):
            cb(uuid, resstr)

    def initFrameData(self, frame):
        super(TEffectEx, self).initFrameData(frame)
        frame.properties['Apply'] = None
        return

    def UpdateMeta(self, proxy, dynamicmeta):
        self.addEditorMeta(self.attrs)
        self._updateCharacterBonesEnum(proxy)

    @staticmethod
    def _updateCharacterBonesEnum(proxy):
        if proxy is not None and proxy.isValid():
            try:
                import Sunshine.Services
                from ..Utils.EffectUtil import UpdateEntityBonesEnums
            except ImportError:
                return

            entityAncestor = proxy.getEntityAncestor()
            if entityAncestor is None:
                return
            UpdateEntityBonesEnums(entityAncestor.uuid)
        return


@TrackMeta
class TEffectFolder(TrackMetaBase):
    EDIT_TYPE = 'Folder'
    _VALID_CHILDREN = [
     (
      'EffectFolder', 'TEffectFolder', {'allowDuplicate': True}),
     (
      'EffectEx', 'TEffectEx', {'allowDuplicate': True,'frametype': 1})]

    def getMetaDefaultValue--- This code section failed: ---

 960       0  BUILD_MAP_1           1 
           3  BUILD_MAP_1           1 
           6  BINARY_SUBSCR    
           7  BINARY_SUBSCR    
           8  BINARY_SUBSCR    
           9  BINARY_SUBSCR    
          10  BINARY_SUBSCR    
          11  STORE_MAP        
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 6

    def addEditorMeta(self, attrs):
        pass


@TrackMeta
class TBaseEntityActor(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Entity
    IS_ENTITY = True
    TRACK_PROPERTIES = {'HardPoint': PEnum(text='\xe7\x88\xb6\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', enumType='HardPoint', default='Scene Root'),
       'BasePoint': PEnum(text='\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', enumType='BasePoint', default='Scene Root'),
       'LookAt': PEnum(text='\xe7\x9c\x8b\xe5\x90\x91\xe5\xaf\xb9\xe8\xb1\xa1Entity', enumType='LookAtEntity', default='')
       }
    _VALID_CHILDREN = [
     (
      'CameraActor', 'TCameraActor', {'icon': ':/Montage/Camera.svg','showText': translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4')}),
     (
      'EntityActor', 'TEntityActor', {'icon': ':/Montage/Entity.svg','showText': translate('Montage', '\xe8\xa7\x92\xe8\x89\xb2')}),
     ('Dummy', 'TDummy'),
     ('EffectEntity', 'TEffectEntity'),
     (
      'PointLight', 'TPointLight', {'showText': translate('Montage', '\xe7\x82\xb9\xe5\x85\x89\xe6\xba\x90')}),
     (
      'SpotLight', 'TSpotLight', {'showText': translate('Montage', '\xe8\x81\x9a\xe5\x85\x89\xe7\x81\xaf')}),
     (
      'Transform', 'TTransform', {'allowDuplicate': False,'defaultvisible': True})]

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TBaseEntityActor, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
            from Montage.Backend.Transaction.MontageProxy import MontageFrameProxy
        except ImportError:
            print "Don't call UpdateMeta at your game, use it only at Montage Editor."
            return

        if isinstance(proxy, MontageTrackProxy):
            parent = proxy.getParent()
            if parent is not None and parent.meta.IS_ENTITY:
                self._updateEnum(parent, 'HardPoint')
            else:
                self._updateEnum(None, 'HardPoint')
            self._updateEnum(proxy, 'BasePoint')
            self._updateEnum(proxy, 'LookAtEntity')
        return

    def _updateEnum(self, proxy, enumName):
        try:
            from ..Utils.EffectUtil import UpdateEntityBonesEnums
            from ..Utils.MetaUtil import UpdateChildAttachModelEnums
            import Sunshine.Services
        except ImportError:
            print 'TBaseEntityActor Update Meta Error'
            return

        if enumName in ('HardPoint', 'BasePoint'):
            if proxy is not None:
                UpdateEntityBonesEnums(proxy.uuid, enumName)
            else:
                montage = Sunshine.Services.GetService('MontageService')
                montage.addMontageEnumDefine(enumName, ['', 'Scene Root'])
        else:
            UpdateChildAttachModelEnums(proxy.uuid, 'LookAtEntity')
        return


@TrackMeta
class TBaseLight(TBaseEntityActor):
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN + [
     (
      'Color', 'TColor3', {'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'Intensity',
      'TFloat', {'default': 5.0,'min': 0,'max': 30,'precision': 4,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'Lumens',
      'TFloat', {'default': 1000,'min': 0,'max': 2100,'precision': 3,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'Temperature', 'TFloat', {'default': 5500,'min': 1700,'max': 12000,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'Range', 'TFloat', {'default': 5.0,'min': 0.01,'max': 10000,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'Hidden', 'TBool', {'default': False,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.Cue})]

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        montageService = Sunshine.Services.GetService('MontageService')
        children = deepcopy(self.getTrackProperties())
        children[attrs['trackName']] = PDict(children={'Color': PColor()})
        montageService.registerTrackMeta('TRACK', self, children)
        self._TRACK_META = PDict(children=children)
        children = deepcopy(self.getFrameProperties())
        children[attrs['trackName']] = PDict(children={'Color': PColor()})
        montageService.registerTrackMeta('FRAME', self, children)
        self._FRAME_META = PDict(children=children)
        colorMeta = GetTrackMetaCls('TColor3')
        if colorMeta:
            colorMeta.updatePreviewCallback('Color', self.__class__.getPreviewCallback('Color'))
        super(TBaseLight, self).addEditorMeta(attrs)


@TrackMeta
class TPointLight(TBaseLight):
    _VALID_CHILDREN = TBaseLight._VALID_CHILDREN


@TrackMeta
class TSpotLight(TBaseLight):
    _VALID_CHILDREN = TBaseLight._VALID_CHILDREN + [
     (
      'InnerAngle', 'TFloat', {'default': 60,'min': 0,'max': 360,'allowDuplicate': False}),
     (
      'OutAngle', 'TFloat', {'default': 90,'min': 0,'max': 360,'allowDuplicate': False})]


@TrackMeta
class TCameraNoise(TrackMetaBase):
    ALLOW_SAMENAME = True
    _VALID_CHILDREN = [('Transform', 'TCamTransform', {'defaultvisible': True,'allowDuplicate': False})]
    TRACK_PROPERTIES = {'start': PFloat(text='\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', min=0),
       'duration': PFloat(text='\xe6\x97\xb6\xe9\x95\xbf', default=10.0, min=0),
       'freq': PFloat(text='\xe9\xa2\x91\xe7\x8e\x87(Hz)', default=2.0, min=0),
       'freqrange': PFloat(text='\xe9\xa2\x91\xe7\x8e\x87\xe5\x8f\x98\xe5\x8c\x96\xe5\xb9\x85\xe5\xba\xa6(Hz)', default=0.5, min=0),
       'hmax': PFloat(text='\xe6\xb0\xb4\xe5\xb9\xb3\xe5\xb9\x85\xe5\xba\xa6(\xe8\xa7\x92\xe5\xba\xa6)', default=1.0, min=0),
       'vmax': PFloat(text='\xe5\x9e\x82\xe7\x9b\xb4\xe5\xb9\x85\xe5\xba\xa6(\xe8\xa7\x92\xe5\xba\xa6)', default=1.0, min=0),
       'generate': PButton(text='\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\x99\xaa\xe5\xa3\xb0', buttonText='\xe7\x94\x9f\xe6\x88\x90')
       }

    def generate(self, proxy):
        from MontageExtend.ExtController.NoiseController import NoiseController
        param = {'freq': proxy.getProperty('freq'),
           'hmax': proxy.getProperty('hmax'),
           'freqrange': proxy.getProperty('freqrange'),
           'vmax': proxy.getProperty('vmax')
           }
        st = proxy.getProperty('start')
        duration = proxy.getProperty('duration')
        c = NoiseController(None, param)
        c.createNoise(proxy, st, duration)
        return


@TrackMeta
class TCameraAim(TrackMetaBase):
    ALLOW_SAMENAME = True
    FRAME_PROPERTIES = {'target': PEnum(text='\xe5\xaf\xb9\xe8\xb1\xa1\xe5\x90\x8d\xe5\xad\x97', enumType='CurrentNPCList'),
       'horizontalDamping': PFloat(text='\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x98\xbb\xe5\xb0\xbc', default=0.1, min=0, max=1),
       'verticalDamping': PFloat(text='\xe5\x9e\x82\xe7\x9b\xb4\xe9\x98\xbb\xe5\xb0\xbc', default=0.1, min=0, max=1),
       'softZoneWidth': PFloat(text='\xe8\xbd\xaf\xe5\x8c\xba\xe5\xae\xbd\xe5\xba\xa6', default=0.5, min=0, max=1),
       'softZoneHeight': PFloat(text='\xe8\xbd\xaf\xe5\x8c\xba\xe9\xab\x98\xe5\xba\xa6', default=0.5, min=0, max=1),
       'deadZoneWidth': PFloat(text='\xe6\xad\xbb\xe5\x8c\xba\xe5\xae\xbd\xe5\xba\xa6', default=0.3, min=0, max=1),
       'deadZoneHeight': PFloat(text='\xe6\xad\xbb\xe5\x8c\xba\xe9\xab\x98\xe5\xba\xa6', default=0.3, min=0, max=1),
       'offsetX': PFloat(text='\xe5\x81\x8f\xe7\xa7\xbbX', default=0, min=0, max=1),
       'offsetY': PFloat(text='\xe5\x81\x8f\xe7\xa7\xbbY', default=0, min=0, max=1),
       'autoFocus': PBool(text='\xe8\x87\xaa\xe5\x8a\xa8\xe5\xaf\xb9\xe7\x84\xa6', default=False)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TCameraAim, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            tracks = mService.getTransaction().getAllEntityTracks()
            npcList = [ t.name for t in tracks if t.trackType in ('EntityActor', 'Dummy') ]
            npcList.append('None')
            mService.addMontageEnumDefine('CurrentNPCList', npcList)
        except ImportError:
            return

    def getIntersectedValue(self, track, time):
        hit_frames = []
        for frame in track.frames:
            startime = frame.time
            if startime <= time <= startime + frame.duration:
                hit_frames.append(frame)

        if len(hit_frames) == 0:
            return ''
        else:
            if len(hit_frames) == 1:
                return {'CameraAim': hit_frames[0].properties}
            return '...'

    def setFrameDataByPath(self, frame, path, data):
        super(TCameraAim, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
            import MontageExtend
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        frameProxy = mService.getTransaction().getProxy(frame.uuid)
        camerProxy = frameProxy.getEntityAncestor()
        ctrl = mService.getController()
        if camerProxy.name != ctrl.previewCamera:
            return
        if frame.time <= ctrl.currentSceneTime < frame.time + frame.duration:
            MontageExtend.Controller.controllers['AimController'].RefreshCameraAimUI()


@TrackMeta
class TEntityBinding(TrackMetaBase):
    TRACK_PROPERTIES = {'name': PStr(editable=False, text='\xe5\x90\x8d\xe7\xa7\xb0'),
       'bindObject': PRes(resSet='Character', text='\xe7\xbb\x91\xe5\xae\x9a\xe7\x89\xa9\xe4\xbb\xb6', default='EMPTY'),
       'bindType': PEnum(enumType='BindType', text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe7\xb1\xbb\xe5\x9e\x8b', default=0),
       'bindSocket': PEnum(enumType='SocketList', text='\xe7\xbb\x91\xe5\xae\x9a\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe5\x90\x8d\xe7\xa7\xb0', default='None')
       }
    FRAME_PROPERTIES = {'BindNPCName': PEnum(text='\xe7\xbb\x91\xe5\xae\x9a\xe7\x89\xa9\xe4\xbb\xb6', enumType='CurrentNPCList', default='None'),
       'BindType': PEnum(enumType='BindType', text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe7\xb1\xbb\xe5\x9e\x8b', default=0),
       'SocketName': PEnum(text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe5\x90\x8d\xe7\xa7\xb0', enumType='SocketList', default='None'),
       'BindingOffset': PVector3(text='\xe4\xbd\x8d\xe7\xbd\xae\xe5\x81\x8f\xe7\xa7\xbb', default=(0.0, 0.0,
                                                                           0.0)),
       'RotationOffset': PVector3(text='\xe8\xa7\x92\xe5\xba\xa6\xe5\x81\x8f\xe7\xa7\xbb', default=(0.0, 0.0,
                                                                           0.0), min=-180.0, max=+180.0)
       }

    def setTrackDataByPath(self, track, path, data):
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            resManager = mService.getResourceManager()
        except ImportError:
            return

        ps = path[-1]
        if ps == 'bindObject':
            if not data:
                track.properties['bindObject'] = ''
            res = resManager.getResByKey('Character', 'path', data)
            if not res:
                return
            if res['charkey'] != track.properties['bindObject']:
                track.properties['bindObject'] = res['charkey']
        elif ps == 'bindType':
            track.properties['bindSocket'] = 'None'
            super(TEntityBinding, self).setTrackDataByPath(track, path, data)
            mService.getController().inspectorCtrl.refresh()
        else:
            super(TEntityBinding, self).setTrackDataByPath(track, path, data)

    def setFrameDataByPath(self, frame, path, data):
        if path[-1] == 'BindNPCName':
            try:
                import Sunshine.Services
                mservice = Sunshine.Services.GetService('MontageService')
            except ImportError:
                return

            if frame.properties['BindNPCName'] != data:
                frame.properties['SocketName'] = 'None'
            mservice.getController().inspectorCtrl.refresh()
        elif path[-1] == 'BindType':
            try:
                import Sunshine.Services
                mservice = Sunshine.Services.GetService('MontageService')
            except ImportError:
                return

            frame.properties['SocketName'] = 'None'
            mservice.getController().inspectorCtrl.refresh()
        super(TEntityBinding, self).setFrameDataByPath(frame, path, data)

    def UpdateMeta(self, proxy, dynamicmeta):
        try:
            import Sunshine.Services
            from Montage.Backend.Transaction.MontageProxy import MontageFrameProxy
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        entityCtrl = mService.getController().entityCtrl
        if isinstance(proxy, MontageFrameProxy):
            entity = proxy.getEntityAncestor()
            entityTrackProxys = mService.getTransaction().getAllEntityTracks()
            entityNames = [ t.name for t in entityTrackProxys if t.trackType == 'EntityActor' ]
            entityNames.remove(entity.name)
            if 'None' not in entityNames:
                entityNames.append('None')
            mService.addMontageEnumDefine('CurrentNPCList', entityNames)
            name = proxy.getProperty('BindNPCName')
            bindType = proxy.getProperty('BindType')
            if not name or name == 'None':
                mService.addMontageEnumDefine('SocketList', ['None'])
                return
        else:
            name = proxy.getEntityAncestor().name
            bindType = proxy.getProperty('bindType')
        entityUuid = entityCtrl.getEntityUuidByName(name)
        data = entityCtrl.getEntityData(entityUuid)
        if not data:
            return
        enumData = []
        if bindType == 0:
            enumData = data.get('sockets', [])
        elif bindType == 1:
            enumData = data.get('bones', [])
        if 'None' not in enumData:
            enumData.append('None')
        mService.addMontageEnumDefine('SocketList', enumData)


@TrackMeta
class TMouthShapes(TSpanCue):
    ALLOW_SAMENAME = True
    BEGIN_CUEID = CueID.MOUTH_SHAPES
    END_CUID = CueID.MOUTH_SHAPES
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False),
       'generateMouthShape': PCustom(editAttribute='GenerateMouthShape', text='\xe7\x94\x9f\xe6\x88\x90\xe5\x8f\xa3\xe5\x9e\x8b')
       }
    FRAME_PROPERTIES = {'mouthShape': PRes(text='\xe5\x8f\xa3\xe5\x9e\x8b\xe6\x96\x87\xe4\xbb\xb6', default='', visible=True, resSet='MouthShapeGraph')
       }

    @classmethod
    def GetBeginArgs(cls, proxy):
        shape = proxy.getProperty('mouthShape', '')
        return str('1:' + shape)

    @classmethod
    def GetEndArgs(cls, proxy):
        return str('0:')

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TMouthShapes, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta['generateMouthShape'] = {'uuid': proxy.uuid}

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback


@TrackMeta
class TCameraActor(TBaseEntityActor):
    TRACK_PROPERTIES = {'lookAtVOffset': PFloat(sort=15, text='\xe5\x9e\x82\xe7\x9b\xb4\xe5\x81\x8f\xe7\xa7\xbb', default=0, min=-0.5, max=0.5, step=0.001),
       'lookAtHOffset': PFloat(sort=16, text='\xe6\xb0\xb4\xe5\xb9\xb3\xe5\x81\x8f\xe7\xa7\xbb', default=0, min=-0.5, max=0.5, step=0.001)
       }
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN[:-1] + [
     (
      'Transform', 'TCamTransform', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'CamAnimation',
      'TCamAnimationRes',
      {'showText': 'Animation',
         'allowDuplicate': False,
         'frametype': 1,
         'default': ''
         }),
     (
      'CamShake', 'TCameraShake', {'frametype': 1,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'FocalLength', 'TFloat', {'showText': '\xe7\x84\xa6\xe6\xae\xb5(FocalLength)','default': 30.5,'allowDuplicate': False}),
     (
      'FocalDis', 'TFocusDistance', {'showText': '\xe7\x89\xa9\xe8\xb7\x9d(FocalDis)','default': 10,'allowDuplicate': False}),
     (
      'Aperture', 'TFloat', {'showText': '\xe5\x85\x89\xe5\x9c\x88(Aperture)','default': 2.8,'allowDuplicate': False}),
     (
      'Fov', 'TFloat', {'default': 42.968,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'FocalDistance', 'TFloat', {'default': 0,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'FocalRegion', 'TFloat', {'default': 50,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'NearTstRegion', 'TFloat', {'default': 0,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'FarTstRegion', 'TFloat', {'default': 50,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'Blurriness', 'TFloat', {'default': 1,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx,'visible': False}),
     (
      'CameraNoise', 'TCameraNoise', {'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'CameraAim', 'TCameraAim', {'allowDuplicate': False,'frametype': 1,'EditorTrackColorType': EditorTrackColorType.EntityEx}),
     (
      'SmartCamera', 'TSmartCamera', {'allowDuplicate': False,'frametype': 1,'EditorTrackColorType': EditorTrackColorType.EntityEx})]

    def setTrackDataByPath(self, track, path, data):
        oldValue = self.getDataByPath(track, path)
        super(TCameraActor, self).setTrackDataByPath(track, path, data)
        ps = path[0]
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            media = mService.getTransaction()
        except:
            return

        if ps == 'name':
            if mService.getController().previewCamera == oldValue:
                mService.getController().previewCamera = data
            shotTrack = media.montageRootProxy['Shot']
            if shotTrack:
                shotTrack.meta.UpdateMeta(shotTrack, None)
                for frameProxy in shotTrack.getFrames():
                    if frameProxy.getProperty('name') == oldValue:
                        frameProxy.setProperty('name', data)

            for track in media.sceneRootProxy.getChildren():
                if track.isValid() and track.trackType == 'Director':
                    for f in track.getFrames():
                        if f.getProperty('name') == oldValue:
                            f.setProperty('name', data)

        return


@TrackMeta
class TEntityActor(TBaseEntityActor):
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN + [('Animation', 'TAnimationRes', {'frametype': 2,'allowDuplicate': False,'default': '','defaultvisible': True}), ('AnimationGraph', 'TAnimationGraph', {'frametype': 1,'allowDuplicate': False,'default': ''}), ('FacialAnimation', 'TFacialAnimationRes', {'frametype': 2,'allowDuplicate': True,'default': '','defaultvisible': False}), ('Hidden', 'TBool', {'default': False,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.Cue}), ('Effect', 'TEffectRes', {'default': ''}), ('EffectRoot', 'TEffectRoot', {'default': '','allowDuplicate': False}), ('Audio', 'TAudioRes', {'default': ''}), ('Cue', 'TCue', {'default': ''}), ('Bind', 'TEntityBinding', {'frametype': 1,'allowDuplicate': False,'showText': '\xe7\xbb\x91\xe5\xae\x9a\xe7\x89\xa9\xe4\xbb\xb6','EditorTrackColorType': EditorTrackColorType.EntityEx}), ('MouthShapes', 'TMouthShapes', {'frametype': 1,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.EntityEx}), ('Weapon', 'TWeaponActor', {'showText': translate('Montage', '\xe6\xad\xa6\xe5\x99\xa8'),'EditorTrackColorType': EditorTrackColorType.EntityEx})] + CustomEntityTracks
    TRACK_PROPERTIES = {'storylineID': PStr(text='StorylineID'),
       'incarnatedKey': PEnum(text='\xe5\x8c\x96\xe8\xba\xab', enumType='IncarnationType', default=0),
       'initPosition': PVector3(visible=False),
       'generate': PButton(text='\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe8\xb7\xaf\xe5\xbe\x84', buttonText='\xe7\x94\x9f\xe6\x88\x90'),
       'charKey': PRes(text='\xe8\xa7\x92\xe8\x89\xb2', default='EMPTY', resSet='Character', resType='Character'),
       'sceneActorName': PStr(visible=False),
       'isDynamicShadow': PEnum(text='\xe6\x98\xaf\xe5\x90\xa6\xe6\x8a\x95\xe5\xb0\x84\xe5\x8a\xa8\xe6\x80\x81\xe9\x98\xb4\xe5\xbd\xb1', enumType='DynamicShadowType', default=0),
       'receiveShadow': PEnum(text='\xe6\x98\xaf\xe5\x90\xa6\xe6\x8e\xa5\xe5\x8f\x97\xe9\x98\xb4\xe5\xbd\xb1', enumType='DynamicShadowType', default=0),
       'warmUp': PBool(text='\xe8\xbd\xa8\xe9\x81\x93\xe9\xa2\x84\xe7\x83\xad(Neox)', default=False)
       }

    def generate(self, proxy):
        try:
            from MontageExtend.ExtController.AutoMoveController import AutoMoveController
        except ImportError:
            return

        c = AutoMoveController(proxy)
        c.getInput(proxy)

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TEntityActor, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta.update({'initData': {'visible': False}})
        if proxy.DynamicEntity:
            dynamicmeta.update({'charKey': {'visible': False}})

    def setTrackDataByPath(self, track, path, data):
        try:
            import Sunshine.Services
        except ImportError:
            return

        mService = Sunshine.Services.GetService('MontageService')
        resManager = mService.getResourceManager()
        media = mService.getTransaction()
        ps = path[0]
        if ps == 'charKey':
            track.properties['name'] = media.getValidName(data)
            res = resManager.getResByKey('Character', 'name', data)
            if res:
                track.properties['charKey'] = res['charkey']
        elif ps == 'incarnatedKey':
            actor0Track = media.getActor0Track()
            if actor0Track:
                actor0Track.setProperty('incarnatedKey', 0)
            super(TEntityActor, self).setTrackDataByPath(track, path, data)
        else:
            super(TEntityActor, self).setTrackDataByPath(track, path, data)

    def _initData(self, model, meta):
        oldValue = model.properties.get('isDynamicShadow', None)
        if type(oldValue) == bool:
            newValue = 1 if oldValue else 2
            model.properties['isDynamicShadow'] = newValue
        super(TEntityActor, self)._initData(model, meta)
        return


@TrackMeta
class TWeaponActor(TEntityActor):
    _VALID_CHILDREN = [
     (
      'Hidden', 'TBool', {'default': False,'allowDuplicate': False,'defaultvisible': True})]
    TRACK_PROPERTIES = {'storylineID': PStr(text='StorylineID', visible=False),
       'incarnatedKey': PEnum(text='\xe5\x8c\x96\xe8\xba\xab', enumType='IncarnationType', default=0, visible=False),
       'initData': PDict(visible=False, children={}),
       'initPosition': PVector3(visible=False),
       'generate': PButton(text='\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe8\xb7\xaf\xe5\xbe\x84', buttonText='\xe7\x94\x9f\xe6\x88\x90', visible=False),
       'sceneActorName': PStr(visible=False),
       'HardPoint': PEnum(text='\xe6\xad\xa6\xe5\x99\xa8\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9', enumType='WeaponPoint', default=''),
       'BasePoint': PEnum(text='\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', enumType='BasePoint', default='HP_wq001', visible=False),
       'LookAt': PEnum(text='\xe7\x9c\x8b\xe5\x90\x91\xe5\xaf\xb9\xe8\xb1\xa1Entity', enumType='LookAtEntity', default='', visible=False),
       'charKey': PRes(text='\xe6\xad\xa6\xe5\x99\xa8', default='EMPTY', resSet='Character', resType='Weapon')
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TWeaponActor, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
            from Montage.Backend.Transaction.MontageProxy import MontageFrameProxy
        except ImportError:
            print "Don't call UpdateMeta at your game, use it only at Montage Editor."
            return

        if isinstance(proxy, MontageTrackProxy):
            mService = Sunshine.Services.GetService('MontageService')
            resManager = mService.getResourceManager()
            res = resManager.getResByKey('Character', 'charkey', proxy.getProperty('charKey'))
            weaponPoint = res['weaponPoint']
            weaponPoint.insert(0, '')
            mService.addMontageEnumDefine('WeaponPoint', weaponPoint)

    def setTrackDataByPath(self, track, path, data):
        super(TWeaponActor, self).setTrackDataByPath(track, path, data)
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
        except:
            return

        if path[0] == 'HardPoint':
            media = mService.getTransaction()
            proxy = media.getProxy(track.uuid)
            resManager = mService.getResourceManager()
            res = resManager.getResByKey('Character', 'charkey', proxy.getProperty('charKey'))
            if not res:
                return
            if res['name'] in ('AK', '95'):
                track.properties['BasePoint'] = 'HP_Hand'


@TrackMeta
class TDummy(TBaseEntityActor):
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN + [
     (
      'Hidden', 'TBool', {'default': False,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.Cue}),
     (
      'Effect', 'TEffectRes', {'default': ''}),
     (
      'EffectRoot', 'TEffectRoot', {'default': '','allowDuplicate': False}),
     (
      'Audio', 'TAudioRes', {'default': ''}),
     (
      'Cue', 'TCue', {'default': ''})]
    TRACK_PROPERTIES = {'initData': PDict(visible=False, children={}),'initPosition': PVector3(visible=False),'charKey': PStr(default='0:9', visible=False)}


@TrackMeta
class TEffectBind(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.EntityEx
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)}
    FRAME_PROPERTIES = {'BindNPCName': PEnum(text='\xe7\xbb\x91\xe5\xae\x9aNPC', default='None', enumType='CurrentNPCList'),
       'SocketName': PEnum(text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe5\x90\x8d\xe7\xa7\xb0', enumType='SocketList', default='None'),
       'EndNPCName': PEnum(text='\xe9\x93\xbe\xe6\x8e\xa5NPC', default='None', enumType='CurrentNPCList'),
       'EndSocketName': PEnum(text='\xe9\x93\xbe\xe6\x8e\xa5\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9\xe5\x90\x8d\xe7\xa7\xb0', enumType='SocketListOther', default='None'),
       'PositionOffset': PVector3(sort=7, text='\xe4\xbd\x8d\xe7\xbd\xae\xe5\x81\x8f\xe7\xa7\xbb', default=(0.0,
                                                                                   0.0,
                                                                                   0.0)),
       'RotationOffset': PVector3(sort=8, text='\xe8\xa7\x92\xe5\xba\xa6\xe5\x81\x8f\xe7\xa7\xbb', default=(0.0,
                                                                                   0.0,
                                                                                   0.0), min=-180.0, max=+180.0)
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TEffectBind, self).setFrameDataByPath(frame, path, data)
        if path[0] in ('BindNPCName', 'EndNPCName'):
            try:
                import Sunshine.Services
                mService = Sunshine.Services.GetService('MontageService')
                frameProxy = mService.getTransaction().getProxy(frame.uuid)
                if path[0] == 'BindNPCName':
                    frameProxy.setProperty('SocketName', 'None')
                else:
                    frameProxy.setProperty('EndSocketName', 'None')
                mService.getController().inspectorCtrl.refresh()
            except ImportError:
                return

    def UpdateMeta(self, proxy, dynamicmeta):
        import Sunshine.Services
        mService = Sunshine.Services.GetService('MontageService')
        entityTrackProxys = mService.getTransaction().getAllEntityTracks()
        entityNames = [ t.name for t in entityTrackProxys if t.trackType == 'EntityActor' ]
        if 'None' not in entityNames:
            entityNames.append('None')
        mService.addMontageEnumDefine('CurrentNPCList', entityNames)
        bindNPCName = proxy.getProperty('BindNPCName')
        if bindNPCName != 'None' and bindNPCName in entityNames:
            mService = Sunshine.Services.GetService('MontageService')
            entityCtrl = mService.getController().entityCtrl
            uuid = entityCtrl.getEntityUuidByName(bindNPCName)
            data = entityCtrl.getEntityData(uuid)
            if not data:
                return
            sockets = data.get('sockets', [])
            sockets.append('None')
            mService.addMontageEnumDefine('SocketList', sockets)
        endNPCName = proxy.getProperty('EndNPCName')
        if endNPCName != 'None' and endNPCName in entityNames:
            mService = Sunshine.Services.GetService('MontageService')
            entityCtrl = mService.getController().entityCtrl
            uuid = entityCtrl.getEntityUuidByName(endNPCName)
            data = entityCtrl.getEntityData(uuid)
            if not data:
                return
            sockets = data.get('sockets', [])
            sockets.append('None')
            mService.addMontageEnumDefine('SocketListOther', sockets)


@TrackMeta
class TRenameBool(TBool):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.EntityEx
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)}


@TrackMeta
class TEffectEntity(TBaseEntityActor):
    IS_ENTITY = True
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN + [
     (
      'Activate', 'TRenameBool', {'default': True,'allowDuplicate': False,'frametype': 1}),
     (
      'Loop', 'TRenameBool', {'default': True,'allowDuplicate': False}),
     (
      'Bind', 'TEffectBind', {'allowDuplicate': False,'frametype': 1}),
     (
      'Hidden', 'TBool', {'default': False,'allowDuplicate': False,'EditorTrackColorType': EditorTrackColorType.Cue})]
    TRACK_PROPERTIES = {'BasePoint': PEnum(text='\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', visible=False, enumType='BasePoint', default='Scene Root'),
       'LookAt': PEnum(text='\xe7\x9c\x8b\xe5\x90\x91\xe5\xaf\xb9\xe8\xb1\xa1Entity', enumType='LookAtEntity', default='', visible=False),
       'Loop': PBool(text='\xe5\xbe\xaa\xe7\x8e\xaf\xe7\x89\xb9\xe6\x95\x88', default=True, visible=False),
       'effect': PRes(text='\xe7\x89\xb9\xe6\x95\x88', default='EMPTY', resSet='Effect'),
       'sceneActorName': PStr(visible=False)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TEffectEntity, self).UpdateMeta(proxy, dynamicmeta)
        if proxy.getProperty('sceneActorName'):
            dynamicmeta.update({'effect': {'visible': False}})


@TrackMeta
class TEnvParam(TrackMetaBase):
    IS_ENTITY = True


@TrackMeta
class TSceneRoot(TSceneRootBase):
    _VALID_CHILDREN = TSceneRootBase._VALID_CHILDREN + [('CameraActor', 'TCameraActor', {'icon': ':/Montage/Camera.svg','showText': translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4')}), ('EntityActor', 'TEntityActor', {'icon': ':/Montage/Entity.svg','showText': translate('Montage', '\xe8\xa7\x92\xe8\x89\xb2')}), ('Dummy', 'TDummy'), ('EffectEntity', 'TEffectEntity'), ('PointLight', 'TPointLight', {'showText': translate('Montage', '\xe7\x82\xb9\xe5\x85\x89\xe6\xba\x90')}), ('SpotLight', 'TSpotLight', {'showText': translate('Montage', '\xe8\x81\x9a\xe5\x85\x89\xe7\x81\xaf')}), ('Cue', 'TCue'), ('Audio', 'TAudioRes', {'showText': translate('Montage', '\xe9\x9f\xb3\xe9\xa2\x91')}), ('EnvParam', 'TEnvParam'), ('DollyTrack', 'TDollyTrack'), ('Clip', 'TClip', {'frametype': 1,'allowDuplicate': False})] + CustomSceneTracks


@TrackMeta
class TDollyTrack(TFloat):
    ALLOW_SAMENAME = False
    IS_ENTITY = True
    EDIT_TYPE = 'Float'
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=True),
       'wayPoints': PArray(text='\xe8\xb7\xaf\xe7\xa8\x8b\xe5\x9f\xba\xe5\x87\x86\xe7\x82\xb9', childAttribute=PDict(default={'X': 0,
                     'xTan': 0,
                     'Y': 0,
                     'yTan': 0,
                     'Z': 0,
                     'zTan': 0,
                     'Roll': 0,
                     'Pitch': 0,
                     'Yaw': 0
                     }, children=OrderedProperties([
                   (
                    'X', PFloat(visible=True)),
                   (
                    'xTan', PFloat(visible=True)),
                   (
                    'Y', PFloat(visible=True)),
                   (
                    'yTan', PFloat(visible=True)),
                   (
                    'Z', PFloat(visible=True)),
                   (
                    'zTan', PFloat(visible=True)),
                   (
                    'Roll', PFloat(visible=True)),
                   (
                    'Pitch', PFloat(visible=True)),
                   (
                    'Yaw', PFloat(visible=True))])))
       }
    FRAME_PROPERTIES = {'value': PFloat(text='\xe8\xb7\xaf\xe7\xa8\x8b\xe6\xaf\x94\xe7\x8e\x87(Ratio)', min=0, max=100)}

    def setTrackDataByPath(self, track, path, data):
        if path[0] == 'wayPoints':
            if isinstance(data, (dict, list)):
                if len(track.properties[path[0]]) < len(data):
                    import Montage
                    import functools
                    Montage.RPC.GetCameraTransform().on_result(functools.partial(self._snapTrackAtSceneCenter, track, len(data) - 1))
        oldValue = self.getDataByPath(track, path)
        super(TDollyTrack, self).setTrackDataByPath(track, path, data)
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            media = mService.getTransaction()
        except:
            return

        if path[0] == 'name':
            shotTrack = media.montageRootProxy['Shot']
            if not shotTrack:
                return
            shotTrack.meta.UpdateMeta(shotTrack, None)
            for frameProxy in shotTrack.getFrames():
                if frameProxy.getProperty('name') == oldValue:
                    frameProxy.setProperty('name', data)

            for track in media.sceneRootProxy.getChildren():
                if track.isValid() and track.trackType == 'Director':
                    for f in track.getFrames():
                        if f.getProperty('name') == oldValue:
                            f.setProperty('name', data)

        return

    def _snapTrackAtSceneCenter(self, track, index, transform):
        wayPoints = track.properties['wayPoints']
        wayPoints[index].update(transform['Translation'])
        wayPoints[index].update(transform['Rotation'])
        track.properties['wayPoints'] = wayPoints


@TrackMeta
class TSmartCamera(TrackMetaBase):
    ALLOW_SAMENAME = True
    _AIM_PARAMS = ('softZoneWidth', 'softZoneHeight', 'deadZoneWidth', 'deadZoneHeight',
                   'offsetX', 'offsetY')
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False)
       }
    FRAME_PROPERTIES = {'name': PRes(text='\xe9\x80\x89\xe6\x8b\xa9\xe9\xa2\x84\xe8\xae\xbe', resSet='CameraPrefab', default=''),
       'Transform': PDict(children={'Translation': PVector3(default=(0.0, 0.0, 0.0), step=0.1),
                     'Rotation': PVector3(default=(0.0, 0.0, 0.0), step=0.1)
                     }),
       '_SnapCamera': PButton(text='\xe9\x95\x9c\xe5\xa4\xb4\xe5\xbf\xab\xe7\x85\xa7', buttonText='\xe5\xbf\xab\xe7\x85\xa7'),
       'FocalLength': PFloat(text='\xe7\x84\xa6\xe6\xae\xb5(FocalLength)', default=30.5),
       'Aperture': PFloat(text='\xe5\x85\x89\xe5\x9c\x88(Aperture)', default=2.8),
       'FocalDis': PFloat(text='\xe7\x89\xa9\xe8\xb7\x9d(FocalDis)', default=10),
       'Fov': PFloat(text='\xe8\xa7\x86\xe5\x9c\xba\xe8\xa7\x92(FoV)', default=60, visible=False),
       'FocalRegion': PFloat(text='\xe7\x84\xa6\xe7\x82\xb9\xe8\x8c\x83\xe5\x9b\xb4', default=50, visible=False),
       'FarTstRegion': PFloat(text='\xe5\x90\x8e\xe7\x84\xa6\xe8\x8c\x83\xe5\x9b\xb4', default=50, visible=False),
       'FocalDistance': PFloat(text='\xe5\xbd\x93\xe5\x89\x8d\xe7\x84\xa6\xe8\xb7\x9d', default=0, visible=False),
       '_Focus': PButton(text='\xe5\xaf\xb9\xe7\x84\xa6', buttonText='\xe5\xaf\xb9\xe7\x84\xa6'),
       'target': PEnum(text='LookAt\xe7\x9b\xae\xe6\xa0\x87', enumType='CurrentNPCList', default='None'),
       'horizontalDamping': PFloat(text='\xe6\xb0\xb4\xe5\xb9\xb3\xe9\x98\xbb\xe5\xb0\xbc', default=0.1, min=0, max=1),
       'verticalDamping': PFloat(text='\xe5\x9e\x82\xe7\x9b\xb4\xe9\x98\xbb\xe5\xb0\xbc', default=0.1, min=0, max=1),
       'softZoneWidth': PFloat(text='\xe8\xbd\xaf\xe5\x8c\xba\xe5\xae\xbd\xe5\xba\xa6', default=0.8, min=0, max=1),
       'softZoneHeight': PFloat(text='\xe8\xbd\xaf\xe5\x8c\xba\xe9\xab\x98\xe5\xba\xa6', default=0.8, min=0, max=1),
       'deadZoneWidth': PFloat(text='\xe6\xad\xbb\xe5\x8c\xba\xe5\xae\xbd\xe5\xba\xa6', default=0.7, min=0, max=1),
       'deadZoneHeight': PFloat(text='\xe6\xad\xbb\xe5\x8c\xba\xe9\xab\x98\xe5\xba\xa6', default=0.7, min=0, max=1),
       'offsetX': PFloat(text='\xe5\x81\x8f\xe7\xa7\xbbX', default=0, min=0, max=1),
       'offsetY': PFloat(text='\xe5\x81\x8f\xe7\xa7\xbbY', default=0, min=0, max=1),
       'autoFocus': PBool(text='\xe8\x87\xaa\xe5\x8a\xa8\xe5\xaf\xb9\xe7\x84\xa6', default=False)
       }

    def _Focus(self, proxy):
        import MontageExtend
        MontageExtend.Controller.controllers['AimController'].focusOnTarget(proxy)

    def _SnapCamera(self, proxy):
        import MontageExtend
        MontageExtend.Controller.controllers['AimController'].snapCamera(proxy)

    def setFrameDataByPath(self, frame, path, data):
        try:
            import Sunshine.Services
            import MontageExtend
            mService = Sunshine.Services.GetService('MontageService')
            resMgr = mService.getResourceManager()
        except ImportError:
            return

        if path[-1] == 'name':
            res = resMgr.getResByKey('CameraPrefab', 'path', data)
            if not res:
                return
            media = mService.getTransaction()
            if frame.properties['target'] and frame.properties['target'] != 'None':
                target = media.getEntityTrackByName(frame.properties['target'])
            else:
                target = None
            result = MontageExtend.Controller.controllers['CameraPrefabController'].applyCameraDataToFrame(res['data'], target, media.getProxy(frame.uuid))
            if result:
                super(TSmartCamera, self).setFrameDataByPath(frame, path, data)
                mService.getController().inspectorCtrl.refresh()
            else:
                mService.getController().inspectorCtrl.refresh()
                return
        super(TSmartCamera, self).setFrameDataByPath(frame, path, data)
        if path[-1] in self._AIM_PARAMS:
            MontageExtend.Controller.controllers['AimController'].RefreshCameraAimUI()
        return

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TSmartCamera, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            tracks = mService.getTransaction().getAllEntityTracks()
            npcList = [ t.name for t in tracks if t.trackType in ('EntityActor', 'Dummy') ]
            npcList.append('None')
            mService.addMontageEnumDefine('CurrentNPCList', npcList)
            if not isinstance(proxy, MontageTrackProxy):
                cameraProxy = proxy.getEntityAncestor()
                if not cameraProxy:
                    return
                editable = True
                if 'Transform' in cameraProxy:
                    editable = False
                dynamicmeta.update({'Transform': {'editable': editable}})
                dynamicmeta['Transform'].update({'Rotation': {'editable': editable},'Translation': {'editable': editable}})
                dynamicmeta.update({'_SnapCamera': {'editable': editable}})
                return
            editMeta = {}
            for key in self.getFrameProperties():
                editMeta.update({key: {'editable': False}})

            dynamicmeta['SmartCamera'].update(editMeta)
            dynamicmeta['SmartCamera']['Transform'] = {'Rotation': {'editable': False},'Translation': {'editable': False}}
        except ImportError:
            return

    def getIntersectedValue(self, track, time):
        hit_frames = []
        for frame in track.frames:
            startime = frame.time
            if startime <= time <= startime + frame.duration:
                hit_frames.append(frame)

        if len(hit_frames) == 0:
            return ''
        else:
            if len(hit_frames) == 1:
                return {'SmartCamera': hit_frames[0].properties}
            return '...'


@TrackMeta
class TFocusDistance(TFloat):
    FRAME_PROPERTIES = {'value': PFloat(),
       'FocusEntity': PEnum(text='\xe5\xaf\xb9\xe7\x84\xa6\xe7\x89\xa9\xe4\xbd\x93', enumType='CurrentNPCList', default='None')
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TFocusDistance, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
            mService = Sunshine.Services.GetService('MontageService')
            tracks = mService.getTransaction().getAllEntityTracks()
            npcList = [ t.name for t in tracks if t.trackType in ('EntityActor', 'Dummy') ]
            npcList.append('None')
            mService.addMontageEnumDefine('CurrentNPCList', npcList)
        except ImportError:
            return

    def setFrameDataByPath(self, frame, path, data):
        super(TFocusDistance, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
            import MontageExtend
            mService = Sunshine.Services.GetService('MontageService')
        except ImportError:
            return

        if path[-1] == 'FocusEntity':
            import math
            media = mService.getTransaction()
            if frame.properties['FocusEntity'] and frame.properties['FocusEntity'] != 'None':
                frameProxy = media.getProxy(frame.uuid)
                entityProxy = media.getEntityTrackByName(frame.properties['FocusEntity'])
                entityTrans = mService.getController().calcWorldTransformMatrix(entityProxy.uuid, frame.time).translate()
                cameraProxy = frameProxy.getEntityAncestor()
                cameraTrans = mService.getController().calcWorldTransformMatrix(cameraProxy.uuid, frame.time).translate()
                distance = math.sqrt(math.pow(round(entityTrans[0] - cameraTrans[0], 3), 2) + math.pow(round(entityTrans[1] - cameraTrans[1], 3), 2) + math.pow(round(entityTrans[2] - cameraTrans[2], 3), 2))
                frameProxy.setProperty('value', round(distance, 3))

    def getFrameSingleValueKey(self):
        return 'value'


@TrackMeta
class TClip(TSpanCue):
    BEGIN_CUEID = CueID.CLIP_START
    END_CUID = CueID.CLIP_END
    FRAME_PROPERTIES = {'name': PStr(text='\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d', visible=False),
       'fileName': PFile(sort=1, text='.mont\xe6\x96\x87\xe4\xbb\xb6', editAttribute='mont'),
       'endBehavior': PEnum(sort=2, text='\xe9\x80\x80\xe5\x87\xba\xe7\x8a\xb6\xe6\x80\x81', default=1, enumType='EndBehavior'),
       'period': PVector2(sort=3, text='\xe5\x89\xa7\xe6\x83\x85\xe8\xb5\xb7\xe6\xad\xa2\xe6\x97\xb6\xe9\x97\xb4', minMaxSlider=True, min=0, max=30, default=(0,
                                                                                                                                             30)),
       'montEndTime': PFloat(default=30.0, visible=False)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TClip, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta['period'] = {'max': proxy.getProperty('montEndTime')}

    def setFrameDataByPath(self, frame, path, data):
        if path[-1] != 'fileName':
            super(TClip, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
            import MontageExtend
            import Paths
            if path[-1] == 'fileName':
                filePath = os.path.join(Paths.CLIENT_RES_PATH, data)
                if not os.path.exists(filePath):
                    return
                super(TClip, self).setFrameDataByPath(frame, path, data)
                mService = Sunshine.Services.GetService('MontageService')
                frameProxy = mService.getTransaction().getProxy(frame.uuid)
                MontageExtend.Controller.controllers['MontsClipController'].setEndTime(frameProxy, data)
                frameProxy.setProperty('name', os.path.basename(data))
        except ImportError:
            return

    @classmethod
    def GetBeginArgs(cls, proxy):
        return json.dumps({'playStat': 'start','uuid': proxy.uuid})

    @classmethod
    def GetEndArgs(cls, proxy):
        return json.dumps({'playStat': 'stop','uuid': proxy.uuid})
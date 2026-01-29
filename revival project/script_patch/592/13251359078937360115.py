# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/RuntimeHelper.py
from __future__ import absolute_import
from six.moves import range
from .. import _Instances
from .MontEventManager import getMontEventMgrInstance as MontEventMgr
from ..Backend.Transaction.TransactionMediator import TransactionMediator
from ..Backend.utils.ShortUUID import uuid
import os

class MontageRuntimeHelper(object):

    def __init__(self):
        self.media = {}
        self.actors = {}
        self.cineData = ''
        self.lastStartTime = 0
        self.lastActor = None
        self.EnvParam = {}
        self.engine = 0
        self.inPreviewMode = False
        return

    def CreateMedia(self, actor=None, groupName=None, isEditor=False):
        if isEditor:
            groupName = 'EditorPreview'
        elif groupName is None:
            groupName = uuid()
        if groupName not in self.media:
            self.media[groupName] = TransactionMediator()
            self.media[groupName].registerRootMeta()
            self.media[groupName].engine = self.engine
            self.actors[groupName] = actor
        return groupName

    def DestroyMedia(self, groupName):
        self.media.pop(groupName, None)
        self.actors.pop(groupName, None)
        return

    def getGroupNameByMedia(self, media, default=None):
        if media in list(self.media.values()):
            return [ k for k, v in self.media.items() if v == media ][0]
        else:
            return default

    def getMediaByGroupName(self, groupName, default=None):
        return self.media.get(groupName, default)

    def getActorByGroupName(self, groupName, default=None):
        return self.actors.get(groupName, default)

    def getActorByMedia(self, media, default=None):
        return self.getActorByGroupName(self.getGroupNameByMedia(media), default)

    def getGroupNamesByActor(self, actor):
        if actor is None or actor not in list(self.actors.values()):
            return False
        else:
            return [ k for k, v in self.actors.items() if v == actor ]

    def getDefaultMedia(self, default=None):
        if len(self.media) == 1:
            return list(self.media.values())[0]
        return default

    def getDefaultGroupName(self, default=None):
        if len(self.media) == 1:
            return list(self.media.keys())[0]
        return default

    def PreviewCinematics(self, cineData, startTime='', isPause=True, editMode=True, actor=None, groupName=None):
        if not _Instances.RuntimeInitiated:
            return
        result = _Instances.Interface.PreviewCinematics(cineData, startTime, isPause, editMode, actor, groupName)
        if result and _Instances.PluginReady:
            _Instances.Montage.Server.UpdatePlayingStatus(isPlaying=isPause)

    def PlayMontAuto(self, fileName, startTime=0, previewCamera=None, isPause=False, isPauseEnd=None, actor=None, isEditor=False, groupName=None):
        groupName = self.CreateMedia(actor, groupName, isEditor)
        if previewCamera is None:
            isLoadSuccess = self._loadMontFileToMedia(fileName, groupName)
            if not isLoadSuccess:
                return
            if previewCamera is None:
                previewCamera = self._getDefaultPreviewCamera(self.getMediaByGroupName(groupName))
        self._playCinematicsByMedia(startTime, previewCamera, isPause, isPauseEnd, '', actor, isEditor, groupName)
        return groupName

    @staticmethod
    def _getDefaultPreviewCamera(media):
        if 'ShotCut' in media.montageRootProxy:
            return 'ShotCut'
        if 'Shot' in media.montageRootProxy:
            return 'Shot'
        for director in media.sceneRootProxy.getChildren():
            if director.trackType == 'Director':
                return director.name

        cameraTracks = media.getPreviewCameraTracksInScene()
        if cameraTracks:
            return cameraTracks[0].name
        return ''

    def PlayMont(self, fileName, startTime, previewCamera='', isPause=True, isPauseEnd=None, lastUuid='', actor=None, isEditor=False, groupName=None):
        groupName = self.CreateMedia(actor, groupName, isEditor)
        isLoadSuccess = self._loadMontFileToMedia(fileName, groupName)
        if not isLoadSuccess:
            return
        self._playCinematicsByMedia(startTime, previewCamera, isPause, isPauseEnd, lastUuid, actor, isEditor, groupName)
        return groupName

    def _loadMontFileToMedia(self, fileName, groupName):
        if not _Instances.RuntimeInitiated:
            _Instances.Interface.PrintFunc('[ERROR]Montage Runtime Initialization failed!')
            return False
        media = self.getMediaByGroupName(groupName)
        if not media.loadMontFile(filename=fileName):
            _Instances.Interface.PrintFunc('The mont file playing cannot match the meta you register! Please check the implementation of "RegisterRootMetaForMedia in MontGameInterface!"')
            return False
        return True

    def _playCinematicsByMedia(self, startTime, previewCamera, isPause, isPauseEnd, lastUuid='', actor=None, isEditor=False, groupName=None):
        if isEditor:
            self.lastStartTime = startTime
            self.lastActor = actor
        media = self.getMediaByGroupName(groupName)
        if isPauseEnd is None:
            media.loop = None
            globalSettings = media.getGlobalSettings()
            isPauseEnd = not globalSettings['playSettings']['loopPlay']
        else:
            media.loop = not isPauseEnd
        self.cineData = _Instances.Interface.TranslateMediaToCinematic(media, previewCamera, isPauseEnd)
        _Instances.TickManager.clearRegistration(media)
        if previewCamera != 'PreviewMode':
            MontEventMgr().TriggerEvent('PRE')
            self.PreviewCinematics(self.cineData, startTime, isPause=isPause, editMode=isEditor, actor=actor, groupName=groupName)
        else:
            self.inPreviewMode = True
            _Instances.Interface.previewResourceByUuid(lastUuid)
        return

    def PopGraphData(self, groupName=None):
        _Instances.Interface.PopCinematics(groupName)
        if _Instances.PluginReady:
            _Instances.Montage.Server.UpdatePlayingStatus(isPlaying=False)

    def reloadGraph(self, startTime, isPause=True, editMode=True):
        return False

    def ChangePreviewCamera(self, previewCamera):
        globalSettings = self.media['EditorPreview'].getGlobalSettings()
        isPauseEnd = not globalSettings['playSettings']['loopPlay']
        self.cineData = _Instances.Interface.TranslateMediaToCinematic(self.media['EditorPreview'], previewCamera, isPauseEnd)
        _Instances.TickManager.clearRegistration(self.media['EditorPreview'])
        MontEventMgr().PreCinematicPlay()
        status = _Instances.Interface.GetScenePlayingStatus()
        self.PreviewCinematics(self.cineData, status['scenetime'], status['isPaused'], editMode=True, actor=None, groupName='EditorPreview')
        return

    def parameterizeMedia(self, media, EnvParam):
        import copy
        if not EnvParam:
            return
        else:
            worldId, worldEntity = _Instances.Interface.specialObjects['World']['key'], _Instances.Interface.specialObjects['World']['entity']
            originParam = worldEntity.Serialize()
            for name, value in EnvParam.items():
                if name not in originParam:
                    continue
                self.EnvParam[name] = copy.deepcopy(originParam[name])
                dynamicTracks = media.animatingEnvParam(name, value, isReplace=True)
                if isinstance(value, (float, bool)):
                    dynamicTracks[0].createFrame(value, 0.1, None, 0, systemname='_Bypass')
                elif isinstance(value, list):
                    for i in range(len(value)):
                        dynamicTracks[i].createFrame(value[i], 0.1, None, 0, systemname='_Bypass')

            return media

    def ResetEnvParameter(self, EnvParam):
        paramName, paramValue = EnvParam
        if self.EnvParam.get(paramName, None) == paramValue:
            _Instances.TickManager.unregisterVirtualTick(self.EnvParam[0], self.EnvParam[1])
        return

    def initializeScriptDialog(self, montFile, EnvParam):
        dirPath = _Instances.ResManager.packageRoot()
        montPath = os.path.join(dirPath, montFile)
        defaultMedia = self.getDefaultMedia()
        defaultMedia.loadMontFile(montPath)
        self.cineData = _Instances.Interface.TranslateMediaToCinematic(defaultMedia, 'Shot', True)
        media = self.parameterizeMedia(defaultMedia, EnvParam)
        if media:
            defaultMedia = media
            self.cineData = _Instances.Interface.TranslateMediaToCinematic(defaultMedia, 'Shot', True)
        if defaultMedia.blendIn > 0:
            initTransform = defaultMedia.initTransform
            self.CameraBlendIn(initTransform, blendInTime=defaultMedia.blendIn)
            _Instances.TickManager.registerGalaxyTick('CameraBlend', {'cineData': self.cineData})
        else:
            self.PreviewCinematics(self.cineData, '0.0', isPause=False, editMode=True)
        if _Instances.PluginReady:
            _Instances.Montage.Server.loadFileInMontage(montPath)

    def clearScriptDialog(self, groupName, EnvParam=None):
        self.PopGraphData(groupName)

    def CameraBlendIn(self, initTransform, blendInTime):
        import math
        initTranslation = initTransform['Translation']
        initRotation = initTransform['Rotation']
        initRotation[2] = math.radians(initRotation[2]) - 2 * math.pi
        initRotation[1] = math.radians(initRotation[1])
        initRotation[0] = math.radians(initRotation[0])
        initRotation = (initRotation[1], initRotation[2], initRotation[0])
        _Instances.blendCamera(blendInTime, initTranslation, initRotation)


def setInstance(instance):
    global RuntimeInstance
    RuntimeInstance = instance


def getInstance():
    return RuntimeInstance


RuntimeInstance = MontageRuntimeHelper()
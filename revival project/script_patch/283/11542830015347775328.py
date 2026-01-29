# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Lib/MontGameInterface.py
from __future__ import absolute_import
from __future__ import print_function
import six
from .. import _Instances
from .MontCastManager import MontCastManagerBase
from .MontResourceManager import MontResourceManagerBase
from .MontEventManager import getMontEventMgrInstance as MontEventMgr
from ..Backend.Transaction.TransactionMediator import TransactionMediator, MontageTrackProxy
from ..Backend.utils.ShortUUID import uuid
from ..Backend.utils.Formula import binarySearchRight
_ResPreview = {}

class MontEditComponent(object):
    EDITTYPE_NULL = 'Null'
    EDITTYPE_EXIST = 'OriginEntity'
    EDITTYPE_RECRUITED = 'CineActor'
    EDITTYPE_VIRTUAL = 'VirtualEntity'
    EDITTYPE_INVALID = 'Invalid'

    def __init__(self, entity):
        self.e = entity
        self.editType = self.EDITTYPE_NULL

    def GetEditType(self):
        return self.EDITTYPE_NULL

    def SetEditType(self, newtype):
        self.editType = newtype

    def GetName(self):
        pass

    def GetPosition(self):
        pass

    def GetRotation(self):
        pass

    def GetScale(self):
        pass

    def GetGuid(self):
        pass

    def ConvertToDict(self):
        return {'MontageInfo': {'name': self.GetName(),
                           'guid': self.GetGuid(),
                           'EditType': self.GetEditType(),
                           'Translation': self.GetPosition(),
                           'Rotation': self.GetRotation(),
                           'Scale': self.GetScale(),
                           'Edit': {'editCategory': self.GetEditType()
                                    }
                           }
           }


class MontEntityManagerBase(object):

    def UpdateEditorComponentExtraData(self, ientity, datadict):
        pass


class MontageGroup(object):

    def __init__(self):
        super(MontageGroup, self).__init__()
        self.media = TransactionMediator()
        self._initMedia()
        self.cineData = None
        self.cineOffsetTransform = {}
        return

    def _initMedia(self):
        self.media.registerRootMeta()
        self.media.engine = _Instances.Interface.engine


def ResPreview(restype):

    def wrapper(fcn):
        global _ResPreview
        _ResPreview[restype] = fcn
        return fcn

    return wrapper


class EndBehavior(object):
    AUTO = 0
    POP_AT_END = 1
    LOOP = 2
    PAUSE_AT_END = 3


class AccelerationMode():
    NoAcceleration = 0
    CastCache = 1
    DiffChange = 2


class MontGameInterfaceBase(object):
    CastManagerCls = MontCastManagerBase
    ResManagerCls = MontResourceManagerBase
    MontageGroupCls = MontageGroup

    def __init__(self):
        super(MontGameInterfaceBase, self).__init__()
        self.montageGroups = {}
        self.entities = {}
        self.cameraMode = 0
        self._modelResourceData = None
        self.engine = 0
        self.inPreviewMode = False
        return

    def RuntimeInit(self, montCastManager=None):
        if _Instances.RuntimeInitiated:
            return
        from . import MontTickHandler
        _Instances.RuntimeInitiated = True
        _Instances.Interface = self
        _Instances.TickManager = MontTickHandler.getInstance()
        _Instances.TickManager.init()
        if montCastManager:
            _Instances.Castmanager = montCastManager
            _Instances.Castmanager.init()
            self.CastManagerCls = montCastManager.__class__
        else:
            _Instances.Castmanager = self.CastManagerCls()
        metaRegister = self.RegisterRootMetaForMedia()
        if not metaRegister:
            _Instances.RuntimeInitiated = False

    def MontageEditorInit(self, castManager=None, resManager=None, pathManager=None, cuedata=None, montagePlugin=None, extendPlugin=None):
        if _Instances.Initiated:
            return
        self.RuntimeInit(castManager)
        _Instances.Initiated = True
        if resManager:
            _Instances.ResManager = resManager
        else:
            _Instances.ResManager = self.ResManagerCls()
        if cuedata:
            _Instances.ResManager.cuedata = cuedata
        else:
            _Instances.ResManager.cuedata = _Instances.Interface.GetCueData()
        if montagePlugin:
            _Instances.Montage = montagePlugin
        _Instances.Montage.Server.SceneReady()
        _Instances.ResManager.scanResource()
        if extendPlugin:
            _Instances.ExtendPlugin = extendPlugin
            _Instances.ExtendPlugin.Server.SceneReady()
        if _Instances.ExtendPlugin:
            _Instances.ExtendPlugin.Server.SetEditTimeInited(True)

    def RegisterRootMetaForMedia(self):
        return False

    def GetFileData(self, filename):
        return {}

    def PreviewResource(self, restype, data):
        if restype not in _ResPreview:
            return
        _ResPreview[restype](data)

    def previewResourceByUuid(self, uuid):
        pass

    @classmethod
    def RegisterMontageGroupCls(cls, montGroupCls):
        cls.MontageGroupCls = montGroupCls

    def CreateMedia(self, groupName):
        if groupName is None:
            groupName = uuid()
        if groupName not in self.montageGroups:
            self.montageGroups[groupName] = self.MontageGroupCls()
        return (groupName, self.montageGroups[groupName])

    def DestroyMedia(self, groupName):
        result = self.montageGroups.pop(groupName, None)
        for eventType in MontEventMgr().EVENT_TYPES:
            MontEventMgr().clearRegisterByEventType(eventType, groupName)

        if result:
            result.media.clearData()
        if result:
            return True
        else:
            return False

    def getDefaultGroupName(self):
        if not self.montageGroups:
            return None
        else:
            if 'EditorPreview' in self.montageGroups.keys():
                return 'EditorPreview'
            return list(self.montageGroups.keys())[0]
            return None

    def getDefaultMedia(self):
        group = self.montageGroups.get(self.getDefaultGroupName())
        if group:
            return group.media
        else:
            return None

    def getEdittimeMedia(self):
        if 'EditorPreview' in self.montageGroups:
            return self.montageGroups['EditorPreview'].media
        else:
            return None

    def getMontageGroupByName(self, groupName):
        return self.montageGroups.get(groupName, None)

    def getGroupNameByMedia(self, media, default=None):
        for groupName, montageGroup in self.montageGroups.items():
            if montageGroup.media == media:
                return groupName

        return default

    def getAllMontageGroup(self):
        return self.montageGroups

    def _getEndBehavior(self, groupName, isPauseEnd, endBehavior):
        if isPauseEnd is None or endBehavior is not EndBehavior.AUTO:
            return endBehavior
        else:
            if isPauseEnd:
                if groupName == 'EditorPreview':
                    return EndBehavior.PAUSE_AT_END
                return EndBehavior.POP_AT_END
            return EndBehavior.LOOP
            return

    def _CineOffset(self, groupName):
        pass

    def PlayMont(self, fileName, startTime=0.0, previewCamera='', isPause=True, isPauseEnd=None, groupName=None, endBehavior=EndBehavior.AUTO, endTime=None):
        if not _Instances.RuntimeInitiated:
            self.PrintFunc('[ERROR]Montage is not runtime initiated! Cannot play montage files.')
            return False
        else:
            endBehavior = self._getEndBehavior(groupName, isPauseEnd, endBehavior)
            groupName, group = self.CreateMedia(groupName)
            if not MontEventMgr().isGroupNameRegistered(groupName):
                self.registerPrePostCinematicEvent(groupName)
            groupName = self.LoadMontFileToTransactionMediator(fileName, endBehavior, groupName)
            if groupName is False:
                return False
            if endTime is not None:
                group.media.sceneRootProxy.setProperty('endTime', endTime)
            previewCamera = previewCamera or group.media.getProperty('previewCamera', '')
            if six.PY2 and isinstance(previewCamera, six.text_type):
                previewCamera = previewCamera.encode('utf-8')
            config = {'startTime': startTime,'previewCamera': previewCamera,
               'isPause': isPause
               }
            result = self.PrePlayCinematics(groupName, config=config, force=False)
            if not result:
                self.PrintFunc("[ERROR]Please don't use [PlayMont] for asynchronous Montage File playing!")
                return False
            cinedata = self.montageGroups[groupName].cineData
            result = self.PreviewCinematics(cinedata, startTime, isPause, groupName)
            if result and group.media.getProperty('currentBranch'):
                self.SwitchToBranch(groupName, group.media.getProperty('currentBranch'), force=True)
            if result:
                return groupName
            return False

    def StopMont(self, groupName=None, ignoreLoop=True):
        from .MontEventManager import getMontEventMgrInstance as MontEventMgr
        if groupName is None:
            groupName = self.getDefaultGroupName()
            if groupName is None:
                return False
        if groupName not in self.montageGroups:
            return False
        else:
            MontEventMgr().TriggerEvent('POST', groupName)
            media = self.getMontageGroupByName(groupName).media
            if media.endBehavior == EndBehavior.PAUSE_AT_END:
                self.PauseCinematics(True, groupName)
                return False
            if media.endBehavior == EndBehavior.LOOP and not ignoreLoop:
                return False
            if groupName == 'EditorPreview':
                self.PauseCinematics(True, groupName)
                return False
            if groupName != 'AutoMontTest':
                self.PopGraphData(groupName)
            return True

    def PopGraphData(self, groupName=None):
        if not groupName:
            groupName = self.getDefaultGroupName()
        if groupName is None:
            return False
        else:
            result = self.PopCinematics(groupName)
            if result:
                if _Instances.PluginReady and groupName == 'EditorPreview':
                    _Instances.Montage.Server.UpdatePlayingStatus(isPlaying=False)
            MontEventMgr().TriggerEvent('POST_POP', groupName)
            return result

    def ReloadMont(self, groupName=None):
        pass

    def LoadMontFileToTransactionMediator(self, fileName, endBehavior=EndBehavior.AUTO, groupName=None):
        groupName, group = self.CreateMedia(groupName)
        media = group.media
        media.engine = self.engine
        result = media.loadMontFile(filename=fileName)
        if not result:
            self.PrintFunc('[ERROR]The mont file playing cannot match the meta you register! \t\t\tPlease check the implementation of [RegisterRootMetaForMedia]! Cannot play montage files.')
            return False
        else:
            media.endBehavior = None
            if endBehavior:
                media.endBehavior = endBehavior
            if group.media.getProperty('currentBranch'):
                _, dea = media.branchHelper.getActDeact('_master', '_master')
                media.branchHelper.tempBranchUuids = []
                for uuid in dea:
                    t = media.getProxy(uuid)
                    ret = t.setProperty('disabled', True, systemname='_Bypass')
                    if ret is True:
                        media.branchHelper.tempBranchUuids.append(uuid)

            MontEventMgr().TriggerEvent('PRE_TRANSLATE', groupName)
            return groupName

    def PrePlayCinematics(self, groupName, config, force=True):
        if MontEventMgr().isMontageGroupAsync(groupName) and not force:
            return False
        media = self.montageGroups[groupName].media
        cinedata = self.TranslateMediaToCinematic(media, previewCamera=config['previewCamera'], isPauseEnd=media.endBehavior)
        if media.getProperty('currentBranch'):
            for uuid in media.branchHelper.tempBranchUuids:
                t = media.getProxy(uuid)
                t.setProperty('disabled', False, systemname='_Bypass')

            media.branchHelper.tempBranchUuids = []
        self.montageGroups[groupName].cineData = cinedata
        MontEventMgr().TriggerEvent('PRE', groupName, config)
        isAsync = MontEventMgr().TriggerEventAsync('PRE_ASYNC', groupName, MontEventMgr().AsyncCallbackReceived, config)
        return not isAsync

    def AsyncTasksFinishedCallback(self, groupName, config):
        self.PrintFunc('All PRE_ASYNC events registered is finished, montage file ready to play.')
        group = self.montageGroups[groupName]
        result = self.PreviewCinematics(group.cineData, config.get('startTime', 0.0), config.get('isPause', True), groupName)
        if not result:
            self.PrintFunc('[ERROR]Failed to preview mont for groupName: [%s]!' % groupName)
            return
        if group.media.getProperty('currentBranch'):
            self.SwitchToBranch(groupName, group.media.getProperty('currentBranch'), force=True)

    def TranslateMediaToCinematic(self, media, previewCamera='', isPauseEnd=EndBehavior.AUTO):
        return None

    def PreviewCinematics(self, data, time, isPaused, groupName=None):
        return False

    def PauseCinematics(self, status, groupName=None):
        MontEventMgr().TriggerEvent('PAUSE_RESUME', groupName, status)

    def PopCinematics(self, groupName):
        return False

    def ResetCineStatus(self):
        MontEventMgr().TriggerEvent('POST', 'EditorPreview')

    def setCineEpisodeTime(self, time, isPaused=None, groupName=None):
        pass

    def JumpToNextShot(self, groupName=None):
        if not groupName:
            groupName = self.getDefaultGroupName()
        group = self.getMontageGroupByName(groupName)
        shot = group.media.montageRootProxy['Shot']
        if not isinstance(shot, MontageTrackProxy):
            return
        else:
            frames = shot.getFrames()
            if len(frames) == 0:
                return
            monttime = self.GetMontTime(groupName)
            if monttime is None:
                return
            index = binarySearchRight(frames, monttime, lambda f: f.getTime())
            if index != len(frames):
                self.SetMontTime(frames[index].getTime(), groupName=groupName)
            return

    def GetMontTime(self, groupName=None):
        pass

    def SetMontTime(self, time, isPaused=None, groupName=None):
        pass

    def ModifyPlayRate(self, groupName, playRate):
        pass

    def GetScenePlayingStatus(self, groupName=None):
        return {'scenetime': float(0.0),
           'isPaused': True
           }

    def registerPrePostCinematicEvent(self, groupName=None):
        if not groupName:
            groupName = self.getDefaultGroupName()
        tickMgr = _Instances.TickManager
        MontEventMgr().registerCinematicEvent(tickMgr.clearRegistration, eventType='PRE', groupName=groupName)
        MontEventMgr().registerCinematicEvent(tickMgr.resetTick, eventType='POST', groupName=groupName)
        MontEventMgr().registerCinematicEvent(self._CineOffset, eventType='PRE_TRANSLATE', groupName=groupName)
        if groupName != 'EditorPreview':
            MontEventMgr().registerCinematicEvent(self.DestroyMedia, eventType='POST_POP', groupName=groupName)

    def PlayMontAuto(self, fileName, groupName=None):
        if not _Instances.RuntimeInitiated:
            self.PrintFunc('[ERROR]Montage is not runtime initiated! Cannot play montage files.')
            return False
        groupName, group = self.CreateMedia(groupName)
        if not MontEventMgr().isGroupNameRegistered(groupName):
            self.registerPrePostCinematicEvent(groupName)
        groupName = self.LoadMontFileToTransactionMediator(fileName, EndBehavior.AUTO, groupName)
        if groupName is False:
            return False
        previewCamera = self.getDefaultPreviewCamera(self.getMontageGroupByName(groupName).media)
        config = {'startTime': 0,
           'previewCamera': previewCamera,
           'isPause': False
           }
        result = self.PrePlayCinematics(groupName, config=config, force=False)
        if not result:
            self.PrintFunc("[ERROR]Please don't use [PlayMont] for asynchronous Montage File playing!")
            return False
        cinedata = self.montageGroups[groupName].cineData
        result = self.PreviewCinematics(cinedata, 0, False, groupName)
        if result and group.media.getProperty('currentBranch'):
            self.SwitchToBranch(groupName, group.media.getProperty('currentBranch'), force=True)
        if result:
            return groupName
        return False

    def PlayMontAsync(self, fileName, groupName, startTime=0.0, previewCamera='', isPause=True, isPauseEnd=None, endBehavior=EndBehavior.AUTO):
        if not _Instances.RuntimeInitiated:
            self.PrintFunc('[ERROR]Montage is not runtime initiated! Cannot play montage files.')
            return False
        else:
            endBehavior = self._getEndBehavior(groupName, isPauseEnd, endBehavior)
            self.LoadMontFileToTransactionMediator(fileName, endBehavior, groupName)
            group = self.getMontageGroupByName(groupName)
            if group is None:
                return False
            config = {'startTime': startTime,'previewCamera': previewCamera,
               'isPause': isPause
               }
            result = self.PrePlayCinematics(groupName, config=config, force=True)
            if result:
                self.PrintFunc('[WARNING]No asynchronous pre play event registered for groupName: %s, recommend using [PlayMont].' % groupName)
                self.AsyncTasksFinishedCallback(groupName, config)
            return True

    def PlayMontAsyncAuto(self, fileName):
        if not _Instances.RuntimeInitiated:
            self.PrintFunc('[ERROR]Montage is not runtime initiated! Cannot play montage files.')
            return False
        else:
            groupName = self.LoadMontFileToTransactionMediator(fileName, EndBehavior.AUTO, 'AutoMontTest')
            if groupName is False:
                return False
            previewCamera = self.getDefaultPreviewCamera(self.getMontageGroupByName('AutoMontTest').media)
            group = self.getMontageGroupByName(groupName)
            if group is None:
                return False
            config = {'startTime': 0,'previewCamera': previewCamera,
               'isPause': False
               }
            result = self.PrePlayCinematics(groupName, config=config, force=True)
            if result:
                self.PrintFunc('[WARNING]No asynchronous pre play event registered for groupName: %s, recommend using [PlayMont].' % groupName)
                self.AsyncTasksFinishedCallback(groupName, config)
            return True

    @staticmethod
    def getDefaultPreviewCamera(media):
        if 'ShotCut' in media.montageRootProxy:
            return 'ShotCut'
        if 'Shot' in media.montageRootProxy:
            return 'Shot'
        for director in media.sceneRootProxy.getChildren():
            if director.trackType == 'Director' and director.name == 'Director':
                return director.name

        cameraTracks = media.getPreviewCameraTracksInScene()
        if cameraTracks:
            if six.PY2 and isinstance(cameraTracks[0].name, six.text_type):
                return cameraTracks[0].name.encode('utf-8')
            else:
                return cameraTracks[0].name

        return ''

    def ChangePreviewCamera(self, previewCamera):
        group = self.getMontageGroupByName('EditorPreview')
        if not group:
            return
        gs = group.media.getGlobalSettings()
        if not gs:
            return
        endBehavior = gs['playSettings']['endBehavior']
        group.cineData = _Instances.Interface.TranslateMediaToCinematic(group.media, previewCamera, endBehavior)
        MontEventMgr().TriggerEvent('PRE', 'EditorPreview', {})
        status = self.GetScenePlayingStatus('EditorPreview')
        self.PreviewCinematics(group.cineData, status['scenetime'], status['isPaused'], groupName='EditorPreview')

    def GetCueData(self):
        pass

    def GetCameraTransform(self):
        pass

    def GetEntityBoneTransform(self, entityId, bone):
        pass

    def screenToGame(self, pos, distance=100):
        pass

    def getEntityByKey(self, key):
        return self.entities.get(key)

    def GetAvailableEntities(self):
        pass

    def PauseCineEpisodeTime(self, status, groupName=None):
        MontEventMgr().TriggerEvent('PAUSE_RESUME', groupName, status)

    @staticmethod
    def makeTransformToDict(transform):
        data = {'Translation': {'X': 0,'Y': 0,'Z': 0},'Rotation': {'Roll': 0,'Pitch': 0,'Yaw': 0},'Scale': {'X': 1,'Y': 1,'Z': 1}}
        return data

    def DebugSave(self, filename):
        self.PrintFunc('debug save not implemented!!!')

    def PrintFunc(self, msg, *args, **kwargs):
        print(msg)

    def GetEntityData(self, uuid, type=MontEditComponent.EDITTYPE_RECRUITED):
        pass

    def SetEditEntity(self, selection):
        pass

    def GetEditorPluginClient(self, name):
        pass

    def FocusEntity(self, uuid):
        pass

    def DragEntityResource(self):
        pass

    def CreateIndicatorEntity(self, charkey, screenPos):
        pass

    def onIndicatorEntityPlaced(self, mp, pos, norm):
        pass

    def SetMontTracksEnabled(self, groupName, enabletracks, disabletracks):
        pass

    def SwitchToBranch(self, groupName, branchName, force=False):
        group = self.getMontageGroupByName(groupName)
        if not group:
            return False
        media = group.media
        currentbranch = media.branchHelper.currentBranch
        media.branchHelper.currentBranch = branchName
        if force:
            act, dea = media.branchHelper.getActDeact(branchName, '_master')
        else:
            act, dea = media.branchHelper.getActDeact(branchName, currentbranch)
        if act or dea:
            self.SetMontTracksEnabled(groupName, act, dea)
        if _Instances.ExtendPlugin and groupName == 'EditorPreview':
            _Instances.ExtendPlugin.Server.SwitchToBranch(branchName)

    def OnEditorDataChange(self, info):
        self.PrintFunc('Messiah\xe6\x9a\x82\xe4\xb8\x8d\xe6\x94\xaf\xe6\x8c\x81')


def setGameInterface(interface_instance):
    global InterfaceInstance
    InterfaceInstance = interface_instance


def getGameInterface():
    return InterfaceInstance


InterfaceInstance = MontGameInterfaceBase()
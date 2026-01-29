# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/CustomTrack.py
from __future__ import absolute_import
from __future__ import print_function
from sunshine.SunshineSDK.Meta.EnumMeta import GetEnumMetaByKey
from sunshine.SunshineSDK.Meta.TypeMeta import GetTypeMeta
from . import TrackMetaBase, TrackMeta, TCustomCue, TCustomFloat, EditorTrackColorType
from . import PStr, PBool, PVector2, PColor, PFloat, PRes, PArray, PInt, PVector3, PEnum, PCustom, PDict
from . import translate
from . import DefEnum
import json
from .CueConsts import CueID
from .Generated import GenCustomSceneTracks, GenCustomEntityTracks
DefEnum('ShotChangeType', {0: '\xe7\xa1\xac\xe5\x88\x87',
   1: '\xe9\x95\x9c\xe5\xa4\xb4\xe8\xbf\x87\xe6\xb8\xa1',
   2: '\xe9\x95\x9c\xe5\xa4\xb4\xe5\x8f\xa0\xe5\x8a\xa0'
   })
DefEnum('VarOperatorType', {'=': '=',
   '+=': '+=',
   '-=': '-='
   })
DefEnum('VarComparatorType', {'==': '==',
   '!=': '!=',
   '>': '>',
   '<': '<',
   '>=': '>=',
   '<=': '<='
   })

@TrackMeta
class TCustomRoot(TrackMetaBase):
    pass


@TrackMeta
class TSubtitle(TCustomCue):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Subtitle
    CUEID = CueID.SUBTITLE
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=True),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False),
       'generateAudio': PCustom(editAttribute='GenerateAudio', text='\xe7\x94\x9f\xe6\x88\x90\xe6\x9c\xba\xe5\x99\xa8\xe9\x9f\xb3\xe9\xa2\x91')
       }
    FRAME_PROPERTIES = {'text': PStr(text='\xe5\xad\x97\xe5\xb9\x95\xe5\x86\x85\xe5\xae\xb9', placeHolder='\xe5\x9c\xa8\xe8\xbf\x99\xe9\x87\x8c\xe8\xbe\x93\xe5\x85\xa5\xe5\xad\x97\xe5\xb9\x95\xe5\x86\x85\xe5\xae\xb9'),
       'pos': PVector2(text='\xe5\xad\x97\xe5\xb9\x95\xe4\xbd\x8d\xe7\xbd\xae', default=[500, 100], visible=False),
       'color': PColor(text='\xe5\xad\x97\xe5\xb9\x95\xe9\xa2\x9c\xe8\x89\xb2'),
       'size': PInt(text='\xe5\xad\x97\xe4\xbd\x93\xe5\xa4\xa7\xe5\xb0\x8f', default=32, max=32, min=1),
       'autohide': PBool(text='\xe8\x87\xaa\xe5\x8a\xa8\xe9\x9a\x90\xe8\x97\x8f', default=True),
       'durationTime': PFloat(text='(TODO)\xe6\x98\xbe\xe7\xa4\xba\xe6\x97\xb6\xe9\x95\xbf(\xe7\xa7\x92)', default=1.0, visible=False),
       'generateAudio': PCustom(editAttribute='GenerateAudio', text='\xe7\x94\x9f\xe6\x88\x90\xe6\x9c\xba\xe5\x99\xa8\xe9\x9f\xb3\xe9\xa2\x91')
       }

    @classmethod
    def Serialize(cls, model):
        data = model.properties
        data['duration'] = model.duration
        return json.dumps(data)

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TSubtitle, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta['generateAudio'] = {'uuid': proxy.uuid}


@TrackMeta
class TWemAudio(TCustomCue):
    CUEID = CueID.WEM_AUDIO
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=True),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }
    FRAME_PROPERTIES = {'Res': PRes(text=translate('Montage', 'Wem\xe9\x9f\xb3\xe9\xa2\x91'), resSet='WemAudio', default=''),
       'recordAudio': PCustom(editAttribute='AudioRecorder', text=translate('Montage', '\xe5\xbd\x95\xe5\x88\xb6\xe9\x9f\xb3\xe9\xa2\x91'), default=''),
       'Volume': PFloat(text=translate('Montage', '\xe9\x9f\xb3\xe9\x87\x8f'), default=1.0)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TWemAudio, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta['recordAudio'] = {'parentUuid': proxy.getParent().uuid,'uuid': proxy.uuid}

    def setFrameDataByPath(self, frame, path, data):
        super(TWemAudio, self).setFrameDataByPath(frame, path, data)
        if path == ['recordAudio']:
            frame.properties['Res'] = data

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback


@TrackMeta
class TDialogAudio(TWemAudio):
    ALLOW_SAMENAME = True
    FRAME_PROPERTIES = {'Res': PRes(text=translate('Montage', 'Wem\xe9\x9f\xb3\xe9\xa2\x91'), resSet='WemAudio', default=''),
       'recordAudio': PCustom(editAttribute='AudioRecorder', text=translate('Montage', '\xe5\xbd\x95\xe5\x88\xb6\xe9\x9f\xb3\xe9\xa2\x91'), default=''),
       'Text': PStr(text=translate('Montage', 'AI\xe8\xbe\x85\xe5\x8a\xa9\xe7\x94\x9f\xe6\x88\x90\xe6\x96\x87\xe6\x9c\xac\xef\xbc\x8c \xe9\x9c\x80\xe8\xa6\x81\xe4\xb8\x8e\xe9\x9f\xb3\xe9\xa2\x91\xe4\xbf\x9d\xe6\x8c\x81\xe4\xb8\x80\xe8\x87\xb4'))
       }


@TrackMeta
class TBlackEdge(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.BLACK_EDGE
    FRAME_PROPERTIES = {'start': PBool(text='\xe5\xbc\x80\xe5\x9c\xba', default=True)}


@TrackMeta
class TSubmodelVisible(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.SUBMODEL_VISIBLE
    FRAME_PROPERTIES = {'show': PBool(text='\xe6\x98\xbe\xe7\xa4\xba', default=True),
       'submodel': PRes(text='\xe5\xad\x90\xe6\xa8\xa1\xe5\x9e\x8b', resSet='Submodels', default='')
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TSubmodelVisible, self).UpdateMeta(proxy, dynamicmeta)
        try:
            import Sunshine.Services
        except ImportError:
            return

        resmgr = Sunshine.Services.GetService('MontageService').getResourceManager()
        name = proxy.getEntityAncestor().name
        res = resmgr.getResByKey('Character', 'name', name)
        dynamicmeta['submodel'] = {}
        if res:
            dynamicmeta['submodel']['subDir'] = res['charkey']
        else:
            dynamicmeta['submodel']['subDir'] = 'dummy'


@TrackMeta
class TSelectDiverge(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.SELECT_DIVERGE
    FRAME_PROPERTIES = {'title': PStr(text=translate('Montage', '\xe6\x8f\x90\xe7\xa4\xba\xe6\x96\x87\xe5\xad\x97'), tip=translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe6\x97\xb6\xe6\x8f\x90\xe7\xa4\xba\xe6\x96\x87\xe5\xad\x97'), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80')),
       'timeLimit': PBool(text=translate('Montage', '\xe6\x98\xaf\xe5\x90\xa6\xe9\x99\x90\xe6\x97\xb6'), tip=translate('Montage', '\xe6\x98\xaf\xe5\x90\xa6\xe9\x99\x90\xe6\x97\xb6'), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80')),
       'limitSecond': PFloat(text=translate('Montage', '\xe9\x99\x90\xe6\x97\xb6\xe7\xa7\x92\xe6\x95\xb0'), tip=translate('Montage', '\xe9\x99\x90\xe6\x97\xb6\xe7\xa7\x92\xe6\x95\xb0'), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80'), min=0.0, default=30.0),
       'overtimeBranch': PStr(text=translate('Montage', '\xe8\xb6\x85\xe6\x97\xb6\xe5\x88\x86\xe6\x94\xaf'), tip=translate('Montage', '\xe4\xb8\x8d\xe6\x98\xbe\xe7\xa4\xba\xe5\x9c\xa8\xe9\x80\x89\xe9\xa1\xb9\xe4\xb8\xad\xef\xbc\x8c\xe8\xb6\x85\xe6\x97\xb6\xe5\x90\x8e\xe9\xbb\x98\xe8\xae\xa4\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x99\xe4\xb8\xaa\xe5\x88\x86\xe6\x94\xaf'), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80')),
       'hidden': PBool(text=translate('Montage', '\xe9\x9a\x90\xe8\x97\x8f\xe8\xb6\x85\xe6\x97\xb6\xe5\x88\x86\xe6\x94\xaf'), tip=translate('Montage', '\xe9\x9a\x90\xe8\x97\x8f\xe8\xb6\x85\xe6\x97\xb6\xe5\x88\x86\xe6\x94\xaf'), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80'), default=True),
       'branches': PArray(text='\xe5\x88\x86\xe6\xad\xa7', childAttribute=PDict(children={'title': PStr(text='\xe9\x80\x89\xe9\xa1\xb9', sort=0),
                    'branch': PStr(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x88\x86\xe6\x94\xaf', default='_master', sort=1)
                    }), category=translate('Montage', '\xe5\x9f\xba\xe7\xa1\x80'))
       }

    @classmethod
    def Serialize(self, model):
        data = model.properties
        data['time'] = model.time
        data['uuid'] = model.uuid
        return json.dumps(data)


DefEnum('VarType', {'Int': 'Int',
   'Float': 'Float',
   'Str': 'Str'
   })

@TrackMeta
class TConditionDiverge(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.CONDITION_DIVERGE
    FRAME_PROPERTIES = {'branches': PArray(text='\xe5\x88\x86\xe6\xad\xa7', childAttribute=PDict(children={'conditions': PArray(text='\xe6\x9d\xa1\xe4\xbb\xb6', childAttribute=PDict(children={'variable': PStr(text='\xe5\x8f\x98\xe9\x87\x8f', sort=0),
                                   'comparator': PEnum(text='\xe6\xaf\x94\xe8\xbe\x83\xe7\xac\xa6', enumType='VarComparatorType', sort=1),
                                   'type': PEnum(text='\xe7\xb1\xbb\xe5\x9e\x8b', enumType='VarType', sort=2),
                                   'ref': PStr(text='\xe5\x8f\x82\xe8\x80\x83\xe5\x80\xbc', sort=3)
                                   }), sort=0),
                    'branch': PStr(text='\xe7\x9b\xae\xe6\xa0\x87\xe5\x88\x86\xe6\x94\xaf', default='_master', sort=1)
                    }))
       }

    @classmethod
    def Serialize(cls, model):
        data = model.properties
        data['time'] = model.time
        data['uuid'] = model.uuid
        return json.dumps(data)


@TrackMeta
class TSetVar(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.SETVAR
    FRAME_PROPERTIES = {'name': PStr(text='\xe5\x8f\x98\xe9\x87\x8f\xe5\x90\x8d'),
       'operator': PEnum(text='\xe8\xbf\x90\xe7\xae\x97\xe7\xac\xa6', enumType='VarOperatorType'),
       'type': PEnum(text='\xe7\xb1\xbb\xe5\x9e\x8b', enumType='VarType')
       }
    for tp in GetEnumMetaByKey('VarType').valueDict.keys():
        typeName = 'value%s' % tp
        FRAME_PROPERTIES[typeName] = GetTypeMeta(tp)(text='\xe5\x80\xbc', visibleCondition='obj["type"] == "%s"' % tp)


@TrackMeta
class TLeap(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.LEAP_FORWARD

    @classmethod
    def Serialize(cls, model):
        data = model.properties
        data['jumpto'] = model.time + model.duration
        return json.dumps(data)


@TrackMeta
class TUserInput(TCustomCue):
    ALLOW_SAMENAME = True
    CUEID = CueID.USER_INPUT
    FRAME_PROPERTIES = {'branches': PArray(text='\xe5\x88\x86\xe6\x94\xaf\xe5\x89\xa7\xe6\x83\x85\xe5\xad\x97\xe5\xb9\x95', childAttribute=PStr()),
       'pause': PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe6\x9a\x82\xe5\x81\x9c\xe6\x97\xb6\xe9\x97\xb4', default=True),
       'endDialog': PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe7\xbb\x93\xe6\x9d\x9f', default=False)
       }

    def getIntersectedValue(self, track, time):
        return None


DefEnum('fadeType', {0: '\xe9\xbb\x91\xe5\xb9\x95\xe6\xb8\x90\xe5\x85\xa5',
   1: '\xe9\xbb\x91\xe5\xb9\x95\xe6\xb8\x90\xe5\x87\xba'
   })

@TrackMeta
class TFade(TCustomFloat):
    ALLOW_SAMENAME = True
    DataType = 'Fade'
    FRAME_PROPERTIES = {'value': PFloat(default=0, min=0, max=255)}


@TrackMeta
class TSun(TCustomRoot):
    _VALID_CHILDREN = [
     (
      'Time', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'Longitude', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'SunAmbientIntensity', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'SunColorIntensity', 'TFloat', {'allowDuplicate': False,'defaultvisible': True})]


@TrackMeta
class TTechParam2(TCustomRoot):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Transform
    _VALID_CHILDREN = [
     (
      'x', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'y', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'z', 'TFloat', {'allowDuplicate': False,'defaultvisible': True}),
     (
      'w', 'TFloat', {'allowDuplicate': False,'defaultvisible': True})]


@TrackMeta
class TSpanCue(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Cue
    BEGIN_CUEID = None
    END_CUID = None
    FRAME_PROPERTIES = {'BeginCueArgs': PStr(default='', category='beginCue', visible=False, editable=False),
       'EndCueArgs': PStr(default='', category='endCue', visible=False, editable=False)
       }

    @classmethod
    def GetBeginArgs(cls, proxy):
        return cls.Serialize(proxy, 'beginCue')

    @classmethod
    def GetEndArgs(cls, proxy):
        return cls.Serialize(proxy, 'endCue')

    @classmethod
    def Serialize(cls, proxy, category):
        p = proxy.properties
        datastr = ''
        for key, item in cls.FRAME_PROPERTIES.items():
            if key == 'BeginCueArgs' or key == 'EndCueArgs' or item.editorMeta.attrs['category'] != category:
                continue
            if isinstance(item, PBool):
                datastr += '1' if p[key] else '0'
            elif isinstance(item, PFloat):
                datastr += str(p[key])
            elif isinstance(item, PInt):
                datastr += str(p[key])
            elif isinstance(item, PStr):
                datastr += p[key]
            elif isinstance(item, PVector2):
                datastr += '%d:%d' % (p[key][0], p[key][1])
            elif isinstance(item, PVector3):
                datastr += '%d:%d:%d' % (p[key][0], p[key][1], p[key][2])
            elif isinstance(item, PEnum):
                datastr += str(p[key])
            else:
                continue
            datastr += ':'

        groupName = proxy.getProperty('groupName')
        if groupName:
            datastr += groupName
        if len(datastr) == 0:
            return '1'
        return datastr[:-1]


@TrackMeta
class TAttachModel(TSpanCue):
    BEGIN_CUEID = CueID.ATTACH_MODEL
    END_CUID = CueID.DETACH_MODEL
    FRAME_PROPERTIES = {'name': PStr(editable=False),
       'BeginCueArgs': PStr(default='', category='beginCue', visible=False, editable=False),
       'EndCueArgs': PStr(default='', category='endCue', visible=False, editable=False),
       'ChildName': PEnum(text='\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1Entity', category='beginCue', enumType='ChildAttachModel', default=''),
       'HardPointName': PEnum(text='\xe7\x88\xb6\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', category='beginCue', enumType='HardPoint', default='Scene Root'),
       'BasePointName': PEnum(text='\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x8c\x82\xe6\x8e\xa5\xe9\xaa\xa8\xe9\xaa\xbc\xe7\x82\xb9', category='beginCue', enumType='BasePoint', default='Scene Root'),
       'UseCurTrans': PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe4\xbd\xbf\xe7\x94\xa8\xe5\xad\x90\xe5\xaf\xb9\xe8\xb1\xa1\xe5\xbd\x93\xe5\x89\x8d\xe6\x97\xb6\xe9\x97\xb4\xe7\x9a\x84\xe4\xbd\x8d\xe7\xa7\xbb\xe6\x95\xb0\xe6\x8d\xae', category='beginCue', default=False),
       'PosOffset': PVector3(text='\xe5\x9d\x90\xe6\xa0\x87\xe5\x81\x8f\xe7\xa7\xbb', category='beginCue', precision=3, default=[0.0, 0.0, 0.0]),
       'RotationOffset': PVector3(text='\xe6\x97\x8b\xe8\xbd\xac\xe5\x81\x8f\xe7\xa7\xbb', category='beginCue', precision=3, default=[0.0, 0.0, 0.0]),
       'ScaleOffset': PVector3(text='\xe7\xbc\xa9\xe6\x94\xbe\xe5\x81\x8f\xe7\xa7\xbb', category='beginCue', precision=3, default=[1.0, 1.0, 1.0], min=0.01)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        self.addEditorMeta(self.attrs)
        try:
            import Sunshine.Services
            from Montage.Backend.Transaction.MontageProxy import MontageFrameProxy
        except ImportError:
            print("Don't call UpdateMeta at your game, use it only at Montage Editor.")
            return

        media = Sunshine.Services.GetService('MontageService').getTransaction()
        if isinstance(proxy, MontageFrameProxy):
            entityancestor = proxy.getEntityAncestor()
            self._updateEnum(entityancestor, 'HardPoint')
            attachmentName = proxy.getProperty('ChildName', '')
            attachProxy = media.getEntityProxyByName(attachmentName)
            self._updateEnum(attachProxy, 'BasePoint')
            self._updateEnum(entityancestor, 'ChildAttachModel')

    def setFrameDataByPath(self, frame, path, data):
        super(TAttachModel, self).setFrameDataByPath(frame, path, data)
        if path[0] == 'ChildName':
            frame.properties['name'] = data

    def _updateEnum(self, proxy, enumName):
        try:
            from ..Utils.EffectUtil import UpdateEntityBonesEnums
            from ..Utils.MetaUtil import UpdateChildAttachModelEnums
            import Sunshine.Services
        except ImportError:
            print('To use AttachModel track, make sure you update MontageImp and MontageExtend plugin!')
            return

        if enumName in ('HardPoint', 'BasePoint'):
            if proxy is not None:
                UpdateEntityBonesEnums(proxy.uuid, enumName)
            else:
                montage = Sunshine.Services.GetService('MontageService')
                montage.addMontageEnumDefine(enumName, ['', 'Scene Root'])
        else:
            UpdateChildAttachModelEnums(proxy.uuid, 'ChildAttachModel')
        return

    @classmethod
    def GetBeginArgs(cls, proxy):
        entityancestor = proxy.getParent().getEntityAncestor()
        parentName = entityancestor.getProperty('name')
        childName = proxy.getProperty('ChildName')
        hardPoint = proxy.getProperty('HardPointName')
        basePoint = proxy.getProperty('BasePointName')
        useCurTrans = proxy.getProperty('UseCurTrans')
        posOffset = proxy.getProperty('PosOffset')
        rotationOffset = proxy.getProperty('RotationOffset')
        r = 3.141592653589793 / 180
        rotationOffset = (rotationOffset[0] * r, rotationOffset[1] * r, rotationOffset[2] * r)
        scaleOffset = proxy.getProperty('ScaleOffset')
        argsStr = parentName + ':' + childName + ':' + hardPoint + ':' + basePoint + ':' + str(useCurTrans) + ':' + str(posOffset[0]) + ':' + str(posOffset[1]) + ':' + str(posOffset[2]) + ':' + str(rotationOffset[0]) + ':' + str(rotationOffset[1]) + ':' + str(rotationOffset[2]) + ':' + str(scaleOffset[0]) + ':' + str(scaleOffset[1]) + ':' + str(scaleOffset[2])
        groupName = proxy.getProperty('groupName')
        if groupName:
            argsStr = argsStr + ':' + groupName
        return argsStr

    @classmethod
    def GetEndArgs(cls, proxy):
        childName = proxy.getProperty('ChildName')
        groupName = proxy.getProperty('groupName')
        if groupName:
            return childName + ':' + groupName
        else:
            return childName


@TrackMeta
class TEnvSound(TSpanCue):
    BEGIN_CUEID = CueID.ENVSOUND
    END_CUID = CueID.ENVSOUND
    FRAME_PROPERTIES = {'EnvMusic': PRes(default='\xe9\x80\x89\xe6\x8b\xa9\xe8\x83\x8c\xe6\x99\xaf\xe9\x9f\xb3\xe4\xb9\x90', resSet='Music'),
       'EnvNoise': PRes(default='\xe9\x80\x89\xe6\x8b\xa9\xe7\x8e\xaf\xe5\xa2\x83\xe5\xa3\xb0', resSet='Music'),
       'MusicVolume': PFloat(default=1.0, text='\xe8\x83\x8c\xe6\x99\xaf\xe9\x9f\xb3\xe9\x87\x8f', min=0.01)
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TSpanCue, self).setFrameDataByPath(frame, path, data)
        try:
            import Sunshine.Services
        except ImportError:
            return

        resManager = Sunshine.Services.GetService('MontageService').getResourceManager()
        ps = path[0]
        if ps == 'EnvMusic' or ps == 'EnvNoise':
            if data:
                audio = resManager.getResByKey('Music', 'path', data)
                frame.properties[ps] = audio['filepath'] + ';' + audio['event']
            else:
                frame.properties[ps] = translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe8\x83\x8c\xe6\x99\xaf\xe9\x9f\xb3\xe4\xb9\x90') if ps == 'EnvMusic' else translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe7\x8e\xaf\xe5\xa2\x83\xe5\xa3\xb0')

    @classmethod
    def GetBeginArgs(cls, proxy):
        return '1:' + proxy.getProperty('EnvMusic') + ':' + proxy.getProperty('EnvNoise') + ':' + str(proxy.getProperty('MusicVolume'))

    @classmethod
    def GetEndArgs(cls, proxy):
        return '0:' + proxy.getProperty('EnvMusic') + ':' + proxy.getProperty('EnvNoise') + ':' + str(proxy.getProperty('MusicVolume'))

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback


@TrackMeta
class TEnvVolume(TSpanCue):
    BEGIN_CUEID = CueID.ENVVOLUME
    END_CUID = CueID.ENVVOLUME
    FRAME_PROPERTIES = {'EnvVolume': PRes(text='\xe7\x8e\xaf\xe5\xa2\x83\xe7\x9b\x92', default='None', resSet='EnvVolume'),
       'EnvVolumeuuid': PStr(visible=False)
       }

    @classmethod
    def GetBeginArgs(cls, proxy):
        return '1:' + proxy.getProperty('EnvVolume')

    @classmethod
    def GetEndArgs(cls, proxy):
        return '0:' + proxy.getProperty('EnvVolume')


@TrackMeta
class TFadeNew(TSpanCue):
    BEGIN_CUEID = CueID.FADE_START
    END_CUID = CueID.FADE_FINISH
    FRAME_PROPERTIES = {'fadeType': PEnum(text='\xe8\xbd\xac\xe5\x9c\xba\xe7\xb1\xbb\xe5\x9e\x8b', default=0, enumType='fadeType')
       }

    @classmethod
    def GetBeginArgs(cls, proxy):
        return json.dumps({'time': proxy.getTime(),'duration': proxy.getDuration(),'fade': proxy.getProperty('fadeType')})

    @classmethod
    def GetEndArgs(cls, proxy):
        return 'finish'


@TrackMeta
class TMonTexture(TCustomCue):
    ALLOW_SAMENAME = False
    CUEID = CueID.SET_TEXTURE
    TRACK_PROPERTIES = {'filename': PRes(text='\xe5\x9b\xbe\xe7\x89\x87', default='', resSet='Image'),
       'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=True),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    FRAME_PROPERTIES = {'pos': PVector2(text='\xe4\xbd\x8d\xe7\xbd\xae', tip='\xe5\x9b\xbe\xe7\x89\x87\xe5\xb7\xa6\xe4\xb8\x8b\xe8\xa7\x92\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe5\xb1\x8f\xe5\xb9\x95\xe7\x9a\x84\xe4\xbd\x8d\xe7\xbd\xae,(1,1)\xe6\x8c\x87\xe5\x8f\xb3\xe4\xb8\x8a\xe8\xa7\x92', min=-1, max=1),
       'size': PVector2(text='\xe5\xb0\xba\xe5\xaf\xb8', tip='\xe5\x9b\xbe\xe7\x89\x87\xe7\x9a\x84\xe7\x9b\xb8\xe5\xaf\xb9\xe5\xb0\xba\xe5\xaf\xb8,(1,1)\xe6\x8c\x87100%\xef\xbc\x8c100%\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe5\xb1\x8f\xe5\xb9\x95', default=(1,
                                                                                                                                                                                                                                                                                     1), min=-1, max=1),
       'activate': PBool(text='\xe6\x98\xbe\xe7\xa4\xba', default=True),
       'origin': PBool(text='\xe5\xb0\xba\xe5\xaf\xb8\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe5\x8e\x9f\xe5\x9b\xbe', tip='\xe5\x8b\xbe\xe9\x80\x89\xe4\xbb\xa3\xe8\xa1\xa8\xe5\x9b\xbe\xe7\x89\x87\xe5\xb0\xba\xe5\xaf\xb8\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe5\x8e\x9f\xe5\x9b\xbe\xef\xbc\x8c\xe4\xb8\x8d\xe5\x8b\xbe\xe9\x80\x89\xe4\xbb\xa3\xe8\xa1\xa8\xe5\x9b\xbe\xe7\x89\x87\xe5\xb0\xba\xe5\xaf\xb8\xe7\x9b\xb8\xe5\xaf\xb9\xe4\xba\x8e\xe5\xb1\x8f\xe5\xb9\x95', default=False),
       'float': PBool(text='\xe6\xb5\xae\xe4\xba\x8e\xe9\xbb\x91\xe8\xbe\xb9\xe4\xb8\x8a\xe6\x96\xb9', tip='\xe5\x8b\xbe\xe9\x80\x89\xe4\xbb\xa3\xe8\xa1\xa8\xe5\x9b\xbe\xe7\x89\x87\xe5\xb1\x82\xe6\xac\xa1\xe5\x9c\xa8\xe9\xbb\x91\xe8\xbe\xb9\xe4\xb8\x8a\xe6\x96\xb9\xef\xbc\x8c\xe4\xb8\x8d\xe8\xa2\xab\xe9\xbb\x91\xe8\xbe\xb9\xe9\x81\xae\xe6\x8c\xa1', default=False),
       'filename': PStr(visible=False),
       'parentid': PStr(visible=False)
       }

    def getFullpathByName(self, name):
        import Sunshine.Services
        resmgr = Sunshine.Services.GetService('MontageService').getResourceManager()
        res = resmgr.getResByKey('Image', 'path', name)
        if not res:
            return ''
        return res['data']

    def setFrameFileData(self, frame, filename, uuid):
        frame.properties['filename'] = filename
        frame.properties['parentid'] = uuid

    def initFrameData(self, frame):
        super(TMonTexture, self).initFrameData(frame)
        try:
            import Sunshine.Services
        except ImportError:
            return

        track = frame.parent
        self.setFrameFileData(frame, self.getFullpathByName(track.properties['filename']), track.uuid)

    def setTrackDataByPath(self, track, path, data):
        super(TMonTexture, self).setTrackDataByPath(track, path, data)
        try:
            import Sunshine.Services
        except ImportError:
            return

        fullpath = self.getFullpathByName(track.properties['filename'])
        for frame in track.frames:
            self.setFrameFileData(frame, fullpath, track.uuid)


@TrackMeta
class TWemAudio(TSpanCue):
    BEGIN_CUEID = CueID.WEM_AUDIO
    END_CUID = CueID.WEM_AUDIO
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=True),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    FRAME_PROPERTIES = {'Res': PRes(text='Wem\xe9\x9f\xb3\xe9\xa2\x91', resSet='WemAudio', default=''),
       'recordAudio': PCustom(editAttribute='AudioRecorder', text='\xe5\xbd\x95\xe5\x88\xb6\xe9\x9f\xb3\xe9\xa2\x91', default=''),
       'Volume': PFloat(text='\xe9\x9f\xb3\xe9\x87\x8f', default=1.0)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TWemAudio, self).UpdateMeta(proxy, dynamicmeta)
        dynamicmeta['recordAudio'] = {'parentUuid': proxy.getParent().uuid,'uuid': proxy.uuid}

    def setFrameDataByPath(self, frame, path, data):
        super(TWemAudio, self).setFrameDataByPath(frame, path, data)
        if path == ['recordAudio']:
            frame.properties['Res'] = data

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback

    @classmethod
    def GetBeginArgs(cls, proxy):
        data = {}
        data['isPlay'] = True
        data['uuid'] = proxy.uuid
        data['Res'] = proxy.getProperty('Res', '')
        data['Volume'] = proxy.getProperty('Volume', 1.0)
        return json.dumps(data)

    @classmethod
    def GetEndArgs(cls, proxy):
        data = {}
        data['isPlay'] = False
        data['uuid'] = proxy.uuid
        return json.dumps(data)


@TrackMeta
class TDialogAudio(TWemAudio):
    ALLOW_SAMENAME = True
    FRAME_PROPERTIES = {'Res': PRes(text='Wem\xe9\x9f\xb3\xe9\xa2\x91', resSet='WemAudio', default=''),
       'recordAudio': PCustom(editAttribute='AudioRecorder', text='\xe5\xbd\x95\xe5\x88\xb6\xe9\x9f\xb3\xe9\xa2\x91', default=''),
       'Text': PStr(text='AI\xe8\xbe\x85\xe5\x8a\xa9\xe7\x94\x9f\xe6\x88\x90\xe6\x96\x87\xe6\x9c\xac\xef\xbc\x8c \xe9\x9c\x80\xe8\xa6\x81\xe4\xb8\x8e\xe9\x9f\xb3\xe9\xa2\x91\xe4\xbf\x9d\xe6\x8c\x81\xe4\xb8\x80\xe8\x87\xb4')
       }


@TrackMeta
class TAudioEx(TSpanCue):
    BEGIN_CUEID = CueID.AUDIO_EX
    END_CUID = CueID.AUDIO_EX
    FRAME_PROPERTIES = {'Name': PRes(sort=35, default='\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88\xe4\xba\x8b\xe4\xbb\xb6', resSet='Music'),
       'Res': PStr(default='', visible=False, editable=False),
       'Volume': PFloat(default=1.0, min=0, max=1.0)
       }

    def setFrameDataByPath(self, frame, path, data):
        super(TSpanCue, self).setFrameDataByPath(frame, path, data)
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

    @classmethod
    def GetBeginArgs(cls, proxy):
        data = {}
        data['isPlay'] = True
        data['uuid'] = proxy.uuid
        data['name'] = proxy.getProperty('Res', '')
        data['event'] = proxy.getProperty('Name', '')
        data['volume'] = proxy.getProperty('Volume', 1.0)
        return json.dumps(data)

    @classmethod
    def GetEndArgs(cls, proxy):
        data = {}
        data['isPlay'] = False
        data['uuid'] = proxy.uuid
        return json.dumps(data)


CustomEntityTracks = [
 (
  '\xe5\xad\x90\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x98\xbe\xe7\xa4\xba', 'TSubmodelVisible', {'default': '','allowDuplicate': False}),
 (
  'TechParam2', 'TTechParam2', {'allowDuplicate': False}),
 (
  'AttachModel', 'TAttachModel', {'frametype': 1,'allowDuplicate': True,'visible': True,'default': ''}),
 (
  'DialogAudio', 'TDialogAudio', {'frametype': 1,'allowDuplicate': False,'visible': True,'showText': translate('Montage', '\xe5\xaf\xb9\xe8\xaf\x9d\xe9\x9f\xb3\xe9\xa2\x91\xe8\xbd\xa8\xe9\x81\x93')})]
CustomEntityTracks.extend(GenCustomEntityTracks)
CustomSceneTracks = [
 ('Sun', 'TSun'),
 (
  'Director', 'TDirector', {'frametype': 2,'allowDuplicate': False}),
 (
  translate('Montage', '\xe8\xb7\xb3\xe8\xbf\x87'), 'TLeap', {'frametype': 1}),
 (
  translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe5\x88\x86\xe6\xad\xa7'), 'TSelectDiverge', {}),
 (
  translate('Montage', '\xe6\x9d\xa1\xe4\xbb\xb6\xe5\x88\x86\xe6\xad\xa7'), 'TConditionDiverge', {}),
 (
  translate('Montage', '\xe5\x9b\xbe\xe7\x89\x87'), 'TMonTexture'),
 (
  translate('Montage', '\xe8\xae\xbe\xe7\xbd\xae\xe5\x8f\x98\xe9\x87\x8f'), 'TSetVar', {}),
 (
  translate('Montage', '\xe5\xad\x97\xe5\xb9\x95\xe8\xbd\xa8\xe9\x81\x93'), 'TSubtitle', {'frametype': 1}),
 (
  'WemAudio', 'TWemAudio', {'frametype': 1,'allowDuplicate': True,'showText': translate('Montage', '\xe6\xb5\x81\xe9\x9f\xb3\xe9\xa2\x91\xe8\xbd\xa8\xe9\x81\x93')}),
 (
  'EnvVolume', 'TEnvVolume', {'frametype': 1,'allowDuplicate': True,'showText': translate('Montage', '\xe7\x8e\xaf\xe5\xa2\x83\xe7\x9b\x92')}),
 (
  '\xe9\xbb\x91\xe8\xbe\xb9', 'TBlackEdge', {'allowDuplicate': False,'visible': False,'showText': translate('Montage', '\xe9\xbb\x91\xe8\xbe\xb9')}),
 (
  'Fade', 'TFade', {'allowDuplicate': False,'showText': translate('Montage', '\xe9\xbb\x91\xe5\xb9\x95\xe8\xbd\xac\xe5\x9c\xba')}),
 (
  'FadeNew', 'TFadeNew', {'allowDuplicate': False,'frametype': 1,'showText': translate('Montage', '\xe9\xbb\x91\xe5\xb9\x95\xe8\xbd\xac\xe5\x9c\xba-\xe9\xa2\x84\xe8\xae\xbe')}),
 (
  'PostProcess', 'TPostProcess', {'frametype': 1,'visible': False,'allowDuplicate': False,'default': ''}),
 (
  'PostProcessRoot', 'TPostProcessRoot', {'allowDuplicate': False,'showText': translate('Montage', '\xe5\x90\x8e\xe5\xa4\x84\xe7\x90\x86\xe8\xbd\xa8\xe9\x81\x93')}),
 (
  'EnvSound', 'TEnvSound', {'frametype': 1,'allowDuplicate': False,'showText': translate('Montage', '\xe8\x83\x8c\xe6\x99\xaf\xe9\x9f\xb3\xe4\xb9\x90\xe8\xbd\xa8\xe9\x81\x93')}),
 (
  'AudioEx', 'TAudioEx', {'frametype': 1,'allowDuplicate': True,'showText': translate('Montage', '\xe9\x9f\xb3\xe9\xa2\x91Ex\xe8\xbd\xa8\xe9\x81\x93')})]
CustomSceneTracks.extend(GenCustomSceneTracks)
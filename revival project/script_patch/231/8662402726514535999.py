# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/PostProcessTrack.py
from __future__ import absolute_import
import json
import copy
from . import TrackMeta, TrackMetaBase, TColor3, PStr, PBool, PRes, PButton, GetTrackMetaCls
from . import translate, TSpanCue, TCustomRoot
from . import PColor, PDict, EditorTrackColorType
from .CueConsts import CueID

@TrackMeta
class TPostProcess(TSpanCue):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.PostProcess
    ALLOW_SAMENAME = True
    BEGIN_CUEID = CueID.SET_POST_PROCESS
    END_CUID = CueID.REVERT_POST_PROCESS
    FRAME_PROPERTIES = {'profileRes': PRes(text='\xe5\x90\x8e\xe5\xa4\x84\xe7\x90\x86\xe9\xa2\x84\xe8\xae\xbe', default='EMPTY', resSet='PostProcessProfile'),
       'ApplyProfile': PButton(text='\xe6\x93\x8d\xe4\xbd\x9c', buttonText='\xe5\xba\x94\xe7\x94\xa8\xe9\xa2\x84\xe8\xae\xbe')
       }

    def ApplyProfile(self, proxy):
        if self.__class__.APPLY_CALLBACK:
            self.__class__.APPLY_CALLBACK(proxy)

    @staticmethod
    def getPostProcessKeyData(proxy):
        name = proxy.getProperty('profileRes')
        res = {}
        try:
            from MontageImp import MontResourceManagerImp
            resList = MontResourceManagerImp.getPostProcessResData()
            for r in resList:
                if r['name'] == name:
                    res = r

        except ImportError:
            res = {}

        data = {}
        if res:
            attr = res.get('attributes', {})
            for k, v in attr.items():
                temp = copy.deepcopy(v)
                for key, value in temp.items():
                    param = value['param']
                    if isinstance(param, bool):
                        temp['param'] = proxy.getProperty(key, False)
                    elif isinstance(param, (dict, tuple, list)):
                        param[4] = proxy.getProperty(key, value['param'][4])
                    data[key] = value

        result = json.dumps(data)
        return result

    @classmethod
    def GetBeginArgs(cls, proxy):
        return cls.getPostProcessKeyData(proxy)

    @classmethod
    def GetEndArgs(cls, proxy):
        return cls.getPostProcessKeyData(proxy)

    def initFrameData(self, frame):
        super(TPostProcess, self).initFrameData(frame)
        frame.properties['ApplyProfile'] = None
        return

    @classmethod
    def updateApplyCallback(cls, callback):
        cls.APPLY_CALLBACK = callback

    def UpdateMeta(self, proxy, dynamicmeta):
        pass

    def getIntersectedValue(self, track, time):
        pass


@TrackMeta
class TPostProcessRoot(TrackMetaBase):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    _VALID_CHILDREN = [
     (
      'HDR', 'THDR', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'HDR')}),
     (
      'ColorGrading', 'TColorGrading', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe9\xa2\x9c\xe8\x89\xb2\xe5\x88\x86\xe7\xba\xa7(ColorGrading)')}),
     (
      'Bloom', 'TBloom', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe6\xb3\x9b\xe5\x85\x89(Bloom)')})]


@TrackMeta
class THDR(TCustomRoot):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    _VALID_CHILDREN = [
     (
      'VignettingRate', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe6\x9a\x97\xe8\xa7\x92\xe6\xaf\x94\xe4\xbe\x8b(VignettingRate)')}),
     (
      'EyeAdaptionLevel',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\x9c\xbc\xe7\x9d\x9b\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe6\xb0\xb4\xe5\xb9\xb3(EyeAdaptionLevel)'),'min': 0.0,'max': 1.0}),
     (
      'EyeAdaptionScale', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\x9c\xbc\xe7\x9d\x9b\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe6\xaf\x94\xe4\xbe\x8b(EyeAdaptionScale)')}),
     (
      'ExposureCompensation', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe6\x9b\x9d\xe5\x85\x89\xe8\xa1\xa5\xe5\x81\xbf(ExposureCompensation)')}),
     (
      'SpeedUp', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\x94\xbb\xe9\x9d\xa2\xe5\x8f\x98\xe4\xba\xae\xe6\x97\xb6\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe9\x80\x9f\xe5\xba\xa6(SpeedUp)')}),
     (
      'SpeedDown', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\x94\xbb\xe9\x9d\xa2\xe5\x8f\x98\xe6\x9a\x97\xe6\x97\xb6\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe9\x80\x9f\xe5\xba\xa6(SpeedDown)')}),
     (
      'FixAdaptionLum', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\x9b\xba\xe5\xae\x9a\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe4\xba\xae\xe5\xba\xa6(FixAdaptionLum)')}),
     (
      'DetailEnhancementLevel', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\xbb\x86\xe8\x8a\x82\xe5\xa2\x9e\xe5\xbc\xba\xe7\xa8\x8b\xe5\xba\xa6(DetailEnhancementLevel)')})]

    def UpdateMeta(self, proxy, dynamicmeta):
        super(THDR, self).UpdateMeta(proxy, dynamicmeta)
        for metaName in proxy.meta.VALID_CHILDREN:
            if isinstance(PostProcessConfig[metaName], list):
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['R'].attrs['default'] = PostProcessConfig[metaName][0]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['G'].attrs['default'] = PostProcessConfig[metaName][1]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['B'].attrs['default'] = PostProcessConfig[metaName][2]
            else:
                proxy.meta.VALID_CHILDREN[metaName].attrs['default'] = PostProcessConfig[metaName]


@TrackMeta
class TColorGrading(TCustomRoot):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    _VALID_CHILDREN = [
     (
      'WhiteTemp', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe8\x89\xb2\xe6\xb8\xa9(WhiteTemp)'),'default': 6500}),
     (
      'WhiteTint', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe8\x89\xb2\xe8\xb0\x83(WhiteTint)')}),
     (
      'Saturation', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe9\xa5\xb1\xe5\x92\x8c\xe5\xba\xa6(Saturation)')}),
     (
      'SaturationLuminance',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe9\xa5\xb1\xe5\x92\x8c\xe4\xba\xae\xe5\xba\xa6(SaturationLuminance)'),'default': 1,'min': 0,'max': 2}),
     (
      'Contrast', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\xaf\xb9\xe6\xaf\x94\xe5\xba\xa6(Contrast)')}),
     (
      'ContrastLuminance',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\xaf\xb9\xe6\xaf\x94\xe4\xba\xae\xe5\xba\xa6(ContrastLuminance)'),'default': 1,'min': 0,'max': 2}),
     (
      'CGGamma', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe4\xbc\xbd\xe9\xa9\xac(CGGamma)')}),
     (
      'GammaLuminance',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe4\xbc\xbd\xe9\xa9\xac\xe4\xba\xae\xe5\xba\xa6(GammaLuminance)'),'default': 1,'min': 0,'max': 2}),
     (
      'Gain', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\xa2\x9e\xe7\x9b\x8a(Gain)')}),
     (
      'GainLuminance',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\xa2\x9e\xe7\x9b\x8a\xe4\xba\xae\xe5\xba\xa6(GainLuminance)'),'default': 1,'min': 0,'max': 2}),
     (
      'Offset', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\x81\x8f\xe7\xa7\xbb(Offset)')}),
     (
      'OffsetLuminance',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe5\x81\x8f\xe7\xa7\xbb\xe4\xba\xae\xe5\xba\xa6(OffsetLuminance)'),'default': 1,'min': 0,'max': 2})]

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TColorGrading, self).UpdateMeta(proxy, dynamicmeta)
        for metaName in proxy.meta.VALID_CHILDREN:
            if isinstance(PostProcessConfig[metaName], list):
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['R'].attrs['default'] = PostProcessConfig[metaName][0]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['G'].attrs['default'] = PostProcessConfig[metaName][1]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['B'].attrs['default'] = PostProcessConfig[metaName][2]
            else:
                proxy.meta.VALID_CHILDREN[metaName].attrs['default'] = PostProcessConfig[metaName]

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        montageService = Sunshine.Services.GetService('MontageService')
        children = copy.deepcopy(self.getTrackProperties())
        colorChildren = {}
        for name, child in self.VALID_CHILDREN.items():
            if isinstance(child, TCustomColor):
                colorChildren[name] = PColor()

        children[attrs['name']] = PDict(children=colorChildren)
        montageService.registerTrackMeta('TRACK', self, children)
        self._TRACK_META = PDict(children=children)
        children = copy.deepcopy(self.getFrameProperties())
        children[attrs['name']] = PDict(children=colorChildren)
        montageService.registerTrackMeta('FRAME', self, children)
        self._FRAME_META = PDict(children=children)
        colorMeta = GetTrackMetaCls('TCustomColor')
        if colorMeta:
            colorMeta.updatePreviewCallback('Color', self.__class__.getPreviewCallback('Color'))
        super(TColorGrading, self).addEditorMeta(attrs)


@TrackMeta
class TBloom(TCustomRoot):
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    _VALID_CHILDREN = [
     (
      'BloomLayers',
      'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'Bloom\xe5\xb1\x82\xe7\xba\xa7(BloomLayers)'),'default': 3,'min': 3,'max': 6,'step': 1.0}),
     (
      'BrightThreshold', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'Bloom\xe9\x98\x88\xe5\x80\xbc(BrightThreshold)'),'default': 1}),
     (
      'BrightDelta', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'BrightDelta'),'default': 3}),
     (
      'BloomLevel', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe6\x9b\x9d\xe5\x85\x89\xe7\xad\x89\xe7\xba\xa7(BloomLevel)'),'default': 3}),
     (
      'BloomDelta', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'BloomDelta'),'default': 3}),
     (
      'LDR_BLOOM_TINT', 'TCustomColor', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe6\xa0\xa1\xe6\xad\xa3\xe5\xb8\xb8\xe9\x87\x8f(LDR_BLOOM_TINT)')}),
     (
      'BloomIntensity', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'Bloom\xe5\xbc\xba\xe5\xba\xa6(BloomIntensity)'),'default': 0.5}),
     (
      'BloomHack', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', '\xe7\x94\xbb\xe9\x9d\xa2\xe7\x94\xb1\xe6\x9a\x97\xe5\x8f\x98\xe4\xba\xae\xe6\x97\xb6\xe8\x87\xaa\xe9\x80\x82\xe5\xba\x94\xe7\x9a\x84\xe9\x80\x9f\xe5\xba\xa6(BloomHack)'),'default': 0}),
     (
      'BloomDirtyIntensity', 'TFloat', {'allowDuplicate': False,'defaultvisible': False,'showText': translate('Montage', 'BloomDirtyIntensity'),'default': 0})]

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TBloom, self).UpdateMeta(proxy, dynamicmeta)
        for metaName in proxy.meta.VALID_CHILDREN:
            if isinstance(PostProcessConfig[metaName], list):
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['R'].attrs['default'] = PostProcessConfig[metaName][0]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['G'].attrs['default'] = PostProcessConfig[metaName][1]
                proxy.meta.VALID_CHILDREN[metaName].VALID_CHILDREN['B'].attrs['default'] = PostProcessConfig[metaName][2]
            else:
                proxy.meta.VALID_CHILDREN[metaName].attrs['default'] = PostProcessConfig[metaName]

    def addEditorMeta(self, attrs):
        import Sunshine.Services
        montageService = Sunshine.Services.GetService('MontageService')
        children = copy.deepcopy(self.getTrackProperties())
        colorChildren = {}
        for name, child in self.VALID_CHILDREN.items():
            if isinstance(child, TCustomColor):
                colorChildren[name] = PColor()

        children[attrs['name']] = PDict(children=colorChildren)
        montageService.registerTrackMeta('TRACK', self, children)
        self._TRACK_META = PDict(children=children)
        children = copy.deepcopy(self.getFrameProperties())
        children[attrs['name']] = PDict(children=colorChildren)
        montageService.registerTrackMeta('FRAME', self, children)
        self._FRAME_META = PDict(children=children)
        colorMeta = GetTrackMetaCls('TCustomColor')
        if colorMeta:
            colorMeta.updatePreviewCallback('Color', self.__class__.getPreviewCallback('Color'))
        super(TBloom, self).addEditorMeta(attrs)


@TrackMeta
class TCustomColor(TColor3, TCustomRoot):

    def __init__(self, **kwargs):
        TColor3.__init__(self, **kwargs)
        TCustomRoot.__init__(self, **kwargs)


@TrackMeta
class TCustomFloatEnum(TrackMetaBase):
    pass


PostProcessConfig = {}
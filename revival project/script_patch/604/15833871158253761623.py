# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Transaction/TrackMeta/TrackMetaBase.py
from copy import deepcopy
import json
from sunshine.SunshineSDK.Meta.TypeMeta import PInt, PFloat, PBool, PStr, PRes, PColor, PDict, PEnum
from sunshine.SunshineSDK.Meta.TypeMeta import InitObject, UpdateObject, ModifyEntityProperty
from sunshine.SunshineSDK.Meta.EnumMeta import DefEnum
from ...utils.Formula import intersectedPos
from ... import PrintFunc
try:
    from I18n import translate
except ImportError:
    translate = lambda x, y: y

DefEnum('EndBehavior', {1: translate('Montage', '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x80\x80\xe5\x87\xba(\xe4\xbb\x85\xe8\xbf\x90\xe8\xa1\x8c\xe6\x97\xb6)'),
   2: translate('Montage', '\xe5\xbe\xaa\xe7\x8e\xaf\xe6\x92\xad\xe6\x94\xbe'),
   3: translate('Montage', '\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe6\x9a\x82\xe5\x81\x9c')
   })
DefEnum('CameraBlendMode', {0: translate('Montage', '\xe9\x9d\x99\xe6\x80\x81\xe4\xba\xa4\xe5\x8f\xa0'),
   1: translate('Montage', '\xe5\x8a\xa8\xe6\x80\x81\xe4\xba\xa4\xe5\x8f\xa0')
   })
BaseAttr = {'default': None,
   'text': '',
   'tip': '',
   'sort': 0,
   'visible': True,
   'frametype': 0,
   'defaultvisible': False,
   'allowDuplicate': True,
   'defaultexpanded': True,
   'showText': None
   }
AttrDict = {'Int': {'default': 0,
           'min': None,
           'max': None
           },
   'Float': {'default': 0.0,
             'step': 1.0,
             'precision': 4,
             'min': None,
             'max': None
             },
   'Bool': {'default': False},'Str': {'default': '','multiLine': False,'maxLen': None,'placeHolder': ''},'Resource': {'default': '','resourcetype': ''}}

class EditorTrackColorType(object):
    Default = 0
    Entity = 1
    Transform = 2
    Animation = 3
    Effect = 4
    EntityEx = 5
    PostProcess = 6
    Shot = 7
    Audio = 8
    Subtitle = 9
    Cue = 10


_TrackMetas = {}
RootMeta = None
SceneRootMeta = None
MontageRootMeta = None

def TrackMeta(cls):
    if cls.__name__ not in _TrackMetas:
        _TrackMetas[cls.__name__] = cls
    elif id(cls) != id(_TrackMetas[cls.__name__]):
        _TrackMetas[cls.__name__] = cls
    return cls


def GetTrackMetaCls(name):
    return _TrackMetas.get(name, None)


def registerRootMeta(metaCls=None):
    global RootMeta
    if not metaCls:
        metaCls = TRootBase
    RootMeta = metaCls(**{'trackName': 'TrackRoot'})
    RootMeta.updateName('TrackRoot')


def registerMontageRootMeta(metaCls=None):
    global MontageRootMeta
    if not metaCls:
        metaCls = TMontageRootBase
    MontageRootMeta = metaCls(**{'trackName': 'MontageRoot'})
    MontageRootMeta.updateName('MontageTrackRoot')


def registerSceneRootMeta(metaCls=None):
    global SceneRootMeta
    if not metaCls:
        metaCls = TSceneRootBase
    SceneRootMeta = metaCls(**{'trackName': 'SceneRoot'})
    SceneRootMeta.updateName('SceneTrackRoot')


class TrackMetaBase(object):
    EDIT_TYPE = 'None'
    KEY_OF_VALUE = '__value'
    ALLOW_SAMENAME = False
    RESOURCE_TRACK = False
    PREVIEW_CALLBACK = {}
    _VALID_CHILDREN = []
    IS_ENTITY = False
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Default
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0')),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }
    FRAME_PROPERTIES = {'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)}

    def __init__(self, **kwargs):
        self._FRAME_META = None
        self._TRACK_META = None
        self.attrs = BaseAttr.copy()
        if self.EDIT_TYPE in AttrDict:
            self.attrs.update(AttrDict[self.EDIT_TYPE])
        for k, v in kwargs.items():
            self.attrs[k] = v

        if len(self._VALID_CHILDREN) > 0:
            self.attrs['frametype'] = 9
        self.typename = ''
        self.__VALID_CHILDREN = None
        self.editorProperties = dict()
        self._registerMeta(self.attrs)
        return

    def _evaluateChildren(self):
        self.__VALID_CHILDREN = dict()
        for childdesc in self._VALID_CHILDREN:
            self.addValidChildren(childdesc)

    @property
    def VALID_CHILDREN(self):
        if self.__VALID_CHILDREN is None:
            self._evaluateChildren()
        return self.__VALID_CHILDREN

    @classmethod
    def updateValidChildren(cls, childrenDesc):
        validChildrenKeys = [ t[1] for t in cls._VALID_CHILDREN ]
        indexes = []
        for childDesc in childrenDesc:
            name = childDesc[1]
            try:
                index = validChildrenKeys.index(name)
            except ValueError:
                index = -1

            indexes.append(index)

        oldValidChildren = deepcopy(cls._VALID_CHILDREN)
        for i in range(len(indexes)):
            if indexes[i] != -1:
                cls._VALID_CHILDREN[indexes[i]] = childrenDesc[i]

        for i in range(len(indexes)):
            if indexes[i] == -1:
                cls._VALID_CHILDREN.append(childrenDesc[i])

        cls.__VALID_CHILDREN = None
        parentSet = set((t[1] for t in oldValidChildren))
        for subCls in cls.__subclasses__():
            subSet = set((t[1] for t in subCls._VALID_CHILDREN))
            if parentSet <= subSet:
                subCls.updateValidChildren(cls._VALID_CHILDREN)
            subCls.__VALID_CHILDREN = None

        return

    def addValidChildren(self, childdesc):
        name = childdesc[0]
        clstype = childdesc[1]
        cls = _TrackMetas.get(clstype)
        if cls is None:
            PrintFunc('ERROR! no such class [%s] in %s, please check track definitions!' % (clstype, self.__class__.__name__))
            return
        else:
            params = self.getClsParamsAndAttrs(childdesc)[0]
            if clstype in ('TSceneRoot', 'TMontageRoot', 'TFolder') or cls.IS_ENTITY:
                params['trackName'] = name
            else:
                parentTrackName = self.attrs['text']
                params['trackName'] = parentTrackName + '_' + name
            meta = cls(**params)
            if self.__VALID_CHILDREN is not None:
                self.__VALID_CHILDREN[name] = meta
            meta.updateName(name)
            return meta

    @classmethod
    def getClsParamsAndAttrs(cls, desc):
        name = desc[0]
        clstype = desc[1]
        if len(desc) > 2:
            params = desc[2]
        else:
            params = {}
        attrs = BaseAttr.copy()
        if cls.EDIT_TYPE in AttrDict:
            attrs.update(AttrDict[cls.EDIT_TYPE])
        if params.get('default') is None and isinstance(cls, TVectorBase):
            parentDefault = attrs['default']
            if isinstance(parentDefault, (tuple, list)):
                parentInd = -1
                for index, child in enumerate(cls._VALID_CHILDREN):
                    if child[0] == name:
                        parentInd = index
                        break

                if parentInd > -1:
                    defaultVal = parentDefault[index]
                    params['default'] = defaultVal
        params['trackName'] = name
        if clstype in ('TSceneRoot', 'TMontageRoot', 'TFolder') or cls.IS_ENTITY:
            params['trackName'] = name
        else:
            parentTrackName = attrs['text']
            params['trackName'] = parentTrackName + '_' + name
        attrs.update(params)
        return (
         params, attrs)

    @classmethod
    def getInheritProperties(cls, pname):
        p = getattr(cls, pname)
        if cls is TrackMetaBase:
            return dict(p)
        inheritp = cls.__bases__[0].getInheritProperties(pname)
        inheritp.update(p)
        return inheritp

    @classmethod
    def getFrameProperties(cls):
        return cls.getInheritProperties('FRAME_PROPERTIES')

    @classmethod
    def getTrackProperties(cls):
        return cls.getInheritProperties('TRACK_PROPERTIES')

    @classmethod
    def getFrameClassMetaName(cls, trackName):
        return trackName + '_Frame'

    @classmethod
    def getTrackClassMetaName(cls, trackName):
        return trackName + '_Track'

    @classmethod
    def isValidChild(cls, metaName):
        for child in cls._VALID_CHILDREN:
            if metaName == child[1]:
                return True

        return False

    @classmethod
    def getChildMetaAttrs(cls, trackType):
        for child in cls._VALID_CHILDREN:
            if trackType == child[0]:
                if len(child) > 2:
                    return child[2]
                return {}

        return None

    def _registerMeta(self, attrs):
        from . import updateSunshineTrackMeta, updateSunshineFrameMeta
        children = deepcopy(self.getTrackProperties())
        self._TRACK_META = PDict(children=children)
        updateSunshineTrackMeta(self, children)
        children = deepcopy(self.getFrameProperties())
        if 'value' in children:
            children['value'].editorMeta.attrs.update(attrs)
        self._FRAME_META = PDict(children=children)
        updateSunshineFrameMeta(self, children)

    def addEditorMeta--- This code section failed: ---

 325       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'VALID_CHILDREN'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 326       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 327      13  LOAD_CONST            1  1
          16  LOAD_CONST            2  ('updateSunshineTrackMeta', 'updateSunshineFrameMeta')
          19  IMPORT_NAME           1  ''
          22  IMPORT_FROM           2  'updateSunshineTrackMeta'
          25  STORE_FAST            2  'updateSunshineTrackMeta'
          28  IMPORT_FROM           3  'updateSunshineFrameMeta'
          31  STORE_FAST            3  'updateSunshineFrameMeta'
          34  POP_TOP          

 329      35  BUILD_MAP_0           0 
          38  STORE_FAST            4  'comEditorMeta'

 330      41  SETUP_LOOP          147  'to 191'
          44  LOAD_FAST             0  'self'
          47  LOAD_ATTR             0  'VALID_CHILDREN'
          50  LOAD_ATTR             4  'items'
          53  CALL_FUNCTION_0       0 
          56  GET_ITER         
          57  FOR_ITER            130  'to 190'
          60  UNPACK_SEQUENCE_2     2 
          63  STORE_FAST            5  'name'
          66  STORE_FAST            6  'meta'

 331      69  LOAD_FAST             6  'meta'
          72  LOAD_ATTR             5  'IS_ENTITY'
          75  POP_JUMP_IF_FALSE    84  'to 84'

 332      78  CONTINUE             57  'to 57'
          81  JUMP_FORWARD          0  'to 84'
        84_0  COME_FROM                '81'

 333      84  LOAD_FAST             6  'meta'
          87  LOAD_ATTR             6  'addEditorMeta'
          90  LOAD_FAST             6  'meta'
          93  LOAD_ATTR             7  'attrs'
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          

 334     100  LOAD_GLOBAL           8  'isinstance'
         103  LOAD_FAST             6  'meta'
         106  LOAD_GLOBAL           9  'TSingle'
         109  CALL_FUNCTION_2       2 
         112  POP_JUMP_IF_FALSE   138  'to 138'

 335     115  LOAD_FAST             6  'meta'
         118  LOAD_ATTR            10  '_FRAME_META'
         121  LOAD_ATTR            11  'metaMap'
         124  LOAD_CONST            3  'value'
         127  BINARY_SUBSCR    
         128  LOAD_FAST             4  'comEditorMeta'
         131  LOAD_FAST             5  'name'
         134  STORE_SUBSCR     
         135  JUMP_BACK            57  'to 57'

 336     138  LOAD_FAST             6  'meta'
         141  LOAD_CONST            4  'name'
         144  BINARY_SUBSCR    
         145  LOAD_FAST             6  'meta'
         148  LOAD_ATTR            12  '_TRACK_META'
         151  LOAD_ATTR            11  'metaMap'
         154  COMPARE_OP            6  'in'
         157  POP_JUMP_IF_FALSE    57  'to 57'

 337     160  LOAD_FAST             6  'meta'
         163  LOAD_ATTR            12  '_TRACK_META'
         166  LOAD_ATTR            11  'metaMap'
         169  LOAD_FAST             6  'meta'
         172  LOAD_CONST            4  'name'
         175  BINARY_SUBSCR    
         176  BINARY_SUBSCR    
         177  LOAD_FAST             4  'comEditorMeta'
         180  LOAD_FAST             5  'name'
         183  STORE_SUBSCR     
         184  JUMP_BACK            57  'to 57'
         187  JUMP_BACK            57  'to 57'
         190  POP_BLOCK        
       191_0  COME_FROM                '41'

 338     191  POP_BLOCK        
         192  POP_BLOCK        
         193  POP_BLOCK        
         194  BINARY_SUBSCR    
         195  LOAD_FAST             0  'self'
         198  LOAD_ATTR            12  '_TRACK_META'
         201  LOAD_ATTR            11  'metaMap'
         204  COMPARE_OP            6  'in'
         207  POP_JUMP_IF_FALSE   240  'to 240'

 339     210  LOAD_FAST             4  'comEditorMeta'
         213  LOAD_ATTR            13  'update'
         216  LOAD_FAST             0  'self'
         219  LOAD_ATTR            12  '_TRACK_META'
         222  LOAD_ATTR            11  'metaMap'
         225  LOAD_ATTR             4  'items'
         228  BINARY_SUBSCR    
         229  BINARY_SUBSCR    
         230  LOAD_ATTR            11  'metaMap'
         233  CALL_FUNCTION_1       1 
         236  POP_TOP          
         237  JUMP_FORWARD          0  'to 240'
       240_0  COME_FROM                '237'

 340     240  BUILD_MAP_1           1 
         243  LOAD_GLOBAL          14  'PDict'
         246  LOAD_CONST            5  'children'
         249  LOAD_FAST             4  'comEditorMeta'
         252  CALL_FUNCTION_256   256 
         255  CALL_FUNCTION_4       4 
         258  BINARY_SUBSCR    
         259  STORE_MAP        
         260  STORE_FAST            7  'editorMeta'

 341     263  LOAD_FAST             7  'editorMeta'
         266  LOAD_ATTR            13  'update'
         269  LOAD_FAST             0  'self'
         272  LOAD_ATTR            15  'getTrackProperties'
         275  CALL_FUNCTION_0       0 
         278  CALL_FUNCTION_1       1 
         281  POP_TOP          

 342     282  LOAD_GLOBAL          14  'PDict'
         285  LOAD_CONST            5  'children'
         288  LOAD_FAST             7  'editorMeta'
         291  CALL_FUNCTION_256   256 
         294  LOAD_FAST             0  'self'
         297  STORE_ATTR           12  '_TRACK_META'

 343     300  LOAD_FAST             2  'updateSunshineTrackMeta'
         303  LOAD_FAST             0  'self'
         306  LOAD_FAST             7  'editorMeta'
         309  CALL_FUNCTION_2       2 
         312  POP_TOP          

 345     313  BUILD_MAP_1           1 
         316  LOAD_GLOBAL          14  'PDict'
         319  LOAD_CONST            5  'children'
         322  LOAD_FAST             4  'comEditorMeta'
         325  CALL_FUNCTION_256   256 
         328  CALL_FUNCTION_4       4 
         331  BINARY_SUBSCR    
         332  STORE_MAP        
         333  STORE_FAST            7  'editorMeta'

 346     336  LOAD_FAST             7  'editorMeta'
         339  LOAD_ATTR            13  'update'
         342  LOAD_FAST             0  'self'
         345  LOAD_ATTR            16  'getFrameProperties'
         348  CALL_FUNCTION_0       0 
         351  CALL_FUNCTION_1       1 
         354  POP_TOP          

 347     355  LOAD_GLOBAL          14  'PDict'
         358  LOAD_CONST            5  'children'
         361  LOAD_FAST             7  'editorMeta'
         364  CALL_FUNCTION_256   256 
         367  LOAD_FAST             0  'self'
         370  STORE_ATTR           10  '_FRAME_META'

 348     373  LOAD_FAST             3  'updateSunshineFrameMeta'
         376  LOAD_FAST             0  'self'
         379  LOAD_FAST             7  'editorMeta'
         382  CALL_FUNCTION_2       2 
         385  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 191

    def UpdateMeta(self, proxy, dynamicmeta):
        self.addEditorMeta(self.attrs)

    @classmethod
    def _initData(cls, model, meta):
        obj = meta.DeserializeData(model.properties)
        InitObject(obj, meta, obj)
        model.properties.update(meta.SerializeData(obj))

    @classmethod
    def _setData(cls, model, meta, data):
        obj = meta.DeserializeData(model.properties)
        UpdateObject(obj, meta, data, True)
        model.properties.update(meta.SerializeData(obj))

    @classmethod
    def _setDataByPath(cls, model, path, meta, data):
        obj = meta.DeserializeData(model.properties)
        ModifyEntityProperty(obj, meta, path, data)
        model.properties.update(meta.SerializeData(obj))

    @classmethod
    def getDataByPath(cls, model, path):
        root = model.properties
        for p in path:
            try:
                p = int(p)
            except:
                pass

            root = root[p]

        return root

    @classmethod
    def getIntersectedValue(cls, track, time):
        data = {}
        for validChild in cls._VALID_CHILDREN:
            name, metaName = validChild[0], validChild[1]
            childMeta = GetTrackMetaCls(metaName)
            if isinstance(childMeta, TCustomCue):
                continue
            if childMeta.IS_ENTITY:
                continue
            params, attrs = childMeta.getClsParamsAndAttrs(validChild)
            if not attrs['visible']:
                continue
            childTracks = []
            for child in track.children:
                if child.properties['type'] == name and child.properties['visible']:
                    childTracks.append(child)

            if len(childTracks) > 0:
                for childTrack in childTracks:
                    childVal = childMeta.getIntersectedValue(childTrack, time)
                    if isinstance(childVal, dict):
                        data.update(childMeta.getIntersectedValue(childTrack, time))
                    else:
                        data[childTrack.properties['type']] = childVal

            else:
                data.update(childMeta.getMetaDefaultValue(validChild))

        return {track.properties['type']: data}

    @classmethod
    def getMetaDefaultValue(cls, desc):
        defaultVal = {}
        params, attrs = cls.getClsParamsAndAttrs(desc)
        if len(cls._VALID_CHILDREN) == 0:
            return {desc[0]: attrs['default']}
        for validChild in cls._VALID_CHILDREN:
            name, metaName = validChild[0], validChild[1]
            childMeta = GetTrackMetaCls(metaName)
            defaultVal.update(childMeta.getMetaDefaultValue(validChild))

        return {desc[0]: defaultVal}

    @classmethod
    def initFrameData(cls, frame):
        FRAME_META = PDict(children=cls.getFrameProperties())
        cls._initData(frame, FRAME_META)

    @classmethod
    def setFrameData(cls, frame, data):
        children = deepcopy(cls.getFrameProperties())
        _FRAME_META = PDict(children=children)
        cls._setData(frame, _FRAME_META, data)

    def serializeFrameData(self, frame):
        return self._FRAME_META.SerializeData(frame.properties)

    @classmethod
    def setFrameDataByPath(cls, frame, path, data):
        children = deepcopy(cls.getFrameProperties())
        if 'value' in children:
            from ..MontageProxy import MontageFrameProxy
            parent = MontageFrameProxy(frame).getParent()
            descDict = {a[0]:a for a in parent.getParent().metaCls._VALID_CHILDREN}
            params, attrs = cls.getClsParamsAndAttrs(descDict[parent.trackType])
            children['value'].editorMeta.attrs.update(attrs)
        _FRAME_META = PDict(children=children)
        cls._setDataByPath(frame, path, _FRAME_META, data)

    @classmethod
    def getFrameSingleValueKey(cls):
        frameprops = cls.getFrameProperties()
        if len(frameprops) <= 2 and frameprops.get('tag', None) is not None:
            if 'value' in frameprops:
                return 'value'
            else:
                return False

        else:
            return False
        return

    @classmethod
    def getFrameSingleValue(cls, frame):
        k = cls.getFrameSingleValueKey()
        if k is False:
            return False
        return frame.properties[k]

    @classmethod
    def setFrameSingleValue(cls, frame, newvalue):
        k = cls.getFrameSingleValueKey()
        if k is False:
            return False
        frame.properties[cls.getFrameSingleValueKey()] = newvalue
        return True

    @classmethod
    def initTrackData(cls, track):
        TRACK_META = PDict(children=cls.getTrackProperties())
        cls._initData(track, TRACK_META)
        for frame in track.frames:
            cls.initFrameData(frame)

    @classmethod
    def setTrackData(cls, track, data):
        TRACK_META = PDict(children=cls.getTrackProperties())
        cls._setData(track, TRACK_META, data)

    def setTrackDataByPath(self, track, path, data):
        self._setDataByPath(track, path, self._TRACK_META, data)

    def updateName(self, name):
        if self.attrs['text'] == '':
            self.attrs['text'] = name
        self.attrs['name'] = name

    def __getitem__(self, item):
        return self.attrs.get(item, None)

    def getMetaByPath(self, path):
        pathlist = path.split('/')
        if len(pathlist) == 0:
            return None
        else:
            currentkey = pathlist.pop(0)
            if currentkey in self.VALID_CHILDREN:
                childmeta = self.VALID_CHILDREN[currentkey]
                if len(pathlist) == 0:
                    return childmeta
                else:
                    return childmeta.getMetaByPath('/'.join(pathlist))

            else:
                return None
            return None

    @classmethod
    def updatePreviewCallback(cls, key, callback):
        if cls.__name__ not in cls.PREVIEW_CALLBACK:
            cls.PREVIEW_CALLBACK[cls.__name__] = {}
        cls.PREVIEW_CALLBACK[cls.__name__][key] = callback

    @classmethod
    def getPreviewCallback(cls, key):
        if cls.__name__ not in cls.PREVIEW_CALLBACK:
            return
        else:
            if key is not None:
                cb = cls.PREVIEW_CALLBACK[cls.__name__].get(key, None)
            else:
                cb = list(cls.PREVIEW_CALLBACK[cls.__name__].values())[0]
            if callable(cb):
                return cb
            return


@TrackMeta
class TSingle(TrackMetaBase):
    EDIT_TYPE = 'Single'
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }

    @classmethod
    def initFrameData(cls, frame):
        children = cls.getFrameProperties()
        if 'value' in children:
            from ..MontageProxy import MontageFrameProxy
            parent = MontageFrameProxy(frame).getParent()
            descDict = {a[0]:a for a in parent.getParent().metaCls._VALID_CHILDREN}
            params, attrs = cls.getClsParamsAndAttrs(descDict[parent.trackType])
            if 'default' in attrs:
                children['value'].editorMeta.attrs['default'] = attrs['default']
        FRAME_META = PDict(children=children)
        cls._initData(frame, FRAME_META)

    @classmethod
    def getIntersectedValue(cls, track, time):
        from ..MontageProxy import MontageFrameProxy
        if len(track.frames) == 0:
            return float(cls.getDataByPath(track, ['default']))
        frames = track.frames
        if frames[0].time > time:
            return float(cls.getDataByPath(track, ['default']))
        for ind in range(len(frames)):
            if time <= frames[ind].time:
                return MontageFrameProxy(frames[ind - 1]).getProperty('value')

        return MontageFrameProxy(frames[-1]).getProperty('value')

    @classmethod
    def getMetaDefaultValue(cls, desc):
        params, attrs = cls.getClsParamsAndAttrs(desc)
        return {desc[0]: attrs['default']}

    def addEditorMeta(self, attrs):
        from . import updateSunshineTrackMeta
        children = deepcopy(self.getTrackProperties())
        children['value'] = self._FRAME_META.metaMap['value']
        updateSunshineTrackMeta(self, children)


@TrackMeta
class TBool(TSingle):
    EDIT_TYPE = 'Bool'
    FRAME_PROPERTIES = {'value': PBool()}


@TrackMeta
class TStr(TSingle):
    EDIT_TYPE = 'Str'
    FRAME_PROPERTIES = {'value': PStr()}


@TrackMeta
class TInt(TSingle):
    EDIT_TYPE = 'Int'
    FRAME_PROPERTIES = {'value': PInt()}


@TrackMeta
class TFloat(TSingle):
    EDIT_TYPE = 'Float'
    FRAME_PROPERTIES = {'value': PFloat()}

    @classmethod
    def getIntersectedValue(cls, track, time):
        from ..MontageProxy import MontageFrameProxy
        if len(track.frames) == 0:
            return float(cls.getDataByPath(track, ['default']))
        else:
            pos = intersectedPos(time, [ MontageFrameProxy(f) for f in track.frames ])[0]
            return float(pos[1])


class TVectorBase(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Transform
    EDIT_TYPE = 'Vector'
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }

    @classmethod
    def getIntersectedValue(cls, track, time):
        data = []
        for child in cls._VALID_CHILDREN:
            name, metaName = child[0], child[1]
            childMeta = GetTrackMetaCls(metaName)
            childTrack = None
            for child in track.children:
                if child.properties['type'] == name:
                    childTrack = child

            if childTrack:
                data.append(childMeta.getIntersectedValue(childTrack, time))
            else:
                params, attrs = childMeta.getClsParamsAndAttrs(child)
                data.append(attrs['default'])

        return {track.properties['type']: data}

    @classmethod
    def getMetaDefaultValue(cls, desc):
        defaultVal = []
        for validChild in cls._VALID_CHILDREN:
            name, metaName = validChild[0], validChild[1]
            childMeta = GetTrackMetaCls(metaName)
            defaultVal.append(childMeta.getMetaDefaultValue(validChild)[name])

        return {desc[0]: defaultVal}

    def addEditorMeta--- This code section failed: ---

 663       0  LOAD_CONST            1  1
           3  LOAD_CONST            2  ('PVector2', 'PVector3', 'PVector4', 'updateSunshineTrackMeta', 'updateSunshineFrameMeta')
           6  IMPORT_NAME           0  ''
           9  IMPORT_FROM           1  'PVector2'
          12  STORE_FAST            2  'PVector2'
          15  IMPORT_FROM           2  'PVector3'
          18  STORE_FAST            3  'PVector3'
          21  IMPORT_FROM           3  'PVector4'
          24  STORE_FAST            4  'PVector4'
          27  IMPORT_FROM           4  'updateSunshineTrackMeta'
          30  STORE_FAST            5  'updateSunshineTrackMeta'
          33  IMPORT_FROM           5  'updateSunshineFrameMeta'
          36  STORE_FAST            6  'updateSunshineFrameMeta'
          39  POP_TOP          

 665      40  LOAD_GLOBAL           6  'deepcopy'
          43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             7  '_TRACK_META'
          49  LOAD_ATTR             8  'metaMap'
          52  CALL_FUNCTION_1       1 
          55  STORE_FAST            7  'children'

 666      58  LOAD_GLOBAL           9  'len'
          61  LOAD_FAST             0  'self'
          64  LOAD_ATTR            10  'VALID_CHILDREN'
          67  CALL_FUNCTION_1       1 
          70  LOAD_CONST            3  2
          73  COMPARE_OP            2  '=='
          76  POP_JUMP_IF_FALSE    94  'to 94'

 667      79  LOAD_FAST             2  'PVector2'
          82  LOAD_FAST             1  'attrs'
          85  CALL_FUNCTION_KW_0     0 
          88  STORE_FAST            8  'editorMeta'
          91  JUMP_FORWARD         76  'to 170'

 668      94  LOAD_GLOBAL           9  'len'
          97  LOAD_FAST             0  'self'
         100  LOAD_ATTR            10  'VALID_CHILDREN'
         103  CALL_FUNCTION_1       1 
         106  LOAD_CONST            4  3
         109  COMPARE_OP            2  '=='
         112  POP_JUMP_IF_FALSE   130  'to 130'

 669     115  LOAD_FAST             3  'PVector3'
         118  LOAD_FAST             1  'attrs'
         121  CALL_FUNCTION_KW_0     0 
         124  STORE_FAST            8  'editorMeta'
         127  JUMP_FORWARD         40  'to 170'

 670     130  LOAD_GLOBAL           9  'len'
         133  LOAD_FAST             0  'self'
         136  LOAD_ATTR            10  'VALID_CHILDREN'
         139  CALL_FUNCTION_1       1 
         142  LOAD_CONST            5  4
         145  COMPARE_OP            2  '=='
         148  POP_JUMP_IF_FALSE   166  'to 166'

 671     151  LOAD_FAST             4  'PVector4'
         154  LOAD_FAST             1  'attrs'
         157  CALL_FUNCTION_KW_0     0 
         160  STORE_FAST            8  'editorMeta'
         163  JUMP_FORWARD          4  'to 170'

 673     166  LOAD_CONST            0  ''
         169  RETURN_VALUE     
       170_0  COME_FROM                '163'
       170_1  COME_FROM                '127'
       170_2  COME_FROM                '91'

 674     170  LOAD_FAST             8  'editorMeta'
         173  LOAD_FAST             7  'children'
         176  LOAD_FAST             6  'updateSunshineFrameMeta'
         179  BINARY_SUBSCR    
         180  STORE_SUBSCR     

 675     181  LOAD_GLOBAL          11  'PDict'
         184  LOAD_CONST            7  'children'
         187  LOAD_FAST             7  'children'
         190  CALL_FUNCTION_256   256 
         193  LOAD_FAST             0  'self'
         196  STORE_ATTR            7  '_TRACK_META'

 676     199  LOAD_FAST             5  'updateSunshineTrackMeta'
         202  LOAD_FAST             0  'self'
         205  LOAD_FAST             7  'children'
         208  CALL_FUNCTION_2       2 
         211  POP_TOP          

 677     212  LOAD_GLOBAL           6  'deepcopy'
         215  LOAD_FAST             0  'self'
         218  LOAD_ATTR            12  '_FRAME_META'
         221  LOAD_ATTR             8  'metaMap'
         224  CALL_FUNCTION_1       1 
         227  STORE_FAST            7  'children'

 678     230  LOAD_FAST             8  'editorMeta'
         233  LOAD_FAST             7  'children'
         236  LOAD_FAST             6  'updateSunshineFrameMeta'
         239  BINARY_SUBSCR    
         240  STORE_SUBSCR     

 679     241  LOAD_FAST             6  'updateSunshineFrameMeta'
         244  LOAD_FAST             0  'self'
         247  LOAD_FAST             7  'children'
         250  CALL_FUNCTION_2       2 
         253  POP_TOP          

Parse error at or near `STORE_SUBSCR' instruction at offset 180


@TrackMeta
class TVector2(TVectorBase):
    _VALID_CHILDREN = [
     (
      'X', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Y', 'TFloat', {'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TVector3(TVectorBase):
    _VALID_CHILDREN = [
     (
      'X', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Y', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Z', 'TFloat', {'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TVector4(TVectorBase):
    _VALID_CHILDREN = [
     (
      'X', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Y', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Z', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'W', 'TFloat', {'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TScaleVector3(TVectorBase):
    _VALID_CHILDREN = [
     (
      'X', 'TFloat', {'defaultvisible': True,'default': 1.0,'min': 0.01,'allowDuplicate': False}),
     (
      'Y', 'TFloat', {'defaultvisible': True,'default': 1.0,'min': 0.01,'allowDuplicate': False}),
     (
      'Z', 'TFloat', {'defaultvisible': True,'default': 1.0,'min': 0.01,'allowDuplicate': False})]


@TrackMeta
class TColorBase(TVectorBase):
    _VALID_CHILDREN = [
     (
      'R', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255}),
     (
      'G', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255}),
     (
      'B', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255})]

    def addEditorMeta(self, attrs):
        from . import updateSunshineFrameMeta, updateSunshineTrackMeta
        children = deepcopy(self.getTrackProperties())
        children[attrs['name']] = PColor()
        updateSunshineTrackMeta(self, children)
        children = deepcopy(self.getFrameProperties())
        if 'value' in children:
            children['value'].editorMeta.attrs.update(attrs)
        children[attrs['name']] = PColor()
        updateSunshineFrameMeta(self, children)


@TrackMeta
class TColor3(TColorBase):
    pass


@TrackMeta
class TColor4(TColorBase):
    _VALID_CHILDREN = [
     (
      'R', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255}),
     (
      'G', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255}),
     (
      'B', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255}),
     (
      'A', 'TFloat', {'defaultvisible': True,'allowDuplicate': False,'min': 0,'max': 255})]

    def addEditorMeta(self, attrs):
        from . import updateSunshineFrameMeta, updateSunshineTrackMeta
        children = deepcopy(self.getTrackProperties())
        children[attrs['name']] = PColor(showAlphaChannle=True)
        updateSunshineTrackMeta(self, children)
        children = deepcopy(self.getFrameProperties())
        if 'value' in children:
            children['value'].editorMeta.attrs.update(attrs)
        children[attrs['name']] = PColor(showAlphaChannle=True)
        updateSunshineFrameMeta(self, children)


@TrackMeta
class TResource(TrackMetaBase):
    EDIT_TYPE = 'Resource'
    RESOURCE_TRACK = True
    ALLOW_SAMENAME = True
    FRAME_PROPERTIES = {'name': PStr(default='')}

    @classmethod
    def getIntersectedValue(cls, track, time):
        raise NotImplementedError

    def getResource(self, frame):
        return frame.properties['resKey']


@TrackMeta
class TRotation(TVectorBase):
    _VALID_CHILDREN = [
     (
      'Roll', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Pitch', 'TFloat', {'defaultvisible': True,'allowDuplicate': False}),
     (
      'Yaw', 'TFloat', {'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TCamTransform(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Transform
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }
    _VALID_CHILDREN = [
     (
      'Translation', 'TVector3', {'precision': 4,'step': 0.1,'defaultvisible': True,'allowDuplicate': False}),
     (
      'Rotation', 'TRotation', {'precision': 4,'step': 0.1,'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TTransform(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Transform
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }
    _VALID_CHILDREN = [
     (
      'Translation', 'TVector3', {'precision': 4,'step': 0.1,'defaultvisible': True,'allowDuplicate': False}),
     (
      'Rotation', 'TRotation', {'precision': 4,'step': 0.1,'defaultvisible': True,'allowDuplicate': False}),
     (
      'Scale', 'TScaleVector3', {'precision': 4,'step': 0.1,'defaultvisible': True,'default': (1, 1, 1),'allowDuplicate': False})]


@TrackMeta
class TCustomFloat(TFloat):
    _VALID_CHILDREN = []
    DataType = ''
    FRAME_PROPERTIES = {'value': PFloat()}


@TrackMeta
class TCustomCue(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Cue
    _VALID_CHILDREN = []
    CUEID = None
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False)
       }

    def __init__(self, **kwargs):
        super(TCustomCue, self).__init__(**kwargs)

    @classmethod
    def Serialize(cls, model):
        return json.dumps(model.properties)

    def addEditorMeta(self, attrs):
        pass


@TrackMeta
class TBaseEntityActor(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Entity
    IS_ENTITY = True
    _VALID_CHILDREN = [
     ('EntityActor', 'TEntityActor'),
     ('CameraActor', 'TCameraActor'),
     (
      'Transform', 'TTransform', {'allowDuplicate': False,'defaultvisible': True})]


@TrackMeta
class TCameraActor(TBaseEntityActor):
    ALLOW_SAMENAME = False
    _VALID_CHILDREN = TBaseEntityActor._VALID_CHILDREN[:-1] + [
     (
      'Transform', 'TCamTransform', {'defaultvisible': True,'allowDuplicate': False})]


@TrackMeta
class TEntityActor(TBaseEntityActor):
    pass


@TrackMeta
class TShot(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Shot
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text=translate('Montage', '\xe5\x90\x8d\xe7\xa7\xb0'), editable=False),
       'disabled': PBool(text=translate('Montage', '\xe7\xa6\x81\xe7\x94\xa8'), default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text=translate('Montage', '\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe'), visible=False),
       'blendInTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4'), default=0),
       'blendOutTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4'), default=0)
       }
    FRAME_PROPERTIES = {'name': PRes(sort=20, text=translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe9\x95\x9c\xe5\xa4\xb4'), default='', resSet='CameraActor'),
       'scenestart': PFloat(text=translate('Montage', 'scene\xe4\xb8\xad\xe7\x9a\x84\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, precision=3),
       'sceneduration': PFloat(text=translate('Montage', 'scene\xe4\xb8\xad\xe7\x9a\x84\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x95\xbf'), min=0.0, precision=3),
       'lockDuration': PBool(text=translate('Montage', '\xe9\x94\x81\xe5\xae\x9a\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4'), default=True),
       'lockStartTime': PBool(text=translate('Montage', '\xe9\x94\x81\xe5\xae\x9a\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe5\x88\xbb'), default=True),
       'blendInTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, max=999999),
       'blendOutTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, max=999999),
       'blendMode': PEnum(text=translate('Montage', '\xe8\x9e\x8d\xe5\x90\x88\xe6\x96\xb9\xe5\xbc\x8f'), enumType='CameraBlendMode', default=0)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TShot, self).UpdateMeta(proxy, dynamicmeta)
        import Montage
        from Montage.Data import MontageResourceMgr
        children = Montage.Transaction.getPreviewCameraTracksInScene()
        resData = []
        for cam in children:
            if cam.trackType in ('CameraActor', 'DollyTrack'):
                cameraName = cam.getProperty('name')
                resData.append({'name': cameraName,'path': cameraName,'type': 'Cameras'})

        oldRes = MontageResourceMgr.getInstance().getDataByType('CameraActor')
        if oldRes == resData:
            return
        MontageResourceMgr.getInstance().updateData('CameraActor', resData, isReplacing=True)

    @classmethod
    def setFrameDataByPath(cls, frame, path, data):
        import Montage
        if path[0] == 'name':
            Montage.SceneWindow.hideAllShotArea()
        super(TShot, cls).setFrameDataByPath(frame, path, data)

    def getBlendOutTime(self, proxy):
        return proxy.getProperty('blendOutTime', 0)

    def getBlendInTime(self, proxy):
        return proxy.getProperty('blendInTime', 0)

    def getBlendKey(self, isBlendIn):
        if isBlendIn:
            return 'blendInTime'
        return 'blendOutTime'

    def getMaxBlendTime(self, proxy):
        return 999999


@TrackMeta
class TTimeline(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Shot
    ALLOW_SAMENAME = True
    TRACK_PROPERTIES = {'name': PStr(text='\xe5\x90\x8d\xe7\xa7\xb0', editable=False),
       'disabled': PBool(text='\xe7\xa6\x81\xe7\x94\xa8', default=False),
       'visible': PBool(default=True, visible=False),
       'tag': PStr(text='\xe9\xbb\x98\xe8\xae\xa4\xe6\xa0\x87\xe7\xad\xbe', visible=False)
       }
    FRAME_PROPERTIES = {'name': PRes(sort=20, text='\xe9\x80\x89\xe6\x8b\xa9\xe9\x95\x9c\xe5\xa4\xb4', default='', resSet='CameraActor'),
       'scenestart': PFloat(text='scene\xe4\xb8\xad\xe7\x9a\x84\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', min=0.0, precision=3),
       'sceneduration': PFloat(text='scene\xe4\xb8\xad\xe7\x9a\x84\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x95\xbf', min=0.0, precision=3),
       'lockDuration': PBool(text='\xe9\x94\x81\xe5\xae\x9a\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4', default=True),
       'lockStartTime': PBool(text='\xe9\x94\x81\xe5\xae\x9a\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe5\x88\xbb', default=True),
       'blendInTime': PFloat(text='\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4', default=0),
       'blendOutTime': PFloat(text='\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4', default=0),
       'blendMode': PEnum(text=translate('Montage', '\xe8\x9e\x8d\xe5\x90\x88\xe6\x96\xb9\xe5\xbc\x8f'), enumType='CameraBlendMode', default=0)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TTimeline, self).UpdateMeta(proxy, dynamicmeta)
        import Montage
        from Montage.Data import MontageResourceMgr
        children = Montage.Transaction.getPreviewCameraTracksInScene()
        resData = []
        for cam in children:
            if cam.trackType in ('CameraActor', 'DollyTrack'):
                cameraName = cam.getProperty('name')
                resData.append({'name': cameraName,'path': cameraName,'type': 'Cameras'})

        oldRes = MontageResourceMgr.getInstance().getDataByType('CameraActor')
        if oldRes == resData:
            return
        MontageResourceMgr.getInstance().updateData('CameraActor', resData, isReplacing=True)

    @classmethod
    def setFrameDataByPath(cls, frame, path, data):
        import Montage
        if path[0] == 'name':
            Montage.SceneWindow.hideAllShotArea()
        super(TTimeline, cls).setFrameDataByPath(frame, path, data)

    def getBlendOutTime(self, proxy):
        return proxy.getProperty('blendOutTime', 0)

    def getBlendInTime(self, proxy):
        return proxy.getProperty('blendInTime', 0)

    def getBlendKey(self, isBlendIn):
        if isBlendIn:
            return 'blendInTime'
        return 'blendOutTime'

    def getMaxBlendTime(self, proxy):
        return 999999


@TrackMeta
class TShotCut(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Shot
    FRAME_PROPERTIES = {'name': PRes(sort=20, text=translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9Director'), default='', resSet='Director'),
       'scenestart': PFloat(text=translate('Montage', 'scene\xe4\xb8\xad\xe7\x9a\x84\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, precision=3),
       'sceneduration': PFloat(text=translate('Montage', 'scene\xe4\xb8\xad\xe7\x9a\x84\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x95\xbf'), min=0.0, precision=3),
       'lockDuration': PBool(text=translate('Montage', '\xe9\x94\x81\xe5\xae\x9a\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4'), default=True),
       'lockStartTime': PBool(text=translate('Montage', '\xe9\x94\x81\xe5\xae\x9a\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe5\x88\xbb'), default=True)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TShotCut, self).UpdateMeta(proxy, dynamicmeta)
        import Montage
        from Montage.Data import MontageResourceMgr
        children = Montage.Transaction.sceneRootProxy.getChildren()
        resData = []
        for track in children:
            if track.trackType == 'Director':
                name = track.getProperty('name')
                resData.append({'name': name,'path': name,'type': 'Directors'})

        oldRes = MontageResourceMgr.getInstance().getDataByType('Director')
        if oldRes == resData:
            return
        MontageResourceMgr.getInstance().updateData('Director', resData, isReplacing=True)

    @classmethod
    def setFrameDataByPath(cls, frame, path, data):
        import Montage
        if path[0] == 'name':
            Montage.SceneWindow.hideAllShotArea()
        super(TShotCut, cls).setFrameDataByPath(frame, path, data)


@TrackMeta
class TDirector(TrackMetaBase):
    EDITOR_TRACK_COLOR_TYPE = EditorTrackColorType.Shot
    FRAME_PROPERTIES = {'name': PRes(sort=20, text=translate('Montage', '\xe9\x80\x89\xe6\x8b\xa9\xe9\x95\x9c\xe5\xa4\xb4'), default='', resSet='CameraActor'),
       'blendInTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, max=999999),
       'blendOutTime': PFloat(text=translate('Montage', '\xe9\x95\x9c\xe5\xa4\xb4\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4'), min=0.0, max=999999),
       'blendMode': PEnum(text=translate('Montage', '\xe8\x9e\x8d\xe5\x90\x88\xe6\x96\xb9\xe5\xbc\x8f'), enumType='CameraBlendMode', default=0)
       }

    def UpdateMeta(self, proxy, dynamicmeta):
        super(TDirector, self).UpdateMeta(proxy, dynamicmeta)
        import Montage
        from Montage.Data import MontageResourceMgr
        children = Montage.Transaction.getPreviewCameraTracksInScene()
        resData = []
        for cam in children:
            if cam.trackType in ('CameraActor', 'DollyTrack'):
                cameraName = cam.getProperty('name')
                resData.append({'name': cameraName,'path': cameraName,'type': 'Cameras'})

        oldRes = MontageResourceMgr.getInstance().getDataByType('CameraActor')
        if oldRes == resData:
            return
        MontageResourceMgr.getInstance().updateData('CameraActor', resData, isReplacing=True)

    @classmethod
    def setFrameDataByPath(cls, frame, path, data):
        import Montage
        if path[0] == 'name':
            Montage.SceneWindow.hideAllShotArea()
        super(TDirector, cls).setFrameDataByPath(frame, path, data)

    def setTrackDataByPath(self, track, path, data):
        import Montage
        oldValue = self.getDataByPath(track, path)
        super(TDirector, self).setTrackDataByPath(track, path, data)
        ps = path[0]
        media = Montage.Transaction
        if ps == 'name':
            if Montage.Controller.previewCamera == oldValue:
                Montage.Controller.previewCamera = data
            shotcutTrack = media.montageRootProxy['ShotCut']
            if not shotcutTrack:
                return
            shotcutTrack.meta.UpdateMeta(shotcutTrack, None)
            for frameProxy in shotcutTrack.getFrames():
                if frameProxy.getProperty('name') == oldValue:
                    frameProxy.setProperty('name', data)

        else:
            super(TDirector, self).setTrackDataByPath(track, path, data)
        return

    def getBlendOutTime(self, proxy):
        return proxy.getProperty('blendOutTime', 0)

    def getBlendInTime(self, proxy):
        return proxy.getProperty('blendInTime', 0)

    def getBlendKey(self, isBlendIn):
        if isBlendIn:
            return 'blendInTime'
        return 'blendOutTime'

    def getMaxBlendTime(self, proxy):
        return 999999


@TrackMeta
class TRootBase(TrackMetaBase):
    _VALID_CHILDREN = [
     ('MontageTrackRoot', 'TMontageRoot'),
     ('SceneTrackRoot', 'TSceneRoot')]
    TRACK_PROPERTIES = {'globalSettings': PDict(sort=1, text=translate('Montage', '\xe5\x85\xa8\xe5\xb1\x80\xe8\xae\xbe\xe7\xbd\xae'), children={'playSettings': PDict(sort=0, text=translate('Montage', '\xe6\x92\xad\xe6\x94\xbe\xe8\xae\xbe\xe7\xbd\xae'), children={'playSpeed': PFloat(sort=1, text=translate('Montage', '\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe5\xba\xa6'), slider=True, min=0.1, max=10, step=0.1, default=1.0),
                                           'loopPlay': PBool(sort=2, text=translate('Montage', '\xe5\xbe\xaa\xe7\x8e\xaf\xe6\x92\xad\xe6\x94\xbe'), default=False, visible=False),
                                           'endBehavior': PEnum(sort=2, text=translate('Montage', '\xe9\x80\x80\xe5\x87\xba\xe7\x8a\xb6\xe6\x80\x81'), default=1, enumType='EndBehavior'),
                                           'dragTrigger': PBool(sort=3, text=translate('Montage', '\xe6\x89\x8b\xe5\x8a\xa8\xe6\x8b\x96\xe6\x8b\xbd\xe8\xa7\xa6\xe5\x8f\x91'), default=False),
                                           'cineOffset': PBool(sort=4, text=translate('Montage', '\xe5\x89\xa7\xe6\x83\x85\xe5\x81\x8f\xe7\xa7\xbb'), default=False)
                                           }),
                          'frameDrive': PBool(sort=6, text=translate('Montage', '\xe5\xbc\x80\xe5\x90\xaf\xe5\xb8\xa7\xe9\xa9\xb1\xe5\x8a\xa8(Neox)'), default=False),
                          'montFPS': PFloat(sort=7, text=translate('Montage', '\xe5\x89\xa7\xe6\x83\x85\xe5\xb8\xa7\xe7\x8e\x87'), default=30.0, min=1, visibleCondition="obj['globalSettings']['frameDrive']"),
                          'recruitByFrame': PBool(sort=8, text=translate('Montage', '\xe5\xbc\x80\xe5\x90\xaf\xe5\x88\x86\xe5\xb8\xa7\xe5\x8a\xa0\xe8\xbd\xbd(Neox)'), default=False),
                          'trackPerFrame': PInt(sort=9, text=translate('Montage', '\xe6\xaf\x8f\xe5\xb8\xa7\xe5\x8a\xa0\xe8\xbd\xbd\xe6\x95\xb0\xe9\x87\x8f'), default=10, min=0, visibleCondition="obj['globalSettings']['recruitByFrame']")
                          }),
       'viewSpan': PDict(sort=1, text=translate('Montage', '\xe8\xa7\x86\xe9\x87\x8e\xe5\x8c\xba\xe9\x97\xb4'), children={'startTime': PFloat(sort=1, text=translate('Montage', '\xe8\xb5\xb7\xe5\xa7\x8b\xe4\xbd\x8d\xe7\xbd\xae'), default=0.0, min=0.0),
                    'endTime': PFloat(sort=2, text=translate('Montage', '\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbd\x8d\xe7\xbd\xae'), min=1, max=1000, step=1, default=10)
                    }),
       'branchInfo': PDict(visible=False, children={}, default={}),
       'dialogInfo': PDict(visible=False, children={}, default={}),
       'previewCamera': PStr(visible=False, default='')
       }
    CUSTOM_SETTINGS = {}

    def _registerMeta(self, attrs):
        if self.CUSTOM_SETTINGS:
            self.TRACK_PROPERTIES['globalSettings'].metaMap.update(self.CUSTOM_SETTINGS)
        super(TRootBase, self)._registerMeta(attrs)

    @classmethod
    def initTrackData(cls, track):
        SETTINGS_META = PDict(children={'globalSettings': cls.TRACK_PROPERTIES['globalSettings']})
        newProperties = {}
        InitObject(newProperties, SETTINGS_META, newProperties)

        def _extendSettings(newp, trackp):
            for k, v in newp.items():
                if k not in trackp:
                    trackp[k] = v
                elif isinstance(v, dict):
                    _extendSettings(v, trackp[k])

        playSettings = track.properties.get('globalSettings', {}).get('playSettings', {})
        if playSettings and 'endBehavior' not in playSettings and 'loopPlay' in playSettings:
            if playSettings['loopPlay']:
                playSettings['endBehavior'] = 2 if 1 else 1
                try:
                    import Montage
                    Montage.Controller.filehandler.setModified()
                except ImportError:
                    pass

        if track.properties.get('globalSettings', None):
            _extendSettings(newProperties['globalSettings'], track.properties['globalSettings'])
        else:
            track.properties.update(newProperties)
        cls._initData(track, SETTINGS_META)
        return

    def getDefaultGlobalSettings(self):
        GLOBAL_META = PDict(children=self.TRACK_PROPERTIES['globalSettings'].metaMap)
        globalProperties = {}
        InitObject(globalProperties, GLOBAL_META, globalProperties)
        return globalProperties


@TrackMeta
class TSceneRootBase(TrackMetaBase):
    _VALID_CHILDREN = [
     (
      'Director', 'TDirector', {'frametype': 2}),
     (
      'CameraActor', 'TCameraActor', {'icon': ':/Montage/Camera.svg'}),
     (
      'EntityActor', 'TEntityActor', {'icon': ':/Montage/Entity.svg'}),
     (
      'Folder', 'TFolder', {'showText': translate('Montage', '\xe6\x96\x87\xe4\xbb\xb6\xe5\xa4\xb9')})]
    TRACK_PROPERTIES = {'startTime': PFloat(text=translate('Montage', '\xe8\xb5\xb7\xe5\xa7\x8b\xe4\xbd\x8d\xe7\xbd\xae'), default=0.0),'endTime': PFloat(text=translate('Montage', '\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbd\x8d\xe7\xbd\xae'), default=30.0)}


@TrackMeta
class TMontageRootBase(TrackMetaBase):
    _VALID_CHILDREN = [
     (
      'ShotCut', 'TShotCut', {'frametype': 1,'allowDuplicate': False}),
     (
      'Shot', 'TShot', {'frametype': 2,'allowDuplicate': False}),
     (
      'Playrate', 'TFloat', {'default': 1.0,'min': 0.01,'allowDuplicate': False}),
     (
      'Timeline', 'TTimeline', {'frametype': 2,'allowDuplicate': False})]
    TRACK_PROPERTIES = {'startTime': PFloat(text=translate('Montage', '\xe8\xb5\xb7\xe5\xa7\x8b\xe4\xbd\x8d\xe7\xbd\xae'), default=0.0),'endTime': PFloat(text=translate('Montage', '\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbd\x8d\xe7\xbd\xae'), default=30.0)}


@TrackMeta
class TFolder(TrackMetaBase):
    EDIT_TYPE = 'Folder'
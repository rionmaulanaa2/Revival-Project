# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/EditorMeta.py
__author__ = 'gzhuangwei@corp.netease.com'
import copy
from .MetaUtils import iteritems
from .LayoutAttributes import Group, _LayoutItem

class PropertyDisplayMode(object):
    DataFirst = 0
    MetaFirst = 1
    Combined = 2
    Intersected = 3


class SelectionMode(object):
    SingleClick = 0
    DoubleClick = 1


BaseAttr = {'default': None,
   'text': '',
   'tip': '',
   'sort': 0,
   'ignoreSort': False,
   'editable': True,
   'editType': None,
   'editableInEditorMode': True,
   'editableInPlayMode': True,
   'editableInNonPrefab': True,
   'editableInPrefab': True,
   'editableInPrefabAssets': True,
   'editableInPrefabInstances': True,
   'visible': True,
   'visibleInEditorMode': True,
   'visibleInPlayMode': True,
   'visibleInNonPrefab': True,
   'visibleInPrefab': True,
   'visibleInPrefabAssets': True,
   'visibleInPrefabInstances': True,
   'hideLabel': False,
   'suffixLabel': '',
   'suffixLabelOverlay': False,
   'required': None,
   'copyable': True,
   'pasteable': True,
   'exportFlag': True,
   'exportCondition': '',
   'autoExpand': True,
   'group': '',
   'location': 'Simple',
   'category': '',
   'heading': False,
   'editCondition': '',
   'visibleCondition': '',
   'preDecorators': None,
   'postDecorators': None,
   'textColor': '',
   'textBackgroundColor': '',
   'delayed': False,
   'displayAsString': False,
   'sizePolicy': None,
   'exAttrs': None,
   'validators': [],'nullable': False,
   'hasDefault': False
   }
AttrDict = {'Int': {'default': 0,
           'step': 1,
           'slider': False,
           'min': None,
           'max': None,
           'wrap': False,
           'progressBar': None,
           'preview': False,
           'enterCommit': True
           },
   'Float': {'default': 0.0,
             'step': 1.0,
             'precision': 2,
             'slider': False,
             'min': None,
             'max': None,
             'wrap': False,
             'progressBar': None,
             'enterCommit': True,
             'preview': False
             },
   'Bool': {'default': False},'Str': {'default': '',
           'multiLine': False,
           'maxLen': None,
           'placeHolder': '',
           'enterCommit': True,
           'regexp': ''
           },
   'Button': {'buttonText': '',
              'clickedCallback': '',
              'exportFlag': False,
              'nullable': True
              },
   'Entity': {'entityType': '',
              'style': 'default',
              'withRef': False
              },
   'StorylineEntity': {'multiSelection': False
                       },
   'Vector2': {'default': (0.0, 0.0),
               'min': -999999.0,
               'max': 999999.0,
               'step': 1.0,
               'precision': 2,
               'showVector': True,
               'minMaxSlider': False,
               'enterCommit': True,
               'readonlyList': [],'enablePointSelectionMode': True,
               'preview': False
               },
   'Vector3': {'default': (0.0, 0.0, 0.0),
               'min': -999999.0,
               'max': 999999.0,
               'step': 1.0,
               'precision': 2,
               'enterCommit': True,
               'readonlyList': [],'enablePointSelectionMode': True,
               'preview': False
               },
   'Vector4': {'default': (0.0, 0.0, 0.0, 0.0),
               'min': -999999.0,
               'max': 999999.0,
               'step': 1.0,
               'precision': 2,
               'enterCommit': True,
               'readonlyList': [],'enablePointSelectionMode': True,
               'preview': False
               },
   'Color': {'default': [
                       255, 255, 255],
             'useColorWheel': True,
             'useFloat': False,
             'normalized': False,
             'showAlphaChannel': False
             },
   'Enum': {'enumType': None,
            'radioStyle': False,
            'multiSelection': False,
            'toggleButtonStyle': False,
            'comboBoxStyle': False,
            'level': [],'autoResort': False
            },
   'DynamicEnum': {'style': 1,
                   'radioStyle': False,
                   'multiSelection': False
                   },
   'Expr': {'default': 0,
            'min': 0,
            'max': 9999999,
            'step': 1.0,
            'slider': False,
            'wrap': False
            },
   'Res': {'default': '',
           'resSet': '',
           'subDir': '',
           'editAttribute': 'None',
           'resType': '',
           'slim': False,
           'nullable': True,
           'selectionMode': SelectionMode.SingleClick,
           'useDialog': False
           },
   'File': {'default': '',
            'editAttribute': '',
            'path': '',
            'absolutePath': False,
            'requireExistingPath': True,
            'base': '${CLIENT_RES_PATH}',
            'nullable': True
            },
   'Path': {'default': '',
            'path': '',
            'absolutePath': False,
            'base': '${CLIENT_RES_PATH}'
            },
   'FixArray': {'size': 1,
                'childAttribute': None,
                'default': [],'listElementLabelName': '',
                'numberOfItemsPerPage': 0,
                'showItemCount': True,
                'searchable': False
                },
   'Array': {'childAttribute': None,
             'default': [],'maxSize': 9999,
             'movable': False,
             'addCopiesLastElement': False,
             'addable': True,
             'removable': True,
             'listElementLabelName': '',
             'numberOfItemsPerPage': 0,
             'showItemCount': True,
             'searchable': False
             },
   'ObjectArray': {'addable': True,
                   'default': [],'maxSize': 9999,
                   'movable': False,
                   'selectType': False,
                   'componentMetaType': None,
                   'searchable': False,
                   'addCopiesLastElement': False,
                   'removable': True,
                   'listElementLabelName': '',
                   'numberOfItemsPerPage': 0,
                   'showItemCount': True
                   },
   'Dict': {'addable': False,
            'removable': False,
            'keyTypeHint': 'str',
            'keyLabel': '',
            'valueLabel': '',
            'DisplayMode': '',
            'showItemCount': False,
            'searchable': False
            },
   'Object': {'type': '',
              'componentized': False,
              'componentMetaType': None,
              'conditionVariables': {},'layout': None,
              'propertyKeys': [],'nullable': True,
              'propertyDisplayMode': PropertyDisplayMode.DataFirst
              },
   'Datetime': {'format': '%Y-%m-%d',
                'displayFormat': 'yyyy-MM-dd',
                'max': None,
                'min': None
                },
   'Custom': {'editAttribute': ''
              }
   }

def GetMetaKeys(editType):
    keys = set(BaseAttr.keys())
    if editType in AttrDict:
        keys |= set(AttrDict[editType].keys())
    return keys


class EditorMeta(object):
    EDIT_TYPE = 'Unknown'

    def __init__(self, **kwargs):
        editType = kwargs.get('editType', None)
        if editType is None:
            editType = self.__class__.EDIT_TYPE
            kwargs['editType'] = editType
        self.attrs = BaseAttr.copy()
        if editType in AttrDict:
            self.attrs.update(AttrDict[editType])
        for k, v in iteritems(kwargs):
            self.attrs[k] = v

        self._ensureAttrSerializable()
        self.children = None
        return

    def _ensureAttrSerializable(self):
        r = self.attrs
        if 'group' in r:
            groups = r['group']
            if isinstance(groups, Group):
                r['group'] = groups.Serialize()
            elif type(groups) in (tuple, list):
                r['group'] = [ g.Serialize() if 1 else g for g in groups if isinstance(g, Group) ]
        if 'preDecorators' in r and r['preDecorators']:
            r['preDecorators'] = [ g.Serialize() if 1 else g for g in r['preDecorators'] if isinstance(g, _LayoutItem) ]
        if 'postDecorators' in r and r['postDecorators']:
            r['postDecorators'] = [ g.Serialize() if 1 else g for g in r['postDecorators'] if isinstance(g, _LayoutItem) ]

    def get(self, name, default=None):
        return self.attrs.get(name, default)

    def GetChildMeta(self, key):
        if isinstance(self.children, dict):
            return self.children.get(key, None)
        else:
            if isinstance(self.children, (list, tuple)):
                key = int(key)
                if key < 0 or key >= len(self.children):
                    return None
                return self.children[key]
            if isinstance(self.children, EditorMeta):
                return self.children
            return None

    def SetChildren(self, children):
        self.children = children

    def copy(self):
        r = EditorMeta(**self.attrs)
        if self.children is not None:
            r.children = self.children.copy()
        return r

    def UpdateMeta(self, meta):
        editType = self.attrs['editType']
        defaultAttrs = BaseAttr.copy()
        defaultAttrs.update(AttrDict[editType])
        defaultAttrs['editType'] = editType
        for k, v in iteritems(meta.attrs):
            if defaultAttrs[k] == v:
                continue
            self.attrs[k] = v

    def ConvertToDict(self):
        r = self.attrs.copy()
        children = self.children
        if isinstance(children, dict):
            attrs = r
            r = dict(((k, v.ConvertToDict()) for k, v in iteritems(children)))
            r['__attribute__'] = attrs
        elif isinstance(children, (list, tuple)):
            r['Array'] = [ i.ConvertToDict() for i in children ]
        elif isinstance(children, EditorMeta):
            r['childAttribute'] = children.ConvertToDict()
        elif children is not None:
            raise Exception('Unsupported children value: ' + repr(children))
        return r

    @classmethod
    def FromDict(cls, data):
        if not isinstance(data, dict):
            return
        else:
            data = copy.deepcopy(data)
            if '__attribute__' in data and isinstance(data['__attribute__'], dict):
                editorMeta = EditorMeta(**data.pop('__attribute__'))
            else:
                editorMeta = EditorMeta(**data)
            if 'Array' in data and isinstance(data['Array'], (tuple, list)):
                children = [ cls.FromDict(k) for k in data['Array'] ]
                editorMeta.SetChildren(children)
            elif 'childAttribute' in data and data.get('editType', None) in ('Array',
                                                                             'FixArray',
                                                                             'ObjectArray'):
                editorMeta.SetChildren(cls.FromDict(data['childAttribute']))
            else:
                children = {k:cls.FromDict(v) for k, v in iteritems(data) if isinstance(v, dict)}
                editorMeta.SetChildren(children)
            return editorMeta

    def GetDefault(self):
        if self.get('editType') == 'Dict' and self.get('default') is None:
            return {key:childMeta.GetDefault() for key, childMeta in iteritems(self.children) if key != '__default__'}
        else:
            return self.get('default')
            return
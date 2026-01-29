# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/EnumMeta.py
__author__ = 'gzhuangwei@corp.netease.com'
from collections import OrderedDict
from .MetaUtils import iteritems
_EnumWatchers = []
EnumMetas = {}

def RegisterEnum(enumType, enum):
    EnumMetas[enumType] = enum
    for watcher in _EnumWatchers:
        watcher(enumType, enum)


def RegisterEnumWatcher(watcher):
    _EnumWatchers.append(watcher)


class EnumMeta(object):

    def GetName(self):
        raise NotImplementedError

    def GetAllValues(self):
        raise NotImplementedError

    def GetDefaultValue(self):
        raise NotImplementedError

    def IsEditable(self):
        return False

    def Serialize(self):
        return {'Style': 0,
           'Type': self.GetName(),
           'Value': self.GetAllValues(),
           'Editable': self.IsEditable()
           }


class TextedEnumMeta(EnumMeta):

    def GetName(self):
        raise NotImplementedError

    def GetAllValues(self):
        raise NotImplementedError

    def GetTextByValue(self, val):
        raise NotImplementedError

    def GetKeyType(self):
        raise NotImplementedError

    def Serialize(self):
        return {'Style': 1,
           'Type': self.GetName(),
           'Value': OrderedDict(((val, self.GetTextByValue(val)) for val in self.GetAllValues())),
           'KeyType': self.GetKeyType(),
           'Editable': self.IsEditable()
           }


class GroupedEnumMeta(TextedEnumMeta):

    def GetName(self):
        raise NotImplementedError

    def GetOrderedGroups(self):
        raise NotImplementedError

    def GetAllValues(self):
        raise NotImplementedError

    def GetTextByValue(self, val):
        raise NotImplementedError

    def GetKeyType(self):
        raise NotImplementedError

    def GetGroupByValue(self, val):
        raise NotImplementedError

    def Serialize(self):
        return {'Style': 2,
           'Type': self.GetName(),
           'Value': dict(((val, {'name': self.GetTextByValue(val),'group': self.GetGroupByValue(val)}) for val in self.GetAllValues())),
           'Groups': self.GetOrderedGroups(),
           'KeyType': self.GetKeyType(),
           'Editable': self.IsEditable()
           }


class DefEnum(TextedEnumMeta):

    def __init__(self, name, valueDict, register=True, editable=False):
        self.name = name
        self.valueDict = valueDict
        self.keyType = None
        self.editable = editable
        self.CheckValueDict()
        if register:
            RegisterEnum(name, self)
        return

    @classmethod
    def fromData(cls, name, data, register=True):
        return cls(name, data['Value'], register, editable=data['Editable'])

    def CheckValueDict(self):
        keyType = None
        valueType = None
        for key, value in iteritems(self.valueDict):
            if keyType is None:
                keyType = type(key)
            if valueType is None:
                valueType = type(value)

        self.keyType = keyType.__name__ if keyType else ''
        return

    def GetTextByValue(self, val):
        return self.valueDict[val]

    def GetName(self):
        return self.name

    def GetAllValues(self):
        return self.valueDict.keys()

    def GetKeyType(self):
        return self.keyType

    def GetDefaultValue(self):
        for k in self.valueDict:
            return k

        return None

    def IsEditable(self):
        return self.editable


class DefGroupedEnum(GroupedEnumMeta):

    def __init__(self, name, register=True, editable=False):
        self.name = name
        self.groupList = []
        self.value2textDict = {}
        self.value2groupDict = {}
        self.editable = editable
        self.register = register
        if register:
            RegisterEnum(name, self)

    @classmethod
    def fromData(cls, name, data, register=True):
        enum = cls(name, register, editable=data['Editable'])
        groups = {}
        for v in data['Value']:
            info = data['Value'][v]
            groups.setdefault(info['group'], {})[v] = info['name']

        for groupName in groups:
            enum.AddGroup(groupName, groups[groupName])

        return enum

    def AddGroup(self, groupName, valueDict):
        groupIdx = len(self.groupList)
        self.groupList.append(groupName)
        for k, v in iteritems(valueDict):
            self.value2textDict[k] = v
            self.value2groupDict[k] = groupIdx

        if self.register:
            RegisterEnum(self.name, self)

    def GetName(self):
        return self.name

    def GetOrderedGroups(self):
        return self.groupList

    def GetGroupByValue(self, val):
        return self.groupList[self.value2groupDict[val]]

    def GetTextByValue(self, val):
        return self.value2textDict[val]

    def GetAllValues(self):
        return self.value2textDict.keys()

    def CheckKeyType(self):
        keyType = None
        valueType = None
        for key, value in iteritems(self.value2textDict):
            if keyType is None:
                keyType = type(key)
            if valueType is None:
                valueType = type(value)

        if keyType:
            return keyType.__name__
        else:
            return ''

    def GetKeyType(self):
        return self.CheckKeyType()

    def GetDefaultValue(self):
        for k in self.value2textDict:
            return k

        return None

    def IsEditable(self):
        return self.editable


def LoadEnum(name, data, register=True):
    keyType = data.get('KeyType', 'str')
    if keyType == 'int':
        _type = int
    elif keyType == 'float':
        _type = float
    else:
        _type = str
    valueDict = {}
    for k in data['Value']:
        valueDict[_type(k)] = data['Value'][k]

    data['Value'] = valueDict
    style = data.get('Style', 1)
    if style == 1:
        return DefEnum.fromData(name, data, register)
    if style == 2:
        return DefGroupedEnum.fromData(name, data, register)


def GetEnumMetaByKey(key):
    return EnumMetas.get(key)


def DelEnum(key):
    return EnumMetas.pop(key, None)
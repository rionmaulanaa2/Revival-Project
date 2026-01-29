# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/PlatformAPI/Platforms/Messiah/TypeMetas.py
from ....Meta.TypeMeta import PDict, PArray

class PAsioMap(PDict):
    valueType = None

    def __init__(self, **kwargs):
        if 'valueType' in kwargs:
            self.valueType = kwargs.pop('valueType')
        super(PAsioMap, self).__init__(**kwargs)

    def GetKeys(self, obj):
        if obj is None:
            return []
        else:
            keys = [ key for key in self.metaMap if key in obj ]
            if keys and 'owner' in keys:
                keys.remove('owner')
            return keys

    def SetRawChildObject(self, obj, key, childObj):
        setattr(obj, key, childObj)

    def GetChildObject(self, obj, key):
        if isinstance(obj, dict):
            return obj.get(key, None)
        else:
            return getattr(obj, key, None)
            return None

    def DeserializeData(self, value):
        return self.valueType(value)

    def SetValue(self, parent, parentMeta, key, value):
        super(PAsioMap, self).SetValue(parent, parentMeta, key, self.DeserializeData(value))


class PAsioList(PArray):
    pass
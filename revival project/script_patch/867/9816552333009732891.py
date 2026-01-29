# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/ComponentMeta.py
import uuid
ComponentMetas = {}
DynamicComponentMetas = {}
_Watchers = []

def RegisterComponentMetaWatcher(watcher):
    _Watchers.append(watcher)


def RegisterComponentMeta(name, meta):
    ComponentMetas[name] = meta
    for watcher in _Watchers:
        watcher(name, meta)


def RegisterDynamicComponentMeta(name, meta):
    DynamicComponentMetas[name] = meta


class ComponentMeta(object):

    def GetName(self):
        raise NotImplementedError

    def AllowedComponents(self):
        return None

    def FixedComponents(self):
        return None

    def MultiComponents(self):
        return None

    def ExclusiveComponents(self):
        return None

    def Serialize(self):
        return {'Style': 0,
           'Type': self.GetName(),
           'AllowedComponents': self.AllowedComponents(),
           'FixedComponents': self.FixedComponents(),
           'MultiComponents': self.MultiComponents(),
           'ExclusiveComponents': self.ExclusiveComponents()
           }


class DefComponentMeta(ComponentMeta):

    def __init__(self, name, allowedComponents=None, fixedComponents=None, multiComponents=None, exclusiveComponents=None, register=True):
        super(DefComponentMeta, self).__init__()
        self.name = name
        self.allowedComponents = allowedComponents
        self.fixedComponents = fixedComponents
        self.multiComponents = multiComponents
        self.exclusiveComponents = exclusiveComponents
        if register:
            RegisterComponentMeta(name, self)

    def GetName(self):
        return self.name

    def AllowedComponents(self):
        return self.allowedComponents

    def FixedComponents(self):
        return self.fixedComponents

    def MultiComponents(self):
        return self.multiComponents

    def ExclusiveComponents(self):
        return self.exclusiveComponents

    def IsAllowed(self, compName):
        if self.allowedComponents is None or compName in self.allowedComponents:
            return True
        else:
            if self.IsFixed(compName):
                return True
            return False

    def IsFixed(self, compName):
        return self.fixedComponents is not None and compName in self.fixedComponents

    def IsMulti(self, compName):
        return self.multiComponents is not None and compName in self.multiComponents

    def GetExclusiveCompNames(self, compName):
        if not self.exclusiveComponents:
            return ()
        exclusiveCompNames = set()
        for _exclusiveComponents in self.exclusiveComponents:
            if compName in _exclusiveComponents:
                exclusiveCompNames.update(_exclusiveComponents)

        if compName in exclusiveCompNames:
            exclusiveCompNames.remove(compName)
        return tuple(exclusiveCompNames)

    def Serialize(self):
        data = super(DefComponentMeta, self).Serialize()
        data['Style'] = 1
        return data


class DefDynamicComponentMeta(object):

    def __init__(self, func, name=None):
        super(DefDynamicComponentMeta, self).__init__()
        self.func = func
        self.name = name or str(uuid.uuid1())
        RegisterDynamicComponentMeta(self.name, self)

    def GetComponentMeta(self, parent):
        data = self.func(parent)
        return DefComponentMeta(None, data.get('AllowedComponents'), data.get('FixedComponents'), data.get('MultiComponents'), register=False)


class DefComponentGroupMeta(DefComponentMeta):
    pass


def GetComponentMeta(key):
    return ComponentMetas.get(key, None)


def GetDynamicComponentMeta(key):
    return DynamicComponentMetas.get(key)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/NodePort.py
__author__ = 'gzhuangwei@corp.netease.com'
from . import StorylineMeta
_ParamPorts = {}

def storyline_parameter_port(cls):
    if cls.PARAM_TYPE not in _ParamPorts:
        _ParamPorts[cls.PARAM_TYPE] = cls
    return cls


def GetParamPortByType(typeName):
    return _ParamPorts.get(typeName, None)


class NodePort(object):
    PARAM_TYPE = ''

    def __init__(self, meta, isTrigger=False):
        super(NodePort, self).__init__()
        self.meta = meta
        self.isTrigger = isTrigger

    def GetName(self):
        return self.meta.name

    def GetTypeName(self):
        return self.meta.portType

    def GetPortMeta(self):
        return self.meta

    def CanConnectFrom(self, fromPort):
        if fromPort.GetTypeName() in ('Any', 'MultiTypes'):
            return True
        return fromPort.GetTypeName() == self.GetTypeName()

    def InputData(self, oldData, fromPort, newData, indegree):
        return newData

    def IsTrigger(self):
        return self.isTrigger

    @classmethod
    def GetDefault(cls):
        return None


NodeInputPort = NodePort

@storyline_parameter_port
class UnknownNodePort(NodePort):
    PARAM_TYPE = 'Unknown'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(UnknownNodePort, self).__init__(StorylineMeta.NodePort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))


@storyline_parameter_port
class FloatNodePort(NodePort):
    PARAM_TYPE = 'Float'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(FloatNodePort, self).__init__(StorylineMeta.FloatPort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    @classmethod
    def GetDefault(cls):
        return 0.0


@storyline_parameter_port
class IntNodePort(NodePort):
    PARAM_TYPE = 'Int'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(IntNodePort, self).__init__(StorylineMeta.IntPort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    @classmethod
    def GetDefault(cls):
        return 0


@storyline_parameter_port
class BoolNodePort(NodePort):
    PARAM_TYPE = 'Bool'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(BoolNodePort, self).__init__(StorylineMeta.BoolPort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    @classmethod
    def GetDefault(cls):
        return False


@storyline_parameter_port
class StrNodePort(NodePort):
    PARAM_TYPE = 'Str'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(StrNodePort, self).__init__(StorylineMeta.StrPort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    @classmethod
    def GetDefault(cls):
        return ''


@storyline_parameter_port
class Vector3NodePort(NodePort):
    PARAM_TYPE = 'Vector3'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None, isTrigger=False):
        super(Vector3NodePort, self).__init__(StorylineMeta.Vector3Port(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes), isTrigger)

    @classmethod
    def GetDefault(cls):
        return [
         0, 0, 0]


@storyline_parameter_port
class AnyNodePort(NodePort):
    PARAM_TYPE = 'Any'

    def __init__(self, name, optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None, isTrigger=False):
        super(AnyNodePort, self).__init__(StorylineMeta.AnyPort(name, name, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes), isTrigger)

    def CanConnectFrom(self, fromPort):
        return True


@storyline_parameter_port
class MultiTypesNodePort(NodePort):
    PARAM_TYPE = 'MultiTypes'

    def __init__(self, name, optional=False, supportedTypes=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(MultiTypesNodePort, self).__init__(StorylineMeta.MultiTypesPort(name, name, optional=optional, supportedTypes=supportedTypes, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    def CanConnectFrom(self, fromPort):
        return True


class TriggerPortMeta(StorylineMeta.NodePort):
    PORT_TYPE = 'Logic'


class TriggerOutPort(NodePort):

    def __init__(self, name='__out__', text='', optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        if name == '__out__':
            text = 'Out'
        text = text or name
        super(TriggerOutPort, self).__init__(TriggerPortMeta(name, text, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes))

    def IsTrigger(self):
        return True


class TriggerInPort(NodePort):

    def __init__(self, name='__in__', text='', optional=False, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        if name == '__in__':
            text = 'In'
        text = text or name
        super(TriggerInPort, self).__init__(TriggerPortMeta(name, text, optional=optional, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes), isTrigger=True)


@storyline_parameter_port
class EntityPort(NodePort):
    PARAM_TYPE = 'Entity'

    def __init__(self, name, entityType=None, isTrigger=False, optional=False, allowedComponents=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(EntityPort, self).__init__(StorylineMeta.EntityPort(name, 'entity', entityType=entityType, optional=optional, allowedComponents=allowedComponents, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes), isTrigger)

    def CanConnectFrom(self, fromPort):
        if not super(EntityPort, self).CanConnectFrom(fromPort):
            return False
        else:
            if self.meta.entityType is None or fromPort.meta.entityType is None or fromPort.GetTypeName() == 'Any':
                return True
            return fromPort.meta.entityType == self.meta.entityType
            return


@storyline_parameter_port
class EntitiesPort(NodePort):
    PARAM_TYPE = 'EntityArray'

    def __init__(self, name, entityType=None, isTrigger=False, optional=False, isOverwrite=False, allowedComponents=None, tip='', limitedConnectCount=-1, canConnectNodeTypes=None):
        super(EntitiesPort, self).__init__(StorylineMeta.EntitiesPort(name, 'entities', entityType=entityType, optional=optional, allowedComponents=allowedComponents, tip=tip, limitedConnectCount=limitedConnectCount, canConnectNodeTypes=canConnectNodeTypes), isTrigger)
        if isOverwrite:
            self.isOverwrite = isOverwrite
        self.inOverwrite = False

    def CanConnectFrom(self, fromPort):
        fromPortTypeName = fromPort.GetTypeName()
        if self.meta.entityType is None or fromPortTypeName == 'Any' or fromPort.meta.entityType is None:
            return True
        else:
            if not fromPortTypeName == 'Entity' and not fromPortTypeName == 'EntityArray':
                return False
            return fromPort.meta.entityType == self.meta.entityType
            return

    def InputData(self, oldData, fromPort, newData, indegree):
        if fromPort == '__Variables__':
            if isinstance(newData, list):
                fromPortTypeName = 'EntityArray' if 1 else 'Entity'
                outOverwrite = False
            else:
                fromPortTypeName = fromPort.GetTypeName()
                outOverwrite = fromPort.__dict__.get('isOverwrite') if fromPortTypeName == 'EntityArray' else False
            if outOverwrite or self.inOverwrite:
                if fromPortTypeName == 'EntityArray':
                    return list(newData)
                return [newData]
            if indegree == 1:
                if fromPortTypeName == 'EntityArray':
                    return list(newData)
                if fromPortTypeName == 'Any' and isinstance(newData, (tuple, list)):
                    return newData
            return [newData]
        oldData = oldData or []
        if fromPortTypeName == 'Entity':
            if newData and newData not in oldData:
                oldData.append(newData)
        elif fromPortTypeName == 'EntityArray':
            if type(newData) is list:
                for d in newData:
                    if d and d not in oldData:
                        oldData.append(d)

        elif fromPortTypeName == 'Any':
            if isinstance(newData, (tuple, list)):
                for x in newData:
                    if x and x not in oldData:
                        oldData.append(x)

            else:
                oldData.append(newData)
        return oldData

    @classmethod
    def GetDefault(cls):
        return []
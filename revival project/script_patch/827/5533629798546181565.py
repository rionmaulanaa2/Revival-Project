# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/NodeManager.py
Nodes = {}
InputParameterNodes = {}
OutputParameterNodes = {}

def storyline_node(cls):
    RegisterNodeClass(cls)
    return cls


def RegisterNodeClass(cls):
    if cls.__name__ not in Nodes:
        Nodes[cls.__name__] = cls


def storyline_input_parameter_node(cls):
    if cls.PARAMETER_NAME not in InputParameterNodes:
        InputParameterNodes[cls.PARAMETER_NAME] = cls
        return cls


def storyline_output_parameter_node(cls):
    if cls.PARAMETER_NAME not in OutputParameterNodes:
        OutputParameterNodes[cls.PARAMETER_NAME] = cls
        return cls


def GetNodeClass(nodeTypeName):
    return Nodes.get(nodeTypeName, None)


def GetAllNodeClasses():
    return Nodes


def CreateNode(nodeTypeName, *args, **kwargs):
    if nodeTypeName in Nodes:
        return Nodes[nodeTypeName](*args, **kwargs)
    else:
        return None


def GetInputParameterNodeClass(clsName):
    return InputParameterNodes.get(clsName, None)


def GetOutputParameterNodeClass(clsName):
    return OutputParameterNodes.get(clsName, None)
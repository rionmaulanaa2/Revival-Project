# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/NodeMetaManager.py
__author__ = 'wanjinsen@corp.netease.com'
from ..Meta import ClassMetaManager
NodeMetas = {}

def storyline_node_meta(cls):
    meta = cls()
    ClassMetaManager.RegisterClassMeta(meta)
    RegisterNodeMeta(meta)
    AutoExportInputNodes(meta)
    return cls


def GenerateNodePort--- This code section failed: ---

  20       0  LOAD_CONST            1  1
           3  LOAD_CONST            2  ('IntNodePort', 'FloatNodePort', 'BoolNodePort', 'StrNodePort', 'Vector3NodePort', 'EntityPort', 'EntitiesPort', 'AnyNodePort')
           6  IMPORT_NAME           0  'NodePort'
           9  IMPORT_FROM           1  'IntNodePort'
          12  STORE_FAST            2  'IntNodePort'
          15  IMPORT_FROM           2  'FloatNodePort'
          18  STORE_FAST            3  'FloatNodePort'
          21  IMPORT_FROM           3  'BoolNodePort'
          24  STORE_FAST            4  'BoolNodePort'
          27  IMPORT_FROM           4  'StrNodePort'
          30  STORE_FAST            5  'StrNodePort'
          33  IMPORT_FROM           5  'Vector3NodePort'
          36  STORE_FAST            6  'Vector3NodePort'
          39  IMPORT_FROM           6  'EntityPort'
          42  STORE_FAST            7  'EntityPort'
          45  IMPORT_FROM           7  'EntitiesPort'
          48  STORE_FAST            8  'EntitiesPort'
          51  IMPORT_FROM           8  'AnyNodePort'
          54  STORE_FAST            9  'AnyNodePort'
          57  POP_TOP          

  23      58  BUILD_MAP_8           8 

  24      61  LOAD_FAST             9  'AnyNodePort'
          64  LOAD_CONST            3  'Any'
          67  STORE_MAP        

  25      68  LOAD_FAST             2  'IntNodePort'
          71  LOAD_CONST            4  'Int'
          74  STORE_MAP        

  26      75  LOAD_FAST             3  'FloatNodePort'
          78  LOAD_CONST            5  'Float'
          81  STORE_MAP        

  27      82  LOAD_FAST             4  'BoolNodePort'
          85  LOAD_CONST            6  'Bool'
          88  STORE_MAP        

  28      89  LOAD_FAST             5  'StrNodePort'
          92  LOAD_CONST            7  'Str'
          95  STORE_MAP        

  29      96  LOAD_FAST             6  'Vector3NodePort'
          99  LOAD_CONST            8  'Vector3'
         102  STORE_MAP        

  30     103  LOAD_FAST             7  'EntityPort'
         106  LOAD_CONST            9  'Entity'
         109  STORE_MAP        

  31     110  LOAD_FAST             8  'EntitiesPort'
         113  LOAD_CONST           10  'EntityArray'
         116  STORE_MAP        
         117  STORE_FAST           10  'portClasses'

  34     120  LOAD_FAST            10  'portClasses'
         123  LOAD_FAST             1  'propMeta'
         126  LOAD_ATTR             9  'editorMeta'
         129  LOAD_ATTR            10  'get'
         132  LOAD_CONST           11  'editType'
         135  CALL_FUNCTION_1       1 
         138  BINARY_SUBSCR    
         139  STORE_FAST           11  'cls'

  35     142  LOAD_FAST             1  'propMeta'
         145  LOAD_ATTR             9  'editorMeta'
         148  LOAD_ATTR            10  'get'
         151  LOAD_CONST           12  'text'
         154  CALL_FUNCTION_1       1 
         157  STORE_FAST           12  'text'

  36     160  LOAD_FAST            12  'text'
         163  POP_JUMP_IF_TRUE    175  'to 175'

  37     166  LOAD_FAST             0  'propName'
         169  STORE_FAST           12  'text'
         172  JUMP_FORWARD          0  'to 175'
       175_0  COME_FROM                '172'

  38     175  LOAD_FAST            11  'cls'
         178  LOAD_CONST           13  'name'
         181  LOAD_CONST           14  'optional'
         184  LOAD_GLOBAL          11  'True'
         187  CALL_FUNCTION_512   512 
         190  STORE_FAST           13  'port'

  39     193  LOAD_FAST            12  'text'
         196  LOAD_FAST            13  'port'
         199  LOAD_ATTR            12  'meta'
         202  STORE_ATTR           13  'text'

  40     205  LOAD_FAST            13  'port'
         208  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_512' instruction at offset 187


def AutoExportInputNodes(meta):
    from . import NodeManager
    nodeCls = NodeManager.GetNodeClass(meta.CLASS_NAME)
    if not nodeCls:
        return
    inputPorts = set()
    from .NodePort import TriggerInPort
    if 'INPUT_PORTS' in nodeCls.__dict__:
        for port in nodeCls.INPUT_PORTS:
            inputPorts.add(port.GetName())

    elif nodeCls.NODE_META_TYPE == 'Action':
        nodeCls.INPUT_PORTS = [
         TriggerInPort()]
    else:
        nodeCls.INPUT_PORTS = []
    props = meta.GetAllProperties()
    for name, propMeta in props.items():
        if propMeta.GetEditType() in ('Any', 'Bool', 'Int', 'Float', 'Str', 'Vector3',
                                      'Entity', 'EntityArray') and name not in inputPorts:
            port = GenerateNodePort(name, propMeta)
            nodeCls.INPUT_PORTS.append(port)


def RegisterNodeMeta(meta):
    global NodeMetas
    from .NodeMeta import NodeMeta
    if meta.className not in NodeMetas:
        NodeMetas[meta.className] = meta


def GetNodeMeta(nodeType):
    return NodeMetas.get(nodeType)


def GetAllClassMetas():
    return NodeMetas
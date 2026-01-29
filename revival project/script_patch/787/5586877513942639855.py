# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/Messiah/EntityUtils.py
from MObject import IEntity

def __GetIEntity--- This code section failed: ---

   6       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'isinstance'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    37  'to 37'
          12  LOAD_GLOBAL           1  'isinstance'
          15  LOAD_FAST             0  'entity'
          18  LOAD_ATTR             2  'instance'
          21  LOAD_GLOBAL           3  'IEntity'
          24  CALL_FUNCTION_2       2 
        27_0  COME_FROM                '9'
          27  POP_JUMP_IF_FALSE    37  'to 37'

   7      30  LOAD_FAST             0  'entity'
          33  LOAD_ATTR             2  'instance'
          36  RETURN_END_IF    
        37_0  COME_FROM                '27'

   8      37  LOAD_GLOBAL           0  'hasattr'
          40  LOAD_GLOBAL           2  'instance'
          43  CALL_FUNCTION_2       2 
          46  POP_JUMP_IF_FALSE   126  'to 126'

   9      49  LOAD_GLOBAL           1  'isinstance'
          52  LOAD_FAST             0  'entity'
          55  LOAD_ATTR             4  'model'
          58  LOAD_GLOBAL           3  'IEntity'
          61  CALL_FUNCTION_2       2 
          64  POP_JUMP_IF_FALSE    74  'to 74'

  10      67  LOAD_FAST             0  'entity'
          70  LOAD_ATTR             4  'model'
          73  RETURN_END_IF    
        74_0  COME_FROM                '64'

  11      74  LOAD_GLOBAL           0  'hasattr'
          77  LOAD_FAST             0  'entity'
          80  LOAD_ATTR             4  'model'
          83  LOAD_CONST            2  'model'
          86  CALL_FUNCTION_2       2 
          89  POP_JUMP_IF_FALSE   130  'to 130'
          92  LOAD_GLOBAL           1  'isinstance'
          95  LOAD_FAST             0  'entity'
          98  LOAD_ATTR             4  'model'
         101  LOAD_ATTR             4  'model'
         104  LOAD_GLOBAL           3  'IEntity'
         107  CALL_FUNCTION_2       2 
       110_0  COME_FROM                '89'
         110  POP_JUMP_IF_FALSE   130  'to 130'

  12     113  LOAD_FAST             0  'entity'
         116  LOAD_ATTR             4  'model'
         119  LOAD_ATTR             4  'model'
         122  RETURN_END_IF    
       123_0  COME_FROM                '110'
         123  JUMP_FORWARD          4  'to 130'

  14     126  LOAD_CONST            0  ''
         129  RETURN_VALUE     
       130_0  COME_FROM                '123'
         130  LOAD_CONST            0  ''
         133  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


_GetIEntity = __GetIEntity

def GetIEntity(entity):
    global _GetIEntity
    return _GetIEntity(entity)


def SetGetIEntity(getIEntity):
    global _GetIEntity
    _GetIEntity = getIEntity


TRANSFORM_NAMELIST = [
 ('position', 'pos'),
 ('direction', 'dir', 'yaw'),
 ('scale', )]

def __GetEntityTransformName(entity):
    position = direction = scale = ''
    for name in TRANSFORM_NAMELIST[0]:
        value = getattr(entity, name, None)
        if isinstance(value, (tuple, list)) and len(value) == 3 and all((isinstance(v, (int, float)) for v in value)):
            position = name
            break

    for name in TRANSFORM_NAMELIST[1]:
        value = getattr(entity, name, None)
        if isinstance(value, (int, float)):
            direction = name
            break

    for name in TRANSFORM_NAMELIST[2]:
        value = getattr(entity, name, None)
        if isinstance(value, (int, float)):
            scale = name
            break

    return (
     position, direction, scale)


_GetEntityTransformName = __GetEntityTransformName

def GetEntityTransformName(entity):
    global _GetEntityTransformName
    return _GetEntityTransformName(entity)


def SetGetEntityTransform(getEntityTransformName):
    global _GetEntityTransformName
    _GetEntityTransformName = getEntityTransformName
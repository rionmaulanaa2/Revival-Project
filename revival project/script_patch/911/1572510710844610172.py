# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/PropertyObject.py
from .TypeMeta import BaseClassMeta, InitObject, UpdateObject, OrderedProperties
from . import ClassMetaManager
import inspect

def sunshine_property_object(cls):
    RegisterPropertyObjectMeta(cls)
    return cls


def RegisterPropertyObjectMeta--- This code section failed: ---

  16       0  LOAD_GLOBAL           0  'OrderedProperties'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            1  'props'

  17       9  BUILD_MAP_0           0 
          12  STORE_FAST            2  'editorAttrs'

  19      15  LOAD_GLOBAL           1  'inspect'
          18  LOAD_ATTR             2  'getmro'
          21  LOAD_FAST             0  'cls'
          24  CALL_FUNCTION_1       1 
          27  STORE_FAST            3  'bases'

  22      30  LOAD_FAST             3  'bases'
          33  LOAD_CONST            1  -1
          36  SLICE+2          
          37  STORE_FAST            3  'bases'

  24      40  SETUP_LOOP          273  'to 316'
          43  LOAD_GLOBAL           3  'reversed'
          46  LOAD_FAST             3  'bases'
          49  CALL_FUNCTION_1       1 
          52  GET_ITER         
          53  FOR_ITER            259  'to 315'
          56  STORE_FAST            4  'base'

  25      59  LOAD_CONST            2  'PROPERTIES'
          62  LOAD_FAST             4  'base'
          65  LOAD_ATTR             4  '__dict__'
          68  COMPARE_OP            6  'in'
          71  POP_JUMP_IF_FALSE    99  'to 99'

  26      74  LOAD_FAST             1  'props'
          77  LOAD_ATTR             5  'update'
          80  LOAD_FAST             4  'base'
          83  LOAD_ATTR             6  'PROPERTIES'
          86  LOAD_ATTR             7  'copy'
          89  CALL_FUNCTION_0       0 
          92  CALL_FUNCTION_1       1 
          95  POP_TOP          
          96  JUMP_FORWARD          0  'to 99'
        99_0  COME_FROM                '96'

  27      99  LOAD_CONST            3  'EDITOR_ATTRIBUTES'
         102  LOAD_FAST             4  'base'
         105  LOAD_ATTR             4  '__dict__'
         108  COMPARE_OP            6  'in'
         111  POP_JUMP_IF_FALSE   188  'to 188'

  28     114  LOAD_FAST             4  'base'
         117  LOAD_ATTR             8  'EDITOR_ATTRIBUTES'
         120  LOAD_ATTR             7  'copy'
         123  CALL_FUNCTION_0       0 
         126  STORE_FAST            5  'ea'

  30     129  LOAD_FAST             5  'ea'
         132  LOAD_ATTR             9  'pop'
         135  LOAD_CONST            4  'conditionVariables'
         138  BUILD_MAP_0           0 
         141  CALL_FUNCTION_2       2 
         144  STORE_FAST            6  'conditionVariables'

  31     147  LOAD_FAST             2  'editorAttrs'
         150  LOAD_ATTR             5  'update'
         153  LOAD_FAST             5  'ea'
         156  CALL_FUNCTION_1       1 
         159  POP_TOP          

  32     160  LOAD_FAST             2  'editorAttrs'
         163  LOAD_ATTR            10  'setdefault'
         166  LOAD_CONST            4  'conditionVariables'
         169  BUILD_MAP_0           0 
         172  CALL_FUNCTION_2       2 
         175  LOAD_ATTR             5  'update'
         178  LOAD_FAST             6  'conditionVariables'
         181  CALL_FUNCTION_1       1 
         184  POP_TOP          
         185  JUMP_FORWARD          0  'to 188'
       188_0  COME_FROM                '185'

  33     188  LOAD_CONST            5  'COMPONENTIZED'
         191  LOAD_FAST             4  'base'
         194  LOAD_ATTR             4  '__dict__'
         197  COMPARE_OP            6  'in'
         200  POP_JUMP_IF_FALSE   219  'to 219'

  34     203  LOAD_FAST             4  'base'
         206  LOAD_ATTR            11  'COMPONENTIZED'
         209  LOAD_FAST             2  'editorAttrs'
         212  LOAD_CONST            6  'componentized'
         215  STORE_SUBSCR     
         216  JUMP_FORWARD          0  'to 219'
       219_0  COME_FROM                '216'

  35     219  LOAD_CONST            7  'COMPONENT_META_TYPE'
         222  LOAD_FAST             4  'base'
         225  LOAD_ATTR             4  '__dict__'
         228  COMPARE_OP            6  'in'
         231  POP_JUMP_IF_FALSE   250  'to 250'

  36     234  LOAD_FAST             4  'base'
         237  LOAD_ATTR            12  'COMPONENT_META_TYPE'
         240  LOAD_FAST             2  'editorAttrs'
         243  LOAD_CONST            8  'componentMetaType'
         246  STORE_SUBSCR     
         247  JUMP_FORWARD          0  'to 250'
       250_0  COME_FROM                '247'

  37     250  LOAD_CONST            9  'OBJECT_VISITOR'
         253  LOAD_FAST             4  'base'
         256  LOAD_ATTR             4  '__dict__'
         259  COMPARE_OP            6  'in'
         262  POP_JUMP_IF_FALSE   281  'to 281'

  38     265  LOAD_FAST             4  'base'
         268  LOAD_ATTR            13  'OBJECT_VISITOR'
         271  LOAD_FAST             2  'editorAttrs'
         274  LOAD_CONST           10  'objVisitor'
         277  STORE_SUBSCR     
         278  JUMP_FORWARD          0  'to 281'
       281_0  COME_FROM                '278'

  39     281  LOAD_CONST           11  'SERIALIZE_ALL_PROPERTIES'
         284  LOAD_FAST             4  'base'
         287  LOAD_ATTR             4  '__dict__'
         290  COMPARE_OP            6  'in'
         293  POP_JUMP_IF_FALSE    53  'to 53'

  40     296  LOAD_FAST             4  'base'
         299  LOAD_ATTR            14  'SERIALIZE_ALL_PROPERTIES'
         302  LOAD_FAST             2  'editorAttrs'
         305  LOAD_CONST           12  'serializeAllProperties'
         308  STORE_SUBSCR     
         309  JUMP_BACK            53  'to 53'
         312  JUMP_BACK            53  'to 53'
         315  POP_BLOCK        
       316_0  COME_FROM                '40'

  41     316  LOAD_GLOBAL          15  'hasattr'
         319  LOAD_GLOBAL          13  'OBJECT_VISITOR'
         322  CALL_FUNCTION_2       2 
         325  POP_JUMP_IF_FALSE   359  'to 359'
         328  LOAD_FAST             0  'cls'
         331  LOAD_ATTR            16  'LAYOUT'
       334_0  COME_FROM                '325'
         334  POP_JUMP_IF_FALSE   359  'to 359'

  42     337  LOAD_FAST             0  'cls'
         340  LOAD_ATTR            16  'LAYOUT'
         343  LOAD_ATTR            17  'Serialize'
         346  CALL_FUNCTION_0       0 
         349  LOAD_FAST             2  'editorAttrs'
         352  LOAD_CONST           14  'layout'
         355  STORE_SUBSCR     
         356  JUMP_FORWARD          0  'to 359'
       359_0  COME_FROM                '356'

  43     359  LOAD_GLOBAL          18  'getattr'
         362  LOAD_GLOBAL          15  'hasattr'
         365  LOAD_CONST            0  ''
         368  CALL_FUNCTION_3       3 
         371  JUMP_IF_TRUE_OR_POP   377  'to 377'
         374  LOAD_GLOBAL          20  'BaseClassMeta'
       377_0  COME_FROM                '371'
         377  LOAD_FAST             0  'cls'
         380  LOAD_ATTR            21  '__name__'
         383  LOAD_FAST             1  'props'
         386  LOAD_FAST             2  'editorAttrs'
         389  CALL_FUNCTION_KW_2     2 
         392  STORE_FAST            7  'meta'

  44     395  LOAD_GLOBAL          22  'ClassMetaManager'
         398  LOAD_ATTR            23  'RegisterClassMeta'
         401  LOAD_FAST             7  'meta'
         404  CALL_FUNCTION_1       1 
         407  POP_TOP          
         408  LOAD_CONST            0  ''
         411  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 322


class PropertyObject(object):
    PROPERTY_META_CLASS = None
    PROPERTIES = {}
    EDITOR_ATTRIBUTES = {}
    COMPONENTIZED = False
    COMPONENT_META_TYPE = None
    OBJECT_VISITOR = None
    LAYOUT = None
    SERIALIZE_ALL_PROPERTIES = False

    def __init__(self, args=None):
        meta = self.GetClassMeta()
        InitObject(self, meta, args)

    def UpdateWithDict(self, args):
        meta = self.GetClassMeta()
        UpdateObject(self, meta, args)

    def Serialize(self):
        meta = self.GetClassMeta()
        return meta.SerializeData(self)

    def Export(self, ignoreDefault=True):
        meta = self.GetClassMeta()
        return meta.Export(self, ignoreDefault)

    def GetEditorMeta(self):
        meta = self.GetClassMeta()
        return meta.GetEditorMeta()

    def GetDynamicEditorMeta(self):
        meta = self.GetClassMeta()
        return meta.GetDynamicEditorMeta(self)

    def GetClassMeta(self):
        return ClassMetaManager.GetClassMeta(self.__class__.__name__)
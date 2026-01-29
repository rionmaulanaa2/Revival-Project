# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/lib/msgpack/bson_msgpack.py
import bson.objectid as objectid
import datetime
from mobile.common.IdManager import IdManager
import msgpack
from msgpack.exceptions import UnpackValueError
ExtType = msgpack.ExtType

def msgpackext(obj):
    if isinstance(obj, objectid.ObjectId):
        return ExtType(42, IdManager.id2bytes(obj))
    if isinstance(obj, datetime.datetime):
        return ExtType(43, obj.strftime('%Y-%m-%d-%H-%M-%S-%f'))
    return repr(obj)


def ext_hook--- This code section failed: ---

  26       0  SETUP_EXCEPT        157  'to 160'

  27       3  SETUP_EXCEPT          1  'to 7'
           6  COMPARE_OP            2  '=='
           9  POP_JUMP_IF_FALSE    25  'to 25'

  28      12  LOAD_GLOBAL           0  'IdManager'
          15  LOAD_ATTR             1  'bytes2id'
          18  LOAD_FAST             1  'data'
          21  CALL_FUNCTION_1       1 
          24  RETURN_END_IF    
        25_0  COME_FROM                '9'

  29      25  RETURN_VALUE     
          26  RETURN_VALUE     
          27  RETURN_VALUE     
          28  COMPARE_OP            2  '=='
          31  POP_JUMP_IF_FALSE   156  'to 156'

  30      34  LOAD_GLOBAL           2  'str'
          37  LOAD_FAST             1  'data'
          40  CALL_FUNCTION_1       1 
          43  LOAD_ATTR             3  'split'
          46  LOAD_CONST            3  '-'
          49  CALL_FUNCTION_1       1 
          52  STORE_FAST            2  'strlist'

  31      55  LOAD_GLOBAL           4  'datetime'
          58  LOAD_ATTR             4  'datetime'
          61  LOAD_GLOBAL           5  'int'
          64  LOAD_FAST             2  'strlist'
          67  LOAD_CONST            4  ''
          70  BINARY_SUBSCR    
          71  CALL_FUNCTION_1       1 
          74  LOAD_GLOBAL           5  'int'
          77  LOAD_FAST             2  'strlist'
          80  LOAD_CONST            5  1
          83  BINARY_SUBSCR    
          84  CALL_FUNCTION_1       1 
          87  LOAD_GLOBAL           5  'int'
          90  LOAD_FAST             2  'strlist'
          93  LOAD_CONST            6  2
          96  BINARY_SUBSCR    
          97  CALL_FUNCTION_1       1 
         100  LOAD_GLOBAL           5  'int'
         103  LOAD_FAST             2  'strlist'
         106  LOAD_CONST            7  3
         109  BINARY_SUBSCR    
         110  CALL_FUNCTION_1       1 
         113  LOAD_GLOBAL           5  'int'
         116  LOAD_FAST             2  'strlist'
         119  LOAD_CONST            8  4
         122  BINARY_SUBSCR    
         123  CALL_FUNCTION_1       1 
         126  LOAD_GLOBAL           5  'int'
         129  LOAD_FAST             2  'strlist'
         132  LOAD_CONST            9  5
         135  BINARY_SUBSCR    
         136  CALL_FUNCTION_1       1 
         139  LOAD_GLOBAL           5  'int'
         142  LOAD_FAST             2  'strlist'
         145  LOAD_CONST           10  6
         148  BINARY_SUBSCR    
         149  CALL_FUNCTION_1       1 
         152  CALL_FUNCTION_7       7 
         155  RETURN_END_IF    
       156_0  COME_FROM                '182'
       156_1  COME_FROM                '31'
         156  POP_BLOCK        
         157  JUMP_FORWARD         23  'to 183'
       160_0  COME_FROM                '0'

  32     160  POP_TOP          
         161  POP_TOP          
         162  POP_TOP          

  33     163  LOAD_GLOBAL           6  'UnpackValueError'
         166  LOAD_CONST           11  'Code %s data error.'
         169  LOAD_FAST             0  'code'
         172  BINARY_MODULO    
         173  CALL_FUNCTION_1       1 
         176  RAISE_VARARGS_1       1 
         179  JUMP_FORWARD          1  'to 183'
         182  END_FINALLY      
       183_0  COME_FROM                '157'

  34     183  LOAD_GLOBAL           7  'ExtType'
         186  LOAD_FAST             0  'code'
         189  LOAD_FAST             1  'data'
         192  CALL_FUNCTION_2       2 
         195  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `COMPARE_OP' instruction at offset 6
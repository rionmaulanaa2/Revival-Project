# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileJsonUtil.py
from __future__ import absolute_import
from __future__ import print_function
import six
import json

class NileJsonUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def Serialize--- This code section failed: ---

  17       0  SETUP_EXCEPT         20  'to 23'

  18       3  LOAD_GLOBAL           0  'json'
           6  LOAD_ATTR             1  'dumps'
           9  LOAD_ATTR             1  'dumps'
          12  LOAD_GLOBAL           2  'False'
          15  CALL_FUNCTION_257   257 
          18  RETURN_VALUE     
          19  POP_BLOCK        
          20  JUMP_FORWARD         60  'to 83'
        23_0  COME_FROM                '0'

  19      23  DUP_TOP          
          24  LOAD_GLOBAL           3  'BaseException'
          27  COMPARE_OP           10  'exception-match'
          30  POP_JUMP_IF_FALSE    82  'to 82'
          33  POP_TOP          
          34  STORE_FAST            1  'e'
          37  POP_TOP          

  20      38  LOAD_GLOBAL           4  'print'
          41  LOAD_CONST            2  '\xe5\xaf\xb9\xe8\xb1\xa1\xe5\xba\x8f\xe5\x88\x97\xe5\x8c\x96\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8cObject: %s Type: %s, Message: %s'
          44  LOAD_GLOBAL           5  'str'
          47  LOAD_FAST             0  'dictObj'
          50  CALL_FUNCTION_1       1 
          53  LOAD_GLOBAL           6  'type'
          56  LOAD_FAST             0  'dictObj'
          59  CALL_FUNCTION_1       1 
          62  LOAD_GLOBAL           5  'str'
          65  LOAD_FAST             1  'e'
          68  CALL_FUNCTION_1       1 
          71  BUILD_TUPLE_3         3 
          74  BINARY_MODULO    
          75  CALL_FUNCTION_1       1 
          78  POP_TOP          
          79  JUMP_FORWARD          1  'to 83'
          82  END_FINALLY      
        83_0  COME_FROM                '82'
        83_1  COME_FROM                '20'

  21      83  LOAD_CONST            3  ''
          86  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_257' instruction at offset 15

    @staticmethod
    def Deserialize(jsonStr, convertUnicodeToStr=True):
        try:
            result = json.loads(jsonStr)
        except BaseException as e:
            print('\xe5\x8f\x8d\xe5\xba\x8f\xe5\x88\x97\xe5\x8c\x96\xe5\xa4\xb1\xe8\xb4\xa5, Json: %s, Message: %s' % (jsonStr, str(e)))
            result = dict()

        if convertUnicodeToStr:
            result = NileJsonUtil.Stringify(result)
        return result

    @staticmethod
    def Stringify(obj, encoding='utf-8'):
        if isinstance(obj, dict):
            return {NileJsonUtil.Stringify(key):NileJsonUtil.Stringify(value) for key, value in six.iteritems(obj)}
        else:
            if isinstance(obj, list):
                return [ NileJsonUtil.Stringify(element) for element in obj ]
            if isinstance(obj, six.text_type):
                return six.ensure_str(obj)
            return obj
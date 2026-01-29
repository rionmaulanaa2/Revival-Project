# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileServiceRedDotHub.py


class NileServiceRedDotHub(object):

    def __init__(self):
        self._dotDict = dict()

    def SetActivityRedDot--- This code section failed: ---

  10       0  LOAD_GLOBAL           0  'False'
           3  STORE_FAST            3  'shouldNotifyRedDotToGame'

  11       6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  '_dotDict'
          12  LOAD_ATTR             2  'get'
          15  LOAD_FAST             1  'activityId'
          18  LOAD_CONST            1  ''
          21  CALL_FUNCTION_2       2 
          24  STORE_FAST            4  'oldValue'

  12      27  LOAD_FAST             2  'status'
          30  LOAD_FAST             4  'oldValue'
          33  COMPARE_OP            3  '!='
          36  POP_JUMP_IF_FALSE    48  'to 48'

  13      39  LOAD_GLOBAL           3  'True'
          42  STORE_FAST            3  'shouldNotifyRedDotToGame'
          45  JUMP_FORWARD          0  'to 48'
        48_0  COME_FROM                '45'

  14      48  LOAD_FAST             2  'status'
          51  LOAD_FAST             0  'self'
          54  LOAD_ATTR             1  '_dotDict'
          57  LOAD_FAST             1  'activityId'
          60  STORE_SUBSCR     

  15      61  LOAD_FAST             3  'shouldNotifyRedDotToGame'
          64  POP_JUMP_IF_FALSE   151  'to 151'

  16      67  LOAD_FAST             0  'self'
          70  LOAD_ATTR             1  '_dotDict'
          73  LOAD_FAST             1  'activityId'
          76  BINARY_SUBSCR    
          77  LOAD_CONST            2  1
          80  COMPARE_OP            2  '=='
          83  POP_JUMP_IF_FALSE    92  'to 92'
          86  LOAD_GLOBAL           3  'True'
          89  JUMP_FORWARD          3  'to 95'
          92  LOAD_GLOBAL           0  'False'
        95_0  COME_FROM                '89'
          95  STORE_FAST            5  'statusBool'

  18      98  LOAD_GLOBAL           4  'getattr'
         101  LOAD_GLOBAL           3  'True'
         104  LOAD_CONST            0  ''
         107  CALL_FUNCTION_3       3 
         110  STORE_FAST            6  'func'

  19     113  LOAD_FAST             6  'func'
         116  POP_JUMP_IF_FALSE   151  'to 151'

  20     119  LOAD_FAST             6  'func'
         122  LOAD_CONST            4  'message'
         125  BUILD_MAP_1           1 
         128  LOAD_FAST             5  'statusBool'
         131  LOAD_CONST            5  'value'
         134  STORE_MAP        
         135  LOAD_CONST            6  'activityId'
         138  LOAD_FAST             1  'activityId'
         141  CALL_FUNCTION_512   512 
         144  POP_TOP          
         145  JUMP_ABSOLUTE       151  'to 151'
         148  JUMP_FORWARD          0  'to 151'
       151_0  COME_FROM                '148'
         151  LOAD_CONST            0  ''
         154  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 107

    def GetActivityRedDot(self, activityId):
        if activityId not in self._dotDict:
            return False
        if self._dotDict[activityId] == 1:
            return True
        return False

    def _ClearRedDotDict(self):
        self._dotDict = dict()
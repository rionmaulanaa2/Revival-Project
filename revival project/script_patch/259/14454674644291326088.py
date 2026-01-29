# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileHttpLoaderHelper.py
from __future__ import absolute_import
import six_ex
from .NileUtil import NileUtil

class NileHttpLoaderHelper(object):

    @staticmethod
    def GeneratePostHeader--- This code section failed: ---

  13       0  LOAD_CONST            1  1
           3  LOAD_CONST            2  ('NileService',)
           6  IMPORT_NAME           0  'NileService'
           9  IMPORT_FROM           0  'NileService'
          12  STORE_FAST            1  'NileService'
          15  POP_TOP          

  14      16  LOAD_FAST             1  'NileService'
          19  LOAD_ATTR             1  'GetInstance'
          22  CALL_FUNCTION_0       0 
          25  LOAD_ATTR             2  'GetUserData'
          28  CALL_FUNCTION_0       0 
          31  STORE_FAST            2  'userData'

  15      34  BUILD_MAP_22         22 

  16      37  LOAD_CONST            3  'application/json'
          40  LOAD_CONST            4  'Content-Type'
          43  STORE_MAP        

  17      44  LOAD_CONST            5  'close'
          47  LOAD_CONST            6  'Connection'
          50  STORE_MAP        

  18      51  LOAD_FAST             2  'userData'
          54  LOAD_ATTR             3  'token'
          57  LOAD_CONST            7  'Nile-Client-Token'
          60  STORE_MAP        

  19      61  LOAD_FAST             2  'userData'
          64  LOAD_ATTR             4  'sdkVersion'
          67  LOAD_CONST            8  'Nile-Client-SystemSdkVersion'
          70  STORE_MAP        

  20      71  LOAD_GLOBAL           5  'NileUtil'
          74  LOAD_ATTR             6  'CalculateSign'
          77  LOAD_ATTR             9  'str'
          80  LOAD_CONST           10  ''
          83  LOAD_FAST             2  'userData'
          86  LOAD_ATTR             3  'token'
          89  CALL_FUNCTION_4       4 
          92  LOAD_CONST           11  'Nile-Client-Sign'
          95  STORE_MAP        

  21      96  LOAD_FAST             2  'userData'
          99  LOAD_ATTR             7  'accountId'
         102  LOAD_CONST           12  'Nile-Client-AccountId'
         105  STORE_MAP        

  22     106  LOAD_FAST             2  'userData'
         109  LOAD_ATTR             8  'aid'
         112  LOAD_CONST           13  'Nile-Client-Aid'
         115  STORE_MAP        

  23     116  LOAD_GLOBAL           9  'str'
         119  LOAD_FAST             2  'userData'
         122  LOAD_ATTR            10  'roleLevel'
         125  CALL_FUNCTION_1       1 
         128  LOAD_CONST           14  'Nile-Client-RoleLevel'
         131  STORE_MAP        

  24     132  LOAD_FAST             2  'userData'
         135  LOAD_ATTR            11  'loginTime'
         138  LOAD_CONST           15  'Nile-Client-LoginTime'
         141  STORE_MAP        

  25     142  LOAD_FAST             2  'userData'
         145  LOAD_ATTR            12  'network'
         148  LOAD_CONST           16  'Nile-Client-Network'
         151  STORE_MAP        

  26     152  LOAD_FAST             2  'userData'
         155  LOAD_ATTR            13  'osName'
         158  LOAD_CONST           17  'Nile-Client-OsName'
         161  STORE_MAP        

  27     162  LOAD_FAST             2  'userData'
         165  LOAD_ATTR            14  'osVer'
         168  LOAD_CONST           18  'Nile-Client-OsVer'
         171  STORE_MAP        

  28     172  LOAD_FAST             2  'userData'
         175  LOAD_ATTR            15  'appVer'
         178  LOAD_CONST           19  'Nile-Client-AppVer'
         181  STORE_MAP        

  29     182  LOAD_FAST             2  'userData'
         185  LOAD_ATTR            16  'appChannel'
         188  LOAD_CONST           20  'Nile-Client-AppChannel'
         191  STORE_MAP        

  30     192  LOAD_FAST             2  'userData'
         195  LOAD_ATTR            17  'engineVer'
         198  LOAD_CONST           21  'Nile-Client-EngineVer'
         201  STORE_MAP        

  31     202  LOAD_FAST             2  'userData'
         205  LOAD_ATTR            18  'macAddr'
         208  LOAD_CONST           22  'Nile-Client-MacAddr'
         211  STORE_MAP        

  32     212  LOAD_FAST             2  'userData'
         215  LOAD_ATTR            19  'deviceModel'
         218  LOAD_CONST           23  'Nile-Client-DeviceModel'
         221  STORE_MAP        

  33     222  LOAD_FAST             2  'userData'
         225  LOAD_ATTR            20  'platform'
         228  LOAD_CONST           24  'Nile-Client-Platform'
         231  STORE_MAP        

  34     232  LOAD_FAST             2  'userData'
         235  LOAD_ATTR            21  'textureFormat'
         238  LOAD_CONST           25  'Nile-Client-TextureFormat'
         241  STORE_MAP        

  35     242  LOAD_FAST             2  'userData'
         245  LOAD_ATTR            22  'language'
         248  LOAD_CONST           26  'Nile-client-AcceptLanguage'
         251  STORE_MAP        

  36     252  LOAD_FAST             2  'userData'
         255  LOAD_ATTR            23  'countryCode'
         258  LOAD_CONST           27  'Nile-Client-CountryCode'
         261  STORE_MAP        

  37     262  LOAD_FAST             2  'userData'
         265  LOAD_ATTR            24  'serverVersion'
         268  LOAD_CONST           28  'Nile-Client-ServerVersion'
         271  STORE_MAP        
         272  STORE_FAST            3  'header'

  39     275  SETUP_LOOP           45  'to 323'
         278  LOAD_GLOBAL          25  'six_ex'
         281  LOAD_ATTR            26  'items'
         284  LOAD_FAST             3  'header'
         287  CALL_FUNCTION_1       1 
         290  GET_ITER         
         291  FOR_ITER             28  'to 322'
         294  UNPACK_SEQUENCE_2     2 
         297  STORE_FAST            4  'key'
         300  STORE_FAST            5  'value'

  40     303  LOAD_GLOBAL           9  'str'
         306  LOAD_FAST             5  'value'
         309  CALL_FUNCTION_1       1 
         312  LOAD_FAST             3  'header'
         315  LOAD_FAST             4  'key'
         318  STORE_SUBSCR     
         319  JUMP_BACK           291  'to 291'
         322  POP_BLOCK        
       323_0  COME_FROM                '275'

  41     323  LOAD_FAST             3  'header'
         326  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_4' instruction at offset 89
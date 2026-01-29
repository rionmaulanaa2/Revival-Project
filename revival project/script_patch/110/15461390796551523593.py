# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileSettings.py
from __future__ import absolute_import
from __future__ import print_function
from ..Utils.NileFileSystem import NileFileSystem
from ..Utils.NileJsonUtil import NileJsonUtil
from ..Utils.NileSystemInfo import NileSystemInfo
NILE_GATEWAY_MAP = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'https://{}-nile-activ.nie.netease.com/api/client/%s'
   }
NILE_GATEWAY_MAP_BACKUP = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'http://45.253.197.214/api/client/%s'
   }
NILE_LOG_MAP = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'https://{}-nile-activ.nie.netease.com/api/client/%s'
   }
NILE_GATEWAY_MAP_OVERSEA = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'https://{}-nile-activ.nie.easebar.com/api/client/%s'
   }
NILE_GATEWAY_MAP_BACKUP_OVERSEA = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'http://3.33.144.41/api/client/%s'
   }
NILE_LOG_MAP_OVERSEA = {0: 'https://office-nile-activ.nie.netease.com/api/client/%s',
   1: 'https://test-nile-activ.nie.netease.com/api/client/%s',
   2: 'https://standby-nile-activ.nie.netease.com/api/client/%s',
   3: 'https://{}-nile-activ.nie.easebar.com/api/client/%s'
   }

class NileSettings(object):
    VERSION = 4
    PRODUCT_CODE = 'g93'
    ENV_OFFICE = 0
    ENV_TEST = 1
    ENV_STANDBY = 2
    ENV_PRODUCT = 3
    _isDebug = False
    _isNetDebug = False
    _env = 3
    _isUnderConstruction = False
    _gatewayUrl = ''
    _localSettings = dict()

    def __init__(self):
        pass

    @staticmethod
    def Initialize():
        NileSettings.ReadSettings()

    @staticmethod
    def ReadSettings--- This code section failed: ---

  91       0  SETUP_EXCEPT         94  'to 97'

  92       3  LOAD_GLOBAL           0  'NileFileSystem'
           6  LOAD_ATTR             1  'JoinPath'
           9  LOAD_GLOBAL           2  'NileSystemInfo'
          12  LOAD_ATTR             3  'GetLocalStorageRoot'
          15  CALL_FUNCTION_0       0 
          18  LOAD_CONST            1  'settings'
          21  CALL_FUNCTION_2       2 
          24  STORE_FAST            0  'settingsDir'

  93      27  LOAD_GLOBAL           0  'NileFileSystem'
          30  LOAD_ATTR             1  'JoinPath'
          33  LOAD_ATTR             2  'NileSystemInfo'
          36  CALL_FUNCTION_2       2 
          39  STORE_FAST            1  'filePath'

  94      42  LOAD_GLOBAL           0  'NileFileSystem'
          45  LOAD_ATTR             4  'Exists'
          48  LOAD_FAST             1  'filePath'
          51  CALL_FUNCTION_1       1 
          54  POP_JUMP_IF_FALSE    93  'to 93'

  95      57  LOAD_GLOBAL           0  'NileFileSystem'
          60  LOAD_ATTR             5  'ReadText'
          63  LOAD_FAST             1  'filePath'
          66  CALL_FUNCTION_1       1 
          69  STORE_FAST            2  'content'

  96      72  LOAD_GLOBAL           6  'NileJsonUtil'
          75  LOAD_ATTR             7  'Deserialize'
          78  LOAD_FAST             2  'content'
          81  CALL_FUNCTION_1       1 
          84  LOAD_GLOBAL           8  'NileSettings'
          87  STORE_ATTR            9  '_localSettings'
          90  JUMP_FORWARD          0  'to 93'
        93_0  COME_FROM                '90'
          93  POP_BLOCK        
          94  JUMP_FORWARD         33  'to 130'
        97_0  COME_FROM                '0'

  97      97  DUP_TOP          
          98  LOAD_GLOBAL          10  'Exception'
         101  COMPARE_OP           10  'exception-match'
         104  POP_JUMP_IF_FALSE   129  'to 129'
         107  POP_TOP          
         108  STORE_FAST            3  'e'
         111  POP_TOP          

  98     112  LOAD_GLOBAL          11  'print'
         115  LOAD_CONST            3  '\xe8\xaf\xbb\xe5\x8f\x96\xe6\x9c\xac\xe5\x9c\xb0\xe9\x85\x8d\xe7\xbd\xae\xe5\xa4\xb1\xe8\xb4\xa5, Message: %s'
         118  LOAD_FAST             3  'e'
         121  BINARY_MODULO    
         122  CALL_FUNCTION_1       1 
         125  POP_TOP          
         126  JUMP_FORWARD          1  'to 130'
         129  END_FINALLY      
       130_0  COME_FROM                '129'
       130_1  COME_FROM                '94'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 36

    @staticmethod
    def GetLocalValue--- This code section failed: ---

 107       0  LOAD_GLOBAL           0  'NileSettings'
           3  LOAD_ATTR             1  '_localSettings'
           6  LOAD_ATTR             2  'get'
           9  LOAD_ATTR             1  '_localSettings'
          12  CALL_FUNCTION_2       2 
          15  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

    @staticmethod
    def SetIsUnderConstruction(value):
        NileSettings._isUnderConstruction = value

    @staticmethod
    def GetIsUnderConstruction():
        return NileSettings._isUnderConstruction

    @staticmethod
    def GetIsDebug():
        return NileSettings._isDebug or NileSettings.GetLocalValue('isDebug')

    @staticmethod
    def SetIsDebug(value):
        NileSettings._isDebug = value

    @staticmethod
    def GetIsNetDebug():
        return NileSettings._isNetDebug

    @staticmethod
    def SetIsNetDebug(value):
        NileSettings._isNetDebug = value

    @staticmethod
    def GetGatewayUrl--- This code section failed: ---

 143       0  LOAD_GLOBAL           0  'NileSettings'
           3  LOAD_ATTR             1  '_gatewayUrl'
           6  POP_JUMP_IF_FALSE    16  'to 16'

 144       9  LOAD_GLOBAL           0  'NileSettings'
          12  LOAD_ATTR             1  '_gatewayUrl'
          15  RETURN_END_IF    
        16_0  COME_FROM                '6'

 145      16  LOAD_GLOBAL           2  'NILE_GATEWAY_MAP'
          19  STORE_FAST            1  'gateway'

 146      22  LOAD_GLOBAL           3  'NILE_GATEWAY_MAP_BACKUP'
          25  STORE_FAST            2  'gatewayBackup'

 147      28  LOAD_GLOBAL           0  'NileSettings'
          31  LOAD_ATTR             4  'IsOversea'
          34  CALL_FUNCTION_0       0 
          37  POP_JUMP_IF_FALSE    55  'to 55'

 148      40  LOAD_GLOBAL           5  'NILE_GATEWAY_MAP_OVERSEA'
          43  STORE_FAST            1  'gateway'

 149      46  LOAD_GLOBAL           6  'NILE_GATEWAY_MAP_BACKUP_OVERSEA'
          49  STORE_FAST            2  'gatewayBackup'
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

 150      55  JUMP_FORWARD          1  'to 59'
          58  BINARY_MODULO    
        59_0  COME_FROM                '55'
          59  LOAD_CONST            2  ''
          62  COMPARE_OP            2  '=='
          65  POP_JUMP_IF_FALSE    94  'to 94'

 151      68  LOAD_FAST             1  'gateway'
          71  LOAD_GLOBAL           0  'NileSettings'
          74  LOAD_ATTR             7  '_env'
          77  BINARY_SUBSCR    
          78  LOAD_ATTR             8  'format'
          81  LOAD_GLOBAL           0  'NileSettings'
          84  LOAD_ATTR             9  'GetProductCode'
          87  CALL_FUNCTION_0       0 
          90  CALL_FUNCTION_1       1 
          93  RETURN_END_IF    
        94_0  COME_FROM                '65'

 153      94  LOAD_FAST             2  'gatewayBackup'
          97  LOAD_GLOBAL           0  'NileSettings'
         100  LOAD_ATTR             7  '_env'
         103  BINARY_SUBSCR    
         104  RETURN_VALUE     

Parse error at or near `BINARY_MODULO' instruction at offset 58

    @staticmethod
    def SetGatewayUrl(url):
        NileSettings._gatewayUrl = url

    @staticmethod
    def GetLogUrl():
        logMap = NILE_LOG_MAP
        if NileSettings.IsOversea():
            logMap = NILE_LOG_MAP_OVERSEA
        return logMap[NileSettings._env].format(NileSettings.GetProductCode())

    @staticmethod
    def SetEnvironment(value):
        NileSettings._env = value
        if NileSettings.GetLocalValue('env'):
            env = int(NileSettings.GetLocalValue('env'))
            if NileSettings.ENV_OFFICE <= env <= NileSettings.ENV_PRODUCT:
                NileSettings._env = env

    @staticmethod
    def GetEnvironment():
        return NileSettings._env

    @staticmethod
    def GetEnvironmentDesc():
        if NileSettings._env == NileSettings.ENV_OFFICE:
            return 'OFFICE'
        if NileSettings._env == NileSettings.ENV_TEST:
            return 'TEST'
        if NileSettings._env == NileSettings.ENV_STANDBY:
            return 'STANDBY'
        return 'PRODUCT'

    @staticmethod
    def GetIsTestEnvironment():
        return NileSettings.ENV_OFFICE <= NileSettings._env <= NileSettings.ENV_STANDBY

    @staticmethod
    def GetPlatformDesc():
        if NileSystemInfo.GetOsName() == 'android':
            return 'android'
        if NileSystemInfo.GetOsName() == 'ios':
            return 'ios'
        return 'windows'

    @staticmethod
    def GetSupportTextureFormat():
        from ext_package import ext_package_utils
        if ext_package_utils.is_support_astc():
            return 'astc'
        else:
            return 'etc'

    @staticmethod
    def GetIsAndroid():
        return NileSystemInfo.GetOsName() == 'android'

    @staticmethod
    def GetIsIOS():
        return NileSystemInfo.GetOsName() == 'ios'

    @staticmethod
    def GetIsPC():
        return NileSystemInfo.GetOsName() == 'windows'

    @staticmethod
    def GetSdkVersion():
        prefix = ''
        if NileSettings.GetIsAndroid():
            prefix = NileSettings.PRODUCT_CODE + '-android-'
        elif NileSettings.GetIsIOS():
            prefix = NileSettings.PRODUCT_CODE + '-ios-'
        else:
            prefix = NileSettings.PRODUCT_CODE + '-pc-'
        return prefix + str(NileSettings.VERSION)

    @staticmethod
    def IsOversea():
        from common.platform.dctool import interface
        return interface.is_mainland_package() == False

    @staticmethod
    def GetCountryCode():
        import game3d
        return game3d.get_country_code()

    @staticmethod
    def GetProductCode():
        from common.platform.dctool import interface
        return interface.get_project_id()
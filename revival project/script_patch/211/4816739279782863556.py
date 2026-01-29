# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileRemoteConfig.py
from __future__ import absolute_import
import six_ex
from ..Utils.NileJsonUtil import NileJsonUtil
from .NileLogger import NileLogger
from .NileUtil import NileUtil

class NileRemoteConfig(object):

    def __init__(self, jsonStr, parse=True):
        self.ruleId = 0
        self.remark = ''
        self.totalSwitch = 0
        self.host = ''
        self.port = 0
        self.backupIp = ''
        self.extraParams = dict()
        self.activityConfigList = list()
        self.isDebug = False
        self.isNetLog = False
        self.isError = False
        self.errorMessage = ''
        self.isEmpty = False
        self.isReloading = False
        self.jonsStr = ''
        if parse:
            self._Parse(jsonStr)

    def Reset(self):
        self.ruleId = 0
        self.remark = 'reset'
        self.totalSwitch = 0
        self.host = ''
        self.port = 0
        self.backupIp = ''
        self.extraParams = dict()
        self.activityConfigList = list()
        self.isDebug = False
        self.isNetLog = False
        self.isError = False
        self.errorMessage = ''
        self.isEmpty = False
        self.isReloading = False
        self.jonsStr = ''

    def _Parse(self, response):
        self.jsonStr = response
        try:
            outer = NileJsonUtil.Deserialize(response)
            if not outer:
                NileLogger.Error('RemoteConfig\xe8\xbf\x94\xe5\x9b\x9e\xe6\xa0\xbc\xe5\xbc\x8f\xe9\x94\x99\xe8\xaf\xaf')
                self.isError = True
                return
            if not outer.get('success', False):
                self.errorMessage = 'RemoteConfig\xe8\xbf\x94\xe5\x9b\x9e\xe5\x86\x85\xe5\xae\xb9\xe9\x94\x99\xe8\xaf\xaf: %s' % outer.get('description', 'internal error')
                NileLogger.Error(self.errorMessage)
                self.isError = True
                return
            data = outer.get('data', dict())
            self.ruleId = int(data.get('rule_id', 0))
            if self.ruleId == 0:
                self.errorMessage = '\xe6\xb2\xa1\xe6\x9c\x89\xe5\x8c\xb9\xe9\x85\x8d\xe5\x88\xb0\xe4\xbb\xbb\xe4\xbd\x95\xe8\xa7\x84\xe5\x88\x99'
                NileLogger.Info(self.errorMessage)
                self.isEmpty = True
                return
            self.remark = data.get('rule_remark', 'remark')
            self.totalSwitch = int(data.get('total_switch', 0))
            if self.totalSwitch == 0:
                self.errorMessage = '\xe6\x80\xbb\xe9\x87\x8f\xe5\xbc\x80\xe5\x85\xb3\xe5\x85\xb3\xe9\x97\xad, \xe8\xa7\x84\xe5\x88\x99id: %s remark: %s' % (self.ruleId, self.remark)
                NileLogger.Info(self.errorMessage)
                self.isEmpty = True
                return
            self.isDebug = int(data.get('is_debug', 0)) == 1
            self.isNetLog = int(data.get('is_net_log', 0)) == 1
            self.host = data.get('host', '')
            if not self.host:
                self.errorMessage = '\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x9f\x9f\xe5\x90\x8d\xe6\xb2\xa1\xe6\x9c\x89\xe9\x85\x8d\xe7\xbd\xae, id: %s remark: %s' % (self.ruleId, self.remark)
                NileLogger.Info(self.errorMessage)
                self.isError = True
                return
            self.backupIp = data.get('backup_ip', '')
            self.port = int(data.get('port', 0))
            self.extraParams = NileJsonUtil.Deserialize(data.get('ext_param_json', '{}') or '{}')
            self.activityConfigList = self._ParseResourceList(data.get('activity_resource_list', list()))
            if not self.activityConfigList:
                self.errorMessage = '\xe8\xa7\x84\xe5\x88\x99\xe4\xb8\xad\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x95\xb0\xe9\x87\x8f\xe4\xb8\xba0, \xe8\xa7\x84\xe5\x88\x99id: %s remark: %s' % (self.ruleId, self.remark)
                NileLogger.Info(self.errorMessage)
                self.isEmpty = True
        except BaseException as e:
            self.errorMessage = 'RemoteConfig \xe8\xa7\xa3\xe6\x9e\x90\xe5\xa4\xb1\xe8\xb4\xa5, message: %s, trace: %s' % (str(e), NileUtil.GetTraceback())
            NileLogger.Error(self.errorMessage)
            self.isError = True

    def _ParseResourceList(self, rawSourceList):
        result = list()
        for activity in rawSourceList:
            result.append(NileActivityConfig(activity))

        return result

    def GetActivityConfigByName(self, name):
        for config in self.activityConfigList:
            if config.name == name:
                return config

        return NileActivityConfig.GetDefault()

    def HasActivityConfig(self, marketId):
        for config in self.activityConfigList:
            if config.marketId == marketId:
                return True

        return False

    def GetActivityConfigByMarketId(self, marketId):
        for config in self.activityConfigList:
            if config.marketId == marketId:
                return config

        return NileActivityConfig.GetDefault()

    def GetExtraParam(self, key):
        return self.extraParams.get(key, 0)


class NileActivityConfig(object):
    _default = None

    def __init__(self, config):
        self.name = config['activity_name']
        self.marketId = int(config['market_id'])
        self.patchVersion = config.get('patch_version', '0.0.0')
        urlDict = self.ExtractResourceUrlDict(config)
        self.urlList = list(six_ex.values(urlDict))

    def ExtractResourceUrlDict(self, resourceConfig):
        result = dict()
        for urlConfig in resourceConfig['resource_list']:
            resourceUrl = urlConfig['resource_url']
            if NileActivityConfig.IsSupportPy3():
                if resourceUrl.endswith('.py3'):
                    name = self.ExtractName(resourceUrl)
                    result[name] = resourceUrl
            elif resourceUrl.endswith('.nile'):
                name = self.ExtractName(resourceUrl)
                result[name] = resourceUrl

        return result

    def ExtractName(self, url):
        return url.split('_')[1]

    @staticmethod
    def GetDefault--- This code section failed: ---

 163       0  LOAD_GLOBAL           0  'NileActivityConfig'
           3  LOAD_ATTR             1  '_default'
           6  POP_JUMP_IF_TRUE     67  'to 67'

 164       9  LOAD_GLOBAL           2  'dict'
          12  CALL_FUNCTION_0       0 
          15  STORE_FAST            0  'config'

 165      18  LOAD_CONST            1  'default'
          21  LOAD_CONST            2  'activity_name'
          24  STORE_SUBSCR     

 166      25  LOAD_CONST            3  ''
          28  LOAD_CONST            4  'market_id'
          31  STORE_SUBSCR     

 167      32  LOAD_CONST            5  '0.0.0'
          35  LOAD_CONST            6  'patch_version'
          38  STORE_SUBSCR     

 168      39  LOAD_GLOBAL           3  'list'
          42  CALL_FUNCTION_0       0 
          45  CALL_FUNCTION_7       7 
          48  STORE_SUBSCR     

 169      49  LOAD_GLOBAL           0  'NileActivityConfig'
          52  LOAD_FAST             0  'config'
          55  CALL_FUNCTION_1       1 
          58  LOAD_GLOBAL           0  'NileActivityConfig'
          61  STORE_ATTR            1  '_default'
          64  JUMP_FORWARD          0  'to 67'
        67_0  COME_FROM                '64'

 170      67  LOAD_GLOBAL           0  'NileActivityConfig'
          70  LOAD_ATTR             1  '_default'
          73  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_SUBSCR' instruction at offset 24

    @staticmethod
    def IsSupportNpk():
        from ..Utils.NileSystemInfo import NileSystemInfo
        return NileSystemInfo.IsSupportNpk()

    @staticmethod
    def IsSupportPy3():
        import six
        return six.PY3
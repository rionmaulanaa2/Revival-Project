# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileUserData.py
from __future__ import absolute_import
from ..Utils.NileSystemInfo import NileSystemInfo
from .NileSettings import NileSettings
from .NileLogger import NileLogger

class NileUserData(object):

    def __init__(self, dataDict):
        from logic.gcommon.common_utils.local_text import get_cur_lang_name
        self.game = ''
        self.server = ''
        self.appVer = ''
        self.appChannel = ''
        self.accountId = ''
        self.aid = ''
        self.roleId = ''
        self.roleName = ''
        self.roleLevel = 0
        self.loginTime = ''
        self.token = ''
        self.serverVersion = ''
        self._ParseDataDict(dataDict)
        self.sdkVersion = NileSettings.GetSdkVersion()
        self.network = NileSystemInfo.GetNetworkStatus()
        self.osName = NileSystemInfo.GetOsName()
        self.osVer = NileSystemInfo.GetOsVersion()
        self.engineVer = NileSystemInfo.GetEngineVersion()
        self.macAddr = NileSystemInfo.GetMacAddress()
        self.deviceModel = NileSystemInfo.GetDeviceInfo()
        self.platform = NileSettings.GetPlatformDesc()
        self.textureFormat = NileSettings.GetSupportTextureFormat()
        self.countryCode = NileSettings.GetCountryCode() or 'CN'
        self.language = get_cur_lang_name()

    def Reset(self):
        self.accountId = ''
        self.aid = ''
        self.roleId = ''
        self.roleName = ''
        self.roleLevel = 0
        self.loginTime = ''
        self.token = 'reset'
        self.serverVersion = ''

    def Update(self, dataDict):
        self._ParseDataDict(dataDict)

    def _ParseDataDict(self, dataDict):
        self.game = dataDict.get('game', '') or self.game
        self.server = dataDict.get('server', '') or self.server
        self.appVer = dataDict.get('app_ver', '') or self.appVer
        self.appChannel = dataDict.get('app_channel', '') or self.appChannel
        self.accountId = dataDict.get('account_id', '') or self.accountId
        self.aid = dataDict.get('aid', '') or self.aid
        self.roleId = dataDict.get('role_id', '') or self.roleId
        self.roleName = dataDict.get('role_name', '') or self.roleName
        self.roleLevel = dataDict.get('role_level', 0) or self.roleLevel
        self.loginTime = dataDict.get('login_time', '') or self.loginTime
        self.token = dataDict.get('token', '') or self.token
        self.serverVersion = dataDict.get('server_version', '') or self.serverVersion
        if not self.appVer:
            self.appVer = '0.0.0'
        if not self.appChannel:
            self.appChannel = 'dev'

    def IsValidate(self):
        if self.VerifyField('game') & self.VerifyField('server') & self.VerifyField('roleId') & self.VerifyField('token'):
            return True
        return False

    def VerifyField(self, fieldName):
        if not self[fieldName]:
            NileLogger.Error('UserData\xe4\xb8\xad %s \xe5\xad\x97\xe6\xae\xb5\xe4\xb8\xba\xe7\xa9\xba\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\xb8\xb8\xe6\x88\x8f\xe5\x92\x8c\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe7\x9a\x84\xe5\xaf\xb9\xe6\x8e\xa5\xe4\xbb\xa3\xe7\xa0\x81' % fieldName)
            return False
        return True

    def GenerateFieldFragment(self, fieldName):
        return '%s=%s&' % (fieldName, self[fieldName])

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        l = list()
        l.append(self.GenerateFieldFragment('game'))
        l.append(self.GenerateFieldFragment('server'))
        l.append(self.GenerateFieldFragment('appVer'))
        l.append(self.GenerateFieldFragment('appChannel'))
        l.append(self.GenerateFieldFragment('sdkVersion'))
        l.append(self.GenerateFieldFragment('accountId'))
        l.append(self.GenerateFieldFragment('aid'))
        l.append(self.GenerateFieldFragment('roleId'))
        l.append(self.GenerateFieldFragment('roleName'))
        l.append(self.GenerateFieldFragment('roleLevel'))
        l.append(self.GenerateFieldFragment('loginTime'))
        l.append(self.GenerateFieldFragment('token'))
        l.append(self.GenerateFieldFragment('network'))
        l.append(self.GenerateFieldFragment('osName'))
        l.append(self.GenerateFieldFragment('osVer'))
        l.append(self.GenerateFieldFragment('engineVer'))
        l.append(self.GenerateFieldFragment('macAddr'))
        l.append(self.GenerateFieldFragment('deviceModel'))
        l.append(self.GenerateFieldFragment('platform'))
        return '' + ''.join(l)
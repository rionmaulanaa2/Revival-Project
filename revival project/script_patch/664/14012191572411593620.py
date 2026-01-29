# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileActivityDataHttpLoader.py
from .NileHttpLoader import NileHttpLoader
from .NileLogger import NileLogger

class NileActivityDataHttpLoader(NileHttpLoader):

    def __init__(self, activityName, api, bodyParams):
        self._activityName = activityName
        self._api = api
        self._bodyParams = bodyParams or dict()
        super(NileActivityDataHttpLoader, self).__init__(retryCount=3, retryDelayInSecond=3, timeoutInSecond=5)

    def GetUrl(self):
        from .NileService import NileService
        remoteConfig = NileService.GetInstance().GetRemoteConfig()
        if self._retryIndex % 2 == 0:
            if remoteConfig.host.find('http') >= 0:
                return self._GenerateUrl('', remoteConfig.host, remoteConfig.port)
            if remoteConfig.port == 443:
                return self._GenerateUrl('https://', remoteConfig.host, remoteConfig.port)
            return self._GenerateUrl('http://', remoteConfig.host, remoteConfig.port)
        else:
            if remoteConfig.backupIp.find('http') >= 0:
                return self._GenerateUrl('', remoteConfig.backupIp, 80)
            return self._GenerateUrl('http://', remoteConfig.backupIp, 80)

    def _GenerateUrl(self, protocol, base, port):
        return '%s%s:%s/api/client/%s' % (protocol, base, port, self._api)

    def GetPostBodyParam(self):
        from .NileService import NileService
        userData = NileService.GetInstance().GetUserData()
        self._bodyParams['game'] = userData.game
        self._bodyParams['server'] = userData.server
        self._bodyParams['role_id'] = userData.roleId
        return self._bodyParams

    def GeneratePostHeader(self):
        header = super(NileActivityDataHttpLoader, self).GeneratePostHeader()
        from .NileService import NileService
        remoteConfig = NileService.GetInstance().GetRemoteConfig()
        activityConfig = remoteConfig.GetActivityConfigByName(self._activityName)
        header.update({'Nile-Client-PatchVersion': str(activityConfig.patchVersion)})
        return header

    def DigestReply(self, reply):
        self._replyBody = reply.body

    def GetReplyBody(self):
        self._replyBody = self._replyBody or '{"code":0, "success":false, "data":{}}'
        NileLogger.Info('\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x8e\xa5\xe5\x8f\xa3\xe8\xbf\x94\xe5\x9b\x9e\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x9a%s' % self.GetUrl())
        NileLogger.Info(self._replyBody)
        return self._replyBody
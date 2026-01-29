# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileRuleHttpLoader.py
from .NileHttpLoader import NileHttpLoader
from .NileSettings import NileSettings
from .NileRemoteConfig import NileRemoteConfig

class NileRuleHttpLoader(NileHttpLoader):

    def __init__(self):
        super(NileRuleHttpLoader, self).__init__(retryCount=6, retryDelayInSecond=5, timeoutInSecond=20)

    def GetUrl(self):
        return NileSettings.GetGatewayUrl(self._retryIndex) % 'patch_list'

    def GetPostBodyParam(self):
        from .NileService import NileService
        userData = NileService.GetInstance().GetUserData()
        return {'game': userData.game,
           'server': userData.server,
           'role_id': userData.roleId
           }

    def DigestReply(self, reply):
        if reply.body is None:
            self._replyBody = None
            return
        else:
            remoteConfig = NileRemoteConfig(reply.body)
            if remoteConfig.isError:
                self._replyBody = None
                return
            self._replyBody = remoteConfig
            return

    def GetReplyBody(self):
        return self._replyBody or NileRemoteConfig('{"code":0, "success":false, "data":{}}')
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileLogDataHttpLoader.py
from .NileHttpLoader import NileHttpLoader
from .NileSettings import NileSettings
from ..Utils.NileJsonUtil import NileJsonUtil

class NileLogDataHttpLoader(NileHttpLoader):
    logNo = 0

    def __init__(self, api):
        super(NileLogDataHttpLoader, self).__init__(0, 3, 3)
        self._api = api
        self._bodyParams = dict()
        self._catchCallbackError = False

    def GetUrl(self):
        return NileSettings.GetLogUrl() % self._api

    def GetPostBodyParam(self):
        from .NileService import NileService
        userData = NileService.GetInstance().GetUserData()
        self._bodyParams['game'] = userData.game
        self._bodyParams['server'] = userData.server
        self._bodyParams['role_id'] = userData.roleId
        return self._bodyParams

    def Report(self, category, detail, callback, *args, **kwargs):
        NileLogDataHttpLoader.logNo += 1
        self._FillBodyParamObj(category, detail)
        self.SendPostRequest(self.GetUrl(), callback, *args, **kwargs)

    def _FillBodyParamObj(self, category, detail):
        from .NileService import NileService
        userData = NileService.GetInstance().GetUserData()
        logJsonObj = dict()
        logJsonObj['game'] = str(userData.game)
        logJsonObj['server'] = str(userData.server)
        logJsonObj['role_id'] = str(userData.roleId)
        logJsonObj['log_no'] = str(NileLogDataHttpLoader.logNo)
        logJsonObj['category'] = str(category)
        logJsonObj['content'] = str(detail)
        self._bodyParams['keyword'] = 'base'
        self._bodyParams['log_json'] = NileJsonUtil.Serialize(logJsonObj) or '{}'

    def DigestReply(self, reply):
        self._replyBody = reply.body or '{"code":0, "success":false, "data":{}}'

    def LogRequest(self, method):
        pass
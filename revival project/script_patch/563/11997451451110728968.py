# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileHttpLoader.py
from ..Utils.NileTimer import NileTimer
from ..Utils.NileHttpClient import NileHttpRequest
from ..Utils.NileCallbackWeakRef import NileCallbackWeakRef
from ..Utils.NileJsonUtil import NileJsonUtil
from .NileHttpClientWorker import NileHttpClientWorker
from .NileUtil import NileUtil
from .NileLogger import NileLogger
from .NileHttpLoaderHelper import NileHttpLoaderHelper

class NileHttpLoader(object):

    def __init__(self, retryCount=3, retryDelayInSecond=5, timeoutInSecond=5):
        self._retryIndex = 0
        self._retryCount = retryCount
        self._retryDelayInSecond = retryDelayInSecond
        self._timeoutInSecond = timeoutInSecond
        self._timeoutId = 0
        self._callback = None
        self._url = ''
        self._requestHeader = None
        self._requestBody = ''
        self._replyBody = None
        self._catchCallbackError = True
        self._sdkSerialNumber = self._GetSdkSerialNumber()
        return

    def SetRetryCount(self, value):
        self._retryCount = value

    def SetRetryDelay(self, value):
        self._retryDelayInSecond = value

    def SetCatchCallbackError(self, value):
        self._catchCallbackError = value

    def SetTimeoutInSecond(self, value):
        self._timeoutInSecond = value

    def SetRequestHeader(self, value):
        self._requestHeader = value

    def SetRequestBody(self, value):
        self._requestBody = value

    def SendPostRequest(self, url, callback, *args, **kwargs):
        self._url = url
        self._callback = self._CreateCallback(callback, *args, **kwargs)
        self.LogRequest('Post')
        self._InternalSendPostRequest()

    def _InternalSendPostRequest(self):
        try:
            NileHttpClientWorker.GetInstance().Request(self.GeneratePostRequest(), self._timeoutInSecond, self.OnPostResponse)
        except BaseException as e:
            NileLogger.Error('\xe6\x9e\x84\xe5\xbb\xba\xe8\xaf\xb7\xe6\xb1\x82\xe5\xa4\xb1\xe8\xb4\xa5, url: %s message: %s' % (self._url, str(e)))

    def OnPostResponse(self, request, reply):
        self._OnResponse(request, reply, self._InternalSendPostRequest)

    def GeneratePostRequest(self):
        url = self.GetUrl()
        result = NileUtil.ParseUrl(url)
        useSsl, port = self.GetSslAndPortConfig(result)
        self._requestHeader = self._requestHeader or self.GeneratePostHeader()
        self._requestBody = self._requestBody or self.GeneratePostBody()
        return NileHttpRequest(url, port, 'POST', self._requestHeader, self._requestBody)

    def GeneratePostHeader(self):
        return NileHttpLoaderHelper.GeneratePostHeader(self.GetPostBodyParam())

    def GeneratePostBody(self):
        import six
        return six.ensure_binary(NileJsonUtil.Serialize(self.GetPostBodyParam()), encoding='utf-8')

    def GetPostBodyParam(self):
        return dict()

    def SendGetRequest(self, url, callback, *args, **kwargs):
        self._url = url
        self._callback = self._CreateCallback(callback, *args, **kwargs)
        self.LogRequest('Get')
        self._InternalSendGetRequest()

    def _InternalSendGetRequest(self):
        try:
            NileHttpClientWorker.GetInstance().Request(self.GenerateGetRequest(), self._timeoutInSecond, self.OnGetResponse)
        except BaseException as e:
            NileLogger.Error('\xe6\x9e\x84\xe5\xbb\xba\xe8\xaf\xb7\xe6\xb1\x82\xe5\xa4\xb1\xe8\xb4\xa5, url: %s message: %s, trace: %s' % (self._url, str(e), NileUtil.GetTraceback()))

    def OnGetResponse(self, request, reply):
        self._OnResponse(request, reply, self._InternalSendGetRequest)

    def GenerateGetRequest(self):
        url = self.GetUrl()
        result = NileUtil.ParseUrl(url)
        useSsl, port = self.GetSslAndPortConfig(result)
        self._requestHeader = self._requestHeader or self.GenerateGetHeader()
        self._requestBody = self._requestBody or self.GenerateGetBody()
        return NileHttpRequest(url, port, 'GET', self._requestHeader, self._requestBody)

    def GenerateGetHeader(self):
        return {'Connection': 'close'}

    def GenerateGetBody(self):
        return ''

    def _CreateCallback(self, callback, *args, **kwargs):
        if self._catchCallbackError:
            return NileCallbackWeakRef(callback, *args, **kwargs).Execute
        return NileCallbackWeakRef(callback, *args, **kwargs).ExecuteUnsafe

    def _GetSdkSerialNumber(self):
        from .NileService import NileService
        return NileService.GetInstance().GetSerialNumber()

    def _OnResponse(self, request, reply, retryFunc):
        if not self._IsValidState():
            return
        else:
            if not self._IsValidSerialNumber():
                return
            if not self._IsValidCallback():
                return
            self.DigestReply(reply)
            if self._replyBody is None and self._retryIndex < self._retryCount:
                self._retryIndex += 1
                self._timeoutId = NileTimer.SetTimeoutUnsafe(retryFunc, self._retryDelayInSecond * 1000)
                return
            self.HandleReplyError(reply)
            self._callback(self.GetReplyBody())
            self._callback = None
            return

    def _IsValidState(self):
        from .NileService import NileService
        if NileService.GetInstance().GetState() != NileService.STATE_START:
            NileLogger.Info('\xe5\xbd\x93\xe5\x89\x8dSDK\xe4\xb8\x8d\xe5\xa4\x84\xe4\xba\x8e\xe8\xbf\x90\xe8\xa1\x8c\xe7\x8a\xb6\xe6\x80\x81, Url: %s' % self.GetUrl())
            return False
        return True

    def _IsValidSerialNumber(self):
        from .NileService import NileService
        if self._sdkSerialNumber != NileService.GetInstance().GetSerialNumber():
            NileLogger.Info('\xe8\xaf\xa5\xe8\xaf\xb7\xe6\xb1\x82\xe7\x9a\x84SN\xe5\x92\x8cSDK\xe6\x9c\x80\xe6\x96\xb0SN\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4, Url: %s' % self.GetUrl())
            return False
        return True

    def _IsValidCallback(self):
        if not self._callback.__self__.IsValid():
            NileLogger.Info('\xe5\x9b\x9e\xe8\xb0\x83\xe5\x87\xbd\xe6\x95\xb0\xe5\xb7\xb2\xe4\xb8\x8d\xe5\x8f\xaf\xe7\x94\xa8, Url: %s' % self.GetUrl())
            return False
        return True

    def GetUrl(self):
        return self._url

    def HandleReplyError(self, reply):
        if reply.error != 0:
            NileLogger.Error('\xe8\xaf\xb7\xe6\xb1\x82%s\xe5\x8f\x91\xe7\x94\x9f\xe9\x94\x99\xe8\xaf\xaf: %s' % (self._url, reply.reason))

    def DigestReply(self, reply):
        self._replyBody = reply.body

    def GetReplyBody(self):
        return self._replyBody

    def GetSslAndPortConfig(self, urlParseResult):
        if urlParseResult.scheme == 'https':
            return (True, 443)
        return (False, urlParseResult.port or 80)

    def Abort(self):
        if not self._timeoutId:
            NileTimer.ClearTimeout(self._timeoutId)

    def LogRequest(self, method):
        NileLogger.Info('\xe5\x8f\x91\xe9\x80\x81%s\xe8\xaf\xb7\xe6\xb1\x82: url: %s body: %s' % (method, self._url, self.GeneratePostBody()))
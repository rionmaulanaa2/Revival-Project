# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NilePatchHttpLoader.py
from __future__ import absolute_import
import time
from .NileSettings import NileSettings
from .NileHttpLoader import NileHttpLoader
from .NileLogger import NileLogger
from .NilePatchExtractor import NilePatchExtractor
from .NilePatchModuleHelper import NilePatchModuleHelper
from .NileLogReporter import NileLogReporter

class NilePatchHttpLoader(NileHttpLoader):

    def __init__(self):
        super(NilePatchHttpLoader, self).__init__(retryCount=5, retryDelayInSecond=5, timeoutInSecond=60)

    def SendGetRequest(self, url, callback, *args, **kwargs):
        if NileSettings.GetIsUnderConstruction():
            super(NilePatchHttpLoader, self).SendGetRequest(url, callback, *args, **kwargs)
            return
        else:
            if NilePatchExtractor.IsPatchExists(url):
                NileLogger.Info('Patch\xe5\x9c\xa8\xe6\x9c\xac\xe5\x9c\xb0\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8, url: %s' % url)
                self._callback = self._CreateCallback(callback, *args, **kwargs)
                self._replyBody = (True, url)
                self._callback(self.GetReplyBody())
                self._callback = None
            else:
                super(NilePatchHttpLoader, self).SendGetRequest(url, callback, *args, **kwargs)
            return

    def DigestReply(self, reply):
        if reply.body is None:
            self._replyBody = None
            return
        else:
            if NileSettings.GetIsUnderConstruction():
                self._replyBody = (
                 True, self._url)
                return
            start = time.time() * 1000
            result = NilePatchExtractor.Extract(self._url, reply.body)
            if result != '':
                self._ChangeReply(reply, -1, result)
                self._replyBody = None
                return
            if not NilePatchExtractor.IsPatchExists(self._url):
                self._ChangeReply(reply, -2, '\xe6\x9c\xac\xe5\x9c\xb0Md5\xe6\xa0\xa1\xe9\xaa\x8c\xe8\xbf\x87\xe7\xa8\x8b\xe5\x87\xba\xe9\x94\x99')
                self._replyBody = None
                return
            self._replyBody = (True, self._url)
            NileLogger.Info('Patch\xe6\x8f\x90\xe5\x8f\x96\xe3\x80\x81\xe6\xa0\xa1\xe9\xaa\x8c\xe8\x80\x97\xe6\x97\xb6: %s' % (time.time() * 1000 - start))
            return

    def _ChangeReply(self, reply, error, reason):
        reply.body = None
        reply.status = 0
        reply.error = error
        reply.reason = reason
        return

    def HandleReplyError(self, reply):
        super(NilePatchHttpLoader, self).HandleReplyError(reply)
        if reply.error != 0:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_PATCH, 'Patch\xe5\x8a\xa0\xe8\xbd\xbd\xe5\xa4\xb1\xe8\xb4\xa5, Url: %s, Description: %s' % (self._url, reply.reason))

    def GetReplyBody(self):
        return self._replyBody or (False, self._url)
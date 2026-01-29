# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileFileHttpLoader.py
from .NileHttpLoader import NileHttpLoader
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper
from .NileLogger import NileLogger
from ..Utils.NileBase64Util import NileBase64Util
from ..Utils.NileFileSystem import NileFileSystem

class NileFileHttpLoader(NileHttpLoader):

    def __init__(self):
        super(NileFileHttpLoader, self).__init__(retryCount=3, retryDelayInSecond=3, timeoutInSecond=10)

    def SendGetRequest(self, url, callback, *args, **kwargs):
        filePath = self.GetTargetPathByUrl(url)
        if NileFileSystem.Exists(filePath):
            NileLogger.Info('\xe8\xb5\x84\xe6\xba\x90\xe5\x9c\xa8\xe6\x9c\xac\xe5\x9c\xb0\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8, url: %s, filePath: %s' % (url, filePath))
            self._callback = self._CreateCallback(callback, *args, **kwargs)
            self._replyBody = filePath
            self._callback(self._replyBody)
            self._callback = None
        else:
            super(NileFileHttpLoader, self).SendGetRequest(url, callback, *args, **kwargs)
        return

    def DigestReply(self, reply):
        if reply.body is None:
            self._replyBody = None
            return
        else:
            filePath = self.GetTargetPathByUrl(self._url)
            NileFileSystem.WriteBytes(filePath, reply.body)
            if not NileFileSystem.Exists(filePath):
                self._ChangeReply(reply, -1, '\xe5\xb0\x86\xe6\x96\x87\xe4\xbb\xb6\xe4\xbf\x9d\xe5\xad\x98\xe5\x88\xb0\xe6\x9c\xac\xe5\x9c\xb0\xe5\xa4\xb1\xe8\xb4\xa5')
                self._replyBody = None
                return
            self._replyBody = filePath
            return

    def GetTargetPathByUrl(self, url):
        name = NileBase64Util.Encode(url)
        postfix = NileFileSystem.GetFilePostfix(url)
        return NileLocalDirectoryHelper.GetAssetFilePath(name + postfix)

    def _ChangeReply(self, reply, error, reason):
        reply.body = None
        reply.status = 0
        reply.error = error
        reply.reason = reason
        return
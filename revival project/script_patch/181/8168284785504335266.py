# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileLogger.py
import time
import logging
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper
from .NileSettings import NileSettings
from ..Utils.NileFileSystem import NileFileSystem

class NileLogger(object):
    __knocker = None
    __level = logging.DEBUG
    __logPath = None
    __hookList = list()
    __wisperer = None

    @staticmethod
    def Initialize():
        NileLogger.__knocker = logging.getLogger('Nile')
        fileName = 'log_%s.txt' % time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        NileLogger.__logPath = NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetLogDirectoryPath(), fileName)

    @staticmethod
    def Reload():
        try:
            NileLogger.__knocker.handlers = list()
            NileLogger.__knocker.setLevel(NileLogger.__level)
            formatter = logging.Formatter(fmt='[Nile][%(asctime)s][%(levelname)-7.7s] %(message)s')
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            NileLogger.__knocker.addHandler(consoleHandler)
            if NileLogger.IsEnabled():
                fileHandler = logging.FileHandler(NileFileSystem.IndicateUTF8(NileLogger.__logPath), encoding='utf-8')
                fileHandler.setFormatter(formatter)
                NileLogger.__knocker.addHandler(fileHandler)
            if NileLogger.IsNetLogEnabled():
                NileLogger.__wisperer = NileWisperer()
        except Exception as e:
            print 'NileLogger reload error: ' + repr(e)

    @staticmethod
    def AddHook(hook):
        if NileLogger.__hookList.count(hook) == 0:
            NileLogger.__hookList.append(hook)

    @staticmethod
    def RemoveHook(hook):
        if NileLogger.__hookList.count(hook) > 0:
            NileLogger.__hookList.remove(hook)

    @staticmethod
    def _LogHook(message):
        for h in NileLogger.__hookList:
            h(message)

    @staticmethod
    def IsEnabled():
        if NileSettings.GetIsUnderConstruction():
            return True
        if NileSettings.GetEnvironment() < NileSettings.ENV_PRODUCT:
            return True
        return NileSettings.GetIsDebug()

    @staticmethod
    def IsNetLogEnabled():
        from .NileService import NileService
        remoteConfig = NileService.GetInstance().GetRemoteConfig()
        if remoteConfig and remoteConfig.isNetLog:
            return True
        return False

    @staticmethod
    def SetLevel(level):
        NileLogger.__level = level
        NileLogger.__knocker.setLevel(level)

    @staticmethod
    def Debug(message, start=2, depth=3):
        if NileLogger.__knocker and len(NileLogger.__knocker.handlers) > 0:
            NileLogger.__knocker.debug(message)
        else:
            print message
        NileLogger._LogHook(message)
        NileLogger.Report(message)

    @staticmethod
    def Info(message, start=2, depth=3):
        if NileLogger.__knocker and len(NileLogger.__knocker.handlers) > 0:
            NileLogger.__knocker.info(message)
        else:
            print message
        NileLogger._LogHook(message)
        NileLogger.Report(message)

    @staticmethod
    def Warning(message, start=2, depth=3):
        if NileLogger.__knocker and len(NileLogger.__knocker.handlers) > 0:
            NileLogger.__knocker.warning(message)
        else:
            print message
        NileLogger._LogHook(message)
        NileLogger.Report(message)

    @staticmethod
    def Error(message, start=2, depth=3):
        if NileLogger.__knocker and len(NileLogger.__knocker.handlers) > 0:
            NileLogger.__knocker.error(message)
        else:
            print message
        NileLogger._LogHook(message)
        NileLogger.Report(message)

    @staticmethod
    def Report(message):
        if NileLogger.__wisperer:
            NileLogger.__wisperer.Send(message)


class NileWisperer:

    def Send(self, content):
        from .NileHttpClientWorker import NileHttpClientWorker
        NileHttpClientWorker.GetInstance().Request(self.GeneratePostRequest(content), 3, self.OnPostResponse)

    def GeneratePostRequest(self, content):
        from .NileSettings import NileSettings
        from .NileUtil import NileUtil
        from ..Utils.NileHttpClient import NileHttpRequest
        url = NileSettings.GetLogUrl() % 'realtime_sdk_log'
        result = NileUtil.ParseUrl(url)
        useSsl, port = self.GetSslAndPortConfig(result)
        bodyParams = self.GetPostBodyParam(content)
        header = self.GeneratePostHeader(bodyParams)
        body = self.GeneratePostBody(bodyParams)
        return NileHttpRequest(url, port, 'POST', header, body)

    def GetSslAndPortConfig(self, urlParseResult):
        if urlParseResult.scheme == 'https':
            return (True, 443)
        return (False, urlParseResult.port or 80)

    def GeneratePostHeader(self, bodyParams):
        from .NileHttpLoaderHelper import NileHttpLoaderHelper
        return NileHttpLoaderHelper.GeneratePostHeader(bodyParams)

    def GeneratePostBody(self, bodyParams):
        from ..Utils.NileJsonUtil import NileJsonUtil
        import six
        return six.ensure_binary(NileJsonUtil.Serialize(bodyParams), encoding='utf-8')

    def GetPostBodyParam(self, content):
        import time
        from .NileService import NileService
        from ..Utils.NileJsonUtil import NileJsonUtil
        userData = NileService.GetInstance().GetUserData()
        logJsonObj = dict()
        logJsonObj['game'] = str(userData.game)
        logJsonObj['server'] = str(userData.server)
        logJsonObj['role_id'] = str(userData.roleId)
        logJsonObj['category'] = 'realtime_sdk_log'
        logJsonObj['content'] = str(content)
        milliseconds = int(round(time.time() * 1000))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S.{}', time.localtime()).format(milliseconds % 1000)
        logJsonObj['sdk_t_when'] = timestamp
        bodyParams = dict()
        bodyParams['game'] = userData.game
        bodyParams['server'] = userData.server
        bodyParams['role_id'] = userData.roleId
        bodyParams['keyword'] = 'realtime_base'
        bodyParams['log_json'] = NileJsonUtil.Serialize(logJsonObj) or '{}'
        return bodyParams

    def OnPostResponse(self, request, reply):
        pass
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileLogReporter.py
from ..Utils.NileJsonUtil import NileJsonUtil
from .NileLogger import NileLogger
from .NileLogDataHttpLoader import NileLogDataHttpLoader

class NileLogReporter(object):
    _instance = None
    _isInited = False
    STATUS_EXECUTE_ENTRY = 'status_execute_entry'
    STATUS_LOAD_REMOTE_CONFIG = 'status_load_remote_config'
    STATUS_RELOAD_REMOTE_CONFIG = 'status_reload_remote_config'
    STATUS_EMPTY_REMOTE_CONFIG = 'status_empty_remote_config'
    STATUS_LOAD_ACTIVITY = 'status_load_activity'
    STATUS_GOT_RULE = 'status_got_rule'
    STATUS_LOGOUT = 'status_logout'
    ERROR_PATCH_EXIST_CHECK = 'error_patch_exist_check'
    ERROR_PATCH_UNZIP = 'error_patch_unzip'
    ERROR_REMOTE_CONFIG = 'error_remote_config'
    ERROR_TIMER = 'error_timer'
    ERROR_EVENT = 'error_event'
    ERROR_CALLBACK = 'error_callback'
    ERROR_PATCH = 'error_patch'
    ERROR_GAME_TO_NILE = 'error_message_game_to_nile'
    ERROR_NILE_TO_GAME = 'error_message_nile_to_game'
    ERROR_GAME_DELEGATE = 'error_game_delegate'
    ERROR_ENTRY = 'error_entry'
    ERROR_MISC = 'error_misc'

    @staticmethod
    def GetInstance():
        if not NileLogReporter._instance:
            NileLogReporter._instance = NileLogReporter()
        return NileLogReporter._instance

    def _Report(self, category, detail):
        logLoader = NileLogDataHttpLoader('sdk_log')
        logLoader.Report(category, detail, self._OnSendReport)

    def ReportStatus(self, category, detail=''):
        NileLogger.Info(detail)
        self._Report(category, detail)

    def ReportTimerError(self, detail):
        NileLogger.Error(detail)
        self._Report(NileLogReporter.ERROR_TIMER, detail)

    def ReportCallbackError(self, detail):
        NileLogger.Error(detail)
        self._Report(NileLogReporter.ERROR_CALLBACK, detail)

    def ReportEventError(self, detail):
        NileLogger.Error(detail)
        self._Report(NileLogReporter.ERROR_EVENT, detail)

    def ReportError(self, category, detail=''):
        NileLogger.Error(detail)
        self._Report(category, detail)

    def _OnSendReport(self, replyBody):
        result = NileJsonUtil.Deserialize(replyBody)
        if not result.get('success', False):
            NileLogger.Error('\xe6\x97\xa5\xe5\xbf\x97\xe4\xb8\x8a\xe6\x8a\xa5\xe5\xa4\xb1\xe8\xb4\xa5, ReplyBody: %s' % replyBody)
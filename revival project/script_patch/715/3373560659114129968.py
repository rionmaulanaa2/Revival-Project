# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileService.py
from __future__ import absolute_import
from __future__ import print_function
from ..Utils.NileSystemInfo import NileSystemInfo
from ..Utils.NileTimer import NileTimer
from ..Utils.NileCallbackWeakRef import NileCallbackWeakRef
from .NileSettings import NileSettings
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper
from .NileLogger import NileLogger
from .NileServiceDelegateHub import NileServiceDelegateHub
from .NileServiceMessageHub import NileServiceMessageHub
from .NileServiceNetworkHub import NileServiceNetworkHub
from .NileServicePanelHub import NileServicePanelHub
from .NileServiceRedDotHub import NileServiceRedDotHub
from .NileUserData import NileUserData
from .NilePatchLoader import NilePatchLoader
from .NilePatchModuleHelper import NilePatchModuleHelper
from .NileRuleHttpLoader import NileRuleHttpLoader
from .NileLogReporter import NileLogReporter

class NileService(NileServiceDelegateHub, NileServiceMessageHub, NileServiceNetworkHub, NileServicePanelHub, NileServiceRedDotHub):
    SN = 0
    STATE_PRE_INIT = 0
    STATE_INIT = 1
    STATE_START = 2
    __instance = None

    def __init__(self):
        try:
            NileServiceDelegateHub.__init__(self)
            NileServiceMessageHub.__init__(self)
            NileServiceNetworkHub.__init__(self)
            NileServicePanelHub.__init__(self)
            NileServiceRedDotHub.__init__(self)
            self._root = None
            self._userData = None
            self._remoteConfig = None
            self._patchLoader = None
            self._state = NileService.STATE_PRE_INIT
            self._serialNumber = NileService.SN
            NileSettings.Initialize()
            NileLocalDirectoryHelper.Initialize()
            NileLogger.Initialize()
        except Exception as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe5\xae\x9e\xe4\xbe\x8b\xe5\x8c\x96\xe9\x94\x99\xe8\xaf\xaf, Message: %s' % str(e))

        return

    def GetSerialNumber(self):
        return self._serialNumber

    def GetState(self):
        return self._state

    def GetPanelRoot(self):
        return self._root

    @staticmethod
    def GetInstance():
        if not NileService.__instance:
            NileService.__instance = NileService()
        return NileService.__instance

    def Init(self, root, environment, gatewayUrl=''):
        try:
            if self._state != NileService.STATE_PRE_INIT:
                NileLogger.Error('\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8d\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x88\x87\xe5\x88\xb0\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe7\x8a\xb6\xe6\x80\x81, State: %s' % self._state)
                return
            if not root:
                NileLogger.Error('\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe9\x9d\xa2\xe6\x9d\xbf\xe6\xa0\xb9\xe8\x8a\x82\xe7\x82\xb9\xe4\xb8\xba\xe7\xa9\xba')
                return
            self._state = NileService.STATE_INIT
            self._root = root
            NileSettings.SetEnvironment(environment)
            if gatewayUrl and NileSettings.GetEnvironment() < NileSettings.ENV_PRODUCT:
                NileSettings.SetGatewayUrl(gatewayUrl)
            NileLogger.Reload()
            NileLogger.Info('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe6\x88\x90\xe5\x8a\x9f, Environment: %s' % NileSettings.GetEnvironmentDesc())
        except BaseException as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe5\x8f\x91\xe7\x94\x9f\xe5\xbc\x82\xe5\xb8\xb8, Message: %s' % str(e))

    def SetEventDelegate(self, value):
        NileLogger.Info('\xe8\xae\xbe\xe7\xbd\xae\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe6\xb6\x88\xe6\x81\xaf\xe5\xa4\x84\xe7\x90\x86\xe5\xa7\x94\xe6\x89\x98')
        self.SetNileMessageHandler(value)

    def GetUserData(self):
        return self._userData

    def SetUserData(self, userDataDict):
        try:
            if not self._userData:
                self._userData = NileUserData(userDataDict)
            else:
                oldToken = self._userData.token
                self._userData.Update(userDataDict)
                if self._userData.token != oldToken:
                    self.ExecuteTokenChangedMessage()
            NileLogger.Info('\xe8\xae\xbe\xe7\xbd\xae\xe7\x8e\xa9\xe5\xae\xb6\xe5\xad\x97\xe6\xae\xb5, UserData: %s' % str(self._userData))
        except BaseException as e:
            print('\xe8\xae\xbe\xe7\xbd\xae\xe7\x8e\xa9\xe5\xae\xb6\xe4\xbf\xa1\xe6\x81\xaf\xe5\x8f\x91\xe7\x94\x9f\xe5\xbc\x82\xe5\xb8\xb8, Message: %s' % str(e))

    def _IncreaseSerialNumber(self):
        NileService.SN += 1
        self._serialNumber = NileService.SN

    def OuterStart(self):
        if not NileSystemInfo.IsOnWorkbench():
            return
        self._DoStart()

    def Start(self):
        if NileSystemInfo.IsOnWorkbench():
            NileLogger.Info('***********\xe5\xa4\x84\xe4\xba\x8e\xe5\xbc\x80\xe5\x8f\x91\xe8\x80\x85\xe7\x8e\xaf\xe5\xa2\x83\xe4\xb8\x8b, \xe8\xaf\xb7\xe4\xbb\x8eNileEntry\xe6\x89\xa7\xe8\xa1\x8c***********')
            return
        self._DoStart()

    def _DoStart(self):
        try:
            NileTimer.SetErrorReportDelegate(NileLogReporter.GetInstance().ReportTimerError)
            NileCallbackWeakRef.SetErrorReportDelegate(NileLogReporter.GetInstance().ReportCallbackError)
            if self._state != NileService.STATE_INIT:
                NileLogger.Error('\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8d\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x88\x87\xe6\x8d\xa2\xe5\x88\xb0\xe5\x90\xaf\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81, State: %s' % self._state)
                return
            if not self._userData:
                NileLogger.Error('UserData\xe4\xb8\xbaNone\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\x98\xaf\xe5\x90\xa6\xe6\xad\xa3\xe5\xb8\xb8\xe8\xb0\x83\xe7\x94\xa8SetUserData\xe6\x8e\xa5\xe5\x8f\xa3')
                return
            if not self._userData.IsValidate():
                NileLogger.Error('UserData\xe5\xbf\x85\xe9\xa1\xbb\xe5\xad\x97\xe6\xae\xb5\xe6\x9c\x89\xe7\xbc\xba\xe5\xa4\xb1\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe5\xaf\xb9\xe6\x8e\xa5\xe9\x83\xa8\xe5\x88\x86\xe4\xbb\xa3\xe7\xa0\x81')
                return
            self._state = NileService.STATE_START
            self._LoadRemoteConfig()
        except BaseException as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe5\x90\xaf\xe5\x8a\xa8\xe5\x8f\x91\xe7\x94\x9f\xe5\xbc\x82\xe5\xb8\xb8, Message: %s' % str(e))

    def _LoadRemoteConfig(self, isReload=False):
        ruleLoader = NileRuleHttpLoader()
        message = '\xe5\xbc\x80\xe5\xa7\x8b\xe8\xaf\xb7\xe6\xb1\x82\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe8\xa7\x84\xe5\x88\x99, Url: %s' % ruleLoader.GetUrl()
        ruleLoader.SendPostRequest(ruleLoader.GetUrl(), self._OnRemoteConfigLoaded)
        if isReload:
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_RELOAD_REMOTE_CONFIG, message)
        else:
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_LOAD_REMOTE_CONFIG, message)

    def _OnRemoteConfigLoaded(self, remoteConfig):
        if self._state != NileService.STATE_START:
            return
        self._remoteConfig = remoteConfig
        if self._remoteConfig.isError:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_REMOTE_CONFIG, '\xe8\xa7\xa3\xe6\x9e\x90\xe8\xa7\x84\xe5\x88\x99\xe5\x8f\x91\xe7\x94\x9f\xe9\x94\x99\xe8\xaf\xaf, Message: %s, UserData: %s' % (self._remoteConfig.errorMessage, self._userData))
            NileLogger.Info('\xe8\xa7\x84\xe5\x88\x99\xe5\x86\x85\xe5\xae\xb9: %s' % self._remoteConfig.jsonStr)
            return
        if self._remoteConfig.isEmpty:
            message = '\xe8\xa7\xa3\xe6\x9e\x90\xe8\xa7\x84\xe5\x88\x99\xe7\xbb\x93\xe6\x9e\x9c\xe4\xb8\xba\xe7\xa9\xba, Message: %s UserData: %s' % (self._remoteConfig.errorMessage, self._userData)
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_EMPTY_REMOTE_CONFIG, message)
            NileLogger.Info('\xe8\xa7\x84\xe5\x88\x99\xe5\x86\x85\xe5\xae\xb9: %s' % self._remoteConfig.jsonStr)
            return
        self._ReloadLoggerSetting(self._remoteConfig)
        message = '\xe5\x8c\xb9\xe9\x85\x8d\xe5\x88\xb0\xe8\xa7\x84\xe5\x88\x99, ruleId:%s, remark: %s, env: %s, userdata: %s' % (self._remoteConfig.ruleId, self._remoteConfig.remark, NileSettings.GetEnvironmentDesc(), self._userData)
        NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_GOT_RULE, message)
        NileLogger.Info('\xe8\xa7\x84\xe5\x88\x99\xe5\x86\x85\xe5\xae\xb9: %s' % self._remoteConfig.jsonStr)
        self._LoadAllActivity()

    def _ReloadLoggerSetting(self, remoteConfig):
        NileSettings.SetIsDebug(remoteConfig.isDebug)
        NileLogger.Reload()

    def GetRemoteConfig(self):
        return self._remoteConfig

    def _LoadAllActivity(self):
        NileLogger.Info('\xe5\xbc\x80\xe5\xa7\x8b\xe5\x8a\xa0\xe8\xbd\xbd\xe6\x89\x80\xe6\x9c\x89\xe6\xb4\xbb\xe5\x8a\xa8\xe8\xb5\x84\xe6\xba\x90')
        self._patchLoader = NilePatchLoader(self._remoteConfig.activityConfigList, self._DelayExecuteOnActivityLoaded)
        self._patchLoader.Start()

    def _DelayExecuteOnActivityLoaded(self, name):
        NileTimer.SetTimeout(self.OnActivityLoaded, 50, name)

    def OnActivityLoaded(self, name):
        if self._state != NileService.STATE_START:
            NileLogger.Error('\xe5\xbd\x93\xe5\x89\x8dSDK\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8d\xe8\x83\xbd\xe6\x89\xa7\xe8\xa1\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x85\xa5\xe5\x8f\xa3, State: %s' % self._state)
            return
        moduleName = 'nileActivity.%s.%s' % (name, name)
        message = '\xe5\xbc\x80\xe5\xa7\x8b\xe6\x89\xa7\xe8\xa1\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x85\xa5\xe5\x8f\xa3, Name: %s' % moduleName
        try:
            __import__(moduleName)
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_EXECUTE_ENTRY, message)
        except BaseException as e:
            if str(e) == 'No module named %s.%s' % (name, name):
                try:
                    import C_file
                    C_file.set_fileloader_enable('patch', True)
                    __import__(moduleName)
                except Exception as e:
                    NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_ENTRY, '\xe6\x89\xa7\xe8\xa1\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x85\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99\xef\xbc\x9a %s, Message: %s' % (moduleName, str(e)))

            else:
                NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_ENTRY, '\xe6\x89\xa7\xe8\xa1\x8c\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x85\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99\xef\xbc\x9a %s, Message: %s' % (moduleName, str(e)))

    def LoadActivity(self, name):
        if self._state == NileService.STATE_PRE_INIT:
            NileLogger.Error('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe5\xb0\x9a\xe6\x9c\xaa\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96')
            return
        if self._state == NileService.STATE_INIT:
            self.Start()
            return
        if self._patchLoader and self._patchLoader.GetToLoadCount() == 0 and self._patchLoader.IsActivityExecuted(name) == False:
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_LOAD_ACTIVITY, 'Load activity: %s' % name)
            self._patchLoader.LoadActivity(name)

    def OpenActivityPanel(self, activityId, params=None):
        if self.GetActivityStatus(activityId) == 0:
            NileLogger.Error('\xe6\xb4\xbb\xe5\x8a\xa8\xe8\xb5\x84\xe6\xba\x90\xe5\xb0\x9a\xe6\x9c\xaa\xe5\x87\x86\xe5\xa4\x87\xe5\xa5\xbd, ActivityId: %s' % activityId)
            return
        self.ExecuteOpenPanelMessage(activityId=activityId, message=params or {})
        return self.GetActivityPanel(activityId)

    def GetActivityStatus(self, activityId):
        result = NileServiceMessageHub.GetActivityStatus(self, activityId)
        if result == 0:
            if self.GetState() == NileService.STATE_START and self.GetRemoteConfig():
                if self.GetRemoteConfig().isError:
                    if not self.GetRemoteConfig().isReloading:
                        self.GetRemoteConfig().isReloading = True
                        self._LoadRemoteConfig(True)
                elif self.GetRemoteConfig().HasActivityConfig(activityId):
                    config = self.GetRemoteConfig().GetActivityConfigByMarketId(activityId)
                    self.LoadActivity(config.name)
        return result

    def Pause(self):
        if self._patchLoader:
            NileLogger.Info('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3Patch\xe5\x8a\xa0\xe8\xbd\xbd\xe6\x9a\x82\xe5\x81\x9c')
            self._patchLoader.Pause()

    def Resume(self):
        if self._patchLoader:
            NileLogger.Info('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3Patch\xe5\x8a\xa0\xe8\xbd\xbd\xe7\xbb\xa7\xe7\xbb\xad')
            self._patchLoader.Resume()

    def Logout(self):
        try:
            if self._state != NileService.STATE_START:
                NileLogger.Info('\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8d\xe5\x8f\xaf\xe6\xb3\xa8\xe9\x94\x80, State: %s' % self._state)
                return
            self._IncreaseSerialNumber()
            self._ExecuteLogoutMessage()
            NileTimer.ClearAll()
            self.ClearGameMessageHandler()
            self._ClearActivityStatusDict()
            self._ClearPanelDict()
            self._ClearRedDotDict()
            NilePatchModuleHelper.UnloadModules()
            NileLogReporter.GetInstance().ReportStatus(NileLogReporter.STATUS_LOGOUT, '\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe6\xb3\xa8\xe9\x94\x80\xe6\x88\x90\xe5\x8a\x9f')
            if self._remoteConfig:
                self._remoteConfig.Reset()
            if self._userData:
                self._userData.Reset()
            self._patchLoader = None
            self._state = NileService.STATE_INIT
        except BaseException as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3SDK\xe6\xb3\xa8\xe9\x94\x80\xe5\x8f\x91\xe7\x94\x9f\xe5\xbc\x82\xe5\xb8\xb8: %s' % str(e))

        return
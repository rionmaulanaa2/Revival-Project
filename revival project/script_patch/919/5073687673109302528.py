# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileServiceMessageHub.py
from .NileUtil import NileUtil
from .NileLogger import NileLogger

class NileServiceMessageHub(object):

    def __init__(self):
        self._activityStatusDict = dict()
        self._debugMessageHandler = None
        self._nileMessageHandler = None
        self._gameMessageHandler = None
        return

    def SetNileMessageHandler(self, value):
        if not value:
            NileLogger.Error('\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe6\xb6\x88\xe6\x81\xafhandler\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba')
            return
        self._nileMessageHandler = value

    def SetGameMessageHandler(self, value):
        if not value:
            NileLogger.Error('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe4\xbe\xa7\xe6\xb8\xb8\xe6\x88\x8f\xe6\xb6\x88\xe6\x81\xafhandler\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba')
            return
        self._gameMessageHandler = value

    def SetDebugMessageHandler(self, value):
        self._debugMessageHandler = value

    def ClearGameMessageHandler(self):
        self._gameMessageHandler = None
        return

    def Execute(self, msgType, message, activityId=0):
        NileLogger.Info('game==>>nile, MsgType: %s Message: %s' % (msgType, message))
        if not self._gameMessageHandler:
            NileLogger.Error('\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe4\xbe\xa7\xe6\xb8\xb8\xe6\x88\x8f\xe6\xb6\x88\xe6\x81\xaf\xe5\xa4\x84\xe7\x90\x86Delegate')
            return
        try:
            self._gameMessageHandler(msgType, message, activityId)
        except BaseException as e:
            NileLogger.Error('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe4\xbe\xa7\xe5\xa4\x84\xe7\x90\x86\xe6\xb8\xb8\xe6\x88\x8f\xe6\xb6\x88\xe6\x81\xaf\xe5\x87\xba\xe9\x94\x99, %s, %s, %s, %s' % (msgType, activityId, str(e), NileUtil.GetTraceback()))

    def ExecuteCurrencyChangeMessage(self):
        self.Execute('currencyChange', {}, 0)

    def ExecuteLevelUpMessage(self, level):
        self.Execute('roleLevelUp', {'level': level}, 0)

    def ExecuteOpenPanelMessage(self, message, activityId):
        self.Execute('openPanel', message, activityId)

    def ExecuteTokenChangedMessage(self):
        self.Execute('tokenChanged', {}, 0)

    def ExecuteServerCommand(self, content):
        self.Execute('serverCommand', content, 0)

    def _ExecuteLogoutMessage(self):
        self.Execute('logout', {}, 0)
        self.Execute('nileFrameLogout', {}, 0)

    def GetActivityStatus(self, activityId):
        return self._activityStatusDict.get(activityId, 0)

    def SendMessageToGame(self, msgType, message, activityId):
        NileLogger.Info('nile==>>game, msgType: %s message: %s activityId: %s' % (msgType, message, activityId))
        if not self._nileMessageHandler:
            NileLogger.Error('\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe6\xb6\x88\xe6\x81\xafhandler\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return
        try:
            self._nileMessageHandler(msgType, message, activityId)
            if self._debugMessageHandler:
                self._debugMessageHandler(msgType, message, activityId)
        except BaseException as e:
            NileLogger.Error('\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\xa4\x84\xe7\x90\x86\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe6\xb6\x88\xe6\x81\xaf\xe5\x87\xba\xe9\x94\x99, %s, %s, %s, %s, %s' % (message.get('msgType', ''), message.get('activityId', ''), message.get('value', ''), str(e), NileUtil.GetTraceback()))

    def SendReadyMessageToGame(self, message, activityId):
        self._activityStatusDict[activityId] = 1
        self.SendMessageToGame('ready', message, activityId)

    def SendRedDotMessageToGame(self, message, activityId):
        self.SendMessageToGame('redDot', message, activityId)

    def SendOpenUrlMessageToGame(self, url):
        self.SendMessageToGame('openUrl', {'url': url}, 0)

    def SendGotoSystemMessageToGame(self, system):
        self.SendMessageToGame('gotoSystem', {'system': system}, 0)

    def SendUpdateTokenMessageToGame(self):
        self.SendMessageToGame('updateToken', {}, 0)

    def _ClearActivityStatusDict(self):
        self._activityStatusDict = dict()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileServiceDelegateHub.py
from .NileLogger import NileLogger
from .NileLogReporter import NileLogReporter
from .NileUtil import NileUtil

class NileServiceDelegateHub(object):

    def __init__(self):
        self._playSoundDelegate = None
        self._getCurrencyDelegate = None
        self._getItemIconDelegate = None
        self._getItemNameDelegate = None
        self._getItemConfigDelegate = None
        self._refreshTokenDelegate = None
        return

    def SetRefreshTokenDelegate(self, value):
        self._refreshTokenDelegate = value

    def RefreshToken(self):
        if not self._refreshTokenDelegate:
            return
        try:
            self._refreshTokenDelegate()
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\x88\xb7\xe6\x96\xb0Token\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99, Message: %s, trace: %s' % (str(e), NileUtil.GetTraceback()))

    def SetPlaySoundDelegate(self, value):
        self._playSoundDelegate = value

    def PlaySound(self, name):
        if not self._playSoundDelegate:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe9\x9f\xb3\xe6\x95\x88\xe6\x92\xad\xe6\x94\xbe\xe5\xa7\x94\xe6\x89\x98\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return
        try:
            NileLogger.Info('\xe6\x92\xad\xe6\x94\xbe\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe5\xa3\xb0\xe9\x9f\xb3: %s' % str(name))
            self._playSoundDelegate(name)
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe9\x9f\xb3\xe6\x95\x88\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99, Name: %s Message: %s, trace: %s' % (name, str(e), NileUtil.GetTraceback()))

    def SetGetCurrencyDelegate(self, value):
        self._getCurrencyDelegate = value

    def GetCurrency(self):
        if not self._getCurrencyDelegate:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe8\x8e\xb7\xe5\x8f\x96\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe8\xb4\xa7\xe5\xb8\x81\xe5\xa7\x94\xe6\x89\x98\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return dict()
        try:
            return self._getCurrencyDelegate() or dict()
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe8\x8e\xb7\xe5\x8f\x96\xe8\xb4\xa7\xe5\xb8\x81\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99\xef\xbc\x8cMessage: %s, trace: %s' % (str(e), NileUtil.GetTraceback()))

        return dict()

    def SetGetItemIconDelegate(self, value):
        self._getItemIconDelegate = value

    def GetItemIcon(self, itemId):
        if not self._getItemIconDelegate:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe8\x8e\xb7\xe5\x8f\x96\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe7\x89\xa9\xe5\x93\x81Icon\xe5\xa7\x94\xe6\x89\x98\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return ''
        try:
            return self._getItemIconDelegate(itemId) or ''
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe8\x8e\xb7\xe5\x8f\x96\xe7\x89\xa9\xe5\x93\x81Icon\xe8\xb7\xaf\xe5\xbe\x84\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99\xef\xbc\x8cItemId: %s, Message: %s, trace: %s' % (itemId, str(e), NileUtil.GetTraceback()))

        return ''

    def SetGetItemNameDelegate(self, value):
        self._getItemNameDelegate = value

    def GetItemName(self, itemId):
        if not self._getItemNameDelegate:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe8\x8e\xb7\xe5\x8f\x96\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe7\x89\xa9\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0\xe5\xa7\x94\xe6\x89\x98\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return ''
        try:
            return self._getItemNameDelegate(itemId) or ''
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe8\x8e\xb7\xe5\x8f\x96\xe9\x81\x93\xe5\x85\xb7\xe5\x90\x8d\xe7\xa7\xb0\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99\xef\xbc\x8cItemId: %s, Message: %s, trace: %s' % (itemId, str(e), NileUtil.GetTraceback()))

        return ''

    def SetGetItemConfigDelegate(self, value):
        self._getItemConfigDelegate = value

    def GetItemConfig(self, itemId):
        if not self._getItemConfigDelegate:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe6\x9c\xaa\xe6\x89\xbe\xe5\x88\xb0\xe8\x8e\xb7\xe5\x8f\x96\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe7\x89\xa9\xe5\x93\x81\xe9\x85\x8d\xe7\xbd\xae\xe5\xa7\x94\xe6\x89\x98\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x92\x8c\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe6\xad\xa3\xe7\xa1\xae\xe5\xaf\xb9\xe6\x8e\xa5')
            return dict()
        try:
            return self._getItemConfigDelegate(itemId) or dict()
        except BaseException as e:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_GAME_DELEGATE, '\xe8\xb0\x83\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe4\xbe\xa7\xe8\x8e\xb7\xe5\x8f\x96\xe9\x81\x93\xe5\x85\xb7\xe9\x85\x8d\xe7\xbd\xae\xe6\x8e\xa5\xe5\x8f\xa3\xe6\x8a\xa5\xe9\x94\x99, ItemId: %s, Message: %s, trace: %s' % (itemId, str(e), NileUtil.GetTraceback()))

        return dict()
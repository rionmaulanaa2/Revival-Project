# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileTimer.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import game3d
import time
from .NileCallbackWeakRef import NileCallbackWeakRef

class NileTimer(object):
    _errorReportDelegate = None
    _timerDict = dict()

    @staticmethod
    def SetInterval(func, delayInMillisecond, *args, **kwargs):
        if not callable(func):
            print('\xe4\xbc\xa0\xe5\x85\xa5func\xe5\xae\x9e\xe5\x8f\x82\xe6\x98\xaf\xe4\xb8\x8d\xe5\x8f\xaf\xe6\x89\xa7\xe8\xa1\x8c\xe5\xaf\xb9\xe8\xb1\xa1')
            return 0
        wrapper = NileTimerCallback(func, *args, **kwargs)
        wrapper.EnableOverheadChecking()
        timer = NileTimerProxy(True, delayInMillisecond, wrapper.Execute)
        NileTimer._RegisterTimer(timer)
        wrapper.SetTimerId(timer.id)
        return timer.id

    @staticmethod
    def SetIntervalUnsafe(func, delayInMillisecond, *args, **kwargs):
        timer = NileTimerProxy(True, delayInMillisecond, func, *args, **kwargs)
        NileTimer._RegisterTimer(timer)
        return timer.id

    @staticmethod
    def ClearInterval(timerId):
        NileTimer.Cancel(timerId)

    @staticmethod
    def SetTimeout(func, delayInMillisecond, *args, **kwargs):
        if not callable(func):
            print('\xe4\xbc\xa0\xe5\x85\xa5func\xe5\xae\x9e\xe5\x8f\x82\xe6\x98\xaf\xe4\xb8\x8d\xe5\x8f\xaf\xe6\x89\xa7\xe8\xa1\x8c\xe5\xaf\xb9\xe8\xb1\xa1')
            return 0
        wrapper = NileTimerCallback(func, *args, **kwargs)
        timer = NileTimerProxy(False, delayInMillisecond, wrapper.Execute)
        NileTimer._RegisterTimer(timer)
        wrapper.SetTimerId(timer.id)
        return timer.id

    @staticmethod
    def SetTimeoutUnsafe(func, delayInMillisecond, *args, **kwargs):
        timer = NileTimerProxy(False, delayInMillisecond, func, *args, **kwargs)
        NileTimer._RegisterTimer(timer)
        return timer.id

    @staticmethod
    def ClearTimeout(timerId):
        NileTimer.Cancel(timerId)

    @staticmethod
    def _RegisterTimer(timer):
        NileTimer._timerDict[timer.id] = timer

    @staticmethod
    def Cancel(timerId):
        if timerId in NileTimer._timerDict:
            NileTimer._timerDict[timerId].Cancel()
            NileTimer._timerDict.pop(timerId, None)
        return

    @staticmethod
    def SetErrorReportDelegate(value):
        NileTimer._errorReportDelegate = value

    @staticmethod
    def ErrorReport(message):
        if NileTimer._errorReportDelegate:
            NileTimer._errorReportDelegate(message)

    @staticmethod
    def ClearAll():
        for timerId in NileTimer._timerDict:
            NileTimer._timerDict[timerId].Cancel()

        NileTimer._timerDict = dict()


class NileTimerCallback(NileCallbackWeakRef):

    def __init__(self, callback, *args, **kwargs):
        super(NileTimerCallback, self).__init__(callback, *args, **kwargs)
        self.timerId = 0
        self.checkOverhead = False

    def EnableOverheadChecking(self):
        self.checkOverhead = True

    def SetTimerId(self, timerId):
        self.timerId = timerId

    def Execute(self, *args, **kwargs):
        if not self.IsValid():
            NileTimer.Cancel(self.timerId)
            NileTimer.ErrorReport('NileTimer\xe5\x9b\x9e\xe8\xb0\x83\xe5\x87\xbd\xe6\x95\xb0\xe5\xb7\xb2\xe4\xb8\x8d\xe5\x8f\xaf\xe7\x94\xa8\xef\xbc\x8c\xe8\xaf\xb7\xe5\x8f\x82\xe7\x9c\x8b\xe5\x87\xbd\xe6\x95\xb0\xe5\xb7\xb2\xe4\xb8\x8d\xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe8\xaf\xb4\xe6\x98\x8e\xe6\x96\x87\xe6\xa1\xa3 https://docs.popo.netease.com/lingxi/5cce50346c01404f8fd3c89963910d21 , Name: %s' % self.funcName)
            return
        try:
            start = six_ex.long_type(time.time() * 1000)
            super(NileTimerCallback, self).ExecuteUnsafe(*args, **kwargs)
            end = six_ex.long_type(time.time() * 1000)
            if self.checkOverhead and end - start > 15:
                NileTimer.ErrorReport('NileTimer\xe5\x9b\x9e\xe8\xb0\x83\xe5\x87\xbd\xe6\x95\xb0\xe8\x80\x97\xe6\x97\xb6\xe8\xbf\x87\xe9\x95\xbf\xef\xbc\x8c\xe8\x80\x97\xe6\x97\xb6: %s\xe6\xaf\xab\xe7\xa7\x92, Name: %s' % (end - start, self.funcName))
        except BaseException as e:
            NileTimer.Cancel(self.timerId)
            NileTimer.ErrorReport('NileTimer\xe5\x9b\x9e\xe8\xb0\x83\xe5\x87\xbd\xe6\x95\xb0\xe6\x89\xa7\xe8\xa1\x8c\xe9\x94\x99\xe8\xaf\xaf, \xe5\x87\xbd\xe6\x95\xb0\xe5\x90\x8d\xe7\xa7\xb0: %s, error message: %s, trace: %s' % (self.funcName, str(e), NileCallbackWeakRef.GetTraceback()))


class NileTimerProxy(object):
    __timerId = 100

    def __init__(self, repeat, delay, func, *args, **kwargs):
        self.id = NileTimerProxy._GetTimerId()
        self._internalId = -1
        self._repeat = repeat
        self._delay = delay
        self._func = func
        self._args = (args, kwargs)
        self._canceled = False
        self._Load()

    def _Load(self):
        if self._canceled:
            return
        try:
            self._internalId = game3d.delay_exec(self._delay, self._Execute)
        except BaseException as e:
            print('\xe7\xb3\xbb\xe7\xbb\x9f\xe5\xb1\x82Timer\xe5\x88\x9b\xe5\xbb\xba\xe5\xa4\xb1\xe8\xb4\xa5, Message: %s' % str(e))

    def _Execute(self):
        self._func(*self._args[0], **self._args[1])
        if self._repeat:
            self._Load()
        else:
            NileTimer.Cancel(self.id)
            self._func = None
            self._args = None
        return

    def Cancel(self):
        self._canceled = True
        game3d.cancel_delay_exec(self._internalId)

    @staticmethod
    def _GetTimerId():
        result = NileTimerProxy.__timerId
        NileTimerProxy.__timerId += 1
        return result
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/Timer.py
from __future__ import absolute_import
try:
    import __pypy__
    pypy = True
except:
    pypy = False

if not pypy:
    from . import mobilecommon
    if mobilecommon.replace_async:
        from ..mobilelog.LogManager import LogManager
        from .mobilecommon import asiocore
        _logger = LogManager.get_logger('asiocore_timer')

        class TimerManager(object):

            def __init__(self):
                asiocore.set_timer_handler(self)
                self.timers = {}

            def set_async_timer(self, flag):
                asiocore.set_async_timer(flag)
                asiocore.set_timer_handler(self)

            def addTimer(self, proxy):
                res = asiocore.add_timer_proxy(False, proxy.delay, proxy)
                timer_id, have_reference = res[0], res[1]
                if not have_reference:
                    self.timers[timer_id] = proxy
                return timer_id

            def addRepeatTimer(self, proxy):
                res = asiocore.add_timer_proxy(True, proxy.delay, proxy)
                timer_id, have_reference = res[0], res[1]
                if not have_reference:
                    self.timers[timer_id] = proxy
                return timer_id

            def delTimer(self, timerID):
                asiocore.del_timer(timerID)
                if timerID in self.timers:
                    self.timers.pop(timerID)

            def onTimer(self, timerID):
                proxy = self.timers.get(timerID, None)
                if not proxy:
                    _logger.error('onTimer not have timer with id(%d)', timerID)
                    return
                else:
                    if not proxy.repeat:
                        self.timers.pop(timerID, None)
                    proxy.tick()
                    return


        _timermanager = TimerManager()

        def _func_wrapper(func, args, kwargs):
            try:
                func(*args, **kwargs)
            except:
                _logger.log_last_except()


        class TimerProxy(object):

            def __init__(self, delay, func, args, kwargs, repeat, timermanager):
                self.delay = delay
                self.repeat = repeat
                self.func = lambda : _func_wrapper(func, args, kwargs)
                self.timermanager = timermanager
                if repeat:
                    self.timerID = timermanager.addRepeatTimer(self)
                else:
                    self.timerID = timermanager.addTimer(self)

            def cancel(self):
                self.timermanager.delTimer(self.timerID)

            def tick(self):
                self.func()

            def get_expire_time(self):
                return asiocore.get_timer_expire_time(self.timerID)


        class CallbackProxy(object):

            def __init__(self, delay, repeat, func):
                self.delay = delay
                self.repeat = repeat
                self.func = lambda : func(self.timerID)
                if repeat:
                    self.timerID = _timermanager.addRepeatTimer(self)
                else:
                    self.timerID = _timermanager.addTimer(self)

            def cancel(self):
                _timermanager.delTimer(self.timerID)
                self.func = None
                return

            def tick(self):
                self.func()


        def addTimer(delay, func, *args, **kwargs):
            return TimerProxy(delay, func, args, kwargs, False, _timermanager)


        def addRepeatTimer(delay, func, *args, **kwargs):
            return TimerProxy(delay, func, args, kwargs, True, _timermanager)


        def addCallback(delay, repeat, func):
            return CallbackProxy(delay, repeat, func).timerID


        def cancelTimer(timer_id):
            if not isinstance(timer_id, int):
                timer_id = timer_id.timerID
            _timermanager.delTimer(timer_id)


        def set_async_timer(flag):
            _timermanager.set_async_timer(flag)


        def tickTimer():
            _timermanager.tick()


    else:
        import asyncore_with_timer

        def addTimer(delay, func, *args, **kwargs):
            return asyncore_with_timer.CallLater(delay, func, *args, **kwargs)


        def addRepeatTimer(delay, func, *args, **kwargs):
            return asyncore_with_timer.CallEvery(delay, func, *args, **kwargs)


        def tickTimer():
            pass


else:

    def addTimer(delay, func, *args, **kwargs):
        raise Exception('not implement')


    def addRepeatTimer(delay, func, *args, **kwargs):
        raise Exception('not implement')
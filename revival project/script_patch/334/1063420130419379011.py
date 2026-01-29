# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/timer.py
from __future__ import absolute_import
import six
LOGIC = 1
CLOCK = 2
try:
    import ctimer_wrapper
    import clogic
    Timer = ctimer_wrapper.CTimerWrapper
    RELEASE = clogic.timer_release_flag()
except ImportError as e:
    RELEASE = 'RELEASE'
    GLOBAL_ID = 1
    CUR_TIMER_GROUP = 0
    MAX_TIMER = 10
    import exception_hook
    import six.moves.collections_abc
    import collections

    class Timer(object):

        class __TimerItem:

            def __init__(self, obj, func, args, interval, times, paused, mode, timedelta, strict):
                if interval == 0:
                    interval = 1 / 65
                self.obj = obj
                self.func = func
                self.args = list(args)
                self.times = times
                self.interval = interval
                self.elapsed = 0
                self.paused = paused
                self.mode = mode
                self.timedelta = timedelta
                self.strict = strict
                self.deleting = False
                self.timedelta_idx = 1 if obj else 0
                if timedelta:
                    self.args.insert(0, 0)
                if obj:
                    self.args.insert(0, obj)

        def __init__(self):
            global CUR_TIMER_GROUP
            self.timers = collections.OrderedDict()
            self._to_adds = collections.OrderedDict()
            self._updating = False
            self._timer_group = CUR_TIMER_GROUP
            CUR_TIMER_GROUP = (CUR_TIMER_GROUP + 1) % MAX_TIMER
            self.set_addcount_callback(None)
            self.set_deccount_callback(None)
            return

        def set_addcount_callback(self, func, *args):
            if func:
                self._addcount_callback = func
                self._addcount_callback_args = args
            else:
                self._addcount_callback = lambda *args: None
                self._addcount_callback_args = ()

        def set_deccount_callback(self, func, *args):
            if func:
                self._deccount_callback = func
                self._deccount_callback_args = args
            else:
                self._deccount_callback = lambda *args: None
                self._deccount_callback_args = ()

        def register(self, obj=None, func=None, args=None, interval=1, times=-1, paused=False, mode=LOGIC, timedelta=False, strict=False):
            global GLOBAL_ID
            if interval <= 0:
                log_error('timer interval cannot be zero.')
                raise ValueError('timer interval cannot be zero.')
            if args is None:
                args = ()
            item = Timer.__TimerItem(obj, func, args, interval, times, paused, mode, timedelta, strict)
            itemid = GLOBAL_ID * MAX_TIMER + self._timer_group
            GLOBAL_ID = GLOBAL_ID + 1
            self._to_adds[itemid] = item
            self._addcount_callback((len(self.timers) + len(self._to_adds)), *self._addcount_callback_args)
            return itemid

        def unregister(self, timerid):
            if timerid <= 0:
                return True
            else:
                if timerid % MAX_TIMER != self._timer_group:
                    exception_hook.post_stack('Timer Unregister Not Match the Register!')
                timer = None
                container = None
                if timerid in self.timers:
                    timer = self.timers[timerid]
                    container = self.timers
                else:
                    if timerid in self._to_adds:
                        timer = self._to_adds[timerid]
                        container = self._to_adds
                    if timer:
                        if self._updating:
                            timer.deleting = True
                        else:
                            container.pop(timerid)
                        return True
                return False

        def restart(self, timerid):
            if timerid % MAX_TIMER != self._timer_group:
                exception_hook.post_stack('Timer Restart Not Match the Register!')
            timer = None
            if timerid in self.timers:
                timer = self.timers[timerid]
            elif timerid in self._to_adds:
                timer = self._to_adds[timerid]
            if timer:
                timer.elapsed = 0
                return True
            else:
                return False

        def clean(self):
            self.timers.clear()
            self._to_adds.clear()

        def set_object(self, id, obj):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.obj = obj

        def set_args(self, id, args):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.args = list(args)
                if item.timedelta:
                    item.args.insert(0, 0)
                if item.obj:
                    item.args.insert(0, item.obj)

        def set_times(self, id, times):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.times = times

        def set_interval(self, id, interval):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.interval = interval

        def set_pause(self, id, pause):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.paused = pause

        def set_mode(self, id, mode):
            item = id in self.timers and self.timers[id] if 1 else self._to_adds.get(id)
            if item:
                item.mode = mode

        def update(self, dt):
            for timerid, timer in six.iteritems(self._to_adds):
                self.timers[timerid] = timer

            self._to_adds.clear()
            self._updating = True
            del_items = []
            timers = self.timers
            for id, item in six.iteritems(timers):
                if item.times == 0:
                    item.deleting = True
                if item.deleting:
                    del_items.append(id)
                elif not item.paused:
                    if item.mode == LOGIC:
                        self._update_logic_mode(item, dt)
                    else:
                        self._update_clock_mode(item, dt)

            for id in del_items:
                self.timers.pop(id)
                self._deccount_callback(len(self.timers), *self._deccount_callback_args)

            self._updating = False

        def _update_logic_mode(self, item, dt):
            item.elapsed += 1
            if item.elapsed >= item.interval and item.func:
                item.elapsed = 0
                if item.times > 0:
                    item.times -= 1
                if item.timedelta:
                    item.args[item.timedelta_idx] = item.interval * dt
                try:
                    ret = item.func(*item.args)
                except:
                    exception_hook.traceback_uploader()
                    ret = None

                if ret == RELEASE:
                    item.deleting = True
            return

        def _update_clock_mode(self, item, dt):
            item.elapsed += dt
            while item.elapsed >= item.interval and item.func and not item.deleting:
                delta_time = item.interval if item.strict else item.elapsed
                item.elapsed -= delta_time
                if item.times > 0:
                    item.times -= 1
                if item.timedelta:
                    item.args[item.timedelta_idx] = delta_time
                try:
                    ret = item.func(*item.args)
                except:
                    exception_hook.traceback_uploader()
                    ret = None

                if ret == RELEASE:
                    item.deleting = True

            return

        @staticmethod
        def reset_all_timer_group():
            global CUR_TIMER_GROUP
            CUR_TIMER_GROUP = 0
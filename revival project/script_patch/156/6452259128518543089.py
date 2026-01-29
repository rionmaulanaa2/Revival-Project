# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/IoService.py
from __future__ import absolute_import
import sys
from ..common import Timer
import datetime
import traceback
from ..common import mobilecommon
if mobilecommon.replace_async:
    import asyncore
    from ..common.mobilecommon import asiocore
else:
    import asyncore_with_timer

class IoService(object):

    def __init__(self, socket_map=None, io_thread=2):
        super(IoService, self).__init__()
        self.stopflag = False
        self.socket_map = socket_map
        self.io_thread = io_thread
        self.prof = None
        self.prof_name = None
        self.prof_flag = 0
        if sys.platform.startswith('linux'):
            import signal
            signal.signal(signal.SIGUSR1, self.prof_handler)
            signal.signal(signal.SIGINT, self.sigint_handler)
        if mobilecommon.replace_async:
            self.loop = self._asiocore_loop
        else:
            self.loop = self._asyncore_loop
        return

    def get_status(self):
        return asiocore.get_status()

    def set_service_max_per_tick(self, m):
        asiocore.set_service_max_per_tick(m)

    def set_timer_max_per_tick(self, m):
        asiocore.set_timer_max_per_tick(m)

    def set_callback_max_per_tick(self, m):
        asiocore.set_callback_max_per_tick(m)

    def _asiocore_loop(self, no_sleep=False):
        asiocore.poll(no_sleep)

    def _asyncore_loop(self, no_sleep=False):
        asyncore_with_timer.loop(0 if no_sleep else 0.01, True, self.socket_map, 1)

    def _io_start(self):
        if not mobilecommon.replace_async:
            return
        asiocore.set_thread_num(self.io_thread)
        asiocore.start()
        self.loop = self._io_loop

    def _io_loop(self):
        asiocore.poll()
        asyncore.loop(0, True, self.socket_map, 1)

    def _io_stop(self):
        if mobilecommon.replace_async:
            asyncore.close_all()
            asyncore.loop(0.05, True, self.socket_map, 1)
        else:
            asyncore_with_timer.close_all()
            asyncore_with_timer.loop(0.05, True, self.socket_map)

    def run(self, timeout=None):
        self._io_start()
        if timeout:
            Timer.addTimer(timeout, self.stop)
        while True:
            try:
                if self.prof_flag == 0:
                    self.loop()
                else:
                    if self.prof == None:
                        self.create_prof()
                    self.prof.runcall(self.loop)
            except KeyboardInterrupt:
                break
            except:
                pass

            if self.stopflag:
                break

        self._io_stop()
        return

    def stop(self):
        self.stopflag = True
        if mobilecommon.replace_async:
            asiocore.stop()
            asiocore.reset_timer_handler()

    def sigint_handler(self, signum, frame):
        self.stop()

    def create_prof(self):
        import cProfile
        self.prof = cProfile.Profile()
        dt = datetime.datetime.now()
        self.prof_name = 'prof_%s_%s.prof' % (str(dt.date()), str(dt.time()))

    def prof_handler(self, signum, frame):
        if self.prof_flag == 0:
            self.prof_flag = 1
            self.create_prof()
        else:
            self.prof_flag = 0
            if self.prof is not None:
                self.prof.dump_stats(self.prof_name)
            self.prof = None
            self.prof_name = None
        return
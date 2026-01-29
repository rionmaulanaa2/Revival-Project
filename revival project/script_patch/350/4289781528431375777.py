# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/AsynTaskExecutor.py
from __future__ import absolute_import
import sys
import time
import asyncore_with_timer

class AsynTaskExecutor(object):

    def __init__(self):
        super(AsynTaskExecutor, self).__init__()
        self.tasks = []

    def add_delay(self, delay_time):
        self.tasks.append(delay_time)

    def add_task(self, func):
        if callable(func):
            self.tasks.append(func)

    def execut(self):
        last_check = time.time()
        delta = 0
        while True:
            asyncore_with_timer.loop(0.1, True, None, 1)
            time.sleep(0.01)
            now = time.time()
            if now - last_check > delta:
                last_check = now
                if len(self.tasks) == 0:
                    break
                t = self.tasks.pop(0)
                if callable(t):
                    t()
                else:
                    delta = t

        return


def main():
    exector = AsynTaskExecutor()
    exector.add_task(lambda : sys.stdout.write('1\n'))
    exector.add_delay(1)
    exector.add_task(lambda : sys.stdout.write('2\n'))
    exector.add_delay(1)
    exector.execut()


if __name__ == '__main__':
    main()
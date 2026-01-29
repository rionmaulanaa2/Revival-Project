# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/daemon_thread.py
from __future__ import absolute_import
from __future__ import print_function
import threading
import queue
import threadpool
from .framework import Singleton

def thread_func(retqueue, callfunc, callback, args, kwargs):
    ret = callfunc(*args, **kwargs)
    retqueue.put((callback, ret, args, kwargs))


class DaemonThreadPoolOld(Singleton):

    def init(self):
        self.work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.threads = []
        self.update_count = 0
        self.update_max_count = 10

    def create_threadpool(self, num_of_threads=0):
        pass

    def add_threadpool(self, callfunc, callback, *args, **kwargs):
        item = (
         self.result_queue, callfunc, callback, args, kwargs)
        threading.Thread(target=thread_func, args=item).start()

    def update_threadpool(self, dt):
        while self.result_queue.qsize() > 0:
            callback, ret, args, kwargs = self.result_queue.get_nowait()
            if callback:
                callback(ret, *args, **kwargs)


class DaemonThreadPoolNew(Singleton):
    ALIAS_NAME = 'daemon_thread_pool'
    POOL_SIZE = 3
    QSIZE = 0

    def init(self):
        self.pool = None
        return

    def create_threadpool(self, num_of_threads=0):
        self.pool = threadpool.ThreadPool(self.POOL_SIZE, self.QSIZE, self.QSIZE, 1.0)

    def add_threadpool(self, callfunc, callback, *args, **kwargs):
        self.pool.putRequest(threadpool.WorkRequest(callfunc, args, kwargs, callback=callback, exc_callback=self._pool_ex_cb), timeout=2.0)

    def _pool_ex_cb(self, request, result):
        print('ERROR:DaemonThreadPoolNew Exception =====', request, result)

    def update_threadpool(self, dt):
        try:
            self.pool.poll(False)
        except threadpool.NoResultsPending:
            return True
        except Exception as e:
            print('update_threadpool ERROR:', str(e))
            import traceback
            traceback.print_exc()
            return False

        return True


DaemonThreadPool = DaemonThreadPoolNew
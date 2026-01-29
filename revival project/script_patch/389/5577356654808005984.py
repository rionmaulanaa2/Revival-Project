# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/FutureAndResponse.py
from __future__ import absolute_import
from .simplerpc_common import RPC_RESPONSE, addTimer
from .rpc_code import RPC_CODE
from ..mobilelog.LogManager import LogManager
logger = LogManager.get_logger('Future')

class Future(object):

    def __init__(self, rid, time_out=2):
        object.__init__(self)
        self._con_obj = None
        self._rid = rid
        self._fired = False
        self._cbs = []
        self._code = RPC_CODE.UNKNOWN
        self._error = None
        self._response_args = None
        self._timeout_seconds = time_out
        self._timeout_timer = addTimer(self._timeout_seconds, self._time_out)
        return

    def stop_time_out(self):
        self._timeout_timer.cancel()
        self._timeout_timer = None
        return

    def start_time_out(self):
        self._timeout_timer = addTimer(self._timeout_seconds, self._time_out)

    def set_con_obj(self, con):
        self._con_obj = con

    def _time_out(self):
        if self._con_obj:
            self._con_obj.fire_future(self._rid, RPC_CODE.TIMEOUT, 'timeout', None)
        else:
            self.fire(RPC_CODE.TIMEOUT, 'timeout', None)
        return

    @property
    def rid(self):
        return self._rid

    def add_listener(self, fn):
        if self._fired:
            self._execute_cb(fn)
        else:
            self._cbs.append(fn)

    def fire(self, code, error, args):
        if self._fired:
            return
        else:
            self._fired = True
            self._con_obj = None
            if self._timeout_timer:
                self._timeout_timer.cancel()
                self._timeout_timer = None
            self._code = code
            self._error = error
            self._response_args = args
            for fn in self._cbs:
                self._execute_cb(fn)

            self._cbs = []
            return

    def _execute_cb(self, fn):
        try:
            fn(self._code, self._error, self._response_args)
        except:
            logger.error('future cb execute error')
            logger.log_last_except()

    def sync(self):
        raise Exception('not implement sync')


class Response(object):

    def __init__(self, rid, con, rpc_processor):
        self._con = con
        self._send_data = con.send_data
        self._encode = rpc_processor.do_encode
        self._rid = rid
        self._send = False

    def send_response(self, code=RPC_CODE.UNKNOWN, args=None, error=''):
        if not self._send:
            self._send = True
            data = self._encode((RPC_RESPONSE, self._rid, (code, error, args)))
            self._send_data(data)
        else:
            raise Exception('duplicate response')

    @property
    def connection(self):
        return self._con

    @property
    def send(self):
        return self._send
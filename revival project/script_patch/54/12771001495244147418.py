# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/ChannelClient2.py
from __future__ import absolute_import
from ..common import Timer
from ..common import mobilecommon
from .TcpClient2 import TcpClient2
from ..mobilelog.LogManager import LogManager

class ChannelClient2(object):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_CONNECT_FAILED = 3
    ST_CONNECT_SUCCESSED = 4

    def __init__(self, ip, port, rpc_handler):
        super(ChannelClient2, self).__init__()
        self.ip = ip
        self.port = port
        self.timer = None
        self.rpc_handler = rpc_handler
        self.logger = LogManager.get_logger('server.ChannelClient2')
        self.client = TcpClient2(self.ip, self.port, self)
        self.status = ChannelClient2.ST_INIT
        return

    def peername(self):
        if self.client:
            return self.client.getpeername()
        return ''

    def reset(self, ip=None, port=None):
        self.status = ChannelClient2.ST_INIT
        if self.client:
            self.client.disconnect()
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port
        self.client = TcpClient2(self.ip, self.port, self)
        self.cancel_timer()

    def add_timer(self, timeout):
        self.cancel_timer()
        self.timer = Timer.addTimer(timeout, self._check_connection)

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return

    def _check_connection(self):
        self.timer = None
        if self.status != ChannelClient2.ST_CONNECT_SUCCESSED:
            self.logger.error('[%s] connection(%s) timeout', self.rpc_handler.__class__.__name__, self.peername())
            self.callback(False)
            self.status = ChannelClient2.ST_CONNECT_FAILED
        return

    def connect(self, callback, timeout):
        self.callback = callback
        self.status = ChannelClient2.ST_CONNECTING
        self.add_timer(timeout)
        self.client.async_connect()

    def disconnect(self):
        if self.client:
            self.client.disconnect()
            self.clear()

    def clear(self):
        self.rpc_handler = None
        self.client = None
        return

    def handle_new_connection(self, con):
        if mobilecommon.replace_async:
            self.client.set_handler(self.rpc_handler)
        self.status = ChannelClient2.ST_CONNECT_SUCCESSED
        self.cancel_timer()
        self.callback(True)

    def handle_connection_failed(self, con):
        self.logger.error('[%s] connection(%s) failed', self.rpc_handler.__class__.__name__, self.peername())
        self.status = ChannelClient2.ST_CONNECT_FAILED
        self.cancel_timer()
        self.callback(False)

    def destroy(self):
        self.disconnect()
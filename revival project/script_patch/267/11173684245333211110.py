# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/AsioUdpChannelClient.py
from __future__ import absolute_import
from ..common import Timer
from ..common import mobilecommon
if mobilecommon.use_kcp:
    from .KcpClient import KcpClient as AsioUdpClient
else:
    from .AsioUdpClient import AsioUdpClient
from ..mobilelog.LogManager import LogManager

class AsioUdpChannelClient(object):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_CONNECT_FAILED = 3
    ST_CONNECT_SUCCESSED = 4

    def __init__(self, ip, port, rpc_handler):
        super(AsioUdpChannelClient, self).__init__()
        self.ip = ip
        self.port = port
        self.timer = None
        self.rpc_handler = rpc_handler
        self.logger = LogManager.get_logger('server.AsioUdpChannelClient')
        self.client = AsioUdpClient(self.ip, self.port, self)
        self.status = AsioUdpChannelClient.ST_INIT
        return

    def peername(self):
        return self.client.getpeername()

    def reset(self, ip=None, port=None):
        self.status = AsioUdpChannelClient.ST_INIT
        if self.client:
            self.client.disconnect()
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port
        self.client = AsioUdpClient(self.ip, self.port, self)
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
        if self.status != AsioUdpChannelClient.ST_CONNECT_SUCCESSED:
            self.logger.error('connection timeout')
            self.callback(False)
            self.status = AsioUdpChannelClient.ST_CONNECT_FAILED
        return

    def connect(self, callback, timeout):
        self.client.async_connect()
        self.callback = callback
        self.status = AsioUdpChannelClient.ST_CONNECTING
        self.add_timer(timeout)

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
        self.status = AsioUdpChannelClient.ST_CONNECT_SUCCESSED
        self.cancel_timer()
        self.callback(True)

    def handle_connection_failed(self, con):
        self.logger.error('connection failed')
        self.status = AsioUdpChannelClient.ST_CONNECT_FAILED
        self.cancel_timer()
        self.callback(False)
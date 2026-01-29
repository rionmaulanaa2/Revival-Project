# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/ChannelClient.py
from __future__ import absolute_import
from ..common import Timer
from ..common import mobilecommon
from .RpcChannel import MobileRpcChannel
from ..mobilelog.LogManager import LogManager
if mobilecommon.replace_async:
    from .TcpClient2 import TcpClient2 as TcpClient
else:
    from .TcpClient import TcpClient

class ChannelClient(object):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_CONNECT_FAILED = 3
    ST_CONNECT_SUCCESSED = 4

    def __init__(self, ip, port, rpc_service):
        super(ChannelClient, self).__init__()
        self.rpc_service = rpc_service
        self.ip = ip
        self.port = port
        self.logger = LogManager.get_logger('server.ChannelClient')
        self.timer = None
        self.client = TcpClient(self.ip, self.port, self) if ip and port else None
        self.status = ChannelClient.ST_INIT
        return

    def peername(self):
        return self.client.getpeername()

    def reset(self, ip=None, port=None):
        if self.client:
            self.client.close()
            self.client = None
        self.status = ChannelClient.ST_INIT
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port
        self.client = TcpClient(self.ip, self.port, self)
        self.cancel_timer()
        return

    def cancel_timer(self):
        if mobilecommon.replace_async:
            if self.timer:
                self.timer.cancel()
                self.timer = None
        elif self.timer and not self.timer.cancelled and not self.timer.expired:
            self.timer.cancel()
            self.timer = None
        return

    def _check_connection(self):
        self.timer = None
        if self.status != ChannelClient.ST_CONNECT_SUCCESSED:
            self.logger.error('connection timeout')
            self.status = ChannelClient.ST_CONNECT_FAILED
            self.callback(None)
        return

    def connect(self, callback, timeout):
        self.client.async_connect()
        self.callback = callback
        self.status = ChannelClient.ST_CONNECTING
        self.timer = Timer.addTimer(timeout, self._check_connection)

    def disconnect(self):
        if self.client:
            self.client.disconnect()

    def handle_new_connection(self, con):
        if self.status != ChannelClient.ST_CONNECTING:
            self.logger.error('status not consist, may be disconnect before, status: %s', self.status)
            return
        if mobilecommon.replace_async:
            pass
        rpc_channel = MobileRpcChannel(self.rpc_service, con)
        self.status = ChannelClient.ST_CONNECT_SUCCESSED
        self.callback(rpc_channel)

    def handle_connection_failed(self, con):
        if self.status == ChannelClient.ST_CONNECTING:
            self.cancel_timer()
            self.logger.error('connection failed')
            self.status = ChannelClient.ST_CONNECT_FAILED
            self.callback(None)
        return
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/AsioChannelClient.py
from __future__ import absolute_import
from ..common import Timer
from .TcpClient2 import TcpClient2
from ..mobilelog.LogManager import LogManager
from .KcpClient import KcpClient

class AsioChannelClient(object):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_CONNECT_FAILED = 3
    ST_CONNECT_SUCCESSED = 4

    def __init__(self, ip, port, rpc_handler, con_type):
        super(AsioChannelClient, self).__init__()
        self.logger = LogManager.get_logger('server.AsioChannelClient')
        self.ip = ip
        self.port = port
        self.timer = None
        self.rpc_handler = rpc_handler
        self.con_type = con_type
        self.client = self._create_client(con_type) if ip and port else None
        self.status = AsioChannelClient.ST_INIT
        return

    def peername(self):
        return self.client.getpeername()

    def reset(self, ip=None, port=None):
        if self.client:
            self.client.disconnect()
            self.client = None
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port
        self.client = self._create_client(self.con_type)
        self.status = AsioChannelClient.ST_INIT
        self.cancel_timer()
        return

    def add_timer(self, timeout):
        self.cancel_timer()
        self.timer = Timer.addTimer(timeout, self._check_connection)

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return

    def _create_client(self, con_type):
        if con_type in ('TCP', 'tcp'):
            client = TcpClient2(self.ip, self.port, self)
        elif con_type in ('KCP', 'kcp'):
            client = KcpClient(self.ip, self.port, self)
        else:
            raise Exception('con_type(%s) not imp' % con_type)
        return client

    def _check_connection(self):
        self.timer = None
        if self.status != AsioChannelClient.ST_CONNECT_SUCCESSED:
            self.logger.error('connection timeout')
            self.status = AsioChannelClient.ST_CONNECT_FAILED
            self.callback(False)
        return

    def connect(self, callback, timeout):
        self.callback = callback
        self.status = AsioChannelClient.ST_CONNECTING
        self.add_timer(timeout)
        self.client.async_connect()

    def disconnect(self):
        client = self.client
        if client:
            self.handle_connection_failed(client)
            client.disconnect()

    def clear(self):
        self.rpc_handler = None
        self.client = None
        return

    def handle_new_connection(self, con):
        if self.status != AsioChannelClient.ST_CONNECTING or con != self.client:
            self.logger.error('status not consist, may be disconnect before, status: %s', self.status)
            return
        self.client.set_handler(self.rpc_handler)
        self.status = AsioChannelClient.ST_CONNECT_SUCCESSED
        self.cancel_timer()
        self.callback(True)

    def handle_connection_failed(self, con):
        if self.status == AsioChannelClient.ST_CONNECTING and con == self.client:
            self.logger.error('connect failed')
            self.status = AsioChannelClient.ST_CONNECT_FAILED
            self.cancel_timer()
            self.callback(False)
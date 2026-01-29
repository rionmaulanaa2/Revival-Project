# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/SimpleIpPortServer.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from .SimpleIpPortConnection import SimpleIpPortConnection
from .simplerpc_common import TCP, ENET, KCP
import os

class SimpleIpPortServer(object):

    def __init__(self, ip, port, buf_size=4096, con_type=TCP):
        self.logger = LogManager.get_logger('simplerpc.SimpleIpPortServer')
        self._type = con_type
        if self._type == TCP:
            from . import check_in_service_env
            if check_in_service_env():
                from ..IO.TCPServer import SimpleTcpServerProxy as simple_tcp_server
                self._server = simple_tcp_server(self)
            else:
                from ..common.mobilecommon import asiocore
                self._server = asiocore.simple_tcp_server(self, buf_size)
        elif self._type == KCP:
            from ..common.mobilecommon import asiocore, KCP_CONNECTION_TIMEOUT
            self._server = asiocore.simple_kcp_server(self, buf_size)
        elif self._type == ENET:
            from ..common.mobilecommon import asiocore
            self._server = asiocore.simple_udp_server(self, buf_size)
        else:
            raise Exception('unknown server type')
        self._ip = ip
        self._port = port

    def get_processor(self):
        con = self.do_get_processor()
        return con

    def do_get_processor(self):
        raise Exception('not implement do_get_processor')

    def start(self):
        self._server.bind(str(self._ip), self._port)
        if self._type == TCP:
            self._server.listen(50)
        else:
            self._server.listen()
        if self._type == TCP:
            type_str = 'TCP'
        elif self._type == ENET:
            type_str = 'ENET'
        else:
            type_str = 'KCP'

    def stop(self):
        self._server.stop()

    def on_close(self):
        pass
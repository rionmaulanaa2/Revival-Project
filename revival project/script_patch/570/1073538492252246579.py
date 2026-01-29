# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/TcpServer2.py
from __future__ import absolute_import
import sys
from ..common.mobilecommon import asiocore
from ..mobilelog.LogManager import LogManager

class TcpServer2(asiocore.async_server):

    def __init__(self, ip, port, con_handler, reuse_addr=False, service_warn_send_limit=0, service_recv_limit=0):
        super(TcpServer2, self).__init__()
        self.logger = LogManager.get_logger('mobilerpc.TcpServer2')
        self.ip = ip
        self.port = port
        self.started = False
        self.con_handler = con_handler
        self.set_reuse_addr(reuse_addr)
        self.set_warn_send_limit(service_warn_send_limit)
        self.set_recv_limit(service_recv_limit)
        self.try_bind()
        self.listen(8192)

    def listen_port(self):
        return (
         self.ip, self.port)

    def try_bind(self):
        self.bind(self.ip, self.port)
        self.started = True

    def reset_connection(self):
        self.set_handler(self.con_handler.create_handler())
        super(TcpServer2, self).reset_connection()

    def stop(self):
        super(TcpServer2, self).stop()

    def close(self):
        self.stop()
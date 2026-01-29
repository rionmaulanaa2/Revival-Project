# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/AsioUdpServer.py
from __future__ import absolute_import
from six.moves import range
import sys
from ..common.mobilecommon import asiocore
from ..mobilelog.LogManager import LogManager

class AsioUdpServer(asiocore.async_udp_server):

    def __init__(self, ip, port, con_handler):
        super(AsioUdpServer, self).__init__()
        self.logger = LogManager.get_logger('mobilerpc.AsioUdpServer')
        self.ip = ip
        self.port = port
        self.started = False
        self.con_handler = con_handler
        self.try_bind()
        self.listen()

    def listen_port(self):
        return (
         self.ip, self.port)

    def try_bind(self):
        for i in range(100):
            try:
                self.bind(self.ip, self.port)
                break
            except:
                self.port += 1
                sys.__excepthook__(*sys.exc_info())

        else:
            raise Exception(' Server failed to find a usable port to bind!')

        self.started = True

    def reset_connection(self):
        self.set_handler(self.con_handler.create_handler())
        super(AsioUdpServer, self).reset_connection()

    def stop(self):
        super(AsioUdpServer, self).stop()

    def close(self):
        self.stop()

    def set_timeout(self, timeout):
        self.timeout = timeout
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/AsioUdpClient.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from .AsioUdpConnection import AsioUdpConnection

class AsioUdpClient(AsioUdpConnection):

    def __init__(self, ip, port, con_handler=None):
        AsioUdpConnection.__init__(self, con_handler, ip, port)
        self.ip = ip
        self.port = port
        self.logger = LogManager.get_logger('mobilerpc.AsioUdpClient')

    def set_connection_handler(self, con_handler):
        self.con_handler = con_handler

    def async_connect(self):
        self.connect(self.ip, self.port)

    def handle_connected(self):
        if self.con_handler:
            self.status = AsioUdpConnection.ST_ESTABLISHED
            self.con_handler.handle_new_connection(self)

    def handle_close(self):
        AsioUdpConnection.handle_close(self)
        self.con_handler.handle_connection_failed(self)
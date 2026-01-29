# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/TcpClient2.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from .TcpConnection2 import TcpConnection2
from ..common import mobilecommon

class TcpClient2(TcpConnection2):

    def __init__(self, ip, port, con_handler=None):
        TcpConnection2.__init__(self, con_handler, ip, port)
        self.ip = ip
        self.port = port
        self.logger = LogManager.get_logger('mobilerpc.TcpClient2')

    def set_connection_handler(self, con_handler):
        self.con_handler = con_handler

    def async_connect(self):
        family, ip, port = mobilecommon.get_sockinfo(self.ip, self.port)
        self.setsockopt(':' in ip)
        self.connect(ip, port)

    def handle_connected(self):
        if self.con_handler:
            self.status = TcpConnection2.ST_ESTABLISHED
            self.con_handler.handle_new_connection(self)

    def handle_close(self):
        if self.con_handler:
            self.con_handler.handle_connection_failed(self)
        TcpConnection2.handle_close(self)
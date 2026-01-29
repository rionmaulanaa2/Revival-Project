# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/SimpleIpPortConnection.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from .simplerpc_common import addTimer, addRepeatTimer
logger = LogManager.get_logger('SimpleIpPortConnection')
from .simplerpc_common import TCP, ENET, KCP

class SimpleIpPortConnection(object):

    def __init__(self, con_type=TCP):
        object.__init__(self)
        self._type = con_type
        self._connected = False
        self._con = None
        self._con_timer = None
        self._connect_str = ''
        self._remote_address = None
        return

    def _release_con_timer(self):
        if self._con_timer:
            self._con_timer.cancel()
            self._con_timer = None
        return

    def get_remote_address_str(self):
        if self._con:
            return self._con.get_remote_address_str()
        return ''

    def connect(self, ip, port, timeout=2):
        self._remote_address = (
         ip, port)
        self._connect_str = ''.join([ip, ':', str(port)])
        if not self._connected and not self._con:
            self._con_timer = addTimer(timeout, lambda : self.connect_timeout(ip, port))
            if self._type == TCP:
                from . import check_in_service_env
                if check_in_service_env():
                    from ..IO.TCPSocket import SimpleMessageTcpConProxy
                    self._con = SimpleMessageTcpConProxy(self, None, None)
                else:
                    from ..common.mobilecommon import asiocore, get_sockinfo
                    family, ip, port = get_sockinfo(ip, port)
                    self._con = asiocore.simple_tcp_connection(self)
                    self._con.setsockopt(':' in ip)
            elif self._type == KCP:
                from ..common.mobilecommon import asiocore, get_sockinfo
                self._con = asiocore.simple_kcp_connection(self)
                family, ip, port = get_sockinfo(ip, port)
            elif self._type == ENET:
                from ..common.mobilecommon import asiocore, get_sockinfo
                self._con = asiocore.simple_udp_connection(self)
                family, ip, port = get_sockinfo(ip, port)
            else:
                raise Exception('unknown connection type')
            self._con.connect(str(ip), port)
        else:
            raise Exception('already connected')
        return

    def connect_sync(self, ip, port, timeout=2):
        from ..IO.TCPSocket import SimpleMessageTcpConProxy
        self._remote_address = (
         ip, port)
        self._connect_str = ''.join([ip, ':', str(port)])
        self._con = SimpleMessageTcpConProxy(self, None, None)
        self._con.connect_sync(ip, port, timeout=timeout)
        return

    def connect_timeout(self, ip, port):
        self._con_timer = None
        if not self._connected:
            logger.error('connect timeout %s', self._connect_str)
            if self._con:
                self._con.close_connection()
                self._con = None
        return

    def set_connection(self, con):
        self._con = con
        from . import check_in_service_env
        if check_in_service_env():
            from ..IO.TCPSocket import SimpleMessageTcpConProxy
            if isinstance(con, SimpleMessageTcpConProxy):
                self._type = TCP
        else:
            from ..common.mobilecommon import asiocore
            if isinstance(con, asiocore.simple_kcp_connection):
                self._type = KCP
            elif isinstance(con, asiocore.simple_tcp_connection):
                self._type = TCP
            elif isinstance(con, asiocore.simple_udp_connection):
                self._type = ENET
            else:
                logger.error('[SimpleIpPortConnection %s] unknown type', con)

    def handle_message(self, message_data):
        pass

    def handle_close(self):
        if self._con_timer:
            self._release_con_timer()
            logger.info('connect fail %s', self._connect_str)
        else:
            if self._con:
                logger.info('SimpleIpPortConnection: connection died, remote: [%s]', self._con.get_remote_address_str())
            self._connected = False
        self._con = None
        return

    def handle_connected(self):
        if self._con:
            logger.info('connection established, remote: [%s]', self._con.get_remote_address_str())
            self._connected = True
            self._release_con_timer()
        else:
            logger.info('connection established, but maybe invoke close or connect timeout before')

    def send_data(self, data):
        if self._connected:
            self._con.send(data)

    def send_data_udp(self, data):
        if not self._connected:
            return
        if self._type == KCP:
            self._con.send_udp(data)
        else:
            self._con.send(data)

    def close(self):
        self._release_con_timer()
        if self._con:
            logger.info('do closing socket, remote: [%s]', self._con.get_remote_address_str())
            self._con.close_connection()
            self._connected = False
            self._con = None
        return
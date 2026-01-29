# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/TcpClient.py
from __future__ import absolute_import
from __future__ import print_function
import sys
import asyncore_with_timer
import time
import gflags
import socket
from .TcpConnection import TcpConnection
from ..mobilelog.LogManager import LogManager
from .ChannelObjs import LogMessageChannelObj
from .ConnectionManager import ConnectionManager
from ..common import mobilecommon

class TcpClient(TcpConnection):

    def __init__(self, ip, port, con_handler=None):
        TcpConnection.__init__(self, None, (ip, port))
        self.con_handler = con_handler
        self.logger = LogManager.get_logger('mobilerpc.TcpClient')
        return

    def close(self):
        self.disconnect(False)

    def set_connection_handler(self, con_handler):
        self.con_handler = con_handler

    def async_connect(self):
        family, ip, port = mobilecommon.get_sockinfo(*self.peername)
        self.create_socket(family, socket.SOCK_STREAM)
        self.setsockopt()
        self.connect((ip, port))

    def sync_connect(self):
        family, sockaddr = self.get_sockinfo()
        sock = socket.socket(family, socket.SOCK_STREAM)
        try:
            sock.connect(sockaddr)
        except socket.error as msg:
            sock.close()
            return False

        sock.setblocking(0)
        self.set_socket(sock)
        self.setsockopt()
        self.status = TcpConnection.ST_ESTABLISHED
        return True

    def handle_connect(self):
        if self.con_handler:
            self.status = TcpConnection.ST_ESTABLISHED
            self.con_handler.handle_new_connection(self)

    def handle_close(self):
        TcpConnection.handle_close(self)
        self.con_handler.handle_connection_failed(self)


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_string('host', '127.0.0.1', 'example server ip')
    gflags.DEFINE_integer('port', 1234, 'example server port', lower_bound=0, upper_bound=65535)
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
        sys.exit(1)

    client = TcpClient(FLAGS.host, FLAGS.port)
    con_manager = ConnectionManager(lambda con: LogMessageChannelObj(con))
    client.set_connection_handler(con_manager)
    client.sync_connect()
    client.send_data('Hello')
    asyncore_with_timer.loop(0.1, True, None, 1)
    time.sleep(1)
    asyncore_with_timer.loop(0.1, True, None, 1)
    client.disconnect()
    asyncore_with_timer.loop(0.1, True, None, 1)
    return


if __name__ == '__main__':
    import gc
    gc.disable()
    print('gc.collect()', gc.collect())
    gc.set_debug(gc.DEBUG_LEAK)
    main(sys.argv)
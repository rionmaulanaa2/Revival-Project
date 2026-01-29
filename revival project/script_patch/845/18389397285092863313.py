# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/TcpServer.py
from __future__ import absolute_import
from __future__ import print_function
import sys
import asyncore
import asyncore_with_timer
import socket
import time
import inspect
import gflags
from ..mobilelog.LogManager import LogManager
from .TcpConnection import TcpConnection
from .ConnectionManager import ConnectionManager
from .ChannelObjs import EchoMessageChannelObj

class TcpServer(asyncore.dispatcher):

    def __init__(self, ip, port, con_handler=None, reuse_addr=False):
        self.ip = ip
        self.port = port
        self.con_handler = con_handler
        asyncore.dispatcher.__init__(self)
        self.logger = LogManager.get_logger('mobilerpc.TcpServer')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        if reuse_addr:
            self.set_reuse_addr()
        self.started = False
        self.try_bind()
        self.listen(50)

    def listen_port(self):
        return (
         self.ip, self.port)

    def try_bind(self):
        try:
            self.bind((self.ip, self.port))
        except:
            self.logger.error('try_bind: Server failed to find a usable port to bind: %s, %d', self.ip, self.port)
            raise Exception(' Server failed to find a usable port to bind!')

        self.started = True

    def set_connection_handler(self, con_handler):
        self.con_handler = con_handler

    def handle_accept(self):
        try:
            sock, addr = self.accept()
        except socket.error:
            self.logger.log_last_except()
            return
        except TypeError:
            self.logger.log_last_except()
            return

        if self.con_handler:
            con = TcpConnection(sock, addr)
            self.con_handler.handle_new_connection(con)

    def handle_error(self):
        self.logger.error('handle_error - uncaptured python exception')
        self.logger.error(str(inspect.stack()))

    def handle_close(self):
        pass

    def stop(self):
        self.close()
        self.started = False

    def close(self):
        asyncore.dispatcher.close(self)


def main(argv):
    FLAGS = gflags.FLAGS
    gflags.DEFINE_string('host', '127.0.0.1', 'example server ip')
    gflags.DEFINE_integer('port', 1234, 'example server port', lower_bound=0, upper_bound=65535)
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print('%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS))
        sys.exit(1)

    con_manager = ConnectionManager(lambda con: EchoMessageChannelObj(con))
    TcpServer(FLAGS.host, FLAGS.port, con_manager)
    while True:
        asyncore_with_timer.loop(1, True, None, 1)
        time.sleep(0.001)

    return


if __name__ == '__main__':
    main(sys.argv)
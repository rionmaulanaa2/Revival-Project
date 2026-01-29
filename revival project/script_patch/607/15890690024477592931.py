# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/TcpConnection.py
from __future__ import absolute_import
import asyncore
import socket
from ..mobilelog.LogManager import LogManager
from six_ex.moves.StringIO import StringIO

class TcpConnection(asyncore.dispatcher):
    DEFAULT_RECV_BUFFER = 4096
    ST_INIT = 0
    ST_ESTABLISHED = 1
    ST_DISCONNECTED = 2

    def __init__(self, sock, peername):
        self.status = TcpConnection.ST_INIT
        self.w_buffer = StringIO()
        if sock:
            self.status = TcpConnection.ST_ESTABLISHED
        asyncore.dispatcher.__init__(self, sock)
        self.logger = LogManager.get_logger('mobilerpc.TcpConnection')
        self.recv_buffer_size = TcpConnection.DEFAULT_RECV_BUFFER
        self.channel_interface_obj = None
        self.peername = peername
        self.encrypter = None
        self.decrypter = None
        self.compressor = None
        if sock:
            self.setsockopt()
        return

    def setsockopt(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if hasattr(socket, 'TCP_KEEPCNT') and hasattr(socket, 'TCP_KEEPIDLE') and hasattr(socket, 'TCP_KEEPINTVL'):
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
            self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)

    def get_channel_interface_obj(self):
        return self.channel_interface_obj

    def set_channel_interface_obj(self, channel_obj):
        self.channel_interface_obj = channel_obj

    def set_compressor(self, compressor):
        self.compressor = compressor

    def set_crypter(self, encrypter, decrypter):
        self.encrypter = encrypter
        self.decrypter = decrypter

    def established(self):
        return self.status == TcpConnection.ST_ESTABLISHED

    def set_rcv_buffer(self, size):
        self.recv_buffer_size = size

    def disconnect(self, flush=True):
        if self.status == TcpConnection.ST_DISCONNECTED:
            return
        else:
            self.status = TcpConnection.ST_DISCONNECTED
            if self.channel_interface_obj:
                self.channel_interface_obj.on_disconnected()
            self.channel_interface_obj = None
            if self.socket:
                if self.writable() and flush:
                    self.handle_write()
                asyncore.dispatcher.close(self)
            return

    def getpeername(self):
        return self.peername

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        self.disconnect(False)

    def handle_expt(self):
        asyncore.dispatcher.handle_expt(self)
        self.disconnect(False)

    def handle_error(self):
        asyncore.dispatcher.handle_error(self)
        self.disconnect(False)

    def handle_read(self):
        data = self.recv(self.recv_buffer_size)
        if data:
            if self.channel_interface_obj == None:
                return
            if self.decrypter:
                data = self.decrypter.decrypt(data)
            if self.compressor:
                data = self.compressor.decompress(data)
            rc = self.channel_interface_obj.input_data(data)
            if rc == 2:
                return
            if rc == 3:
                self.logger.error('buf length error')
            elif rc == 0:
                self.disconnect(False)
                return
            else:
                self.disconnect(False)
                return

        return

    def handle_write(self):
        buff = self.w_buffer.getvalue()
        if buff:
            sent = self.send(buff)
            self.w_buffer = StringIO(buff[sent:])
            self.w_buffer.seek(0, 2)

    def send_data(self, data):
        if self.compressor:
            data = self.compressor.compress(data)
        if self.encrypter:
            data = self.encrypter.encrypt(data)
        self.w_buffer.write(data)

    def writable(self):
        return self.w_buffer and self.w_buffer.getvalue() or self.status != TcpConnection.ST_ESTABLISHED
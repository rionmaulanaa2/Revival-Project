# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/tcp/main.py
import socket
from collections import deque
from ..interfaces import IConnection, IServer, IClient, ServerOnConnectMessage, ServerOnCloseMessage, ClientOnConnectMessage, ClientOnCloseMessage
from .asynctcp import Host, Client, init_loop, asyncore
from .protocol import SimpleProtocolFilter
DEFAULT_ADDR = ('localhost', 5001)

class TcpConn(IConnection):

    def __init__(self, client):
        super(TcpConn, self).__init__()
        self.client = client
        self.prot = SimpleProtocolFilter()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.client.say(msg_bytes)

    def recv(self):
        msg_bytes = self.client.read_message()
        return self.prot.input(msg_bytes)

    @property
    def cid(self):
        return self.client.cid


class TcpServer(IServer):

    def __init__(self, addr=DEFAULT_ADDR, backend=False, maxClientCount=0):
        super(TcpServer, self).__init__()
        self.msg_queue = deque()
        self.s = None
        self.addr = addr
        self.backend = backend
        self.initServer(addr, maxClientCount)
        self._s_handle_accept, self._s_close_client = self.s.handle_accept, self.s.close_client
        self.s.handle_accept, self.s.close_client = self._handle_accept, self._close_client
        self._connections = {}
        return

    def initServer(self, addr, maxClientCount):
        startPort = port = addr[1]
        for i in range(10):
            try:
                self.s = Host(('0.0.0.0', port), maxClientCount)
            except OSError as err:
                if err.errno in (10048, 48):
                    port += 1
                    continue
            else:
                self.addr = (
                 addr[0], port)
                return port

        raise Exception('wtf!!!socket in use from %d to %d' % (startPort, startPort + 10))

    def start(self):
        if self.backend:
            init_loop()

    @property
    def connections(self):
        return self._connections

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

        buf = []
        for cid, conn in list(self._connections.items()):
            for msg in conn.recv():
                buf.append((conn, msg))

        for i in buf:
            yield i

    def update(self):
        if not self.backend:
            asyncore.loop(timeout=0.0, count=1)

    def close(self):
        self.s.close()

    def close_client(self, cid):
        if cid not in self._connections:
            return
        self._close_client(cid)

    def _handle_accept(self):
        client = self._s_handle_accept()
        if client is None:
            return
        else:
            if self.backend:
                client.set_thread_mode()
            conn = TcpConn(client)
            self._connections[client.cid] = conn
            self.msg_queue.append((conn, ServerOnConnectMessage()))
            return

    def _close_client(self, client_id):
        client = self._s_close_client(client_id)
        conn = self._connections.pop(client.cid)
        self.msg_queue.append((conn, ServerOnCloseMessage()))

    def closeClient(self, client):
        for clientid in self.s.remote_clients:
            if self.s.remote_clients[clientid] == client:
                self.s.close_client(clientid)
                break


class TcpClient(IClient):

    def __init__(self, addr=DEFAULT_ADDR, backend=False):
        super(TcpClient, self).__init__()
        self.backend = backend
        self.prot = SimpleProtocolFilter()
        self.msg_queue = deque()
        self.c = Client(addr)
        self._c_handle_connect, self._c_handle_close = self.c.handle_connect, self.c.handle_close
        self.c.handle_connect, self.c.handle_close = self._handle_connect, self._handle_close

    @property
    def cid(self):
        return self.c.id

    def connect(self):
        if self.backend:
            init_loop()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.c.say(msg_bytes)

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

        msg_bytes = self.c.read_message()
        for m in self.prot.input(msg_bytes):
            yield m

    def update(self):
        if not self.backend:
            asyncore.loop(timeout=0.0, count=1)

    def close(self):
        self.c.close()

    def _handle_connect(self):
        self._c_handle_connect()
        self.msg_queue.append(ClientOnConnectMessage())

    def _handle_close(self):
        self._c_handle_close()
        self.msg_queue.append(ClientOnCloseMessage())
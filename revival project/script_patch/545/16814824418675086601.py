# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/ws/main.py
from collections import deque
from .websocket_server import WebsocketServer as BaseWsServer
from ..interfaces import IServer, IConnection, ServerOnConnectMessage, ServerOnCloseMessage
DEFAULT_ADDR = ('localhost', 5003)

class ClientWrapper(object):

    def __init__(self, client):
        self.cid = client['id']
        self.addr = client['address']
        self.handler = client['handler']


class WebsocketConn(IConnection):

    def __init__(self, client):
        super(WebsocketConn, self).__init__()
        self.client = ClientWrapper(client)
        self.messages = deque()

    def addMessage(self, msg):
        self.messages.append(msg)

    def send(self, msg):
        self.client.handler.send_message(msg)

    def recv(self):
        while self.messages:
            yield self.messages.popleft().encode('utf-8')

    @property
    def handler(self):
        return self.client.handler

    @property
    def cid(self):
        return self.client.cid


class WebSocketServer(IServer):

    def __init__(self, addr=DEFAULT_ADDR):
        super(WebSocketServer, self).__init__()
        self.msg_queue = deque()
        self._connections = {}
        self._addr = addr
        self._initServer()
        self._server = None
        return

    def start(self):
        import threading
        t = threading.Thread(target=self.s.run_forever)
        t.daemon = True
        t.start()
        self._server = self.s

    def close(self):
        self.s.server_close()

    def close_client(self, cid):
        conn = self._connections.pop(cid)
        handler = conn.handler
        handler.connection.close()
        self.msg_queue.append((conn, ServerOnCloseMessage()))

    def _initServer(self):
        self.s = BaseWsServer(self._addr[1], self._addr[0])
        self.s.set_fn_new_client(self._onNewClient)
        self.s.set_fn_message_received(self._onMessageReceived)
        self.s.set_fn_client_left(self._onClientClosed)

    def _onNewClient(self, client, server):
        conn = WebsocketConn(client)
        self._connections[conn.cid] = conn
        self.msg_queue.append((conn, ServerOnConnectMessage()))

    def _onClientClosed(self, client, server):
        conn = self._connections.pop(client['id'])
        self.msg_queue.append((conn, ServerOnCloseMessage()))

    def _onMessageReceived(self, client, server, message):
        self._connections[client['id']].addMessage(message)

    @property
    def addr(self):
        return self._addr

    @property
    def connections(self):
        return self._connections

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

        buf = []
        for cid in self._connections:
            conn = self._connections[cid]
            for msg in conn.recv():
                buf.append((conn, msg))

        for i in buf:
            yield i

    def update(self):
        pass
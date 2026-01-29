# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/direct/main.py
from ..... import PY2
if PY2:
    from Queue import Queue
else:
    from queue import Queue
from ..interfaces import IServer, IClient, IConnection, ServerOnConnectMessage, ServerOnCloseMessage, ClientOnConnectMessage, ClientOnCloseMessage

class DirectConnection(IConnection):

    def __init__(self, other, callback=None):
        self._cid = other.cid
        self.other = other
        self.callback = callback
        self.buffer = []

    def send(self, msg):
        self.other.on_direct_send(msg)

    def recv(self):
        ret, self.buffer = self.buffer, []
        return ret

    def close(self):
        self.other.close()
        self.other = None
        self._cid = None
        self.callback = None
        return

    def on_direct_send(self, msg):
        if self.callback:
            self.callback(self, msg)
        else:
            self.buffer.append(msg)

    @property
    def cid(self):
        return self._cid

    def __str__(self):
        return '<DirectConn: %s>' % repr(self._cid)

    __repr__ = __str__


class DirectClient(IClient):

    def __init__(self, cid, other, callback=None):
        self._cid = cid
        self.other = other
        self.otherConn = None
        self.callback = callback
        self.buffer = []
        return

    def send(self, msg):
        self.otherConn.on_direct_send(msg)

    def recv(self):
        ret, self.buffer = self.buffer, []
        return ret

    @property
    def cid(self):
        return self._cid

    def connect(self, other=None):
        if other:
            self.other = other
        if not self.other:
            return
        self.other.on_client_connect(self)
        if self.callback:
            self.callback(self, ClientOnConnectMessage())
        else:
            self.buffer.append(ClientOnConnectMessage())

    def update(self):
        pass

    def close(self):
        self.other.on_client_close(self)
        self.otherConn = None
        self.other = None
        if self.callback:
            self.callback(self, ClientOnCloseMessage())
        else:
            self.buffer.append(ClientOnCloseMessage())
        return

    def on_direct_send(self, msg):
        if self.callback:
            self.callback(self, msg)
        else:
            self.buffer.append(msg)


class DirectServerClient(DirectClient):

    def on_client_connect(self, client):
        self.other = client
        self.otherConn = client
        client.otherConn = self
        client.other = self
        if self.callback:
            self.callback(self, ClientOnConnectMessage())
        else:
            self.buffer.append(ClientOnConnectMessage())

    def on_client_close(self, client):
        self.other = None
        self.otherConn = None
        if self.callback:
            self.callback(self, ClientOnCloseMessage())
        else:
            self.buffer.append(ClientOnCloseMessage())
        return

    def close(self):
        self.other.close()


class DirectServer(IServer):

    def __init__(self, callback=None):
        self._connections = {}
        self.callback = callback
        self.queue = Queue()

    @property
    def connections(self):
        return self._connections

    def start(self):
        pass

    def update(self):
        pass

    def recv(self):
        while self.queue:
            yield self.queue.get_nowait()

        buf = []
        for cid, conn in self._connections.items():
            for msg in conn.recv():
                buf.append((conn, msg))

        for i in buf:
            yield i

    def close(self):
        for cid in list(self._connections.keys()):
            self._connections[cid].close()

    def on_client_connect(self, client):
        conn = DirectConnection(client, self.callback)
        client.otherConn = conn
        self._connections[client.cid] = conn
        if self.callback:
            self.callback(conn, ServerOnConnectMessage())
        else:
            self.queue.put((conn, ServerOnConnectMessage()))

    def on_client_close(self, client):
        conn = self._connections.pop(client.cid)
        if self.callback:
            self.callback(conn, ServerOnCloseMessage())
        else:
            self.queue.put((conn, ServerOnCloseMessage()))
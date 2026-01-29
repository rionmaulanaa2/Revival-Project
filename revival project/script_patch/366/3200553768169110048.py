# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/rmq/main.py
from collections import deque
from ..interfaces import IServer, IClient, IConnection, ServerOnConnectMessage, ServerOnCloseMessage, ClientOnConnectMessage, ClientOnCloseMessage
from .RmqRPC import RmqRPCClient, RmqRPCServer

class SSRmqConn(IConnection):

    def __init__(self, cid, sh):
        self.cid = cid
        self.sh = sh
        self.inbox = []

    def on_message(self, message):
        self.inbox.append(message)

    def send(self, msg):
        self.sh.send(msg, self.cid)

    def recv(self):
        msgs, self.inbox = self.inbox, []
        return msgs

    def __str__(self):
        return '<SSRmqConn: %s>' % repr(self.cid)

    __repr__ = __str__


class SSRmqServer(RmqRPCServer, IServer):

    def __init__(self, url, serverId, backend=False):
        RmqRPCServer.__init__(self, url, serverId, backend)
        self.msg_queue = deque()
        self.online_clients = {}

    def on_message(self, sender, message):
        conn = self.online_clients.get(sender)
        if not conn:
            conn = SSRmqConn(sender, self)
            self.online_clients[sender] = conn
            self.msg_queue.append((conn, ServerOnConnectMessage()))
        conn.on_message(message)

    def start(self):
        if self.backend:
            self.run_backend()

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

        buf = []
        for cid, conn in self.online_clients.items():
            for msg in conn.recv():
                buf.append((conn, msg))

        for i in buf:
            yield i

    @property
    def connections(self):
        return self.online_clients

    def update(self):
        self.tick()


class SSRmqClient(RmqRPCClient, IClient):

    def __init__(self, url, serverId, backend=False):
        RmqRPCClient.__init__(self, url, serverId, backend)
        self.msg_queue = deque()
        self.msg_queue.append(ClientOnConnectMessage())
        self.inbox = []

    def on_message(self, sender, message):
        self.inbox.append(message)

    def connect(self):
        if self.backend:
            self.run_backend()

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

        msgs, self.inbox = self.inbox, []
        for m in msgs:
            yield m

    def update(self):
        self.tick()
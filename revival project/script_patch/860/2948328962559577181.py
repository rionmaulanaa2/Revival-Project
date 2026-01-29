# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/redis/main.py
from collections import deque
import uuid
from ..interfaces import IServer, IConnection, OnMessage
from .RedisRPC import RedisMqClient

class SSRedisMqConn(IConnection):

    def __init__(self, reply, sh):
        self.reply = reply
        self.sh = sh
        self.inbox = []

    def on_message(self, message):
        self.inbox.append(message)

    def send(self, msg):
        if self.reply is not None:
            self.sh.send(self.reply, msg)
        return

    def recv(self):
        msgs, self.inbox = self.inbox, []
        return msgs

    def __str__(self):
        return '<SSRedisMqConn: {}'.format(self.reply)

    __repr__ = __str__


class SSRedisMqServer(RedisMqClient, IServer):

    def __init__(self, conn, channelListen, backend=False):
        RedisMqClient.__init__(self, conn, backend, channelListen)
        self.msg_queue = deque()

    def on_message(self, message, reply_queue=None):
        conn = SSRedisMqConn(reply_queue, self)
        self.msg_queue.append((conn, OnMessage()))
        conn.on_message(message)

    def start(self):
        if self.backend:
            self.run_backend()

    def recv(self):
        while self.msg_queue:
            yield self.msg_queue.popleft()

    def send(self, channel, data, need_reply=False):
        reply = None
        if need_reply:
            reply = uuid.uuid4().hex
        self._redisPublish(channel, data, reply)
        return

    @property
    def connections(self):
        return {}

    def update(self):
        self.tick()
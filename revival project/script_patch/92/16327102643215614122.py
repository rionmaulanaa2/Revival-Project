# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/RedisRpc.py
from .simplerpc.simplerpc import RpcAgent
from .simplerpc.transport.redis.main import SSRedisMqServer
from .simplerpc.transport.interfaces import OnMessage

class RedisRPC(RpcAgent):

    def __init__(self, conn, channelListen):
        super(RedisRPC, self).__init__()
        self.server = SSRedisMqServer(conn, channelListen)
        self.server.start()

    def add_method(self, func, name=None):

        def rpc_wrapper(f):

            def wrapper(context, *args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        super(RedisRPC, self).add_method(rpc_wrapper(func), name or func.__name__)

    def update(self):
        self.server.update()
        for conn, event in self.server.recv():
            if isinstance(event, OnMessage):
                for msg in conn.recv():
                    self.handle_message(msg, conn)

        super(RedisRPC, self).update()

    def call(self, channel, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        self.server.send(channel, req)
        return cb

    def call_with_reply(self, channel, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        self.server.send(channel, req, True)
        return cb

    def close(self):
        self.server.close()
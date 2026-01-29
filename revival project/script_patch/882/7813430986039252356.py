# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/interfaces.py


class IConnection(object):

    def send(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

    @property
    def cid(self):
        raise NotImplementedError


class IClient(IConnection):

    def connect(self):
        raise NotImplementedError

    def update(self):
        pass

    def close(self):
        pass


class IServer(object):

    @property
    def connections(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def broadcast(self, msg):
        for conn in self.connections.values():
            conn.send(msg)

    def update(self):
        pass

    def close(self):
        pass

    def close_client(self, cid):
        raise NotImplementedError


class IMessage(object):
    pass


class ClientOnConnectMessage(IMessage):
    pass


class ClientOnCloseMessage(IMessage):
    pass


class ServerOnConnectMessage(IMessage):
    pass


class ServerOnCloseMessage(IMessage):
    pass


class OnMessage(IMessage):
    pass
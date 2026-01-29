# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/SunshineRpc.py
from functools import partial
from .Proxy import ServerProxy, plugin_method
from .simplerpc.rpcclient import RpcClient, ClientContext
from .simplerpc.rpcserver import RpcServer, ServerContext
from .Event import Event
from .Decorator import REMOTE_NAMES, UNKNOWN
from .simplerpc.jsonrpc.exceptions import *
from .simplerpc.simplerpc import AsyncResponse

def _rpc_method_wrapper(handler, func, context, *args, **kwargs):
    if not handler:
        return func(*args, **kwargs)
    else:
        context.uuid = handler.SUNSHINE_UUID
        handler.Context = context
        res = func(*args, **kwargs)
        handler.Context = None
        return res


class SSRpcClientContext(ClientContext):

    def __init__(self, rid, method, params, agent, peerType):
        super(SSRpcClientContext, self).__init__(rid, method, params, agent)
        self.peerType = peerType
        self.uuid = None
        return

    def peer_info(self):
        return '<%s> at remote' % REMOTE_NAMES[self.peerType]

    def call_peer(self, func, *args, **kwargs):
        if self.uuid:
            func = plugin_method(self.uuid, func)
        return super(SSRpcClientContext, self).call_peer(func, *args, **kwargs)


class SSRpcClient(RpcClient):

    def __init__(self, conn, eventMode=False, twoStepConnection=False, clientInfo=None, protocol='json'):
        super(SSRpcClient, self).__init__(conn, eventMode, twoStepConnection, clientInfo, protocol)
        self.proxy = ServerProxy(self.call)
        self.EventRPCReady = Event()
        self.EventRPCClosed = Event()
        self._rpcCache = []
        self._remotePeerType = UNKNOWN

    @property
    def remote_peer_type(self):
        return self._remotePeerType

    @remote_peer_type.setter
    def remote_peer_type(self, tp):
        self._remotePeerType = tp

    def on_connect(self):
        super(SSRpcClient, self).on_connect()
        while self._rpcCache:
            self.conn.send(self._rpcCache.pop(0))

        self.EventRPCReady()

    def on_close(self):
        self.EventRPCClosed()
        super(SSRpcClient, self).on_close()

    def add_method(self, func, name=None, handler=None):
        super(SSRpcClient, self).add_method(partial(_rpc_method_wrapper, handler, func), name)

    def call(self, func, *args, **kwargs):
        if self._status == self.CONNECTING:
            req, cb = self.format_request(func, *args, **kwargs)
            self._rpcCache.append(req)
            return cb
        else:
            return super(SSRpcClient, self).call(func, *args, **kwargs)

    def create_context(self, conn, data):
        return SSRpcClientContext(data['id'], data['method'], data['params'], self, self._remotePeerType)


class SSRpcServerContext(ServerContext):

    def __init__(self, rid, method, params, cid, agent, clientInfo, peerType):
        super(SSRpcServerContext, self).__init__(rid, method, params, cid, agent, clientInfo)
        self.peerType = peerType
        self.uuid = None
        return

    @property
    def clientUuid(self):
        if self.clientInfo and 'uuid' in self.clientInfo:
            return self.clientInfo['uuid']
        return self.cid

    def peer_info(self):
        return '<%s %s> at remote' % (REMOTE_NAMES[self.peerType], self.clientUuid)

    def call_peer(self, func, *args, **kwargs):
        if self.uuid:
            func = plugin_method(self.uuid, func)
        return super(SSRpcServerContext, self).call_peer(func, *args, **kwargs)


class SSRpcServer(RpcServer):

    def __init__(self, server, manager, eventMode=False, twoStepConnection=False, protocol='json'):
        super(SSRpcServer, self).__init__(server, eventMode, twoStepConnection, protocol)
        self.manager = manager
        self.manager.rpcServer = self
        self.manager.set_cache_func(self._cache_rpc_call)
        self._rpcCache = []
        self.EventMainRPCReady = Event()
        self.EventMainRPCClosed = Event()
        self.EventClientRPCReady = Event()
        self.EventClientRPCClosed = Event()
        self._remotePeerType = None
        return

    @property
    def remote_peer_type(self):
        return self._remotePeerType

    @remote_peer_type.setter
    def remote_peer_type(self, tp):
        self._remotePeerType = tp

    def on_client_connect(self, conn):
        super(SSRpcServer, self).on_client_connect(conn)
        cid = conn.cid
        clientInfo = self._clientInfoMap.get(cid, None)
        uuid = clientInfo['uuid'] if clientInfo and 'uuid' in clientInfo else cid
        isMainAgent = self.manager.count() == 0
        self.manager.on_new_connect(uuid, partial(self.call, cid))
        clientProxy = self.manager.get_client_proxy(uuid)
        self.EventClientRPCReady(clientProxy)
        if isMainAgent:
            while self._rpcCache:
                req = self._rpcCache.pop(0)
                conn.send(req)

            self.EventMainRPCReady()
        return

    def on_client_close(self, conn):
        super(SSRpcServer, self).on_client_close(conn)
        cid = conn.cid
        clientInfo = self._clientInfoMap.get(cid, None)
        uuid = clientInfo['uuid'] if clientInfo and 'uuid' in clientInfo else cid
        clientProxy = self.manager.get_client_proxy(uuid)
        self.EventClientRPCClosed(clientProxy)
        self.manager.on_lose_connect(uuid)
        if self.manager.get_main_client_proxy() is None:
            self.EventMainRPCClosed()
        return

    def _cache_rpc_call(self, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        self._rpcCache.append(req)
        return cb

    def add_method(self, func, name=None, handler=None):
        super(SSRpcServer, self).add_method(partial(_rpc_method_wrapper, handler, func), name)

    def create_context(self, conn, data):
        return SSRpcServerContext(data['id'], data['method'], data['params'], conn.cid, self, self._clientInfoMap.get(conn.cid, None), self._remotePeerType)

    def get_client(self, cid):
        return self.server.connections.get(cid, None)
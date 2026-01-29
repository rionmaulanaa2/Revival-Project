# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/Proxy.py
from .simplerpc.jsonrpc.exceptions import JSONRPCRemoteException
from .simplerpc.transport.direct import DirectClient
from .simplerpc.transport.interfaces import ClientOnCloseMessage, ClientOnConnectMessage
from .simplerpc.rpcclient import RpcClient
from .simplerpc.transport.tcp import TcpClient
from .. import PY3
if PY3:
    from asyncio.futures import Future
    from asyncio import TimeoutError
    import asyncio

    class CompatFuture(Future):

        def __init__(self, cb=None, loop=None):
            if loop is None:
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()

            super(CompatFuture, self).__init__(loop=loop)
            self._cb = None
            self._callback = None
            self._errorCb = None
            self._timeout = 0
            self._timeoutCb = None
            if cb:
                self._setupCb(cb)
            self._log_traceback = False
            return

        def _setupCb(self, cb):
            self._cb = cb
            self._cb.on_result(self._on_result)
            self._cb.on_error(self._on_error)
            if self._timeout > 0:
                self._cb.timeout(self._timeout)
            self._cb.on_timeout(self._on_timeout)

        def _on_result(self, result):
            if self.done():
                self._clear()
                return
            self.set_result(result)
            if self._callback:
                self._callback(result)
            self._clear()

        def on_result(self, cb):
            self._callback = cb
            return self

        def _on_error(self, error):
            if self.done():
                self._clear()
                return
            self.set_exception(JSONRPCRemoteException(error))
            if self._errorCb:
                self._errorCb(error)
            self._clear()

        def on_error(self, cb):
            self._errorCb = cb
            return self

        def _on_timeout(self):
            if self.done():
                self._clear()
                return
            self.set_exception(TimeoutError('RPC call to %s has expired.' % self._cb.func))
            if self._timeoutCb:
                self._timeoutCb()
            self._clear()

        def timeout(self, expire):
            self._timeout = expire
            if self._cb:
                self._cb.timeout(expire)
            return self

        def on_timeout(self, cb):
            self._timeoutCb = cb
            return self

        def cancel(self):
            self._clear()
            super(CompatFuture, self).cancel()

        def _clear(self):
            self._log_traceback = False
            self._callback = None
            self._errorCb = None
            self._timeoutCb = None
            self._cb = None
            return

        def wait(self):
            pass


def plugin_method(pluginid, method):
    return '_%s_%s' % (pluginid, method)


class Proxy(object):

    def __init__(self, rpcCall):
        self.rpcCall = rpcCall

    def call(self, *args, **kwargs):
        timeout = kwargs.pop('timeout', 0)
        cb = self.rpcCall(*args, **kwargs)
        if PY3:
            future = CompatFuture(cb)
            if timeout > 0:
                future.timeout(timeout)
            return future
        else:
            return cb

    def call_with_future(self, future, *args, **kwargs):
        timeout = kwargs.pop('timeout', 0)
        cb = self.rpcCall(*args, **kwargs)
        if future:
            if timeout > 0:
                future.timeout(timeout)
            future._setupCb(cb)
            return future
        else:
            return cb

    def call_plugin_method(self, uuid, method, *args, **kwargs):
        return self.call(plugin_method(uuid, method), *args, **kwargs)


class PluginProxy(object):

    def __init__(self, uuid, proxy):
        self.uuid = uuid
        self.proxy = proxy
        self.cachedCalls = []

    def CallRPC(self, funcname, *args, **kwargs):
        plugin_funcname = '_%s_%s' % (self.uuid, funcname)
        if not self.proxy:
            if PY3:
                future = CompatFuture()
            else:
                future = None
            self.cachedCalls.append((plugin_funcname, args, kwargs, future))
            return future
        else:
            return self.proxy.call(plugin_funcname, *args, **kwargs)

    def SendCachedRPC(self):
        while self.cachedCalls:
            funcname, args, kwargs, future = self.cachedCalls.pop(0)
            self.proxy.call_with_future(future, funcname, *args, **kwargs)

    def __getattr__(self, funcname):

        def _call(*args, **kwargs):
            return self.CallRPC(funcname, *args, **kwargs)

        return _call


class ClientProxy(Proxy):

    def __init__(self, cid, rpcCall):
        super(ClientProxy, self).__init__(rpcCall)
        self.cid = cid


class ClientProxyManager(object):

    def __init__(self):
        self._proxyMap = {}
        self._mainProxy = None
        self._cacheProxy = None
        self._rpcServer = None
        return

    @property
    def rpcServer(self):
        return self._rpcServer

    @rpcServer.setter
    def rpcServer(self, server):
        self._rpcServer = server

    def set_cache_func(self, func):
        self._cacheProxy = ClientProxy(None, func)
        return

    def get_cache_proxy(self):
        return self._cacheProxy

    def on_new_connect(self, cid, rpcCall):
        clientProxy = ClientProxy(cid, rpcCall)
        self._proxyMap[cid] = clientProxy
        if not self._mainProxy:
            self._mainProxy = clientProxy

    def on_lose_connect(self, cid):
        if cid not in self._proxyMap:
            return
        else:
            proxy = self._proxyMap[cid]
            del self._proxyMap[cid]
            if proxy is self._mainProxy:
                self._mainProxy = None
                print 'Main client changed!!!'
                if self._proxyMap:
                    for p in self._proxyMap.values():
                        self._mainProxy = p
                        break

            return

    def get_client_proxy(self, cid):
        return self._proxyMap.get(cid, None)

    def get_all_client_proxy(self):
        return self._proxyMap

    def set_main_client_proxy(self, cid):
        self._mainProxy = self._proxyMap[cid]

    def get_main_client_proxy(self):
        return self._mainProxy

    def get_main_client_id(self):
        if self._mainProxy:
            return self._mainProxy.cid
        else:
            return None

    def count(self):
        return len(self._proxyMap)


class ClientPluginProxy(PluginProxy):
    DEFAULT_VERSION = (0, 0, 0)

    def __init__(self, uuid, manager=None, clientProxy=None):
        super(ClientPluginProxy, self).__init__(uuid, clientProxy)
        self._manager = manager
        self.__cid = None
        self._clientMetaData = {}
        if manager and manager.rpcServer:
            manager.rpcServer.EventClientRPCReady += self._FetchClientMetaData
        return

    def _FetchClientMetaData(self, clientProxy):

        def on_result--- This code section failed: ---

 250       0  LOAD_CONST            1  'apiVersion'
           3  LOAD_FAST             0  'v'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    48  'to 48'

 251      12  LOAD_GLOBAL           0  'tuple'
          15  LOAD_GENEXPR             '<code_object <genexpr>>'
          18  MAKE_FUNCTION_0       0 
          21  MAKE_FUNCTION_1       1 
          24  BINARY_SUBSCR    
          25  LOAD_ATTR             1  'split'
          28  LOAD_CONST            3  '.'
          31  CALL_FUNCTION_1       1 
          34  GET_ITER         
          35  CALL_FUNCTION_1       1 
          38  CALL_FUNCTION_1       1 
          41  CALL_FUNCTION_1       1 
          44  STORE_SUBSCR     
          45  JUMP_FORWARD          0  'to 48'
        48_0  COME_FROM                '45'

 252      48  LOAD_FAST             0  'v'
          51  LOAD_DEREF            0  'self'
          54  LOAD_ATTR             2  '_clientMetaData'
          57  LOAD_DEREF            1  'clientProxy'
          60  LOAD_ATTR             3  'cid'
          63  STORE_SUBSCR     

Parse error at or near `MAKE_FUNCTION_1' instruction at offset 21

        self._clientMetaData[clientProxy.cid] = {}
        self.CallClient(clientProxy.cid, 'GetPluginClientMetaData').on_result(on_result)

    def getClientProxy(self):
        return self.proxy

    def CallRPC(self, funcname, *args, **kwargs):
        proxy = self.proxy or self._manager.get_main_client_proxy() or self._manager.get_cache_proxy()
        if proxy is not None:
            return proxy.call_plugin_method(self.uuid, funcname, *args, **kwargs)
        else:
            return

    CallMainRPC = CallRPC

    def CallAllClients(self, funcname, *args, **kwargs):
        return [ proxy.call_plugin_method(self.uuid, funcname, *args, **kwargs) for proxy in self._manager.get_all_client_proxy().values() ]

    def CallClient(self, cid, funcname, *args, **kwargs):
        proxy = self._manager.get_client_proxy(cid)
        return proxy.call_plugin_method(self.uuid, funcname, *args, **kwargs)

    def __getattr__(self, funcname):

        def _call(*args, **kwargs):
            if self.__cid is not None:
                cid = self.__cid
                self.__cid = None
                return self.CallClient(cid, funcname, *args, **kwargs)
            else:
                return self.CallMainRPC(funcname, *args, **kwargs)

        return _call

    def __getitem__(self, cid):
        self.__cid = cid
        return self

    def RegisterRPCHandler(self, handler):
        handler.ClientStub = self
        self._manager.rpcServer.EventMainRPCReady += handler.OnPluginReady
        self._manager.rpcServer.EventMainRPCClosed += handler.OnPluginClose
        mainProxy = self._manager.get_main_client_proxy()
        if mainProxy:
            self._FetchClientMetaData(mainProxy)
            handler.OnPluginReady()
        import inspect
        methods = inspect.getmembers(handler, predicate=inspect.ismethod)
        for name, method in methods:
            if name.startswith('_'):
                continue
            plugin_method_name = plugin_method(handler.SUNSHINE_UUID, name)
            self._manager.rpcServer.add_method(method, plugin_method_name, handler)

    def GetClientMetaData(self, cid=None):
        if cid is None:
            cid = self._manager.get_main_client_id()
        return self._clientMetaData.get(cid, None)

    def GetClientAPIVersion(self, cid=None):
        if cid is None:
            cid = self._manager.get_main_client_id()
        if cid not in self._clientMetaData:
            return self.DEFAULT_VERSION
        else:
            return self._clientMetaData[cid].get('apiVersion', self.DEFAULT_VERSION)


class ServerProxy(Proxy):
    pass


class ServerPluginProxy(PluginProxy):

    def RegisterPluginClient(self, plugin, callServer):
        pass


class GameServerProxy(Proxy):
    pass


class GameClientProxy(ClientProxy):
    pass


class GameServerPluginProxy(ServerPluginProxy):
    pass


class GameClientPluginProxy(ClientPluginProxy):
    pass


class GameBridgeClient(object):

    def __init__(self, avatarId, callback):
        self.conn = DirectClient(avatarId, None, self._on_message)
        self.callback = callback
        return

    def connect(self, server):
        self.conn.other = server
        self.conn.connect()

    def close(self):
        self.conn.close()

    def send(self, msg):
        self.conn.send(msg)

    def update(self):
        pass

    def _on_message(self, _, msg):
        if isinstance(msg, ClientOnConnectMessage):
            print 'game bridge client connected'
        elif isinstance(msg, ClientOnCloseMessage):
            print 'game bridget client closed'
        else:
            self.callback(msg)


class StandaloneGameBridgeClient(RpcClient):

    def __init__(self, sunshineClient, serverAddr, clientInfo=None):
        super(StandaloneGameBridgeClient, self).__init__(TcpClient(serverAddr), twoStepConnection=True, clientInfo=clientInfo)
        self._id = -100000
        self.sunshineClient = sunshineClient
        self.bridgeConn = DirectClient(None, None, self._on_message)
        return

    def _on_message(self, _, msg):
        if not isinstance(msg, (ClientOnConnectMessage, ClientOnCloseMessage)):
            self.conn.send(msg)

    def handle_message(self, msg, conn):
        data = self._decode_message(msg)
        if 'method' not in data and data['id'] in self._callbacks:
            callback = self._callbacks.pop(data['id'])
            if 'result' in data:
                callback.rpc_result(data['result'])
            elif 'error' in data:
                callback.rpc_error(data['error'])
        else:
            self.bridgeConn.send(msg)

    def on_connect(self):
        super(StandaloneGameBridgeClient, self).on_connect()
        self.sunshineClient.ConnectGame(self.bridgeConn)

    def on_close(self):
        super(StandaloneGameBridgeClient, self).on_close()
        self.bridgeConn.close()
        self.bridgeConn = None
        self.sunshineClient = None
        return
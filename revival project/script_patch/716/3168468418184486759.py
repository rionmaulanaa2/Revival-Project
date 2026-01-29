# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineClient.py
from .SunshineRpc.Proxy import ServerPluginProxy, GameClientPluginProxy, GameServerPluginProxy, GameServerProxy, ClientProxyManager, plugin_method
from .SunshineRpc.Decorator import SERVER, GAME_CLIENT, GAME_SERVER
from . import LocalRpc
CONNECT_TYPE_SIMPLERPC = 1
CONNECT_TYPE_LOCAL = 2
SDK_CLIENT, SDK_SERVER = ('SDK_CLIENT', 'SDK_SERVER')
DEFAULT_SUNSHINE_ADDRESS = {SDK_CLIENT: ('127.0.0.1', 29102)
   }
DEFAULT_RMQ_URL = 'amqp://myuser:163a163@@59.111.129.112:5672/parasite'
SUNSHINE_CLIENT_INST = None

def GetSunshineClient():
    global SUNSHINE_CLIENT_INST
    return SUNSHINE_CLIENT_INST


class Response(object):

    def __init__(self, uuid, methodName, *args):
        self.uuid = uuid
        self.methodName = methodName
        self.args = args


class SunshineClient(object):

    def __init__(self, connectType=CONNECT_TYPE_SIMPLERPC, agentType=SDK_CLIENT, standaloneServer=False, rpcSerializeProtocol='json'):
        global SUNSHINE_CLIENT_INST
        SUNSHINE_CLIENT_INST = self
        self.connectType = connectType
        self.agentType = agentType
        self.rpcProtocol = rpcSerializeProtocol
        self._standaloneServer = standaloneServer
        self.address = None
        self._plugins = {}
        self.updateCallbacks = []
        self.readyCallbacks = []
        self.closeCallbacks = []
        self.gameInfo = {}
        self._RpcAgent = None
        self._serverProxy = None
        self._gameBridgeServer = None
        self._gameServerProxy = None
        self._gameClientProxyManager = None
        return

    def RegisterPlugin(self, editorPlugin):
        self._plugins[editorPlugin.PLUGIN_NAME] = editorPlugin
        if self.connectType == CONNECT_TYPE_SIMPLERPC:
            editorPlugin.Server = ServerPluginProxy(editorPlugin.SUNSHINE_UUID, None)
        else:
            editorPlugin.Server = LocalRpc.LocalRpcManager.get_plugin_server(editorPlugin.SUNSHINE_UUID)
        if self.agentType == SDK_CLIENT:
            editorPlugin.GameServer = GameServerPluginProxy(editorPlugin.SUNSHINE_UUID, None)
        elif self.agentType == SDK_SERVER:
            editorPlugin.GameClient = GameClientPluginProxy(editorPlugin.SUNSHINE_UUID, None)
        return

    def Connect(self, address=None):
        if 'Atmosphere' not in self._plugins:
            from .Plugin.AtmospherePlugin.AtmospherePluginClient import AtmospherePluginClient
            self.RegisterPlugin(AtmospherePluginClient())
        if self.connectType == CONNECT_TYPE_LOCAL:
            self._RpcAgent = LocalRpc.LocalRpcClient()
        elif self.connectType == CONNECT_TYPE_SIMPLERPC:
            if self._RpcAgent:
                print '[WARNING] Sunshine has already connected!'
                return
            if self.agentType == SDK_CLIENT:
                if not address:
                    address = DEFAULT_SUNSHINE_ADDRESS[self.agentType]
                from .SunshineRpc.SunshineRpc import SSRpcClient
                from .SunshineRpc.simplerpc.transport.tcp import TcpClient
                from .SunshineRpc.simplerpc.transport.direct import DirectServerClient
                self._RpcAgent = SSRpcClient(TcpClient(address), protocol=self.rpcProtocol)
                self._RpcAgent.remote_peer_type = SERVER
                self._RpcAgent.EventRPCReady += self._OnRPCReady
                self._RpcAgent.EventRPCClosed += self._OnRPCClose
                self._serverProxy = self._RpcAgent.proxy
                self.address = address
                self._gameBridgeServer = SSRpcClient(DirectServerClient(None, None), True, protocol=self.rpcProtocol)
                self._gameBridgeServer.remote_peer_type = GAME_SERVER
                self._gameBridgeServer.dispatcher = self._RpcAgent.dispatcher
                self._gameServerProxy = GameServerProxy(self._gameBridgeServer.call)
            elif self.agentType == SDK_SERVER:
                from .SunshineRpc.SunshineRpc import SSRpcServer
                if self._standaloneServer:
                    from .SunshineRpc.simplerpc.transport.tcp import TcpServer
                    self._RpcAgent = SSRpcServer(TcpServer(address), ClientProxyManager(), twoStepConnection=True)
                    self.address = address
                else:
                    from .SunshineRpc.simplerpc.transport.direct import DirectServer
                    self._RpcAgent = SSRpcServer(DirectServer(), ClientProxyManager(), True)
                self._RpcAgent.remote_peer_type = GAME_CLIENT
                self._RpcAgent.EventMainRPCClosed += self._OnRPCClose
                self._gameClientProxyManager = self._RpcAgent.manager
                self._gameBridgeServer = self._RpcAgent

            def _postCallInterceptor(agent, result, conn):
                if 'result' in result:
                    response = result['result']
                    responses = []
                    if isinstance(response, Response):
                        responses = [
                         response]
                    else:
                        if isinstance(response, (tuple, list)):
                            if any((isinstance(k, Response) for k in response)):
                                responses = response
                        for res in responses:
                            try:
                                respStr, _ = agent.format_request(plugin_method(res.uuid, res.methodName), *res.args)
                            except TypeError:
                                print '[RPC ERROR] Fail to serialize response, uuid=%s, method=%s, args=%s' % (res.uuid, res.methodName, res.args)
                            else:
                                conn.send(respStr)

                        if responses:
                            return True
                return False

            self._RpcAgent.add_post_call_interceptor(_postCallInterceptor)
        for uuid, editorPlugin in self._plugins.items():
            methodMap = editorPlugin.Register()
            for uuid_name, method in methodMap.items():
                plugin_funcname = '_%s_%s' % uuid_name
                if self.connectType == CONNECT_TYPE_SIMPLERPC:
                    self._RpcAgent.add_method(method, plugin_funcname, editorPlugin)
                elif self.connectType == CONNECT_TYPE_LOCAL:
                    dispatcher = LocalRpc.LocalRpcManager.CLIENT_METHOD_DISPATCHER
                    dispatcher[plugin_funcname] = method

            if self.connectType == CONNECT_TYPE_SIMPLERPC:
                editorPlugin.Server.proxy = self._serverProxy
                if self.agentType == SDK_CLIENT:
                    editorPlugin.GameServer.proxy = self._gameServerProxy
                    if self._RpcAgent.status == self._RpcAgent.CONNECTED:
                        editorPlugin.OnPluginReady()
                elif self.agentType == SDK_SERVER:
                    editorPlugin.GameClient._manager = self._gameClientProxyManager
            elif self.connectType == CONNECT_TYPE_LOCAL:
                editorPlugin.OnPluginReady()

        return

    def ConnectGame(self, conn):
        if self.agentType == SDK_CLIENT:
            conn.connect(self._gameBridgeServer.conn)
        else:
            conn.connect(self._gameBridgeServer.server)

    def Close(self):
        if self.connectType == CONNECT_TYPE_SIMPLERPC:
            if self._RpcAgent:
                self._RpcAgent.close()

    def _OnRPCReady(self):
        for plugin in self._plugins.values():
            plugin.OnPluginReady()

        if self.readyCallbacks:
            for readyCallback in self.readyCallbacks:
                readyCallback()

    def _OnRPCClose(self):
        if self.connectType == CONNECT_TYPE_SIMPLERPC:
            if self.agentType == SDK_CLIENT:
                self._RpcAgent.EventRPCClosed -= self._OnRPCClose
                self._RpcAgent = None
        for plugin in self._plugins.values():
            plugin.OnPluginClose()

        if self._gameBridgeServer and self.agentType == SDK_CLIENT:
            if self._gameBridgeServer.status == self._gameBridgeServer.CONNECTED:
                self._gameBridgeServer.close()
            self._gameBridgeServer = None
        if self.closeCallbacks:
            for closeCallback in self.closeCallbacks:
                closeCallback()

        return

    def RegisterReadyCallback(self, callback):
        if callback not in self.readyCallbacks:
            self.readyCallbacks.append(callback)

    def UnregisterReadyCallback(self, callback):
        if callback in self.readyCallbacks:
            self.readyCallbacks.remove(callback)

    def RegisterCloseCallback(self, callback):
        if callback not in self.closeCallbacks:
            self.closeCallbacks.append(callback)

    def UnregisterCloseCallback(self, callback):
        if callback in self.closeCallbacks:
            self.closeCallbacks.remove(callback)

    def RegisterUpdateCallback(self, callback):
        if callback not in self.updateCallbacks:
            self.updateCallbacks.append(callback)

    def UnregisterUpdateCallback(self, callback):
        if callback in self.updateCallbacks:
            self.updateCallbacks.remove(callback)

    def Update(self):
        if self.connectType == CONNECT_TYPE_SIMPLERPC and self._RpcAgent:
            self._RpcAgent.update()
        for callback in self.updateCallbacks:
            callback()

    def GetPlugin(self, pluginName):
        return self._plugins.get(pluginName)

    def SetGameInfo(self, tag, val):
        self.gameInfo[tag] = val
        self._plugins['Atmosphere'].Server.UpdateGameInfo(self.gameInfo, tag)

    @property
    def RpcAgent(self):
        return self._RpcAgent

    @staticmethod
    def SetGameEncoding(encoding):
        from .SunshineRpc.simplerpc.simplerpc import JSONRPCResponseManager
        JSONRPCResponseManager.DISPATCH_ENCODING = encoding
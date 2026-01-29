# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/LocalRpc.py


class LocalRpcClient(object):

    def call_server(self, uuid, method, *args):
        print (
         'CallServer:', uuid, method, args)
        server_plugin = LocalRpcManager.get_plugin_server(uuid)
        method = getattr(server_plugin, method)
        method(*args)


class LocalRpcManager(object):
    CLIENT_MAPPING = {}
    CLIENT_METHOD_DISPATCHER = {}
    SERVER_MAPPING = {}

    @classmethod
    def register_plugin_client(cls, uuid, pluginClient):
        cls.CLIENT_MAPPING[uuid] = pluginClient

    @classmethod
    def get_plugin_client(cls, uuid):
        return cls.CLIENT_MAPPING.get(uuid)

    @classmethod
    def register_plugin_server(cls, uuid, pluginServer):
        cls.SERVER_MAPPING[uuid] = pluginServer

    @classmethod
    def get_plugin_server(cls, uuid):
        return cls.SERVER_MAPPING.get(uuid)


class LocalRpcService(object):
    EventMainRPCReady = None

    @staticmethod
    def Update():
        pass

    @staticmethod
    def Close():
        pass

    @staticmethod
    def CloseMainClient():
        print 'cannot close local rpc'

    @staticmethod
    def GetClientPluginProxy(plugin_uuid):
        return LocalRpcServerPlugin(plugin_uuid)


class LocalRpcServerAgent(object):
    pass


class LocalRpcServerPlugin(object):

    def __init__(self, plugin_uuid):
        super(LocalRpcServerPlugin, self).__init__()
        self.uuid = plugin_uuid

    def CallMainRPC(self, method, *args):
        try:
            method_name = '_%s_%s' % (self.uuid, method)
            method = LocalRpcManager.CLIENT_METHOD_DISPATCHER[method_name]
            res = method(*args)
            from SunshineClient import Response
            if isinstance(res, Response):
                server_plugin = LocalRpcManager.get_plugin_server(res.uuid)
                method = getattr(server_plugin, res.methodName)
                method(*res.args)
            elif isinstance(res, list):
                for r in res:
                    server_plugin = LocalRpcManager.get_plugin_server(r.uuid)
                    method = getattr(server_plugin, r.methodName)
                    method(*r.args)

            elif res:
                print (
                 'Unknown Response:', res)
        except NotImplementedError:
            pass
        except:
            import traceback
            traceback.print_exc()

    def RegisterRPCHandler(self, handler):
        print ('Register RPC Handler', handler)
        LocalRpcManager.register_plugin_server(self.uuid, handler)

    @property
    def EventMainRPCReady(self):
        return LocalRpcService.EventMainRPCReady

    @EventMainRPCReady.setter
    def EventMainRPCReady(self, value):
        LocalRpcService.EventMainRPCReady = value
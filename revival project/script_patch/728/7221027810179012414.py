# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/rpcserver.py
import time
from .simplerpc import RpcAgent, Context
from .transport.interfaces import ServerOnConnectMessage, ServerOnCloseMessage

class ServerContext(Context):

    def __init__(self, rid, method, params, cid, agent, clientInfo):
        super(ServerContext, self).__init__(rid, method, params)
        self.cid = cid
        self._agent = agent
        self.clientInfo = clientInfo

    def call_peer(self, func, *args, **kwargs):
        return self._agent.call(self.cid, func, *args, **kwargs)

    def peer_info(self):
        return '<Client %s> at remote' % self.cid


class RpcServer(RpcAgent):

    def __init__(self, server, eventMode=False, twoStepConnection=False, protocol='json'):
        super(RpcServer, self).__init__(eventMode, protocol)
        self.server = server
        if self.eventMode:
            self.server.callback = self.handle_transport_message
        self._twoStepConnection = twoStepConnection
        self.heartbeatEnabled = False
        self.heartbeatInterval = 2.0
        self.heartbeatMaxTimes = 10
        self._heartbeatTime = 0
        self._clientHeartbeats = {}
        self.dispatcher.add_method(self._on_heartbeat, '__HEARTBEAT__')
        self.dispatcher.add_method(self.on_second_step_connect, '__CONNECT__')
        self._clientInfoMap = {}
        self.server.start()

    def enable_heartbeat(self):
        self.heartbeatEnabled = True
        for cid in self.server.connections:
            self.call(cid, '__HEARTBEAT_ARGS__', self.heartbeatInterval * self.heartbeatMaxTimes)

    def disable_heartbeat(self):
        self.heartbeatEnabled = False
        for cid in self.server.connections:
            self.call(cid, '__HEARTBEAT_ARGS__', 0)

    def on_client_connect(self, conn):
        print ('on_client_connect', conn)

    def on_second_step_connect(self, context, clientInfo):
        self._clientInfoMap[context.cid] = clientInfo
        self.on_client_connect(self.server.connections[context.cid])

    def on_client_close(self, conn):
        print (
         'on_client_close', conn)

    def update(self):
        super(RpcServer, self).update()
        if self.eventMode:
            return
        self.server.update()
        for conn, msg in self.server.recv():
            self.handle_transport_message(conn, msg)

        if self.heartbeatEnabled and time.time() - self._heartbeatTime >= self.heartbeatInterval:
            self._heartbeatTime = time.time()
            for cid in list(self.server.connections.keys()):
                info = self._clientHeartbeats.setdefault(cid, [0, 0])
                counter = info[0]
                if counter == 0:
                    self.call(cid, '__HEARTBEAT_ARGS__', self.heartbeatInterval * self.heartbeatMaxTimes)
                self.call(cid, '__HEARTBEAT__', counter)
                info[1] += 1
                if info[1] > self.heartbeatMaxTimes:
                    print 'heartbeat timeout!!!'
                    self.close_client(cid)

    def handle_transport_message(self, conn, msg):
        if isinstance(msg, ServerOnConnectMessage):
            if not self._twoStepConnection:
                self.on_client_connect(conn)
        elif isinstance(msg, ServerOnCloseMessage):
            self.on_client_close(conn)
            if conn.cid in self._clientInfoMap:
                del self._clientInfoMap[conn.cid]
        else:
            self.handle_message(msg, conn)

    def call(self, cid, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        conn = self.server.connections.get(cid, None)
        if conn is None:
            import sys
            sys.stderr.write('rpc server fail to call client %s, connection is lost!' % cid)
            return
        else:
            conn.send(req)
            return cb

    def close(self):
        self.server.close()

    def close_client(self, cid):
        self.server.close_client(cid)

    def create_context(self, conn, data):
        return ServerContext(data['id'], data['method'], data['params'], conn.cid, self, self._clientInfoMap.get(conn.cid, None))

    def _on_heartbeat(self, context, counter):
        cid = context.cid
        info = self._clientHeartbeats.setdefault(cid, [0, 0])
        if counter == info[0] + 1:
            info[0] += 1
            info[1] = 0
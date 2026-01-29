# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/rpcclient.py
import time
from collections import deque
import logging
from .simplerpc import RpcAgent, Context
from .transport.interfaces import ClientOnConnectMessage, ClientOnCloseMessage

class ClientContext(Context):

    def __init__(self, rid, method, params, agent):
        super(ClientContext, self).__init__(rid, method, params)
        self._agent = agent

    def call_peer(self, func, *args, **kwargs):
        return self._agent.call(func, *args, **kwargs)

    def peer_info(self):
        return '<Server> at remote'


class RpcClient(RpcAgent):
    CONNECTING, CONNECTED, CLOSED = (1, 2, 3)

    def __init__(self, conn, eventMode=False, twoStepConnection=False, clientInfo=None, protocol='json'):
        super(RpcClient, self).__init__(eventMode, protocol)
        self.logger = logging.getLogger('simplerpc')
        self._twoStepConnection = twoStepConnection
        self._clientInfo = clientInfo
        self._status = self.CONNECTING
        self._inbox = deque()
        self._outbox = deque()
        self.conn = conn
        if self.eventMode:
            self.conn.callback = self.handle_transport_message
        self.heartbeatTimeout = 0
        self.heartbeatStamp = 0
        self.dispatcher.add_method(self._on_heartbeat, '__HEARTBEAT__')
        self.dispatcher.add_method(self._on_heartbeat_args, '__HEARTBEAT_ARGS__')
        self.conn.connect()

    @property
    def status(self):
        return self._status

    def on_connect(self):
        print 'on_connect'
        if self._status == self.CLOSED:
            self._status = self.CONNECTED
        if self._status == self.CONNECTING:
            self._status = self.CONNECTED
        if self._twoStepConnection:
            self.second_step_connect(self._clientInfo or {})
        while self._inbox:
            item = self._inbox.popleft()
            self.handle_message(*item)

    def on_close(self):
        print 'on_close'
        self._status = self.CLOSED

    def create_context(self, conn, data):
        return ClientContext(data['id'], data['method'], data['params'], self)

    def second_step_connect(self, metaData):
        self.call('__CONNECT__', metaData)

    def call(self, func, *args, **kwargs):
        if self._status != self.CONNECTED:
            raise RuntimeError('Unable to call rpc at state: %s' % self._status)
        msg, cb = self.format_request(func, *args, **kwargs)
        self.conn.send(msg)
        return cb

    def update(self):
        super(RpcClient, self).update()
        if self.eventMode:
            return
        self.conn.update()
        data = self.conn.recv()
        for msg in data:
            self.handle_transport_message(self.conn, msg)

        if self.heartbeatTimeout and self.heartbeatStamp:
            if time.time() - self.heartbeatStamp > self.heartbeatTimeout:
                self.close()

    def handle_transport_message(self, conn, msg):
        if isinstance(msg, ClientOnConnectMessage):
            self.on_connect()
        elif isinstance(msg, ClientOnCloseMessage):
            self.on_close()
        elif self._status == self.CONNECTED:
            self.handle_message(msg, conn)
        else:
            self._inbox.append((msg, conn))

    def close(self):
        self.conn.close()
        self.on_close()

    def _on_heartbeat(self, _, counter):
        self.heartbeatStamp = time.time()
        counter += 1
        self.call('__HEARTBEAT__', counter)

    def _on_heartbeat_args(self, _, timeout):
        self.heartbeatTimeout = timeout
        if timeout == 0:
            self.heartbeatStamp = 0
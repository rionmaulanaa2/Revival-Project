# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/rmq/RmqRPC.py
import sys
import uuid
import pika
IS_PY3 = sys.version_info[0] == 3

class RmqClient(object):

    def __init__(self, url, exchange, backend=False, broadcastListen=None, broadcastSend=None):
        super(RmqClient, self).__init__()
        self.backend = backend
        self.key = str(uuid.uuid4())
        self.exchange = exchange
        self.broadcastListen = broadcastListen
        self.broadcastSend = broadcastSend
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        queue = self.channel.queue_declare(exclusive=True)
        queue_name = queue.method.queue
        binding_keys = ['*.to.%s' % self.key]
        if self.broadcastListen:
            binding_keys.append('*.broadcast.%s' % self.broadcastListen)
        for binding_key in binding_keys:
            self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=binding_key)

        self.channel.basic_consume(self._on_raw_message, queue=queue_name, no_ack=True)
        self.backendThread = None
        if self.backend:
            self.run_backend()
        return

    def _on_raw_message(self, ch, method, properties, body):
        routing_key = method.routing_key
        sender = routing_key.split('.')[0]
        self.on_message(sender, self._unpack_data(body))

    def on_message(self, sender, message):
        pass

    def run_backend(self):
        if self.backendThread:
            return
        import threading
        self.backendThread = threading.Thread(target=self.channel.start_consume)
        self.backendThread.daemon = True
        self.backendThread.start()

    def tick(self):
        self.connection.process_data_events()

    def wait_tick(self):
        self.tick()

    def _pack_data(self, data):
        return data

    def _unpack_data(self, data):
        if IS_PY3:
            return data.decode('utf-8')
        return data

    def send(self, data, remote_id=None):
        if remote_id:
            self._rmqSend(data, remote_id)
        else:
            self._rmqBroadcast(data, self.broadcastSend)

    def _rmqPublish(self, data, routing_key):
        message = self._pack_data(data)
        self.corr_id = uuid.uuid4().hex
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, properties=pika.BasicProperties(delivery_mode=2), body=message)

    def _rmqSend(self, data, remote_id):
        routing_key = '%s.to.%s' % (self.key, remote_id)
        self._rmqPublish(data, routing_key)

    def _rmqBroadcast(self, data, broadcast='toServer'):
        routing_key = '%s.broadcast.%s' % (self.key, broadcast)
        self._rmqPublish(data, routing_key)

    def close(self):
        self.connection.close()

    def isConnectionOpen(self):
        return self.connection.is_open


class RmqRPCClient(RmqClient):

    def __init__(self, url, exchange, backend=False):
        super(RmqRPCClient, self).__init__(url, exchange, backend, 'toClient', 'toServer')


class RmqRPCServer(RmqClient):

    def __init__(self, url, exchange, backend=False):
        super(RmqRPCServer, self).__init__(url, exchange, backend, 'toServer', 'toClient')
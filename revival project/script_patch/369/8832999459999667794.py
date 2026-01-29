# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/simplerpc/transport/redis/RedisRPC.py
import sys
IS_PY3 = sys.version_info[0] == 3

class RedisMqClient(object):

    def __init__(self, conn, backend=False, channelListen=None):
        super(RedisMqClient, self).__init__()
        self.backend = backend
        self.conn = conn
        self.ps = self.conn.pubsub()
        self.temp_channel = []
        if channelListen is not None:
            if isinstance(channelListen, str):
                channelListen = [
                 channelListen]
            self.ps.subscribe(channelListen)
        self.backendThread = None
        if self.backend:
            self.run_backend()
        return

    def on_message(self, message, reply_queue=None):
        pass

    def _on_raw_message(self, message):
        if message['channel'] in self.temp_channel:
            self.ps.unsubscribe(message['channel'])
            self.temp_channel.remove(message['channel'])
        message = message['data']
        data, reply_queue = self._unpack_data(message)
        self.on_message(data, reply_queue)

    def __backend_loop(self):
        for item in self.ps.listen():
            if item['type'] == 'message':
                self._on_raw_message(item)

    def run_backend(self):
        if self.backendThread:
            return
        import threading
        self.backendThread = threading.Thread(target=self.__backend_loop)
        self.backendThread.daemon = True
        self.backendThread.start()

    def tick(self):
        while True:
            message = self.ps.get_message()
            if message and message['type'] == 'message':
                self._on_raw_message(message)
            else:
                break

    def wait_tick(self):
        self.tick()

    def isConnectionOpen(self):
        return self.conn.ping == 'PONG'

    @staticmethod
    def _unpack_data--- This code section failed: ---

  74       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'struct'
           9  STORE_FAST            1  'struct'

  75      12  LOAD_FAST             1  'struct'
          15  LOAD_ATTR             1  'unpack_from'
          18  LOAD_CONST            2  '?'
          21  LOAD_CONST            3  ''
          24  CALL_FUNCTION_3       3 
          27  LOAD_CONST            3  ''
          30  BINARY_SUBSCR    
          31  STORE_FAST            2  'need_reply'

  76      34  LOAD_FAST             1  'struct'
          37  LOAD_ATTR             2  'calcsize'
          40  LOAD_CONST            2  '?'
          43  CALL_FUNCTION_1       1 
          46  STORE_FAST            3  'pos'

  77      49  LOAD_CONST            0  ''
          52  STORE_FAST            4  'replay_queue'

  78      55  LOAD_FAST             2  'need_reply'
          58  POP_JUMP_IF_FALSE   170  'to 170'

  79      61  LOAD_FAST             1  'struct'
          64  LOAD_ATTR             1  'unpack_from'
          67  LOAD_CONST            4  '<H'
          70  LOAD_FAST             0  'data'
          73  LOAD_FAST             3  'pos'
          76  CALL_FUNCTION_3       3 
          79  LOAD_CONST            3  ''
          82  BINARY_SUBSCR    
          83  STORE_FAST            5  'replay_queue_len'

  80      86  LOAD_FAST             3  'pos'
          89  LOAD_FAST             1  'struct'
          92  LOAD_ATTR             2  'calcsize'
          95  LOAD_CONST            4  '<H'
          98  CALL_FUNCTION_1       1 
         101  INPLACE_ADD      
         102  STORE_FAST            3  'pos'

  81     105  LOAD_FAST             1  'struct'
         108  LOAD_ATTR             1  'unpack_from'
         111  LOAD_CONST            5  '{}s'
         114  LOAD_ATTR             4  'format'
         117  LOAD_FAST             5  'replay_queue_len'
         120  CALL_FUNCTION_1       1 
         123  LOAD_FAST             0  'data'
         126  LOAD_FAST             3  'pos'
         129  CALL_FUNCTION_3       3 
         132  LOAD_CONST            3  ''
         135  BINARY_SUBSCR    
         136  STORE_FAST            4  'replay_queue'

  82     139  LOAD_FAST             3  'pos'
         142  LOAD_FAST             1  'struct'
         145  LOAD_ATTR             2  'calcsize'
         148  LOAD_CONST            5  '{}s'
         151  LOAD_ATTR             4  'format'
         154  LOAD_FAST             5  'replay_queue_len'
         157  CALL_FUNCTION_1       1 
         160  CALL_FUNCTION_1       1 
         163  INPLACE_ADD      
         164  STORE_FAST            3  'pos'
         167  JUMP_FORWARD          0  'to 170'
       170_0  COME_FROM                '167'

  83     170  LOAD_FAST             0  'data'
         173  LOAD_FAST             3  'pos'
         176  SLICE+1          
         177  STORE_FAST            0  'data'

  84     180  LOAD_GLOBAL           5  'IS_PY3'
         183  POP_JUMP_IF_FALSE   201  'to 201'
         186  LOAD_FAST             0  'data'
         189  LOAD_ATTR             6  'decode'
         192  LOAD_CONST            6  'utf-8'
         195  CALL_FUNCTION_1       1 
         198  JUMP_FORWARD          3  'to 204'
         201  LOAD_FAST             0  'data'
       204_0  COME_FROM                '198'
         204  LOAD_FAST             4  'replay_queue'
         207  BUILD_TUPLE_2         2 
         210  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 24

    @staticmethod
    def _pack_data(data, replay_queue=None):
        import struct
        header = struct.pack('?', replay_queue is not None)
        if replay_queue is not None:
            header += struct.pack('<H{}s'.format(len(replay_queue)), len(replay_queue), replay_queue)
        return header + data

    def _redisPublish(self, channel, data, reply=None):
        if reply is not None:
            self.temp_channel.append(reply)
            self.ps.subscribe(reply)
        self.conn.publish(channel, self._pack_data(data, reply))
        return

    def close(self):
        self.ps.close()
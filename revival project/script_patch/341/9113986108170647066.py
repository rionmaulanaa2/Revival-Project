# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilerpc/RpcChannel.py
from __future__ import absolute_import
from google.protobuf import service
from . import MobileRequest
from struct import pack, unpack
from ..mobilelog.LogManager import LogManager

class MobileRpcController(service.RpcController):

    def __init__(self, channel):
        super(MobileRpcController, self).__init__()
        self.rpc_channel = channel


class MobileRpcChannel(service.RpcChannel):

    def __init__(self, rpc_service, conn):
        super(MobileRpcChannel, self).__init__()
        self.rpc_service = rpc_service
        self.rpc_request = MobileRequest.request()
        self.rpc_request_parser = MobileRequest.request_parser()
        self.conn = conn
        self.conn.set_channel_interface_obj(self)
        self.controller = MobileRpcController(self)
        self.con_listeners = set()
        self.logger = LogManager.get_logger('mobilerpc.MobileRpcChannel')
        self.user_data = None
        self.session_seed = None
        return

    def set_max_data(self, size):
        self.rpc_request_parser.set_max_data(size)

    def reg_listener(self, listener):
        self.con_listeners.add(listener)

    def unreg_listener(self, listener):
        self.con_listeners.remove(listener)

    def getpeername(self):
        if self.conn:
            return self.conn.getpeername()
        return 'No connection attached'

    def set_compressor(self, compressor):
        self.conn.set_compressor(compressor)

    def set_crypter(self, encrypter, decrypter):
        self.conn.set_crypter(encrypter, decrypter)

    def set_user_data(self, user_data):
        self.user_data = user_data

    def get_user_data(self):
        return self.user_data

    def set_session_seed(self, seed):
        self.session_seed = seed

    def get_session_seed(self):
        return self.session_seed

    def on_disconnected(self):
        for listener in list(self.con_listeners):
            if listener in self.con_listeners:
                listener.on_channel_disconnected(self)

        self.rpc_request.reset()
        self.rpc_request_parser.reset()
        self.con_listeners = None
        self.conn = None
        self.user_data = None
        return

    def disconnect(self):
        if self.conn:
            self.conn.disconnect()

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        cmd_index = method_descriptor.index
        data = request.SerializeToString()
        total_len = len(data) + 2
        self.conn.send_data(''.join([pack('<I', total_len), pack('<H', cmd_index), data]))

    def parse(self, data, skip):
        result, consum = self.rpc_request_parser.parse(self.rpc_request, data, skip)
        if result == 1:
            l = len(self.rpc_request.data)
            if l < 2:
                self.logger.error('Got error request size: %d', l)
                return (
                 0, consum, None, None)
            index_data = self.rpc_request.data[0:2]
            cmd_index = unpack('<H', index_data)[0]
            rpc_service = self.rpc_service
            s_descriptor = rpc_service.GetDescriptor()
            if cmd_index > len(s_descriptor.methods):
                self.logger.error('Got error method index: %d %d', cmd_index, len(s_descriptor.methods))
                return (
                 0, consum, None, None)
            method = s_descriptor.methods[cmd_index]
            request = rpc_service.GetRequestClass(method)()
            serialized = self.rpc_request.data[2:]
            request.ParseFromString(serialized)
            return (
             1, consum, method, request)
        else:
            if result == 2:
                return (2, consum, None, None)
            if result == 0:
                return (0, consum, None, None)
            if result == 3:
                return (0, consum, None, None)
            return None

    def request(self, method, request):
        try:
            self.rpc_service.CallMethod(method, self.controller, request, None)
        except:
            self.logger.error('Call rpc method failed!')
            self.logger.log_last_except()

        return

    def input_data(self, data):
        total = len(data)
        skip = 0
        while skip < total:
            result, consum, method, request = self.parse(data, skip)
            skip += consum
            if result == 0:
                return 0
            if result == 1:
                self.request(method, request)
                self.rpc_request.reset()
                continue
            elif result == 2:
                break
            else:
                continue

        return 2
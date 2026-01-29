# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/SimpleIpPortRpcProcessor.py
from __future__ import absolute_import
import six
from msgpack import DEFAULT_STR_LEN_LIMIT, DEFAULT_ARRAY_LEN_LIMIT, DEFAULT_MAP_LEN_LIMIT, DEFAULT_EXT_LEN_LIMIT
try:
    from msgpack import packb, unpackb
except ImportError:
    from msgpack.embed import packb, unpackb

from .rpc_code import RPC_CODE
from .IpPortRpcProcessor import IpPortRpcProcessor, IpPortConnection
from msgpack.bson_msgpack import ext_hook
from msgpack.bson_msgpack import msgpackext
from .SimpleIpPortConnection import SimpleIpPortConnection
from .SimpleIpPortServer import SimpleIpPortServer
from ..mobilelog.LogManager import LogManager
from .SimpleServiceManager import SimpleServiceManager, CAN_RPC_FLAG, RPC_TYPE, MESSAGE_INJECT
GET_SERVICE = SimpleServiceManager.get_service
from .FutureAndResponse import Response
from .simplerpc_common import TCP, ENET, KCP
encode = --- This code section failed: ---

  24       0  LOAD_GLOBAL           0  'packb'
           3  LOAD_GLOBAL           1  'True'
           6  LOAD_GLOBAL           1  'True'
           9  LOAD_CONST            2  'default'
          12  LOAD_GLOBAL           2  'msgpackext'
          15  CALL_FUNCTION_513   513 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 15
if six.PY3:
    decode = --- This code section failed: ---

  26       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_CONST            2  'utf-8'
           9  LOAD_CONST            3  'ext_hook'
          12  LOAD_GLOBAL           1  'ext_hook'
          15  LOAD_CONST            4  'use_list'
          18  LOAD_GLOBAL           2  'True'
          21  LOAD_CONST            5  'max_str_len'

  27      24  LOAD_GLOBAL           3  'DEFAULT_STR_LEN_LIMIT'
          27  LOAD_CONST            6  'max_array_len'

  28      30  LOAD_GLOBAL           4  'DEFAULT_ARRAY_LEN_LIMIT'
          33  LOAD_CONST            7  'max_map_len'

  29      36  LOAD_GLOBAL           5  'DEFAULT_MAP_LEN_LIMIT'
          39  LOAD_CONST            8  'max_ext_len'

  30      42  LOAD_GLOBAL           6  'DEFAULT_EXT_LEN_LIMIT'
          45  CALL_FUNCTION_1793  1793 
          48  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_1793' instruction at offset 45
else:
    decode = --- This code section failed: ---

  32       0  LOAD_GLOBAL           0  'unpackb'
           3  LOAD_GLOBAL           1  'ext_hook'
           6  LOAD_GLOBAL           1  'ext_hook'
           9  LOAD_CONST            2  'use_list'
          12  LOAD_GLOBAL           2  'True'
          15  LOAD_CONST            3  'max_str_len'

  33      18  LOAD_GLOBAL           3  'DEFAULT_STR_LEN_LIMIT'
          21  LOAD_CONST            4  'max_array_len'

  34      24  LOAD_GLOBAL           4  'DEFAULT_ARRAY_LEN_LIMIT'
          27  LOAD_CONST            5  'max_map_len'

  35      30  LOAD_GLOBAL           5  'DEFAULT_MAP_LEN_LIMIT'
          33  LOAD_CONST            6  'max_ext_len'

  36      36  LOAD_GLOBAL           6  'DEFAULT_EXT_LEN_LIMIT'
          39  CALL_FUNCTION_1537  1537 
          42  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_1537' instruction at offset 39

class _IpPortConnection(SimpleIpPortConnection, IpPortConnection):

    def __init__--- This code section failed: ---

  44       0  LOAD_GLOBAL           0  'IpPortConnection'
           3  LOAD_ATTR             1  '__init__'
           6  LOAD_FAST             0  'self'
           9  LOAD_FAST             1  'rpc_processor'
          12  CALL_FUNCTION_2       2 
          15  POP_TOP          

  45      16  LOAD_GLOBAL           2  'SimpleIpPortConnection'
          19  LOAD_ATTR             1  '__init__'
          22  LOAD_ATTR             1  '__init__'
          25  LOAD_FAST             2  'con_type'
          28  CALL_FUNCTION_257   257 
          31  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 28

    @property
    def connect_remote_address(self):
        return self._remote_address

    @property
    def connect_remote_str(self):
        return self._connect_str

    def handle_message(self, message_data):
        IpPortConnection.handle_message(self, message_data)

    def handle_close(self):
        SimpleIpPortConnection.handle_close(self)
        IpPortConnection.handle_close(self)

    def handle_connected(self):
        SimpleIpPortConnection.handle_connected(self)
        IpPortConnection.handle_connected(self)

    def send_data(self, data):
        SimpleIpPortConnection.send_data(self, data)

    def send_data_udp(self, data):
        SimpleIpPortConnection.send_data_udp(self, data)

    def enable_encrypter(self, key):
        self._con.enable_encrypter(key)

    def delay_enable_encrypt(self, key):
        self._con.delay_enable_encrypt(key)

    def delay_enable_compress(self):
        self._con.delay_enable_compress()

    def enable_compressor(self, enable):
        self._con.enable_compressor(enable)

    def set_compressor_type(self, compressor_type):
        self._con.set_compressor_type(compressor_type)

    def set_oodnet_dict_path(self, oodnet_up_path, oodnet_down_path):
        self._con.set_oodnet_dict_path(oodnet_up_path, oodnet_down_path)

    def enable_capture_msg(self, enable, up_path, down_path):
        self._con.enable_capture_msg(enable, up_path, down_path)

    def set_kcp_interval(self, interval):
        if self._type == KCP:
            self._con.interval = interval

    def close(self):
        SimpleIpPortConnection.close(self)


class _IpPortServer(SimpleIpPortServer):

    def __init__(self, rpc_processor, *args, **kwargs):
        self._prc_processor = rpc_processor
        SimpleIpPortServer.__init__(self, *args, **kwargs)

    def do_get_processor(self):
        return _IpPortConnection(self._prc_processor)


class SimpleIpPortRpcProcessor(IpPortRpcProcessor):

    def __init__(self, tcp_address, con_type=TCP, *args, **kwargs):
        self._type = con_type
        IpPortRpcProcessor.__init__(self, tcp_address, *args, **kwargs)

    @property
    def con_type(self):
        return self._type

    def get_server(self, address):
        return _IpPortServer(self, address[0], address[1], con_type=self._type)

    def do_create_connection--- This code section failed: ---

 129       0  LOAD_GLOBAL           0  '_IpPortConnection'
           3  LOAD_GLOBAL           1  '_type'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  '_type'
          12  CALL_FUNCTION_257   257 
          15  STORE_FAST            3  'con'

 130      18  LOAD_FAST             3  'con'
          21  LOAD_ATTR             2  'connect'
          24  LOAD_FAST             1  'address'
          27  LOAD_CONST            2  ''
          30  BINARY_SUBSCR    
          31  LOAD_FAST             1  'address'
          34  LOAD_CONST            3  1
          37  BINARY_SUBSCR    
          38  LOAD_FAST             2  'timeout'
          41  CALL_FUNCTION_3       3 
          44  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12

    def handle_rpc(self, rpc_message, con):
        pass

    def handle_sync(self, args, con):
        pass

    def handle_sync_misty(self, args, con):
        pass

    def do_decode(self, data):
        return decode(data)

    def do_encode(self, message):
        return encode(message)


class DefaultRpc(SimpleIpPortRpcProcessor):

    def __init__(self, listen_address=None, con_type=TCP, con_timeout=2):
        SimpleIpPortRpcProcessor.__init__(self, listen_address, con_type=con_type, con_timeout=con_timeout)

    def handle_rpc(self, rpc_message, con):
        service_id, method_name, args = rpc_message[2], rpc_message[4], rpc_message[5]
        service_obj = GET_SERVICE(service_id)
        response = None
        if len(rpc_message) == 7:
            rid = rpc_message[6]
            response = Response(rid, con, self)
        if not service_obj:
            self.logger.error('do not exist service id:%s', service_id)
            if response:
                response.send_response(code=RPC_CODE.NOT_SERVICE, error='do not exist service id%s' % service_id)
            return
        else:
            method = getattr(service_obj, method_name, None)
            if not method:
                self.logger.error('service:%s do not exist method_name:%s', str(service_obj), method_name)
                if response:
                    response.send_response(code=RPC_CODE.NOT_METHOD, error='service:%s do not exist method_name:%s' % (str(service_obj), method_name))
                return
            method_flag = getattr(method, CAN_RPC_FLAG, None)
            if method_flag:
                try:
                    if response:
                        if method_flag == RPC_TYPE:
                            method(response, *args)
                        else:
                            error = 'service:%s invoke method_name:%s not have response' % (str(service_obj), method_name)
                            response.send_response(code=RPC_CODE.NOT_RESPONSE, error=error)
                            self.logger.error(error)
                    elif method_flag == MESSAGE_INJECT:
                        method(con, *args)
                    else:
                        method(*args)
                except:
                    self.logger.error('service:%s invoke error method_name:%s', str(service_obj), method_name)
                    self.logger.log_last_except()

            else:
                self.logger.error('service:%s can not invoke method_name:%s', str(service_obj), method_name)
                if response:
                    response.send_response(code=RPC_CODE.NOT_INVOKE, error='service:%s can not invoke method_name:%s' % (str(service_obj), method_name))
            return
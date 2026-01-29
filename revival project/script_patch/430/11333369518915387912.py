# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/DirectEntityRpcProcessor.py
from __future__ import absolute_import
import sys
from .rpc_code import RPC_CODE
from .SimpleIpPortRpcProcessor import SimpleIpPortRpcProcessor
from .simplerpc_common import TCP, ENET, KCP
from .FutureAndResponse import Response
from .SimpleServiceManager import CAN_RPC_FLAG, RPC_TYPE, MESSAGE_INJECT
from .defaultservice.DirectEntityService import DirectEntityServiceForClient, DirectEntityServiceForServer
from .SimpleIpPortRpcProcessor import _IpPortConnection, _IpPortServer
try:
    from msgpack import packb, unpackb
except ImportError:
    from msgpack.embed import packb, unpackb

from msgpack.bson_msgpack import msgpackext
encode = --- This code section failed: ---

  32       0  LOAD_GLOBAL           0  'packb'
           3  LOAD_GLOBAL           1  'True'
           6  LOAD_GLOBAL           1  'True'
           9  LOAD_CONST            2  'default'
          12  LOAD_GLOBAL           2  'msgpackext'
          15  CALL_FUNCTION_513   513 
          18  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 15

class _DirectIpPortConnection(_IpPortConnection):

    def __init__(self, rpc_processor, con_type=TCP):
        _IpPortConnection.__init__(self, rpc_processor, con_type=con_type)
        self.entity = None
        self.check_finish = False
        return

    def handle_close(self):
        _IpPortConnection.handle_close(self)
        self.entity = None
        return


class _DirectIpPortServer(_IpPortServer):

    def __init__(self, rpc_processor, *args, **kwargs):
        _IpPortServer.__init__(self, rpc_processor, *args, **kwargs)

    def do_get_processor(self):
        return _DirectIpPortConnection(self._prc_processor)


class DirectEntityRpcProcessor(SimpleIpPortRpcProcessor):

    def __init__(self, is_server, con_type=TCP, listen_address=None, key_path=None, tb_handler=None):
        self.tb_handler = tb_handler
        if is_server:
            self._service = DirectEntityServiceForServer(key_path=key_path)
        else:
            self._service = DirectEntityServiceForClient(tb_handler)
        SimpleIpPortRpcProcessor.__init__(self, listen_address, con_type=con_type)
        self._clear_timer.cancel()

    def set_traceback_handler(self, handler):
        self.tb_handler = handler

    def set_handle_sync(self, sync_handler, sync_misty_handler):
        self.handle_sync = sync_handler
        self.handle_sync_misty = sync_misty_handler

    def do_handle_trace_back(self, t, v, tb):
        if self.tb_handler is not None:
            self.tb_handler(t, v, tb)
        return

    def _handle_last_traceback(self, err_str=None):
        if self.tb_handler is not None:
            t, v, tb = sys.exc_info()
            self.tb_handler(t, v, tb)
        if err_str is not None:
            self.logger.error(err_str)
        self.logger.log_last_except()
        return

    def get_server(self, address):
        return _DirectIpPortServer(self, address[0], address[1], con_type=self._type)

    def do_create_connection--- This code section failed: ---

 102       0  LOAD_GLOBAL           0  '_DirectIpPortConnection'
           3  LOAD_GLOBAL           1  '_type'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  '_type'
          12  CALL_FUNCTION_257   257 
          15  STORE_FAST            3  'con'

 103      18  LOAD_FAST             3  'con'
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
        method_name, args = rpc_message[4], rpc_message[5]
        service_obj = self._service
        if not method_name:
            try:
                service_obj.entity_message(con, *args)
            except:
                self._handle_last_traceback('handle_rpc: call method entity_message has exception')

        else:
            response = None
            if len(rpc_message) == 7:
                rid = rpc_message[6]
                response = Response(rid, con, self)
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
                self._handle_last_traceback('handle_rpc: call method %s has exception' % method_name)

        else:
            self.logger.error('service:%s can not invoke method_name:%s', str(service_obj), method_name)
            if response:
                response.send_response(code=RPC_CODE.NOT_INVOKE, error='service:%s can not invoke method_name:%s' % (str(service_obj), method_name))
        return

    def do_encode(self, message):
        return encode(message)
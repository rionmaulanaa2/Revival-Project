# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/GameToGameProcessor.py
from __future__ import absolute_import
from .SimpleIpPortRpcProcessor import DefaultRpc
import msgpack
from msgpack.bson_msgpack import ext_hook
from msgpack.bson_msgpack import msgpackext
from .rpc_code import RPC_CODE
from .SimpleServiceManager import SimpleServiceManager, CAN_RPC_FLAG, RPC_TYPE, MESSAGE_INJECT
GET_SERVICE = SimpleServiceManager.get_service
from .FutureAndResponse import Response
from .simplerpc_common import TCP, ENET, KCP, LogManager, RPC_REQUEST
from .defaultservice.EntityMessageWrapper import EntityMessageService
from .FutureAndResponse import Future
encode = --- This code section failed: ---

  22       0  LOAD_GLOBAL           0  'msgpack'
           3  LOAD_ATTR             1  'packb'
           6  LOAD_ATTR             1  'packb'
           9  LOAD_GLOBAL           2  'True'
          12  LOAD_CONST            2  'default'
          15  LOAD_GLOBAL           3  'msgpackext'
          18  CALL_FUNCTION_513   513 
          21  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 18
decode = --- This code section failed: ---

  23       0  LOAD_GLOBAL           0  'msgpack'
           3  LOAD_ATTR             1  'unpackb'
           6  LOAD_ATTR             1  'unpackb'
           9  LOAD_CONST            2  'utf-8'
          12  LOAD_CONST            3  'ext_hook'
          15  LOAD_GLOBAL           2  'ext_hook'
          18  CALL_FUNCTION_513   513 
          21  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_513' instruction at offset 18
_logger = LogManager.get_logger('GameToGameFuture')

class GameToGameFuture(Future):

    def __init__(self, rid, time_out=2, invoke_info=None):
        Future.__init__(self, rid, time_out=time_out)
        self._invoke_info = invoke_info

    def fire(self, code, error, args):
        if code != RPC_CODE.OK:
            _logger.error('game2game rpc error, reason:%s, invoke info: %s', error, self._invoke_info)
        Future.fire(self, code, error, args)


class GameToGameProcessor(DefaultRpc):

    def __init__--- This code section failed: ---

  45       0  LOAD_GLOBAL           0  'DefaultRpc'
           3  LOAD_ATTR             1  '__init__'
           6  LOAD_ATTR             1  '__init__'
           9  LOAD_FAST             1  'listen_address'
          12  LOAD_CONST            2  'con_type'
          15  LOAD_FAST             2  'con_type'
          18  LOAD_CONST            3  'con_timeout'
          21  LOAD_FAST             3  'con_timeout'
          24  CALL_FUNCTION_769   769 
          27  POP_TOP          

  46      28  LOAD_GLOBAL           2  'EntityMessageService'
          31  CALL_FUNCTION_0       0 
          34  LOAD_FAST             0  'self'
          37  STORE_ATTR            3  '_service'

  47      40  LOAD_GLOBAL           4  'GameToGameFuture'
          43  LOAD_FAST             0  'self'
          46  STORE_ATTR            5  '_future_type'

Parse error at or near `CALL_FUNCTION_769' instruction at offset 24

    def request_rpc(self, address, service_id, method_name, args=None, service_id_type=0, method_name_type=0, need_reply=False, timeout=2, target_con=None):
        args = args or []
        message = [RPC_REQUEST, service_id_type, service_id, method_name_type, method_name, args]
        future = None
        if need_reply:
            now_rid = self._get_rid()
            future = self._future_type(now_rid, time_out=timeout, invoke_info=args)
            message.append(now_rid)
        use_con = target_con if target_con else self.get_connection(address)
        if use_con:
            if future:
                use_con.add_future(future)
            self._send_rpc_message(message, use_con)
        else:
            if future:
                future.stop_time_out()
                message.append(future)
            self.buffer_send_message(address, message)
            self._create_connection(address)
        return future

    def handle_rpc(self, rpc_message, con):
        method_name, args = rpc_message[4], rpc_message[5]
        service_obj = self._service
        response = None
        if len(rpc_message) == 7:
            rid = rpc_message[6]
            response = Response(rid, con, self)
        if not method_name:
            if not response:
                method = service_obj.e_s if 1 else service_obj.b_s
            else:
                method = getattr(service_obj, method_name, None)
            method or self.logger.error('service:%s do not exist method_name:%s', str(service_obj), method_name)
            if response:
                response.send_response(code=RPC_CODE.NOT_METHOD, error='service:%s do not exist method_name:%s' % (str(service_obj), method_name))
            return
        else:
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
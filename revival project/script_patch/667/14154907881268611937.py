# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/IpPortRpcProcessor.py
from __future__ import absolute_import
import six_ex
from ..mobilelog.LogManager import LogManager
from .simplerpc_common import addTimer, addRepeatTimer
from .rpc_code import RPC_CODE
import sys
from .FutureAndResponse import Future
from .simplerpc_common import RPC_REQUEST, RPC_RESPONSE, RPC_HEARTBEAT, RPC_SYNC, RPC_SYNC_MISTY
RECONNECT_WAIT_TIME = 0.4
RECONNECT_MAX_TIME = 3
from .simplerpc_common import RPC_PROCESSOR_CONNECTION_CLEAR_INTERVAL as CLEAR_INTERVAL
CONNECTION_LOGGER = LogManager.get_logger('IpPortConnection')

class IpPortConnection(object):

    def __init__(self, rpc_processor):
        object.__init__(self)
        self._disconnect_cbs = []
        self._rpc_processor = rpc_processor
        self.send_count = 0
        self._futures = dict()
        self._do_decode = self._rpc_processor.do_decode
        self._handle_rpc = self._rpc_processor.handle_rpc
        self._handle_sync = self._rpc_processor.handle_sync
        self._handle_sync_misty = self._rpc_processor.handle_sync_misty

    def add_disconnect_cb(self, cb):
        self._disconnect_cbs.append(cb)

    def del_disconnect_cb(self, cb):
        try:
            self._disconnect_cbs.remove(cb)
        except:
            pass

    def add_future(self, future):
        if future.rid in self._futures:
            raise Exception('duplicate rid')
        self._futures[future.rid] = future
        future.set_con_obj(self)

    def fire_future(self, rid, code, error, args):
        try:
            future = self._futures[rid]
            del self._futures[rid]
            future.fire(code, error, args)
        except:
            CONNECTION_LOGGER.log_last_except()

    @property
    def connect_remote_address(self):
        raise Exception('not implement remote_address')

    @property
    def connect_remote_str(self):
        raise Exception('not implement connect_remote_str')

    def close(self):
        raise Exception('not implement connect_remote_str')

    def handle_message(self, message_data):
        try:
            rpc_message = self._do_decode(message_data)
        except:
            self.close()
            CONNECTION_LOGGER.error('decode data error %s  connection will be close', self.connect_remote_str)
            CONNECTION_LOGGER.log_last_except()
            self._rpc_processor.handle_traceback()
        else:
            try:
                message_type = rpc_message[0]
                if message_type == RPC_REQUEST:
                    self._handle_rpc(rpc_message, self)
                elif message_type == RPC_SYNC:
                    self._handle_sync(rpc_message[1], self)
                elif message_type == RPC_SYNC_MISTY:
                    self._handle_sync_misty(rpc_message[1], self)
                elif message_type == RPC_RESPONSE:
                    rid = rpc_message[1]
                    code, error, args = rpc_message[2]
                    self.fire_future(rid, code, error, args)
                elif message_type == RPC_HEARTBEAT:
                    pass
                else:
                    CONNECTION_LOGGER.error('unknown rpc type, %s', str(message_type))
                    self.close()
            except:
                CONNECTION_LOGGER.error('rpc execute error')
                CONNECTION_LOGGER.log_last_except()
                self._rpc_processor.handle_traceback()

    def handle_close(self):
        if self._rpc_processor is not None:
            self._rpc_processor.handle_connection_close(self)
            for _cb in self._disconnect_cbs:
                try:
                    _cb()
                except:
                    CONNECTION_LOGGER.error('disconnect cb error')
                    CONNECTION_LOGGER.log_last_except()
                    self._rpc_processor.handle_traceback()

            self._rpc_processor = None
            self._handle_rpc = None
            self._handle_sync = None
            self._handle_sync_misty = None
            self._disconnect_cbs = []
            rids = set(six_ex.keys(self._futures))
            for rid in rids:
                self.fire_future(rid, RPC_CODE.CLOSE, 'connection_closed', None)

            self._futures.clear()
            self._do_decode = None
        return

    def handle_connected(self):
        self._rpc_processor.handle_connection_connected(self)

    def send_data_and_count(self, data):
        self.send_count += 1
        self.send_data(data)

    def request_rpc(self, service_id, method_name, args=None, service_id_type=0, method_name_type=0, need_reply=False, timeout=2):
        args = args or []
        return self._rpc_processor.request_rpc(None, service_id, method_name, args, service_id_type, method_name_type, need_reply, timeout, self)

    def request_rpc_misty(self, service_id, method_name, args=None, service_id_type=0, method_name_type=0, need_reply=False, timeout=2):
        args = args or []
        return self._rpc_processor.request_rpc_misty(None, service_id, method_name, args, service_id_type, method_name_type, need_reply, timeout, self)

    def request_sync(self, args=None):
        args = args or []
        self._rpc_processor.request_sync(self, args)

    def request_sync_misty(self, args=None):
        args = args or []
        self._rpc_processor.request_sync_misty(self, args)

    def send_data(self, data):
        raise Exception('not implement send_data')

    def enable_encrypter(self, key):
        raise Exception('not implement enable_encrypter')

    def enable_compressor(self, enable):
        raise Exception('not implement enable_compressor')


class IpPortRpcProcessor(object):

    def __init__(self, address, future_type=Future, con_timeout=2):
        object.__init__(self)
        self._future_type = future_type
        self.logger = LogManager.get_logger(self.__class__.__name__)
        self._listen_address = address
        if address:
            self._server = self.get_server(address)
        else:
            self._server = None
        self._clear_timer = addRepeatTimer(CLEAR_INTERVAL, self._do_clear)
        self._connect_fail_time = dict()
        self._in_connecting_address = set()
        self._rid = 0
        self._connected_remote_cons = dict()
        self._buffered_send_message = dict()
        self._con_timeout = con_timeout
        return

    @property
    def my_address(self):
        return self._listen_address

    def start(self):
        if self._server:
            self._server.start()

    def stop(self):
        if self._server:
            self._server.stop()
            self._server = None
        if self._clear_timer:
            self._clear_timer.cancel()
            self._clear_timer = None
        for con in six_ex.values(self._connected_remote_cons):
            con.close()

        return

    def _get_rid(self):
        self._rid += 1
        if self._rid > 50000000:
            self._rid = 1
        return self._rid

    def handle_traceback(self):
        t, v, tb = sys.exc_info()
        try:
            self.do_handle_trace_back(t, v, tb)
        except:
            self.logger.error('do_handle_trace_back error')
            self.logger.log_last_except()

    def buffer_send_message(self, address, data):
        try:
            self._buffered_send_message[address].append(data)
        except:
            self._buffered_send_message[address] = [
             data]

    def get_buffer_data_not_clear(self, address):
        return self._buffered_send_message.get(address, [])

    def get_buffered_data_and_clear(self, address):
        return self._buffered_send_message.pop(address, [])

    def _do_clear(self):
        for con in six_ex.values(self._connected_remote_cons):
            if con.send_count == 0:
                con.close()
            else:
                con.send_count = 0

    def _remove_connection(self, con):
        if con.connect_remote_address and con.connect_remote_address in self._connected_remote_cons:
            if self._connected_remote_cons.get(con.connect_remote_address) == con:
                del self._connected_remote_cons[con.connect_remote_address]
            else:
                self.logger.error('remove connection error, not consistency')

    def get_connection(self, address):
        return self._connected_remote_cons.get(address, None)

    def _create_connection_later(self, address, wait):
        address_str = ':'.join([address[0], str(address[1])])
        if address_str not in self._in_connecting_address:
            self._in_connecting_address.add(address_str)
            addTimer(wait, lambda : self.do_create_connection(address, self._con_timeout))

    def _create_connection(self, address):
        address_str = ':'.join([address[0], str(address[1])])
        if address_str not in self._in_connecting_address:
            self._in_connecting_address.add(address_str)
            self.do_create_connection(address, self._con_timeout)

    def handle_connection_close(self, con):
        if con.connect_remote_address:
            self._remove_connection(con)
            if con.connect_remote_str in self._in_connecting_address:
                self._in_connecting_address.remove(con.connect_remote_str)
                self.logger.error('do connect remote fail %s', con.connect_remote_str)
                if con.connect_remote_str not in self._connect_fail_time:
                    self._connect_fail_time[con.connect_remote_str] = 1
                else:
                    self._connect_fail_time[con.connect_remote_str] += 1
                if self._connect_fail_time[con.connect_remote_str] >= RECONNECT_MAX_TIME:
                    self.logger.error('can not connect remote %s  after try connect %d times, abandon', con.connect_remote_str, RECONNECT_MAX_TIME)
                    datas = self.get_buffered_data_and_clear(con.connect_remote_address)
                    for item in datas:
                        if len(item) == 8:
                            item[7].fire(RPC_CODE.CONNECT_FAIL, 'can not connect remote ' + con.connect_remote_str, None)

                    self._connect_fail_time[con.connect_remote_str] = 0
                elif self.get_buffer_data_not_clear(con.connect_remote_address):
                    self.logger.error('still exist buffered data need send %s, try connect %fs after', con.connect_remote_str, RECONNECT_WAIT_TIME)
                    self._create_connection_later(con.connect_remote_address, RECONNECT_WAIT_TIME)
        return

    def handle_connection_connected(self, con):
        if con.connect_remote_address:
            self._connect_fail_time[con.connect_remote_str] = 0
            self._in_connecting_address.discard(con.connect_remote_str)
            buffer_messages = self.get_buffered_data_and_clear(con.connect_remote_address)
            for message in buffer_messages:
                if len(message) == 8:
                    future = message.pop(7)
                    future.start_time_out()
                    con.add_future(future)
                self._send_rpc_message(message, con)

            if con.connect_remote_address not in self._connected_remote_cons:
                self._connected_remote_cons[con.connect_remote_address] = con
            else:
                con.close()

    def do_create_connection(self, address, timeout=2):
        raise Exception('not implement do_create_connection')

    def _send_rpc_message(self, message, con):
        try:
            data = self.do_encode(message)
        except:
            self.logger.error('encode request message error')
            self.logger.log_last_except()
            self.handle_traceback()
        else:
            con.send_data_and_count(data)

    def _send_rpc_message_misty(self, message, con):
        try:
            data = self.do_encode(message)
        except:
            self.logger.error('encode request message error')
            self.logger.log_last_except()
            self.handle_traceback()
        else:
            con.send_data_udp(data)

    def request_rpc(self, address, service_id, method_name, args=None, service_id_type=0, method_name_type=0, need_reply=False, timeout=2, target_con=None):
        args = args or []
        message = [RPC_REQUEST, service_id_type, service_id, method_name_type, method_name, args]
        future = None
        if need_reply:
            now_rid = self._get_rid()
            future = self._future_type(now_rid, time_out=timeout)
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

    def request_rpc_misty(self, address, service_id, method_name, args=None, service_id_type=0, method_name_type=0, need_reply=False, timeout=2, target_con=None):
        args = args or []
        message = [RPC_REQUEST, service_id_type, service_id, method_name_type, method_name, args]
        use_con = target_con if target_con else self.get_connection(address)
        self._send_rpc_message_misty(message, use_con)

    def request_sync(self, target_con, args=None):
        if not target_con:
            return
        args = args or []
        message = [RPC_SYNC, args]
        self._send_rpc_message(message, target_con)

    def request_sync_misty(self, target_con, args=None):
        if not target_con:
            return
        args = args or []
        message = [RPC_SYNC_MISTY, args]
        self._send_rpc_message_misty(message, target_con)

    def handle_rpc(self, rpc_message, con):
        raise Exception('not implement handle_rpc')

    def handle_sync(self, args, con):
        raise Exception('not implement handle_sync')

    def handle_sync_misty(self, args, con):
        raise Exception('not implement handle_sync_misty')

    def do_encode(self, message):
        raise Exception('not implement do_encode')

    def do_decode(self, data):
        raise Exception('not implement do_encode')

    def get_server(self, address):
        raise Exception('not implement get_server')

    def do_handle_trace_back(self, t, v, tb):
        pass
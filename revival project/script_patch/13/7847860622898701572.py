# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/defaultservice/MBServiceCenter.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from ..SimpleServiceManager import SimpleServiceManager, SIMPLE_RPC_METHOD
from ..rpc_code import RPC_CODE
from ..simplerpc_common import SERVICE_CENTER_ID, addTimer, addRepeatTimer, HEART_TIMEOUT, LogManager

class MBServiceCenter(object):

    def __init__(self, rpc_processor, my_id=SERVICE_CENTER_ID):
        object.__init__(self)
        self._logger = LogManager.get_logger('MBServiceCenter')
        self._id = my_id
        self._rpc_processor = rpc_processor
        SimpleServiceManager.add_service(my_id, self)
        self._services = dict()
        self._service_stubs = set()
        self._hearts = dict()
        self._heart_timer = addRepeatTimer(HEART_TIMEOUT, self._check_heart_beat)

    def destroy(self):
        SimpleServiceManager.remove_service(self._id)

    def _check_heart_beat(self):
        overs = set()
        for address in six_ex.keys(self._hearts):
            if self._hearts[address] > 0:
                self._hearts[address] = 0
            else:
                self._logger.error('remote heart timeout address:%s', address)
                overs.add(address)

        if overs:
            self._clear_address(overs)

    def _clear_address(self, overs):
        for address in overs:
            if address in self._hearts:
                del self._hearts[address]

        need_remove_stubs = set()
        for item in self._service_stubs:
            if item[1] in overs:
                need_remove_stubs.add(item)

        self._service_stubs.difference_update(need_remove_stubs)
        need_remove_services = []
        for item in six_ex.values(self._services):
            if item[2] in overs:
                need_remove_services.append([item[0], item[2]])

        if need_remove_services:
            for item in need_remove_services:
                del self._services[item[0]]

            self._send_items(need_remove_services, which=2)

    def _send_items(self, need_send_infos, which=1, target=None):
        if which == 1:
            method = 'remote_service_register'
        else:
            method = 'remote_service_un_register'
        while need_send_infos:
            out_info = []
            for _ in range(200):
                if need_send_infos:
                    out_info.append(need_send_infos.pop())
                else:
                    break

            def _send(infos):
                args = [
                 infos]
                if not target:
                    for stub_info in self._service_stubs:
                        self._rpc_processor.request_rpc(stub_info[1], stub_info[0], method, args=args)

                else:
                    self._rpc_processor.request_rpc(target[1], target[0], method, args=args)

            _send(out_info)

    @SIMPLE_RPC_METHOD(response=True)
    def register_stub(self, response, service_id, address):
        address = tuple(address)
        self._hearts[address] = 1
        obj = (service_id, address)
        if obj in self._service_stubs:
            response.send_response(code=RPC_CODE.OK, args=(False, 'duplicate'))
        else:
            self._service_stubs.add(obj)
            response.send_response(code=RPC_CODE.OK, args=(True, 'success'))
            need_send_infos = list(six_ex.values(self._services))
            self._send_items(need_send_infos, which=1, target=obj)
            response.connection.add_disconnect_cb(lambda : addTimer(0.2, lambda : self._disconnect_cb(service_id, address)))

    def _disconnect_cb(self, s_id, address):
        future = self._rpc_processor.request_rpc(address, s_id, 'center_check', need_reply=True, timeout=4)

        def _cb(code, error, args):
            if code == RPC_CODE.OK:
                pass
            else:
                self._logger.error('remote check fail address:%s, code:%s, error:%s', address, code, error)
                self._clear_address([address])

        future.add_listener(_cb)

    @SIMPLE_RPC_METHOD(response=True)
    def register_connection(self, response, service_id, address):
        response.connection.add_disconnect_cb(lambda : self._disconnect_cb(service_id, tuple(address)))
        response.send_response(code=RPC_CODE.OK)

    @SIMPLE_RPC_METHOD(response=True)
    def register_service(self, response, service_id, tag_name, address):
        address = tuple(address)
        self._hearts[address] = 1
        if service_id in self._services:
            response.send_response(code=RPC_CODE.OK, args=(False, 'duplicate id'))
        else:
            self._services[service_id] = (
             service_id, tag_name, address)
            response.send_response(code=RPC_CODE.OK, args=(True, 'success'))
            self._send_items([[service_id, tag_name, address]], which=1)

    @SIMPLE_RPC_METHOD()
    def un_register_service(self, service_id, address):
        address = tuple(address)
        self._hearts[address] = 1
        if service_id in self._services and self._services[service_id][2] == address:
            del self._services[service_id]
            self._send_items([[service_id, address]], which=2)

    @SIMPLE_RPC_METHOD()
    def heart_beat(self, address):
        address = tuple(address)
        self._hearts[address] = 1
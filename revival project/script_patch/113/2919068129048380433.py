# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/ServiceStandaloneStarter.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import os
os.environ['REPLACE_ASYNC'] = 'True'
import json
from .SimpleIpPortRpcProcessor import DefaultRpc
from .defaultservice.MBServiceCenterStub import MBServiceCenterStub
from .simplerpc_common import TCP, KCP
from . import simplerpc_common

class Main(object):

    def __init__(self, conf_file_path):
        object.__init__(self)
        self._config_file_path = conf_file_path
        if not os.path.exists(conf_file_path):
            raise Exception('config file not exist')
        self._config_data = self._init_config()
        if self._config_data.get('io_type', 0) == 1:
            simplerpc_common.USE_EV_IO = True
        self._rpc_processors = dict()
        self._main_rpc_processor_info = self._config_data['main_rpc_processor_info']
        self._main_rpc_processor_info[1] = tuple(self._main_rpc_processor_info[1])
        self._manager_address = tuple(self._config_data['manager_address'])
        self._main_rpc_processor = None
        self._service_center_stub = None
        return

    def _init_config(self):
        with open(self._config_file_path) as conf_file:
            file_data = conf_file.read()
            return json.loads(file_data)

    def _create_rpc_processors(self):
        pors = self._config_data.get('rpc_processors', [])
        out_processors = dict()
        for item in pors:
            item[1] = tuple(item[1])
            if item[2] == 'TCP':
                use_type = TCP if 1 else KCP
                rpc_processor = DefaultRpc(listen_address=item[1], con_type=use_type)
                out_processors[item[0]] = rpc_processor

        return out_processors

    def _do_bootstrap(self):
        try:
            bootstrap_module = self._config_data['bootstrap_module']
            __import__(bootstrap_module)
        except:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self._rpc_processors = self._create_rpc_processors()
        self._main_rpc_processor = self._rpc_processors[self._main_rpc_processor_info[0]]
        simplerpc_common.MAIN_RPC_PROCESSOR = self._main_rpc_processor
        self._service_center_stub = MBServiceCenterStub(self._main_rpc_processor, self._main_rpc_processor_info[1], self._manager_address)
        simplerpc_common.SERVICE_CENTER_STUB = self._service_center_stub
        for pc in six_ex.values(self._rpc_processors):
            pc.start()

        simplerpc_common.addTimer(2, self._do_bootstrap)
        if self._config_data.get('io_type', 0) == 1:
            from EvIO.libevcore import IO
            while 1:
                IO.run()

        else:
            from ..common.mobilecommon import asiocore
            asiocore.start()
            while 1:
                asiocore.poll()
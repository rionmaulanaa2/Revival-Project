# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/ServiceManagerStarter.py
from __future__ import absolute_import
import json
import os
from . import simplerpc_common
from .SimpleIpPortRpcProcessor import DefaultRpc
from .defaultservice.MBServiceCenter import MBServiceCenter

class Main(object):

    def __init__(self, conf_file_path):
        object.__init__(self)
        self._config_file_path = conf_file_path
        if not os.path.exists(conf_file_path):
            raise Exception('config file not exist')
        self._config_data = self._init_config()
        self._ip = str(self._config_data['ip'])
        self._port = self._config_data['port']
        if self._config_data.get('io_type', 0) == 1:
            simplerpc_common.USE_EV_IO = True
        self._rpc_processor = DefaultRpc(listen_address=(self._ip, self._port))
        self._center = MBServiceCenter(self._rpc_processor)

    def _init_config(self):
        with open(self._config_file_path) as conf_file:
            file_data = conf_file.read()
            return json.loads(file_data)

    def start(self):
        self._rpc_processor.start()
        if self._config_data.get('io_type', 0) == 1:
            from EvIO.libevcore import IO
            while 1:
                IO.run()

        else:
            from ..common.mobilecommon import asiocore
            asiocore.start()
            while 1:
                asiocore.poll()
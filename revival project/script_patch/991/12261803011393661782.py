# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impVeteran.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Dict, Int
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
import time

class impVeteran(object):

    def _init_veteran_from_dict(self, bdict):
        self.is_sea_pc_veteran = bdict.get('is_sea_pc_veteran', False)
        self.steam_return_info = bdict.get('pc_veteran_info', None)
        self.steam_host_list = bdict.get('steam_host_list', [])
        self._last_return_steam = 0
        self._last_search_steam = 0
        return

    def can_return_steam_server(self):
        return self.is_sea_pc_veteran

    def get_steam_host_list(self):
        return self.steam_host_list

    def get_steam_return_info(self):
        return self.steam_return_info

    def request_return_to_steam(self, host, uid):
        self.call_server_method('verify_sea_pc_veteran', (host, uid))
        self._last_return_steam = time.time()

    def request_return_to_steam_again(self):
        if not self.steam_return_info or self.steam_return_info.get('ret', True):
            return
        now = time.time()
        if now < self._last_return_steam + 30:
            return False
        self._last_return_steam = now
        self.call_server_method('verify_sea_pc_veteran', (0, 0))

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def request_return_to_steam_result(self, data):
        self.steam_return_info = data
        ui = global_data.ui_mgr.get_ui('PCVeteranSuccessUI')
        ui and ui.set_confirm_info(data)
        ui = global_data.ui_mgr.get_ui('PCVeteranUI')
        ui and ui.check_has_bind()

    def query_steam_char_name(self, host, uid):
        if self.steam_return_info:
            return False
        now = time.time()
        if now < self._last_search_steam + 5:
            return False
        self._last_search_steam = now
        self.call_server_method('query_sea_steam_name', (host, uid))
        return True

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def query_steam_char_name_result(self, data):
        ui = global_data.ui_mgr.get_ui('PCVeteranConfirmUI')
        ui and ui.set_confirm_info(data)
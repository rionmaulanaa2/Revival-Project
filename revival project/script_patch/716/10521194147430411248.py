# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impGuangmu.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int

class impGuangmu(object):

    def _init_guangmu_from_dict(self, bdict):
        self.selected_guangmu = bdict.get('selected_canopy_item_no', None)
        return

    def get_selected_guangmu(self):
        return self.selected_guangmu

    def set_selected_guangmu(self, guangmu_no):
        self.call_server_method('select_canopy', (int(guangmu_no),))

    @rpc_method(CLIENT_STUB, (Int('guangmu_no'),))
    def resp_select_canopy(self, guangmu_no):
        self.selected_guangmu = guangmu_no
        global_data.emgr.on_selected_guangmu_changed.emit(guangmu_no)
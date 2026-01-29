# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impProjectionKill.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int

class impProjectionKill(object):

    def _init_projectionkill_from_dict(self, bdict):
        self._selected_projection_kill_no = bdict.get('selected_projection_kill_no', 0)

    def get_current_selected_projection_kill_no(self):
        return self._selected_projection_kill_no

    def try_set_selected_projection_kill_no(self, new_projection_kill_no):
        print (
         'try_set_selected_projection_kill_no', new_projection_kill_no)
        self.call_server_method('set_selected_projection_kill_no', (int(new_projection_kill_no),))

    @rpc_method(CLIENT_STUB, (Int('new_projection_kill_no'),))
    def on_selected_projection_kill_no_changed(self, new_projection_kill_no):
        self._selected_projection_kill_no = new_projection_kill_no
        print ('on_selected_projection_kill_no_changed', self._selected_projection_kill_no)
        global_data.emgr.player_item_update_event.emit()
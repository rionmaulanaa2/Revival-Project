# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impAnticheat.py
from __future__ import absolute_import
from mobile.common.RpcMethodArgs import Str, List, Int, Float, Dict, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class impAnticheat(object):

    @rpc_method(CLIENT_STUB, (List('detect_data'),))
    def request_detect_client(self, detect_data):
        for detect_type, interval, times in detect_data:
            global_data.anticheat_utils.detect(detect_type, interval, times)

    def respon_detect_client(self, detect_data):
        self.call_soul_method('respon_detect_client', (detect_data,))

    @rpc_method(CLIENT_STUB, (Int('ban'),))
    def physics_ban(self, ban):
        from logic.comsys.login.LoginHelper import set_physics_ban, del_physics_ban
        if ban:
            set_physics_ban()
        else:
            del_physics_ban()

    @rpc_method(CLIENT_STUB)
    def on_upload_screenshot(self):
        self.do_upload_screenshot()

    def do_upload_screenshot(self):
        import game3d
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return
        if global_data.anticheatsdk_mgr:
            global_data.anticheatsdk_mgr.upload_screenshot()
        if global_data.deviceinfo:
            global_data.deviceinfo.upload_process_info()

    @rpc_method(CLIENT_STUB, ())
    def request_upload_state(self):
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_DUMP_ALL_STATE')
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_DUMP_ALL_STATE')

    @rpc_method(CLIENT_STUB, (Int('tag'), Float('ts')))
    def detect_timer(self, tag, ts):
        global_data.anticheat_utils.detect_timer(tag, ts)

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def detect_data(self, data):
        global_data.anticheat_utils.detect_data(data)
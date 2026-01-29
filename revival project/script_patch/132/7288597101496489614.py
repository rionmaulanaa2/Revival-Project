# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/MuSdkMgr.py
from __future__ import absolute_import
from common.framework import Singleton
import game3d

class MuSdkMgr(Singleton):
    ALIAS_NAME = 'musdk_mgr'

    def init(self):
        import game3d
        self._timer = 0
        self._last_state = None
        self.check_and_report_mouse_state()
        self.register_timer()
        return

    def on_finalize(self):
        self.unregister_timer()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.check_and_report_mouse_state, interval=60, mode=CLOCK, times=-1)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def check_and_report_mouse_state(self):
        if self._last_state is None:
            self._last_state = game3d.mumu_keymousemod()
            return
        else:
            cur_state = game3d.mumu_keymousemod()
            if cur_state != self._last_state:
                self._last_state = cur_state
                global_data.game_mgr.show_tip(get_text_by_id(635074))
            return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_login_reconnect_event': self.on_net_reconnect,
           'net_reconnect_event': self.on_net_reconnect
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_net_reconnect(self):
        self.register_timer()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/NetworkWidget.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
from common.utils import network_utils
SIGNAL_RES_PATTERN = 'gui/ui_res_2/battle/icon/signal_%s_%d.png'
SIGNAL_LOST_RES = 'gui/ui_res_2/battle/icon/signal_cut.png'
import game3d
COLOR_MAP = {1: '#SR',
   2: '#SO',
   3: '#SW'
   }

class NetworkWidget(object):

    def __init__(self, panel):
        super(NetworkWidget, self).__init__()
        self.map_panel = panel
        self.title_widget = panel.temp_title
        self.init_event()
        self.cnt_delay = 0
        self.update_network_type()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 40)
        self.on_update()

    def update_network_type(self):
        self.cnt_network_type = network_utils.g93_get_network_type()

    def init_event(self):
        global_data.emgr.net_delay_time_event += self.update_network_delay
        global_data.emgr.net_disconnect_event += self.on_net_disconnect
        global_data.emgr.net_reconnect_event += self.on_net_reconnect
        global_data.emgr.net_login_reconnect_event += self.on_net_reconnect

    def uninit_event(self):
        global_data.emgr.net_delay_time_event -= self.update_network_delay
        global_data.emgr.net_disconnect_event -= self.on_net_disconnect
        global_data.emgr.net_reconnect_event -= self.on_net_reconnect
        global_data.emgr.net_login_reconnect_event -= self.on_net_reconnect

    def destroy(self):
        self.title_widget = None
        self.map_panel = None
        self.uninit_event()
        global_data.game_mgr.unregister_logic_timer(self.timer_id)
        return

    def on_update(self):
        self.update_network_type()
        self.update_widget()

    def update_widget(self):
        pic_path = SIGNAL_LOST_RES
        intensity = 1
        if self.cnt_network_type != network_utils.TYPE_INVALID:
            intensity = 3 if self.cnt_delay < 100 else (2 if self.cnt_delay < 250 else 1)
            net_type = 'wifi' if self.cnt_network_type == network_utils.TYPE_WIFI else 'move'
            pic_path = SIGNAL_RES_PATTERN % (net_type, intensity)
        self.title_widget.signal_img.SetDisplayFrameByPath('', pic_path)
        self.title_widget.lab_signal.SetColor(COLOR_MAP[intensity])
        self.title_widget.lab_signal.SetString('{0}ms'.format(min(999, self.cnt_delay)))

    def update_network_delay(self, rtt_type, rtt):
        if not global_data.player:
            return
        if tutil.TYPE_BATTLE == rtt_type or global_data.player.is_in_global_spectate():
            self.cnt_delay = int(rtt * 1000)
            self.update_widget()

    def on_net_disconnect(self):
        self.title_widget.signal_img.setVisible(False)
        self.title_widget.nd_connecting.setVisible(True)
        self.title_widget.PlayAnimation('connecting')

    def on_net_reconnect(self, *args):
        self.title_widget.nd_connecting.setVisible(False)
        self.title_widget.StopAnimation('connecting')
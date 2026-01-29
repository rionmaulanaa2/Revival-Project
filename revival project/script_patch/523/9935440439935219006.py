# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/NetworkLagUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities
from common.const import uiconst

class NetworkLagUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/network_loading'
    DLG_ZORDER = common.const.uiconst.TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = common.const.uiconst.UI_TYPE_SPECIAL
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'net_lag_warn_event': 'on_net_lag_warn',
       'net_lag_clear_event': 'on_net_lag_clear',
       'net_reconnect_event': 'on_net_lag_clear',
       'net_login_reconnect_event': 'on_net_lag_clear'
       }

    def on_init_panel(self, *args, **kargs):
        self.panel.RecordAnimationNodeState('network_loading_1')
        self.panel.RecordAnimationNodeState('network_loading_2')
        self.leave_screen()

    def on_net_lag_warn(self, where):
        self.enter_screen()
        if global_data.player and global_data.player.is_in_battle():
            ani_name = 'network_loading_1'
        else:
            ani_name = 'network_loading_2'
        if not self.panel.IsPlayingAnimation(ani_name):
            self.panel.PlayAnimation(ani_name)

    def on_net_lag_clear(self):
        self.leave_screen()
        if not self.panel.IsPlayingAnimation('network_loading_1'):
            self.panel.StopAnimation('network_loading_1')
            self.panel.RecoverAnimationNodeState('network_loading_1')
        if not self.panel.IsPlayingAnimation('network_loading_2'):
            self.panel.StopAnimation('network_loading_2')
            self.panel.RecoverAnimationNodeState('network_loading_2')
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/KnockoutUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class KnockoutUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_point/fight_point_mode_die'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, close_cb=None):
        self.close_cb = close_cb
        self.init_parameters()
        self.init_event()
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.show_main_ui()

    def init_parameters(self):
        pass

    def init_event(self):
        pass

    def on_delay_close(self, _cb):
        self.panel.PlayAnimation('break')
        alltime = self.panel.GetAnimationMaxRunTime('break')

        def refresh_time(pass_time):
            pass

        def refresh_time_finsh():
            self.close()
            _cb and _cb()

        self.panel.StopTimerAction()
        self.panel.TimerAction(refresh_time, alltime, callback=refresh_time_finsh)
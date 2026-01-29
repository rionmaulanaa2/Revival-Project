# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingBattleBeginUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class KingBattleBeginUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/koth_begin'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.panel.nd_time.StopTimerAction()

    def init_parameters(self):
        self.last_left_time = None
        return

    def init_event(self):
        pass

    def on_delay_close(self, revive_time):
        self.pass_time = 0
        self.panel.StopAnimation('count')
        self.is_run_count_ani = False

        def refresh_time(pass_time):
            left_time = int(revive_time - pass_time)
            if left_time <= 5 and not self.is_run_count_ani:
                self.panel.PlayAnimation('count')
                self.is_run_count_ani = True
            if left_time <= 5:
                if self.last_left_time is None or self.last_left_time != left_time:
                    self.last_left_time = left_time
                    global_data.sound_mgr.play_ui_sound('resurrection_countdown')
            if left_time < 0:
                self.panel.setVisible(False)
            self.panel.lab_time.SetString(str(left_time) + 'S')
            self.panel.lab_time_dec.SetString(str(left_time) + 'S')
            return

        def refresh_time_finsh():
            self.panel.lab_time.SetString(str(0) + 'S')
            self.panel.lab_time_dec.SetString(str(0) + 'S')
            self.close()

        self.panel.nd_time.StopTimerAction()
        self.panel.nd_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)
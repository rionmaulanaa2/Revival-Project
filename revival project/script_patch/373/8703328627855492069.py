# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathBeginCountDown.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.cfg import confmgr
from logic.gutils import item_utils
import math
from common.const import uiconst

class DeathBeginCountDown(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_tdm/tdm_begin_count_down'

    def on_init_panel(self):
        self.panel.nd_locate.ResizeAndPosition(include_self=False)

    def on_finalize_panel(self):
        pass

    def on_delay_close(self, revive_time):

        def refresh_time_finsh():
            self.panel.lab_time.SetString(str(0))
            self.count_down_end()

        def refresh_time(pass_time):
            if not self.panel:
                return
            left_time = int(math.ceil(revive_time - pass_time))
            self.panel.lab_time.SetString(str(left_time))
            if left_time <= 0:
                self.panel.StopTimerAction()
                refresh_time_finsh()
                return

        self.panel.StopTimerAction()
        if revive_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        global_data.emgr.death_count_down_start.emit()
        self.panel.TimerAction(refresh_time, revive_time, interval=0.1)

    def count_down_end(self):
        self.close()
        global_data.emgr.death_count_down_over.emit()
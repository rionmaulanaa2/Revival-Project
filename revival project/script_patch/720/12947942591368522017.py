# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/ThrowProgressUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst

class ThrowProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'fight_progress_throw'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.panel.nd_progress_throw.setVisible(False)
        self._total_time = 1
        self._cur_time = 1
        self.timer = None
        self._finish_callback = None
        return

    def show_progress(self, time, finish_callback):
        if time <= 0:
            self.panel.nd_progress_throw.setVisible(False)
            self._finish_callback = None
            self._cur_time = 0
            if finish_callback:
                finish_callback()
            return
        else:
            self._total_time = time
            self._cur_time = time
            self._finish_callback = finish_callback
            self.panel.nd_progress_throw.setVisible(True)
            tm = global_data.game_mgr.get_logic_timer()
            from common.utils.timer import CLOCK
            self._collision_check_timer = tm.register(func=self.update_progress, interval=0.1, times=int(self._total_time * 10), mode=CLOCK)
            return

    def update_progress(self):
        self._cur_time -= 0.1
        if self._cur_time < 0.1 and self.panel.nd_progress_throw.isVisible():
            self.panel.nd_progress_throw.setVisible(False)
            if self._finish_callback:
                self._finish_callback()
            return
        self.set_progress()

    def set_progress(self):
        progress_throw = self.panel.nd_progress_throw
        progress_throw.lab_time.SetString('{:.1f}'.format(self._cur_time))
        progress_throw.progress.SetPercentage(int(100.0 * self._cur_time / self._total_time))
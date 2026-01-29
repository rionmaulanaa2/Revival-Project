# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/GroundedUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.utils import timer
import time
from common.const import uiconst

class GroundedUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_ground'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kargs):
        self._cur_time = 10.0
        self._all_time = 10.0
        self.timer = None
        return

    def set_cd_time(self, cd_time):
        self._cur_time = cd_time
        self._all_time = cd_time
        if self._all_time > 0:
            self.show()
        else:
            self.hide()

    def update_callback(self, dt):
        if self._cur_time <= 0:
            self.hide()
            return
        self._cur_time = max(0.0, self._cur_time - dt)
        per = int(self._cur_time * 100 / self._all_time)
        self.panel.nd_pro.pro.setPercent(per)

    def destroy_timer(self):
        if not self.timer:
            return
        else:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
            return

    def do_show_panel(self):
        super(GroundedUI, self).do_show_panel()
        if not self.timer:
            self.timer = global_data.game_mgr.register_logic_timer(self.update_callback, interval=1, timedelta=True)

    def do_hide_panel(self):
        super(GroundedUI, self).do_hide_panel()
        self.destroy_timer()

    def on_finalize_panel(self):
        self.destroy_timer()
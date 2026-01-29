# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAFinishCountDown.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst
from logic.comsys.battle.ffa.FFAFinishCountDownWidget import FFAFinishCountDownWidget

class FFAFinishCountDown(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_ffa/battle_finish_time'

    def on_init_panel(self):

        def count_down_end_cb():
            self.close()

        self._widget = FFAFinishCountDownWidget(self.panel, count_down_end_cb)
        self._widget.on_init_panel()

    def on_finalize_panel(self):
        self._widget.on_finalize_panel()
        self._widget = None
        return

    def on_delay_close(self, revive_time):
        self._widget.on_delay_close(revive_time)
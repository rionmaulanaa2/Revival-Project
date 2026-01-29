# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoReport.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_TYPE_MESSAGE

class BattleInfoReport(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle/fight_enermy_down'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE

    def process_one_message(self, message, finish_cb):
        time = self.panel.GetAnimationMaxRunTime('down')

        def finished():
            if self and self.is_valid():
                self.panel.setVisible(False)
                self.finish_cb()

        self.panel.StopAnimation('down')
        self.panel.SetTimeOut(time, finished)
        self.panel.PlayAnimation('down')
        self.panel.setVisible(True)
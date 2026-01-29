# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/GulagBattleInfoUI.py
from __future__ import absolute_import
from .BattleInfoUI import BattleInfoUI

class GulagBattleInfoUI(BattleInfoUI):

    def init_parameters(self):
        super(GulagBattleInfoUI, self).init_parameters()
        global_data.emgr.refresh_gulag_poison_circle += self.refresh_gulag_poison_circle

    def refresh_gulag_poison_circle(self, game_id, show_info):
        if not global_data.cam_lplayer:
            return
        cam_game_id = global_data.cam_lplayer.ev_g_gulag_game_id()
        if cam_game_id != game_id:
            return
        if not show_info:
            return
        self.refresh_poison_circle(**show_info)

    def on_finalize_panel(self):
        super(GulagBattleInfoUI, self).on_finalize_panel()
        global_data.emgr.refresh_gulag_poison_circle -= self.refresh_gulag_poison_circle
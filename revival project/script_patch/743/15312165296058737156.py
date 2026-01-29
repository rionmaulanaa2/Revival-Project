# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CNewbieStageMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CNormalMode import CNormalMode

class CNewbieStageMode(CNormalMode):

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()
        global_data.death_battle_data and global_data.death_battle_data.finalize()
        global_data.death_battle_door_col and global_data.death_battle_door_col.finalize()
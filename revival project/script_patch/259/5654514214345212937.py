# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Train/TrainSkillUIPC.py
from __future__ import absolute_import
from .TrainSkillUI import TrainSkillUI

class TrainSkillUIPC(TrainSkillUI):

    def on_init_panel(self):
        super(TrainSkillUIPC, self).on_init_panel()
        self.panel.temp_pc.setVisible(True)
        self.panel.temp_pc.pc_tip_list.SetInitCount(1)
        self.panel.temp_pc.pc_tip_list.GetItem(0).lab_pc.SetString('H')
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag2/Flag2PlantProgUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id

class Flag2PlantProgUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_flagsnatch2/battle_flagsnatch2_prog_tips'
    GLOBAL_EVENT = {'flagsnatch_flag_plant_state_change': '_on_plant_state_change',
       'flagsnatch_flag_plant_point_change': '_on_plant_point_change',
       'flagsnatch_flag_recover': '_on_flag_recover'
       }

    def on_init_panel(self):
        self.is_showing = False
        self.lab_1.setVisible(False)

    def show_prog_anim(self, is_show):
        if is_show and not self.is_showing:
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('appear')
            self.is_showing = True
        if not is_show and self.is_showing:
            self.panel.StopAnimation('disappear')
            self.panel.PlayAnimation('disappear')
            self.is_showing = False

    def _on_plant_state_change(self, is_start_plant, faction_id, flag_picker_id):
        if flag_picker_id != global_data.player.id:
            return
        if is_start_plant:
            self.show_prog_anim(True)

    def _on_flag_recover(self, holder_id, holder_faction, reason):
        if holder_id != global_data.player.id:
            return
        self.show_prog_anim(False)

    def _on_plant_point_change(self, point, total_point, faction_id, flag_picker_id):
        if flag_picker_id != global_data.player.id:
            return
        if total_point and total_point > 0:
            percent = point / total_point * 100.0
        else:
            percent = 0
        self.panel.prog.SetPercent(percent)
        self.show_prog_anim(percent > 0 and percent < 100)
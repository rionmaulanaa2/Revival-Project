# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownMarkUI.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.comsys.battle.Crown.CrownMarkWidget import CrownMarkWidget
from logic.gcommon.common_const.battle_const import CROWN_BATTLE_CROWN_TEAMMATE_LOCATE_UI, CROWN_BATTLE_CROWN_SELF_LOCATE_UI, CROWN_BATTLE_CROWN_OTHER_LOCATE_UI
OTHER_FACTION = 1
TEAMMATE_FACTION = 2
SELF_FACTION = 3
TEAMMATE_MARK = 2041
OTHER_MAKR = 2042
SELF_MARK = 2043

class CrownMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_mark_icon()

    def init_parameters(self):
        self.mark_widgets = []
        if global_data.player and global_data.battle:
            global_data.battle.call_soul_method('request_crown_info_all', (global_data.player.id,))

    def on_finalize_panel(self):
        for tmp_mark_widget in self.mark_widgets:
            tmp_mark_widget.on_finalize()

        self.mark_widgets = []

    def init_mark_icon(self):
        if global_data.battle and global_data.battle.is_settle:
            return
        else:
            self.mark_widgets.append(CrownMarkWidget(self.panel, CROWN_BATTLE_CROWN_OTHER_LOCATE_UI, OTHER_FACTION, OTHER_MAKR))
            self.mark_widgets.append(CrownMarkWidget(self.panel, CROWN_BATTLE_CROWN_TEAMMATE_LOCATE_UI, TEAMMATE_FACTION, TEAMMATE_MARK))
            self.mark_widgets.append(CrownMarkWidget(self.panel, None, SELF_FACTION, SELF_MARK))
            return
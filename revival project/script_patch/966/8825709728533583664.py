# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombStartReadyUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.NBomb import nbomb_utils
from common.const import uiconst

class NBombStartReadyUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_bomb/i_battle_bomb_tip_start'
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.update_display()

    def on_finalize_panel(self):
        pass

    def update_display(self):
        bg_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_countdown_0.png'
        self.bar.SetDisplayFrameByPath('', bg_path)
        self.lab_title.setString(get_text_by_id(18356))

    def set_sub_title(self, tips):
        self.lab_title2.setString(tips)
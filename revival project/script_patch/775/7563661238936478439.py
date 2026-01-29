# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeWeaponRefreshUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id

class ScavengeWeaponRefreshUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_pick_up/battle_pick_weapon_refresh'
    GLOBAL_EVENT = {'show_scavenge_item_refreshed_event': 'show_refresh'
       }
    SHOW_TIME = 1.0
    EXIST_TIME = 2.0

    def on_init_panel(self, *args):
        pass

    def on_finalize_panel(self):
        pass

    def show_refresh(self, item_id):
        self.panel.PlayAnimation('appear')

        def finished_break():
            self.panel.StopAnimation('appear')
            self.panel.PlayAnimation('disappear')

        def finished_show():
            global_data.ui_mgr.close_ui('ScavengeWeaponRefreshUI', 'logic.comsys.battle.Scavenge')

        self.panel.SetTimeOut(self.SHOW_TIME, finished_break)
        self.panel.SetTimeOut(self.EXIST_TIME, finished_show)
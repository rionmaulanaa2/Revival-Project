# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/SnatchEggGuideUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_NO_EFFECT, UI_VKB_CLOSE

class SnatchEggGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_golden_egg/guide_human_golden_egg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'snatchegg_egg_pick_up': '_on_egg_pick_up',
       'snatchegg_round_begin_event': 'snatchegg_round_begin'
       }

    def on_init_panel(self):
        pass

    def _on_egg_pick_up(self, picker_id, picker_faction, npc_id):
        if not global_data.player:
            return
        if picker_id == global_data.player.id:
            show_guide_name = 'SnatchEggGuideUI' + str(global_data.player.uid)
            show_guide_ui = global_data.achi_mgr.get_cur_user_archive_data(show_guide_name, 0)
            if show_guide_ui < 3:
                self.panel.PlayAnimation('show_step_4')
                global_data.achi_mgr.set_cur_user_archive_data(show_guide_name, show_guide_ui + 1)
        show_throw_name = 'SnatchEggGuideUI_eggthrow'
        show_throw = global_data.achi_mgr.get_cur_user_archive_data(show_throw_name, False)
        if not show_throw:
            self.panel.SetTimeOut(3.0, self.show_egg_throw)

    def snatchegg_round_begin(self):
        if not global_data.battle:
            return
        round_idx = global_data.battle.get_snatchegg_round()
        if round_idx == 0:

            def cb():
                self.panel.PlayAnimation('show_step_1')

            self.panel.SetTimeOut(3.0, cb)

    def show_egg_throw(self):
        if not global_data.death_battle_data:
            return
        if not global_data.player:
            return
        if global_data.player.id in global_data.death_battle_data.egg_picker_dict:
            show_throw_name = 'SnatchEggGuideUI_eggthrow'
            global_data.achi_mgr.set_cur_user_archive_data(show_throw_name, True)
            self.panel.PlayAnimation('show_step_3')
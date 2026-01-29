# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag/FlagThrowUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import math
import math3d
from common.const import uiconst

class FlagThrowUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_flag_throw'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_squat.OnClick': '_on_click_drop_btn'
       }
    HOT_KEY_FUNC_MAP = {'flag_drop_flag.DOWN_UP': '_on_click_drop_btn'
       }

    def on_init_panel(self):
        self.init_custom_com()
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_flag_pick_up': self._on_flag_pick_up,
           'flagsnatch_flag_recover': self._on_flag_recover
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_flag_pick_up(self, picker_id, picker_faction, *args):
        if picker_id == global_data.player.id:
            self.panel.nd_squat.setVisible(True)

    def _on_flag_recover(self, *args):
        self.panel.nd_squat.setVisible(False)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')
        self.process_event(False)

    def _on_click_drop_btn(self, *args):
        flag_id = global_data.death_battle_data.flag_ent_id
        if not global_data.battle:
            return
        flag = global_data.battle.get_entity(flag_id)
        if flag:
            flag.logic.send_event('E_TRY_DROP_FLAG')
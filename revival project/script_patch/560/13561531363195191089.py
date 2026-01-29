# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaWaitUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils import item_utils
from random import shuffle
from mobile.common.EntityManager import EntityManager
import cc

class ArenaWaitUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arena/battle_arena_btn'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_solo.OnClick': 'on_btn_solo_click'
       }
    HOT_KEY_FUNC_MAP = {'concert_wait_btn': 'keyboard_concert_wait_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'concert_wait_btn': {'node': 'btn_solo.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_panel()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_stage': self.update_battle_stage
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_panel(self):
        self.update_battle_stage()

    def update_battle_stage(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        show_btn_solo = bat.is_wait_duel_stage() or bat.is_wait_player()
        self.panel.btn_solo.setVisible(show_btn_solo)
        if not show_btn_solo:
            global_data.ui_mgr.close_ui('ArenaApplyUI')
        self.panel.lab_wait_tips.setVisible(bat.is_wait_duel_stage() and bat.is_king())

    def keyboard_concert_wait_btn(self, msg, keycode):
        if self.panel.btn_solo.isVisible():
            self.panel.btn_solo.OnClick(self.panel.btn_solo)

    def on_btn_solo_click(self, btn, touch):
        global_data.ui_mgr.show_ui('ArenaApplyUI', 'logic.comsys.concert')
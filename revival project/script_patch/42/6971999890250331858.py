# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaTopUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from mobile.common.EntityManager import EntityManager
from logic.gutils import role_head_utils
from logic.gcommon import time_utility as tutil
import math

class ArenaTopUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_solo/fight_top_score'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.panel.lab_time.StopTimerAction()
        self.process_event(False)

    def init_panel(self):
        self.panel.nd_prog_blue.prog_blue.SetPercentage(0)
        self.panel.nd_prog_red.prog_red.SetPercentage(0)
        self.refresh_player_info()
        self.on_count_down()

    def refresh_player_info(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        king, defier, _, _ = bat.get_battle_data()
        is_king = bat.is_king()
        if is_king:
            blue_camp = king
            red_camp = defier
        else:
            blue_camp = defier
            red_camp = king
        self.update_photo(self.panel.temp_head_blue, blue_camp)
        self.update_photo(self.panel.temp_head_red, red_camp)

    def update_photo(self, ui_item, entity_id):
        if not entity_id:
            return
        player = EntityManager.getentity(entity_id)
        if not (player and player.logic):
            return
        char_name = player.logic.ev_g_char_name()
        head_frame = player.logic.ev_g_head_frame()
        head_photo = player.logic.ev_g_head_photo()
        role_head_utils.init_role_head(ui_item, head_frame, head_photo)

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        self.left_time = None
        return

    def on_count_down(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        _, _, duel_end_time = bat.get_duel_info()
        revive_time = 0
        if duel_end_time:
            revive_time = int(duel_end_time - tutil.time())

        def refresh_time(pass_time):
            if global_data.death_battle_data and global_data.death_battle_data.is_ready_state:
                return
            left_time = revive_time - pass_time
            left_time = int(math.ceil(left_time))
            if self.left_time == left_time:
                return
            self.left_time = left_time
            left_time = tutil.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)
            self.panel.lab_time_vx.SetString(left_time)

        def refresh_time_finsh():
            left_time = tutil.get_delta_time_str(0)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.StopTimerAction()
        refresh_time(0)
        self.panel.lab_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=0.5)
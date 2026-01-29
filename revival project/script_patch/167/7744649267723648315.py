# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/BeaconTowerOccupyUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import battle_const
from common.const import uiconst

class BeaconTowerOccupyUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_mech_charge'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self._timer = None
        self.on_hide()
        self.panel.progress_charge_increase.SetPercentage(0)
        self.panel.nd_charge.lab_desc.SetString(get_text_by_id(17013))
        self.panel.nd_charge.lab_time.SetString('')
        self.init_parameters()
        return

    def on_finalize_panel(self):
        self.on_hide()
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        self.spectate_target = None
        if global_data.player and global_data.player.logic:
            self.spectate_target = global_data.player.logic.ev_g_spectate_target()
        if self.spectate_target and self.spectate_target.logic:
            self.on_player_setted(self.spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self.on_player_setted
        econf = {'on_observer_occupy_change_process': self.on_update_occupy_process
           }
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.player = player

    def on_update_occupy_process(self, occupy_state, total_cd, left_time):
        if occupy_state == battle_const.BEACON_OCCUPY_ON:
            self.on_show(total_cd, left_time)
        elif occupy_state == battle_const.BEACON_OCCUPY_STOP:
            self.on_hide()
        elif occupy_state == battle_const.BEACON_OCCUPY_SUCC:
            self.on_hide()

    def show_progress_catch_up(self, cur_percent, left_time):
        FRAMES = 20
        self.panel.progress_charge.SetPercentage(cur_percent)
        SPEED = (100 - cur_percent) / FRAMES / left_time

        def cb(dt):
            cur_percent = self.panel.progress_charge.getPercentage()
            new_percent = min(cur_percent + SPEED, 100)
            self.panel.progress_charge.SetPercentage(new_percent)

        self.panel.nd_charge.StopTimerAction()
        self._timer = self.panel.nd_charge.TimerAction(cb, left_time, interval=0.05)

    def on_show(self, total_cd, left_time):
        percent = self.get_percent(total_cd, left_time)
        self.show_progress_catch_up(percent, left_time)
        self.add_show_count(self.__class__.__name__)

    def on_hide(self):
        self.add_hide_count(self.__class__.__name__)
        if self._timer:
            self._timer = None
        self.panel.nd_charge.StopTimerAction()
        return

    def get_percent(self, total_cd, left_time):
        if left_time >= 0:
            percent = 100 * (1 - float(left_time) / total_cd)
        else:
            percent = 100
        return percent
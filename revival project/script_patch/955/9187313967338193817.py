# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaChargeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import mecha_const
from common.const import uiconst

class MechaChargeUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_mech_charge'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'scene_player_setted_event': 'on_player_setted',
       'scene_observed_player_setted_event': 'on_player_setted',
       'net_reconnect_event': 'hide',
       'on_observer_charging_event': 'on_observer_charging',
       'on_observer_state_change_cd': 'on_update_change_cd',
       'set_observe_target_id_event': 'on_observe_target_changed',
       'charger_user_count_changed': 'on_charger_user_count_changed'
       }

    def on_init_panel(self):
        self._timer = None
        self.on_hide()
        self.init_parameters()
        self._on_charging = False
        self._charge_left_time = 0
        self._recall_cd_rate = 1
        self._charger = None
        self.panel.lab_time.SetString('')
        return

    def on_finalize_panel(self):
        self.on_hide()
        self.player = None
        return

    def init_parameters(self):
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        self.spectate_target = None
        self.cur_end_time = 0
        self.total_cd_time = 0
        self.cd_type = 0
        self._charger_available_time = 0
        if global_data.player and global_data.player.logic:
            self.spectate_target = global_data.player.logic.ev_g_spectate_target()
        if self.spectate_target and self.spectate_target.logic:
            self.on_player_setted(self.spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        return

    def on_player_setted(self, player):
        self.player = player
        if not player:
            return
        com = player.get_com('ComCtrlMecha')
        if com:
            self._recall_cd_rate = com._recall_cd_rate

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        percent = self.get_percent(cd_type, total_cd, left_time)
        self.panel.progress_charge.SetPercentage(percent)
        self.show_progress()

    def show_progress(self):
        left_time = 2

        def reset():
            self._timer = None
            if not self._on_charging:
                self.on_hide()
            else:
                if self._timer:
                    self._timer = None
                self.panel.StopTimerAction()
            return

        def cb(dt):
            new_percent = self.get_percent(self.cd_type, self.total_cd_time, self.cur_end_time - time.time())
            self.panel.progress_charge.SetPercentage(new_percent)
            cur_left_time = self.get_cur_left_time()
            charger_time = self.get_charge_available_time()
            self.panel.lab_time.SetString('%.0fs' % min(cur_left_time, charger_time))
            if self.total_cd_time > 0:
                progress = 100 * (1 - float(cur_left_time - charger_time) * self.get_recall_rate() / self.total_cd_time)
            else:
                progress = 100
            cur_target_percentage = self.panel.progress_charge_increase.getPercentage()
            if abs(cur_target_percentage - progress) > 1:
                self.panel.progress_charge_increase.SetPercentage(min(progress, 100))
            if new_percent >= 100:
                reset()

        self._start_time = time.time()
        self.panel.StopTimerAction()
        self._timer = self.panel.TimerAction(cb, left_time, reset, interval=0.1)

    def on_observer_charging(self, is_on_charging, bf_data):
        if bf_data:
            if is_on_charging and not self._on_charging:
                self.on_hide()
            return
        self._on_charging = is_on_charging
        if is_on_charging:
            self.on_show()
        else:
            self.on_hide()

    def on_show(self):
        if self.player:
            cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
            percent = self.get_percent(cd_type, total_cd, left_time)
            self.panel.progress_charge.SetPercentage(percent)
        self.add_show_count(self.__class__.__name__)

    def on_hide(self):
        self.add_hide_count(self.__class__.__name__)
        if self._timer:
            self._timer = None
        self.panel.StopTimerAction()
        return

    def on_observe_target_changed(self, *args):
        if not self.player:
            return
        else:
            if not global_data.player:
                return
            spectate_target = global_data.player.logic.ev_g_spectate_target()
            if not spectate_target or not spectate_target.logic:
                return
            charging_state = spectate_target.logic.ev_g_charging_state()
            if charging_state is not None:
                if not charging_state:
                    self.on_hide()
                else:
                    self.on_show()
            return

    def get_recall_rate(self):
        charge_rate = 0 if self._charger is None else self._charger._charge_rate
        return self._recall_cd_rate + charge_rate

    def get_cur_left_time(self):
        return max(self.cur_end_time - time.time(), 0) / float(self.get_recall_rate())

    def get_charge_available_time(self):
        if self._charger and len(self._charger._charging_target_infos) > 0:
            charger_time = self._charger._energy / (float(len(self._charger._charging_target_infos)) * self._charger._charge_rate)
        else:
            charger_time = 0
        return charger_time

    def get_percent(self, cd_type, total_cd, left_time):
        self.cur_end_time = time.time() + left_time
        self.total_cd_time = total_cd
        self.cd_type = cd_type
        if total_cd <= 0.1:
            return 100
        if cd_type in [mecha_const.RECALL_CD_TYPE_GETMECHA, mecha_const.RECALL_CD_TYPE_DIE] and left_time >= 0:
            percent = 100 * (1 - float(left_time) / total_cd)
        else:
            percent = 100
        return percent

    def sync_mecha_percent(self, progress):
        self.panel.progress_charge.SetPercentage(progress)

    def on_charger_user_count_changed(self, charger):
        self._charger = charger
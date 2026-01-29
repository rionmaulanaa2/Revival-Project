# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaChargeWidget.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import mecha_const

class MechaChargeWidget(object):
    PANEL_CONFIG_NAME = 'battle/fight_mech_charge'
    DLG_ZORDER = BASE_LAYER_ZORDER

    def __init__(self, panel):
        self.panel = panel
        self._timer = None
        self.init_parameters()
        return

    def get_events(self):
        econf = {'scene_player_setted_event': self.on_player_setted,
           'on_observer_state_change_cd': self.on_update_change_cd
           }
        return econf

    def destroy(self):
        self.on_hide()
        emgr = global_data.emgr
        econf = self.get_events()
        emgr.unbind_events(econf)
        self.panel = None
        self.player = None
        return

    def init_parameters(self):
        self.speed_rate = 1
        self.speed_up = mecha_const.RECALL_MAXCD_TYPE_GETMECHA / 2
        self._target_percent = 0
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        if global_data.player and global_data.player.logic:
            self.on_player_setted(player)
        econf = self.get_events()
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.player = player
        self.on_show()

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        self.get_mecha_count_down = left_time
        self.get_mecha_total_cd = total_cd
        if self._timer:
            return
        if left_time > 0:
            tick_interval = 0.03

            def reset():
                if self.panel and self.panel.isValid():
                    self.get_mecha_count_down = 0
                    self.get_mecha_count_down_progress = 0
                    if self.get_mecha_cd_timer:
                        self.panel.stopAction(self.get_mecha_cd_timer)
                        self.get_mecha_cd_timer = None
                        self.panel.progress_call.SetPercentage(100)
                        self.panel.lab_call.SetString('%d%%' % int(100))
                        self.panel.img_full.setVisible(True)
                return

            def cb(dt):
                if self.get_mecha_count_down < self.get_mecha_count_down_progress:
                    self.get_mecha_count_down_progress -= tick_interval * self.speed_up * self.speed_rate
                    if self.get_mecha_count_down_progress < self.get_mecha_count_down:
                        self.get_mecha_count_down_progress = self.get_mecha_count_down
                else:
                    self.get_mecha_count_down_progress -= tick_interval * self.speed_rate
                if self.get_mecha_count_down_progress <= 0:
                    reset()
                else:
                    new_percent = self.get_percent(cd_type, total_cd, self.get_mecha_count_down_progress)
                    self.panel.progress_call.SetPercentage(new_percent)
                    self.panel.lab_call.SetString('%d%%' % int(new_percent))

            self.get_mecha_count_down_progress = left_time
            self.panel.StopTimerAction()
            self.get_mecha_cd_timer = self.panel.TimerAction(cb, left_time, reset, interval=tick_interval)
        elif left_time <= 0:
            self.panel.progress_call.SetPercentage(100)
            self.panel.lab_call.SetString('%d%%' % int(100))
            self.panel.img_full.setVisible(True)

    def on_show(self):
        if self.player:
            cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
            percent = self.get_percent(cd_type, total_cd, left_time)
            self.panel.progress_call.SetPercentage(percent)
            self.panel.lab_call.SetString('%d%%' % int(percent))
            if percent < 100:
                self.panel.img_full.setVisible(False)
            self.on_update_change_cd(cd_type, total_cd, left_time)

    def on_hide(self):
        if self._timer:
            self._timer = None
        self.panel.StopTimerAction()
        return

    def get_percent(self, cd_type, total_cd, left_time):
        if total_cd <= 0.1:
            return 100
        if cd_type in [mecha_const.RECALL_CD_TYPE_GETMECHA, mecha_const.RECALL_CD_TYPE_DIE] and left_time >= 0:
            percent = 100 * (1 - float(left_time) / total_cd)
        else:
            percent = 100
        return percent
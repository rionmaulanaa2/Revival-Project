# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/PrepareCountDownWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon import time_utility as tutil
COUNTDOWN_TAG = 1

class PrepareCountDownWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, *args, **kwargs):
        self.nd_countdown = panel.nd_info
        self.global_events = {'on_battle_status_changed': self.on_battle_status_changed
           }
        super(PrepareCountDownWidget, self).__init__(parent_ui, panel, *args, **kwargs)
        self.end_ts = 0
        self.reset_widget()

    def reset_widget(self):
        battle = global_data.player.get_battle()
        if not battle:
            return
        self.nd_countdown.stopActionByTag(COUNTDOWN_TAG)
        if not global_data.cam_lplayer.ev_g_is_parachute_stage_plane():
            self.nd_countdown.setVisible(False)
        else:
            plane_id = battle.plane_id
            plane = battle.get_entity(plane_id)
            if plane and plane.logic:
                self.init_countdown(plane.logic.ev_g_plane_arrived_end_timestamp())
            else:
                self.nd_countdown.setVisible(False)

    def on_battle_status_changed(self, *args):
        self.reset_widget()

    def init_countdown(self, end_ts):
        self.nd_countdown.setVisible(True)
        self.end_ts = end_ts
        self.update_countdown()
        self.nd_countdown.DelayCallWithTag(1, self.update_countdown, COUNTDOWN_TAG)

    def update_countdown(self):
        if self.end_ts is None:
            player = global_data.player
            if not player:
                return True
            battle = global_data.player.get_battle()
            if not battle:
                return True
            plane_id = battle.plane_id
            plane = battle.get_entity(plane_id)
            if plane and plane.logic:
                self.end_ts = plane.logic.ev_g_plane_arrived_end_timestamp()
            if self.end_ts is None:
                return True
        delta = max(0, self.end_ts - tutil.get_server_time())
        str_time = tutil.get_delta_time_str(delta)[3:]
        self.nd_countdown.lab_time.SetString(str_time)
        if delta <= 0 or delta > 10.0:
            self.nd_countdown.lab_time1.setVisible(False)
            if self.panel.IsPlayingAnimation('daojishi'):
                self.panel.StopAnimation('daojishi')
        else:
            self.nd_countdown.lab_time1.SetString(str_time)
            self.nd_countdown.lab_time1.setVisible(True)
            if not self.panel.IsPlayingAnimation('daojishi'):
                self.panel.PlayAnimation('daojishi')
        return delta > 0

    def destroy(self):
        self.nd_countdown.stopActionByTag(COUNTDOWN_TAG)
        self.nd_countdown = None
        super(PrepareCountDownWidget, self).destroy()
        return
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ArmRace/ArmRaceBeginCountDownWidget.py
from __future__ import absolute_import
import six_ex
import math
from logic.client.const import game_mode_const
MODE_2_TOP_SCORE_UI = {game_mode_const.GAME_MODE_DEATH: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_MECHA_DEATH: 'MechaDeathTopScoreUI',
   game_mode_const.GAME_MODE_CLONE: 'CloneTopScoreUI',
   game_mode_const.GAME_MODE_SNIPE: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_HUMAN_DEATH: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_FLAG: 'FlagTopScoreUI',
   game_mode_const.GAME_MODE_CROWN: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_SCAVENGE: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_GOOSE_BEAR: 'MechaDeathTopScoreUI'
   }

class ArmRaceBeginCountDownWidget(object):

    def __init__(self, root_node):
        self.panel = root_node

    def on_init_panel(self):
        self._context = None
        self._count_down_end_cb = None
        return

    def on_finalize_panel(self):
        self.panel = None
        self._context = None
        self._count_down_end_cb = None
        return

    def set_context(self, context):
        self._context = context

    def get_context(self):
        return self._context

    def on_delay_close(self, revive_time, callback=None):
        self._count_down_end_cb = callback

        def refresh_time_finsh():
            self.panel.lab_time.SetString('G')
            self.panel.lab_time_big.SetString('G')
            if self._context == 'GVG':
                global_data.sound_mgr.play_ui_sound('ui_gvg_go')
            self.panel.PlayAnimation('appear')
            self.panel.SetTimeOut(1, lambda : self._count_down_end())

        def refresh_time(pass_time):
            if not self.panel:
                return
            left_time = int(math.ceil(revive_time - pass_time))
            self.panel.lab_time.SetString(str(left_time))
            self.panel.lab_time_big.SetString(str(left_time))
            self.set_top_score_ui_time(str(left_time))
            if self._context == 'GVG':
                if left_time in (3, 2, 1):
                    global_data.sound_mgr.play_ui_sound('ui_gvg_countdown')
            if left_time <= 0:
                self.panel.StopTimerAction()
                refresh_time_finsh()
                return
            self.panel.PlayAnimation('appear')

        self.panel.StopTimerAction()
        if revive_time <= 0:
            refresh_time(0)
            self._count_down_end()
            return
        refresh_time(0)
        global_data.emgr.death_count_down_start.emit()
        self.panel.TimerAction(refresh_time, revive_time, interval=1)

    def _count_down_end(self):
        if callable(self._count_down_end_cb):
            self._count_down_end_cb()

    def set_top_score_ui_time(self, text):
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type not in six_ex.keys(MODE_2_TOP_SCORE_UI):
            return
        if global_data.death_battle_data.is_ready_state:
            top_score_ui_name = MODE_2_TOP_SCORE_UI.get(mode_type)
            if not top_score_ui_name:
                return
            ui = global_data.ui_mgr.get_ui(top_score_ui_name)
            ui and ui.lab_time.SetString(text)
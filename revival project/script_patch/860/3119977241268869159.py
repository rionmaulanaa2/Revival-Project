# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFABeginCountDownWidget.py
from __future__ import absolute_import
import six_ex
import math
from logic.client.const import game_mode_const
from common.utils import timer
MODE_2_TOP_SCORE_UI = {game_mode_const.GAME_MODE_DEATH: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_MECHA_DEATH: 'MechaDeathTopScoreUI',
   game_mode_const.GAME_MODE_CLONE: 'CloneTopScoreUI',
   game_mode_const.GAME_MODE_SNIPE: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_HUMAN_DEATH: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_FLAG: 'FlagTopScoreUI',
   game_mode_const.GAME_MODE_CONTROL: 'OccupyBattleUI',
   game_mode_const.GAME_MODE_CROWN: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_CRYSTAL: 'CrystalTopScoreUI',
   game_mode_const.GAME_MODE_ADCRYSTAL: 'ADCrystalTopScoreUI',
   game_mode_const.GAME_MODE_SCAVENGE: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_TRAIN: 'DeathTopScoreUI',
   game_mode_const.GAME_MODE_SNATCHEGG: 'SnatchEggTopScoreUI',
   game_mode_const.GAME_MODE_GOOSE_BEAR: 'MechaDeathTopScoreUI',
   game_mode_const.GAME_MODE_ASSAULT: 'DeathTopScoreUI'
   }

class FFABeginCountDownWidget(object):

    def __init__(self, root_node):
        self.panel = root_node
        self.last_time = None
        self.start_show_time = None
        self.tick_sound = None
        self._need_ceil = False
        self.end_time_count_down_player_id = None
        return

    def on_init_panel(self):
        self._context = None
        self._count_down_end_cb = None
        return

    def on_finalize_panel(self):
        self.panel = None
        if self.end_time_count_down_player_id:
            global_data.sound_mgr.stop_playing_id(self.end_time_count_down_player_id)
            self.end_time_count_down_player_id = None
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
            if not (self.panel and self.panel.isValid()):
                return
            else:
                if self.end_time_count_down_player_id:
                    global_data.sound_mgr.stop_playing_id(self.end_time_count_down_player_id)
                    self.end_time_count_down_player_id = None
                self.last_time = 0
                if self._context == 'DUEL':
                    self._count_down_end()
                else:
                    self.panel.lab_time.SetString('G')
                    self.panel.lab_time_big.SetString('G')
                    if self._context == 'GVG':
                        global_data.sound_mgr.play_ui_sound('ui_gvg_go')
                    self.panel.PlayAnimation('appear')
                    global_data.game_mgr.get_logic_timer().register(func=self._count_down_end, mode=timer.CLOCK, interval=1, times=1)
                return

        def refresh_time(pass_time):
            if not (self.panel and self.panel.isValid()):
                return
            if not self._need_ceil:
                left_time = int(revive_time - pass_time)
            else:
                left_time = int(math.ceil(revive_time - pass_time))
            if self.last_time == left_time:
                return
            if left_time <= 0:
                self.panel.StopTimerAction()
                refresh_time_finsh()
                return
            self.last_time = left_time
            is_show = True
            if self.start_show_time:
                if left_time <= self.start_show_time:
                    is_show = True
                    self.panel.nd_time.setVisible(True)
                else:
                    is_show = False
                    self.panel.nd_time.setVisible(False)
            if is_show:
                if self.tick_sound:
                    if not self.end_time_count_down_player_id:
                        self.end_time_count_down_player_id = global_data.sound_mgr.play_sound(self.tick_sound)
            self.panel.lab_time.SetString(str(left_time))
            self.panel.lab_time_big.SetString(str(left_time))
            self.set_top_score_ui_time(str(left_time))
            if self._context == 'GVG':
                if left_time in (3, 2, 1):
                    global_data.sound_mgr.play_ui_sound('ui_gvg_countdown')
            self.panel.PlayAnimation('appear')

        self.panel.StopTimerAction()
        if revive_time <= 0:
            refresh_time(0)
            self._count_down_end()
            return
        refresh_time(0)
        global_data.emgr.death_count_down_start.emit()
        self.panel.TimerAction(refresh_time, revive_time, interval=0.1)

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

    def set_start_show_time(self, show_time):
        self.start_show_time = show_time

    def set_count_down_sound(self, sound):
        self.tick_sound = sound

    def set_time_need_ceil(self, need_ceil):
        self._need_ceil = need_ceil
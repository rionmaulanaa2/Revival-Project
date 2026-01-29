# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseTimerUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon import time_utility
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.const import uiconst

class ExerciseTimerUI(MechaDistortHelper, BasePanel):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    PANEL_CONFIG_NAME = 'battle_train/fight_time'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseTimerUI, self).on_init_panel()
        self.process_events(True)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_exit_timestamp': self.update_timer,
           'scene_camera_player_setted_event': self.on_cam_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self):
        self.on_ctrl_target_changed()

    def switch_to_mecha(self):
        if global_data.is_pc_mode:
            self.panel.nd_time.SetPosition('100%-20', 'i0')
        else:
            self.panel.nd_time.SetPosition('i290', 'i29')
        super(ExerciseTimerUI, self).switch_to_mecha()

    def switch_to_non_mecha(self):
        if global_data.is_pc_mode:
            self.panel.nd_time.SetPosition('100%-20', 'i0')
        else:
            self.panel.nd_time.SetPosition('i220', 'i0')
        super(ExerciseTimerUI, self).switch_to_non_mecha()

    def update_timer(self, exit_timestamp):
        exit_time = exit_timestamp - time_utility.get_server_time()

        def update_time(pass_time):
            left_time = int(exit_time - pass_time)
            left_time = time_utility.get_delta_time_str(left_time)[3:]
            self.panel.lab_time.SetString(left_time)

        self.panel.lab_time.StopTimerAction()
        self.panel.lab_time.TimerAction(update_time, exit_time, callback=self.on_timer_end, interval=1.0)

    def on_timer_end(self):
        global_data.ui_mgr.show_ui('ExerciseTimerEndUI', module_path='logic.comsys.exercise_ui')

    def on_finalize_panel(self):
        self.process_events(False)
        super(ExerciseTimerUI, self).on_finalize_panel()
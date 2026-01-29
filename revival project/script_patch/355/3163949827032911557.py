# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseTimerEndUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel, MAIN_UI_LIST
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst

class ExerciseTimerEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_train_finish'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_exit.OnClick': 'on_click_exit'
       }
    DELAY_EXIT_TIME = 5

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseTimerEndUI, self).on_init_panel()
        self.add_blocking_ui_list(MAIN_UI_LIST)
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)
        self.process_events(True)
        self.nd_finish.setVisible(True)
        self.btn_exit.setVisible(True)
        self.play_show_animation()
        self.set_timer()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def play_show_animation(self):
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')

    def set_timer(self):

        def update_time(pass_time):
            left_time = int(self.DELAY_EXIT_TIME - pass_time)
            self.panel.lab_time.SetString('( ' + str(left_time) + 's )')

        self.panel.lab_time.StopTimerAction()
        self.panel.lab_time.TimerAction(update_time, self.DELAY_EXIT_TIME, callback=self.on_click_exit)

    def on_click_exit(self, *args, **kwargs):
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event('E_QUIT_EXERCISE_FIELD')
        return

    def on_finalize_panel(self):
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        self.process_events(False)
        super(ExerciseTimerEndUI, self).on_finalize_panel()
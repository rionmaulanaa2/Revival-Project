# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaLiveEndUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.uisys.basepanel import BasePanel, MAIN_UI_LIST
from logic.gcommon import time_utility as tutil
from common.const import uiconst
from logic.gutils.concert_utils import get_concert_end_ts

class KizunaLiveEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/kizuna_live_end'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'btn_exit.OnClick': 'on_click_exit'
       }

    def on_init_panel(self, *args, **kwargs):
        super(KizunaLiveEndUI, self).on_init_panel()
        self.add_blocking_ui_list(MAIN_UI_LIST)
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)
        self.play_show_animation()
        self.set_timer()

    def play_show_animation(self):
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')
            self.panel.PlayAnimation('loop_line')

    def set_timer(self):
        server_time = tutil.get_server_time()
        delay_exit_time = global_data.battle.concert_start_ts + get_concert_end_ts() - server_time

        def update_time(pass_time):
            left_time = int(delay_exit_time - pass_time)
            self.panel.lab_time.SetString('( ' + str(left_time) + 's )')

        self.panel.lab_time.StopTimerAction()
        self.panel.lab_time.TimerAction(update_time, delay_exit_time, callback=self.on_click_exit)

    def on_finalize_panel(self):
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        super(KizunaLiveEndUI, self).on_finalize_panel()

    def on_click_exit(self, *args, **kwargs):

        def cb():
            if global_data.player and global_data.player.logic:
                global_data.player.quit_battle(True)

        self.panel.PlayAnimation('disappear')
        self.panel.SetTimeOut(self.panel.GetAnimationMaxRunTime('disappear'), cb)
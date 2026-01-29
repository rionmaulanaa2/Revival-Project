# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.gcommon import time_utility as tutil
import math

class ArenaConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arena/battle_arena_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_cancel.btn_common.OnClick': 'on_btn_cancel_click',
       'btn_go.btn_common.OnClick': 'on_btn_go_click'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self.revive_time = 10
        self.confirm_idx = -1

    def set_timeout_ts(self, confirm_idx, timeout_ts):
        from logic.gcommon.time_utility import get_server_time_battle
        self.revive_time = int(math.ceil(timeout_ts - get_server_time_battle()))
        self.confirm_idx = confirm_idx
        self.refresh_time()

    def refresh_time(self):
        if not (self.panel and self.panel.isValid()):
            return

        def refresh_time_finsh(show_tips=True):
            if not (self.panel and self.panel.isValid()):
                return
            self.panel.btn_go.btn_common.SetText(get_text_by_id(609909).format(num=str(0)))
            if show_tips:
                global_data.game_mgr.show_tip(get_text_by_id(609918))
            self.close()

        def refresh_time(pass_time, show_tips=True):
            if not (self.panel and self.panel.isValid()):
                return
            left_time = self.revive_time - pass_time
            left_time = int(math.ceil(left_time))
            self.panel.btn_go.btn_common.SetText(get_text_by_id(609909).format(num=str(left_time)))
            if left_time <= 0:
                refresh_time_finsh(show_tips)

        self.panel.btn_go.StopTimerAction()
        refresh_time(0, False)
        if not (self.panel and self.panel.isValid()):
            return
        self.panel.btn_go.TimerAction(refresh_time, self.revive_time, callback=refresh_time_finsh, interval=1)

    def on_btn_cancel_click(self, btn, touch):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def callback():
            bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
            if bat:
                bat.confirm_duel(self.confirm_idx, False)
            self.close()

        SecondConfirmDlg2().confirm(content=get_text_by_id(609907), confirm_callback=callback)

    def on_btn_go_click(self, btn, touch):
        self.close()
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if bat:
            bat.confirm_duel(self.confirm_idx, True)
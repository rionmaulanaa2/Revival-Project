# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/HangUpUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.time_utility import get_server_time, get_delta_time_str
from common.const import uiconst
from logic.gcommon.common_const.team_const import HANG_UP_TIME

class HangUpUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/match_shortcut'
    ACT_TAG = 210101
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_cancel_hang_up'
       }
    GLOBAL_EVENT = {'player_leave_team_event': 'on_leave_team'
       }
    IS_PLAY_WINDOWS_SOUND = False

    def on_init_panel(self):
        self._is_matching = False
        self.hang_up_ts = None
        self.match_tag = 10
        self.panel.setLocalZOrder(10)
        self.panel.lab_tips.SetString(13129)
        return

    def disappear(self):
        if self.panel.IsPlayingAnimation('in'):
            self.panel.StopAnimation('in')
        self.panel.PlayAnimation('out')
        delay = self.panel.GetAnimationMaxRunTime('out')
        self.panel.SetTimeOut(delay, lambda : self.close(), tag=self.ACT_TAG)

    def start_hang_up(self, hang_up_ts):
        self.hang_up_ts = hang_up_ts
        self.panel.StopAnimation('out')
        self.panel.stopActionByTag(self.ACT_TAG)
        self.panel.PlayAnimation('in')
        self._show_time_passed()
        self.panel.DelayCallWithTag(1, self._show_time_passed, self.match_tag)

    def _show_time_passed(self):
        left_hang_time = self.hang_up_ts - get_server_time()
        if left_hang_time < 0:
            self.close()
        else:
            self.panel.lab_time.setString('%ds' % left_hang_time)
        return True

    def on_click_cancel_hang_up(self, btn, touch):
        if global_data.player:
            global_data.player.req_leave_team()
        self.close()

    def on_finalize_panel(self):
        global_data.emgr.battle_match_status_event.emit(False)

    def on_leave_team(self):
        self.close()
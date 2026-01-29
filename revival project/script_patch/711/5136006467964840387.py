# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleMatchUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility as tutil
from common.const import uiconst
from common.cfg import confmgr

class BattleMatchUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/match_shortcut'
    ACT_TAG = 210101
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_cancel_match'
       }
    GLOBAL_EVENT = {'player_change_leader_event': 'update_match_widget',
       'battle_match_status_event': 'update_match_widget'
       }
    IS_PLAY_WINDOWS_SOUND = False

    def on_init_panel(self):
        self._is_matching = False
        self.match_tag = 10
        self.panel.setLocalZOrder(10)
        self.update_match_widget()

    def disappear(self):
        if self.panel.IsPlayingAnimation('in'):
            self.panel.StopAnimation('in')
        self.panel.PlayAnimation('out')
        delay = self.panel.GetAnimationMaxRunTime('out')
        self.panel.SetTimeOut(delay, lambda : self.close(), tag=self.ACT_TAG)

    def update_match_widget(self, *args):
        is_matching = global_data.player.is_matching
        team_info = global_data.player.get_team_info()
        is_ready = global_data.player.get_self_ready() and bool(team_info)
        if is_matching:
            if global_data.player.get_match_start_timestamp() is not None:
                self.panel.StopAnimation('out')
                self.panel.stopActionByTag(self.ACT_TAG)
                self.panel.PlayAnimation('in')
                self._show_time_passed()
                self.panel.DelayCallWithTag(1, self._show_time_passed, self.match_tag)
                self.update_lab_tips()
        else:
            self.panel.stopActionByTag(self.match_tag)
            self.disappear()
        return

    def _show_time_passed(self):
        if not global_data.player:
            return
        if not global_data.player.get_match_start_timestamp():
            self.panel.stopActionByTag(self.match_tag)
            return
        delta = tutil.time() - global_data.player.get_match_start_timestamp()
        self.panel.lab_time.setString(tutil.get_delta_time_str(delta)[3:])
        return True

    def on_click_cancel_match(self, btn, touch):
        if global_data.player and global_data.player.is_matching:
            global_data.player.cancel_match()

    def update_lab_tips(self):
        matching_type = global_data.player.get_matching_type()
        if matching_type:
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(matching_type))
            name_text_id = battle_info.get('cNameTID', -1)
            name_text = get_text_by_id(name_text_id)
            self.panel.lab_tips.setString(get_text_by_id(635152).format(name_text))
        else:
            self.panel.lab_tips.setString(get_text_by_id(80277))
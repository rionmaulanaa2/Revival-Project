# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Fire/FireSurvivalBattleTopCounterUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import LOW_MESSAGE_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility
import math
from common.const import uiconst

class FireSurvivalBattleTopCounterUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_fire/i_fire_num'
    DLG_ZORDER = LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.init_panel()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_panel(self):
        if global_data.battle:
            self.fire_count = global_data.battle.get_fire_num()
            self.update_fire_count(self.fire_count)

    def init_event(self):
        self.process_event(True)

    def init_parameters(self):
        self.fire_count = 0
        self.cfg_data = global_data.game_mode.get_cfg_data('play_data')
        self.observed_player_id = None
        self.fire_extinguishing_count = self.cfg_data.get('fire_immune_num', 7)
        self.panel.list_item.SetInitCount(self.fire_extinguishing_count)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_fire_count': self.update_fire_count,
           'scene_camera_player_setted_event': self.on_camera_target_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_fire_count(self, count):
        if global_data.player:
            for idx in range(self.fire_extinguishing_count):
                ui_item = self.panel.list_item.GetItem(idx)
                ui_item.icon_ban.setVisible(idx + 1 <= count)
                if idx + 1 <= count and idx + 1 > self.fire_count:
                    ui_item.PlayAnimation('show')

        self.fire_count = count
        if self.fire_count == self.fire_extinguishing_count:
            self.SetTimeOut(5.0, self.close)

    def on_camera_target_setted(self, *args):
        if global_data.cam_lplayer and global_data.player:
            hidden = global_data.cam_lplayer.id != global_data.player.id
            if hidden:
                self.close()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/BornIslandUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import parachute_utils
COUNTDOWN_TAG = 1

class BornIslandUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_before/fight_born_island'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(BornIslandUI, self).on_init_panel(*args, **kwargs)
        self.panel.PlayAnimation('count_down_show')
        self.panel.lab_count_down.SetString(get_text_by_id(80221))
        self.prepare_timestamp = global_data.battle.prepare_timestamp
        self.update_countdown()
        self.panel.DelayCallWithTag(1, self.update_countdown, COUNTDOWN_TAG)
        from logic.comsys.battle.TeammateStatusWidget import TeammateStatusWidget
        if not global_data.battle.is_single_person_battle():
            if global_data.is_pc_mode:
                self.panel.PlayAnimation('pc')
            self.teammate_widget = TeammateStatusWidget(self.panel.temp_teammate)
        else:
            self.panel.temp_teammate.setVisible(False)

    def update_countdown(self):
        delta = self.prepare_timestamp - tutil.get_server_time() - parachute_utils.PARACHUTE_ANIM_TIME
        delta = int(max(0, delta))
        self.panel.lab_count_down_num.SetString(str(delta))
        self.panel.vx_lab_count_down_num.SetString(str(delta))
        if delta <= 10:
            self.panel.PlayAnimation('count_down')
            if delta >= 1:
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'ui_fight_count'))
            elif delta < 1:
                global_data.sound_mgr.play_sound_2d('play_ui_notice', ('ui_notice',
                                                                       'ui_fight_count_end'))
        return delta > 0

    def on_finalize_panel(self):
        self.destroy_widget('teammate_widget')
        super(BornIslandUI, self).on_finalize_panel()
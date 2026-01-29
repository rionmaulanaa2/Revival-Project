# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonAdvance2.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import logic.gutils.season_utils as season_utils
from common.const import uiconst

class SeasonAdvance2(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/open_ad_1'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_OPEN_SOUND = 'season_next'

    def on_init_panel(self, *args):
        global_data.ui_mgr.show_ui('SeasonAdvance2bg', 'logic.comsys.battle_pass')
        self.panel.PlayAnimation('appear')
        self._player_id = season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)
        max_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.DelayCallWithTag(max_time, self.on_anim_finish, 1)
        self.enable_show_next_frame()
        self._set_reward_item()

    def on_anim_finish(self):
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('continue')

    def enable_show_next_frame(self):

        @self.nd_touch_continue.callback()
        def OnClick(*args):
            self.close()
            global_data.ui_mgr.close_ui('SeasonAdvance1')

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('SeasonAdvance2bg')
        if self._player_id:
            global_data.sound_mgr.stop_playing_id(self._player_id)
            self._player_id = None
        return

    def hide_go_btn(self):
        self.panel.nd_btn_go.setVisible(False)

    def _set_reward_item(self):
        from logic.gutils.advance_utils import set_season_small, set_reward_item
        set_season_small(self.panel)
        set_reward_item(self.panel, True)
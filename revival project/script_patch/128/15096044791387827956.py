# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonAdvance1.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import logic.gutils.season_utils as season_utils
from common.const import uiconst

class SeasonAdvance1(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/open_logo'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    UI_OPEN_SOUND = 'season_logo'

    def on_init_panel(self, *args):
        self._enable_jump = True
        self.hide_main_ui()
        global_data.ui_mgr.show_ui('SeasonAdvance1bg', 'logic.comsys.battle_pass')
        self.panel.PlayAnimation('appear')
        self._player_id = season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)
        max_time = self.panel.GetAnimationMaxRunTime('appear')
        self.panel.DelayCallWithTag(max_time, self.on_anim_finish, 1)
        self.enable_show_next_frame()

    def on_anim_finish(self):
        self.panel.PlayAnimation('continue')

    def enable_show_next_frame(self):

        @self.nd_bg.callback()
        def OnClick(*args):
            self.close()

        @self.temp_btn_close.btn_back.callback()
        def OnClick(*args):
            self.close()

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('SeasonAdvance1bg')
        if self._player_id:
            global_data.sound_mgr.stop_playing_id(self._player_id)
            self._player_id = None
        self.show_main_ui()
        return

    def hide_go_btn(self):
        pass
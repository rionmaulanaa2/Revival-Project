# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/BuyCardSuccess.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.cinematic.VideoPlayer import VideoPlayer
from common.const.uiconst import UI_TYPE_NORMAL, DIALOG_LAYER_ZORDER_2, UI_VKB_NO_EFFECT
PANEL_NAME = 'battle_pass/battle_pass_unlock_successfully'
VIDEO_NAME = 'video/season_logo.mp4'

class BuyCardSuccess(BasePanel):
    PANEL_CONFIG_NAME = PANEL_NAME
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_NORMAL
    GLOBAL_EVENT = {'receive_award_end_event': '_show_ui'
       }
    UI_ACTION_EVENT = {'nd_close.OnClick': 'close'
       }

    def on_init_panel(self):
        self._hide_main = False
        ui_receive = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        ui_display = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        cond_1 = ui_receive and ui_receive.isPanelVisible()
        cond_2 = ui_receive and ui_receive.is_showing()
        cond_3 = ui_display and ui_display.is_showing_model_item()
        if cond_1 or cond_2 or cond_3:
            self.hide()
            return
        self._show_ui()

    def _show_ui(self):
        self.clear_show_count_dict()
        self._hide_main = False
        self._play_mainland_anim()
        self.hide_main_ui()
        self._init_lab()
        self._hide_main = True
        from common.cinematic.VideoPlayer import VideoPlayer
        ui = global_data.ui_mgr.get_ui('SeasonPassLevelUp')
        if ui:
            ui.hide()
        VideoPlayer().play_video(VIDEO_NAME, None, repeat_time=1, bg_play=True, complete_cb=self._on_complete_cb)
        return

    def _init_lab(self):
        from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L2, SEASON_PASS_L3
        now_bp_types = global_data.player or set() if 1 else global_data.player.get_battlepass_types()
        now_high_card_type = None
        for card_type in (SEASON_PASS_L2, SEASON_PASS_L1, SEASON_PASS_L3):
            if card_type in now_bp_types:
                now_high_card_type = card_type
                break

        if now_high_card_type:
            name_info = {SEASON_PASS_L3: 608438,SEASON_PASS_L1: 608439,
               SEASON_PASS_L2: 608440
               }
            self.panel.lab_get.SetString(82133)
        return

    def _play_mainland_anim(self):
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.panel.PlayAnimation('appear')

    def _on_complete_cb(self, *args):
        pass

    def on_finalize_panel(self):
        VideoPlayer().stop_video()
        if self._hide_main:
            self.show_main_ui()
        global_data.emgr.receive_award_end_event.emit()
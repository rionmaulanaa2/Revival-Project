# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/UnlockRetrospectUI.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.cinematic.VideoPlayer import VideoPlayer
from common.const.uiconst import UI_TYPE_NORMAL, DIALOG_LAYER_ZORDER_2, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id
PANEL_NAME = 'battle_pass/bp_retrospect/open_bp_retrospect_task_unlock'
VIDEO_NAME = 'video/retrospect_s{}.mp4'

class UnlockRetrospectUI(BasePanel):
    PANEL_CONFIG_NAME = PANEL_NAME
    DLG_ZORDER = DIALOG_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_NORMAL
    GLOBAL_EVENT = {}
    UI_ACTION_EVENT = {'nd_close.OnClick': 'close'
       }

    def on_init_panel(self, season):
        ui_receive = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        ui_display = global_data.ui_mgr.get_ui('GetModelDisplayUI')
        cond_1 = ui_receive and ui_receive.isPanelVisible()
        cond_2 = ui_receive and ui_receive.is_showing()
        cond_3 = ui_display and ui_display.is_showing_model_item()
        self.season = season
        self._hide_main = False
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
        VideoPlayer().play_video(VIDEO_NAME.format(self.season), None, repeat_time=1, bg_play=True, complete_cb=self._on_complete_cb)
        return

    def _init_lab(self):
        text = get_text_by_id(confmgr.get('season_retrospect_{}'.format(self.season)).get('season_title'))
        self.panel.lab_get.SetString(text.format(G_IS_NA_PROJECT or self.season if 1 else self.season + 5))

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
        super(UnlockRetrospectUI, self).on_finalize_panel()
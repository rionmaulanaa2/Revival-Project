# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyDuelModeConfirmUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL
from logic.gcommon.common_utils.local_text import get_text_by_id

class LobbyDuelModeConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/bg_second_confirm_2'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, text_id, first_click_callback, second_click_callback, *args, **kwargs):
        super(LobbyDuelModeConfirmUI, self).on_init_panel()
        self.panel.temp_second_confirm.lab_content.SetString(text_id)
        self.first_click_callback = first_click_callback
        self.second_click_callback = second_click_callback
        self.init_ui_event()

    def init_ui_event(self):

        @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(*args):
            if self.first_click_callback:
                self.first_click_callback()
            self.close()

        @self.panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(*args):
            if self.second_click_callback:
                self.second_click_callback()
            self.close()

    def on_finalize_panel(self):
        self.first_click_callback = None
        self.second_click_callback = None
        self.choose_cb = None
        return
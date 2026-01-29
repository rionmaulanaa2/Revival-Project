# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/GenericMechaSkinSalesConfirmUI.py
from __future__ import absolute_import
from common.const.uiconst import SECOND_CONFIRM_LAYER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL
from logic.gcommon.common_utils.local_text import get_text_by_id

class GenericMechaSkinSalesConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/bg_second_confirm_2'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.init_btn_event()

    def init_btn_event(self):

        @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(*args):
            self.close()

        @self.panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(*args):
            self.on_confirm()

    def config(self, title_id, cancel_id, confirm_id, call_back):
        self.callback = call_back
        self.panel.temp_second_confirm.lab_content.SetString(get_text_by_id(title_id))
        self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(get_text_by_id(cancel_id))
        self.panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(get_text_by_id(confirm_id))

    def on_confirm(self, *args):
        if self.callback:
            self.callback()
            self.callback = None
        self.close()
        return
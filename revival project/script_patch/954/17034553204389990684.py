# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/privilege/PrivilegeSettingTips.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL
from logic.gcommon.common_utils.local_text import get_text_by_id

class PrivilegeSettingTips(BasePanel):
    PANEL_CONFIG_NAME = 'common/bg_second_confirm_2'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self):
        self.panel.temp_second_confirm.lab_content.SetString(get_text_by_id(610279))
        self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(get_text_by_id(19850))
        self.panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(get_text_by_id(2297))
        self.init_btn_event()

    def init_btn_event(self):

        @self.panel.temp_second_confirm.temp_btn_1.btn_common_big.unique_callback()
        def OnClick(*args):
            from logic.comsys.setting_ui.PrivilegeSettingUI import PrivilegeSettingUI
            PrivilegeSettingUI()
            self.close()

        @self.panel.temp_second_confirm.temp_btn_2.btn_common_big.unique_callback()
        def OnClick(*args):
            self.close()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/UpdateGameConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const.property_const import *
import game3d
from common.const import uiconst

class UpdateGameConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/normal_second_confirm_2'
    DLG_ZORDER = TOP_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_second_confirm.temp_btn_1.btn_common_big.OnClick': 'cancel',
       'temp_second_confirm.temp_btn_2.btn_common_big.OnClick': 'confirm'
       }

    def on_init_panel(self):
        is_auto_jump = True
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if global_data.channel.get_name() not in ('netease', 'netease_global'):
                is_auto_jump = False
        self._is_auto_jump = is_auto_jump
        if is_auto_jump:
            self.panel.temp_second_confirm.lab_content.SetString(609232)
        else:
            self.panel.temp_second_confirm.lab_content.SetString(609233)

    def cancel(self, *args):
        self.close()

    def confirm(self, *args):
        if not self._is_auto_jump:
            self.close()
            return
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_install_package()
        self.close()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/veteran/PCVeteranConfirmUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.const import uiconst
import time

class PCVeteranConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/tips_return_finish_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'btn_cancel.btn_common_big.OnClick': 'cancel_confirm',
       'btn_confirm.btn_common_big.OnClick': 'confirm'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args):
        self.panel.lab_confirm.SetString(860050)
        self.panel.lab_tips.setVisible(False)
        self._confirm_time = None
        self._confirm_fail = True
        self._host = None
        self._uid = None
        return

    def on_finalize_panel(self):
        pass

    def set_confirm_info(self, data):
        if data:
            self._host = data.get('host', 0)
            self._uid = data.get('uid', 0)
            name = data.get('char_name', '')
            self.panel.lab_confirm.SetString(name)
            self._confirm_time = time.time() + 1
            self.panel.lab_tips.setVisible(True)
            self._confirm_fail = False
        else:
            self.panel.lab_confirm.SetString(112)
            self._confirm_fail = True

    def cancel_confirm(self, *args):
        ui = global_data.ui_mgr.get_ui('PCVeteranUI')
        ui and ui.unlock()
        self.close()

    def confirm(self, *args):
        if self._confirm_fail:
            self.cancel_confirm()
            return
        if not self._confirm_time or time.time() < self._confirm_time:
            return
        global_data.player.request_return_to_steam(self._host, self._uid)
        global_data.ui_mgr.show_ui('PCVeteranSuccessUI', 'logic.comsys.veteran')
        self.close()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/veteran/PCVeteranSuccessUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.const import uiconst
import time

class PCVeteranSuccessUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/tips_return_finish_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {'btn_go.btn_common_big.OnClick': 'confirm'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args):
        self.panel.nd_confirm.setVisible(False)
        self.panel.nd_finish.setVisible(True)
        self.panel.lab_content.SetString(860050)

    def on_finalize_panel(self):
        pass

    def set_confirm_info(self, data):
        if not data:
            self.panel.lab_content.SetString(112)
        else:
            text = get_text_by_id(906554).format(uid=data.get('uid', 0))
            self.panel.lab_content.SetString(text)

    def confirm(self, *args):
        ui = global_data.ui_mgr.get_ui('PCVeteranUI')
        ui and ui.unlock()
        self.close()
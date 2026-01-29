# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaChuChangUI.py
from __future__ import absolute_import
import render
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER
EXCEPT_HIDE_UI_LIST = []
from common.const import uiconst

class MechaChuChangUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_chuchang'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn'
       }
    GLOBAL_EVENT = {'close_special_lobby_scene_event': 'on_click_back_btn'
       }

    def on_init_panel(self):
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))

    def on_finalize_panel(self):
        ret_data = global_data.emgr.get_mecha_chuchang_data.emit()
        if ret_data and len(ret_data) > 0:
            mecha_skin_id = ret_data[0]
            self.show_main_ui()

    def on_click_back_btn(self, *args):
        self.close()
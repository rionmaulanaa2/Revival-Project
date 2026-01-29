# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEEquipWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE

class PVEEquipWidgetUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/i_pve_book_widget'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': '_on_click_back'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVEEquipWidgetUI, self).on_init_panel()
        self.init_params()
        self.process_events(True)
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self):
        pass

    def init_ui_events(self):
        pass

    def on_resolution_changed(self):
        super(PVEEquipWidgetUI, self).on_resolution_changed()

    def _on_click_back(self, *args):
        self.close()

    @staticmethod
    def check_red_point():
        return False

    def on_finalize_panel(self):
        self.process_events(False)
        super(PVEEquipWidgetUI, self).on_finalize_panel()
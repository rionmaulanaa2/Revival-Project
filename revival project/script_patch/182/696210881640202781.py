# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/GranbelmAdvance.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance

class GranbelmAdvance(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202004/open_granbelm_kv'

    def on_init_panel(self, *args):
        super(GranbelmAdvance, self).on_init_panel()
        global_data.ui_mgr.show_ui('GranbelmAdvanceVx', 'logic.comsys.activity')

    def set_content(self):
        pass

    def get_close_node(self):
        return (
         self.panel.nd_close, self.panel.temp_btn_close.btn_back)

    def on_finalize_panel(self):
        super(GranbelmAdvance, self).on_finalize_panel()
        global_data.ui_mgr.close_ui('GranbelmAdvanceVx')
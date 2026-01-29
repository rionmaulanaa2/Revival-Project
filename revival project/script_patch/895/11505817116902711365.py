# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/mode/PCVersionAdvance.py
from __future__ import absolute_import
from ..SimpleAdvance import SimpleAdvance

class PCVersionAdvance(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202004/open_pc_version'
    LASTING_TIME = 0.5
    UI_ACTION_EVENT = {'btn_go.OnClick': 'on_click_btn'
       }

    def set_content(self):
        pass

    def get_close_node(self):
        return (
         self.panel.nd_close, self.temp_btn_close.btn_back)

    def on_click_btn(self, *args):
        from logic.gcommon.common_const.activity_const import ACTIVITY_PC_VERSION
        from logic.gutils import jump_to_ui_utils
        from common.cfg import confmgr
        ui_data = confmgr.get('c_activity_config', ACTIVITY_PC_VERSION, 'cUiData', default={})
        web_url = ui_data.get('url')
        jump_to_ui_utils.jump_to_website(web_url)
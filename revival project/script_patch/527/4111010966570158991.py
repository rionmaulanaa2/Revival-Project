# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/AIDebugUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const import uiconst

class AIDebugUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/flght_ai_number'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        pass

    def refresh_info(self, info):
        num = info.get('battle_time', 0)
        self.panel.nd_ai_number.img_time.lab_time_number.SetString(str(num))
        num = info.get('real_ai', 0)
        self.panel.nd_ai_number.img_real_ai.lab_real_ai_number.SetString(str(num))
        num = info.get('move_ai', 0)
        self.panel.nd_ai_number.img_move_ai.lab_move_ai_number.SetString(str(num))
        num = info.get('chat_ai', 0)
        self.panel.nd_ai_number.img_chat_ai.lab_chat_ai_number.SetString(str(num))
        num = info.get('agent_num', 0)
        self.panel.nd_ai_number.img_manage_ai.lab_manage_ai_number.SetString(str(num))
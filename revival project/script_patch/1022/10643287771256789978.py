# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/NewbieStageSideTipUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.common_utils.local_text import get_text_by_id

class NewbieStageSideTipUI(BasePanel):
    PANEL_CONFIG_NAME = 'guide/i_guide_task_tips'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def set_tip_content(self, tip_text_id):
        self.panel.nd_task_tips.lab_task.SetString(get_text_by_id(tip_text_id))
        self.panel.nd_task_tips.setVisible(True)

    def set_tip_visible(self, visible):
        self.panel.nd_task_tips.setVisible(visible)
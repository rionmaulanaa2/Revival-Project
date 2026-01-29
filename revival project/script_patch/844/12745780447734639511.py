# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TestSpineUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
import re
from common.uisys.basepanel import BasePanel

class TestSpineUI(BasePanel):
    PANEL_CONFIG_NAME = 'test_spine'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(TestSpineUI, self).on_init_panel()

    def on_click_close(self, *args):
        self.close()
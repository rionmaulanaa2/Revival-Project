# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/test/TempBgUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER
from common.const import uiconst

class TempBgUI(BasePanel):
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test/bg_temp'

    def show_effect_gaosi(self):
        self.close_effect_gaosi()
        from logic.comsys.effect.ui_effect import GaussianEffect
        self._effect_gaosi = GaussianEffect(self.panel.bg, self.panel.pnl_gaosi)
        self._effect_gaosi.start()

    def close_effect_gaosi--- This code section failed: ---

  24       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  '_effect_gaosi'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

  25      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

  26      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             1  '_effect_gaosi'
          22  JUMP_IF_FALSE_OR_POP    37  'to 37'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             1  '_effect_gaosi'
          31  LOAD_ATTR             2  'destroy'
          34  CALL_FUNCTION_0       0 
        37_0  COME_FROM                '22'
          37  POP_TOP          

  27      38  LOAD_CONST            0  ''
          41  LOAD_FAST             0  'self'
          44  STORE_ATTR            1  '_effect_gaosi'
          47  LOAD_CONST            0  ''
          50  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_finalize_panel(self):
        self.close_effect_gaosi()
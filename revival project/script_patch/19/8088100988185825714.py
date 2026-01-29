# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AimScopeAdjust/CommonAimScopeAdjustUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import LOW_MESSAGE_ZORDER
from logic.comsys.battle.AimScopeAdjust.AimScopeAdjustUIWidget import AimScopeAdjustUIWidget
from data import hot_key_def
from common.const import uiconst

class CommonAimScopeAdjustUI(BasePanel):
    DLG_ZORDER = LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle/fight_hit_sniper_adjust'
    PROG_ADJUST_FLOOR = 72
    PROG_ADJUST_CEIL = 81
    TURN_ADJUST_FLOOR = -18
    TURN_ADJUST_CEIL = 22
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    USE_CUSTOM_UI_PANEL_KEY = 'HumanAimScopeAdjustUI'
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.MOUSE_WHEEL_MSG: {'node': 'temp_pc'}}

    def _populate_nodes(self, *args, **kwargs):
        self.nd_adjust = self.panel.nd_adjust
        self.btn_adjust = self.panel.btn_adjust
        self.prog_adjust = self.panel.prog_adjust
        self.nd_btn_turn = self.panel.nd_btn_turn

    def on_init_panel(self, *args, **kwargs):
        self._populate_nodes(*args, **kwargs)
        self.init_custom_com()
        self.aim_scope_adjust_ui_widget = None
        self.nd_adjust.setVisible(False)
        magnification_triplet = kwargs.get('magnification_triplet', None)
        aim_scope_id = kwargs.get('aim_scope_id', 0)
        if aim_scope_id and isinstance(magnification_triplet, tuple) and len(magnification_triplet) == 3 and magnification_triplet[1] != magnification_triplet[2]:
            self.aim_scope_adjust_ui_widget = AimScopeAdjustUIWidget()
            self.aim_scope_adjust_ui_widget.on_init_panel(self.nd_adjust, self.panel, aim_scope_id, magnification_triplet[0], magnification_triplet[1], magnification_triplet[2], self.btn_adjust, self.prog_adjust, self.nd_btn_turn, {'prog_adjust_floor': self.PROG_ADJUST_FLOOR,
               'prog_adjust_ceil': self.PROG_ADJUST_CEIL,
               'turn_adjust_floor': self.TURN_ADJUST_FLOOR,
               'turn_adjust_ceil': self.TURN_ADJUST_CEIL
               })
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {}, ui_custom_panel_name=self.USE_CUSTOM_UI_PANEL_KEY)

    def on_finalize_panel--- This code section failed: ---

  66       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'aim_scope_adjust_ui_widget'
           6  LOAD_CONST            0  ''
           9  COMPARE_OP            9  'is-not'
          12  POP_JUMP_IF_FALSE    40  'to 40'

  67      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             0  'aim_scope_adjust_ui_widget'
          21  LOAD_ATTR             2  'on_finalize_panel'
          24  CALL_FUNCTION_0       0 
          27  POP_TOP          

  68      28  LOAD_CONST            0  ''
          31  LOAD_FAST             0  'self'
          34  STORE_ATTR            0  'aim_scope_adjust_ui_widget'
          37  JUMP_FORWARD          0  'to 40'
        40_0  COME_FROM                '37'

  69      40  LOAD_GLOBAL           3  'hasattr'
          43  LOAD_GLOBAL           1  'None'
          46  CALL_FUNCTION_2       2 
          49  POP_JUMP_IF_FALSE    86  'to 86'
          52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             4  'custom_ui_com'
        58_0  COME_FROM                '49'
          58  POP_JUMP_IF_FALSE    86  'to 86'

  70      61  LOAD_FAST             0  'self'
          64  LOAD_ATTR             4  'custom_ui_com'
          67  LOAD_ATTR             5  'destroy'
          70  CALL_FUNCTION_0       0 
          73  POP_TOP          

  71      74  LOAD_CONST            0  ''
          77  LOAD_FAST             0  'self'
          80  STORE_ATTR            4  'custom_ui_com'
          83  JUMP_FORWARD          0  'to 86'
        86_0  COME_FROM                '83'
          86  LOAD_CONST            0  ''
          89  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 46

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        if self.aim_scope_adjust_ui_widget:
            self.aim_scope_adjust_ui_widget.on_hot_key_mouse_scroll(delta)

    def check_can_mouse_scroll(self):
        if not (self.aim_scope_adjust_ui_widget and self.aim_scope_adjust_ui_widget.can_drag):
            return False
        return True
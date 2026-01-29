# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownGuideUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_NO_EFFECT, UI_VKB_CLOSE
from common.const import uiconst
NUM_NAME_DICT = {1: 'first',
   2: 'second',
   3: 'third',
   4: 'forth',
   0: 'last'
   }

class CrownGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_king/guide_human_king'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'on_show_step'
       }

    def on_init_panel(self, auto_unlocker_time=30):
        self.init_parameters(auto_unlocker_time)
        self.init_panel()

    def init_panel(self):
        self.top_score_ui = global_data.ui_mgr.get_ui('CrownTopCounterUI')
        self.top_score_ui.update_ui_state(False)
        self.panel.temp_hint.setVisible(False)
        if global_data.player:
            show_crown_guide_name = self.__class__.__name__ + str(global_data.player.uid)
            global_data.achi_mgr.set_cur_user_archive_data(show_crown_guide_name, True)
        self.show_step_first()

    def init_parameters(self, auto_unlocker_time):
        self._lock_timer = None
        self._lock_timer = self.panel.SetTimeOut(auto_unlocker_time, self.show_step_last)
        self.step_now = 1
        self.last_click_time = time.time()
        return

    def on_show_step--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'time'
           3  LOAD_ATTR             0  'time'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            3  'cur_time'

  52      12  LOAD_FAST             3  'cur_time'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'last_click_time'
          21  BINARY_SUBTRACT  
          22  LOAD_CONST            1  0.5
          25  COMPARE_OP            0  '<'
          28  POP_JUMP_IF_FALSE    35  'to 35'

  53      31  LOAD_CONST            0  ''
          34  RETURN_END_IF    
        35_0  COME_FROM                '28'

  54      35  LOAD_GLOBAL           2  'getattr'
          38  LOAD_GLOBAL           2  'getattr'
          41  LOAD_ATTR             3  'format'
          44  LOAD_GLOBAL           4  'NUM_NAME_DICT'
          47  LOAD_FAST             0  'self'
          50  LOAD_ATTR             5  'step_now'
          53  BINARY_SUBSCR    
          54  CALL_FUNCTION_1       1 
          57  LOAD_CONST            0  ''
          60  CALL_FUNCTION_3       3 
          63  STORE_FAST            4  'step_func'

  55      66  LOAD_FAST             4  'step_func'
          69  POP_JUMP_IF_FALSE    82  'to 82'

  56      72  LOAD_FAST             4  'step_func'
          75  CALL_FUNCTION_0       0 
          78  POP_TOP          
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'
          82  LOAD_CONST            0  ''
          85  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 60

    def show_step_first(self):
        self.step_now = 2
        self.panel.PlayAnimation('frame')
        self.panel.nd_step_1.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(17297))

    def show_step_second(self):
        self.step_now = 3
        self.panel.nd_step_1.setVisible(False)
        self.panel.nd_step_2.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(17300))

    def show_step_third(self):
        self.step_now = 4
        self.panel.nd_step_2.setVisible(False)
        self.panel.nd_step_3.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(17298))

    def show_step_forth(self):
        self.step_now = 0
        self.panel.nd_step_3.setVisible(False)
        self.panel.nd_step_4.setVisible(True)
        self.panel.temp_human_tips.lab_tips.SetString(get_text_by_id(17299))

    def show_step_last(self):
        self.top_score_ui.update_ui_state(True)
        self.close()

    def update_panel_state(self, state):
        self.panel.setVisible(state)
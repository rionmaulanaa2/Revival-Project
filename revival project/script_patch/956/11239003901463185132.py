# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ItemNumInputWidget.py
from __future__ import absolute_import
import six
from logic.comsys.common_ui.InputBox import InputBox

class ItemNumInputWidget(object):

    def __init__(self, panel):
        self.btn_mgr = None
        self.panel = panel
        self.input_box = None
        return

    def destroy(self):
        self.btn_mgr.destroy()
        self.panel = None
        self.btn_mgr = None
        return

    def init_input_widget(self, on_num_changed, init_quantity=1, max_quantity=99):
        self.btn_mgr = NumAdjustBtnManager(init_quantity)

        def num_input_callback--- This code section failed: ---

  28       0  LOAD_FAST             0  'text'
           3  STORE_FAST            1  'final_text'

  29       6  STORE_FAST            1  'final_text'
           9  COMPARE_OP            2  '=='
          12  POP_JUMP_IF_FALSE    24  'to 24'

  30      15  LOAD_CONST            2  '0'
          18  STORE_FAST            1  'final_text'
          21  JUMP_FORWARD        109  'to 133'

  31      24  LOAD_GLOBAL           0  'str'
          27  LOAD_ATTR             1  'isdigit'
          30  LOAD_ATTR             3  'cur_num'
          33  BINARY_SUBSCR    
          34  CALL_FUNCTION_1       1 
          37  POP_JUMP_IF_TRUE     61  'to 61'

  32      40  LOAD_GLOBAL           0  'str'
          43  LOAD_DEREF            0  'self'
          46  LOAD_ATTR             2  'btn_mgr'
          49  LOAD_ATTR             3  'cur_num'
          52  CALL_FUNCTION_1       1 
          55  STORE_FAST            1  'final_text'
          58  JUMP_FORWARD         72  'to 133'

  33      61  LOAD_GLOBAL           0  'str'
          64  LOAD_ATTR             1  'isdigit'
          67  LOAD_FAST             0  'text'
          70  CALL_FUNCTION_1       1 
          73  POP_JUMP_IF_FALSE   133  'to 133'
          76  LOAD_GLOBAL           4  'int'
          79  LOAD_FAST             0  'text'
          82  CALL_FUNCTION_1       1 
          85  LOAD_DEREF            1  'max_quantity'
          88  COMPARE_OP            4  '>'
          91  POP_JUMP_IF_TRUE    112  'to 112'
          94  LOAD_GLOBAL           4  'int'
          97  LOAD_FAST             0  'text'
         100  CALL_FUNCTION_1       1 
         103  LOAD_CONST            4  ''
         106  COMPARE_OP            1  '<='
       109_0  COME_FROM                '91'
       109_1  COME_FROM                '73'
         109  POP_JUMP_IF_FALSE   133  'to 133'

  34     112  LOAD_GLOBAL           0  'str'
         115  LOAD_DEREF            0  'self'
         118  LOAD_ATTR             2  'btn_mgr'
         121  LOAD_ATTR             3  'cur_num'
         124  CALL_FUNCTION_1       1 
         127  STORE_FAST            1  'final_text'
         130  JUMP_FORWARD          0  'to 133'
       133_0  COME_FROM                '130'
       133_1  COME_FROM                '58'
       133_2  COME_FROM                '21'

  37     133  LOAD_GLOBAL           0  'str'
         136  LOAD_ATTR             1  'isdigit'
         139  LOAD_FAST             1  'final_text'
         142  CALL_FUNCTION_1       1 
         145  POP_JUMP_IF_TRUE    163  'to 163'

  38     148  LOAD_GLOBAL           0  'str'
         151  LOAD_DEREF            2  'init_quantity'
         154  CALL_FUNCTION_1       1 
         157  STORE_FAST            1  'final_text'
         160  JUMP_FORWARD          0  'to 163'
       163_0  COME_FROM                '160'

  41     163  LOAD_GLOBAL           4  'int'
         166  LOAD_FAST             1  'final_text'
         169  CALL_FUNCTION_1       1 
         172  LOAD_DEREF            0  'self'
         175  LOAD_ATTR             2  'btn_mgr'
         178  STORE_ATTR            3  'cur_num'

  43     181  LOAD_DEREF            0  'self'
         184  LOAD_ATTR             5  'input_box'
         187  LOAD_ATTR             6  'set_text'
         190  LOAD_GLOBAL           0  'str'
         193  LOAD_DEREF            0  'self'
         196  LOAD_ATTR             2  'btn_mgr'
         199  LOAD_ATTR             3  'cur_num'
         202  CALL_FUNCTION_1       1 
         205  CALL_FUNCTION_1       1 
         208  POP_TOP          

  45     209  LOAD_DEREF            3  'on_num_changed'
         212  LOAD_DEREF            0  'self'
         215  LOAD_ATTR             2  'btn_mgr'
         218  LOAD_ATTR             3  'cur_num'
         221  CALL_FUNCTION_1       1 
         224  POP_TOP          

Parse error at or near `STORE_FAST' instruction at offset 6

        self.input_box = InputBox(self.panel.temp_input, max_length=6)
        self.input_box.set_text(str(self.btn_mgr.cur_num))
        self.input_box.enable_input(False)

        def btn_touch_callback(num):
            self.input_box.set_text(str(self.btn_mgr.cur_num))
            on_num_changed(self.btn_mgr.cur_num)

        btn_data = {'max_num': max_quantity,'min_num': init_quantity,'adjust_cb': btn_touch_callback}
        btn_data['per_num'] = 1
        self.btn_mgr.add_new_btn(self.panel, self.panel.btn_plus, btn_data)
        btn_data['per_num'] = -1
        self.btn_mgr.add_new_btn(self.panel, self.panel.btn_minus, btn_data)
        btn_data['per_num'] = 10
        self.btn_mgr.add_new_btn(self.panel, self.panel.btn_add_value, btn_data)
        on_num_changed(self.btn_mgr.cur_num)


class NumAdjustBtn(object):

    def __init__(self, panel, btn, data, btn_mgr):
        self.panel = panel
        self.adjust_btn = btn
        self.btn_mgr = btn_mgr
        self.max_num = data.get('max_num')
        self.min_num = data.get('min_num')
        self.per_num = data.get('per_num')
        self.adjust_cb = data.get('adjust_cb')
        self.press_act_delay = 0.5
        self.press_act_interval = 0.03
        self.press_event = True
        self.break_change = False
        self.press_act_tag = 202205060 + self.per_num
        self.init_adjust_btn()

    def destroy(self):
        self.panel and self.panel.stopAllActions()
        self.adjust_btn and self.adjust_btn.stopAllActions()
        self.panel = None
        self.adjust_cb = None
        return

    def init_adjust_btn(self):

        @self.adjust_btn.unique_callback()
        def OnBegin(btn, touch):
            btn.SetSelect(True)
            if self.press_event:
                btn.SetTimeOut(self.press_act_delay, self.start_press_timer, self.press_act_tag)
            self.break_change = False
            return True

        @self.adjust_btn.unique_callback()
        def OnEnd(btn, touch):
            btn.SetSelect(False)
            if self.press_event:
                self.break_change = True
                btn.stopActionByTag(self.press_act_tag)

        @self.adjust_btn.unique_callback()
        def OnClick(btn, touch):
            self.change_num()

        @self.adjust_btn.unique_callback()
        def OnCancel(btn, touch):
            btn.SetSelect(False)
            if self.press_event:
                self.break_change = True
                btn.stopActionByTag(self.press_act_tag)
            return True

    def start_press_timer(self):
        self.panel.DelayCall(0.03, self.change_num)

    def change_num(self):
        next_delay_time = self.press_act_interval
        self.btn_mgr.cur_num += self.per_num
        if self.btn_mgr.cur_num > self.max_num:
            self.btn_mgr.cur_num = self.max_num
            next_delay_time = None
        if self.btn_mgr.cur_num < self.min_num:
            self.btn_mgr.cur_num = self.min_num
            next_delay_time = None
        if self.break_change:
            next_delay_time = None
        if self.adjust_cb and callable(self.adjust_cb):
            self.adjust_cb(self.btn_mgr.cur_num)
        return next_delay_time


class NumAdjustBtnManager(object):

    def __init__(self, num):
        self.cur_num = num
        self.btns = {}
        self.btn_cnt = 0

    def destroy(self):
        for btn in six.itervalues(self.btns):
            btn.destroy()

        self.btns = {}
        self.btn_cnt = 0

    def add_new_btn(self, panel, btn, data):
        self.btns[self.btn_cnt] = NumAdjustBtn(panel, btn, data, self)
        self.btn_cnt += 1
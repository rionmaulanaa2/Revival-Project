# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/InputMockHelper.py
from __future__ import absolute_import
import cc

class TouchMock(object):

    def __init__(self, pos=None, start_pos=None):
        self._tid = 1
        self._need_add_start_pos = False
        self.setTouchStartPos(start_pos)
        self.setTouchPos(pos)

    def setTouchPos(self, pos=None):
        if pos:
            self._touch_pos = pos
        else:
            self._touch_pos = cc.Vec2(0, 0)
        if self._touch_start_pos and self._need_add_start_pos:
            self._touch_pos = cc.Vec2(self._touch_pos.x + self._touch_start_pos.x, self._touch_pos.y + self._touch_start_pos.y)

    def setTouchStartPos(self, pos=None):
        if pos:
            self._touch_start_pos = pos
        else:
            self._touch_start_pos = None
        return

    def setTouchId(self, tid):
        self._tid = tid

    def setNeedAddStartPos(self, val):
        self._need_add_start_pos = val

    def getLocation(self):
        return self._touch_pos

    def getId(self):
        return self._tid

    def getDelta(self):
        return cc.Vec2(0, 0)

    def getStartLocation(self):
        if self._touch_start_pos is not None:
            return self._touch_start_pos
        else:
            return cc.Vec2(0, 0)
            return


def trigger_ui_btn_event(ui_name, node_path, event_name='OnClick', pos_spec=None, need_check_vis=False):
    ui_inst = global_data.ui_mgr.get_ui(ui_name)
    if ui_inst:
        node_name_list = node_path.split('.')
        ctrl = ui_inst.panel
        for name in node_name_list:
            ctrl = getattr(ctrl, name)

        node = ctrl
        if need_check_vis and not global_data.is_yunying:
            if not node.IsVisible():
                return
        if node and node.isTouchEnabled():
            event_func = getattr(node, event_name)
            if event_func:
                if pos_spec:
                    pos = pos_spec
                else:
                    pos = None
                event_func(TouchMock(pos))
    return


def trigger_ui_btn_event_compatible--- This code section failed: ---

  75       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'is_pc_mode'
           6  POP_JUMP_IF_FALSE    35  'to 35'

  76       9  LOAD_GLOBAL           2  'trigger_ui_btn_event'
          12  LOAD_GLOBAL           1  'is_pc_mode'
          15  BINARY_ADD       
          16  LOAD_FAST             1  'node_path'
          19  LOAD_FAST             2  'event_name'
          22  LOAD_FAST             3  'pos_spec'
          25  LOAD_FAST             4  'need_check_vis'
          28  CALL_FUNCTION_5       5 
          31  POP_TOP          
          32  JUMP_FORWARD         22  'to 57'

  78      35  LOAD_GLOBAL           2  'trigger_ui_btn_event'
          38  LOAD_FAST             0  'ui_name'
          41  LOAD_FAST             1  'node_path'
          44  LOAD_FAST             2  'event_name'
          47  LOAD_FAST             3  'pos_spec'
          50  LOAD_FAST             4  'need_check_vis'
          53  CALL_FUNCTION_5       5 
          56  POP_TOP          
        57_0  COME_FROM                '32'

Parse error at or near `CALL_FUNCTION_5' instruction at offset 28
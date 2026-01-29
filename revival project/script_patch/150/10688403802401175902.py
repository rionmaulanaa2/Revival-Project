# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonGuideTipsUI.py
from __future__ import absolute_import
import copy
from logic.gutils import role_head_utils
from common.cfg import confmgr
import cc
from logic.gutils.template_utils import set_node_position_in_screen
from common.const.uiconst import BATTLE_MESSAGE_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon import time_utility as tutil
import math
from common.const import uiconst

class CommonGuideTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/tips_label_with_ani'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        self.panel.nd_vx_lab.setVisible(False)

    def set_tips(self, txt):
        self.panel.temp_lab.lab_tips.SetString(txt)

    def set_show_parent(self, parent_class, wpos, scale=1.0, pos_consider_offset=True):
        ass_parent_ui = global_data.ui_mgr.get_ui(parent_class)
        if ass_parent_ui:
            ass_parent_ui.add_associate_vis_ui(str(self.__class__.__name__))
            adjust_pos_node = self.panel.nd_vx_lab
            adjust_pos_node.setScale(scale)
            if pos_consider_offset:
                set_node_position_in_screen(adjust_pos_node, ass_parent_ui.panel, wpos)
            else:
                pos = adjust_pos_node.getParent().convertToNodeSpace(wpos)
                adjust_pos_node.setPosition(pos)

    def show_tips(self, need_close=True):
        self.panel.StopAnimation('hide_lab')
        self.panel.stopActionByTag(20220608)
        self.panel.stopActionByTag(20220607)
        self.panel.nd_vx_lab.setVisible(True)
        self.panel.PlayAnimation('show_lab')

        def hide_lab--- This code section failed: ---

  52       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'PlayAnimation'
           9  LOAD_CONST            1  'hide_lab'
          12  CALL_FUNCTION_1       1 
          15  POP_TOP          

  54      16  LOAD_CLOSURE          1  'need_close'
          19  LOAD_CLOSURE          0  'self'
          25  LOAD_CONST               '<code_object cb>'
          28  MAKE_CLOSURE_0        0 
          31  STORE_FAST            0  'cb'

  59      34  LOAD_DEREF            0  'self'
          37  LOAD_ATTR             0  'panel'
          40  LOAD_ATTR             2  'SetTimeOut'
          43  LOAD_CONST            3  1.0
          46  LOAD_CONST            4  'tag'
          49  LOAD_CONST            5  20220608
          52  CALL_FUNCTION_258   258 
          55  POP_TOP          

Parse error at or near `CALL_FUNCTION_258' instruction at offset 52

        self.panel.SetTimeOut(3.0, lambda : hide_lab(), tag=20220607)
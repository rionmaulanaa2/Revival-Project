# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoCandyShop.py
from __future__ import absolute_import
import cc
import time
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
STABLE_TIME = 0.46

class BattleInfoCandyShop(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_top_candy_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }
    PC_ROOT_NODE_POS_X = 201

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoCandyShop, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.init_custom_com()
        self.panel.RecordAnimationNodeState('up_show')
        self.check_visible('BattleInfoMessageVisibleUI')
        if global_data.is_pc_mode:
            self.panel.SetPosition(self.PC_ROOT_NODE_POS_X, self.panel.GetPosition()[1])

    def on_finalize_panel--- This code section failed: ---

  34       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'custom_ui_com'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'custom_ui_com'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    46  'to 46'

  35      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'custom_ui_com'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

  36      34  LOAD_CONST            0  ''
          37  LOAD_FAST             0  'self'
          40  STORE_ATTR            1  'custom_ui_com'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'
          46  LOAD_CONST            0  ''
          49  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_event(self):
        pass

    def process_one_message(self, message, finish_cb):

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        show_in_t = self.panel.GetAnimationMaxRunTime('up_show')
        ac_list = [
         cc.DelayTime.create(1)]
        ac_list.append(cc.DelayTime.create(show_in_t))
        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self._recover_animation_node_without_position('up_show')
        self.panel.up.setOpacity(0)
        self.panel.nd_ab.setOpacity(0)
        self.panel.PlayAnimation('up_show')
        self.panel.runAction(cc.Sequence.create(ac_list))
        self.up.setVisible(True)

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()

    def _recover_animation_node_without_position(self, animation):
        position = self.panel.up.getPosition()
        self.panel.RecoverAnimationNodeState(animation)
        self.panel.up.setPosition(position)
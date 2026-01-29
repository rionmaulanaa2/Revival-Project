# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Magic/MagicHunterFieldRefresh.py
from __future__ import absolute_import
from logic.comsys.battle.BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.gcommon.common_const import poison_circle_const
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import cc
from logic.gcommon.time_utility import time

class MagicHunterFieldRefresh(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/hunter_tips/fight_top_hunter_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }
    PC_ROOT_NODE_POS_X = 201

    def on_init_panel(self, on_process_done=None):
        super(MagicHunterFieldRefresh, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.check_visible('BattleInfoMessageVisibleUI')
        self.init_custom_com()
        self.panel.RecordAnimationNodeState('up_show')
        self.panel.RecordAnimationNodeState('up_disappear')
        self.cur_text_id = 6002
        if global_data.is_pc_mode:
            self.panel.SetPosition(self.PC_ROOT_NODE_POS_X, self.panel.GetPosition()[1])

    def on_finalize_panel--- This code section failed: ---

  33       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'custom_ui_com'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'custom_ui_com'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    46  'to 46'

  34      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'custom_ui_com'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

  35      34  LOAD_CONST            0  ''
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
        if not global_data.battle:
            return
        wpos = global_data.emgr.get_map_hint_wpos_event.emit()
        if wpos and len(wpos) > 0:
            lpos = self.panel.getParent().convertToNodeSpace(wpos[0])
            self.panel.setPosition(lpos)
        self.cnt = 0
        is_ace_time = global_data.battle.is_in_ace_state
        self.panel.lab_poison1.setVisible(is_ace_time)
        self.panel.lab_begin.setVisible(not is_ace_time)

        def show_out():
            if self and self.is_valid():
                self._recover_animation_node_without_position('up_disappear')
                self.panel.PlayAnimation('up_disappear')

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        show_in_t = self.panel.GetAnimationMaxRunTime('up_show')
        show_out_t = self.panel.GetAnimationMaxRunTime('up_disappear')
        self._recover_animation_node_without_position('up_show')
        self.add_hide_count('TEMPO')
        cur_time = time()

        def start_show():
            self.add_show_count('TEMPO')
            self.panel.PlayAnimation('up_show')

        ac_list = []
        ac_list.extend([
         cc.CallFunc.create(start_show),
         cc.DelayTime.create(2),
         cc.CallFunc.create(show_out),
         cc.DelayTime.create(show_out_t),
         cc.CallFunc.create(finished)])
        self.panel.stopAllActions()
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
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoPlayerNumber.py
from __future__ import absolute_import
import cc
import time
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
STABLE_TIME = 0.46

class BattleInfoPlayerNumber(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_top_survive'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoPlayerNumber, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.init_custom_com()
        self.panel.RecordAnimationNodeState('survive_x')
        self.check_visible('BattleInfoMessageVisibleUI')
        self._survive_num = 0
        self._last_play_time = 0

    def on_finalize_panel--- This code section failed: ---

  31       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'custom_ui_com'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'custom_ui_com'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    46  'to 46'

  32      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'custom_ui_com'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

  33      34  LOAD_CONST            0  ''
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

    def process_next_message(self):
        if len(self.message_sequence) > 0:
            self.playing = True
            message = self.message_sequence[-1]
            now_number = message[0][1]
            if time.time() - self._last_play_time < STABLE_TIME:
                self.panel.lab_distance_now.SetString(str(now_number))
                self._survive_num = now_number
            else:
                last_number = message[0][0]
                self.process_message(last_number, now_number)
            self.message_sequence = []
        else:
            self.playing = False
            if self.on_process_done:
                self.on_process_done()

    def process_message(self, last_number, now_number):
        self.panel.lab_distance_pre.SetString(str(last_number))
        self.panel.lab_distance_now.SetString(str(now_number))

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        def update_map_num():
            global_data.emgr.update_map_info_widget_event.emit(self._survive_num)

        anim_time = self.panel.GetAnimationMaxRunTime('survive_x')
        ac_list = [
         cc.DelayTime.create(STABLE_TIME),
         cc.CallFunc.create(update_map_num),
         cc.DelayTime.create(anim_time - STABLE_TIME),
         cc.CallFunc.create(finished)]
        self.panel.up.setVisible(True)
        self.panel.stopAllActions()
        self._recover_animation_node_without_position('survive_x')
        self.panel.PlayAnimation('survive_x')
        self.panel.runAction(cc.Sequence.create(ac_list))
        self._last_play_time = time.time()
        self._survive_num = now_number

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()

    def _recover_animation_node_without_position(self, animation):
        position = self.panel.up.getPosition()
        self.panel.RecoverAnimationNodeState(animation)
        self.panel.up.setPosition(position)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoAreaInfo.py
from __future__ import absolute_import
import cc
import time
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.cfg import confmgr
from logic.gutils import judge_utils

class BattleInfoAreaInfo(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_area_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoAreaInfo, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.init_custom_com()
        self.panel.RecordAnimationNodeState('show')
        self.panel.RecordAnimationNodeState('disappear')
        self.check_visible('BattleInfoMessageVisibleUI')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

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

    def init_event(self):
        pass

    def add_message(self, *args):
        if judge_utils.is_ob():
            return
        super(BattleInfoAreaInfo, self).add_message(*args)

    def process_next_message(self):
        if len(self.message_sequence) > 0:
            message = self.message_sequence[-1]
            self.playing = True
            self.process_message(message)
            self.message_sequence = []
        else:
            self.playing = False
            if self.on_process_done:
                self.on_process_done()

    def process_message(self, message):
        area_info = message[0]
        name_text_id = area_info.get('name_text_id')
        self.panel.lab_name.SetString(name_text_id)
        rich_id = area_info.get('rich_id')
        rich_info = confmgr.get('map_area_conf', 'MapAreaRichConfig', 'Content', str(rich_id))
        self.panel.lab_rich.SetString(rich_info.get('text_id'))
        self.panel.lab_rich.SetColor(rich_info.get('text_color'))
        self.panel.icon_rich.SetDisplayFrameByPath('', rich_info.get('icon_path'))
        self.up.setVisible(False)

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        def start_show():
            if self and self.is_valid():
                self.panel.up.setVisible(True)
                self.panel.PlayAnimation('show')

        def show_out():
            if self and self.is_valid():
                self._recover_animation_node_without_position('disappear')
                self.panel.PlayAnimation('disappear')

        anim_time = self.panel.GetAnimationMaxRunTime('show')
        disappear_anim_time = self.panel.GetAnimationMaxRunTime('disappear')
        ac_list = [
         cc.CallFunc.create(start_show),
         cc.DelayTime.create(anim_time + 5),
         cc.CallFunc.create(show_out),
         cc.DelayTime.create(disappear_anim_time),
         cc.CallFunc.create(finished)]
        self.panel.stopAllActions()
        self._recover_animation_node_without_position('show')
        self.panel.runAction(cc.Sequence.create(ac_list))

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()

    def _recover_animation_node_without_position(self, animation):
        position = self.panel.up.getPosition()
        self.panel.RecoverAnimationNodeState(animation)
        self.panel.up.setPosition(position)
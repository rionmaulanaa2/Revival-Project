# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoVoice.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import math3d
import cc
from common.utilities import get_utf8_length, cut_string_by_len
import common.utils.timer as timer

class BattleInfoVoice(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/i_host_voice'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoVoice, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.init_custom_com()
        self.msg_text = None
        self.text_index = 0
        self.finish_callback = None
        self._is_showing = False
        self.init_pos()
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_pos(self):
        wpos = global_data.emgr.get_map_hint_wpos_event.emit()
        if wpos and len(wpos) > 0:
            lpos = self.panel.getParent().convertToNodeSpace(wpos[0])
            self.panel.setPosition(lpos)

    def process_one_message(self, message, finish_cb):
        self._is_showing = True
        self.finish_callback = finish_cb
        ui = global_data.ui_mgr.get_ui('AnchorVoiceTip')
        if not ui:
            self.on_finish()
            return
        self.msg_text = ui.get_text()
        if not self.msg_text:
            self.on_finish()
            return
        self.msg_text = message[0]
        self.show()
        self.panel.StopAnimation('up_disappear')
        self.panel.PlayAnimation('up_show')
        show_in_t = self.panel.GetAnimationMaxRunTime('up_show')
        self.panel.lab_airdrop.SetString('')
        self.panel.stopActionByTag(1)
        self.panel.DelayCallWithTag(show_in_t, self.start_show, 1)

    def start_show(self):
        self.text_fade_in()
        self.panel.PlayAnimation('up_keep')
        self.panel.stopActionByTag(1)
        self.panel.DelayCallWithTag(30, self.on_finish, 1)

    def text_fade_in(self):
        count = get_utf8_length(self.msg_text)
        self.text_index = 0

        def add_one_char(dt):
            self.text_index += 1
            if self.text_index >= count:
                self.text_index = count
            sub_text = cut_string_by_len(self.msg_text, self.text_index)
            self.panel.lab_airdrop.SetString(sub_text)

        self.panel.TimerAction(add_one_char, 0.0333 * (count + 1), interval=0.0333)

    def on_finish(self):
        if not self._is_showing:
            return
        else:
            self._is_showing = False
            self.panel.stopActionByTag(1)
            self.panel.StopTimerAction()
            self.panel.StopAnimation('up_show')
            self.panel.StopAnimation('up_keep')
            self.panel.PlayAnimation('up_disappear')
            if self.finish_callback:
                self.finish_callback()
                self.finish_callback = None
            return

    def on_finalize_panel--- This code section failed: ---

  98       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'custom_ui_com'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'custom_ui_com'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    46  'to 46'

  99      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'custom_ui_com'
          27  LOAD_ATTR             2  'destroy'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

 100      34  LOAD_CONST            0  ''
          37  LOAD_FAST             0  'self'
          40  STORE_ATTR            1  'custom_ui_com'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'
          46  LOAD_CONST            0  ''
          49  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_click_bg_layer(self, btn, touch):
        self.on_finish()
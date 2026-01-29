# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/FightChatUIPC.py
from __future__ import absolute_import
from .FightChatUI import FightChatBaseUI
from logic.gutils import judge_utils
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
import cc

class FightChatUIPC(FightChatBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_chat_pc'
    UI_ACTION_EVENT = {'bg_layer.OnBegin': 'on_bg_layer_begin',
       'btn_enter.OnEnd': 'on_click_btn_send'
       }

    def on_init_panel(self, *args, **kargs):
        super(FightChatUIPC, self).on_init_panel()
        self.panel.btn_enter.setVisible(True)
        self.is_in_spectate = False

    def on_enter_observe(self, target):
        self.is_in_spectate = True

    def on_fight_chat_ui(self, *args):
        if self.is_in_spectate or judge_utils.is_ob():
            if self.panel.pnl_chat_list.isVisible:
                self.chat_close()
            return
        if not self.panel.pnl_chat_list.isVisible():
            self.chat_open()
        else:
            self.chat_close()

    def chat_open_core(self):
        super(FightChatUIPC, self).chat_open_core()
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(lambda : self.auto_click_input_box())]))

    def auto_click_input_box(self):
        if self._input_box is None:
            return
        else:
            click_input_box = getattr(self._input_box._pnl_input.touch_layer, 'OnClick')
            click_input_box(TouchMock(None))
            return

    def resize_record_list(self, small):
        self.panel.list_chat_record.SetContentSize(296, 70 if small else 226)
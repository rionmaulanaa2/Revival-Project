# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatEditedInput.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import logic.comsys.common_ui.InputBox as InputBox
MAX_LENGTH = 15
from common.const import uiconst

class ChatEditedInput(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'chat/add_quick_chat'
    UI_ACTION_EVENT = {'panel.panel.btn_close.OnClick': 'on_close',
       'confirm.btn_common_big.OnClick': 'on_confirm'
       }

    def on_init_panel(self, *args, **kargs):
        self._input_box = InputBox.InputBox(self.panel.inputbox, max_length=MAX_LENGTH, placeholder=' ')
        self._callback = None
        return

    def set_callback(self, callback):
        self._callback = callback

    def on_confirm(self, *args):
        text = self._input_box.get_text()
        if text:
            if self._callback:
                self._callback(text)
        self.close()

    def on_close(self, *args):
        self.close()

    def set_close_callback(self, callback):
        self.close_callback = callback

    def on_finalize_panel(self):
        pass
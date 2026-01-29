# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/ChatCharge.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
from common.const import uiconst

class ChatCharge(BasePanel):
    PANEL_CONFIG_NAME = 'chat/chat_charge'
    UI_TYPE = common.const.uiconst.UI_TYPE_CONFIRM
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_click_close',
       'temp_btn_voice.btn_common.OnClick': 'on_send_voice',
       'temp_btn_text.btn_common.OnClick': 'on_send_text'
       }

    def on_init_panel(self, *args, **kwargs):
        self.voice_data = None
        self.voice_text = None
        self._send_voice_callback = None
        self._send_text_callback = None
        self.init_widget()
        return

    def on_finalize_panel(self):
        pass

    def init_widget(self):
        self.panel.txt_content.SetString(11115)
        self.panel.temp_btn_text.setVisible(False)
        self.panel.temp_btn_voice.setVisible(False)

    def on_voice_msg_send(self, voice_text, voice_data, finish=True):
        if not self.panel:
            return
        self.voice_data = voice_data
        self.voice_text = voice_text
        self.panel.txt_content.SetString(voice_text)
        if finish:
            self.panel.temp_btn_text.setVisible(True)
            self.panel.temp_btn_voice.setVisible(True)

    def set_send_voice_callback(self, callback):
        self._send_voice_callback = callback

    def set_send_text_callback(self, callback):
        self._send_text_callback = callback

    def on_click_close(self, *args):
        self.close()

    def on_send_voice(self, *args):
        if self._send_voice_callback:
            self._send_voice_callback(self.voice_text, self.voice_data)
            self._send_voice_callback = None
        self.close()
        return

    def on_send_text(self, *args):
        if self._send_text_callback:
            self._send_text_callback(self.voice_text)
            self._send_text_callback = None
        self.close()
        return
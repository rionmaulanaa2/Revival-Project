# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/PhoneBindUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
TimerId = None
REQ_CD = 60
REQ_CNT = 0

class PhoneBindUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/common_verify'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_pnl'

    def on_click_close_btn(self, *args):
        self.close()

    def on_init_panel(self, phone=None):
        global REQ_CNT
        super(PhoneBindUI, self).on_init_panel()
        self._input_number = InputBox.InputBox(self.panel.input_phone_number, placeholder=get_text_by_id(147), max_length=50)
        self._input_number.set_rise_widget(self.panel)
        if phone:
            self._input_number.set_text(phone)
        self._input_code = InputBox.InputBox(self.panel.input_verify_num, placeholder=get_text_by_id(148), max_length=6)
        self._input_code.set_rise_widget(self.panel)

        @self.panel.temp_btn_getcode.btn_common.callback()
        def OnClick(*args):
            global REQ_CNT
            phone = self._input_number.get_text()
            if not self.check_valid_number(phone, 'phone'):
                return global_data.player.notify_client_message((get_text_by_id(149),))
            global_data.player.req_send_sms(phone)
            REQ_CNT = REQ_CD
            self.start_timer()
            self.enbale_get_btn(False)

        @self.panel.btn_create.btn_common_big.callback()
        def OnClick(*args):
            phone = self._input_number.get_text()
            if not self.check_valid_number(phone, 'phone'):
                return global_data.player.notify_client_message((get_text_by_id(149),))
            code = self._input_code.get_text()
            if not self.check_valid_number(code, 'code'):
                return global_data.player.notify_client_message((get_text_by_id(150),))
            global_data.player.req_verify_and_bind(phone, code)

        if REQ_CNT > 0:
            self.stop_timer()
            self.start_timer()
            self.panel.temp_btn_getcode.btn_common.SetText(get_text_by_id(151).format(REQ_CNT))
            self.enbale_get_btn(False)

    def check_valid_number(self, text, ctype):
        if ctype == 'phone':
            return len(text) == 11 and text.isdigit() and text[0] == '1'
        if ctype == 'code':
            return len(text) == 6 and text.isdigit()
        if ctype == 'email':
            import re
            ret = re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$', text)
            return bool(ret)

    def start_timer(self):
        global TimerId
        from common.utils.timer import CLOCK
        tm = global_data.game_mgr.get_logic_timer()
        TimerId = tm.register(func=self.update, interval=1.0, times=-1, mode=CLOCK)

    def stop_timer(self):
        global TimerId
        if TimerId:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(TimerId)
            TimerId = None
        if self and self.is_valid():
            self.enbale_get_btn(True)
        return

    def update(self):
        global REQ_CNT
        REQ_CNT -= 1
        if self and self.is_valid():
            self.panel.temp_btn_getcode.btn_common.SetText(get_text_by_id(151).format(REQ_CNT))
        if REQ_CNT <= 0:
            self.stop_timer()

    def enbale_get_btn(self, enable):
        self.panel.temp_btn_getcode.btn_common.SetEnableTouch(enable)
        if enable:
            self.panel.temp_btn_getcode.btn_common.SetText(get_text_by_id(152))

    def on_finalize_panel(self):
        if self._input_number:
            self._input_number.destroy()
            self._input_number = None
        if self._input_code:
            self._input_code.destroy()
            self._input_code = None
        return
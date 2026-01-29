# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/EmailBindUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
TimerId = None
REQ_CD = 60
REQ_CNT = 0

class EmailBindUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/email_binding'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_pnl'

    def on_init_panel(self):
        super(EmailBindUI, self).on_init_panel()
        self._input_email = InputBox.InputBox(self.panel.input_mail)

        @self.panel.btn_create.btn_common_big.callback()
        def OnClick(*args):
            email = self._input_email.get_text()
            if not self.check_valid_number(email, 'email'):
                return global_data.player.notify_client_message((get_text_by_id(169),))
            self.panel.btn_create.btn_common_big.SetEnable(False)
            self.panel.btn_create.btn_common_big.SetText(get_text_by_id(80621))
            global_data.game_mgr.show_tip(80622)
            global_data.player.req_bind_email(email)

    def check_valid_number(self, text, ctype):
        if ctype == 'phone':
            return len(text) == 11 and text.isdigit() and text[0] == '1'
        if ctype == 'code':
            return len(text) == 6 and text.isdigit()
        if ctype == 'email':
            import re
            ret = re.match('^[a-zA-Z0-9_\\.\\-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$', text)
            return bool(ret)

    def on_finalize_panel(self):
        if self._input_email:
            self._input_email.destroy()
            self._input_email = None
        return
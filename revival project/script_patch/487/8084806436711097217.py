# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/EmailUnBindUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class EmailUnBindUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/phone_binding_result'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_pnl'

    def on_init_panel(self, email=None):
        super(EmailUnBindUI, self).on_init_panel()
        self.cur_email = email
        self.panel.temp_pnl.lab_title.SetString(get_text_by_id(80617))
        self.panel.lab_phone.SetString(get_text_by_id(80619))
        self.panel.btn_cancel_binding.btn_common_big.SetText(get_text_by_id(80618))

        @self.panel.btn_cancel_binding.btn_common_big.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            cur_email = self.cur_email

            def unbind():
                global_data.player.req_unbind_email(cur_email)
                global_data.player.set_cur_bind_email('')
                self.close()

            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(80620).format(self.get_display_number(str(cur_email))), confirm_callback=unbind)

        if self.cur_email:
            self.panel.btn_cancel_binding.setVisible(True)
            self.panel.lab_phone_num.SetString(self.get_display_number(str(self.cur_email)))
        else:
            global_data.player.query_cur_bind_email()

    def on_get_cur_phone(self, email):
        self.cur_email = email
        if self.cur_email:
            self.panel.btn_cancel_binding.setVisible(True)
            self.panel.lab_phone_num.SetString(self.get_display_number(str(self.cur_email)))

    def get_display_number(self, number):
        prefix = number[0:3]
        sufix = number[7:]
        return prefix + '****' + sufix
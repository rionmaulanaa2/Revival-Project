# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/ProtocolConfirmUI.py
from __future__ import absolute_import
import game3d
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_MSG_ZORDER
from common.platform import channel
from common.const import uiconst
from common.platform.dctool import interface

class ProtocolConfirmUI(BasePanel):
    DLG_ZORDER = TOP_MSG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'login/agreement'
    IS_FULLSCREEN = True

    def on_init_panel(self, *args, **kargs):
        self.reject_btn = self.panel.bg_panel.temp_btn_1.btn_common_big
        self.confirm_btn = self.panel.bg_panel.temp_btn_2.btn_common_big
        self.agreement_btn = self.panel.btn_read_agreement
        self._init_text()
        self.init_event()
        self.init_data()

    def _init_text(self):
        if not interface.is_tw_package():
            self.panel.bg_panel.show_lable.SetString(83400)
            self.panel.btn_read_agreement.click_txt.SetString(83399)

    def init_data(self):
        pass

    def init_event(self):
        self.reject_btn.BindMethod('OnClick', self.on_click_reject)
        self.confirm_btn.BindMethod('OnClick', self.on_click_confirmed)
        self.agreement_btn.BindMethod('OnClick', self.on_click_read)

    def on_click_confirmed(self, *args):
        channel.Channel().on_protocol_finish_callback(channel.PROTOCOL_CODE_ACCEPT)
        self.close()

    def on_click_reject(self, *args):
        channel.Channel().on_protocol_finish_callback(channel.PROTOCOL_CODE_REJECT)
        self.close()
        game3d.exit()

    def on_click_read(self, *args):
        channel.Channel().show_compact_view()
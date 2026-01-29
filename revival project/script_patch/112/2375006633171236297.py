# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/InviteConfirmUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const.property_const import *
from common.const import uiconst

class InviteConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/normal_second_confirm_2'
    DLG_ZORDER = TOP_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_second_confirm.temp_btn_1.btn_common_big.OnClick': 'cancel',
       'temp_second_confirm.temp_btn_2.btn_common_big.OnClick': 'confirm'
       }

    def set_invite_info(self, confirm_id, content, option, confirm_cb=None, cancel_cb=None):
        self.confirm_id = confirm_id
        self.panel.temp_second_confirm.lab_content.SetString(unpack_text(content))
        self.panel.temp_second_confirm.temp_btn_1.btn_common_big.SetText(unpack_text(option[0]))
        self.panel.temp_second_confirm.temp_btn_2.btn_common_big.SetText(unpack_text(option[1]))
        self.confirm_cb = confirm_cb
        self.cancel_cb = cancel_cb

    def cancel(self, *args):
        if not global_data.player:
            self.close()
            print('??????[error] cancel global_data.player is None!!!!')
            return
        global_data.player.req_confirm(self.confirm_id, 0)
        callable(self.cancel_cb) and self.cancel_cb()
        self.close()

    def confirm(self, *args):
        if not global_data.player:
            self.close()
            print('????????[error] confirm global_data.player is None!!!!')
            return
        global_data.player.req_confirm(self.confirm_id, 1)
        callable(self.confirm_cb) and self.confirm_cb()
        self.close()
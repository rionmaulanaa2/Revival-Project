# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/AppointmentConfirmUI.py
from __future__ import absolute_import
import time
from .TeamRequestConfirmUI import TeamRequestConfirmUI
from common.const.uiconst import TOP_ZORDER, UI_TYPE_CONFIRM
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon import const
from common.const import uiconst

class AppointmentConfirmUI(TeamRequestConfirmUI):

    def set_invite_info(self, confirm_id, extra_info, confirm_type):
        super(AppointmentConfirmUI, self).set_invite_info(confirm_id, extra_info, confirm_type)
        self.panel.lab_title.SetString(19852)
        self.panel.btn_refuse.btn_common.SetText(907164)
        self.panel.btn_agree.btn_common.SetText(13141)
        self.init_count_down_timer()

    def cancel(self, *args):
        global_data.player.req_confirm(self.confirm_id, 1)
        self.close()

    def confirm(self, *args):
        global_data.player.req_confirm(self.confirm_id, 0)
        if global_data.player.is_in_team():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(13027), confirm_callback=lambda : global_data.player.confirm_join_if_in_team(True), cancel_callback=lambda : global_data.player.confirm_join_if_in_team(False))
        self.close()

    def close_invite(self, *args):
        self.cancel()
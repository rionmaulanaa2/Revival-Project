# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TeamRequestConfirmUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_TYPE_CONFIRM
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon import const
from common.const import uiconst

class TeamRequestConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/team_invite'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'btn_refuse.btn_common.OnClick': 'cancel',
       'btn_agree.btn_common.OnClick': 'confirm',
       'btn_close.OnClick': 'close_invite'
       }

    def on_init_panel(self):
        self.count_down_timer = None
        self._start_count_time = 0
        self._limit_count_down_time = 30
        self.panel.PlayAnimation('invite_show')
        self._init_refuse_text = self.panel.btn_refuse.btn_common.GetText()
        global_data.emgr.on_request_login_event += self.on_request_login
        return

    def on_request_login(self):
        self.close()

    def on_finalize_panel(self):
        self.destrot_count_down_timer()

    def destrot_count_down_timer(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
        self.count_down_timer = None
        return

    def init_count_down_timer(self):
        from common.utils.timer import CLOCK
        self._start_count_time = time.time()
        self.destrot_count_down_timer()
        self.count_down_timer = global_data.game_mgr.register_logic_timer(self.update_count_down, interval=1, times=self._limit_count_down_time, mode=CLOCK)
        self.update_count_down()

    def update_count_down(self):
        left_time = int(self._limit_count_down_time - (time.time() - self._start_count_time))
        if left_time <= 0:
            self.panel.btn_refuse.btn_common.SetText(self._init_refuse_text)
            self.cancel()
        else:
            self.panel.btn_refuse.btn_common.SetText(self._init_refuse_text + '(%ds)' % left_time)

    def set_invite_info(self, confirm_id, extra_info, confirm_type):
        self.confirm_id = confirm_id
        char_name = extra_info.get('char_name', '')
        head_frame = extra_info.get('head_frame')
        head_photo = extra_info.get('head_photo')
        uid = extra_info.get('uid')
        self.name.setString(unpack_text(char_name))
        role_head_utils.init_role_head(self.panel.head, head_frame, head_photo)
        nd = self.panel.head

        @nd.callback()
        def OnClick(*args):
            if not uid:
                return
            ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
            if ui:
                ui.clear_show_count_dict()
                ui.hide_main_ui()
            else:
                ui = global_data.ui_mgr.show_ui('PlayerInfoUI', 'logic.comsys.role')
            ui.refresh_by_uid(uid)

        fate_group_point = extra_info.get('fate_group_point', 0)
        if fate_group_point:
            self.panel.lab_recruit.SetString(get_text_by_id(13101, [fate_group_point]))
            self.panel.lab_recruit.setVisible(True)
        else:
            self.panel.lab_recruit.setVisible(False)
        role_head_utils.set_role_dan(self.panel.temp_tier, extra_info.get('dan_info'))
        if confirm_type == const.CONFIRM_TEAM_INVITE:
            self.panel.lab_title.setString(get_text_by_id(80527))
            self.init_count_down_timer()
        elif confirm_type == const.CONFIRM_TEAM_JOIN:
            self.panel.lab_title.setString(get_text_by_id(13077))
            self.init_count_down_timer()
        elif confirm_type == const.CONFIRM_CHANGE_SEAT:
            self.init_count_down_timer()
            self.panel.lab_title.setString(get_text_by_id(862017))

    def cancel(self, *args):
        global_data.player.req_confirm(self.confirm_id, 0)
        self.close()

    def confirm(self, *args):
        global_data.player.req_confirm(self.confirm_id, 1)
        self.close()

    def close_invite(self, *args):
        self.close()
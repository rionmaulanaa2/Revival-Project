# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/InviteRoomConfirmUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_TYPE_CONFIRM
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon import const
from logic.comsys.room.RoomPasswordUI import RoomPasswordUI
from common.cfg import confmgr
from logic.gcommon.common_utils.battle_utils import get_mode_name
from common.const import uiconst

class InviteRoomConfirmUI(BasePanel):
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
        self.panel.lab_title.setString(get_text_by_id(608181))
        self.panel.lab_recruit.setVisible(False)
        self.panel.PlayAnimation('invite_show')
        self._init_refuse_text = self.panel.btn_refuse.btn_common.GetText()
        return

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
        self.extra_info = extra_info
        char_name = extra_info.get('char_name', '')
        head_frame = extra_info.get('head_frame')
        head_photo = extra_info.get('head_photo')
        battle_type = extra_info.get('battle_type')
        mode_name = get_mode_name(battle_type)
        curr_player_num = extra_info.get('curr_player_num')
        max_player_num = extra_info.get('max_player_num')
        self.name.setString(unpack_text(char_name))
        self.lab_num.setVisible(True)
        self.lab_mode.setVisible(True)
        self.lab_num.SetString('({0}/{1})'.format(str(curr_player_num), str(max_player_num)))
        self.lab_mode.SetString(mode_name)
        role_head_utils.init_role_head(self.panel.head, head_frame, head_photo)
        role_head_utils.set_role_dan(self.panel.temp_tier, extra_info.get('dan_info'))
        self.init_count_down_timer()
        uid = extra_info.get('uid')
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

    def cancel(self, *args):
        global_data.player.req_confirm(self.confirm_id, 0)
        self.close()

    def confirm(self, *args):
        if global_data.player:
            room_id = self.extra_info.get('room_id')
            need_pwd = self.extra_info.get('need_pwd')
            battle_type = self.extra_info.get('battle_type')
            if need_pwd:

                def request_pwd(password=''):
                    global_data.player and global_data.player.req_enter_room(room_id, battle_type, password)

                RoomPasswordUI(None, confirm_cb=request_pwd, need_pwd=True, place_holder=get_text_by_id(19316))
            else:
                global_data.player.req_enter_room(room_id, battle_type, '')
            global_data.player.req_confirm(self.confirm_id, 1)
        self.close()
        return

    def close_invite(self, *args):
        self.close()
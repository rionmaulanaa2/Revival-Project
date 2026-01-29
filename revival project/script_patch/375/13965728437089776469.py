# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyMgr.py
from common.framework import Singleton
from logic.gcommon.const import OPEN_INTIMACY_REQUEST_KEY
from logic.gutils.jump_to_ui_utils import jump_to_player_info
from common.const.property_const import C_NAME
from logic.comsys.common_ui.NormalConfirmUI import LoginIntimacyEventOpenConfirmDlg
from logic.gcommon.common_utils.local_text import get_text_by_id

class IntimacyMgr(Singleton):
    ALIAS_NAME = 'intimacy_mgr'

    def init(self):
        self._archive_data = global_data.achi_mgr.get_general_archive_data()
        self._intimacy_event_uid_list = []
        global_data.emgr.lobby_ui_visible += self.on_lobby_ui_visible

    def on_finalize(self):
        global_data.emgr.lobby_ui_visible -= self.on_lobby_ui_visible
        self._archive_data = None
        self._intimacy_event_uid_list = None
        return

    def on_lobby_ui_visible(self, visible):
        if visible:
            self.check_show_intimacy_request_ui()
            self.check_show_intimacy_event_ui()

    def _get_intimacy_request_msg_list(self):
        return self._archive_data.get_field(OPEN_INTIMACY_REQUEST_KEY, [])

    def _set_intimacy_request_msg_list(self, cur_intimacy_msg_list):
        return self._archive_data.set_field(OPEN_INTIMACY_REQUEST_KEY, cur_intimacy_msg_list)

    def peek_next_request_msg(self):
        cur_intimacy_msg_list = self._get_intimacy_request_msg_list()
        if len(cur_intimacy_msg_list) > 0:
            return cur_intimacy_msg_list[0]
        else:
            return None
            return None

    def pop_next_request_msg(self):
        cur_intimacy_msg_list = self._get_intimacy_request_msg_list()
        if len(cur_intimacy_msg_list) > 0:
            cur_intimacy_msg = cur_intimacy_msg_list.pop(0)
            self._set_intimacy_request_msg_list(cur_intimacy_msg_list)
            return cur_intimacy_msg
        else:
            return None
            return None

    def try_add_intimacy_request_msg(self, uid, intimacy_type):
        if uid is None:
            log_error('try_add_intimacy_request_msg uid None')
            return
        else:
            if intimacy_type is None:
                log_error('try_add_intimacy_request_msg intimacy_type None')
                return
            uid = int(uid)
            cur_intimacy_msg_list = self._get_intimacy_request_msg_list()
            if uid in cur_intimacy_msg_list:
                return
            cur_intimacy_msg_list.append([uid, intimacy_type])
            self._archive_data.set_field(OPEN_INTIMACY_REQUEST_KEY, cur_intimacy_msg_list)
            return

    def check_show_intimacy_request_ui(self):
        msg = self.peek_next_request_msg()
        if msg is None:
            return
        else:
            ui = global_data.ui_mgr.get_ui('OpenIntimacyRequestUI')
            if global_data.player.has_advance_callback('OpenIntimacyRequestUI') or ui:
                return

            def callback():
                global_data.ui_mgr.show_ui('OpenIntimacyRequestUI', 'logic.comsys.intimacy')

            if global_data.player and global_data.player.is_running_show_advance():
                global_data.player.add_advance_callback('OpenIntimacyRequestUI', callback, advance_first=False)
            else:
                callback()
            return

    def try_add_intimacy_event_msg(self, uid):
        if uid is None:
            log_error('try_add_intimacy_event_msg uid None')
            return
        else:
            uid = int(uid)
            if uid in self._intimacy_event_uid_list:
                return
            self._intimacy_event_uid_list.append(uid)
            return

    def check_show_intimacy_event_ui(self):
        if not self._intimacy_event_uid_list:
            return
        if global_data.player and global_data.player.is_running_show_advance():
            if not global_data.player.has_advance_callback('LoginIntimacyEventOpenConfirmDlg'):
                global_data.player.add_advance_callback('LoginIntimacyEventOpenConfirmDlg', self.advance_callback, advance_first=False)
        else:
            self.advance_callback()

    def advance_callback(self):
        friend_name = ''
        for i, uid in enumerate(self._intimacy_event_uid_list):
            friend_info = global_data.message_data.get_friends().get(uid, None)
            if not friend_info:
                continue
            friend_name = friend_name + str(friend_info[C_NAME])
            if i != len(self._intimacy_event_uid_list) - 1:
                friend_name = friend_name + ','

        friend_str = get_text_by_id(860269).format(friend_name)

        def confirm_callback():
            from logic.comsys.role.PlayerInfoUI import TAB_INTIMACY_INFO
            jump_to_player_info(TAB_INTIMACY_INFO)
            ui = global_data.ui_mgr.get_ui('IntimacyLevelupUI')
            if ui:
                ui.close()

        global_data.player.add_enable_inti_mem_frds(self._intimacy_event_uid_list)
        self._intimacy_event_uid_list = []
        LoginIntimacyEventOpenConfirmDlg().confirm(content=friend_str, confirm_callback=confirm_callback)
        return
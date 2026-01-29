# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/LineGameInviteList.py
from __future__ import absolute_import
from common.const.property_const import *
import logic.gcommon.const as const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import share_const
import logic.gutils.share_utils
from logic.comsys.message.LineGameFriendList import LineGameFriendList
from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
from logic.gcommon.common_const import friend_const
from logic.gutils import friend_utils
from logic.comsys.effect.ui_effect import set_gray
from logic.gutils import online_state_utils as st_utils

class LineGameInviteList(LineGameFriendList):
    PANEL_CONFIG_NAME = 'lobby/invite_other_friend_list'

    def refresh_linegame_friends(self):
        self._list_add.DeleteAllSubItem()
        social_friends = self._message_data.get_social_friends(friend_const.SOCIAL_ID_TYPE_LINEGAME)
        linegame_friendinfos = self._message_data.get_linegame_friends()
        count = 0
        for data in social_friends:
            linegame_data = linegame_friendinfos.get(data.get('social_id'))
            self.add_linegame_friend_elem(data, linegame_data)
            count += 1
            if count > 50:
                break

        if count == 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.nd_content.setVisible(False)

            @self.panel.temp_btn_add_friend.btn_major.callback()
            def OnClick(*args):
                self.on_send_link()

        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.nd_content.setVisible(True)

            @self.panel.temp_btn_other_friend.btn_major.callback()
            def OnClick(*args):
                self.on_send_link()

    def add_linegame_friend_elem(self, data, linegame_data):
        panel = super(LineGameInviteList, self).add_linegame_friend_elem(data, linegame_data)
        friend_online_state = self._message_data.get_player_online_state()
        state = int(friend_online_state.get(int(data['uid']), 0))
        visible = False
        if st_utils.is_not_online(state):
            visible = True
            panel.lab_name.SetColor('#SD')
            set_gray(panel.img_head, True)
        panel.btn_invite.setVisible(visible)
        panel.btn_add.setVisible(not visible)

    def add_linegame_icon(self, elem_panel, file_path, data):
        sprite = super(LineGameInviteList, self).add_linegame_icon(elem_panel, file_path, data)
        friend_online_state = self._message_data.get_player_online_state()
        state = int(friend_online_state.get(int(data['uid']), 0))
        if st_utils.is_not_online(state):
            set_gray(sprite, True)

    def on_touch_item(self, panel, data):
        uid = data['uid']
        battle_tid = global_data.player.get_battle_tid()
        if battle_tid is None:
            battle_tid = DEFAULT_INVITE_TID
        team_info = global_data.player.get_team_info() or {}
        auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
        from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
        global_data.player.invite_frd(uid, battle_tid, auto_flag, TEAM_MODE_FRIEND)
        panel.btn_add.setVisible(False)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_INVITE_VIA_LINEGAME)
        return

    def on_touch_invite(self, panel, data):
        from logic.comsys.message import SendLineMessage
        SendLineMessage.SendLineMessageInvite(None, social_id=data.get('social_id'))
        return

    def on_send_link(self):
        key_word = '%s=%s' % (share_const.DEEP_LINK_JOIN_TEAM, str(global_data.player.uid))
        logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_LINE)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_SHARE_VIA_LINEGAME)
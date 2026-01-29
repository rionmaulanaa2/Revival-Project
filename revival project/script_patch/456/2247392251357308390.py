# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/TwitterInviteList.py
from __future__ import absolute_import
from common.const.property_const import *
import logic.gcommon.const as const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import share_const
import logic.gutils.share_utils
from logic.comsys.message.TwitterFriendList import TwitterFriendList
from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
from logic.gcommon.common_const import friend_const
from logic.gutils import friend_utils

class TwitterInviteList(TwitterFriendList):
    PANEL_CONFIG_NAME = 'lobby/invite_other_friend_list_tw'

    def refresh_friends(self):
        self._list_add.DeleteAllSubItem()
        social_friends = self._message_data.get_social_friends(friend_const.SOCIAL_ID_TYPE_TW)
        twitter_friendinfos = self._message_data.get_twitter_friendinfos()
        count = 0
        for data in social_friends:
            twitter_data = twitter_friendinfos.get(data.get('social_id'), {})
            self.add_twitter_friend_elem(data, twitter_data)
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

    def on_touch_item(self, panel, uid):
        battle_tid = global_data.player.get_battle_tid()
        if battle_tid is None:
            battle_tid = DEFAULT_INVITE_TID
        team_info = global_data.player.get_team_info() or {}
        auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
        from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
        global_data.player.invite_frd(uid, battle_tid, auto_flag, TEAM_MODE_FRIEND)
        panel.btn_add.setVisible(False)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_INVITE_VIA_TWITTER)
        return

    def on_send_link(self):
        key_word = '%s=%s' % (share_const.DEEP_LINK_JOIN_TEAM, str(global_data.player.uid))
        logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_TWITTER)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_SHARE_VIA_TWITTER)
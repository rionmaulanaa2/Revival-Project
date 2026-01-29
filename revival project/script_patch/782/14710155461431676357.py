# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomInviteUINew.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.lobby.LobbyTeamInviteWidget import LobbyTeamInviteWidget
from common.framework import Functor
from logic.comsys.room.RoomRecruitUI import RoomRecruitUI
from common.const.property_const import C_NAME, U_ID, U_LV, ROLE_ID, HEAD_FRAME, HEAD_PHOTO
import logic.gcommon.const as const
from logic.gutils import share_utils
from common.platform.dctool import interface
from logic.client.const import share_const
TAB_UNINIT = -1
TAB_FRIEND = 0
TAB_RECENT_TEAM = 1
TAB_FACE_TO_FACE = 2
TAB_RECOMMEND = 3
BTN_LIN_PIC = 'gui/ui_res_2/share/icon_link.png'

class RoomInviteUINew(LobbyTeamInviteWidget):
    VIS_ACT = 210118

    def __init__(self, parent_ui, panel):
        self._room_ui = parent_ui
        super(RoomInviteUINew, self).__init__(parent_ui, panel)

    def init_animation_name(self):
        self.show_animation_name = 'appear'
        self.hide_animation_name = 'disappear'

    def init_event(self):
        self.nd_invite.BindMethod('OnClick', self.hide)
        for tab_type, btn in six.iteritems(self.tab_btn_dict):
            btn.btn_tab_window.BindMethod('OnClick', Functor(self.on_click_tab, tab_type))

        self.nd_invite.btn_recruit.BindMethod('OnClick', Functor(self.on_click_recruit_btn))
        self.nd_invite.btn_search.BindMethod('OnClick', Functor(self.on_click_search))
        self.nd_invite.btn_clear.BindMethod('OnClick', Functor(self.on_click_clear_input))
        support_platform = share_utils.get_join_customroom_url_support_platform_enum()
        is_share_enable = share_utils.is_share_enable()
        self._show_share_for_mainland = interface.is_mainland_package() and is_share_enable and bool(support_platform)
        self.nd_invite.btn_invite_others.setVisible(False)
        self.nd_invite.nd_share.setVisible(False)
        self.nd_invite.list_others.setVisible(False)
        self.nd_invite.bar_list_others.setVisible(False)
        self.nd_invite.nd_invite_others_cn.setVisible(False)
        if is_share_enable and support_platform and interface.is_mainland_package():
            self.nd_invite.nd_invite_others_cn.setVisible(True)
            self.nd_invite.list_platform.SetInitCount(len(support_platform) + 1)
            platform_info_list = global_data.share_mgr.get_support_platforms_from_enum(support_platform)
            for idx in range(len(support_platform) + 1):
                if idx == len(support_platform):
                    btn_share = self.nd_invite.list_platform.GetItem(idx)
                    btn_share.SetFrames('', [BTN_LIN_PIC, BTN_LIN_PIC, ''])

                    @btn_share.callback()
                    def OnClick(*args):
                        self.on_click_copy_url()

                    continue
                btn_share = self.nd_invite.list_platform.GetItem(idx)
                platform_info = platform_info_list[idx]
                share_pic = platform_info.get('pic', '')
                btn_share.SetFrames('', [share_pic, share_pic, ''])
                share_type = support_platform[idx]

                @btn_share.callback()
                def OnClick(btn, touch, _share_type=share_type):
                    self.on_click_platform_share(_share_type)

        self.on_room_battle_type_changed()

    def refresh_friend_item(self, panel, data):
        super(RoomInviteUINew, self).refresh_friend_item(panel, data)
        friend_id = data[U_ID]
        online_state = self.set_online_state(panel, friend_id)
        if online_state == const.STATE_SINGLE:
            panel.btn_invite.setVisible(True)
        else:
            panel.btn_invite.setVisible(False)
        panel.btn_team.setVisible(False)
        panel.btn_invite.BindMethod('OnClick', Functor(self.on_click_list_invite, friend_id))

    def init_nd_empty_recent_team(self, nd_empty):
        nd_empty.lab_empty.setVisible(False)
        nd_empty.btn_empty.setVisible(False)

    def on_click_recruit_btn(self, *args):
        RoomRecruitUI()

    def on_click_list_invite(self, uid, btn, *args):
        global_data.player.invite_friend_into_room(uid)

    def update_match_status(self, is_matching):
        pass

    def on_click_auto_match(self, *args):
        pass

    def on_click_add_friend(self, *args):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

    def on_click_join_clan(self, *args):
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        lobby_ui and lobby_ui.on_click_clan_btn()

    def on_click_tab(self, tab_type, *args):
        super(RoomInviteUINew, self).on_click_tab(tab_type, *args)
        if tab_type in [TAB_FRIEND, TAB_RECENT_TEAM]:
            self.nd_invite.btn_recruit.setVisible(True)
        else:
            self.nd_invite.btn_recruit.setVisible(False)

    def on_click_platform_share(self, share_type):
        share_url, s_title, s_message = share_utils.get_mainland_invite_customroom_url()
        share_args = global_data.share_mgr.get_share_app_share_args(share_type)
        share_inform_cb = lambda *args: True
        global_data.share_mgr.share(share_args, share_const.TYPE_LINK, '', link=share_url, title=s_title, message=s_message, share_inform_cb=share_inform_cb)

    def on_click_copy_url(self):
        import game3d
        share_url, s_title, s_message = share_utils.get_mainland_invite_customroom_url()
        game3d.set_clipboard_text(share_url)
        global_data.game_mgr.show_tip(get_text_by_id(610379))

    def on_room_battle_type_changed(self):
        show_btn_recruit = self._room_ui and not self._room_ui.is_competition_room()
        self.nd_invite.btn_recruit.setVisible(show_btn_recruit)

    def refresh_players(self):
        super(RoomInviteUINew, self).refresh_players()
        if self.nd_invite and self.nd_invite.btn_invite_others:
            self.nd_invite.btn_invite_others.setVisible(False)
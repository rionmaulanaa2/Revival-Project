# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyTeamInviteWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from functools import cmp_to_key
import game3d
from common.framework import Functor
from common.uisys.BaseUIWidget import BaseUIWidget
from common.const.property_const import C_NAME, U_ID, U_LV, ROLE_ID, HEAD_FRAME, HEAD_PHOTO
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as const
import time
import cc
from logic.gcommon.common_const.battle_const import DEFAULT_BATTLE_TID
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray
from logic.gutils import role_head_utils
from logic.gcommon.common_const import chat_const
from logic.client.const import share_const
from common.platform.dctool import interface
from common.platform import channel_const
from common.cfg import confmgr
import logic.gutils.share_utils
from logic.gutils import friend_utils
from logic.gcommon.common_const import log_const
from logic.gutils import share_utils
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from logic.gutils.online_state_utils import is_not_online, get_friend_online_count
from logic.gcommon.common_utils.local_text import get_mode_text_by_id
import six
TAB_UNINIT = -1
TAB_FRIEND = 0
TAB_RECENT_TEAM = 1
TAB_FACE_TO_FACE = 2
TAB_RECOMMEND = 3
TAB_CLAN = 4
TAB_NEAR = 5
BTN_LIN_PIC = 'gui/ui_res_2/share/icon_link.png'
TEAM_INVITE_SORT_RULE = {const.STATE_INVISIBLE: 0,
   const.STATE_OFFLINE: 0,
   const.STATE_BATTLE: 1,
   const.STATE_BATTLE_FIGHT: 2,
   const.STATE_EXERCISE: 3,
   const.STATE_SPECTATING: 4,
   const.STATE_TEAM: 5,
   const.STATE_ROOM: 6,
   const.STATE_SINGLE: 10
   }
TAB_2_LOG_MODE = {TAB_FRIEND: log_const.TEAM_MODE_FRIEND,
   TAB_RECENT_TEAM: log_const.TEAM_MODE_RECENT,
   TAB_RECOMMEND: log_const.TEAM_MODE_RECOMMEND,
   TAB_FACE_TO_FACE: log_const.TEAM_MODE_RECENT,
   TAB_CLAN: log_const.TEAM_MODE_CLAN,
   TAB_NEAR: log_const.TEAM_MODE_NEAR
   }

class LobbyTeamInviteWidget(BaseUIWidget):
    VIS_ACT = 180720

    def __init__(self, parent_ui, panel):
        self.cur_appoint_uid = None
        self.panel = panel
        self.nd_invite = panel.nd_team_invite
        self.nd_temp_content = panel.nd_team_invite.temp_content
        self.init_animation_name()
        self.select_tab = TAB_UNINIT
        self.global_events = {'battle_match_status_event': self.update_match_status,
           'message_refresh_friends': self.refresh_players,
           'message_friend_state': self.refresh_players,
           'message_on_get_neighbor_player': self.show_neighbor_players,
           'message_on_players_detail_inf': self.show_clan_players,
           'clan_member_data': self.show_clan_players,
           'team_invite_count_down_event': self.update_invite_count_down,
           'refresh_recommend_teammates': self.refresh_recommend_teammates
           }
        self.cur_tab_type = None
        self.tab_btn_dict = {TAB_FRIEND: self.nd_invite.btn_tab_friend,
           TAB_RECENT_TEAM: self.nd_invite.btn_tab_recently,
           TAB_FACE_TO_FACE: self.nd_invite.btn_tab_face2face,
           TAB_CLAN: self.nd_invite.btn_tab_crew,
           TAB_NEAR: self.nd_invite.btn_tab_near
           }
        self.tab_btn_dict[TAB_NEAR] and self.tab_btn_dict[TAB_NEAR].setVisible(not G_IS_NA_PROJECT and game3d.get_platform() != game3d.PLATFORM_WIN32)
        self.tab_template_dict = {TAB_FRIEND: 'lobby/i_invite_list',
           TAB_RECENT_TEAM: 'lobby/i_invite_list',
           TAB_FACE_TO_FACE: 'lobby/i_invite_list',
           TAB_RECOMMEND: 'lobby/i_invite_recommend_list',
           TAB_UNINIT: 'lobby/i_invite_search_result',
           TAB_CLAN: 'lobby/i_invite_list',
           TAB_NEAR: 'lobby/i_invite_list'
           }
        self.uid_to_btn_dict = dict()
        self.player_info_manager = PlayerInfoManager()
        self.search_time = 0
        self.content_data = []
        self._is_check_sview = False
        self._sview_index = 0
        self._sview_height = self.nd_temp_content.friend_content.lv_list.getContentSize().height
        self._sview_content_height = 0
        self._is_show_platform = False
        self.platform_item_temp = global_data.uisystem.load_template('lobby/i_match_invite_others')
        super(LobbyTeamInviteWidget, self).__init__(parent_ui, panel)
        self.init_widget()
        self.hide()
        return

    def init_animation_name(self):
        self.show_animation_name = 'show'
        self.hide_animation_name = 'hide'

    def destroy(self):
        if self._input_friend:
            self._input_friend.destroy()
            self._input_friend = None
        if self.request_online_state_enable:
            global_data.message_data.destroy_request_online_state_timer()
            self.request_online_state_enable = False
        global_data.emgr.message_refresh_friend_search -= self.on_search_friends
        global_data.emgr.message_on_get_neighbor_player -= self.show_neighbor_players
        super(LobbyTeamInviteWidget, self).destroy()
        return

    def update_match_status(self, is_matching):
        if is_matching:
            self.hide()

    def on_click_tab(self, tab_type, *args):
        content = getattr(self.nd_temp_content, 'friend_content')
        pos = content.GetPosition()
        archor = content.getAnchorPoint()
        parent = content.GetParent()
        parent.DestroyChild('friend_content')
        new_conent = global_data.uisystem.load_template_create(self.tab_template_dict[tab_type], parent=parent, name='friend_content')
        new_conent.ResizeAndPosition()
        new_conent.SetPosition(*pos)
        new_conent.setAnchorPoint(archor)
        self.clear_content_list()
        self.add_list_view_check()
        if self.cur_tab_type is not None:
            tab_btn = self.tab_btn_dict.get(self.cur_tab_type, None)
            if tab_btn:
                tab_btn.btn_tab_window.SetSelect(False)
        self.cur_tab_type = tab_type
        new_tab_btn = self.tab_btn_dict.get(tab_type, None)
        if tab_type == TAB_RECENT_TEAM:
            self.init_nd_empty_recent_team(new_conent.nd_empty)
        elif tab_type == TAB_FRIEND:
            new_conent.btn_empty.BindMethod('OnClick', Functor(self.on_click_add_friend))
        elif tab_type == TAB_CLAN:
            self.init_nd_empty_clan(new_conent.nd_empty)
        elif tab_type == TAB_NEAR:
            self.init_nd_empty_near(new_conent.nd_empty)
        if new_tab_btn:
            new_tab_btn.btn_tab_window.SetSelect(True)
            self.refresh_players()
        tab_btn = self.tab_btn_dict.get(tab_type, None)
        if tab_btn:
            tab_btn.btn_tab_window.SetSelect(True)
        return

    def init_nd_empty_recent_team(self, nd_empty):
        nd_empty.btn_empty.BindMethod('OnClick', Functor(self.on_click_auto_match))
        nd_empty.lab_empty.SetString(get_text_by_id(80092))
        nd_empty.btn_empty.SetText(get_text_by_id(80516))
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        nd_empty.btn_empty.setVisible(not bool(ui))

    def init_nd_empty_clan(self, nd_empty):
        nd_empty.btn_empty.BindMethod('OnClick', Functor(self.on_click_join_clan))
        nd_empty.lab_empty.SetString(get_text_by_id(10329))
        nd_empty.btn_empty.SetText(get_text_by_id(800020))

    def init_nd_empty_near(self, nd_empty):
        nd_empty.btn_empty.setVisible(False)
        nd_empty.lab_empty.SetString(get_text_by_id(15079))

    def add_list_view_check(self):

        def scroll_callback(sender, eventType):
            if not self._is_check_sview:
                self._is_check_sview = True
                self.nd_invite.SetTimeOut(0.021, self.check_sview)

        self.nd_temp_content.friend_content.lv_list.addEventListener(scroll_callback)

    def on_click_share(self, *args):
        nd = self.nd_invite
        nd.btn_share.setVisible(False)
        self.nd_invite.PlayAnimation('show_share')

    def on_click_cancel_share(self, *args):
        nd = self.nd_invite
        nd.btn_share.setVisible(False)
        self.nd_invite.PlayAnimation('disappear_share')

    def on_click_search(self, *args):
        valid, frd_uid, frd_name = self.check_search_type()
        if not valid:
            return
        else:
            if not G_IS_NA_USER:
                if frd_uid != 0:
                    frd_uid += global_data.uid_prefix
            nd_empty = self.nd_temp_content.friend_content.nd_empty
            nd_empty and nd_empty.setVisible(False)
            self.clear_content_list()
            self.add_list_view_check()
            self.cur_tab_type = None
            friends = global_data.message_data.get_friends()
            search_friend_result = self.get_search_result(friends, frd_uid, frd_name)
            title_str = get_text_by_id(13012)
            online_num = get_friend_online_count(search_friend_result)
            num_str = '%d/%d' % (online_num, len(search_friend_result))
            title = {'title': title_str,'num': num_str}
            self.content_data.append(title)
            search_friend_result = self.sort_friend_list(search_friend_result)
            self.content_data.extend(search_friend_result)
            teams = global_data.message_data.get_team_friends()
            search_team_result = self.get_search_result(teams, frd_uid, frd_name)
            title_str = get_text_by_id(13013)
            online_num = get_friend_online_count(search_team_result)
            num_str = '%d/%d' % (online_num, len(search_team_result))
            title = {'title': title_str,'num': num_str}
            self.content_data.append(title)
            search_team_result = self.sort_friend_list(search_team_result, True)
            self.content_data.extend(search_team_result)
            if not search_friend_result and not search_team_result:
                if not global_data.player.search_friend(frd_uid, frd_name):
                    global_data.game_mgr.show_tip(get_text_by_id(10044))
                global_data.emgr.message_refresh_friend_search += self.on_search_friends
            else:
                self.refresh_friend_content(self.content_data)
            return

    def get_search_result(self, friend_data, frd_uid, frd_name):
        search_friend_result = []
        for friend in six.itervalues(friend_data):
            if frd_name:
                char_name = friend.get('char_name', '')
                if char_name.find(frd_name) != -1:
                    search_friend_result.append(friend)
            elif frd_uid:
                uid = friend.get(U_ID, '')
                if uid == frd_uid:
                    search_friend_result.append(friend)

        return search_friend_result

    def on_search_friends(self, *args):
        ui_list = self.nd_temp_content.friend_content.lv_list
        search_friends = global_data.message_data.get_search_friends()
        title_str = get_text_by_id(13014)
        online_num = get_friend_online_count(search_friends)
        num_str = '%d/%d' % (online_num, len(search_friends))
        title = {'title': title_str,'num': num_str}
        self.content_data.append(title)
        search_friends = self.sort_friend_list(search_friends)
        self.content_data.extend(search_friends)
        self.refresh_friend_content(self.content_data)
        global_data.emgr.message_refresh_friend_search -= self.on_search_friends

    def check_search_type(self):
        text = self._input_friend.get_text()
        if not text:
            return (False, None, None)
        else:
            now = time.time()
            interval = now - self.search_time
            if interval < const.SEARCH_FRIEND_MIN_TIME:
                notify_text = get_text_by_id(10039, {'time': int(const.SEARCH_FRIEND_MIN_TIME - interval) + 1})
                global_data.player.notify_client_message((notify_text,))
                return (
                 False, None, None)
            self.search_time = now
            self._input_friend.set_text('')
            if self.check_is_int(text):
                frd_uid = int(text)
                frd_name = ''
                return (
                 True, frd_uid, frd_name)
            frd_uid = 0
            frd_name = str(text)
            return (
             True, frd_uid, frd_name)
            return None

    def check_is_int(self, text):
        try:
            int(text)
            return True
        except:
            return False

    def update_teammate_panel(self, *args):
        pass

    def init_teammate_panel(self, *args):
        pass

    def init_event(self):
        super(LobbyTeamInviteWidget, self).init_event()
        self.nd_invite.BindMethod('OnClick', self.hide)
        tab_iteritems = six.iteritems(self.tab_btn_dict)
        for tab_type, btn in tab_iteritems:
            btn.btn_tab_window.BindMethod('OnClick', Functor(self.on_click_tab, tab_type))

        self.nd_invite.btn_share.BindMethod('OnClick', Functor(self.on_click_share))
        self.nd_invite.btn_share_cancel.BindMethod('OnClick', Functor(self.on_click_cancel_share))
        self.nd_invite.btn_search.BindMethod('OnClick', Functor(self.on_click_search))
        self.nd_invite.btn_clear.BindMethod('OnClick', Functor(self.on_click_clear_input))
        support_platform = share_utils.get_team_up_url_support_platform_enum()
        is_share_enable = share_utils.is_share_enable()
        self._show_share_for_mainland = interface.is_mainland_package() and is_share_enable and bool(support_platform)
        if self.is_show_invite_others():
            self.nd_invite.nd_invite_others_cn.setVisible(False)
            self.nd_invite.btn_invite_others.setVisible(True)
            self.nd_invite.btn_invite_others.BindMethod('OnClick', Functor(self.on_show_plafrom))
            self.nd_invite.nd_share_instruction.setVisible(False)
        else:
            self.nd_invite.btn_invite_others.setVisible(False)
            self.nd_invite.nd_invite_others_cn.setVisible(True)
            if global_data.channel and global_data.channel.get_name() in ('bilibili_sdk',
                                                                          'huawei'):
                self.nd_invite.nd_share_instruction.setVisible(False)
                self.nd_invite.nd_invite_others_cn.setVisible(False)
                return
        if share_utils.is_share_enable():
            support_platform = share_utils.get_team_up_url_support_platform_enum()
            if support_platform:
                self.nd_invite.nd_invite_others_cn.setVisible(True)
                self.nd_invite.list_platform.SetInitCount(len(support_platform) + 1)
                import sys
                platform_info_list = global_data.share_mgr.get_support_platforms_from_enum(support_platform)
                for index in range(len(support_platform) + 1):
                    if index == len(support_platform):
                        btn_share = self.nd_invite.list_platform.GetItem(index)
                        btn_share.SetFrames('', [BTN_LIN_PIC, BTN_LIN_PIC, ''])

                        @btn_share.callback()
                        def OnClick(*args):
                            self.on_click_copy_url()

                        continue
                    btn_share = self.nd_invite.list_platform.GetItem(index)
                    platform_info = platform_info_list[index]
                    share_pic = platform_info.get('pic', '')
                    btn_share.SetFrames('', [share_pic, share_pic, ''])

                    @btn_share.callback()
                    def OnClick(btn, touch, index=index):
                        share_url, s_title, s_message = share_utils.get_mainland_invite_team_url()
                        share_args = global_data.share_mgr.get_share_app_share_args(support_platform[index])
                        share_inform_cb = lambda *args: True
                        global_data.share_mgr.share(share_args, share_const.TYPE_LINK, '', link=share_url, title=s_title, message=s_message, share_inform_cb=share_inform_cb)

    def is_show_invite_others(self):
        return not (interface.get_game_id() == 'g93' or not logic.gutils.share_utils.is_share_enable())

    def init_widget(self):
        self.request_online_state_enable = False
        self.player_item_template = global_data.uisystem.load_template('lobby/match_friend_item')
        self.title_template = global_data.uisystem.load_template('lobby/i_invite_list_title')
        self.on_click_tab(TAB_FRIEND)
        self.init_friend_panel()
        self.init_share_panel()
        self.init_search_panel()
        self.init_search_result_panel()
        self.init_nd_appoint()

    def init_share_panel(self):
        from logic.gutils.share_utils import init_platform_list

        def share_callback(pf, circle):
            self.parent.show_developing_message()

        init_platform_list(self.nd_invite.pnl_share_list, share_callback)

    def init_search_panel(self):

        def on_input_cd(text):
            if text:
                self.nd_invite.btn_clear.setVisible(True)
            else:
                self.nd_invite.btn_clear.setVisible(False)
            if self.cur_tab_type != TAB_UNINIT:
                self.on_click_tab(TAB_UNINIT)

        if global_data.is_pc_mode:
            send_callback = self.on_click_search
        else:
            send_callback = None
        self._input_friend = InputBox.InputBox(self.nd_invite.lab_search, input_callback=on_input_cd, placeholder=get_text_by_id(80347), send_callback=send_callback)
        self._input_friend.set_rise_widget(self.panel)
        return

    def init_search_result_panel(self):
        pass

    def init_nd_appoint(self):
        self.nd_invite.temp_input.layerout.input_box.setEnabled(False)
        list_reply = self.nd_invite.list_reply

        @self.nd_invite.btn_reply.callback()
        def OnClick(*args):
            list_reply.setVisible(not list_reply.isVisible())

        @self.nd_invite.btn_block.callback()
        def OnClick(*args):
            list_reply.setVisible(False)

        def click_replay_text(text_id, *args):
            self.nd_invite.temp_input.layerout.input_box.SetText(get_text_by_id(text_id))
            list_reply.setVisible(False)

        reply_text_list = confmgr.get('appoint_quick_chat', 'content', default=[])
        if reply_text_list:
            self.nd_invite.temp_input.layerout.input_box.SetText(get_text_by_id(reply_text_list[0]))
        list_reply.nd_close.SetEnableTouch(False)
        option_list = list_reply.option_list
        option_list.SetInitCount(len(reply_text_list))
        for idx, text_id in enumerate(reply_text_list):
            item = option_list.GetItem(idx)
            item.button.SetText(get_text_by_id(text_id))
            item.button.BindMethod('OnClick', Functor(click_replay_text, text_id))

        self.nd_invite.temp_input.touch_layer.SetEnableTouch(False)
        self.nd_invite.nd_appoint.bg.lab_time.setVisible(False)
        self.nd_invite.nd_appoint.bg.lab_mode.setVisible(False)

        @self.nd_invite.btn_click.btn_common.callback()
        def OnClick(*args):
            if list_reply.isVisible():
                return
            if self.cur_appoint_uid:
                msg = self.nd_invite.temp_input.layerout.input_box.getString()
                global_data.player.reserve_friend(self.cur_appoint_uid, msg)
            self.nd_invite.nd_appoint.setVisible(False)

    def on_click_clear_input(self, *args):
        self._input_friend.set_text('')
        self.nd_invite.btn_clear.setVisible(False)

    def on_click_add_friend(self, *args):
        self.parent.on_main_friend_ui()

    def on_show_plafrom(self, *args):
        self._is_show_platform = not self._is_show_platform
        self.nd_invite.list_others.setVisible(self._is_show_platform)
        self.nd_invite.bar_list_others.setVisible(self._is_show_platform)
        if self._is_show_platform:
            self.nd_invite.list_others.DeleteAllSubItem()
            panel = self.nd_invite.list_others.AddItem(self.platform_item_temp, bRefresh=True)
            panel.icon.SetDisplayFrameByPath('', chat_const.FACEBOOK_ICON)
            bind_types = global_data.channel.get_bind_types()
            is_bind_facebook = True if str(channel_const.AUTH_TYPE_FACEBOOK) in bind_types else False
            panel.icon_tick.setVisible(is_bind_facebook)
            if is_bind_facebook:
                panel.lab.setString(get_text_by_id(10291))
            else:
                panel.lab.setString(get_text_by_id(10287))

            @panel.btn_item.callback()
            def OnClick(*args):
                bind_types = global_data.channel.get_bind_types()
                is_bind_facebook = True if str(channel_const.AUTH_TYPE_FACEBOOK) in bind_types else False
                if is_bind_facebook:
                    global_data.ui_mgr.show_ui('FaceBookInviteList', 'logic.comsys.message')
                else:
                    global_data.channel.set_prop_str('BIND_TYPE', '1')
                    global_data.channel.set_prop_str('AUTH_CHANNEL', 'facebook')
                    global_data.channel.guest_bind()
                    self._is_show_platform = False
                    self.nd_invite.list_others.setVisible(self._is_show_platform)
                    self.nd_invite.bar_list_others.setVisible(self._is_show_platform)
                    friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_INVITE_BIND_FACEBOOK)

            panel = self.nd_invite.list_others.AddItem(self.platform_item_temp, bRefresh=True)
            panel.icon.SetDisplayFrameByPath('', chat_const.TWITTER_ICON)
            is_bind_twitter = True if str(channel_const.AUTH_TYPE_TWITTER) in bind_types else False
            panel.icon_tick.setVisible(is_bind_twitter)
            if is_bind_twitter:
                panel.lab.setString(get_text_by_id(10292))
            else:
                panel.lab.setString(get_text_by_id(10288))

            @panel.btn_item.callback()
            def OnClick(*args):
                bind_types = global_data.channel.get_bind_types()
                is_bind_twitter = True if str(channel_const.AUTH_TYPE_TWITTER) in bind_types else False
                if is_bind_twitter:
                    global_data.ui_mgr.show_ui('TwitterInviteList', 'logic.comsys.message')
                else:
                    global_data.channel.set_prop_str('BIND_TYPE', '1')
                    global_data.channel.set_prop_str('AUTH_CHANNEL', 'twitter')
                    global_data.channel.guest_bind()
                    self._is_show_platform = False
                    self.nd_invite.list_others.setVisible(self._is_show_platform)
                    self.nd_invite.bar_list_others.setVisible(self._is_show_platform)
                    friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_INVITE_BIND_TWITTER)

            panel = self.nd_invite.list_others.AddItem(self.platform_item_temp, bRefresh=True)
            panel.icon.SetDisplayFrameByPath('', chat_const.MESSENGER_ICON)
            panel.icon_tick.setVisible(True)
            panel.lab.setString(get_text_by_id(81260))

            @panel.btn_item.callback()
            def OnClick(*args):
                key_word = '%s=%s' % (share_const.DEEP_LINK_JOIN_TEAM, str(global_data.player.uid))
                logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_MESSENGER)
                friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_SHARE_VIA_MESSENGER)

            if global_data.feature_mgr.is_linegame_ready():
                panel = self.nd_invite.list_others.AddItem(self.platform_item_temp, bRefresh=True)
                panel.icon.SetDisplayFrameByPath('', chat_const.LINE_ICON)
                bind_types = global_data.channel.get_bind_types()
                is_bind_linegame = True if str(channel_const.AUTH_TYPE_LINEGAME) in bind_types else False
                panel.icon_tick.setVisible(is_bind_linegame)
                if is_bind_linegame:
                    panel.lab.setString(get_text_by_id(609013))
                else:
                    panel.lab.setString(get_text_by_id(609014))

                @panel.btn_item.callback()
                def OnClick(*args):
                    from logic.comsys.message import HintLineUI
                    bind_types = global_data.channel.get_bind_types()
                    is_bind_linegame = True if str(channel_const.AUTH_TYPE_LINEGAME) in bind_types else False
                    if is_bind_linegame:
                        HintLineUI.check_hint_line(lambda : global_data.ui_mgr.show_ui('LineGameInviteList', 'logic.comsys.message'))
                    else:
                        global_data.channel.set_prop_str('BIND_TYPE', '1')
                        global_data.channel.set_prop_str('AUTH_CHANNEL', 'linegame')
                        global_data.channel.guest_bind()
                        self._is_show_platform = False
                        self.nd_invite.list_others.setVisible(self._is_show_platform)
                        self.nd_invite.bar_list_others.setVisible(self._is_show_platform)
                        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_INVITE_BIND_LINEGAME)

            W, H = self.nd_invite.list_others.GetContentSize()
            self.nd_invite.bar_list_others.SetContentSize(W + 12, H)

    def show(self, *args):
        if not self.request_online_state_enable:
            global_data.message_data.create_request_online_state_timer()
            self.request_online_state_enable = True
        self.nd_vis = True
        self.nd_invite.setVisible(True)
        self.nd_invite.PlayAnimation(self.show_animation_name)
        self.hide_chat_ui_btn(True)
        self.query_player_role_head_info()
        self.refresh_players()
        count_down_data = global_data.player.get_count_down()
        self.update_invite_count_down(count_down_data)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(self.__class__.__name__, '')
        self.on_click_change_recommend()

    def query_player_role_head_info(self):
        global_data.message_data.request_role_head_info(['friend', 'recent_team'])

    def hide(self, *args):
        if self.request_online_state_enable:
            global_data.message_data.destroy_request_online_state_timer()
            self.request_online_state_enable = False
        self.nd_vis = False
        self.nd_invite.PlayAnimation(self.hide_animation_name)
        dis_time = self.nd_invite.GetAnimationMaxRunTime(self.hide_animation_name)
        self.hide_chat_ui_btn(False)

        def disappear_callback():
            self.nd_invite.setVisible(False)

        self.nd_invite.SetTimeOut(dis_time, disappear_callback, self.VIS_ACT)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(self.__class__.__name__, '')
        self.nd_invite.nd_appoint.setVisible(False)

    def hide_chat_ui_btn(self, is_hide):
        chat_ui = global_data.ui_mgr.get_ui('MainChat')
        if chat_ui:
            if is_hide:
                chat_ui.add_hide_count(self.__class__.__name__)
            else:
                chat_ui.add_show_count(self.__class__.__name__)

    def init_friend_panel(self):
        pass

    def sort_friend_list(self, friend_list, cmp_team=False):
        friend_online_state = global_data.message_data.get_player_online_state()

        def cmp_func--- This code section failed: ---

 681       0  LOAD_GLOBAL           0  'int'
           3  LOAD_GLOBAL           1  'get'
           6  BINARY_SUBSCR    
           7  CALL_FUNCTION_1       1 
          10  STORE_FAST            2  'a_uid'

 682      13  LOAD_GLOBAL           0  'int'
          16  LOAD_FAST             1  'b'
          19  LOAD_CONST            1  'uid'
          22  BINARY_SUBSCR    
          23  CALL_FUNCTION_1       1 
          26  STORE_FAST            3  'b_uid'

 683      29  LOAD_GLOBAL           0  'int'
          32  LOAD_DEREF            0  'friend_online_state'
          35  LOAD_ATTR             1  'get'
          38  LOAD_FAST             2  'a_uid'
          41  LOAD_CONST            2  ''
          44  CALL_FUNCTION_2       2 
          47  CALL_FUNCTION_1       1 
          50  STORE_FAST            4  'a_state'

 684      53  LOAD_GLOBAL           0  'int'
          56  LOAD_DEREF            0  'friend_online_state'
          59  LOAD_ATTR             1  'get'
          62  LOAD_FAST             3  'b_uid'
          65  LOAD_CONST            2  ''
          68  CALL_FUNCTION_2       2 
          71  CALL_FUNCTION_1       1 
          74  STORE_FAST            5  'b_state'

 686      77  LOAD_GLOBAL           2  'is_not_online'
          80  LOAD_FAST             4  'a_state'
          83  CALL_FUNCTION_1       1 
          86  UNARY_NOT        
          87  STORE_FAST            6  'a_online'

 687      90  LOAD_GLOBAL           2  'is_not_online'
          93  LOAD_FAST             5  'b_state'
          96  CALL_FUNCTION_1       1 
          99  UNARY_NOT        
         100  STORE_FAST            7  'b_online'

 688     103  LOAD_FAST             6  'a_online'
         106  LOAD_FAST             7  'b_online'
         109  COMPARE_OP            3  '!='
         112  POP_JUMP_IF_FALSE   131  'to 131'

 689     115  LOAD_GLOBAL           3  'six_ex'
         118  LOAD_ATTR             4  'compare'
         121  LOAD_FAST             6  'a_online'
         124  LOAD_FAST             7  'b_online'
         127  CALL_FUNCTION_2       2 
         130  RETURN_END_IF    
       131_0  COME_FROM                '112'

 691     131  LOAD_GLOBAL           5  'global_data'
         134  LOAD_ATTR             6  'player'
         137  POP_JUMP_IF_FALSE   152  'to 152'
         140  LOAD_GLOBAL           5  'global_data'
         143  LOAD_ATTR             6  'player'
         146  LOAD_ATTR             7  '_top_frds'
         149  JUMP_FORWARD          3  'to 155'
         152  BUILD_LIST_0          0 
       155_0  COME_FROM                '149'
         155  STORE_FAST            8  'top_frds'

 692     158  LOAD_FAST             2  'a_uid'
         161  LOAD_FAST             8  'top_frds'
         164  COMPARE_OP            6  'in'
         167  POP_JUMP_IF_FALSE   185  'to 185'
         170  LOAD_FAST             8  'top_frds'
         173  LOAD_ATTR             8  'index'
         176  LOAD_FAST             2  'a_uid'
         179  CALL_FUNCTION_1       1 
         182  JUMP_FORWARD          3  'to 188'
         185  LOAD_CONST            3  -1
       188_0  COME_FROM                '182'
         188  STORE_FAST            9  'a_top'

 693     191  LOAD_FAST             3  'b_uid'
         194  LOAD_FAST             8  'top_frds'
         197  COMPARE_OP            6  'in'
         200  POP_JUMP_IF_FALSE   218  'to 218'
         203  LOAD_FAST             8  'top_frds'
         206  LOAD_ATTR             8  'index'
         209  LOAD_FAST             3  'b_uid'
         212  CALL_FUNCTION_1       1 
         215  JUMP_FORWARD          3  'to 221'
         218  LOAD_CONST            3  -1
       221_0  COME_FROM                '215'
         221  STORE_FAST           10  'b_top'

 694     224  LOAD_FAST             9  'a_top'
         227  LOAD_FAST            10  'b_top'
         230  COMPARE_OP            3  '!='
         233  POP_JUMP_IF_FALSE   252  'to 252'

 695     236  LOAD_GLOBAL           3  'six_ex'
         239  LOAD_ATTR             4  'compare'
         242  LOAD_FAST             9  'a_top'
         245  LOAD_FAST            10  'b_top'
         248  CALL_FUNCTION_2       2 
         251  RETURN_END_IF    
       252_0  COME_FROM                '233'

 697     252  LOAD_FAST             4  'a_state'
         255  LOAD_FAST             5  'b_state'
         258  COMPARE_OP            3  '!='
         261  POP_JUMP_IF_FALSE   288  'to 288'

 698     264  LOAD_GLOBAL           3  'six_ex'
         267  LOAD_ATTR             4  'compare'
         270  LOAD_GLOBAL           9  'TEAM_INVITE_SORT_RULE'
         273  LOAD_FAST             4  'a_state'
         276  BINARY_SUBSCR    
         277  LOAD_GLOBAL           9  'TEAM_INVITE_SORT_RULE'
         280  LOAD_FAST             5  'b_state'
         283  BINARY_SUBSCR    
         284  CALL_FUNCTION_2       2 
         287  RETURN_END_IF    
       288_0  COME_FROM                '261'

 700     288  LOAD_DEREF            1  'cmp_team'
         291  POP_JUMP_IF_FALSE   427  'to 427'

 701     294  LOAD_FAST             0  'a'
         297  LOAD_ATTR             1  'get'
         300  LOAD_CONST            4  'cnt'
         303  LOAD_CONST            2  ''
         306  CALL_FUNCTION_2       2 
         309  LOAD_FAST             1  'b'
         312  LOAD_ATTR             1  'get'
         315  LOAD_CONST            4  'cnt'
         318  LOAD_CONST            2  ''
         321  CALL_FUNCTION_2       2 
         324  ROT_TWO          
         325  STORE_FAST           11  'a_cnt'
         328  STORE_FAST           12  'b_cnt'

 702     331  LOAD_FAST             0  'a'
         334  LOAD_ATTR             1  'get'
         337  LOAD_CONST            5  'tm'
         340  LOAD_CONST            2  ''
         343  CALL_FUNCTION_2       2 
         346  LOAD_FAST             1  'b'
         349  LOAD_ATTR             1  'get'
         352  LOAD_CONST            5  'tm'
         355  LOAD_CONST            2  ''
         358  CALL_FUNCTION_2       2 
         361  ROT_TWO          
         362  STORE_FAST           13  'a_tm'
         365  STORE_FAST           14  'b_tm'

 703     368  LOAD_FAST            11  'a_cnt'
         371  LOAD_FAST            12  'b_cnt'
         374  COMPARE_OP            3  '!='
         377  POP_JUMP_IF_FALSE   396  'to 396'

 704     380  LOAD_GLOBAL           3  'six_ex'
         383  LOAD_ATTR             4  'compare'
         386  LOAD_FAST            11  'a_cnt'
         389  LOAD_FAST            12  'b_cnt'
         392  CALL_FUNCTION_2       2 
         395  RETURN_END_IF    
       396_0  COME_FROM                '377'

 705     396  LOAD_FAST            13  'a_tm'
         399  LOAD_FAST            14  'b_tm'
         402  COMPARE_OP            3  '!='
         405  POP_JUMP_IF_FALSE   448  'to 448'

 706     408  LOAD_GLOBAL           3  'six_ex'
         411  LOAD_ATTR             4  'compare'
         414  LOAD_FAST            13  'a_tm'
         417  LOAD_FAST            14  'b_tm'
         420  CALL_FUNCTION_2       2 
         423  RETURN_END_IF    
       424_0  COME_FROM                '405'
         424  JUMP_FORWARD         21  'to 448'

 708     427  LOAD_GLOBAL           3  'six_ex'
         430  LOAD_ATTR             4  'compare'
         433  LOAD_ATTR             1  'get'
         436  BINARY_SUBSCR    
         437  LOAD_FAST             1  'b'
         440  LOAD_CONST            1  'uid'
         443  BINARY_SUBSCR    
         444  CALL_FUNCTION_2       2 
         447  RETURN_VALUE     
       448_0  COME_FROM                '424'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 7

        return sorted(friend_list, key=cmp_to_key(cmp_func), reverse=True)

    def refresh_friend_content(self, friend_list):
        index = 0
        self.uid_to_btn_dict = dict()
        while self._sview_content_height < self._sview_height and index < len(friend_list):
            data = friend_list[index]
            panel = self.add_player_item(data)
            self._sview_content_height += panel.getContentSize().height
            index += 1

        if self._sview_index == 0:
            self._sview_index = index - 1
        else:
            self._sview_index += index

    def refresh_friend_content_data(self, friend_list, item_count):
        lv_list = self.nd_temp_content.friend_content.lv_list
        data_index = self._sview_index - item_count
        for panel in lv_list.GetAllItem():
            data_index += 1
            data = friend_list[data_index]
            self.refresh_friend_item(panel, data)

        count_down_data = global_data.player.get_count_down()
        self.update_invite_count_down(count_down_data)

    def update_invite_count_down(self, count_down_dict):
        if not count_down_dict:
            return
        else:
            del_uid_list = []
            for uid, seconds in six.iteritems(count_down_dict):
                button = self.uid_to_btn_dict.get(uid, None)
                if button and button.isValid():
                    if button.lab_time:
                        if seconds <= 0:
                            button.SetEnable(True)
                            button.icon_team.setVisible(True)
                            button.lab_time.setVisible(False)
                            continue
                        button.lab_time.SetString('{}s'.format(seconds))
                        if not button.lab_time.isVisible():
                            button.SetEnable(False)
                            button.icon_team.setVisible(False)
                            button.lab_time.setVisible(True)
                        else:
                            button.SetShowEnable(False)
                    else:
                        del_uid_list.append(uid)

            for uid in del_uid_list:
                self.uid_to_btn_dict.pop(uid)

            return

    def on_click_auto_match(self, *args):
        self.parent.match_widget.on_click_match_btn()

    def on_click_join_clan(self, *args):
        if self.parent and self.parent.is_valid():
            self.parent.on_click_clan_btn()

    def on_click_list_invite(self, uid, btn, *args):
        if not global_data.player:
            return
        count_down_data = global_data.player.get_count_down() if global_data.player else {}
        down_count = count_down_data.get(uid, 0)
        if down_count > 0:
            return
        battle_id = global_data.player.get_battle_tid() or DEFAULT_BATTLE_TID
        team_info = global_data.player.get_team_info() or {}
        auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
        mode = self.get_cur_invite_mode()
        global_data.player.invite_frd(uid, battle_id, auto_flag, mode)
        log_dict = {'d_role_id': uid,
           'scene': mode,
           'action': 'invite_team'
           }
        global_data.player.call_server_method('client_sa_log', ('FriendRec', log_dict))

    def get_cur_invite_mode(self):
        mode = TAB_2_LOG_MODE.get(self.cur_tab_type, log_const.TEAM_MODE_RECENT)
        return mode

    def on_click_list_item(self, uid, btn, *args):
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        ui.refresh_by_uid(uid, show_btn_more=True)
        import cc
        ui.set_position(btn.ConvertToWorldSpace(0, 0), anchor_point=cc.Vec2(1, 1))

    def on_click_list_follow(self, uid, btn, *args):
        global_data.player.req_add_friend(uid)

    def on_click_list_appoint(self, uid, btn, *args):
        self.cur_appoint_uid = uid
        self.nd_invite.nd_appoint.setVisible(True)

    def set_online_state(self, panel, friend_id):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        friend_online_state = global_data.message_data.get_player_online_state()
        state = const.STATE_OFFLINE
        if friend_online_state:
            state = int(friend_online_state.get(int(friend_id), const.STATE_OFFLINE))
        text_id, color = ui_utils.get_online_inf(state)
        panel.btn_item.lab_status.SetString(get_text_by_id(text_id))
        panel.btn_item.lab_status.SetColor(color)
        return state

    def add_player_item(self, data, is_back_item=True, index=-1):
        if 'title' in data and 'uid' not in data:
            return self._add_title(data, is_back_item)
        else:
            ui_list = self.nd_temp_content.friend_content.lv_list
            if is_back_item:
                panel = ui_list.AddTemplateItem(bRefresh=True)
            else:
                panel = ui_list.AddTemplateItem(0, bRefresh=True)
            if not panel:
                return None
            self.refresh_friend_item(panel, data)
            return panel

    def refresh_friend_item(self, panel, data):
        friend_id = data[U_ID]
        name = data.get(C_NAME, '')
        panel.lab_name.setString(name)
        remark = global_data.player._frds_remark.get(int(friend_id), '') if global_data.player else ''
        if panel.lab_name2:
            panel.lab_name2.setVisible(bool(remark))
            if remark:
                panel.lab_name2.SetString('(%s)' % remark)
        if panel.nd_top:
            if global_data.player:
                is_top = int(friend_id) in global_data.player._top_frds if 1 else False
                panel.nd_top.setVisible(is_top)
            self.player_info_manager.add_head_item_auto(panel.temp_head, friend_id, 0, data, show_tips=True, show_btn_more=True)
            self.player_info_manager.add_dan_info_item(panel.temp_tier, friend_id)
            role_head_utils.init_dan_info(panel.temp_tier, friend_id)
            online_state = self.set_online_state(panel, friend_id)
            battle_type = global_data.message_data.get_player_battle_type_by_uid(friend_id)
            if battle_type and online_state in set([const.STATE_BATTLE, const.STATE_BATTLE_FIGHT, const.STATE_ROOM]):
                panel.lab_mode.setString(get_mode_text_by_id(battle_type))
            else:
                panel.lab_mode.setString('')
            priv_data = global_data.message_data.get_player_simple_inf(friend_id)
            priv_data = priv_data or {}
        role_head_utils.init_privilege_name_color_and_badge(panel.lab_name, panel.temp_head, priv_data, 0)
        panel.btn_team.setVisible(online_state == const.STATE_SINGLE)
        panel.btn_appoint.setVisible(self.cur_tab_type == TAB_FRIEND and online_state in (const.STATE_BATTLE, const.STATE_BATTLE_FIGHT))
        friends = global_data.message_data.get_friends()
        is_friend = friend_id in friends
        panel.btn_item.btn_play.setVisible(False)
        if is_not_online(online_state):
            panel.bg_offline.setVisible(True)
            panel.bg_online.setVisible(False)
            if is_friend:
                pass
            elif self.cur_tab_type != TAB_RECOMMEND:
                panel.btn_follow.setVisible(True)
            set_gray(panel.temp_head, True)
        else:
            set_gray(panel.temp_head, False)
            panel.bg_offline.setVisible(False)
            panel.bg_online.setVisible(True)
        if global_data.player:
            count_down_data = global_data.player.get_count_down() or {}
        else:
            count_down_data = {}
        down_count = count_down_data.get(friend_id, 0)
        if down_count <= 0:
            panel.btn_team.SetEnable(True)
            panel.btn_team.icon_team.setVisible(True)
            panel.btn_team.lab_time.setVisible(False)
        self.uid_to_btn_dict[friend_id] = panel.btn_team
        panel.btn_team.BindMethod('OnClick', Functor(self.on_click_list_invite, friend_id))
        panel.btn_item.BindMethod('OnClick', Functor(self.on_click_list_item, friend_id))
        panel.btn_follow.BindMethod('OnClick', Functor(self.on_click_list_follow, friend_id))
        panel.btn_appoint.BindMethod('OnClick', Functor(self.on_click_list_appoint, friend_id))
        labels = data.get('label', [])
        if panel.nd_tags:
            for i in range(3):
                lab_tag_txt = getattr(panel, 'lab_tag%d' % (i + 1))
                if i < len(labels):
                    name_id = confmgr.get('us_recommend_tag', str(labels[i]), 'cName', default=None)
                    txt = get_text_by_id(name_id)
                    lab_tag_txt.SetString(txt)
                    lab_tag_txt.setVisible(bool(txt))
                else:
                    lab_tag_txt.setVisible(False)

        return

    def _add_title(self, data, is_back_item):
        title = data.get('title', '')
        num = data.get('num', '')
        if title and num:
            ui_list = self.nd_temp_content.friend_content.lv_list
            if is_back_item:
                recent_team_title = ui_list.AddItem(self.title_template, bRefresh=True)
            else:
                recent_team_title = ui_list.AddItem(self.title_template, 0, bRefresh=True)
            recent_team_title.lab_title.SetString(title)
            recent_team_title.lab_num.SetString(num)
            return recent_team_title
        else:
            return None

    def refresh_recommend_teammates(self, friends):
        if self.cur_tab_type == TAB_RECOMMEND:
            self.show_friends(friends)

    def refresh_players(self):
        if self.cur_tab_type == None:
            return
        else:
            friend_list = []
            if not self.nd_invite.btn_invite_others:
                return
            self.nd_invite.btn_invite_others.setVisible(self.is_show_invite_others() and self.cur_tab_type != TAB_RECOMMEND)
            self.nd_invite.nd_invite_others_cn.setVisible(bool(self._show_share_for_mainland and self.cur_tab_type != TAB_RECOMMEND))
            if self.cur_tab_type == TAB_FRIEND:
                friend_list = six_ex.values(global_data.message_data.get_friends())
            elif self.cur_tab_type == TAB_RECENT_TEAM:
                friend_list = six_ex.values(global_data.message_data.get_team_friends())
            elif self.cur_tab_type == TAB_RECOMMEND:
                if global_data.player:
                    friend_list = global_data.player.get_recommend_players()
                self.nd_invite.btn_change.BindMethod('OnClick', Functor(self.on_click_change_recommend, show_tips=True))
            elif self.cur_tab_type == TAB_CLAN:
                global_data.player.request_clan_info(open_ui=False, is_silent=True)
                clan_member_data = global_data.player.get_clan_member_data()
                if clan_member_data:
                    friend_list = [ member for member in six.itervalues(clan_member_data) if member[U_ID] != global_data.player.uid ]
                else:
                    friend_list = []
            elif self.cur_tab_type == TAB_NEAR:
                neighbor_players = global_data.player.try_get_neighbor_player()
                if neighbor_players:
                    friend_list = six_ex.values(neighbor_players)
                else:
                    friend_list = []
            self.nd_invite.btn_change.setVisible(self.cur_tab_type == TAB_RECOMMEND)
            self.show_friends(friend_list)
            return

    def show_neighbor_players(self, neighbor_players):
        if self.cur_tab_type != TAB_NEAR:
            return
        if neighbor_players:
            friend_list = six_ex.values(neighbor_players)
        else:
            friend_list = []
        self.show_friends(friend_list)
        if neighbor_players:
            global_data.player.test_get_online_state(six_ex.keys(neighbor_players), immediately=True, include_friends=False)

    def show_clan_players(self, *args):
        if self.cur_tab_type != TAB_CLAN:
            return
        clan_member_data = global_data.player.get_clan_member_data()
        if clan_member_data:
            friend_list = [ member for member in six.itervalues(clan_member_data) if member[U_ID] != global_data.player.uid ]
        else:
            friend_list = []
        self.show_friends(friend_list)

    def show_friends(self, friend_list):
        nd_empty = self.nd_temp_content.friend_content.nd_empty
        if self.cur_tab_type == TAB_CLAN:
            nd_empty and nd_empty.setVisible(not bool(global_data.player.is_in_clan()))
        else:
            nd_empty and nd_empty.setVisible(len(friend_list) == 0)
        friend_list = self.sort_friend_list(friend_list, self.cur_tab_type == TAB_RECENT_TEAM)
        item_count = self.nd_temp_content.friend_content.lv_list.GetItemCount()
        if len(friend_list) < item_count or len(friend_list) < len(self.content_data) or item_count <= 7:
            self.clear_content_list()
            self.refresh_friend_content(friend_list)
        else:
            self.refresh_friend_content_data(friend_list, item_count)
        self.content_data = friend_list

    def on_click_change_recommend(self, *args, **kargs):
        show_tips = kargs.get('show_tips', False)
        cur_battle_tid = None
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if lobby_ui and lobby_ui.match_widget:
            cur_battle_tid = lobby_ui.match_widget.cur_battle_tid
        if cur_battle_tid is None and global_data.player:
            cur_battle_tid = global_data.player.get_battle_tid()
        if cur_battle_tid:
            global_data.player.request_recommend_teammates(cur_battle_tid, show_tips)
        return

    def clear_content_list(self):
        ui_list = self.nd_temp_content.friend_content.lv_list
        ui_list.DeleteAllSubItem()
        self.uid_to_btn_dict = dict()
        self.content_data = []
        self._sview_index = 0
        self._sview_content_height = 0

    def check_sview(self):
        player_num = len(self.content_data)
        self._sview_index = self.nd_temp_content.friend_content.lv_list.AutoAddAndRemoveItem(self._sview_index, self.content_data, player_num, self.add_player_item, 300, 300)
        self._is_check_sview = False

    def on_resolution_changed(self):
        self.nd_invite.ClearAllNodeActionCache()
        if self.nd_vis:
            self.nd_invite.PlayAnimation(self.show_animation_name)
            self.nd_invite.StopAnimation(self.show_animation_name, finish_ani=True)
        else:
            self.nd_invite.PlayAnimation(self.hide_animation_name)
            self.nd_invite.StopAnimation(self.hide_animation_name, finish_ani=True)

    def on_click_copy_url(self):
        import game3d
        share_url, s_title, s_message = share_utils.get_mainland_invite_team_url()
        game3d.set_clipboard_text(share_url)
        global_data.game_mgr.show_tip(get_text_by_id(610379))
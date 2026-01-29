# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomInviteUI.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray
from common.framework import Functor
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.property_const import C_NAME, U_ID, U_LV, ROLE_ID, HEAD_FRAME, HEAD_PHOTO
import logic.gcommon.const as const
import time
from common.platform.dctool import interface
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_const import chat_const
from logic.client.const import share_const
from common.platform import channel_const
from logic.gutils import friend_utils
from logic.gutils import role_head_utils
from logic.gcommon.common_const.battle_const import DEFAULT_BATTLE_TID
from logic.comsys.room.RoomRecruitUI import RoomRecruitUI
from logic.gutils.online_state_utils import is_not_online, get_friend_online_count
TAB_UNINIT = -1
TAB_FRIEND = 0
TAB_RECENT_TEAM = 1
TAB_FACE_TO_FACE = 2
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

class RoomInviteUI(BaseUIWidget):
    VIS_ACT = 180720

    def __init__(self, parent_ui, panel):
        self.panel = panel
        self._room_ui = parent_ui
        self.nd_invite = panel.nd_room_invite
        self.nd_temp_content = panel.nd_room_invite.temp_content
        self.select_tab = TAB_UNINIT
        self.global_events = {'message_refresh_friends': self.refresh_players,
           'message_friend_state': self.refresh_players,
           'room_invite_count_down_event': self.update_invite_count_down
           }
        self.cur_tab_type = None
        self.tab_btn_dict = {TAB_FRIEND: self.nd_invite.btn_tab_friend,
           TAB_RECENT_TEAM: self.nd_invite.btn_tab_recently,
           TAB_FACE_TO_FACE: self.nd_invite.btn_tab_face2face
           }
        self.tab_template_dict = {TAB_FRIEND: 'lobby/i_invite_list',
           TAB_RECENT_TEAM: 'lobby/i_invite_list',
           TAB_FACE_TO_FACE: 'lobby/i_invite_list',
           TAB_UNINIT: 'lobby/i_invite_search_result'
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
        super(RoomInviteUI, self).__init__(parent_ui, panel)
        self.init_widget()
        self.hide()
        return

    def destroy(self):
        if self._input_friend:
            self._input_friend.destroy()
            self._input_friend = None
        self._room_ui = None
        global_data.message_data.destroy_request_online_state_timer()
        global_data.emgr.message_refresh_friend_search -= self.on_search_friends
        super(RoomInviteUI, self).destroy()
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
            new_conent.nd_empty.btn_empty.BindMethod('OnClick', Functor(self.on_click_auto_match))
            new_conent.nd_empty.lab_empty.SetString(get_text_by_id(80092))
            new_conent.nd_empty.btn_empty.SetText(get_text_by_id(80516))
        elif tab_type == TAB_FRIEND:
            new_conent.btn_empty.BindMethod('OnClick', Functor(self.on_click_add_friend))
        if new_tab_btn:
            new_tab_btn.btn_tab_window.SetSelect(True)
            self.refresh_players()
        tab_btn = self.tab_btn_dict.get(tab_type, None)
        if tab_btn:
            tab_btn.btn_tab_window.SetSelect(True)
        return

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
            self.nd_temp_content.friend_content.nd_empty.setVisible(False)
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

    def init_event(self):
        super(RoomInviteUI, self).init_event()
        self.nd_invite.BindMethod('OnClick', self.hide)
        for tab_type, btn in six.iteritems(self.tab_btn_dict):
            btn.btn_tab_window.BindMethod('OnClick', Functor(self.on_click_tab, tab_type))

        self.nd_invite.btn_search.BindMethod('OnClick', Functor(self.on_click_search))
        self.nd_invite.btn_clear.BindMethod('OnClick', Functor(self.on_click_clear_input))
        self.nd_invite.btn_recruit.BindMethod('OnClick', Functor(self.on_click_recruit_btn))
        self.nd_invite.btn_invite_others.setVisible(False)
        self._refresh_btn_recruit()

    def _refresh_btn_recruit(self):
        show_btn_recruit = self._room_ui and not self._room_ui.is_competition_room()
        self.nd_invite.btn_recruit.setVisible(show_btn_recruit)

    def on_room_battle_type_changed(self):
        self._refresh_btn_recruit()

    def init_widget(self):
        global_data.message_data.create_request_online_state_timer()
        self.player_item_template = global_data.uisystem.load_template('lobby/match_friend_item')
        self.title_template = global_data.uisystem.load_template('lobby/i_invite_list_title')
        self.on_click_tab(TAB_FRIEND)
        self.init_friend_panel()
        self.init_share_panel()
        self.init_search_panel()

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

        self._input_friend = InputBox.InputBox(self.nd_invite.lab_search, input_callback=on_input_cd, placeholder=get_text_by_id(80347))
        self._input_friend.set_rise_widget(self.panel)

    def on_click_clear_input(self, *args):
        self._input_friend.set_text('')
        self.nd_invite.btn_clear.setVisible(False)

    def on_click_add_friend(self, *args):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

    def show(self, *args):
        self.nd_vis = True
        self.nd_invite.setVisible(True)
        self.nd_invite.PlayAnimation('appear')
        self.query_player_role_head_info()
        self.refresh_players()
        count_down_data = global_data.player.get_count_down()
        self.update_invite_count_down(count_down_data)

    def query_player_role_head_info(self):
        global_data.message_data.request_role_head_info(['friend', 'recent_team'])

    def hide(self, *args):
        self.nd_vis = False
        self.nd_invite.PlayAnimation('disappear')
        dis_time = self.nd_invite.GetAnimationMaxRunTime('disappear')

        def disappear_callback():
            self.nd_invite.setVisible(False)

        self.nd_invite.SetTimeOut(dis_time, disappear_callback, self.VIS_ACT)

    def init_friend_panel(self):
        pass

    def sort_friend_list(self, friend_list, cmp_team=False):
        friend_online_state = global_data.message_data.get_player_online_state()

        def cmp_func--- This code section failed: ---

 353       0  LOAD_GLOBAL           0  'int'
           3  LOAD_DEREF            0  'friend_online_state'
           6  LOAD_ATTR             1  'get'
           9  LOAD_GLOBAL           0  'int'
          12  LOAD_GLOBAL           1  'get'
          15  BINARY_SUBSCR    
          16  CALL_FUNCTION_1       1 
          19  LOAD_CONST            2  ''
          22  CALL_FUNCTION_2       2 
          25  CALL_FUNCTION_1       1 
          28  STORE_FAST            2  'a_state'

 354      31  LOAD_GLOBAL           0  'int'
          34  LOAD_DEREF            0  'friend_online_state'
          37  LOAD_ATTR             1  'get'
          40  LOAD_GLOBAL           0  'int'
          43  LOAD_FAST             1  'b'
          46  LOAD_CONST            1  'uid'
          49  BINARY_SUBSCR    
          50  CALL_FUNCTION_1       1 
          53  LOAD_CONST            2  ''
          56  CALL_FUNCTION_2       2 
          59  CALL_FUNCTION_1       1 
          62  STORE_FAST            3  'b_state'

 355      65  LOAD_FAST             2  'a_state'
          68  LOAD_FAST             3  'b_state'
          71  COMPARE_OP            3  '!='
          74  POP_JUMP_IF_FALSE   101  'to 101'

 356      77  LOAD_GLOBAL           2  'six_ex'
          80  LOAD_ATTR             3  'compare'
          83  LOAD_GLOBAL           4  'TEAM_INVITE_SORT_RULE'
          86  LOAD_FAST             2  'a_state'
          89  BINARY_SUBSCR    
          90  LOAD_GLOBAL           4  'TEAM_INVITE_SORT_RULE'
          93  LOAD_FAST             3  'b_state'
          96  BINARY_SUBSCR    
          97  CALL_FUNCTION_2       2 
         100  RETURN_END_IF    
       101_0  COME_FROM                '74'

 358     101  LOAD_DEREF            1  'cmp_team'
         104  POP_JUMP_IF_FALSE   240  'to 240'

 359     107  LOAD_FAST             0  'a'
         110  LOAD_ATTR             1  'get'
         113  LOAD_CONST            3  'cnt'
         116  LOAD_CONST            2  ''
         119  CALL_FUNCTION_2       2 
         122  LOAD_FAST             1  'b'
         125  LOAD_ATTR             1  'get'
         128  LOAD_CONST            3  'cnt'
         131  LOAD_CONST            2  ''
         134  CALL_FUNCTION_2       2 
         137  ROT_TWO          
         138  STORE_FAST            4  'a_cnt'
         141  STORE_FAST            5  'b_cnt'

 360     144  LOAD_FAST             0  'a'
         147  LOAD_ATTR             1  'get'
         150  LOAD_CONST            4  'tm'
         153  LOAD_CONST            2  ''
         156  CALL_FUNCTION_2       2 
         159  LOAD_FAST             1  'b'
         162  LOAD_ATTR             1  'get'
         165  LOAD_CONST            4  'tm'
         168  LOAD_CONST            2  ''
         171  CALL_FUNCTION_2       2 
         174  ROT_TWO          
         175  STORE_FAST            6  'a_tm'
         178  STORE_FAST            7  'b_tm'

 361     181  LOAD_FAST             4  'a_cnt'
         184  LOAD_FAST             5  'b_cnt'
         187  COMPARE_OP            3  '!='
         190  POP_JUMP_IF_FALSE   209  'to 209'

 362     193  LOAD_GLOBAL           2  'six_ex'
         196  LOAD_ATTR             3  'compare'
         199  LOAD_FAST             4  'a_cnt'
         202  LOAD_FAST             5  'b_cnt'
         205  CALL_FUNCTION_2       2 
         208  RETURN_END_IF    
       209_0  COME_FROM                '190'

 363     209  LOAD_FAST             6  'a_tm'
         212  LOAD_FAST             7  'b_tm'
         215  COMPARE_OP            3  '!='
         218  POP_JUMP_IF_FALSE   261  'to 261'

 364     221  LOAD_GLOBAL           2  'six_ex'
         224  LOAD_ATTR             3  'compare'
         227  LOAD_FAST             6  'a_tm'
         230  LOAD_FAST             7  'b_tm'
         233  CALL_FUNCTION_2       2 
         236  RETURN_END_IF    
       237_0  COME_FROM                '218'
         237  JUMP_FORWARD         21  'to 261'

 366     240  LOAD_GLOBAL           2  'six_ex'
         243  LOAD_ATTR             3  'compare'
         246  LOAD_ATTR             1  'get'
         249  BINARY_SUBSCR    
         250  LOAD_FAST             1  'b'
         253  LOAD_CONST            1  'uid'
         256  BINARY_SUBSCR    
         257  CALL_FUNCTION_2       2 
         260  RETURN_VALUE     
       261_0  COME_FROM                '237'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 25

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

        count_down_data = global_data.player.get_room_count_down()
        self.update_invite_count_down(count_down_data)

    def update_invite_count_down(self, count_down_dict):
        if not count_down_dict:
            return
        else:
            for uid, seconds in six.iteritems(count_down_dict):
                button = self.uid_to_btn_dict.get(uid, None)
                if button and button.isValid():
                    if seconds <= 0:
                        button.SetEnable(True)
                        button.icon_invite.setVisible(True)
                        button.lab_time_2.setVisible(False)
                        continue
                    button.lab_time_2.SetString('{}s'.format(seconds))
                    if not button.lab_time_2.isVisible():
                        button.SetEnable(False)
                        button.icon_invite.setVisible(False)
                        button.lab_time_2.setVisible(True)
                    else:
                        button.SetShowEnable(False)

            return

    def on_click_auto_match(self, *args):
        pass

    def on_click_list_invite(self, uid, btn, *args):
        global_data.player.invite_friend_into_room(uid)

    def on_click_list_spectate(self, uid, btn, *args):
        global_data.player.request_spectate(uid)

    def on_click_list_item(self, uid, btn, *args):
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        ui.refresh_by_uid(uid)
        import cc
        ui.set_position(btn.ConvertToWorldSpace(0, 0), anchor_point=cc.Vec2(1, 1))

    def on_click_list_follow(self, uid, btn, *args):
        global_data.player.req_add_friend(uid)

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
        if data.get('title'):
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
        self.player_info_manager.add_head_item_auto(panel.temp_head, friend_id, 0, data, show_tips=True)
        role_head_utils.set_role_dan(panel.temp_tier, data.get('dan_info'))
        online_state = self.set_online_state(panel, friend_id)
        if online_state == const.STATE_SINGLE:
            panel.btn_invite.setVisible(True)
        else:
            panel.btn_invite.setVisible(False)
        panel.btn_team.setVisible(False)
        panel.btn_item.btn_play.setVisible(False)
        friends = global_data.message_data.get_friends()
        is_friend = friend_id in friends
        if is_not_online(online_state):
            panel.bg_offline.setVisible(True)
            panel.bg_online.setVisible(False)
            if is_friend:
                pass
            else:
                panel.btn_follow.setVisible(True)
            set_gray(panel.temp_head, True)
        else:
            set_gray(panel.temp_head, False)
            panel.bg_offline.setVisible(False)
            panel.bg_online.setVisible(True)
        count_down_data = global_data.player.get_count_down()
        down_count = count_down_data.get(friend_id, 0)
        if down_count <= 0:
            panel.btn_invite.SetEnable(True)
            panel.btn_invite.icon_invite.setVisible(True)
            panel.btn_invite.lab_time_2.setVisible(False)
        self.uid_to_btn_dict[friend_id] = panel.btn_invite
        panel.btn_invite.BindMethod('OnClick', Functor(self.on_click_list_invite, friend_id))
        panel.btn_play.BindMethod('OnClick', Functor(self.on_click_list_spectate, friend_id))
        panel.btn_item.BindMethod('OnClick', Functor(self.on_click_list_item, friend_id))
        panel.btn_follow.BindMethod('OnClick', Functor(self.on_click_list_follow, friend_id))

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

    def refresh_players(self):
        if self.cur_tab_type == None:
            return
        else:
            friends = {}
            if self.cur_tab_type == TAB_FRIEND:
                friends = global_data.message_data.get_friends()
            else:
                if self.cur_tab_type == TAB_RECENT_TEAM:
                    friends = global_data.message_data.get_team_friends()
                friend_list = six_ex.values(friends)
                if self.nd_temp_content is None or self.nd_temp_content.friend_content is None:
                    return
            if len(friend_list) == 0:
                self.nd_temp_content.friend_content.nd_empty.setVisible(True)
            else:
                self.nd_temp_content.friend_content.nd_empty.setVisible(False)
            friend_list = self.sort_friend_list(friend_list, self.cur_tab_type == TAB_RECENT_TEAM)
            item_count = self.nd_temp_content.friend_content.lv_list.GetItemCount()
            if len(friend_list) < item_count or item_count == 0 or len(friend_list) < len(self.content_data):
                self.clear_content_list()
                self.refresh_friend_content(friend_list)
            else:
                self.refresh_friend_content_data(friend_list, item_count)
            self.content_data = friend_list
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

    def on_click_recruit_btn(self, *args):
        RoomRecruitUI()
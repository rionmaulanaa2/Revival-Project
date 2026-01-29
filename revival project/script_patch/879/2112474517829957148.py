# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FriendList.py
from __future__ import absolute_import
import six
from six.moves import range
from cocosui import cc
from common.const.property_const import *
import logic.gcommon.const as const
from logic.gcommon.common_const import chat_const, friend_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from . import FriendChat
from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray
from logic.gutils import role_head_utils
from logic.gcommon.common_const import spectate_const as sp_const
from logic.gutils.observe_utils import goto_spectate_player, decode_global_spectate_brief_info, is_global_spectate_data_time_valid
from logic.gcommon import time_utility as t_util
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from logic.gutils.online_state_utils import is_not_online
STATE_WEIGHT_MAP = {const.STATE_INVISIBLE: 0,
   const.STATE_OFFLINE: 0,
   const.STATE_BATTLE: 1,
   const.STATE_BATTLE_FIGHT: 2,
   const.STATE_EXERCISE: 3,
   const.STATE_SPECTATING: 4,
   const.STATE_TEAM: 5,
   const.STATE_ROOM: 6,
   const.STATE_SINGLE: 10
   }
FRIEND_LIST_TAB_CONTACT = 0
FRIEND_LIST_TAB_FRIEND = 1
FRIEND_LIST_COUNT = 2
TAB_MAP = {FRIEND_LIST_TAB_CONTACT: {'tab_name': 10258},FRIEND_LIST_TAB_FRIEND: {'tab_name': 10259}}
LIST_SHOW_MAX_COUNT = 14

def is_linegame_friend--- This code section failed: ---

  50       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'feature_mgr'
           6  LOAD_ATTR             2  'is_linegame_ready'
           9  CALL_FUNCTION_0       0 
          12  POP_JUMP_IF_FALSE    68  'to 68'
          15  LOAD_GLOBAL           0  'global_data'
          18  LOAD_ATTR             3  'channel'
          21  LOAD_ATTR             4  'is_bind_linegame'
          24  CALL_FUNCTION_0       0 
          27  POP_JUMP_IF_FALSE    68  'to 68'
          30  LOAD_FAST             0  'linegame_ids'
        33_0  COME_FROM                '27'
        33_1  COME_FROM                '12'
          33  POP_JUMP_IF_FALSE    68  'to 68'

  51      36  LOAD_GLOBAL           0  'global_data'
          39  LOAD_ATTR             5  'message_data'
          42  LOAD_ATTR             6  'get_line_friend_name'
          45  LOAD_ATTR             1  'feature_mgr'
          48  BINARY_SUBSCR    
          49  CALL_FUNCTION_1       1 
          52  STORE_FAST            1  'line_name'

  52      55  LOAD_FAST             1  'line_name'
          58  POP_JUMP_IF_FALSE    68  'to 68'

  53      61  LOAD_GLOBAL           7  'True'
          64  RETURN_END_IF    
        65_0  COME_FROM                '58'
          65  JUMP_FORWARD          0  'to 68'
        68_0  COME_FROM                '65'

  55      68  LOAD_GLOBAL           8  'False'
          71  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 48


def get_name_richtext(data, clr_str):
    social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
    name = data.get(C_NAME, '')
    if is_linegame_friend(social_ids):
        icon = '<img="{}",scale=0.72>'.format(chat_const.LINE_ICON)
        name = '#SW{}#n<color={}>{}</color>({})#n'.format(icon, clr_str, name, global_data.message_data.get_line_friend_name(social_ids[0]))
    else:
        name = '<color={}>{}</color>'.format(clr_str, name)
    return name


class FriendList(object):

    def click_uid_button(self, f_id):
        if f_id in self.uid_to_btn_dict:
            item = self.uid_to_btn_dict[f_id]
            item.btn_item.OnClick(None)
        return

    def __init__(self, main_panel, **kargs):
        panel_temp = global_data.uisystem.load_template_create('friend/i_relationship', main_panel.panel, name='chat_content')
        panel_temp.SetPosition('50%', '50%')
        self.main_panel = main_panel
        self.panel = main_panel.panel
        self._message_data = global_data.message_data
        self._contacts = global_data.message_data.get_contacts()
        self._friends = global_data.message_data.get_friends()
        self._black_friends = global_data.message_data.get_black_friends()
        self._friend_datas = [
         self._contacts, self._friends, self._black_friends]
        self._lv_friend = None
        self._sort_data_list = []
        self._cur_show_index = -1
        self._is_check_sview = False
        self._cur_tab_index = 0
        self._tab_panels = {}
        self._friend_chat_ui = None
        self._last_chat_uid = None
        init_tab_index = kargs.get('tab_index', FRIEND_LIST_TAB_CONTACT)
        if init_tab_index == None:
            init_tab_index = FRIEND_LIST_TAB_CONTACT
        self._init_tab_index = init_tab_index
        self.uid_to_btn_dict = dict()
        self.player_info_manager = PlayerInfoManager()
        self._player_simple_inf_pos_y = self.panel.chat_content.getContentSize().height - 20
        self.init_list()
        self.init_event()
        self._cached_spectate_detail_info = {}
        self._requesting_watch_uid = None
        self._requesting_watch_time = None
        return

    def init_list(self):
        list_tab = self.panel.chat_content.nd_friend.nd_list.nd_tab.list_tab
        self._lv_friend = self.panel.chat_content.nd_friend.nd_list.list_friend
        for tab_index in range(FRIEND_LIST_COUNT):
            panel = list_tab.AddTemplateItem()
            panel.btn_tab.SetText(get_text_by_id(TAB_MAP[tab_index]['tab_name']))
            self.add_touch_tab(panel, tab_index)

        self.touch_tab_by_index(self._init_tab_index)

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self._lv_friend.SetTimeOut(0.001, self.check_sview)

        self._lv_friend.addEventListener(scroll_callback)
        self._friend_chat_ui = FriendChat.FriendChat(self.main_panel)

    def init_event(self):
        global_data.emgr.message_refresh_friends += self.refresh_all_friend
        global_data.emgr.message_refresh_contact_group += self.refresh_all_contact
        global_data.emgr.message_receive_friend_msg += self.refresh_friend_msg_redpoint
        global_data.emgr.message_friend_state += self.refresh_friends_list_state
        global_data.emgr.message_refresh_contact_chat_time += self.refresh_all_contact
        global_data.emgr.team_invite_count_down_event += self.update_invite_count_down
        global_data.emgr.message_social_coins += self.refresh_friends_list_linegame
        global_data.emgr.message_send_friend_gold_gift += self.refresh_friends_list_state
        global_data.emgr.message_on_friend_gold_gift += self.refresh_friends_list_state
        global_data.emgr.message_recv_friend_gold_gift += self.refresh_friends_list_state
        global_data.message_data.request_player_online_state(immediately=True)
        global_data.emgr.on_received_global_spectate_list += self._on_received_global_spectate_list
        global_data.emgr.on_received_global_spectate_brief_list += self._on_received_global_spectate_brief_list

    def add_touch_tab(self, panel, tab_index):
        self._tab_panels[tab_index] = panel
        panel.btn_tab.EnableCustomState(True)

        @panel.btn_tab.callback()
        def OnClick(*args):
            self.touch_tab_by_index(tab_index)

    def touch_tab_by_index(self, tab_index):
        tab_panel = self._tab_panels.get(self._cur_tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(False)
            tab_panel.PlayAnimation('unclick')
            tab_panel.img_vx.setVisible(False)
        tab_panel = self._tab_panels.get(tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(True)
            tab_panel.img_vx.setVisible(True)
            tab_panel.PlayAnimation('click')
        self._cur_tab_index = tab_index
        self.refresh_all_by_index(tab_index)
        count_down_data = global_data.player.get_count_down() if global_data.player else None
        if count_down_data is not None:
            self.update_invite_count_down(count_down_data)
        self._request_spectate_brief_info()
        return

    def refresh_all_by_index(self, tab_index):
        self.uid_to_btn_dict = dict()
        self._lv_friend.DeleteAllSubItem()
        self._sort_data_list = self.get_sort_data(tab_index)
        data_count = len(self._sort_data_list)
        sview_height = self._lv_friend.getContentSize().height
        all_height = 0
        index = 0
        nd_empty_visible = True if data_count == 0 else False
        self.panel.chat_content.nd_friend.nd_list.nd_empty.setVisible(nd_empty_visible)
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._sort_data_list[index]
            uid = data.get('uid', None)
            if uid:
                update_head_info = global_data.message_data.get_role_head_info(uid)
                frame = update_head_info.get('head_frame', None)
                photo = update_head_info.get('head_photo', None)
                if frame and photo:
                    data['head_frame'] = frame
                    data['head_photo'] = photo
            chat_pnl = self.add_friend_item(data, True)
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._lv_friend.ScrollToTop()
        self._lv_friend._container._refreshItemPos()
        self._lv_friend._refreshItemPos()
        self._cur_show_index = index - 1
        return

    def refresh_content_by_index(self, tab_index):
        last_data_count = len(self._sort_data_list)
        self._sort_data_list = self.get_sort_data(tab_index)
        item_count = self._lv_friend.GetItemCount()
        now_data_count = len(self._sort_data_list)
        if now_data_count < item_count:
            self.refresh_all_by_index(tab_index)
            return
        if self._cur_show_index >= len(self._sort_data_list):
            self._cur_show_index = len(self._sort_data_list) - 1
        data_index = self._cur_show_index - item_count
        if now_data_count > last_data_count:
            self.refresh_all_by_index(tab_index)
        else:
            for panel in self._lv_friend.GetAllItem():
                data_index += 1
                data = self._sort_data_list[data_index]
                self.refresh_friend_item(panel, data)

        self.refresh_choose_panel(self._last_chat_uid)

    def get_sort_data(self, tab_index):
        friend_online_state = global_data.message_data.get_player_online_state()
        is_team_friends = False

        def get_cmp_key--- This code section failed: ---

 266       0  LOAD_GLOBAL           0  'int'
           3  LOAD_GLOBAL           1  'global_data'
           6  BINARY_SUBSCR    
           7  CALL_FUNCTION_1       1 
          10  STORE_FAST            1  'uid'

 268      13  LOAD_GLOBAL           1  'global_data'
          16  LOAD_ATTR             2  'player'
          19  POP_JUMP_IF_FALSE    61  'to 61'
          22  LOAD_FAST             1  'uid'
          25  LOAD_GLOBAL           1  'global_data'
          28  LOAD_ATTR             2  'player'
          31  LOAD_ATTR             3  '_top_frds'
          34  COMPARE_OP            6  'in'
        37_0  COME_FROM                '19'
          37  POP_JUMP_IF_FALSE    61  'to 61'
          40  LOAD_GLOBAL           1  'global_data'
          43  LOAD_ATTR             2  'player'
          46  LOAD_ATTR             3  '_top_frds'
          49  LOAD_ATTR             4  'index'
          52  LOAD_FAST             1  'uid'
          55  CALL_FUNCTION_1       1 
          58  JUMP_FORWARD          3  'to 64'
          61  LOAD_CONST            2  -1
        64_0  COME_FROM                '58'

 269      64  LOAD_GLOBAL           0  'int'
          67  LOAD_DEREF            0  'friend_online_state'
          70  LOAD_ATTR             5  'get'
          73  LOAD_FAST             1  'uid'
          76  LOAD_CONST            3  ''
          79  CALL_FUNCTION_2       2 
          82  CALL_FUNCTION_1       1 
          85  BUILD_LIST_2          2 
          88  STORE_FAST            2  'cmp_key'

 271      91  LOAD_DEREF            1  'is_team_friends'
          94  POP_JUMP_IF_FALSE   120  'to 120'

 272      97  LOAD_FAST             2  'cmp_key'
         100  LOAD_ATTR             6  'append'
         103  LOAD_GLOBAL           0  'int'
         106  LOAD_GLOBAL           4  'index'
         109  BINARY_SUBSCR    
         110  CALL_FUNCTION_1       1 
         113  CALL_FUNCTION_1       1 
         116  POP_TOP          
         117  JUMP_FORWARD         63  'to 183'

 273     120  LOAD_DEREF            2  'tab_index'
         123  LOAD_GLOBAL           7  'FRIEND_LIST_TAB_CONTACT'
         126  COMPARE_OP            2  '=='
         129  POP_JUMP_IF_FALSE   160  'to 160'

 274     132  LOAD_FAST             2  'cmp_key'
         135  LOAD_ATTR             6  'append'
         138  LOAD_FAST             0  'x'
         141  LOAD_ATTR             5  'get'
         144  LOAD_CONST            5  'time'
         147  LOAD_CONST            3  ''
         150  CALL_FUNCTION_2       2 
         153  CALL_FUNCTION_1       1 
         156  POP_TOP          
         157  JUMP_FORWARD         23  'to 183'

 276     160  LOAD_FAST             2  'cmp_key'
         163  LOAD_ATTR             6  'append'
         166  LOAD_GLOBAL           0  'int'
         169  LOAD_FAST             0  'x'
         172  LOAD_GLOBAL           8  'U_LV'
         175  BINARY_SUBSCR    
         176  CALL_FUNCTION_1       1 
         179  CALL_FUNCTION_1       1 
         182  POP_TOP          
       183_0  COME_FROM                '157'
       183_1  COME_FROM                '117'

 277     183  LOAD_FAST             2  'cmp_key'
         186  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_1' instruction at offset 7

        data_list = self._friend_datas[tab_index]
        no_black_data_list = []
        for uid, value in six.iteritems(data_list):
            if not global_data.message_data.is_black_friend(int(uid)):
                no_black_data_list.append(value)

        sort_data_list = sorted(no_black_data_list, key=get_cmp_key, reverse=True)
        return sort_data_list

    def add_friend_item(self, data, is_back_item, index=-1, show_last_msg=False):
        if is_back_item:
            panel = self._lv_friend.AddTemplateItem(bRefresh=True)
        else:
            panel = self._lv_friend.AddTemplateItem(0, bRefresh=True)
        self.refresh_friend_item(panel, data, show_last_msg)
        self.uid_to_btn_dict[data[U_ID]] = panel
        return panel

    def refresh_friend_item(self, panel, data, show_last_msg=False):
        friend_id = data[U_ID]
        panel.btn_item.SetEnableCascadeOpacityRecursion(True)
        panel.nd_top.setVisible(int(data.get(U_ID, None)) in global_data.player._top_frds if global_data.player else False)
        setattr(panel, 'panel_type', 'item')
        setattr(panel, 'data', data)
        social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
        if panel.btn_item.lab_name:
            panel.btn_item.lab_name.SetString(get_name_richtext(data, '0X363B51FF'))
        if panel.btn_item.lab_name2:
            if global_data.player:
                remark = global_data.player._frds_remark.get(int(data[U_ID]), '') if 1 else False
                panel.btn_item.lab_name2.setVisible(bool(remark))
                if remark:
                    panel.btn_item.lab_name2.SetString('(%s)' % remark)
            self.player_info_manager.add_head_item_auto(panel.btn_item.temp_head, friend_id, 0, data)
            self.player_info_manager.add_dan_info_item(panel.temp_tier, friend_id)
            role_head_utils.init_dan_info(panel.temp_tier, friend_id)
            self.set_online_state(panel, data)
            if show_last_msg:
                last_msg = data.get('msg', '')
                panel.btn_item.lab_duanwei.setString(last_msg)
            else:
                panel.btn_item.lab_duanwei.setString(str(friend_id))
            self.refresh_panel_unread_count(panel, friend_id)

            @panel.btn_item.callback()
            def OnClick(*args):
                if self._message_data.get_friend_msg_unread_count(friend_id) != 0:
                    self._message_data.set_friend_msg_read(friend_id)
                    self.refresh_friend_msg_redpoint(friend_id)
                self.refresh_friend_chat(panel.data)
                self.refresh_choose_panel(friend_id)

            @panel.temp_head.callback()
            def OnClick(btn, touch):
                pos_x, pos_y = panel.GetPosition()
                world_pos = panel.ConvertToWorldSpace(pos_x, pos_y)
                size = panel.getContentSize()
                world_pos.x += size.width
                ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
                from .PlayerSimpleInf import BTN_TYPE_INTIMACY
                ui.set_extra_btns([BTN_TYPE_INTIMACY])
                ui.refresh_by_uid(int(data[U_ID]), show_btn_more=True, show_btn_del=True)
                ui.set_position(world_pos)

            panel.btn_play.setVisible(False)
            panel.temp_head.SetSwallowTouch(False)

            @panel.btn_play.callback()
            def OnClick(*args):
                if not global_data.player:
                    return
                self._requesting_watch_uid = friend_id
                self._requesting_watch_time = t_util.get_server_time()
                spectate_info = self._cached_spectate_detail_info.get(friend_id)
                if spectate_info:
                    spectate_info['spectate_type'] = sp_const.SPECTATE_LIST_FRIEND
                    goto_spectate_player(spectate_info)
                else:
                    global_data.player.request_global_spectate_details(sp_const.SPECTATE_LIST_FRIEND, [friend_id])

            panel.btn_play.SetSwallowTouch(False)

            @panel.btn_team.callback()
            def OnClick(*args):
                if not global_data.player:
                    return
                else:
                    battle_tid = global_data.player.get_battle_tid()
                    if battle_tid is None:
                        battle_tid = DEFAULT_INVITE_TID
                    team_info = global_data.player.get_team_info() or {}
                    auto_flag = team_info.get('auto_match', global_data.player.get_self_auto_match())
                    from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
                    global_data.player.invite_frd(friend_id, battle_tid, auto_flag, TEAM_MODE_FRIEND)
                    return

            panel.btn_team.SetSwallowTouch(False)
            friend_info = self._message_data.get_player_simple_inf(friend_id)
            if not friend_info:
                friend_info = {}
            priv_lv = friend_info.get('priv_lv', 0)
            priv_settings = friend_info.get('priv_settings', {})
            priv_purple_id = friend_info.get('priv_purple_id', False)
            role_head_utils.init_privliege_badge(panel.btn_item.temp_head, priv_lv, priv_settings.get(const.PRIV_SHOW_BADGE, False))
            if priv_lv != 0 and panel.btn_item.lab_name and priv_purple_id and priv_settings.get(const.PRIV_SHOW_PURPLE_ID, False):
                priv_name_color = '%sFF' % hex(COLOR_NAME)
                panel.btn_item.lab_name.SetString(get_name_richtext(data, priv_name_color))
                panel.data['privilege_color'] = priv_name_color
            elif self._last_chat_uid == friend_id:
                panel.data['privilege_color'] = '0X19247DFF'
            else:
                panel.data['privilege_color'] = '0X363B51FF'
        panel.btn_close.setVisible(self._cur_tab_index == FRIEND_LIST_TAB_CONTACT)

        @panel.btn_close.callback()
        def OnClick(*args):
            global_data.message_data.del_contact(str(friend_id))
            self._contacts = global_data.message_data.get_contacts()
            self.refresh_all_by_index(self._cur_tab_index)
            self._friend_chat_ui and self._friend_chat_ui.on_refresh_contact()

        return

    def update_invite_count_down(self, count_down_dict):
        for uid, seconds in six.iteritems(count_down_dict):
            item = self.uid_to_btn_dict.get(uid, None)
            if item and not item.IsDestroyed():
                button = item.btn_team
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

        return

    def refresh_friend_chat(self, data):
        if self._friend_chat_ui:
            self._friend_chat_ui.refresh_friend_chat(data)

    def refresh_choose_panel(self, uid):
        friend_online_state = self._message_data.get_player_online_state()
        self._refresh_friends_list_state(select_uid=uid)
        self._last_chat_uid = uid

    def refresh_friends_list_state(self, *args):
        self._refresh_friends_list_state()

    def refresh_friends_list_linegame(self, taker_uid):
        from logic.comsys.message import SendLineMessage
        if not self._lv_friend:
            return
        else:
            social_friend = self._message_data.get_social_friend_by_uid(friend_const.SOCIAL_ID_TYPE_LINEGAME, taker_uid)
            if social_friend:
                social_id = social_friend.get('social_id')
                text = get_text_by_id(609023).format(social_friend.get(C_NAME, ''), self._message_data.get_line_friend_name(social_id))
                content = get_text_by_id(609026)
                SendLineMessage.SendLineMessageCoin(None, text=text, sub_text=content, social_id=social_id)
            for item in self._lv_friend.GetAllItem():
                self.set_give_coin(item, item.data)

            return

    def _refresh_friends_list_state(self, select_uid=None):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        friend_online_state = self._message_data.get_player_online_state()
        last_uid = self._last_chat_uid

        def select(list_item):
            uid = list_item.data[U_ID]
            state = int(friend_online_state.get(int(uid), 0))
            item.btn_item.SetSelect(True)
            id_color = list_item.data.get('privilege_color', '0X19247DFF')
            item.btn_item.lab_name.SetString(get_name_richtext(list_item.data, id_color))
            remark = global_data.player._frds_remark.get(int(uid), '') if global_data.player else False
            item.btn_item.lab_name2.setVisible(bool(remark))
            if remark:
                item.btn_item.lab_name2.SetString('(%s)' % remark)
            if is_not_online(state):
                item.btn_item.lab_name.setOpacity(int(204.0))
            else:
                item.btn_item.lab_name.setOpacity(255)
            _, color = ui_utils.get_online_inf(state)
            item.lab_status.SetColor(color)
            if state == const.STATE_SINGLE:
                item.lab_status.SetColor(8781602)

        def unselect(list_item):
            uid = list_item.data[U_ID]
            state = int(friend_online_state.get(int(uid), 0))
            text_id, color = ui_utils.get_online_inf(state)
            list_item.lab_status.SetColor(color)
            id_color = list_item.data.get('privilege_color', '0X363B51FF')
            list_item.btn_item.lab_name.SetString(get_name_richtext(list_item.data, id_color))
            remark = global_data.player._frds_remark.get(int(uid), '') if global_data.player else False
            list_item.btn_item.lab_name2.setVisible(bool(remark))
            if remark:
                list_item.btn_item.lab_name2.SetString('(%s)' % remark)
            list_item.btn_item.SetShowEnable(not is_not_online(state))
            if is_not_online(state):
                item.btn_item.lab_name.setOpacity(int(204.0))
            else:
                item.btn_item.lab_name.setOpacity(255)

        for item in self._lv_friend.GetAllItem():
            uid = item.data[U_ID]
            if select_uid == None:
                self.set_online_state(item, item.data)
                continue
            if uid == select_uid:
                select(item)
            elif uid == last_uid:
                unselect(item)

        return

    def refresh_panel_unread_count(self, panel, friend_id):
        count = self._message_data.get_friend_msg_unread_count(friend_id)
        if count != 0:
            panel.red_dot_1.setVisible(True)
        else:
            panel.red_dot_1.setVisible(False)

    def set_give_coin(self, panel, data):
        from logic.comsys.message import SendLineMessage
        from logic.comsys.message.message_data import GOLD_GIFT_LV_LIMIT
        friend_id = data[U_ID]
        social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
        unlock_lv = GOLD_GIFT_LV_LIMIT
        newest_data = self._message_data.get_player_by_uid(friend_id)
        if not newest_data:
            newest_data = data
        lv_limit = not global_data.player or global_data.player.get_lv() < unlock_lv or newest_data[U_LV] < unlock_lv
        is_line_friend = is_linegame_friend(social_ids)
        is_friend = self._message_data.is_friend(friend_id) and not lv_limit
        if not is_line_friend and not is_friend:
            panel.btn_coin.setVisible(False)
            return
        panel.btn_coin.SetSwallowTouch(False)
        panel.btn_coin.setVisible(True)

        @panel.btn_coin.callback()
        def OnClick(*args):
            if not global_data.player:
                return
            if panel.IsPlayingAnimation('vx_btn_coin'):
                global_data.achi_mgr.get_general_archive_data().set_field(const.HAS_CLICK_FRIEND_CHAT_HINT_KEY, 1)
                panel.StopAnimation('vx_btn_coin')
                panel.btn_coin.nd_vx.setVisible(False)
            if is_line_friend:
                if not global_data.player.has_given_daily_gold_gift(friend_id):
                    global_data.player.give_social_daily_gold_gift(friend_const.SOCIAL_ID_TYPE_LINEGAME, friend_id)
            elif global_data.player.can_send_gold_gift(friend_id):
                global_data.player.request_send_friend_gold_gift(friend_id)

        if panel.btn_invite.isVisible():
            panel.btn_coin.SetPosition('50%45', '50%-20')
        else:
            panel.btn_coin.SetPosition('50%57', '50%-20')
        if is_line_friend:
            has_gave = global_data.player.has_given_daily_gold_gift(friend_id)
            panel.btn_coin.SetEnable(not has_gave)
        else:
            has_gave = global_data.player.has_send_gold_gift(friend_id)
            panel.btn_coin.SetEnable(not has_gave)
        if is_line_friend:

            @panel.btn_invite.callback()
            def OnClick(*args):
                if is_line_friend:
                    SendLineMessage.SendLineMessageInvite(None, social_id=social_ids[0])
                return

    def set_coin_animation(self):
        for item in self._lv_friend.GetAllItem():
            btn_coin = item.btn_coin
            if btn_coin.isVisible() and btn_coin.IsEnable():
                item.PlayAnimation('vx_btn_coin')
                item.nd_vx.setVisible(True)
                return

    def set_btn_gift(self, panel, data):
        social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
        is_line_friend = is_linegame_friend(social_ids)
        is_friend = is_line_friend or self._message_data.is_friend(data[U_ID])
        panel.btn_gift.SetSwallowTouch(False)
        panel.btn_gift.setVisible(is_friend)
        if not is_friend:
            return
        if panel.btn_invite.isVisible():
            panel.btn_gift.SetPosition('50%10', '50%-20')
        else:
            panel.btn_gift.SetPosition('50%5', '50%-20')

        @panel.btn_gift.callback()
        def OnClick(btn, touch):
            ui = global_data.ui_mgr.get_ui('IntimacyGiftUseConfirmUI')
            if not ui:
                ui = global_data.ui_mgr.show_ui('IntimacyGiftUseConfirmUI', 'logic.comsys.intimacy')
            if ui:
                ui.show_window(data)

    def set_online_state(self, panel, data):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        import logic.gcommon.const as const
        friend_id = data[U_ID]
        friend_online_state = self._message_data.get_player_online_state()
        state = int(friend_online_state.get(int(friend_id), 0))
        text_id, color = ui_utils.get_online_inf(state)
        panel.lab_status.setString(get_text_by_id(text_id))
        panel.lab_status.SetColor(color)
        if self._last_chat_uid == friend_id:
            id_color = data.get('privilege_color', '0X19247DFF')
            panel.btn_item.lab_name.SetString(get_name_richtext(data, id_color))
            panel.btn_item.SetSelect(True)
            if state == const.STATE_SINGLE:
                panel.lab_status.SetColor(8781602)
        else:
            id_color = data.get('privilege_color', '0X363B51FF')
            panel.btn_item.lab_name.SetString(get_name_richtext(data, id_color))
            panel.btn_item.SetShowEnable(not is_not_online(state))
        remark = global_data.player._frds_remark.get(int(friend_id), '') if global_data.player else False
        panel.btn_item.lab_name2.setVisible(bool(remark))
        if remark:
            panel.btn_item.lab_name2.SetString('(%s)' % remark)
        if is_not_online(state):
            panel.btn_item.lab_name.setOpacity(int(204.0))
        else:
            panel.btn_item.lab_name.setOpacity(255)
        panel.btn_invite.setVisible(False)
        if is_not_online(state):
            panel.btn_team.setVisible(False)
            set_gray(panel.btn_item.temp_head, True)
            social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
            if is_linegame_friend(social_ids):
                panel.btn_invite.setVisible(True)
        else:
            set_gray(panel.btn_item.temp_head, False)
            panel.btn_team.setVisible(state == const.STATE_SINGLE)
            player = global_data.player
            is_friend = self._message_data.is_friend(friend_id)
            if not is_friend or state != const.STATE_BATTLE_FIGHT or player.is_matching or player.is_in_room() or player.is_in_team():
                panel.btn_play.setVisible(False)
        self.set_give_coin(panel, data)
        self.set_btn_gift(panel, data)
        return not is_not_online(state)

    def refresh_friend_msg_redpoint(self, *args):
        if self._last_chat_uid == args[0] and self._message_data.get_friend_msg_unread_count(args[0]) != 0 and self.panel.chat_content.isVisible():
            self._message_data.set_friend_msg_read(self._last_chat_uid)
        for item in self._lv_friend.GetAllItem():
            if item.panel_type == 'item':
                self.refresh_panel_unread_count(item, item.data[U_ID])

    def refresh_all_friend(self, *args):
        self.refresh_content_by_index(self._cur_tab_index)

    def refresh_all_contact(self, *args):
        if self._cur_tab_index == FRIEND_LIST_TAB_CONTACT:
            self.refresh_content_by_index(self._cur_tab_index)

    def check_sview(self):
        self._cur_show_index = self._lv_friend.AutoAddAndRemoveItem(self._cur_show_index, self._sort_data_list, len(self._sort_data_list), self.add_friend_item, 300, 400)
        self._is_check_sview = False

    def set_visible(self, flag):
        self.panel.chat_content.setVisible(flag)
        if flag and self._last_chat_uid:
            self._message_data.set_friend_msg_read(self._last_chat_uid)
            for item in self._lv_friend.GetAllItem():
                self.refresh_panel_unread_count(item, self._last_chat_uid)

    def hide_inputbox(self):
        if self._friend_chat_ui:
            self._friend_chat_ui.hide_inputbox()

    def destroy(self):
        self.player_info_manager = None
        self._cached_spectate_detail_info = None
        self._requesting_watch_uid = None
        if self._friend_chat_ui:
            self._friend_chat_ui.destroy()
            self._friend_chat_ui = None
        self.uid_to_btn_dict = dict()
        global_data.player and global_data.player.clear_global_spectate_cached()
        global_data.emgr.message_refresh_friends -= self.refresh_all_friend
        global_data.emgr.message_refresh_contact_group -= self.refresh_all_contact
        global_data.emgr.message_receive_friend_msg -= self.refresh_friend_msg_redpoint
        global_data.emgr.message_friend_state -= self.refresh_friends_list_state
        global_data.emgr.message_refresh_contact_chat_time -= self.refresh_all_contact
        global_data.emgr.on_received_global_spectate_list -= self._on_received_global_spectate_list
        global_data.emgr.on_received_global_spectate_brief_list -= self._on_received_global_spectate_brief_list
        global_data.emgr.message_social_coins -= self.refresh_friends_list_linegame
        global_data.emgr.message_send_friend_gold_gift -= self.refresh_friends_list_state
        global_data.emgr.message_on_friend_gold_gift -= self.refresh_friends_list_state
        global_data.emgr.message_recv_friend_gold_gift -= self.refresh_friends_list_state
        global_data.emgr.team_invite_count_down_event -= self.update_invite_count_down
        return

    def _on_received_global_spectate_brief_list(self, list_type):
        if list_type != sp_const.SPECTATE_LIST_FRIEND:
            return
        else:
            list_info = global_data.player.get_global_specate_brief_info(sp_const.SPECTATE_LIST_FRIEND) if global_data.player else []
            for brief_data in list_info:
                item_data = decode_global_spectate_brief_info(brief_data)
                if not item_data:
                    continue
                player_uid = int(item_data.get('uid', 0))
                if not player_uid:
                    continue
                panel = self.uid_to_btn_dict.get(player_uid, None)
                if panel and panel.isValid():
                    if is_global_spectate_data_time_valid(item_data):
                        panel.btn_play.setVisible(True)
                    else:
                        panel.btn_play.setVisible(False)

            return

    def _on_received_global_spectate_list(self, list_type, list_info):
        if not global_data.player or list_type != sp_const.SPECTATE_LIST_FRIEND:
            return
        else:
            for item_data in list_info:
                player_uid = int(item_data.get('uid', 0))
                if player_uid > 0:
                    self._cached_spectate_detail_info[player_uid] = item_data

            if self._requesting_watch_uid and self._requesting_watch_time and t_util.get_server_time() - self._requesting_watch_time <= 1:
                item_data = self._cached_spectate_detail_info.get(self._requesting_watch_uid)
                if item_data:
                    item_data['spectate_type'] = sp_const.SPECTATE_LIST_FRIEND
                    goto_spectate_player(item_data)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19459), True)
                    panel = self.uid_to_btn_dict.get(self._requesting_watch_uid, None)
                    if panel and panel.isValid():
                        panel.btn_play.setVisible(False)
            self._requesting_watch_uid = None
            self._requesting_watch_time = None
            return

    def _request_spectate_brief_info(self):
        player = global_data.player
        if not player:
            return
        request_spectate_brief_uids = []
        friend_online_state = self._message_data.get_player_online_state()
        for item in self._lv_friend.GetAllItem():
            friend_id = int(item.data[U_ID])
            is_friend = self._message_data.is_friend(friend_id)
            state = int(friend_online_state.get(friend_id, 0))
            if state == const.STATE_BATTLE_FIGHT and not player.is_matching and not player.is_in_room() and not player.is_in_team() and is_friend:
                request_spectate_brief_uids.append(friend_id)

        if request_spectate_brief_uids:
            global_data.player and global_data.player.request_global_spectate_brief_list(sp_const.SPECTATE_LIST_FRIEND, request_spectate_brief_uids)

    def get_friend_list(self):
        return self._lv_friend
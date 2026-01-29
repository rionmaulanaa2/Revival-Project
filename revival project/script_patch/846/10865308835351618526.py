# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TeamHall/TeamHallList.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import copy
from cocosui import cc
from logic.gutils import template_utils
from logic.gutils import role_head_utils
from logic.gcommon.common_utils import battle_utils
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gcommon.common_const.team_const import PUBLIC_TEAM_REQUEST_CNT
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gcommon.common_const.battle_const import DEFAULT_DEATH_TID, DEFAULT_BATTLE_TID, DEFAULT_PVE_TID
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY
from logic.gcommon.common_utils.battle_utils import get_mode_name
import time
REQUEST_INTERVAL = 3
TEAM_NUM = 3
BATTLE_TYPE_LIST = [
 DEFAULT_DEATH_TID, DEFAULT_BATTLE_TID, DEFAULT_PVE_TID]
DEFAULT_RECREATION = 0

def check_join_team--- This code section failed: ---

  28       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('dan_data',)
           6  IMPORT_NAME           0  'logic.gcommon.cdata'
           9  IMPORT_FROM           1  'dan_data'
          12  STORE_FAST            1  'dan_data'
          15  POP_TOP          

  29      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('SecondConfirmDlg2',)
          22  IMPORT_NAME           2  'logic.comsys.common_ui.NormalConfirmUI'
          25  IMPORT_FROM           3  'SecondConfirmDlg2'
          28  STORE_FAST            2  'SecondConfirmDlg2'
          31  POP_TOP          

  31      32  POP_TOP          
          33  POP_TOP          
          34  POP_TOP          
          35  BINARY_SUBSCR    
          36  STORE_FAST            3  'battle_type'

  32      39  STORE_FAST            5  'need_voice'
          42  BINARY_SUBSCR    
          43  STORE_FAST            4  'limit_dan'

  33      46  STORE_FAST            6  'chapter'
          49  BINARY_SUBSCR    
          50  STORE_FAST            5  'need_voice'

  34      53  STORE_FAST            7  'unlock_chapter_list'
          56  BINARY_SUBSCR    
          57  STORE_DEREF           0  'leader_uid'

  37      60  LOAD_FAST             3  'battle_type'
          63  LOAD_GLOBAL           4  'DEFAULT_PVE_TID'
          66  COMPARE_OP            2  '=='
          69  POP_JUMP_IF_FALSE   231  'to 231'

  38      72  POP_JUMP_IF_FALSE     8  'to 8'
          75  BINARY_SUBSCR    
          76  STORE_FAST            6  'chapter'

  39      79  LOAD_GLOBAL           5  'global_data'
          82  LOAD_ATTR             6  'player'
          85  POP_JUMP_IF_FALSE   103  'to 103'
          88  LOAD_GLOBAL           5  'global_data'
          91  LOAD_ATTR             6  'player'
          94  LOAD_ATTR             7  'get_unlock_chapter'
          97  CALL_FUNCTION_0       0 
         100  JUMP_FORWARD          6  'to 109'
         103  LOAD_CONST            9  1
         106  BUILD_LIST_1          1 
       109_0  COME_FROM                '100'
         109  STORE_FAST            7  'unlock_chapter_list'

  40     112  LOAD_FAST             6  'chapter'
         115  LOAD_FAST             7  'unlock_chapter_list'
         118  COMPARE_OP            7  'not-in'
         121  POP_JUMP_IF_FALSE   150  'to 150'

  41     124  LOAD_GLOBAL           5  'global_data'
         127  LOAD_ATTR             8  'game_mgr'
         130  LOAD_ATTR             9  'show_tip'
         133  LOAD_GLOBAL          10  'get_text_by_id'
         136  LOAD_CONST           10  541
         139  CALL_FUNCTION_1       1 
         142  CALL_FUNCTION_1       1 
         145  POP_TOP          

  42     146  LOAD_CONST            0  ''
         149  RETURN_END_IF    
       150_0  COME_FROM                '121'

  44     150  LOAD_GLOBAL           5  'global_data'
         153  LOAD_ATTR             6  'player'
         156  POP_JUMP_IF_FALSE   177  'to 177'
         159  LOAD_GLOBAL           5  'global_data'
         162  LOAD_ATTR             6  'player'
         165  LOAD_ATTR            11  'get_chapter_unlock_difficulty'
         168  LOAD_FAST             6  'chapter'
         171  CALL_FUNCTION_1       1 
         174  JUMP_FORWARD          3  'to 180'
         177  LOAD_GLOBAL          12  'NORMAL_DIFFICUTY'
       180_0  COME_FROM                '174'
         180  STORE_FAST            8  'unlock_difficulty'

  45     183  STORE_FAST           11  'team_voice'
         186  BINARY_SUBSCR    
         187  STORE_FAST            9  'difficulty'

  46     190  LOAD_FAST             9  'difficulty'
         193  LOAD_FAST             8  'unlock_difficulty'
         196  COMPARE_OP            4  '>'
         199  POP_JUMP_IF_FALSE   231  'to 231'

  47     202  LOAD_GLOBAL           5  'global_data'
         205  LOAD_ATTR             8  'game_mgr'
         208  LOAD_ATTR             9  'show_tip'
         211  LOAD_GLOBAL          10  'get_text_by_id'
         214  LOAD_CONST           12  511
         217  CALL_FUNCTION_1       1 
         220  CALL_FUNCTION_1       1 
         223  POP_TOP          

  48     224  LOAD_CONST            0  ''
         227  RETURN_END_IF    
       228_0  COME_FROM                '199'
       228_1  COME_FROM                '72'
         228  JUMP_FORWARD          0  'to 231'
       231_0  COME_FROM                '228'

  51     231  LOAD_GLOBAL           5  'global_data'
         234  LOAD_ATTR             6  'player'
         237  LOAD_ATTR            13  'get_dan'
         240  LOAD_FAST             1  'dan_data'
         243  LOAD_ATTR            14  'DAN_SURVIVAL'
         246  CALL_FUNCTION_1       1 
         249  STORE_FAST           10  'cur_dan'

  52     252  LOAD_FAST            10  'cur_dan'
         255  LOAD_FAST             4  'limit_dan'
         258  COMPARE_OP            0  '<'
         261  POP_JUMP_IF_FALSE   290  'to 290'

  53     264  LOAD_GLOBAL           5  'global_data'
         267  LOAD_ATTR             8  'game_mgr'
         270  LOAD_ATTR             9  'show_tip'
         273  LOAD_GLOBAL          10  'get_text_by_id'
         276  LOAD_CONST           13  13119
         279  CALL_FUNCTION_1       1 
         282  CALL_FUNCTION_1       1 
         285  POP_TOP          

  54     286  LOAD_CONST            0  ''
         289  RETURN_END_IF    
       290_0  COME_FROM                '261'

  57     290  LOAD_CONST            1  ''
         293  LOAD_CONST           14  ('LOBBY_TEAM_SPEAKER', 'LOBBY_TEAM_MIC')
         296  IMPORT_NAME          15  'common.audio.ccmini_mgr'
         299  IMPORT_FROM          16  'LOBBY_TEAM_SPEAKER'
         302  STORE_DEREF           1  'LOBBY_TEAM_SPEAKER'
         305  IMPORT_FROM          17  'LOBBY_TEAM_MIC'
         308  STORE_DEREF           2  'LOBBY_TEAM_MIC'
         311  POP_TOP          

  58     312  LOAD_GLOBAL           5  'global_data'
         315  LOAD_ATTR            18  'message_data'
         318  LOAD_ATTR            19  'get_seting_inf'
         321  LOAD_DEREF            1  'LOBBY_TEAM_SPEAKER'
         324  CALL_FUNCTION_1       1 
         327  STORE_FAST           11  'team_voice'

  59     330  LOAD_GLOBAL           5  'global_data'
         333  LOAD_ATTR            18  'message_data'
         336  LOAD_ATTR            19  'get_seting_inf'
         339  LOAD_DEREF            2  'LOBBY_TEAM_MIC'
         342  CALL_FUNCTION_1       1 
         345  STORE_FAST           12  'team_mic'

  61     348  LOAD_FAST             5  'need_voice'
         351  POP_JUMP_IF_FALSE   432  'to 432'
         354  LOAD_FAST            11  'team_voice'
         357  JUMP_IF_FALSE_OR_POP   363  'to 363'
         360  LOAD_FAST            12  'team_mic'
       363_0  COME_FROM                '357'
         363  UNARY_NOT        
       364_0  COME_FROM                '351'
         364  POP_JUMP_IF_FALSE   432  'to 432'

  64     367  LOAD_FAST             2  'SecondConfirmDlg2'
         370  CALL_FUNCTION_0       0 
         373  STORE_DEREF           3  'dlg'

  66     376  LOAD_CLOSURE          3  'dlg'
         379  LOAD_CLOSURE          1  'LOBBY_TEAM_SPEAKER'
         382  LOAD_CLOSURE          2  'LOBBY_TEAM_MIC'
         385  LOAD_CLOSURE          0  'leader_uid'
         391  LOAD_CONST               '<code_object on_confirm>'
         394  MAKE_CLOSURE_0        0 
         397  STORE_FAST           13  'on_confirm'

  71     400  LOAD_DEREF            3  'dlg'
         403  LOAD_ATTR            20  'confirm'
         406  LOAD_CONST           16  'content'
         409  LOAD_GLOBAL          10  'get_text_by_id'
         412  LOAD_CONST           17  13121
         415  CALL_FUNCTION_1       1 
         418  LOAD_CONST           18  'confirm_callback'
         421  LOAD_FAST            13  'on_confirm'
         424  CALL_FUNCTION_512   512 
         427  POP_TOP          

  72     428  LOAD_CONST            0  ''
         431  RETURN_END_IF    
       432_0  COME_FROM                '364'

  74     432  LOAD_GLOBAL           5  'global_data'
         435  LOAD_ATTR             6  'player'
         438  LOAD_ATTR            21  'apply_join_team'
         441  LOAD_DEREF            0  'leader_uid'
         444  LOAD_CONST           19  'is_public'
         447  LOAD_GLOBAL          22  'True'
         450  CALL_FUNCTION_257   257 
         453  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 32


class TeamHallList(ClanPageBase):
    DEATH_IDX = 0
    NORMAL_IDX = 1
    PVE_IDX = 2

    def __init__(self, dlg):
        self.global_events = {'refresh_public_teams': self.on_refresh_public_teams,
           'player_join_team_event': self.on_my_team_change,
           'player_leave_team_event': self.on_my_team_change,
           'player_add_teammate_event': self.on_my_team_change,
           'player_del_teammate_event': self.on_my_team_change,
           'player_change_leader_event': self.on_my_team_change,
           'refresh_public_single_team': self.on_refresh_public_single_team
           }
        super(TeamHallList, self).__init__(dlg)

    def on_init_panel(self):
        super(TeamHallList, self).on_init_panel()
        self._refresh_team_cb = {}
        self.last_request_time = 0
        self.update_act = None
        self._cur_index = 0
        self._last_index = 0
        self._cur_battle_type = DEFAULT_DEATH_TID
        self._teams_data = {}
        self._team_list_map = {}
        self.tab_widgets = {}
        self.tab_list = [{'battle_type': DEFAULT_DEATH_TID,'widget_func': self.init_death_hall,'template': 'lobby/i_team_hall_room_normal'}, {'battle_type': DEFAULT_BATTLE_TID,'widget_func': self.init_normal_hall,'template': 'lobby/i_team_hall_room_normal'}, {'battle_type': DEFAULT_PVE_TID,'widget_func': self.init_pve_hall,'template': 'lobby/i_team_hall_room_pve'}]
        self.init_widget()
        self._init_hall_bar()
        self.register_timer()
        return

    def on_finalize_panel(self):
        super(TeamHallList, self).on_finalize_panel()
        self.update_act = None
        self._refresh_team_cb = {}
        return

    def refresh_panel(self):
        self.set_default_touch_tap()

    def is_pve_mode(self):
        return self._cur_battle_type == DEFAULT_PVE_TID

    def request_teams_data(self, index=None, show_tips=True):
        if index is None:
            index = self._cur_index
        global_data.player and global_data.player.request_public_teams(self._cur_battle_type, index, index + PUBLIC_TEAM_REQUEST_CNT, show_tips)
        return

    def on_refresh_public_teams(self, start, end, data):
        self.last_request_time = time.time()
        self._last_index = self._cur_index
        if self._last_index != 0 and start != 0 and not data:
            self._cur_index = 0
            return
        self._cur_index = start
        self._teams_data = {}
        for i, team_info in enumerate(data):
            team_member = team_info['mem']
            battle_type = team_info['battle_type']
            if len(team_member) < TEAM_NUM or global_data.player.uid in team_member:
                battle_type_key = battle_type if battle_type in BATTLE_TYPE_LIST else DEFAULT_RECREATION
                if battle_type_key not in self._teams_data:
                    self._teams_data[battle_type_key] = []
                self._teams_data[battle_type_key].append(team_info)

        self.show_option()
        self.show_team_list()

    def count_down(self):
        cur_time = time.time()
        if cur_time - self.last_request_time > REQUEST_INTERVAL:
            self.request_teams_data(self._last_index, False)

    def register_timer(self):
        if self.update_act:
            return
        self.count_down()
        if self.panel:
            self.update_act = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
             cc.DelayTime.create(1.0),
             cc.CallFunc.create(self.count_down)])))

    def init_widget(self):
        from logic.gcommon.cdata import dan_data
        from logic.comsys.lobby.TeamHall import TeamReleaseUI

        @self.panel.btn_refresh.unique_callback()
        def OnClick(btn, touch):
            self.request_teams_data()

        self.panel.btn_filter.setVisible(False)
        self.panel.nd_top.temp_information.setVisible(False)

        @self.panel.btn_filter.unique_callback()
        def OnClick(btn, touch):
            TeamReleaseUI.TeamFilterUI(None)
            return

        @self.panel.btn_release.unique_callback()
        def OnClick(btn, touch):
            TeamReleaseUI.TeamReleaseUI(None, battle_type=self._cur_battle_type)
            return

        @self.panel.btn_join.unique_callback()
        def OnClick(btn, touch):
            global_data.player.auto_join_public_team(self._cur_battle_type)

        @self.panel.btn_change.unique_callback()
        def OnClick(btn, touch):
            team_info = global_data.player.get_team_info()
            if team_info and team_info['public_info']:
                TeamReleaseUI.TeamReleaseUI(None, is_change=True, battle_type=self._cur_battle_type)
            else:
                TeamReleaseUI.TeamReleaseUI(None, battle_type=self._cur_battle_type)
            return

        @self.panel.btn_quit.unique_callback()
        def OnClick(btn, touch):
            global_data.player.req_leave_team()

        self.show_my_team()

    def init_death_hall(self, nd):
        self._team_list_map[DEFAULT_DEATH_TID] = nd.list_team

    def init_normal_hall(self, nd):
        self._team_list_map[DEFAULT_BATTLE_TID] = nd.list_team

    def init_recreation_hall(self, nd):
        self._team_list_map[DEFAULT_RECREATION] = nd.list_team

    def init_pve_hall(self, nd):
        self._team_list_map[DEFAULT_PVE_TID] = nd.list_team

    def _init_hall_bar(self):

        def init_hall_btn(node, data):
            battle_type = data['battle_type']
            tap_str = get_text_by_id(83515) if battle_type == DEFAULT_RECREATION else get_mode_name(battle_type)
            node.btn_tab.SetText(tap_str)

        def hall_btn_click_cb(ui_item, data, index):
            self._cur_battle_type = data.get('battle_type')
            if self._cur_battle_type not in self.tab_widgets:
                template = data.get('template')
                _nd = global_data.uisystem.load_template_create(template, self.panel.nd_list)
                _nd.SetPosition('50%', '50%')
                widget_func = data.get('widget_func')
                widget_func(_nd)
                self.tab_widgets[self._cur_battle_type] = _nd
            can_request_public_teams = global_data.player.check_can_request_public_teams(self._cur_battle_type) if global_data.player else False
            if can_request_public_teams:
                self._hall_bar_wrapper.set_node_select(ui_item)
            for cur_battle_type in self.tab_widgets:
                widget = self.tab_widgets[cur_battle_type]
                if self._cur_battle_type == cur_battle_type:
                    widget.setVisible(True)
                    if can_request_public_teams:
                        self._cur_index = 0
                        self.request_teams_data()
                else:
                    widget.setVisible(False)

        list_tab = self.panel.list_tab
        self._hall_bar_wrapper = WindowTopSingleSelectListHelper()
        self._hall_bar_wrapper.set_up_list(list_tab, self.tab_list, init_hall_btn, hall_btn_click_cb)
        self.set_default_touch_tap()

    def set_default_touch_tap(self):
        list_tab = self.panel.list_tab
        default_index = self.DEATH_IDX
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        if ui:
            default_index = self.PVE_IDX
        self._hall_bar_wrapper.set_node_click(list_tab.GetItem(default_index))

    def show_option(self):
        return
        message_data = global_data.message_data
        play_type = battle_utils.get_play_type_by_battle_id(message_data.get_seting_inf('filter_team_battle_tid'))
        cur_dan = message_data.get_seting_inf('filter_team_dan_limit')
        need_voice = True if message_data.get_seting_inf('filter_team_need_voice') else False
        team_desc = message_data.get_seting_inf('invite_player_msg')
        template_utils.init_team_hall_info(self.panel.nd_top.temp_information, play_type, cur_dan, need_voice, team_desc)

    def set_player_simple_inf_cb(self, temp_head, uid):

        @temp_head.callback()
        def OnClick(layer, touch):
            if not uid:
                return
            if uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(uid)
            ui.set_position(touch.getLocation(), cc.Vec2(0.0, 1.0))

    def on_create_item(self, inst_cb, data_list):

        def _on_create_item(list_reward, index, widget_item):
            inst_cb(widget_item, index, data_list)

        return _on_create_item

    def on_team_item(self, widget_item, index, data_list, is_mine=False):
        from common.utilities import cut_string_by_len
        widget_item.list_team_role.SetInitCount(TEAM_NUM)

        def refresh_cb(widget_item=widget_item):
            team_info = data_list[index]
            battle_type = team_info['battle_type']
            if not is_mine:
                list_team = self._team_list_map[self._cur_battle_type]
                if self._cur_battle_type != battle_type:
                    list_team.DeleteItem(widget_item)
                    del self._refresh_team_cb[index]
                    return
            limit_dan = team_info['limit_dan']
            need_voice = team_info['need_voice']
            team_desc = team_info['declaration']
            team_member = team_info['mem']
            members_num = len(team_member)
            leader_uid = team_info['leader_uid']
            if leader_uid not in team_member:
                return
            else:
                player_info = team_member[leader_uid]
                is_my_team = global_data.player.uid in team_member
                if is_my_team:
                    widget_item.lab_name.SetString(19408)
                else:
                    name = player_info.get('char_name', '')
                    widget_item.lab_name.SetString('{}\xe7\x9a\x84\xe5\xb0\x8f\xe9\x98\x9f'.format(name))
                if battle_type == DEFAULT_PVE_TID:
                    template_utils.init_pve_team_hall_info(widget_item.temp_information, team_info, limit_dan, need_voice, team_desc)
                else:
                    play_type = battle_utils.get_play_type_by_battle_id(battle_type)
                    template_utils.init_team_hall_info(widget_item.temp_information, play_type, limit_dan, need_voice, team_desc)
                if getattr(widget_item, 'btn_join'):
                    widget_item.btn_join.setVisible(not is_my_team)

                    @widget_item.btn_join.unique_callback()
                    def OnClick(btn, touch):
                        check_join_team(team_info)
                        widget_item.btn_join.setVisible(False)

                if getattr(widget_item, 'btn_change'):
                    public_info = team_info['public_info']
                    text_id = 13108 if public_info else 13106
                    widget_item.btn_change.SetText(text_id)
                    widget_item.btn_change.setVisible(global_data.player.uid == global_data.player.get_leader_id())
                if getattr(widget_item, 'lab_myteam_num'):
                    widget_item.lab_myteam_num.SetString('{}/{}'.format(members_num, TEAM_NUM))
                member_ids = [
                 leader_uid]
                for mid in six_ex.keys(team_member):
                    if mid not in member_ids:
                        member_ids.append(mid)

                for i in range(TEAM_NUM):
                    nd_role = widget_item.list_team_role.GetItem(i)
                    nd_role.lab_name.setVisible(False)
                    nd_role.temp_tier.setVisible(False)
                    nd_role.temp_head.icon_leader.setVisible(False)
                    if i >= members_num:
                        self.set_player_simple_inf_cb(nd_role.temp_head, 0)
                        role_head_utils.init_role_head(nd_role.temp_head, 0, None)
                        nd_role.temp_head.img_head.setVisible(False)
                        continue
                    uid = member_ids[i]
                    player_info = team_member[uid]
                    nd_role.temp_head.img_head.setVisible(True)
                    if leader_uid == uid:
                        nd_role.temp_head.icon_leader.setVisible(True)
                    if not is_mine:
                        nd_role.lab_name.setVisible(True)
                        nd_role.temp_tier.setVisible(True)
                        name = player_info.get('char_name', '')
                        name = cut_string_by_len(name, 3, end='...')
                        nd_role.lab_name.SetString(name)
                        role_head_utils.set_role_dan(nd_role.temp_tier, player_info.get('dan_info'))
                    self.set_player_simple_inf_cb(nd_role.temp_head, uid)
                    role_head_utils.init_role_head(nd_role.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))

                return

        if not is_mine:
            self._refresh_team_cb[index] = refresh_cb
        refresh_cb()

    def show_team_list(self):
        team_list = self._teams_data.get(self._cur_battle_type, [])
        list_team = self._team_list_map[self._cur_battle_type]
        self._refresh_team_cb = {}
        list_team.BindMethod('OnCreateItem', self.on_create_item(self.on_team_item, team_list))
        list_team.DeleteAllSubItem()
        list_team.SetInitCount(len(team_list))
        list_team.scroll_Load()

    def on_refresh_public_single_team(self, op_type, new_team_info):
        self.show_my_team()
        team_list = self._teams_data.get(self._cur_battle_type, [])
        for i, team_info in enumerate(team_list):
            if new_team_info['team_id'] == team_info['team_id']:
                if op_type == 'DELETE':
                    self.panel.SetTimeOut(2, lambda : self.request_teams_data())
                else:
                    team_info.update(new_team_info)
                    if i in self._refresh_team_cb:
                        self._refresh_team_cb[i]()
                break

    def on_my_team_change(self, *args):
        self.show_my_team()

    def show_my_team(self):
        team_info = global_data.player.get_team_info()
        self.panel.nd_team.setVisible(False)
        self.panel.nd_noteam.setVisible(False)
        if team_info:
            self.panel.nd_team.setVisible(True)
            message_data = global_data.message_data
            wrap_team_info = {}
            public_info = team_info['public_info']
            if public_info:
                wrap_team_info['limit_dan'] = public_info['limit_dan']
                wrap_team_info['need_voice'] = public_info['need_voice']
                wrap_team_info['declaration'] = public_info['declaration']
                wrap_team_info['battle_type'] = team_info['battle_type']
                wrap_team_info['chapter'] = public_info.get('chapter', 1)
                wrap_team_info['difficulty'] = public_info.get('difficulty', NORMAL_DIFFICUTY)
            else:
                wrap_team_info['limit_dan'] = message_data.get_seting_inf('team_dan_limit')
                wrap_team_info['need_voice'] = True if message_data.get_seting_inf('team_need_voice') else False
                wrap_team_info['declaration'] = message_data.get_seting_inf('invite_player_msg')
                wrap_team_info['battle_type'] = message_data.get_seting_inf('team_battle_tid')
                wrap_team_info['chapter'] = message_data.get_seting_inf('team_chapter')
                wrap_team_info['difficulty'] = message_data.get_seting_inf('team_difficulty')
            my_uid = global_data.player.uid
            wrap_team_info['leader_uid'] = global_data.player.get_leader_id()
            wrap_team_info['mem'] = copy.deepcopy(team_info['members'])
            my_info = {}
            wrap_team_info['mem'][my_uid] = my_info
            wrap_team_info['public_info'] = public_info
            my_info['char_name'] = global_data.player.char_name
            my_info['dan_info'] = global_data.player.get_dan_info()
            my_info['head_frame'] = global_data.player.get_head_frame()
            my_info['head_photo'] = global_data.player.get_head_photo()
            self.on_team_item(self.panel.nd_team, 0, [wrap_team_info], is_mine=True)
        else:
            self.panel.nd_noteam.setVisible(True)
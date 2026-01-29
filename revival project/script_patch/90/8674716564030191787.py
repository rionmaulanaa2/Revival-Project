# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyTeamListWidget.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.framework import Functor
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
import logic.gcommon.const as const
from logic.gcommon.common_const.battle_const import MATCH_TEAM, DEFAULT_PVE_TID
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, init_privliege_badge, set_gray_by_online_state
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_const.team_const import HANG_UP_TIME
from common.utils.timer import CLOCK
TEAM_WIDGET_HEIGHT_DICT = {2: 210,
   3: 300,
   4: 300
   }

class LobbyTeamListWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel):
        self.global_events = {'player_join_team_event': self.update_teammate_list,
           'player_leave_team_event': self.update_teammate_list,
           'player_set_ready_event': self.on_ready_state_update,
           'player_add_teammate_event': self.update_teammate_list,
           'player_del_teammate_event': self.update_teammate_list,
           'player_change_leader_event': self.on_change_leader,
           'battle_match_status_event': self.update_teammate_list,
           'player_match_info_change_event': self.update_teammate_list,
           'message_friend_state': self.on_refresh_player_state,
           'player_enter_visit_scene_event': self.update_visit_icon,
           'player_leave_visit_scene_event': self.update_visit_icon,
           'on_login_success_event': self.update_teammate_list,
           'net_reconnect_event': self.update_teammate_list,
           'ccmini_team_speaking_list': self.refresh_team_speak
           }
        super(LobbyTeamListWidget, self).__init__(parent_ui, panel)
        self.teammate_dict = {}
        self.player_info_manager = PlayerInfoManager()
        self.leader_id = 0
        self.hang_up_timer = None
        self.init_team_widget()
        return

    def destroy(self):
        self.teammate_dict = {}
        self.avatar_widget = None
        if self.hang_up_timer:
            global_data.game_mgr.unregister_logic_timer(self.hang_up_timer)
            self.hang_up_timer = None
        super(LobbyTeamListWidget, self).destroy()
        return

    def init_event(self):
        super(LobbyTeamListWidget, self).init_event()
        self.panel.btn_leave.BindMethod('OnClick', self.on_click_leave_team)
        self.panel.btn_add_player.BindMethod('OnClick', self.on_invite_clicked)
        self.panel.btn_lobby_change.BindMethod('OnClick', self.on_lobby_change_clicked)

    def init_team_widget(self):
        self.avatar_widget = self.panel.btn_head
        self.teammate_list = self.panel.list_teammate
        self.teammate_list.DeleteAllSubItem()
        self.teammate_conf = global_data.uisystem.load_template('lobby/i_teammate_head')
        self.btn_add_conf = global_data.uisystem.load_template('lobby/i_teammate_head_add')
        self.update_teammate_list()

    def update_visit_icon(self, *args):
        if not global_data.player:
            return
        if global_data.player.is_leader():
            self.panel.btn_lobby_change.setVisible(False)
            return
        res_path = 'gui/ui_res_2/main/icon_in_house.png'
        if global_data.player.is_visit_others():
            res_path = 'gui/ui_res_2/main/icon_out_house.png'
        self.panel.icon_lobby_change.SetDisplayFrameByPath('', res_path)
        self.panel.btn_lobby_change.setVisible(True)

    def update_teammate_list(self, *args):
        if not global_data.player:
            return
        else:
            team_info = global_data.player.get_team_info()
            team_info = team_info or {}
            team_member = 1 + global_data.player.get_team_size()
            self.teammate_dict = {}
            self.leader_id = 0
            self.teammate_list.DeleteAllSubItem()
            self.teammate_dict[global_data.player.uid] = self.panel.btn_head
            self.set_ready_state(self.panel.btn_head, global_data.player.get_self_ready() and team_member > 1, global_data.player.get_ready_battle_type())
            self.set_leader_state(self.panel.btn_head, global_data.player.is_leader(False))
            self.panel.btn_add_player.setVisible(not bool(team_info))
            self.panel.btn_invite.setVisible(not bool(team_info))
            self.update_visit_icon()
            nd_teammate = self.panel.nd_teammate
            nd_teammate.setVisible(bool(team_info))
            if not team_info:
                return
            leader_id = team_info.get('leader', None)
            self.leader_id = leader_id
            if team_info:
                team_dict = team_info.get('members', {})
                for uid, member in six.iteritems(team_dict):
                    ui_item = self.teammate_list.AddItem(self.teammate_conf)
                    self.teammate_dict[uid] = ui_item
                    ready = member.get('ready', False)
                    battle_type = member.get('battle_type', None)
                    self.set_ready_state(ui_item, ready, battle_type)
                    is_leader = uid == leader_id
                    self.set_leader_state(ui_item, is_leader)
                    self.set_leader_house(ui_item, is_leader)
                    ui_item.temp_role_head.SetEnableTouch(True)
                    ui_item.temp_role_head.BindMethod('OnClick', Functor(self.on_click_teammate_head, uid))
                    self.player_info_manager.add_head_item_auto(ui_item.temp_role_head, uid, 1, member)
                    priv_lv = member.get('priv_lv', 0)
                    priv_settings = member.get('priv_settings', {})
                    if priv_lv != 0:
                        init_privliege_badge(ui_item.temp_role_head, priv_lv, priv_settings.get(const.PRIV_SHOW_BADGE, False))
                    hang_up_ts = member.get('hang_up_ts', 0)
                    cur_time = get_server_time()
                    is_hang_up = cur_time < hang_up_ts
                    ui_item.nd_hang and ui_item.nd_hang.setVisible(is_hang_up)
                    if is_hang_up:
                        if self.hang_up_timer is not None:
                            global_data.game_mgr.unregister_logic_timer(self.hang_up_timer)
                            self.hang_up_timer = None
                        self.hang_up_timer = global_data.game_mgr.register_logic_timer(self.update_hang_up_state, 1, times=-1, mode=CLOCK)
                        is_leader = global_data.player.is_leader()
                        ui_item.nd_hang and ui_item.nd_hang.btn_close.setVisible(is_leader)
                        is_leader and ui_item.btn_close.BindMethod('OnClick', lambda btn, touch, uid=uid: global_data.player and global_data.player.kick_teammate(uid))

            self.update_hang_up_state()
            self.update_quit_team_btn(team_info)
            self.update_teammate_list_state()
            tid = team_info['battle_type']
            battle_type, match_mode = battle_utils.get_type_and_mode_by_battle_id(tid)
            is_matching = global_data.player.is_matching
            if team_member < MATCH_TEAM and not is_matching:
                self.add_invite_btn()
            return

    def update_hang_up_state(self):

        def end_timer():
            global_data.game_mgr.unregister_logic_timer(self.hang_up_timer)
            self.hang_up_timer = None
            return

        if not global_data.player:
            end_timer()
            return
        team = global_data.player._team
        if not team:
            end_timer()
            return
        cur_time = get_server_time()
        someone_hang_up = False
        for uid, item in six.iteritems(self.teammate_dict):
            team_member = team.get_teammate(int(uid))
            if not team_member:
                continue
            hang_up_ts = team_member.get_hang_up_ts()
            left_hang_up = hang_up_ts - cur_time
            item.nd_hang and item.nd_hang.setVisible(left_hang_up > 0)
            if left_hang_up > 0:
                item.lab_time.SetString('%ds' % left_hang_up)
                someone_hang_up = True

        if not someone_hang_up:
            end_timer()

    def update_teammate_list_state(self):
        from logic.comsys.effect import ui_effect
        if self and self.panel and self.teammate_list:
            for uid, ui_item in six.iteritems(self.teammate_dict):
                ui_item = self.teammate_dict.get(uid, None)
                if ui_item and ui_item.temp_role_head:
                    state = global_data.message_data.get_player_online_state_by_uid(uid)
                    set_gray_by_online_state(ui_item.temp_role_head, state)

        return

    def add_invite_btn(self):
        ui_item = self.teammate_list.AddItem(self.btn_add_conf)
        ui_item.btn_teammate_add.set_click_sound_name('menu_open')
        ui_item.btn_teammate_add.BindMethod('OnClick', self.on_invite_clicked)
        ui_item.btn_teammate_add.icon_add.setVisible(True)

    def on_invite_clicked(self, *args):
        if not global_data.player:
            return
        cur_battle_tid = global_data.player.get_battle_tid()
        battle_type, match_mode = battle_utils.get_type_and_mode_by_battle_id(cur_battle_tid)
        play_type = battle_utils.get_play_type_by_battle_id(cur_battle_tid)
        nxt_battle_tid = battle_utils.get_battle_id_by_player_mode_and_type(play_type, MATCH_TEAM, battle_type)
        opened = True
        if opened:
            self.parent.update_team_invite_widget_vis(True)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(13070))

    def on_lobby_change_clicked(self, *args):
        player = global_data.player
        if not player:
            return
        if player.is_visit_others():
            player.request_visit_home()
        else:
            player.request_visit_leader()

    def on_click_teammate_head(self, uid, btn, *args):
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        ui.refresh_by_uid(uid)
        import cc
        ui.set_position(btn.ConvertToWorldSpace(0, 0), anchor_point=cc.Vec2(1, 1))

    def set_ready_state(self, widget, ready, battle_type):
        if battle_type == DEFAULT_PVE_TID:
            ready = False
        if ready == widget.icon_ready.isVisible():
            return
        if ready:
            widget.PlayAnimation('ready')
        else:
            widget.StopAnimation('ready')
            widget.icon_ready.setVisible(False)
        widget.icon_ready.setVisible(ready)

    def set_leader_state(self, widget, is_leader):
        widget.icon_leader.setVisible(is_leader)

    def set_leader_house(self, widget, is_leader):
        widget.icon_house.setVisible(is_leader)

    def on_ready_state_update(self, uid, is_ready, battle_type):
        if uid == self.leader_id:
            is_ready = False
        widget = self.teammate_dict.get(uid, None)
        if widget:
            self.set_ready_state(widget, is_ready, battle_type)
        return

    def on_change_leader(self, leader_id):
        if not global_data.player:
            return
        self_id = global_data.player.uid
        for k, v in six.iteritems(self.teammate_dict):
            is_leader = k == leader_id
            self.set_leader_state(v, is_leader)
            if k != self_id:
                self.set_leader_house(v, is_leader)

    def update_quit_team_btn(self, team_info):
        self.panel.btn_leave.setVisible(bool(team_info))

    def on_click_leave_team(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(13027), confirm_callback=lambda : global_data.player and global_data.player.req_leave_team())

    def on_refresh_player_state(self):
        self.update_teammate_list_state()

    def refresh_team_speak(self, session_id, all_list, all_energy):
        if all_list:
            for index, eid in enumerate(all_list):
                uid = global_data.ccmini_mgr.get_uid_by_eid(eid, session_id)
                widget = self.teammate_dict.get(uid, None)
                if widget and widget.voice:
                    voice = widget.voice
                    energy_level = ui_utils.get_energy_level(all_energy[index])
                    voice.setVisible(True)
                    for i in range(3):
                        img_voice = getattr(voice, 'voice_%d' % (i + 1), None)
                        if img_voice:
                            if i + 1 <= energy_level:
                                img_voice.setVisible(True)
                            else:
                                img_voice.setVisible(False)

        else:
            for widget in six_ex.values(self.teammate_dict):
                if widget and widget.voice:
                    voice = widget.voice
                    voice.setVisible(False)

        return
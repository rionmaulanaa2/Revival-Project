# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVELeftTopWidget.py
from __future__ import absolute_import
from logic.gutils.client_utils import safe_call, post_ui_method, safe_widget
from logic.gutils.red_point_utils import get_LobbyUI_role_head_level, show_red_point_template
from logic.comsys.role.RoleBuffWidget import RoleBuffWidget
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_const.battle_const import MATCH_TWO, MATCH_TEAM
from logic.gutils.lobby_click_interval_utils import check_click_interval
from logic.gutils.role_head_utils import init_role_head, init_privilege_name_color_and_badge
from logic.gutils.lv_template_utils import init_lv_template
from logic.comsys.lobby.LobbyTeamInviteWidget import LobbyTeamInviteWidget
from .PVETeamListWidget import PVETeamListWidget
from logic.gutils import system_unlock_utils
from logic.gutils import clan_utils
import cc

class PVELeftTopWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.init_params()
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.init_panel),
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.init_event),
         cc.CallFunc.create(self.init_ui_event)]))

    def destroy(self):
        global_data.emgr.player_on_change_name -= self.on_change_name
        global_data.emgr.player_info_update_event -= self.update_player_info
        global_data.emgr.update_privilege_state -= self.update_privilege_state
        global_data.emgr.privilege_level_upgrade -= self.update_privilege_state
        if self.teamlist_widget:
            self.teamlist_widget.destroy()
            self.teamlist_widget = None
        if self.team_invite_widget:
            self.team_invite_widget.destroy()
            self.team_invite_widget = None
        if self.role_buff_widget:
            self.role_buff_widget.on_finalize_panel()
            self.role_buff_widget = None
        return

    def init_params(self):
        self.teamlist_widget = None
        self.team_invite_widget = None
        self.role_buff_widget = None
        return

    def init_panel(self):
        enable_pve_team = global_data.enable_pve_team
        self.panel.nd_team.setVisible(enable_pve_team)
        if enable_pve_team:
            self.init_teamlist_widget()
            self.init_team_invite_widget()
        self.init_role_buff_widget()
        self.update_player_info()
        self.update_privilege_state()

    @safe_widget
    def init_teamlist_widget(self):
        self.teamlist_widget = PVETeamListWidget(self, self.panel)

    @safe_widget
    def init_team_invite_widget(self):
        self.team_invite_widget = LobbyTeamInviteWidget(self, self.panel)

    def update_team_invite_widget_vis(self, visible):
        self.team_invite_widget.show() if visible else self.team_invite_widget.hide()

    @safe_widget
    def init_role_buff_widget--- This code section failed: ---

  79       0  LOAD_GLOBAL           0  'RoleBuffWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'close'
          15  CALL_FUNCTION_257   257 
          18  LOAD_FAST             0  'self'
          21  STORE_ATTR            3  'role_buff_widget'

Parse error at or near `CALL_FUNCTION_257' instruction at offset 15

    def init_event(self):
        global_data.emgr.player_on_change_name += self.on_change_name
        global_data.emgr.player_info_update_event += self.update_player_info
        global_data.emgr.update_privilege_state += self.update_privilege_state
        global_data.emgr.privilege_level_upgrade += self.update_privilege_state

    def init_ui_event(self):
        self.panel.btn_head.BindMethod('OnClick', self.on_click_player_detail_inf)
        self.panel.btn_invite.BindMethod('OnClick', self.on_click_add_player)
        self.panel.btn_recruit.BindMethod('OnClick', self.on_click_team_hall)

    def on_click_add_player(self, *args):
        if not global_data.player:
            return
        cur_battle_tid = global_data.player.get_battle_tid()
        battle_type, match_mode = battle_utils.get_type_and_mode_by_battle_id(cur_battle_tid)
        play_type = battle_utils.get_play_type_by_battle_id(cur_battle_tid)
        match_mode_list = [
         MATCH_TWO, MATCH_TEAM]
        for _match_mode in match_mode_list:
            nxt_battle_tid = battle_utils.get_battle_id_by_player_mode_and_type(play_type, _match_mode, battle_type)
            opened = True
            if opened:
                self.update_team_invite_widget_vis(True)
                return

        global_data.game_mgr.show_tip(get_text_by_id(13070))

    def on_click_team_hall(self, *args):
        global_data.ui_mgr.show_ui('TeamHallUI', 'logic.comsys.lobby.TeamHall')

    def on_click_visitor(self):
        global_data.ui_mgr.show_ui('LobbyVisitMainUI', 'logic.comsys.home_message_board')

    def on_click_msg(self):
        global_data.ui_mgr.show_ui('LobbyMessageBoardMainUI', 'logic.comsys.home_message_board')

    @check_click_interval()
    def on_click_player_detail_inf(self, *args):
        ui = global_data.ui_mgr.show_ui('PlayerInfoUI', 'logic.comsys.role')
        ui.refresh_by_uid(global_data.player.uid)
        global_data.lobby_red_point_data.record_main_rp('role_head_rp')

    @check_click_interval()
    def on_main_friend_ui(self, *args):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

    def update_player_info(self, *args):
        player = global_data.player
        if not player:
            return
        else:
            init_role_head(self.panel.btn_head, player.get_head_frame(), player.get_head_photo())
            init_lv_template(self.panel.temp_level, player.get_lv())
            self.panel.lab_name.SetString(player.get_name())
            if G_IS_NA_USER:
                self.panel.lab_id.SetString('ID:{}'.format(global_data.player.uid))
            else:
                show_id = int(global_data.player.uid)
                show_id -= global_data.uid_prefix
                self.panel.lab_id.SetString('ID:{}'.format(show_id))
            have_click_lottery_tab = getattr(global_data, 'have_click_lottery_tab', None)
            if have_click_lottery_tab is None:
                global_data.have_click_lottery_tab = {}
            self.update_role_head_rp()
            return

    @post_ui_method
    def update_role_head_rp(self):
        rp_level = get_LobbyUI_role_head_level()
        show_red_point_template(self.panel.btn_head.temp_head_red, rp_level, rp_level)

    def update_privilege_state(self):
        if not global_data.player:
            return
        player_data = global_data.player.get_privilege_data()
        init_privilege_name_color_and_badge(self.panel.lab_name, self.panel.btn_head, player_data)

    def on_change_name(self, cname):
        self.panel.lab_name.SetString(cname)

    def is_valid(self):
        return self.panel is not None and self.panel.isValid()

    def on_click_clan_btn(self, *args):
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_CLAN)
        if not has_unlock:
            system_unlock_utils.show_sys_unlock_tips(system_unlock_utils.SYSTEM_CLAN)
            return
        has_red_point = clan_utils.has_level_red_point()
        if has_red_point:
            clan_utils.set_first_visit_entry_lv()
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if lobby_ui:
                lobby_ui.update_clan_red_point()
        if global_data.player and global_data.player.is_in_clan():
            if global_data.player.get_new_clan_intro():
                global_data.player.confirm_new_clan_intro()
            global_data.player.request_clan_info(open_ui=True)
        else:
            global_data.player.search_clan_by_limit(1, 99999, 99999, 0, open_ui=True)
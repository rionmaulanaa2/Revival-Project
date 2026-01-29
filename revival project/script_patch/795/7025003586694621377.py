# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/GvgRoomTeamListUI.py
from __future__ import absolute_import
import six
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_ROOM_KICK_OUT, BTN_TYPE_TRANSFER_OWNERSHIP, BTN_TYPE_REPORT, BTN_TYPE_CHANGE_SEAT, BTN_TYPE_JUDGEMENT_ADJUST_SEAT, BTN_TYPE_MODIFY_NAME
from logic.gutils.role_head_utils import init_role_head_auto, set_gray, set_role_dan
import time
from logic.gutils.template_utils import update_badge_node
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon.const import STATE_OFFLINE, STATE_BATTLE, STATE_BATTLE_FIGHT
from logic.gcommon.const import BATTLE_STATE_FIGHTING, BATTLE_STATE_INROOM
from logic.gcommon import const
from logic.gutils.custom_room_utils import is_in_judge_seat, judgement_before_adjust_seat, on_click_temp_head, show_modify_name_dialog
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.text_utils import check_review_words
from logic.gutils.online_state_utils import is_not_online
GVG_TEAM_SIZE = 5
CHANGE_SEAT_CD = 30
DEFAULT_CLIP_PATH = 'gui/ui_res_2/room/bar_role_nopick.png'

class GvgRoomTeamListUI(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'on_self_judgement_change': self.on_self_judgement_change
           }
        super(GvgRoomTeamListUI, self).__init__(parent, panel)
        self.team_list = [self.panel.list_team_1, self.panel.list_team_2]
        self._uid2change_seat_timestamp = {}

    def init_room_team_list_ui(self, room_info):
        self.room_info = room_info
        for team_index, curr_team in enumerate(self.team_list):
            self.init_team(curr_team, team_index)

        self.init_team_name_ui(room_info)

    def init_team_name_ui(self, room_info):
        lab_team_name_list = [
         self.panel.img_bar_1.lab_num_1, self.panel.img_bar_2.lab_num_2]
        btn_edit_list = [self.panel.img_bar_1.btn_blue_edit, self.panel.img_bar_2.btn_red_edit]
        is_competition = self.room_info.is_competition(self.room_info.battle_type)
        if not is_competition:
            for btn_edit in btn_edit_list:
                btn_edit.setVisible(False)

            return
        is_creator = global_data.player.uid == self.room_info.creator
        is_judgement = is_in_judge_seat(self.room_info.get_player_seat_idx(global_data.player.uid))
        for idx, btn_edit in enumerate(btn_edit_list):
            btn_edit.setVisible(is_creator or is_judgement)

            @btn_edit.unique_callback()
            def OnClick(btn, touch, _team_idx=idx + 1):
                self.on_click_edit_team_name_btn(_team_idx)

        team_names = room_info.team_names or {}
        for idx, lab_team_name in enumerate(lab_team_name_list):
            team_idx = idx + 1
            lab_team_name.SetString(team_names.get(team_idx, ''))

    def on_click_edit_team_name_btn(self, team_idx):
        from logic.gutils.custom_room_utils import show_modify_team_name_dialog
        show_modify_team_name_dialog(team_idx)

    def on_self_judgement_change(self, become_judgement):
        if not self.room_info:
            return
        is_competition = self.room_info.is_competition(self.room_info.battle_type)
        if not is_competition:
            return
        if not self.panel.img_bar_2 or not self.panel.img_bar_1:
            return
        is_creator = global_data.player.uid == self.room_info.creator
        btn_edit_list = [self.panel.img_bar_1.btn_blue_edit, self.panel.img_bar_2.btn_red_edit]
        for btn_edit in btn_edit_list:
            btn_edit.setVisible(become_judgement or is_creator)

    def on_set_competition_team_name(self, team_idx, team_name):
        lab_team_name_list = [self.panel.img_bar_1.lab_num_1, self.panel.img_bar_2.lab_num_2]
        lab_team_name_list[team_idx - 1].SetString(team_name)

    def put_all_player_in_seat(self):
        for player_id, player_info in six.iteritems(self.room_info.players):
            self.put_one_player_in_seat(player_info)

    def put_one_player_in_seat(self, player_info):
        if not player_info:
            return
        else:
            seat_index = player_info.get('seat_index', None)
            if seat_index is None:
                return
            seat_ui = self.get_seat_ui_by_index(seat_index)
            self.populate_seat_ui(seat_ui, seat_index, player_info)
            return

    def get_seat_ui_by_index(self, seat_index):
        if const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
            return None
        else:
            team_index = seat_index // self.room_info.max_team_size
            seat_index_in_team = seat_index % self.room_info.max_team_size
            return self.team_list[team_index].GetItem(seat_index_in_team)

    def get_seat_ui_by_player_uid(self, player_uid):
        player_info = self.room_info.get_player_data(player_uid)
        if player_info is None:
            return
        else:
            seat_index = player_info.get('seat_index', None)
            if seat_index is None or const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
                return
            seat_ui = self.get_seat_ui_by_index(seat_index)
            return seat_ui

    def init_team(self, team_ui, team_idx):
        team_ui.SetNumPerUnit(1, False)
        team_ui.SetInitCount(self.room_info.max_team_size)
        for team_seat_idx, seat_ui in enumerate(team_ui.GetAllItem()):
            self.create_seat_ui(seat_ui, self.room_info.max_team_size, team_idx, team_seat_idx)

        self.put_all_player_in_seat()

    def create_seat_ui(self, seat_ui, team_size, team_idx, team_seat_idx):
        seat_idx = team_idx * team_size + team_seat_idx
        player_info = self.room_info.get_team_seat_player_data(seat_idx)
        self.populate_seat_ui(seat_ui, seat_idx, player_info)

    def populate_seat_ui(self, seat_ui, seat_idx, player_data=None):
        if seat_ui is None:
            return
        else:
            if player_data:
                player_id = player_data.get('uid', None)
                is_creator = self.room_info.creator == player_id
                player_name = player_data.get('char_name', '')
                player_name_in_room = player_data.get('char_name_in_room', player_name)
                clan_name = player_data.get('clan_name', '')
                clan_lv = player_data.get('clan_lv', '')
                clan_badge = player_data.get('clan_badge', 0)
                battle_state = player_data.get('battle_state', 0)
                dan_info = player_data.get('dan_info', {})
                if battle_state == BATTLE_STATE_FIGHTING:
                    seat_ui.temp_head.nd_battle.setVisible(True)
                else:
                    seat_ui.temp_head.nd_battle.setVisible(False)
                seat_ui.img_bar.setVisible(True)
                seat_ui.img_owner.setVisible(is_creator)
                seat_ui.nd_info.setVisible(True)
                seat_ui.nd_empty.setVisible(False)
                seat_ui.nd_info.lab_name.setVisible(True)
                seat_ui.nd_info.lab_name.SetString(str(player_name_in_room))
                seat_ui.temp_head.setVisible(True)
                seat_ui.temp_head.img_role_bar.setVisible(True)
                seat_ui.temp_head.frame_head.img_head.setVisible(True)
                seat_ui.temp_head.img_head_frame.setVisible(True)
                seat_ui.temp_head.nd_scale.nd_vx.setVisible(True)
                seat_ui.temp_head.img_head.setVisible(True)
                seat_ui.temp_head.img_empty.setVisible(False)
                seat_ui.temp_head.head_vx.nd_head_vx and seat_ui.temp_head.head_vx.nd_head_vx.setVisible(False)
                init_role_head_auto(seat_ui.temp_head, player_id, 0, None, head_frame=player_data.get('head_frame'), head_photo=player_data.get('head_photo'))
                if clan_name == '':
                    seat_ui.lab_crew.setVisible(False)
                    seat_ui.nd_crew.setVisible(False)
                else:
                    seat_ui.lab_crew.setVisible(True)
                    seat_ui.nd_crew.setVisible(True)
                    seat_ui.lab_crew.SetString(str(clan_name))
                    seat_ui.lab_crew_level.SetString(str(clan_lv))
                    update_badge_node(clan_badge, seat_ui.temp_crew_logo)
                if global_data.player.uid == player_id:
                    seat_ui.lab_name.SetColor('#DB')
                    seat_ui.lab_crew.SetColor('#SY')
                else:
                    seat_ui.lab_name.SetColor('#SW')
                    seat_ui.lab_crew.SetColor('#SW')
                seat_ui.temp_tier.setVisible(True)
                set_role_dan(seat_ui.temp_tier, dan_info)
            else:
                player_id = None
                player_name = ''
                set_gray(seat_ui.temp_head, False)
                seat_ui.img_bar.setVisible(True)
                seat_ui.img_owner.setVisible(False)
                seat_ui.nd_info.setVisible(False)
                seat_ui.nd_info.lab_name.SetString(player_name)
                seat_ui.nd_info.lab_name.setVisible(False)
                seat_ui.nd_empty.setVisible(True)
                seat_ui.nd_empty.lab_name.SetColor(9211572)
                seat_ui.nd_empty.lab_name.SetString(get_text_by_id(19513))
                seat_ui.temp_tier.setVisible(False)
                seat_ui.temp_head.setVisible(True)
                seat_ui.temp_head.frame_head.img_head.setVisible(False)
                seat_ui.temp_head.img_head_frame.setVisible(False)
                seat_ui.temp_head.img_role_bar.setVisible(True)
                seat_ui.temp_head.nd_scale.nd_vx.setVisible(False)
                seat_ui.temp_head.nd_battle.setVisible(False)
                seat_ui.temp_head.img_role_bar.SetDisplayFrameByPath('', DEFAULT_CLIP_PATH)
                seat_ui.temp_head.img_head.setVisible(False)
                seat_ui.temp_head.img_empty.setVisible(True)
                seat_ui.temp_head.head_vx.nd_head_vx and seat_ui.temp_head.head_vx.nd_head_vx.setVisible(False)
                seat_ui.lab_crew.setVisible(False)
                seat_ui.nd_crew.setVisible(False)

            @seat_ui.temp_head.unique_callback()
            def OnClick(btn, touch, player_id=player_id):
                is_competition = self.room_info.is_competition(self.room_info.battle_type)
                self_seat_idx = self.room_info.get_player_seat_idx(global_data.player.uid)
                on_click_temp_head(player_id, seat_ui, seat_idx, self.show_player_brief_info, is_competition, self_seat_idx)

            return

    def show_player_brief_info(self, seat_ui, player_id, seat_idx):
        if player_id == global_data.player.uid:
            return
        player_info_ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        player_info_ui.del_btn(BTN_TYPE_REPORT)
        self_seat_idx = self.room_info.get_player_seat_idx(global_data.player.uid)
        if self.room_info.creator == global_data.player.uid:
            is_competition = self.room_info.is_competition(self.room_info.battle_type)
            player_info_ui.custom_show_btns_func({BTN_TYPE_ROOM_KICK_OUT: lambda uid=player_id: self.owner_kick_player_out(uid),
               BTN_TYPE_TRANSFER_OWNERSHIP: lambda uid=player_id: self.transfer_ownership(uid),
               BTN_TYPE_CHANGE_SEAT: lambda uid=player_id, seat_index=self_seat_idx: self.change_seat_with_someone(uid, seat_index),
               BTN_TYPE_JUDGEMENT_ADJUST_SEAT: lambda uid=player_id, seat_index=seat_idx: judgement_before_adjust_seat(uid, seat_index),
               BTN_TYPE_MODIFY_NAME: lambda uid=player_id: show_modify_name_dialog(uid)
               })
            if player_id == global_data.player.uid:
                show_btns = []
            else:
                show_btns = is_competition or [BTN_TYPE_ROOM_KICK_OUT, BTN_TYPE_TRANSFER_OWNERSHIP, BTN_TYPE_CHANGE_SEAT] if 1 else [BTN_TYPE_ROOM_KICK_OUT, BTN_TYPE_JUDGEMENT_ADJUST_SEAT, BTN_TYPE_MODIFY_NAME]
            player_info_ui.custom_show_btn(show_btns)
        else:
            player_info_ui.custom_show_btns_func({BTN_TYPE_CHANGE_SEAT: lambda uid=player_id, seat_index=self_seat_idx: self.change_seat_with_someone(uid, seat_index),
               BTN_TYPE_JUDGEMENT_ADJUST_SEAT: lambda uid=player_id, seat_index=seat_idx: judgement_before_adjust_seat(uid, seat_index),
               BTN_TYPE_MODIFY_NAME: lambda uid=player_id: show_modify_name_dialog(uid)
               })
            if player_id == global_data.player.uid:
                show_btns = []
            elif is_in_judge_seat(self_seat_idx):
                show_btns = [
                 BTN_TYPE_JUDGEMENT_ADJUST_SEAT, BTN_TYPE_MODIFY_NAME]
            else:
                show_btns = [
                 BTN_TYPE_CHANGE_SEAT]
            player_info_ui.custom_show_btn(show_btns)
        player_info_ui.refresh_by_uid(player_id)
        wpos = seat_ui.ConvertToWorldSpacePercentage(100, 0)
        player_info_ui.set_position(wpos, anchor_point=cc.Vec2(1, 1))

    def owner_kick_player_out(self, uid):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            global_data.ui_mgr.close_ui('PlayerSimpleInf')
            global_data.player.req_kick_player(uid)

        SecondConfirmDlg2().confirm(content=get_text_by_id(862054), confirm_callback=confirm_callback)

    def transfer_ownership(self, uid):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            global_data.ui_mgr.close_ui('PlayerSimpleInf')
            global_data.player.req_transfer_ownership(uid)

        SecondConfirmDlg2().confirm(content=get_text_by_id(862012), confirm_callback=confirm_callback)

    def change_seat_with_someone(self, uid, seat_index):
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        last_ask_timestamp = self._uid2change_seat_timestamp.get(uid)
        now = time.time()
        if last_ask_timestamp is not None:
            if now - last_ask_timestamp < CHANGE_SEAT_CD:
                left_seconds = int(CHANGE_SEAT_CD - (now - last_ask_timestamp))
                global_data.game_mgr.show_tip(get_text_by_id(862021).format(left_seconds))
                return
            self._uid2change_seat_timestamp[uid] = now
        else:
            self._uid2change_seat_timestamp[uid] = now
        global_data.player.req_change_seat_with_someone(uid, seat_index)
        return

    def refresh_roommate_online_state(self, roommate_state):
        if not roommate_state:
            return
        else:
            for uid, st in six.iteritems(roommate_state):
                if uid == global_data.player.uid:
                    continue
                player_info = self.room_info.get_player_data(uid)
                if player_info is None:
                    continue
                seat_index = player_info.get('seat_index', None)
                if seat_index is None:
                    continue
                seat_ui = self.get_seat_ui_by_index(seat_index)
                if not seat_ui:
                    continue
                if st == STATE_OFFLINE:
                    set_gray(seat_ui.temp_head, True)
                else:
                    room_ui = global_data.ui_mgr.get_ui('RoomUINew')
                    if room_ui:
                        is_battle_finished = room_ui.is_waiting()
                        if is_battle_finished and (st == STATE_BATTLE_FIGHT or st == STATE_BATTLE):
                            set_gray(seat_ui.temp_head, True)
                            continue
                    set_gray(seat_ui.temp_head, False)

            return

    def on_other_player_quit_battle_state(self, uid, state):
        player_info = self.room_info.get_player_data(uid)
        if player_info is None:
            return
        else:
            seat_index = player_info.get('seat_index', None)
            if seat_index is None:
                return
            seat_ui = self.get_seat_ui_by_index(seat_index)
            if not seat_ui:
                return
            if state == BATTLE_STATE_FIGHTING:
                seat_ui.temp_head.nd_battle.setVisible(True)
            else:
                seat_ui.temp_head.nd_battle.setVisible(False)
            return

    def set_all_player_battle_state(self, state=BATTLE_STATE_INROOM):
        for player_id, player_info in six.iteritems(self.room_info.players):
            seat_index = player_info.get('seat_index', None)
            if seat_index is None:
                return
            seat_ui = self.get_seat_ui_by_index(seat_index)
            if not seat_ui:
                return
            if state == BATTLE_STATE_FIGHTING:
                seat_ui.temp_head.nd_battle.setVisible(True)
            else:
                seat_ui.temp_head.nd_battle.setVisible(False)

        return

    def on_set_char_name_in_room(self, uid, char_name_in_room):
        seat_ui = self.get_seat_ui_by_player_uid(uid)
        if not seat_ui:
            return
        seat_ui.nd_info.lab_name.SetString(char_name_in_room)
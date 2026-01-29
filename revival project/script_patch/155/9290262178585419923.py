# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_00, UI_VKB_CLOSE
from logic.gcommon.const import OB_GROUP_ID_START, OB_SIT_INDEX_END
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import CommonAsynTeamList
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import DEFAULT_KOTH_TID
from logic.gcommon.common_const.battle_const import DEFAULT_RECRUITMENT_TID

def is_in_judge_seat(seat_idx):
    return seat_idx is not None and OB_GROUP_ID_START <= seat_idx <= OB_SIT_INDEX_END


def is_in_waiting_seat--- This code section failed: ---

  21       0  LOAD_FAST             0  'seat_idx'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  JUMP_IF_TRUE_OR_POP    18  'to 18'
          12  JUMP_IF_TRUE_OR_POP     1  'to 1'
          15  COMPARE_OP            2  '=='
        18_0  COME_FROM                '9'
          18  RETURN_VALUE     

Parse error at or near `JUMP_IF_TRUE_OR_POP' instruction at offset 12


class RoomInfo(object):

    def __init__(self):
        self.rid = 0
        self.teams = []

    def init_from_dict(self, info):
        self.rid = info.get('room_id', 0)
        self.max_team_size = int(info.get('max_team_size', -1))
        self.max_team_cnt = int(info.get('max_team_cnt', -1))
        self.battle_type = info.get('battle_type', -1)
        self.name = unpack_text(info.get('name', ''))
        self.players = info.get('players')
        self.team_seat2player = {}
        self.creator = info.get('creator')
        self.need_pwd = info.get('need_pwd', False)
        self.judge_list = {}
        self.waiting_list = {}
        self.init_data()

    def get_share_dict(self):
        from common.cfg import confmgr
        battle_conf = confmgr.get('battle_config')
        battle_name = battle_conf.get(str(self.battle_type), {}).get('name', '')
        return {'room_id': self.rid,
           'room_name': self.name,
           'battle_name': battle_name,
           'battle_type': self.battle_type
           }

    def init_data(self):
        for uid, data in six.iteritems(self.players):
            seat_idx = data.get('seat_index', None)
            if is_in_judge_seat(seat_idx):
                self.judge_list.update({uid: seat_idx})
            if is_in_waiting_seat(seat_idx):
                self.waiting_list.update({uid: seat_idx})
            else:
                self.team_seat2player[seat_idx] = uid

        return

    def player_leave_room(self, uid):
        old_seat = self.get_player_seat_idx(uid)
        if uid in self.players:
            del self.players[uid]
        if uid in self.judge_list:
            del self.judge_list[uid]
        if uid in self.waiting_list:
            del self.waiting_list[uid]
        if old_seat in self.team_seat2player:
            del self.team_seat2player[old_seat]

    def player_enter_room(self, uid, player_data):
        self.players.update({uid: player_data})
        self.waiting_list[uid] = player_data.get('seat_index', None)
        return

    def on_player_seat_down(self, uid, seat_idx):
        old_seat = self.get_player_seat_idx(uid)
        if uid in self.players:
            self.players[uid].update({'seat_index': seat_idx})
        is_judge_seat = is_in_judge_seat(seat_idx)
        if is_judge_seat:
            self.judge_list.update({uid: seat_idx})
        elif uid in self.judge_list:
            del self.judge_list[uid]
        is_waiting_seat = is_in_waiting_seat(seat_idx)
        if is_waiting_seat:
            self.waiting_list.update({uid: seat_idx})
        elif uid in self.waiting_list:
            del self.waiting_list[uid]
        if old_seat in self.team_seat2player:
            del self.team_seat2player[old_seat]
        if not is_judge_seat and not is_waiting_seat:
            self.team_seat2player[seat_idx] = uid

    def get_player_seat_idx(self, uid):
        if uid in self.players:
            return self.players[uid].get('seat_index', None)
        else:
            return None

    def get_player_data(self, uid):
        if uid in self.players:
            return self.players[uid]
        else:
            return None
            return None

    def get_team_seat_player_data(self, seat_idx):
        if seat_idx in self.team_seat2player:
            uid = self.team_seat2player[seat_idx]
            return self.get_player_data(uid)
        else:
            return None

    def get_available_judge_seat(self):
        total_seat = range(OB_GROUP_ID_START, OB_SIT_INDEX_END + 1)
        occupied_seat = six_ex.values(self.judge_list)
        for seat_idx in total_seat:
            if seat_idx not in occupied_seat:
                return seat_idx

        return None

    def get_player_num_in_team(self):
        return len(self.players) - len(self.waiting_list) - len(self.judge_list)

    def destroy(self):
        self.judge_list = {}
        self.waiting_list = {}
        self.players = {}

    def update_roommate_info(self, uid, info):
        player_info = self.players.get(uid, None)
        if player_info is None:
            return
        else:
            player_info.update(info)
            return


from common.const import uiconst

class RoomUI(BasePanel):
    PANEL_CONFIG_NAME = 'room/room_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    JUDGE_MAX_NUM = 3
    CAMP_NUM = 3
    UI_ACTION_EVENT = {'btn_refresh.OnClick': 'req_refresh_room_list',
       'btn_waiting_list.OnClick': 'switch_show_waiting_list',
       'btn_judgment.OnClick': 'switch_show_judge_list',
       'btn_exit.btn_common.OnClick': 'on_click_exit_btn',
       'layer_list_bg.OnClick': 'on_click_list_bg',
       'pnl_waiting_list.OnClick': 'on_click_waiting_list',
       'pnl_judgment_list.OnClick': 'on_click_judge_list',
       'btn_start.btn_common.OnClick': 'on_click_start_btn',
       'btn_be_waiting.btn_common.OnClick': 'on_click_waiting_btn',
       'btn_be_judge.btn_common.OnClick': 'on_click_judge_btn',
       'btn_share.btn_common.OnClick': 'on_click_share_btn'
       }

    def on_init_panel(self, room_info):
        self.init_parameters()
        self.init_event()
        self.update_widget()
        self._has_set_appear_effect = False
        self.room_info = None
        self.team_list_wrapper = None
        self.init_room(room_info)
        return

    def check_is_valid(self):
        return self.room_info is not None

    def init_room(self, room_info):
        if not room_info:
            self.add_hide_count('WAIT_SERVER')
            return
        global_data.ui_mgr.close_ui('MatchMode')
        if self.get_show_count('WAIT_SERVER') < 0:
            self.add_show_count('WAIT_SERVER')
        else:
            self.do_show_panel()
        if self.room_info:
            log_error('Re init the same RoomUI! Should check!!!')
        self.room_info = RoomInfo()
        self.room_info.init_from_dict(room_info)
        self.init_room_widget()
        self.init_team_list(self.room_info.max_team_cnt, self.room_info.max_team_size, self.room_info.battle_type)
        self.init_judge_list()
        self.init_waiting_list()
        self.init_all_player_seat()

    def init_all_player_seat(self):
        for p_uid, player_info in six.iteritems(self.room_info.players):
            self.arrange_people_by_seat(player_info, skip_team_seat=True)

        self.update_player_in_team_seat_num()
        self.check_highlight_avatar(is_cancel=False)

    def init_room_widget(self):
        self.panel.lab_room_no.SetString(str(self.room_info.rid))
        self.panel.lab_room_name.SetString(str(self.room_info.name))
        self.panel.img_lock.setVisible(self.room_info.need_pwd)
        self.panel.lab_player_no.SetString('{0}/{1}'.format(0, int(self.room_info.max_team_cnt * self.room_info.max_team_size)))
        if self.is_room_owner(global_data.player.uid):
            self.panel.btn_start.setVisible(True)
            self.panel.lab_waiting.setVisible(False)
        else:
            self.panel.btn_start.setVisible(False)
            self.panel.lab_waiting.setVisible(True)
        if self.is_room_owner(global_data.player.uid):
            self.panel.btn_exit.btn_common.SetText(get_text_by_id(13022))

    def init_judge_list(self):
        self.panel.pnl_judgment_list.setVisible(False)
        self.panel.pnl_judgment_list.lv_name_list.setVisible(False)
        self.panel.pnl_judgment_list.lv_name_list.DeleteAllSubItem()
        self.panel.pnl_judgment_list.lab_no_player.setVisible(True)
        self.panel.btn_judgment.SetText(get_text_by_id(19305, (0, RoomUI.JUDGE_MAX_NUM)))
        self.update_be_judge_btn_visible()

    def init_waiting_list(self):
        self.panel.pnl_waiting_list.setVisible(False)
        self.panel.pnl_waiting_list.lv_name_list.setVisible(False)
        self.panel.pnl_waiting_list.lv_name_list.DeleteAllSubItem()
        self.panel.pnl_waiting_list.lab_no_player.setVisible(True)
        self.panel.btn_waiting_list.SetText(get_text_by_id(19306, (0, )))

    def init_parameters(self):
        self.is_can_refresh_room_list = True
        self.is_avatar_seated = False
        self._camp_num_lst = [0, 0, 0]

    def init_event(self):
        global_data.emgr.player_info_update_event += self._on_player_info_update
        global_data.emgr.room_player_return_from_lobby_event += self.return_from_lobby

    def init_team_list(self, team_count, team_size, battle_type):
        if team_count <= 0:
            return
        if battle_type == DEFAULT_RECRUITMENT_TID:
            team_size = 1
        self.team_list_wrapper = CommonAsynTeamList(self.panel.lv_team_list, team_count, team_size, self.on_create_team_item, self.on_create_seat_item, battle_type)
        self.team_list_wrapper.init()
        self.is_first_create_room_item = True
        if battle_type == DEFAULT_KOTH_TID:
            self.panel.nd_koth.setVisible(True)
            self.panel.lv_team_list.SetPosition('50%', '50%-55')
            self.panel.lv_team_list.SetContentSize(1238, '80%-50')
            camp_num = int(self.room_info.max_team_cnt * self.room_info.max_team_size / self.CAMP_NUM)
            for team_node in [self.panel.team_a, self.panel.team_b, self.panel.team_c]:
                team_node.lab_num.SetString('%d/%d' % (0, camp_num))

    def on_create_team_item(self):
        self.check_highlight_avatar(is_cancel=False)

    def on_create_seat_item(self, seat_ui, team_size, team_idx, team_seat_idx):
        seat_idx = team_idx * team_size + team_seat_idx
        player_data = self.room_info.get_team_seat_player_data(seat_idx)
        self.init_team_seat_ui_item(seat_ui, seat_idx, player_data)

    def init_team_seat_ui_item(self, ui_item, seat_idx, player_data=None):
        if player_data:
            p_id = player_data.get('uid', None)
            p_name = player_data.get('char_name', '')
        else:
            p_id = None
            p_name = ' '
        ui_item.lab_name.SetString(p_name)

        @ui_item.btn_seat.unique_callback()
        def OnClick(btn, touch, p_id=p_id):
            if p_id:
                if p_id == global_data.player.uid:
                    return
                self.show_player_sim_inf(ui_item, p_id, seat_idx)
            else:
                global_data.player.req_sit_down(global_data.player.uid, seat_idx)

        return

    def show_player_sim_inf(self, ui_item, p_id, seat_idx):
        import cc
        from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_ROOM_AS_JUDGE, BTN_TYPE_ROOM_KICK_OUT, BTN_TYPE_ROOM_RETURN_WAITING, BTN_TYPE_PLAYER_INF
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        if self.is_room_owner(global_data.player.uid):
            ui.custom_show_btns_func({BTN_TYPE_ROOM_AS_JUDGE: lambda uid=p_id: self.owner_move_people_to_judge(uid),
               BTN_TYPE_ROOM_KICK_OUT: lambda uid=p_id: self.owner_kick_player_out(uid),
               BTN_TYPE_ROOM_RETURN_WAITING: lambda uid=p_id: self.owner_move_people_to_waiting(uid)
               })
            if seat_idx is None or seat_idx == -1:
                show_btns = [
                 BTN_TYPE_ROOM_AS_JUDGE,
                 BTN_TYPE_ROOM_KICK_OUT]
            elif self.is_in_judge_seat(seat_idx):
                show_btns = [
                 BTN_TYPE_ROOM_RETURN_WAITING,
                 BTN_TYPE_ROOM_KICK_OUT]
            else:
                show_btns = [
                 BTN_TYPE_ROOM_RETURN_WAITING,
                 BTN_TYPE_ROOM_AS_JUDGE, BTN_TYPE_ROOM_KICK_OUT]
            if p_id == global_data.player.uid:
                if BTN_TYPE_ROOM_KICK_OUT in show_btns:
                    show_btns.remove(BTN_TYPE_ROOM_KICK_OUT)
            ui.custom_show_btn(show_btns)
        else:
            ui.custom_show_btns_func({BTN_TYPE_ROOM_RETURN_WAITING: lambda : self.move_self_to_waiting()})
            if seat_idx is None or seat_idx == -1:
                ui.custom_show_btn([])
            elif self.is_in_judge_seat(seat_idx):
                ui.custom_show_btn([])
            elif p_id == global_data.player.uid:
                ui.custom_show_btn([BTN_TYPE_ROOM_RETURN_WAITING])
            else:
                ui.custom_show_btn([])
        ui.refresh_by_uid(p_id)
        wpos = ui_item.ConvertToWorldSpacePercentage(100, 0)
        ui.set_position(wpos, anchor_point=cc.Vec2(1, 1))
        return

    def owner_kick_player_out(self, uid):
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        global_data.player.req_kick_player(uid)

    def owner_move_people_to_judge(self, uid):
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        global_data.game_mgr.show_tip(get_text_by_id(18169))
        return
        avail_seat = self.room_info.get_available_judge_seat()
        if not avail_seat:
            global_data.game_mgr.show_tip(get_text_by_id(19307))
        else:
            global_data.player.req_sit_down(uid, avail_seat)

    def owner_move_people_to_waiting(self, uid):
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        global_data.player.req_leave_seat(uid)

    def move_self_to_waiting(self):
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        global_data.player.req_leave_seat(global_data.player.uid)

    def on_finalize_panel(self):
        if self.team_list_wrapper:
            self.team_list_wrapper.destroy()
            self.team_list_wrapper = None
        self.set_hide_effect()
        return

    def update_widget(self):
        from logic.gutils import template_utils

        def close(*args):
            self.on_click_close_btn()

        template_utils.init_common_pnl_title(self.panel.pnl_title, '', close)

    def on_click_close_btn(self):
        self.return_to_lobby()

    def return_to_lobby(self):
        self.set_hide_effect()
        self.add_hide_count('ToLobby')
        global_data.emgr.room_player_return_to_lobby_event.emit()

    def return_from_lobby(self):
        self.set_appear_effect()
        self.add_show_count('ToLobby')

    def switch_show_waiting_list(self, *args):
        is_vis = self.panel.pnl_waiting_list.isVisible()
        self.set_waiting_list_vis(not is_vis)

    def switch_show_judge_list(self, *args):
        is_vis = self.panel.pnl_judgment_list.isVisible()
        self.set_judge_list_vis(not is_vis)

    def on_click_list_bg(self, *args):
        self.set_waiting_list_vis(False)
        self.set_judge_list_vis(False)

    def req_to_be_waiting(self):
        seat_idx = self.room_info.get_player_seat_idx(global_data.player.uid)
        if not self.is_in_waiting_seat(seat_idx):
            global_data.player.req_leave_seat(global_data.player.uid)

    def on_click_waiting_list(self, *args):
        self.req_to_be_waiting()

    def on_click_waiting_btn(self, *args):
        self.req_to_be_waiting()

    def req_to_be_judege(self):
        global_data.game_mgr.show_tip(get_text_by_id(18169))
        return
        uid = global_data.player.uid
        old_seat_idx = self.room_info.get_player_seat_idx(uid)
        if self.is_room_owner(uid):
            if not self.is_in_judge_seat(old_seat_idx):
                av_seat = self.room_info.get_available_judge_seat()
                if av_seat:
                    global_data.player.req_sit_down(uid, av_seat)
                else:
                    global_data.game_mgr.show_tip(get_text_by_id(19307))

    def on_click_judge_list(self, *args):
        self.req_to_be_judege()

    def on_click_judge_btn(self, *args):
        self.req_to_be_judege()

    def on_click_exit_btn(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        if self.is_room_owner(global_data.player.uid):

            def confirm_callback():
                global_data.player.req_dissolve_room()
                global_data.ui_mgr.close_ui(self.__class__.__name__)

            SecondConfirmDlg2().confirm(content=get_text_by_id(19308), confirm_callback=confirm_callback)
        else:

            def confirm_callback():
                global_data.player.req_leave_room()
                global_data.ui_mgr.close_ui(self.__class__.__name__)

            SecondConfirmDlg2().confirm(content=get_text_by_id(19309), confirm_callback=confirm_callback)

    def on_click_start_btn(self, *args):
        if self.is_room_owner(global_data.player.uid):
            global_data.player.req_start()

    def on_click_share_btn(self, *args):
        if self.is_room_owner(global_data.player.uid):
            global_data.player.req_share(self.room_info)

    def is_room_owner(self, uid):
        return self.room_info.creator == uid

    def show_player_by_data(self, player_data):
        pass

    def get_team_seat_ui_item_by_idx(self, seat_idx):
        team_idx = seat_idx // self.room_info.max_team_size
        seat_offset = seat_idx - team_idx * self.room_info.max_team_size
        return self.team_list_wrapper.get_team_seat_ui_item_by_idx(team_idx, seat_offset)

    def add_player_to_waiting_list(self, player_info):
        new_ui_item = self.panel.pnl_waiting_list.lv_name_list.AddTemplateItem()
        self.init_player_list_ui_item(new_ui_item, player_info)
        self.update_waiting_list_num()

    def add_player_to_judge_list(self, player_info):
        new_ui_item = self.panel.pnl_judgment_list.lv_name_list.AddTemplateItem()
        self.init_player_list_ui_item(new_ui_item, player_info)
        self.update_judge_list_num()

    def update_waiting_list_num(self):
        waiting_person = self.panel.pnl_waiting_list.lv_name_list.GetItemCount()
        self.panel.btn_waiting_list.SetText(get_text_by_id(19306, (waiting_person,)))
        if waiting_person <= 0:
            self.panel.pnl_waiting_list.lv_name_list.setVisible(False)
            self.panel.pnl_waiting_list.lab_no_player.setVisible(True)
        else:
            self.panel.pnl_waiting_list.lv_name_list.setVisible(True)
            self.panel.pnl_waiting_list.lab_no_player.setVisible(False)

    def set_waiting_list_vis(self, vis):
        self.panel.pnl_waiting_list.setVisible(vis)
        self.panel.layer_list_bg.setVisible(vis)

    def set_judge_list_vis(self, vis):
        self.panel.pnl_judgment_list.setVisible(vis)
        self.panel.layer_list_bg.setVisible(vis)

    def remove_player_from_waiting_list(self, uid):
        self.panel.pnl_waiting_list.lv_name_list.DeleteItemByTag(uid)
        self.update_waiting_list_num()

    def remove_player_from_judge_list(self, uid):
        self.panel.pnl_judgment_list.lv_name_list.DeleteItemByTag(uid)
        self.update_judge_list_num()

    def update_judge_list_num(self):
        judge_person = self.panel.pnl_judgment_list.lv_name_list.GetItemCount()
        self.panel.btn_judgment.SetText(get_text_by_id(19305, (judge_person, RoomUI.JUDGE_MAX_NUM)))
        if judge_person <= 0:
            self.panel.pnl_judgment_list.lv_name_list.setVisible(False)
            self.panel.pnl_judgment_list.lab_no_player.setVisible(True)
        else:
            self.panel.pnl_judgment_list.lv_name_list.setVisible(True)
            self.panel.pnl_judgment_list.lab_no_player.setVisible(False)
        self.update_be_judge_btn_visible()

    def update_be_judge_btn_visible(self):
        judge_person = self.panel.pnl_judgment_list.lv_name_list.GetItemCount()
        self.panel.btn_be_judge.setVisible(False)
        if self.is_room_owner(global_data.player.uid):
            if not is_in_judge_seat(self.room_info.get_player_seat_idx(global_data.player.uid)):
                if judge_person < self.JUDGE_MAX_NUM:
                    self.panel.btn_be_judge.setVisible(True)

    def init_player_list_ui_item(self, ui_item, player_info):
        uid = player_info.get('uid')
        ui_item.lab_name.SetString(player_info.get('char_name', ''))
        ui_item.setTag(uid)

        @ui_item.btn.unique_callback()
        def OnClick(btn, touch):
            if uid == global_data.player.uid:
                return
            self.show_player_sim_inf(ui_item, uid, self.room_info.get_player_seat_idx(uid))

    def is_in_judge_seat(self, seat_idx):
        from logic.gcommon.const import OB_GROUP_ID_START, OB_SIT_INDEX_END
        return OB_GROUP_ID_START <= seat_idx <= OB_SIT_INDEX_END

    def is_in_waiting_seat(self, seat_idx):
        if seat_idx is None or seat_idx == -1:
            return True
        else:
            return False
            return

    def add_player_to_team_seat(self, seat_idx, player_data):
        if seat_idx == -1 or self.is_in_judge_seat(seat_idx):
            log_error('Try to add player to team seat, while player not in there seat!', seat_idx, player_data)
            return
        seat_ui = self.get_team_seat_ui_item_by_idx(seat_idx)
        if seat_ui:
            self.init_team_seat_ui_item(seat_ui, seat_idx, player_data)
            self.player_cur_seat_ui = seat_ui

    def remove_player_from_team_seat(self, seat_idx, uid):
        if seat_idx == -1 or self.is_in_judge_seat(seat_idx):
            log_error('Try to remove player from team seat, while player not in there seat!', seat_idx, uid)
            return
        else:
            seat_ui = self.get_team_seat_ui_item_by_idx(seat_idx)
            if seat_ui:
                self.init_team_seat_ui_item(seat_ui, seat_idx, None)
            return

    def check_highlight_avatar(self, is_cancel=False):
        from common.utils.cocos_utils import ccp, ccc4FromHex, ccc3FromHex
        seat_idx = self.room_info.get_player_seat_idx(global_data.player.uid)
        if seat_idx is None or seat_idx == -1:
            scroll = self.panel.pnl_waiting_list.lv_name_list
            ui_item = scroll.GetItemByTag(global_data.player.uid)
        elif self.is_in_judge_seat(seat_idx):
            ui_item = self.panel.pnl_judgment_list.lv_name_list.GetItemByTag(global_data.player.uid)
        else:
            ui_item = self.get_team_seat_ui_item_by_idx(seat_idx)
            if ui_item:
                ui_item.img_self.setVisible(not is_cancel)
        if ui_item:
            if is_cancel:
                ui_item.lab_name.SetColor('#SW')
            else:
                ui_item.lab_name.SetColor('#SG')
        return

    def do_show_panel(self):
        super(RoomUI, self).do_show_panel()
        self.set_appear_effect()

    def do_hide_panel(self):
        super(RoomUI, self).do_hide_panel()
        self.set_hide_effect()

    def set_appear_effect(self):
        self._has_set_appear_effect = True
        self.hide_main_ui()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def set_hide_effect(self):
        if self._has_set_appear_effect:
            self._has_set_appear_effect = False
            self.show_main_ui()
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def on_player_leave_room(self, uid):
        if not self.check_is_valid():
            return
        player_old_seat = self.room_info.get_player_seat_idx(uid)
        self.on_player_leave_old_seat(uid, player_old_seat)
        self.room_info.player_leave_room(uid)
        self.update_player_in_team_seat_num()
        if uid == global_data.player.uid:
            self.close()

    def on_player_enter_room(self, player_data):
        if not self.check_is_valid():
            return
        uid = player_data.get('uid')
        if not uid:
            return
        self.room_info.player_enter_room(uid, player_data)
        self.on_player_sit_down(uid, player_data.get('seat_index'))

    def on_player_sit_down(self, uid, seat_idx):
        if not self.check_is_valid():
            return
        player_old_seat = self.room_info.get_player_seat_idx(uid)
        self.on_player_leave_old_seat(uid, player_old_seat)
        self.check_highlight_avatar(is_cancel=True)
        self.room_info.on_player_seat_down(uid, seat_idx)
        self.arrange_people_by_seat(self.room_info.get_player_data(uid))
        self.check_highlight_avatar(is_cancel=False)
        self.update_player_in_team_seat_num()
        self.update_be_judge_btn_visible()
        if not self.is_avatar_seated:
            if uid == global_data.player.uid:
                self.is_avatar_seated = True
                if self.is_in_judge_seat(seat_idx) or self.is_in_waiting_seat(seat_idx):
                    return
                team_idx = seat_idx // self.room_info.max_team_size
                self.team_list_wrapper.load_team_ui_item_by_idx(team_idx)
                self.panel.lv_team_list.LocatePosByItem(team_idx, 0.3)

    def on_player_leave_old_seat(self, uid, seat_idx):
        if not self.check_is_valid():
            return
        else:
            if not uid:
                return
            if seat_idx is None or seat_idx == -1:
                self.remove_player_from_waiting_list(uid)
            elif self.is_in_judge_seat(seat_idx):
                self.remove_player_from_judge_list(uid)
            else:
                self.remove_player_from_team_seat(seat_idx, uid)
                self.update_camp_num(seat_idx, True)
            return

    def arrange_people_by_seat(self, player_data, skip_team_seat=False):
        if not self.check_is_valid():
            return
        else:
            if not player_data:
                return
            seat_idx = player_data.get('seat_index')
            if seat_idx is None or seat_idx == -1:
                self.add_player_to_waiting_list(player_data)
            elif self.is_in_judge_seat(seat_idx):
                self.add_player_to_judge_list(player_data)
            else:
                self.update_camp_num(seat_idx, False)
                if not skip_team_seat:
                    self.add_player_to_team_seat(seat_idx, player_data)
            return

    def on_player_leave_to_waiting_area(self, uid):
        if not self.check_is_valid():
            return
        self.on_player_sit_down(uid, -1)

    def update_player_in_team_seat_num(self):
        not_wait_num = self.room_info.get_player_num_in_team()
        total_num = self.room_info.max_team_size * self.room_info.max_team_cnt
        self.panel.lab_player_no.SetString('{0}/{1}'.format(not_wait_num, total_num))

    def update_camp_num(self, seat_id, is_leave):
        if not self.room_info.battle_type == DEFAULT_KOTH_TID:
            return
        camp_num = int(self.room_info.max_team_cnt * self.room_info.max_team_size / self.CAMP_NUM)
        camp_nods = [self.panel.team_a, self.panel.team_b, self.panel.team_c]
        camp_idx = seat_id % 12 / self.room_info.max_team_size
        change_num = -1 if is_leave else 1
        self._camp_num_lst[camp_idx] = self._camp_num_lst[camp_idx] + change_num
        camp_nods[camp_idx].lab_num.SetString('%d/%d' % (self._camp_num_lst[camp_idx], camp_num))

    def _on_player_info_update(self, *args):
        self.update_widget()

    def update_roommate_info(self, uid, info):
        self.room_info.update_roommate_info(uid, info)
        player_seat = self.room_info.get_player_seat_idx(uid)
        self.on_player_sit_down(uid, player_seat)
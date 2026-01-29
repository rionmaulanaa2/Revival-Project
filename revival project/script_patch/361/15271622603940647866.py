# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomUINew.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_00
from .DeathRoomTeamListUI import DeathRoomTeamListUI
from .CustomRoomInfo import CustomRoomInfo
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import ITEM_NO_ROOM_POINT
from common.cfg import confmgr
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.gutils import template_utils
from logic.gcommon.common_utils.battle_utils import get_mode_name
import cc
from logic.gcommon import time_utility
from logic.gcommon import const
from logic.gutils.role_head_utils import init_role_head_auto, set_gray, set_role_dan
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_ROOM_KICK_OUT, BTN_TYPE_TRANSFER_OWNERSHIP, BTN_TYPE_REPORT, BTN_TYPE_CHANGE_SEAT
import time
from logic.gcommon.const import BATTLE_STATE_FIGHTING, BATTLE_STATE_INROOM
from logic.gcommon.common_utils.battle_utils import get_room_layout_by_battle_id
from logic.gutils.custom_room_utils import get_room_layout_cls, RANDOM_MAP_TEXT_ID
from logic.gutils.online_state_utils import is_not_online
from logic.comsys.setting_ui.SettingWidget.CustomBattleSettingWidget import CustomBattleSettingWidget
from logic.gcommon.common_const.custom_battle_const import CUSTOM_SETTINGS_MEMORY_ACHI_NAME, CUSTOM_SETTINGS_MEMORY_ROOM_GUIDE, CUSTOM_SETTINGS_ROOM_GUIDE_TXT, CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE, CUSTOM_SETTINGS_TIP_TXT_SAVE
DEFAULT_CLIP_PATH = 'gui/ui_res_2/room/bar_role_nopick.png'
from common.const import uiconst

class RoomUINew(BasePanel):
    PANEL_CONFIG_NAME = 'room/room_main_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_00
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'btn_dissolve.btn_major.OnClick': 'on_click_dissolve_btn',
       'btn_exit.btn_major.OnClick': 'on_click_exit_btn',
       'btn_start.btn_major.OnClick': 'on_click_start_btn',
       'btn_tips.OnClick': 'on_click_tips_btn',
       'btn_time_1.OnClick': 'on_click_time1_btn',
       'btn_time_2.OnClick': 'on_click_time2_btn',
       'btn_friends.OnClick': 'on_click_invite_btn',
       'temp_choose.btn.OnClick': 'on_click_enbale_change_seat',
       'temp_lock.btn.OnClick': 'on_click_enable_leave_room',
       'temp_lock_voice.btn.OnClick': 'on_click_disable_chat',
       'btn_help.OnClick': 'on_click_help_btn',
       'nd_content.nd_info.btn_setting.OnClick': 'on_click_setting_btn',
       'nd_content.temp_setting.pnl_create_custom.btn_close.OnClick': 'on_click_setting_close_btn',
       'nd_content.temp_setting.pnl_create_custom.temp_btn_1.btn_common_big.OnClick': 'on_click_setting_reset_btn',
       'nd_content.temp_setting.pnl_create_custom.temp_btn_2.btn_common_big.OnClick': 'on_click_setting_save_btn'
       }
    ITEM_NO_ROOM_POINT_IN_MALL = '50302026'
    DEFAULT_MAP_ID = '11'
    REFRESH_ROOMMATE_STATE_TAG = 1

    def on_init_panel(self, room_info):
        self._has_set_appear_effect = False
        self._dissolve_info = {}
        self._uid2change_seat_timestamp = {}
        self._curr_map_id = room_info.get('map_id', -1)
        self._curr_battle_type = -1
        self._mode_options = []
        self.team_layout = None
        self.init_event()
        self.room_info = None
        self._roommate_state = None
        self.room_invite_widget = None
        self.in_adjust_seat_state = False
        self.need_guide_room_setting = True
        self.init_room(room_info)
        self.process_event(True)
        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.stop_refresh_roommate_online_state()
        self.show_main_ui()
        self.set_hide_effect()
        if self.room_invite_widget:
            self.room_invite_widget.destroy()
            self.room_invite_widget = None
        return

    def init_room(self, room_info):
        if not room_info:
            self.add_hide_count('WAIT_SERVER')
            return
        else:
            global_data.ui_mgr.close_ui('MatchMode')
            if self.get_show_count('WAIT_SERVER') < 0:
                self.add_show_count('WAIT_SERVER')
            else:
                self.do_show_panel()
            if self.room_info:
                log_error('Re init the same RoomUINew! Should check!!!')
            self._is_week_competition = room_info.get('is_week_competition', False)
            self.room_info = CustomRoomInfo()
            self._curr_map_id = room_info.get('map_id', -1)
            self.room_info.init_from_dict(room_info)
            self.init_widget()
            mode = room_info.get('battle_type', None)
            if not mode:
                return
            self.set_mode_layout(mode)
            self.update_player_num()
            self.start_refresh_roommate_online_state()
            return

    def set_mode_layout(self, mode):
        if self.team_layout != None:
            self.team_layout.hide()
        layout_info = get_room_layout_by_battle_id(mode)
        template_name = layout_info['ui_template']
        widget_cls = get_room_layout_cls(layout_info['ui_class'])
        panel = global_data.uisystem.load_template_create(template_name, parent=self.panel.temp_seat, name=str(mode))
        widget = widget_cls(self, panel)
        self.team_layout = widget
        widget.init_room_team_list_ui(self.room_info)
        widget.panel.setVisible(True)
        return

    def init_widget(self):
        self.panel.nd_bg.setVisible(True)
        if not isinstance(self.room_info.name, str):
            self.room_info.name = ''
        self.panel.lab_name.SetString(self.room_info.name)
        self.panel.img_lock.setVisible(self.room_info.need_pwd)
        self.panel.lab_room_num.SetString(str(self.room_info.room_id))
        self.update_widget()
        if not self.room_info:
            return
        if global_data.player.uid == self.room_info.creator:
            is_creator = True if 1 else False
            is_competition = self.is_competition(self.room_info.battle_type)
            self.panel.btn_tips.setVisible(not is_competition)
            self.panel.nd_btn_owner.setVisible(is_creator)
            self.panel.nd_btn_player.setVisible(not is_creator)
            self.panel.nd_owner.setVisible(True)
            self.panel.nd_player.setVisible(True)
            self.panel.nd_owner.btn_map_choose.setVisible(is_creator)
            self.panel.nd_player.img_map_bar.setVisible(not is_creator)
            self.panel.nd_owner.btn_mode_choose.setVisible(is_creator)
            self.panel.nd_player.img_mode_bar.setVisible(not is_creator)
            self.panel.nd_player.img_mode_bar.lab_mode.SetString(get_mode_name(self.room_info.battle_type))
            self.panel.lab_tips.setVisible(False)
            self.panel.nd_judgement_seat.setVisible(True)
            self.init_judgement_seat_list(self.panel.nd_judgement_seat.judgement_list.list_judgement_seat)
            self.update_judgement_seat_list()
            battle_config = confmgr.get('battle_config')
            map_id = battle_config[str(self.room_info.battle_type)].get('iMapID', '')
            map_config = confmgr.get('map_config')
            born_list = map_config[map_id].get('bornList', [])
            born_list or self.panel.nd_player.img_map_bar.setVisible(False)
        self.panel.lab_time_1.setVisible(False)
        self.panel.lab_time_2.setVisible(False)
        self.panel.lab_battle.SetString(get_text_by_id(862028))
        self.panel.lab_waite.SetString(get_text_by_id(862027))
        self.init_room_invite_widget()
        self.init_custom_room_data()
        if global_data.player.uid == self.room_info.creator:
            self.init_mode_list()
        self.init_price_list()
        self.req_dissolve_timestamp()
        self.on_change_map_area(self.room_info.room_born_idx)
        self.init_can_change_seat_widget()
        self.init_can_leave_room_widget()
        self.init_can_chat_room_widget()
        self.init_rejoin_spectate_btn()
        self.init_main_chat_input_box()
        self.need_guide_room_setting = global_data.achi_mgr.get_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ROOM_GUIDE, True)
        self._customed_battle_dict = self.room_info.customed_battle_dict
        self.init_custom_setting_widget()
        self.enable_custom_setting_panel(is_creator)
        if self.room_info.is_customed_battle:
            self.on_click_setting_btn()

    def init_room_invite_widget(self):
        from logic.comsys.room.RoomInviteUINew import RoomInviteUINew
        self.room_invite_widget = RoomInviteUINew(self, self.panel)
        self.room_invite_widget.hide()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_lobby_bag_item_changed_event': self.init_price_list,
           'update_dissolve_timestamp': self.init_dissolve_count_down
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_price_list(self):
        if self.room_info is not None and self.is_competition(self.room_info.battle_type):
            self.panel.nd_top.list_money.setVisible(False)
            return
        else:
            self.list_money = self.panel.nd_top.list_money
            self.list_money.DeleteAllSubItem()
            self.list_money.SetInitCount(1)
            room_point_num = global_data.player.get_item_num_by_no(ITEM_NO_ROOM_POINT)
            ui_item = self.list_money.GetItem(0)
            ui_item.txt_price.SetString(str(room_point_num))
            if self.room_info is not None and global_data.player.uid == self.room_info.creator:
                self.init_start_btn(self._curr_battle_type)

            @ui_item.btn_add.unique_callback()
            def OnClick(btn, touch):
                GroceriesBuyConfirmUI(goods_id=RoomUINew.ITEM_NO_ROOM_POINT_IN_MALL)

            return

    def init_custom_room_data(self):
        battle_config = confmgr.get('battle_config')
        cur_team_num = battle_config.get(str(self.room_info.battle_type), {}).get('cTeamNum', '')
        cur_play_type = battle_config.get(str(self.room_info.battle_type), {}).get('play_type', '')
        is_competition = self.is_competition(self.room_info.battle_type)
        self._supported_mode = []
        if not is_competition:
            for battle_type, mode_conf in six.iteritems(battle_config):
                if mode_conf.get('bSupportCustom', 0) == 2 and not self.is_competition(battle_type):
                    self._supported_mode.append(battle_type)

        else:
            for battle_type, mode_conf in six.iteritems(battle_config):
                if mode_conf.get('bSupportCustom', 0) == 2 and mode_conf['play_type'] == cur_play_type and mode_conf['cTeamNum'] == cur_team_num and self.is_competition(battle_type):
                    self._supported_mode.append(battle_type)

    def init_mode_list(self):
        battle_config = confmgr.get('battle_config')
        mode_options = [ {'name': get_mode_name(mode),'battle_type': mode,'map_id': battle_config[mode].get('iMapID', '')} for mode in self._supported_mode ]
        self._mode_options = [ {'name': get_mode_name(mode),'battle_type': mode,'map_id': battle_config[mode].get('iMapID', '')} for mode in self._supported_mode ]

        @self.panel.btn_mode_choose.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.mode_list.isVisible():
                self.panel.mode_list.setVisible(True)
                self.panel.btn_mode_choose.img_icon.setRotation(180)
            else:
                self.panel.mode_list.setVisible(False)
                self.panel.btn_mode_choose.img_icon.setRotation(0)

        def call_back(index):
            option = mode_options[index]
            battle_type = option['battle_type']
            if self._curr_battle_type != int(battle_type):
                global_data.player.req_change_room_battle_type({'battle_type': battle_type})
            self.panel.btn_mode_choose.img_icon.setRotation(0)
            self.panel.mode_list.setVisible(False)

        template_utils.init_common_choose_list_2(self.panel.mode_list, self.panel.btn_mode_choose.img_icon, mode_options, call_back, max_height=354)
        self.change_mode_cb(self.room_info.battle_type)

    def change_mode_cb(self, battle_type):
        for option in self._mode_options:
            if option['battle_type'] == str(battle_type):
                self._curr_battle_type = battle_type
                self.init_map_list(option['map_id'])
                self._curr_map_id = option['map_id']
                self.panel.btn_mode_choose.SetText(option['name'])
                self.panel.mode_list.setVisible(False)
                self.panel.btn_mode_choose.img_icon.setRotation(0)
                self.init_start_btn(battle_type)
                break

        self.panel.nd_player.img_mode_bar.lab_mode.SetString(get_mode_name(battle_type))
        if global_data.player.uid == self.room_info.creator and self.is_competition(battle_type):
            battle_config = confmgr.get('battle_config')
            map_id = battle_config.get(str(battle_type), {}).get('iMapID', '')
            self._curr_battle_type = battle_type
            self.init_map_list(map_id)
            self._curr_map_id = map_id
            self.init_start_btn(battle_type)

    def init_map_list(self, map_id):
        map_config = confmgr.get('map_config')
        born_list = map_config[map_id].get('bornList', [])
        if not born_list:
            self.panel.btn_map_choose.setVisible(False)
            self.panel.map_list.setVisible(False)
            self._cur_born_idx = None
            self._cur_env_name = None
        else:
            self.panel.btn_map_choose.setVisible(True)
            self.panel.map_list.setVisible(False)
            born_option = []
            if len(born_list) > 1:
                born_option.append({'name': get_text_by_id(RANDOM_MAP_TEXT_ID),
                   'born_idx': -1,
                   'env_name': None
                   })
            for born_idx, born_type in enumerate(born_list):
                name = get_text_local_content(born_type)
                born_option.append({'name': name,
                   'born_idx': born_idx,
                   'env_name': None
                   })

            @self.panel.btn_map_choose.unique_callback()
            def OnClick(btn, touch):
                if not self.panel.map_list.isVisible():
                    self.panel.map_list.setVisible(True)
                    self.panel.btn_map_choose.img_icon.setRotation(180)
                else:
                    self.panel.map_list.setVisible(False)
                    self.panel.btn_map_choose.img_icon.setRotation(0)

            def call_back(index):
                option = born_option[index]
                self._cur_born_idx = option['born_idx']
                self._cur_env_name = option['env_name']
                global_data.player.req_change_map_area({'born_idx': self._cur_born_idx,
                   'env_name': self._cur_env_name
                   })
                self.panel.btn_map_choose.SetText(option['name'])
                self.panel.map_list.setVisible(False)
                self.panel.btn_map_choose.img_icon.setRotation(0)

            template_utils.init_common_choose_list_2(self.panel.map_list, self.panel.btn_map_choose.img_icon, born_option, call_back, max_height=354)
            call_back(0)
        return

    def init_start_btn(self, battle_type):
        if battle_type == -1:
            return
        else:
            if self.room_info is None:
                return
            if self.room_info.room_battled_times > 0 and not self.is_competition(battle_type):
                battle_config = confmgr.get('battle_config')
                battle_info = battle_config.get(str(battle_type))
                if battle_info is None:
                    return
                needed_points = int(battle_info.get('iRoomPoints', 0))
                self.panel.img_cost.setVisible(True)
                self.panel.lab_num.SetString(str(needed_points))
                if global_data.player.has_enough_item(ITEM_NO_ROOM_POINT, needed_points) or needed_points == 0:
                    self.panel.lab_num.SetColor('#SK')
                else:
                    self.panel.lab_num.SetColor('#SR')
                self.panel.btn_start.btn_major.SetTextOffset({'x': '50%30','y': '50%'})
            else:
                self.panel.img_cost.setVisible(False)
                self.panel.btn_start.btn_major.SetTextOffset({'x': '50%','y': '50%'})
            return

    def req_dissolve_timestamp(self):
        global_data.player.req_dissolve_timestamp()

    def init_dissolve_count_down(self, dissolve_info):
        self._dissolve_info = dissolve_info
        if not dissolve_info:
            return
        else:
            dissolve_timestamp = dissolve_info.get('dissolve_timestamp', 0)
            room_is_in_battle = dissolve_info.get('room_battle_state', False)
            if self.room_info is not None and not self.is_competition(self.room_info.battle_type):
                if not room_is_in_battle:
                    exit_time = dissolve_timestamp - time_utility.get_server_time()

                    def update_time(passed_time):
                        left_time = int(exit_time - passed_time)
                        left_time = time_utility.get_delta_time_str(left_time)
                        if global_data.player.uid == self.room_info.creator:
                            self.panel.lab_time_1.SetString(left_time)
                            self.panel.lab_time_1.setVisible(True)
                        else:
                            self.panel.lab_time_2.SetString(left_time)
                            self.panel.lab_time_2.setVisible(True)

                    if global_data.player.uid == self.room_info.creator:
                        self.panel.lab_time_1.StopTimerAction()
                        self.panel.lab_time_1.TimerAction(update_time, exit_time, interval=1.0)
                    else:
                        self.panel.lab_time_2.StopTimerAction()
                        self.panel.lab_time_2.TimerAction(update_time, exit_time, interval=1.0)
                else:
                    self.panel.lab_time_1.setVisible(False)
                    self.panel.lab_time_2.setVisible(False)
            if room_is_in_battle:
                self.panel.lab_battle.setVisible(True)
                self.panel.lab_battle.SetString(get_text_by_id(862028))
                self.panel.lab_waite.setVisible(False)
                if global_data.player.uid == self.room_info.creator:
                    self.panel.btn_start.btn_major.SetEnable(False)
                    self.panel.btn_start.btn_major.SetText(get_text_by_id(862028))
                    self.panel.img_cost.setVisible(False)
                    self.panel.btn_start.btn_major.SetTextOffset({'x': '50%','y': '50%'})
            else:
                self.panel.lab_battle.setVisible(False)
                self.panel.lab_waite.setVisible(True)
                self.panel.lab_waite.SetString(get_text_by_id(862027))
                if global_data.player.uid == self.room_info.creator:
                    self.panel.btn_start.btn_major.SetEnable(True)
                    self.panel.btn_start.btn_major.SetText(get_text_by_id(80576))
                    self.init_start_btn(self._curr_battle_type)
            return

    def init_can_change_seat_widget(self):
        if self.room_info:
            show_can_change_seat_widget = self.is_competition(self.room_info.battle_type)
            show_choose = show_can_change_seat_widget and self.room_info.can_change_seat
            self.panel.temp_choose.setVisible(show_can_change_seat_widget)
            self.panel.temp_choose.choose.setVisible(show_choose)

    def init_can_leave_room_widget(self):
        if self.room_info:
            show_can_leave_room_widget = self.is_competition_room()
            show_choose = show_can_leave_room_widget and not self.room_info.can_leave_room
            self.panel.temp_lock.setVisible(show_can_leave_room_widget)
            self.panel.temp_lock.choose.setVisible(show_choose)

    def init_can_chat_room_widget(self):
        if self.room_info:
            show_lock_voice_widget = self.is_competition_room() and self.room_info.creator == global_data.player.uid
            is_lock = show_lock_voice_widget and not self.room_info.can_chat_in_room
            self.panel.temp_lock_voice.setVisible(show_lock_voice_widget)
            self.panel.temp_lock_voice.choose.setVisible(is_lock)

    def init_rejoin_spectate_btn(self):
        if not self.room_info:
            self.panel.btn_help.setVisible(False)
            return
        if not self.is_competition(self.room_info.battle_type):
            self.panel.btn_help.setVisible(False)
            return
        if global_data.player.uid == self.room_info.creator or self.is_judgement():
            self.panel.btn_help.setVisible(True)
        else:
            self.panel.btn_help.setVisible(False)

    def init_main_chat_input_box(self):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if self.is_judgement():
            ui and ui.adjust_text_input_box_length()
        else:
            ui and ui.reset_text_input_box_length()

    def init_judgement_seat_list(self, judge_list_ui):
        self.update_judgement_btn()

        @self.panel.nd_judgement_seat.btn_judgement_seat.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.judgement_list.isVisible():
                self.panel.judgement_list.setVisible(True)
                self.panel.btn_judgement_seat.img_judgement_icon.setRotation(180)
            else:
                self.panel.judgement_list.setVisible(False)
                self.panel.btn_judgement_seat.img_judgement_icon.setRotation(0)

        judge_list_ui.SetNumPerUnit(2, False)
        judge_list_ui.SetInitCount(const.OB_GROUP_ID_END - const.OB_GROUP_ID_START + 1)
        for seat_idx, judge_seat in enumerate(judge_list_ui.GetAllItem()):
            self.create_judge_seat_ui(judge_seat, seat_idx + const.OB_GROUP_ID_START)

        self.panel.nd_judgement_seat.judgement_list.setVisible(False)

    def update_judgement_seat_list(self, *args):
        judge_list_ui = self.panel.nd_judgement_seat.judgement_list.list_judgement_seat
        if not self.room_info:
            return
        else:
            creator_id = self.room_info.creator
            for seat_idx, ui_item in enumerate(judge_list_ui.GetAllItem()):
                if not ui_item:
                    continue
                real_seat_idx = seat_idx + const.OB_GROUP_ID_START
                judge_info = self.room_info.get_team_seat_player_data(real_seat_idx) or {}
                judge_id = judge_info.get('uid', None)
                ui_item.nd_empty.setVisible(self.is_judgement() and judge_id != global_data.player.uid and judge_id != creator_id and self.is_competition_room())
                ui_item.nd_empty.lab_become_judge.setVisible(self.is_judgement() and not judge_id and self.is_competition_room())

            return

    def create_judge_seat_ui(self, seat_ui, seat_idx):
        judge_info = self.room_info.get_team_seat_player_data(seat_idx)
        self.populate_judge_seat_ui(seat_ui, seat_idx, judge_info)

    def get_judge_seat_ui_by_index(self, seat_index):
        return self.panel.judgement_list.list_judgement_seat.GetItem(seat_index - const.OB_GROUP_ID_START)

    def get_judge_seat_ui_by_player_uid(self, uid):
        player_info = self.room_info.get_player_data(uid)
        if player_info is None:
            return
        else:
            seat_index = player_info.get('seat_index', None)
            if seat_index is None or not const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
                return
            return self.get_judge_seat_ui_by_index(seat_index)

    def populate_judge_seat_ui(self, seat_ui, seat_idx, judge_data=None):
        if seat_ui is None:
            return
        else:
            if judge_data:
                judge_id = judge_data.get('uid', None)
                judge_name = judge_data.get('char_name', '')
                judge_name_in_room = judge_data.get('char_name_in_room', judge_name)
                battle_state = judge_data.get('battle_state', 0)
                seat_ui.temp_head.nd_battle.setVisible(battle_state == const.BATTLE_STATE_FIGHTING)
                if judge_id == global_data.player.uid:
                    seat_ui.temp_head.nd_battle.setVisible(False)
                seat_ui.img_bar.setVisible(True)
                seat_ui.nd_info.setVisible(True)
                seat_ui.nd_empty.setVisible(self.is_judgement() and judge_id != global_data.player.uid and self.is_competition_room())
                seat_ui.nd_info.lab_name.setVisible(True)
                seat_ui.nd_info.lab_name.SetString(str(judge_name_in_room))
                seat_ui.temp_head.setVisible(True)
                seat_ui.temp_head.img_role_bar.setVisible(True)
                seat_ui.temp_head.frame_head.img_head.setVisible(True)
                seat_ui.temp_head.img_head_frame.setVisible(True)
                seat_ui.temp_head.nd_scale.nd_vx.setVisible(True)
                seat_ui.temp_head.img_head.setVisible(True)
                seat_ui.temp_head.img_empty.setVisible(False)
                init_role_head_auto(seat_ui.temp_head, judge_id, 0, None, head_frame=judge_data.get('head_frame'), head_photo=judge_data.get('head_photo'))
                if global_data.player.uid == judge_id:
                    seat_ui.lab_name.SetColor('#DB')
                else:
                    seat_ui.lab_name.SetColor('#SW')
            else:
                judge_id = None
                judge_name = ''
                seat_ui.img_bar.setVisible(True)
                set_gray(seat_ui.temp_head, False)
                seat_ui.temp_head.setVisible(True)
                seat_ui.temp_head.frame_head.img_head.setVisible(False)
                seat_ui.temp_head.img_head_frame.setVisible(False)
                seat_ui.temp_head.img_role_bar.setVisible(True)
                seat_ui.temp_head.nd_scale.nd_vx.setVisible(False)
                seat_ui.temp_head.nd_battle.setVisible(False)
                seat_ui.temp_head.img_role_bar.SetDisplayFrameByPath('', DEFAULT_CLIP_PATH)
                seat_ui.temp_head.img_head.setVisible(False)
                seat_ui.temp_head.img_empty.setVisible(True)
                seat_ui.nd_info.setVisible(False)
                seat_ui.nd_info.lab_name.SetString(judge_name)
                seat_ui.nd_info.lab_name.setVisible(False)
                seat_ui.nd_empty.setVisible(self.is_judgement() and self.is_competition_room())
                seat_ui.nd_empty.lab_become_judge.setVisible(self.is_judgement() and self.is_competition_room())

            @seat_ui.temp_head.unique_callback()
            def OnClick(btn, touch, judge_id=judge_id):
                if judge_id:
                    self.show_player_brief_info(seat_ui, judge_id, seat_idx)
                elif not self.is_competition_room():
                    global_data.player.req_sit_down(global_data.player.uid, seat_idx)

            if self._is_week_competition:
                seat_ui.nd_empty.btn_add.setVisible(False)
                seat_ui.nd_empty.img_become_judge.setVisible(False)

            @seat_ui.nd_empty.btn_add.unique_callback()
            def OnClick(btn, touch, judge_id=judge_id, seat_idx=seat_idx):
                if self.is_competition_room():
                    judge_id = judge_id or -1 if 1 else judge_id
                    self.judgement_before_adjust_seat(judge_id, seat_idx)
                    self.in_adjust_seat_state = True

            return

    def is_in_judge_seat(self, seat_idx):
        return seat_idx is not None and const.OB_GROUP_ID_START <= seat_idx <= const.OB_SIT_INDEX_END

    def update_judgement_btn(self):
        curr_judge_num = len(self.room_info.uid2judge_seat)
        if self.is_competition_room():
            self.panel.nd_judgement_seat.btn_judgement_seat.SetText(get_text_by_id(19305, (curr_judge_num, const.OB_GROUP_ID_END - const.OB_GROUP_ID_START + 1)))
        else:
            self.panel.nd_judgement_seat.btn_judgement_seat.SetText(get_text_by_id(19684, (curr_judge_num, const.OB_GROUP_ID_END - const.OB_GROUP_ID_START + 1)))

    def show_player_brief_info(self, seat_ui, player_id, seat_idx):
        if player_id == global_data.player.uid:
            return
        player_info_ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        player_info_ui.del_btn(BTN_TYPE_REPORT)
        self_seat_idx = self.room_info.get_player_seat_idx(global_data.player.uid)
        if self.room_info.creator == global_data.player.uid:
            is_competition = self.is_competition(self.room_info.battle_type)
            player_info_ui.custom_show_btns_func({BTN_TYPE_ROOM_KICK_OUT: lambda uid=player_id: self.owner_kick_player_out(uid),
               BTN_TYPE_TRANSFER_OWNERSHIP: lambda uid=player_id: self.transfer_ownership(uid),
               BTN_TYPE_CHANGE_SEAT: lambda uid=player_id, seat_index=self_seat_idx: self.change_seat_with_someone(uid, seat_index)
               })
            if player_id == global_data.player.uid:
                show_btns = []
            else:
                show_btns = [
                 BTN_TYPE_ROOM_KICK_OUT]
            player_info_ui.custom_show_btn(show_btns)
        else:
            player_info_ui.custom_show_btns_func({BTN_TYPE_CHANGE_SEAT: lambda uid=player_id, seat_index=self_seat_idx: self.change_seat_with_someone(uid, seat_index)
               })
            show_btns = []
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
            if now - last_ask_timestamp < DeathRoomTeamListUI.CHANGE_SEAT_CD:
                left_seconds = int(DeathRoomTeamListUI.CHANGE_SEAT_CD - (now - last_ask_timestamp))
                global_data.game_mgr.show_tip(get_text_by_id(862021).format(left_seconds))
                return
            self._uid2change_seat_timestamp[uid] = now
        else:
            self._uid2change_seat_timestamp[uid] = now
        global_data.player.req_change_seat_with_someone(uid, seat_index)
        return

    def refresh_judge_online_state(self, roommate_state):
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
                if seat_index is None or not const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
                    continue
                seat_ui = self.get_judge_seat_ui_by_index(seat_index)
                if not seat_ui:
                    continue
                if is_not_online(st):
                    set_gray(seat_ui.temp_head, True)
                else:
                    if self.is_waiting() and (st == const.STATE_BATTLE_FIGHT or st == const.STATE_BATTLE):
                        set_gray(seat_ui.temp_head, True)
                        continue
                    set_gray(seat_ui.temp_head, False)

            return

    def judgement_before_adjust_seat(self, uid, seat_index):
        self.panel.judgement_list.setVisible(False)
        self.panel.btn_judgement_seat.img_judgement_icon.setRotation(0)
        global_data.player.judgement_before_adjust_seat(uid, seat_index)

    def judgement_on_set_char_name_in_room(self, uid, char_name_in_room):
        seat_ui = self.get_judge_seat_ui_by_player_uid(uid)
        if not seat_ui:
            return
        seat_ui.nd_info.lab_name.SetString(char_name_in_room)

    def set_judge_battle_state_by_uid(self, uid, state):
        player_info = self.room_info.get_player_data(uid)
        if not player_info:
            return
        else:
            seat_index = player_info.get('seat_index', None)
            if seat_index is None or not const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
                return
            seat_ui = self.get_judge_seat_ui_by_index(seat_index)
            if not seat_ui:
                return
            if state == BATTLE_STATE_FIGHTING:
                seat_ui.temp_head.nd_battle.setVisible(True)
            else:
                seat_ui.temp_head.nd_battle.setVisible(False)
            return

    def on_self_judegement_change(self, become_judgement):
        global_data.emgr.on_self_judgement_change.emit(become_judgement)
        ui = global_data.ui_mgr.get_ui('MainChat')
        if become_judgement:
            ui and ui.adjust_text_input_box_length()
        else:
            ui and ui.reset_text_input_box_length()
        self.init_rejoin_spectate_btn()
        if self.is_competition(self.room_info.battle_type):
            self.init_mode_list()
            battle_config = confmgr.get('battle_config')
            map_id = battle_config.get(str(self.room_info.battle_type), {}).get('iMapID', '')
            map_config = confmgr.get('map_config')
            born_list = map_config[map_id].get('bornList', [])
            if born_list:
                self.panel.nd_owner.btn_map_choose.setVisible(become_judgement)
                self.panel.nd_player.img_map_bar.setVisible(not become_judgement)
            self.panel.nd_owner.btn_mode_choose.setVisible(become_judgement)
            self.panel.nd_player.img_mode_bar.setVisible(not become_judgement)

    def on_player_enter_room(self, player_info):
        uid = player_info.get('uid', None)
        if not uid:
            return
        else:
            if self.room_info is None:
                return
            self.room_info.player_enter_room(uid, player_info)
            self.on_player_sit_down(uid, player_info.get('seat_index'))
            return

    def on_player_sit_down(self, uid, seat_index, clear_old_seat=True):
        if self.room_info is None:
            return
        else:
            old_seat_index = self.room_info.get_player_seat_idx(uid)
            if clear_old_seat:
                self.on_player_leave_old_seat(uid, old_seat_index)
            self.room_info.player_sit_down(uid, seat_index, clear_old_seat=clear_old_seat)
            if self.is_in_judge_seat(seat_index):
                self.populate_judge_seat_ui(self.get_judge_seat_ui_by_index(seat_index), seat_index, self.room_info.get_player_data(uid))
            else:
                self.team_layout.put_one_player_in_seat(self.room_info.get_player_data(uid))
            self.update_player_num()
            self.update_judgement_btn()
            if self.is_in_judge_seat(seat_index) or self.is_in_judge_seat(old_seat_index):
                self.update_judgement_seat_list()
            if global_data.player.uid == uid:
                self.on_self_judegement_change(self.is_in_judge_seat(seat_index))
            return

    def on_player_leave_old_seat(self, uid, seat_index):
        if seat_index is None:
            return
        else:
            self.remove_player_from_team_seat(seat_index, uid)
            return

    def remove_player_from_team_seat(self, seat_index, uid):
        if self.is_in_judge_seat(seat_index):
            seat_ui = self.get_judge_seat_ui_by_index(seat_index)
            self.populate_judge_seat_ui(seat_ui, seat_index, None)
        else:
            seat_ui = self.team_layout.get_seat_ui_by_index(seat_index)
            self.team_layout.populate_seat_ui(seat_ui, seat_index, None)
        return

    def on_player_leave_room(self, uid):
        if self.room_info is None:
            return
        else:
            old_seat_index = self.room_info.get_player_seat_idx(uid)
            self.on_player_leave_old_seat(uid, old_seat_index)
            self.room_info.player_leave_room(uid)
            self.update_player_num()
            self.update_judgement_btn()
            if uid == global_data.player.uid:
                self.close()
            return

    def update_player_num(self):
        curr_num = self.room_info.get_player_num_in_team()
        total_num = self.room_info.max_team_size * self.room_info.max_team_cnt
        self.panel.lab_player_num.SetString(get_text_by_id(19313, (curr_num, total_num)))

    def update_roommate_info(self, uid, info):
        target_uid = info.get('uid', None)
        if not target_uid:
            return
        else:
            self.room_info.update_roommate_info(target_uid, info)
            self.team_layout.room_info.update_roommate_info(target_uid, info)
            new_creator = info.get('new_creator', None)
            old_creator = info.get('old_creator', None)
            if new_creator and old_creator:
                self.room_info.set_creator(new_creator)
                self.team_layout.room_info.set_creator(new_creator)
                if global_data.player.uid == new_creator:
                    self.panel.nd_btn_owner.setVisible(True)
                    self.panel.nd_btn_player.setVisible(False)
                    self.panel.nd_owner.setVisible(True)
                    self.panel.nd_owner.btn_map_choose.setVisible(True)
                    self.panel.nd_owner.btn_mode_choose.setVisible(True)
                    self.panel.nd_player.setVisible(False)
                    self.init_mode_list()
                    self.enable_custom_setting_panel(True)
                    from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                    NormalConfirmUI2(content=get_text_by_id(862016))
                elif global_data.player.uid == old_creator:
                    self.panel.nd_btn_owner.setVisible(False)
                    self.panel.nd_btn_player.setVisible(True)
                    self.panel.nd_owner.setVisible(False)
                    self.panel.nd_player.setVisible(True)
                    self.panel.nd_player.img_map_bar.setVisible(True)
                    self.panel.nd_player.img_mode_bar.setVisible(True)
                    self.enable_custom_setting_panel(False)
                self.init_dissolve_count_down(self._dissolve_info)
            player_seat = self.room_info.get_player_seat_idx(target_uid)
            self.on_player_sit_down(target_uid, player_seat)
            self.team_layout.refresh_roommate_online_state(self._roommate_state)
            self.init_can_chat_room_widget()
            return

    def refresh_roommate_online_state(self, roommate_state):
        if not roommate_state:
            return
        self._roommate_state = roommate_state
        self.team_layout.refresh_roommate_online_state(roommate_state)
        self.refresh_judge_online_state(self._roommate_state)

    def start_refresh_roommate_online_state(self):
        action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.req_roommate_online_state),
         cc.DelayTime.create(10)])))
        action.setTag(RoomUINew.REFRESH_ROOMMATE_STATE_TAG)

    def stop_refresh_roommate_online_state(self):
        self.panel.stopActionByTag(RoomUINew.REFRESH_ROOMMATE_STATE_TAG)

    def req_roommate_online_state(self):
        uid_list = self.room_info.get_players_uid_list()
        if not uid_list:
            return
        global_data.player.req_roommate_online_state(uid_list)

    def on_other_player_quit_battle_state(self, uid, state):
        self.room_info.update_player_battle_state(uid, state)
        self.team_layout.on_other_player_quit_battle_state(uid, state)
        self.set_judge_battle_state_by_uid(uid, state)

    def set_all_player_battle_state(self):
        self.room_info.set_all_player_battle_state()
        self.team_layout.set_all_player_battle_state()
        self.set_judge_online_state()

    def set_judge_online_state(self, state=BATTLE_STATE_INROOM):
        for player_id, player_info in six.iteritems(self.room_info.players):
            seat_index = player_info.get('seat_index', None)
            if seat_index is None or not const.OB_GROUP_ID_START <= seat_index <= const.OB_SIT_INDEX_END:
                continue
            seat_ui = self.get_judge_seat_ui_by_index(seat_index)
            if not seat_ui:
                continue
            if state == BATTLE_STATE_FIGHTING:
                seat_ui.temp_head.nd_battle.setVisible(True)
            else:
                seat_ui.temp_head.nd_battle.setVisible(False)

        return

    def on_change_map_area(self, born_idx):
        map_config = confmgr.get('map_config')
        born_list = map_config[str(self._curr_map_id)].get('bornList', [])
        if born_idx == -1:
            map_name = get_text_by_id(RANDOM_MAP_TEXT_ID)
        else:
            map_name = get_text_by_id(born_list[born_idx])
        self.panel.nd_player.img_map_bar.lab_map.SetString(map_name)

    def is_competition_room(self):
        return self.room_info and self.is_competition(self.room_info.battle_type)

    def on_change_room_battle_type(self, room_info):
        battle_type = room_info.get('battle_type', -1)
        self._curr_battle_type = battle_type
        self._curr_map_id = room_info.get('map_id', -1)
        self.room_info.battle_type = battle_type
        self.room_info.max_team_cnt = room_info.get('max_team_cnt', -1)
        self.room_info.max_team_size = room_info.get('max_team_size', -1)
        self.room_info.reset_player_seat(room_info.get('players'))
        self.set_mode_layout(battle_type)
        self.change_mode_cb(battle_type)
        self.update_player_num()
        self.room_invite_widget and self.room_invite_widget.on_room_battle_type_changed()
        mode_name = get_mode_name(battle_type)
        global_data.game_mgr.show_tip(get_text_by_id(608174).format(mode_name))

    def on_set_can_change_seat(self, change_seat):
        self.room_info.update_can_change_seat(change_seat)
        self.panel.temp_choose.choose.setVisible(change_seat)

    def on_set_can_chat_in_room(self, can_chat_in_room):
        self.room_info.update_can_chat_in_room(can_chat_in_room)
        self.panel.temp_lock_voice.choose.setVisible(not can_chat_in_room)

    def on_set_can_leave_room(self, can_leave_room):
        self.room_info.update_can_leave_room(can_leave_room)
        self.panel.temp_lock.choose.setVisible(not can_leave_room)

    def on_set_char_name_in_room(self, uid, char_name_in_room):
        self.room_info and self.room_info.update_roommate_info(uid, {'char_name_in_room': char_name_in_room})
        if self.is_judgement(uid):
            self.judgement_on_set_char_name_in_room(uid, char_name_in_room)
        else:
            self.team_layout.on_set_char_name_in_room(uid, char_name_in_room)

    def on_set_competition_team_name(self, team_idx, team_name):
        self.room_info and self.room_info.on_set_competition_team_name(team_idx, team_name)
        self.team_layout and self.team_layout.on_set_competition_team_name(team_idx, team_name)

    def on_click_dissolve_btn(self, *args):

        def confirm_callback():
            global_data.player.req_dissolve_room()
            global_data.ui_mgr.close_ui(self.__class__.__name__)

        SecondConfirmDlg2().confirm(content=get_text_by_id(19308), confirm_callback=confirm_callback)

    def on_click_start_btn(self, *args):
        if self.room_info.creator != global_data.player.uid:
            return
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(str(self.room_info.battle_type))
        needed_points = int(battle_info.get('iRoomPoints', 0))
        min_player_num = int(battle_info.get('iMinPlayerNum', 0))
        min_team_num = int(battle_info.get('iMinTeamNum', 0))
        if self.room_info.get_team_num() < min_team_num:
            global_data.game_mgr.show_tip(get_text_by_id(608164))
            return
        if self.room_info.room_battled_times == 0 or self.is_competition(self.room_info.battle_type):

            def confirm_callback():
                global_data.player.req_start()

            SecondConfirmDlg2().confirm(content=get_text_by_id(862029).format(needed_points), confirm_callback=confirm_callback)
        elif not global_data.player.has_enough_item(ITEM_NO_ROOM_POINT, needed_points) and needed_points != 0:

            def confirm_callback():
                GroceriesBuyConfirmUI(goods_id=RoomUINew.ITEM_NO_ROOM_POINT_IN_MALL)

            SecondConfirmDlg2().confirm(content=get_text_by_id(862010), confirm_callback=confirm_callback)
        else:

            def confirm_callback():
                global_data.player.req_start()

            SecondConfirmDlg2().confirm(content=get_text_by_id(862011).format(needed_points), confirm_callback=confirm_callback)

    def on_click_exit_btn(self, *args):

        def confirm_callback():
            global_data.player.req_leave_room()

        SecondConfirmDlg2().confirm(content=get_text_by_id(19309), confirm_callback=confirm_callback)

    def ui_vkb_custom_func(self):
        self.on_click_exit_btn()

    def on_click_tips_btn(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_local_content(608157), get_text_local_content(608158))

    def on_click_time1_btn(self, *args):
        from logic.comsys.room.AutoDissolveDescUI import AutoDissolveDescUI
        wpos = self.panel.btn_time_1.ConvertToWorldSpacePercentage(0, 0)
        import cc
        anchor = cc.Vec2(1, 0.5)
        wpos.x -= 20
        global_data.emgr.show_item_desc_text_ui_event.emit(get_text_by_id(862026), wpos, anchor, True, self.panel)

    def on_click_time2_btn(self, *args):
        from logic.comsys.room.AutoDissolveDescUI import AutoDissolveDescUI
        wpos = self.panel.btn_time_2.ConvertToWorldSpacePercentage(0, 0)
        import cc
        anchor = cc.Vec2(1, 0.5)
        wpos.x -= 20
        global_data.emgr.show_item_desc_text_ui_event.emit(get_text_by_id(862026), wpos, anchor, True, self.panel)

    def on_click_invite_btn(self, *args):
        self.room_invite_widget.show()

    def on_click_enbale_change_seat(self, *args):
        if self.room_info.creator != global_data.player.uid:
            return
        global_data.player.set_can_change_seat()

    def on_click_enable_leave_room(self, *args):
        if not self.is_judgement():
            return
        global_data.player.set_can_leave_room()

    def on_click_disable_chat(self, *args):
        if not self.is_judgement():
            return
        global_data.player.set_can_chat_in_room()

    def on_click_help_btn(self, *args):
        global_data.player and global_data.player.request_rejoin_competition_ob()

    def init_event(self):
        global_data.emgr.player_info_update_event += self._on_player_info_update
        global_data.emgr.room_player_return_from_lobby_event += self.return_from_lobby

    def _on_player_info_update(self, *args):
        self.update_widget()

    def update_widget(self):
        from logic.gutils import template_utils

        def close(*args):
            self.on_click_close_btn()

        template_utils.init_common_pnl_title(self.panel.nd_top, '', close)

    def on_click_close_btn(self):
        self.return_to_lobby()

    def return_to_lobby(self):
        self.set_hide_effect()
        self.add_hide_count('ToLobby')
        global_data.emgr.room_player_return_to_lobby_event.emit()

    def return_from_lobby(self):
        self.set_appear_effect()
        self.add_show_count('ToLobby')

    def set_hide_effect(self):
        if self._has_set_appear_effect:
            self._has_set_appear_effect = False
            self.show_main_ui()
            ui = global_data.ui_mgr.get_ui('MainChat')
            ui and ui.mod_input_box_pos()
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def set_appear_effect(self):
        self.hide_main_ui(exceptions=('MainChat', ))
        ui = global_data.ui_mgr.get_ui('MainChat')
        ui and ui.mod_input_box_pos((41, 37))
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self._has_set_appear_effect = True

    def do_show_panel(self):
        super(RoomUINew, self).do_show_panel()
        self.set_appear_effect()

    def do_hide_panel(self):
        super(RoomUINew, self).do_hide_panel()
        self.set_hide_effect()

    def _on_room_point_num_update(self):
        room_point_num = global_data.player.get_item_num_by_no(ITEM_NO_ROOM_POINT)
        ui_item = self.list_money.GetItem(0)
        ui_item.txt_price.SetString(str(room_point_num))

    def is_waiting(self):
        return self.panel.lab_waite.isVisible()

    def is_competition(self, battle_type):
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(str(battle_type))
        if battle_info is None:
            log_error('RoomUINew, is_competition non exist battle_type', battle_type)
            return False
        else:
            if battle_info.get('iRoomNeededItem', None) is None:
                return False
            return True

    def is_judgement(self, uid=None):
        if not uid:
            uid = global_data.player.uid
        seat_idx = self.room_info.get_player_seat_idx(uid)
        return self.is_in_judge_seat(seat_idx)

    def update_ob_btn(self):
        curr_judge_num = len(self.room_info.uid2judge_seat)
        if self.is_competition_room():
            self.panel.nd_judgement_seat.btn_judgement_seat.SetText(get_text_by_id(19305, (curr_judge_num, const.OB_GROUP_ID_END - const.OB_GROUP_ID_START + 1)))
        else:
            self.panel.nd_judgement_seat.btn_judgement_seat.SetText(get_text_by_id(19684, (curr_judge_num, const.OB_GROUP_ID_END - const.OB_GROUP_ID_START + 1)))

    def init_custom_setting_widget(self):
        self._custom_setting_widget = CustomBattleSettingWidget(self.panel.temp_setting, self._customed_battle_dict)

    def enable_custom_setting_panel(self, enable):
        if not self._custom_setting_widget:
            return
        self._custom_setting_widget.enable_buttons(enable)

    def on_change_custom_battle_dict(self, customed_battle_dict):
        self._customed_battle_dict = customed_battle_dict
        self._custom_setting_widget.recover_settings(self._customed_battle_dict)

    def on_click_setting_btn(self, *args):
        self._custom_setting_widget.recover_settings(self._customed_battle_dict)
        self.panel.temp_setting.setVisible(True)

    def on_click_setting_close_btn(self, *args):
        self.panel.temp_setting.setVisible(False)
        self.show_custom_battle_setting_guide()

    def on_click_setting_reset_btn(self, *args):
        self._customed_battle_dict = {}
        self._custom_setting_widget.recover_settings(self._customed_battle_dict)
        global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ACHI_NAME, self._customed_battle_dict)
        global_data.player.req_change_custom_battle_dict(self._customed_battle_dict)

    def on_click_setting_save_btn(self, *args):
        self._customed_battle_dict = self._custom_setting_widget.get_setting_dict()
        global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ACHI_NAME, self._customed_battle_dict)
        global_data.game_mgr.show_tip(get_text_by_id(CUSTOM_SETTINGS_TIP_TXT_SAVE))
        global_data.player.req_change_custom_battle_dict(self._customed_battle_dict)

    def show_custom_battle_setting_guide(self, *args):
        if not self.need_guide_room_setting:
            return
        else:
            self.guide_room_setting = template_utils.init_guide_temp(self.panel.nd_content.nd_info.btn_setting, None, CUSTOM_SETTINGS_ROOM_GUIDE_TXT, 'custom_battle_guide_4', 'common/i_guide_left_below')
            global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ROOM_GUIDE, False)
            self.need_guide_room_setting = False

            @self.panel.nd_touch.callback()
            def OnClick(*args):
                self.destroy_guide_ui()

            return

    def destroy_guide_ui(self):
        if self.guide_room_setting:
            self.guide_room_setting.removeFromParent()
            self.guide_room_setting = None
        return
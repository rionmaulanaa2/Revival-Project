# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomCreateUINew.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils.battle_utils import get_mode_name
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.comsys.mall_ui.GroceriesBuyConfirmUI import GroceriesBuyConfirmUI
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.item.item_const import ITEM_NO_ROOM_POINT
from logic.gcommon.const import BATTLE_STATE_FIGHTING, BATTLE_STATE_INROOM
import logic.gcommon.item.item_const as iconst
from logic.comsys.setting_ui.SettingWidget.CustomBattleSettingWidget import CustomBattleSettingWidget
from logic.gcommon.common_const.custom_battle_const import CUSTOM_SETTINGS_MEMORY_ACHI_NAME, CUSTOM_SETTINGS_MEMORY_GUIDE, CUSTOM_SETTINGS_CLICK_GUIDE_TXT, CUSTOM_SETTINGS_TIP_TXT_SAVE, CUSTOM_SETTINGS_TIP_TXT_CANNOT_CHANGE
from logic.gutils import guide_utils as gu
from logic.gutils import template_utils

class RoomCreateUINew(WindowMediumBase):
    PANEL_CONFIG_NAME = 'room/create_room_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'pnl_create'
    UI_ACTION_EVENT = {'btn_create.btn_common_big.OnClick': 'on_click_create_btn',
       'btn_tick.OnClick': 'on_click_need_password_btn',
       'btn_map.OnClick': 'on_click_map_btn',
       'btn_exchange.OnClick': 'on_click_exchange_btn',
       'btn_setting.OnClick': 'on_click_setting_btn',
       'temp_setting.pnl_create_custom.btn_close.OnClick': 'on_click_setting_close_btn',
       'temp_setting.pnl_create_custom.temp_btn_1.btn_common_big.OnClick': 'on_click_setting_reset_btn',
       'temp_setting.pnl_create_custom.temp_btn_2.btn_common_big.OnClick': 'on_click_setting_save_btn'
       }
    DEFAULT_MODE = '90001'
    ITEM_NO_ROOM_POINT_IN_MALL = '50302026'
    DEFAULT_MAX_ROOM_NAME_LENGTH = 12
    DEFAULT_MAX_COMPETITION_ROOM_NAME_LENGTH = 24

    def on_init_panel(self, *args, **kwargs):
        super(RoomCreateUINew, self).on_init_panel()
        if global_data.is_inner_server:
            self.panel.btn_exchange.setVisible(True)
        else:
            self.panel.btn_exchange.setVisible(False)
        self.init_parameters()
        self.init_custom_room_data()
        self.init_widget()

    def init_parameters(self):
        self._max_room_name_length = self.DEFAULT_MAX_ROOM_NAME_LENGTH
        self._custom_setting_widget = None
        self.guide_click_setting = None
        self._customed_battle_dict = self.decode_setting_achi()
        self.need_guide = global_data.achi_mgr.get_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_GUIDE, True)
        return

    def decode_setting_achi(self):
        dict = global_data.achi_mgr.get_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ACHI_NAME, {})
        for idx in six_ex.keys(dict):
            if not isinstance(idx, int):
                dict[int(idx)] = dict[idx]
                dict.pop(idx)

        return dict

    def init_custom_room_data(self):
        battle_config = confmgr.get('battle_config')
        self._supported_mode_people_size = {}
        for battle_type, mode_conf in six.iteritems(battle_config):
            if mode_conf.get('bSupportCustom', 0) == 2 and self._can_create_room(battle_type):
                people_size = mode_conf.get('cPlayerConf').get('people_size')
                self._supported_mode_people_size[battle_type] = people_size

    def init_widget(self):
        self.init_input()
        self.init_mode_list()
        self.init_custom_setting_widget()
        self.show_custom_battle_click_setting_guide_ui()

    def init_input(self):

        def name_check():
            name_text = self._name_input_box.get_text()
            is_valid, msg = self._valid_name_text_check(name_text)
            if not is_valid:
                global_data.game_mgr.show_tip(msg)

        self._name_input_box = InputBox.InputBox(self.panel.input_room_name, max_length=self._max_room_name_length, placeholder=get_text_by_id(19318), need_sp_length_func=True)
        self._name_input_box.set_rise_widget(self.panel)
        self._password_input_box = InputBox.InputBox(self.panel.input_password, placeholder=get_text_by_id(19316))
        self._password_input_box.setPasswordEnabled(True)
        self._password_input_box.set_rise_widget(self.panel)
        self.panel.sp_password.setVisible(False)
        self._num_input_box = InputBox.InputBox(self.panel.input_member_num)
        self._num_input_box.set_rise_widget(self.panel)
        self._num_input_box.enable_input(False)

    def update_max_room_name_length(self, battle_type):
        if self.is_competition(battle_type):
            self._max_room_name_length = self.DEFAULT_MAX_COMPETITION_ROOM_NAME_LENGTH
        else:
            self._max_room_name_length = self.DEFAULT_MAX_ROOM_NAME_LENGTH
        if self._name_input_box:
            cur_input_text = self._name_input_box.get_text()
        else:
            cur_input_text = ''
        self._name_input_box = InputBox.InputBox(self.panel.input_room_name, max_length=self._max_room_name_length, placeholder=get_text_by_id(19318), need_sp_length_func=True)
        self._name_input_box.set_rise_widget(self.panel)
        cur_input_text and self._name_input_box.set_text(cur_input_text)

    def init_create_btn(self, battle_type):
        if self.is_competition(battle_type):
            self.panel.img_cost.setVisible(False)
            self.btn_create.btn_common_big.SetTextOffset({'x': '50%','y': '50%'})
        else:
            self.panel.img_cost.setVisible(True)
            self.btn_create.btn_common_big.SetTextOffset({'x': '50%','y': '50%'})
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            needed_points = int(battle_info.get('iRoomPoints', 0))
            self.panel.lab_num.SetString(str(needed_points))
            if global_data.player.has_enough_item(ITEM_NO_ROOM_POINT, needed_points) or needed_points == 0:
                self.panel.lab_num.SetColor('#SK')
            else:
                self.panel.lab_num.SetColor('#SR')

    def get_mode_people_size(self, battle_type):
        battle_config = confmgr.get('battle_config')
        return battle_config[battle_type].get('cPlayerConf').get('people_size')

    def get_mode_map_id(self, battle_type):
        battle_config = confmgr.get('battle_config')
        return battle_config[battle_type].get('iMapID')

    def init_mode_list(self):
        modes = sorted(six_ex.keys(self._supported_mode_people_size))
        mode_options = [ {'name': get_mode_name(mode),'battle_type': mode} for mode in modes ]

        @self.panel.btn_map.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.map_list.isVisible():
                self.panel.map_list.setVisible(True)
                self.panel.btn_map.img_icon.setRotation(180)
            else:
                self.panel.map_list.setVisible(False)
                self.panel.btn_map.img_icon.setRotation(0)

        def call_back(index):
            option = mode_options[index]
            battle_type = option['battle_type']
            self._curr_battle_type = battle_type
            self.panel.btn_map.SetText(option['name'])
            self._num_input_box and self._num_input_box.set_text(str(self.get_mode_people_size(self._curr_battle_type)))
            self.panel.map_list.setVisible(False)
            self.panel.btn_map.img_icon.setRotation(0)
            self.init_create_btn(str(battle_type))
            self.update_max_room_name_length(battle_type)

        template_utils.init_common_choose_list_2(self.panel.map_list, self.panel.btn_map.img_icon, mode_options, call_back, max_height=354)
        call_back(modes.index(RoomCreateUINew.DEFAULT_MODE))

    def on_click_create_btn(self, *args):
        is_valid, info = self.get_create_room_spec()
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(self._curr_battle_type)
        needed_points = int(battle_info.get('iRoomPoints', 0))
        if not global_data.player.has_enough_item(ITEM_NO_ROOM_POINT, needed_points) and needed_points != 0:

            def confirm_callback():
                global_data.ui_mgr.close_ui(self.__class__.__name__)
                GroceriesBuyConfirmUI(goods_id=RoomCreateUINew.ITEM_NO_ROOM_POINT_IN_MALL)

            SecondConfirmDlg2().confirm(content=get_text_by_id(862010), confirm_callback=confirm_callback)
            return

        def confirm_callback():
            if is_valid:
                global_data.player.req_create_room(info)
            else:
                global_data.game_mgr.show_tip(info)

        if self.is_competition(self._curr_battle_type):
            SecondConfirmDlg2().confirm(content=get_text_by_id(80560).format(needed_points), confirm_callback=confirm_callback)
        else:
            SecondConfirmDlg2().confirm(content=get_text_by_id(862053).format(needed_points), confirm_callback=confirm_callback)

    def on_click_need_password_btn(self, *args):
        self.panel.sp_password.setVisible(not self.panel.sp_password.isVisible())
        self.panel.btn_tick.SetSelect(self.panel.sp_password.isVisible())

    def on_click_exchange_btn(self, *args):
        from logic.comsys.room.RoomCreateUI import RoomCreateUI
        self.close()
        RoomCreateUI()

    def get_create_room_spec(self):
        room_name = self._name_input_box.get_text()
        if not room_name:
            room_name = get_text_by_id(19318)
        else:
            is_valid, msg = self._valid_name_text_check(room_name)
            if not is_valid:
                return (False, msg)
        need_pwd = self.panel.sp_password.isVisible()
        if need_pwd:
            pwd = self._password_input_box.get_text()
        else:
            pwd = ''
        if pwd:
            is_valid, msg = self._valid_password_text_check(pwd)
            if not is_valid:
                return (False, msg)
        is_customed_battle = False
        if self._customed_battle_dict:
            is_customed_battle = True
        room_info = {'name': room_name,
           'pwd': pwd,
           'battle_type': int(self._curr_battle_type),
           'map_id': self.get_mode_map_id(self._curr_battle_type),
           'max_player_cnt': self.get_mode_people_size(self._curr_battle_type),
           'clan_name': global_data.player.get_clan_name(),
           'clan_lv': global_data.player.get_clan_lv(),
           'clan_badge': global_data.player.get_clan_badge(),
           'battle_state': BATTLE_STATE_INROOM,
           'dan_info': global_data.player.get_dan_info(),
           'inner_server_room': False,
           'customed_battle_dict': self._customed_battle_dict,
           'is_customed_battle': is_customed_battle
           }
        return (
         True, room_info)

    def _valid_name_text_check(self, text):
        from logic.gcommon.common_utils.text_utils import check_review_words
        flag, text = check_review_words(text)
        if not flag:
            error_text = get_text_by_id(11009)
            return (
             False, error_text)
        return (True, '')

    def _valid_password_text_check(self, text):
        from logic.gcommon.common_utils.text_utils import check_review_words
        flag, text = check_review_words(text)
        if not flag:
            error_text = get_text_by_id(10371)
            return (
             False, error_text)
        return (True, '')

    def _can_create_room(self, battle_type):
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(str(battle_type))
        needed_item_no = battle_info.get('iRoomNeededItem', None)
        if needed_item_no is None:
            return True
        else:
            return global_data.player.has_item_by_no(iconst.ITEM_NO_ROOM_COMPETITION_CARD)
            return

    def is_competition(self, battle_type):
        battle_config = confmgr.get('battle_config')
        battle_info = battle_config.get(str(battle_type))
        if battle_info.get('iRoomNeededItem', None) is None:
            return False
        else:
            return True

    def init_custom_setting_widget(self):
        self._custom_setting_widget = CustomBattleSettingWidget(self.panel.temp_setting, self._customed_battle_dict)

    def on_click_setting_btn(self, *args):
        self._custom_setting_widget.recover_settings(self._customed_battle_dict)
        self.panel.temp_setting.setVisible(True)

    def on_click_setting_close_btn(self, *args):
        self.panel.temp_setting.setVisible(False)

    def on_click_setting_reset_btn(self, *args):
        self._customed_battle_dict = {}
        self._custom_setting_widget.recover_settings(self._customed_battle_dict)
        global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ACHI_NAME, self._customed_battle_dict)

    def on_click_setting_save_btn(self, *args):
        self._customed_battle_dict = self._custom_setting_widget.get_setting_dict()
        global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_ACHI_NAME, self._customed_battle_dict)
        global_data.game_mgr.show_tip(get_text_by_id(CUSTOM_SETTINGS_TIP_TXT_SAVE))

    def show_custom_battle_click_setting_guide_ui(self):
        if not self.need_guide:
            return
        else:
            self.guide_click_setting = template_utils.init_guide_temp(self.panel.pnl_create.btn_setting, None, CUSTOM_SETTINGS_CLICK_GUIDE_TXT, 'custom_battle_guide_1')

            @self.panel.nd_touch.callback()
            def OnClick(*args):
                self.destroy_guide_ui()

            self.need_guide = False
            global_data.achi_mgr.set_cur_user_archive_data(CUSTOM_SETTINGS_MEMORY_GUIDE, False)
            return

    def destroy_guide_ui(self):
        if self.guide_click_setting:
            self.guide_click_setting.removeFromParent()
            self.guide_click_setting = None
        return
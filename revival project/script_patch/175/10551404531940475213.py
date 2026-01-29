# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomCreateUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from common.platform.dctool import interface
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.custom_room_utils import RANDOM_MAP_TEXT_ID
TeamNum2BattleType = {1: 7,
   2: 8,4: 9}

class RoomCreateUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'room/create_room'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'pnl_create'
    UI_ACTION_EVENT = {'btn_create.btn_common_big.OnClick': 'on_click_create_btn',
       'btn_tick.OnClick': 'on_click_need_password_btn',
       'btn_exchange.OnClick': 'on_click_exchange_btn'
       }

    def on_init_panel(self):
        super(RoomCreateUI, self).on_init_panel()
        self.panel.btn_exchange.setVisible(True)
        self.init_event()
        self.init_widget()

    def init_event(self):
        global_data.player.req_room_list()

    def on_click_create_btn(self, *args):
        is_valid, info = self.get_create_room_spec()
        if is_valid:
            global_data.player.req_create_room(info)
        else:
            global_data.game_mgr.show_tip(info)

    def get_room_limit_num(self):
        battle_type = self._mode_team_size_to_battle_type_dict.get((str(self._cur_map_id), str(self._cur_team_size)), None)
        battle_config = confmgr.get('battle_config')
        return battle_config.get(str(battle_type), {}).get('cPlayerConf', {}).get('people_size')

    def get_create_room_spec(self):
        import math
        room_name = self._name_input_box.get_text()
        if not room_name:
            room_name = get_text_by_id(19318)
        else:
            is_valid, msg = self._valid_name_text_check(room_name)
            if not is_valid:
                return (False, msg)
        room_num_text = self._num_input_box.get_text()
        if not room_num_text:
            room_max_num = self.get_room_limit_num()
        else:
            is_valid, msg = self._valid_member_num_text_check(room_num_text)
            if not is_valid:
                return (False, msg)
            room_max_num = int(room_num_text)
        need_pwd = self.panel.sp_password.isVisible()
        if need_pwd:
            pwd = self._password_input_box.get_text()
        else:
            pwd = ''
        battle_type = self._mode_team_size_to_battle_type_dict.get((
         str(self._cur_map_id), str(self._cur_team_size)), None)
        if battle_type is not None:
            room_info = {'name': room_name,'max_player_cnt': math.ceil(room_max_num / self._cur_team_size) * self._cur_team_size,
               'pwd': pwd,
               'battle_type': int(battle_type),
               'map_id': int(self._cur_map_id),
               'inner_server_room': True
               }
            if self._cur_born_idx is not None:
                room_info['born_idx'] = self._cur_born_idx
                room_info['env_name'] = self._cur_env_name
            return (
             True, room_info)
        else:
            return (
             False, get_text_by_id(13020))
            return

    def on_click_need_password_btn(self, *args):
        self.panel.sp_password.setVisible(not self.panel.sp_password.isVisible())
        self.panel.btn_tick.SetSelect(self.panel.sp_password.isVisible())

    def on_click_exchange_btn(self, *args):
        from logic.comsys.room.RoomCreateUINew import RoomCreateUINew
        self.close()
        RoomCreateUINew()

    def on_finalize_panel(self):
        if self._name_input_box:
            self._name_input_box.destroy()
            self._name_input_box = None
        if self._num_input_box:
            self._num_input_box.destroy()
            self._num_input_box = None
        if self._password_input_box:
            self._password_input_box.destroy()
            self._password_input_box = None
        return

    def init_widget(self):
        self.init_custom_room_data()
        self.init_input()
        self.init_map_list()

    def init_custom_room_data(self):
        battle_config = confmgr.get('battle_config')
        modes = set()
        all_possible_team_size = set()
        self._map_support_team_size = {}
        self._mode_team_size_to_battle_type_dict = {}
        for battle_type, mode_conf in six.iteritems(battle_config):
            if mode_conf.get('bSupportCustom', 0) == 1:
                map_id = mode_conf['iMapID']
                team_size = mode_conf.get('cTeamNum', 1)
                modes.add(map_id)
                all_possible_team_size.add(team_size)
                if map_id not in self._map_support_team_size:
                    self._map_support_team_size[map_id] = []
                self._map_support_team_size[map_id].append(team_size)
                self._mode_team_size_to_battle_type_dict[str(map_id), str(team_size)] = battle_type

        self._support_custom_maps = list(modes)
        self._support_custom_team_size = list(all_possible_team_size)

    def init_mode_list(self, map_id=None):
        from logic.gutils import template_utils
        TEAM_SIZE_ONE = 1
        TEAM_SIZE_SECOND = 2
        TEAM_SIZE_THREE = 3
        TEAM_SIZE_FOUR = 4
        team_size_to_name_dict = {TEAM_SIZE_ONE: get_text_local_content(19005),
           TEAM_SIZE_SECOND: get_text_local_content(19006),
           TEAM_SIZE_THREE: get_text_local_content(19007),
           TEAM_SIZE_FOUR: get_text_local_content(19007)
           }
        all_possibile_team_sizes = sorted(self._map_support_team_size.get(map_id, self._support_custom_team_size))
        mode_option = [ {'name': team_size_to_name_dict.get(team_size, str(team_size)),'mode': team_size} for team_size in all_possibile_team_sizes ]

        @self.panel.btn_mode.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.mode_list.isVisible():
                self.panel.mode_list.setVisible(True)
                self.panel.btn_mode.img_icon.setRotation(180)
            else:
                self.panel.mode_list.setVisible(False)
                self.panel.btn_mode.img_icon.setRotation(0)

        def call_back(index):
            option = mode_option[index]
            self._cur_team_size = option['mode']
            self.panel.btn_mode.SetText(option['name'])
            self.panel.mode_list.setVisible(False)
            self.panel.btn_mode.img_icon.setRotation(0)
            self._num_input_box and self._num_input_box.set_text(str(self.get_room_limit_num()))

        template_utils.init_common_choose_list(self.panel.mode_list, mode_option, call_back, max_height=354)
        call_back(0)

    def init_born_list(self, map_id):
        from logic.gutils import template_utils
        map_config = confmgr.get('map_config')
        born_list = map_config[map_id].get('bornList', [])
        environment_list = map_config[map_id].get('cSceneConfig', None)
        if not isinstance(environment_list, dict):
            environment_list = {None: 0}
        if not born_list:
            self.panel.btn_born.setVisible(False)
            self.panel.born_list.setVisible(False)
            self._cur_born_idx = None
            self._cur_env_name = None
        else:
            self.panel.btn_born.setVisible(True)
            self.panel.born_list.setVisible(False)
            born_option = []
            if len(born_list) > 1:
                born_option.append({'name': get_text_by_id(RANDOM_MAP_TEXT_ID),
                   'born_idx': -1,
                   'env_name': None
                   })
            for env in six.iterkeys(environment_list):
                for born_idx, born_type in enumerate(born_list):
                    name = get_text_local_content(born_type)
                    if env:
                        name += '_' + env[0]
                    born_option.append({'name': name,
                       'born_idx': born_idx,
                       'env_name': env
                       })

            @self.panel.btn_born.unique_callback()
            def OnClick(btn, touch):
                if not self.panel.born_list.isVisible():
                    self.panel.born_list.setVisible(True)
                    self.panel.btn_born.img_icon.setRotation(180)
                else:
                    self.panel.born_list.setVisible(False)
                    self.panel.btn_born.img_icon.setRotation(0)

            def call_back(index):
                option = born_option[index]
                self._cur_born_idx = option['born_idx']
                self._cur_env_name = option['env_name']
                self.panel.btn_born.SetText(option['name'])
                self.panel.born_list.setVisible(False)
                self.panel.btn_born.img_icon.setRotation(0)

            template_utils.init_common_choose_list(self.panel.born_list, born_option, call_back, max_height=354)
            call_back(0)
        return

    def init_map_list(self):
        from logic.gutils import template_utils
        modes = sorted(self._support_custom_maps)
        map_config = confmgr.get('map_config')
        mode_option = [ {'name': get_text_local_content(map_config[mode].get('nameTID', 19335)),'map_id': mode} for mode in modes ]

        @self.panel.btn_map.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.map_list.isVisible():
                self.panel.map_list.setVisible(True)
                self.panel.btn_map.img_icon.setRotation(180)
            else:
                self.panel.map_list.setVisible(False)
                self.panel.btn_map.img_icon.setRotation(0)

        def call_back(index):
            option = mode_option[index]
            map_id = option['map_id']
            self._cur_map_id = map_id
            self.init_mode_list(map_id)
            self.init_born_list(map_id)
            self.panel.btn_map.SetText(option['name'])
            self._num_input_box and self._num_input_box.set_text(str(self.get_room_limit_num()))
            self.panel.map_list.setVisible(False)
            self.panel.btn_map.img_icon.setRotation(0)

        template_utils.init_common_choose_list(self.panel.map_list, mode_option, call_back, max_height=354)
        DEFAULT_MAP_ID = '2'
        if DEFAULT_MAP_ID in modes:
            idx = modes.index(DEFAULT_MAP_ID)
            call_back(idx)
        else:
            call_back(len(mode_option) - 1)

    def _valid_member_num_text_check(self, num_text, min_num=1, max_num=100):
        if num_text:
            if not num_text.isdigit():
                error_text = get_text_by_id(19319)
                return (
                 False, error_text)
            num = int(num_text)
            if not min_num <= num <= max_num:
                error_text = get_text_by_id(19320, (min_num, max_num))
                return (
                 False, error_text)
        return (
         True, '')

    def _valid_name_text_check(self, text):
        from logic.gcommon.common_utils.text_utils import check_review_words
        flag, text = check_review_words(text)
        if not flag:
            error_text = get_text_by_id(11009)
            return (
             False, error_text)
        return (True, '')

    def init_input(self):
        import logic.comsys.common_ui.InputBox as InputBox
        self.panel.btn_tick.EnableCustomState(True)
        self.panel.btn_tick.SetSelect(False)
        self._name_input_box = InputBox.InputBox(self.panel.input_room_name, max_length=20, placeholder=get_text_by_id(19318))
        self._name_input_box.set_rise_widget(self.panel)
        self._num_input_box = InputBox.InputBox(self.panel.input_member_num, max_length=20, placeholder='100')
        self._num_input_box.set_rise_widget(self.panel)
        self._password_input_box = InputBox.InputBox(self.panel.input_password, max_length=20, placeholder=get_text_by_id(19316))
        self._password_input_box.setPasswordEnabled(True)
        self._password_input_box.set_rise_widget(self.panel)
        self.panel.sp_password.setVisible(False)
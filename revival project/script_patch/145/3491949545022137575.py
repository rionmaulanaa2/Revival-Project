# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/room/RoomRecruitUI.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_const import chat_const
from logic.gutils.custom_room_utils import RANDOM_MAP_TEXT_ID
from logic.gcommon.common_utils.battle_utils import get_mode_name
ROOM_MODE_BG_PIC = {90001: 'gui/ui_res_2/main/mode_img_tdm.png',
   90002: 'gui/ui_res_2/main/mode_img_suger.png',
   90003: 'gui/ui_res_2/main/mode_img_suger.png',
   90004: 'gui/ui_res_2/main/mode_img_gvg.png',
   90005: 'gui/ui_res_2/main/mode_img_suger.png',
   90006: 'gui/ui_res_2/main/mode_img_suger.png',
   90007: 'gui/ui_res_2/main/mode_img_tdm.png'
   }

class RoomRecruitUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'room/room_recruit'
    TEMPLATE_NODE_NAME = 'nd_recruit'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_crew.btn_common.OnClick': 'on_click_crew_btn',
       'temp_common.btn_common.OnClick': 'on_click_common_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(RoomRecruitUI, self).on_init_panel()
        self._max_player_num = -1
        self._cur_player_num = -1
        self._mode_name = ''
        self._need_pwd = False
        self._room_name = ''
        self._room_id = -1
        self._battle_type = -1
        self.init_widget()

    def on_finalize_panel(self):
        pass

    def init_widget(self):
        room_info = global_data.player.get_cur_custom_room_info()
        max_player_num = global_data.player.get_custom_room_max_player_num()
        cur_player_num = len(room_info.get('players', {}))
        battle_type = room_info.get('battle_type', -1)
        born_idx = room_info.get('born_idx', -1)
        room_name = room_info.get('name', '')
        mode_name = get_mode_name(battle_type)
        area_name = self.get_born_area_name(battle_type, born_idx)
        mode_pic = self.get_mode_bg_pic(battle_type)
        place_holder = get_text_by_id(608180)
        self.panel.lab_player_num.SetString(get_text_by_id(19313, (cur_player_num, max_player_num)))
        self.panel.lab_name.SetString(room_name)
        self.panel.lab_mode.SetString('{}-{}'.format(mode_name, area_name))
        self.panel.img_mode.SetDisplayFrameByPath('', mode_pic)
        self.input_box = InputBox.InputBox(self.panel.temp_inputbox, max_length=22, placeholder=place_holder, need_sp_length_func=True)
        self.input_box.set_rise_widget(self.panel)
        self._max_player_num = max_player_num
        self._cur_player_num = cur_player_num
        self._mode_name = mode_name
        self._need_pwd = room_info.get('need_pwd')
        self._room_id = room_info.get('room_id', -1)
        self._battle_type = room_info.get('battle_type', -1)
        self._room_name = room_name

    def get_born_area_name(self, battle_type, born_idx):
        if battle_type is None:
            return ''
        else:
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(battle_type))
            if battle_info is None:
                return ''
            map_id = battle_info.get('iMapID', -1)
            if map_id == -1:
                return ''
            map_config = confmgr.get('map_config')
            map_info = map_config.get(str(map_id))
            if map_info is None:
                return ''
            born_list = map_info.get('bornList')
            if not born_list:
                return ''
            if born_idx == -1:
                return get_text_by_id(RANDOM_MAP_TEXT_ID)
            born_idx = born_idx if 0 <= born_idx <= len(born_list) - 1 else None
            if born_idx is None:
                return ''
            return get_text_by_id(born_list[born_idx])

    def get_mode_bg_pic(self, battle_type):
        return ROOM_MODE_BG_PIC.get(int(battle_type), 'gui/ui_res_2/main/btn_mode_choose_tdm.png')

    def on_click_crew_btn(self, *args):
        extra_data = self.get_extra_data()
        self.show_main_chat(True, chat_const.CHAT_CLAN)
        global_data.player.send_msg(chat_const.CHAT_CLAN, '', extra=extra_data)
        self.close()

    def on_click_common_btn(self, *args):
        extra_data = self.get_extra_data()
        self.show_main_chat(True, chat_const.CHAT_WORLD)
        global_data.player.send_msg(chat_const.CHAT_WORLD, '', extra=extra_data)
        self.close()

    def show_main_chat(self, flag=None, channel=chat_const.CHAT_CLAN):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if not ui:
            return
        else:
            is_chat_open = ui.is_chat_open()
            if flag == is_chat_open:
                return
            if flag == None:
                flag = not is_chat_open
            if flag:
                ui.do_show_panel()
                ui.chat_open()
                ui.touch_channel_btn(channel)
            else:
                ui.chat_close()
            return

    def get_extra_data(self):
        return {'room_name': self._room_name,
           'mode_name': self._mode_name,
           'cur_player_num': self._cur_player_num,
           'max_player_num': self._max_player_num,
           'need_pwd': self._need_pwd,
           'room_id': self._room_id,
           'battle_type': self._battle_type,
           'type': chat_const.MSG_TYPE_ROOM_CARD,
           'slogan': self.input_box.get_text()
           }
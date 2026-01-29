# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/LobbyKeyboard.py
from __future__ import absolute_import
from __future__ import print_function
from .CtrlKeyboardBase import CtrlKeyboardBase
import game
import math3d
from .DirectionKeyboardHelper import DirectionKeyboardHelper
from logic.gutils.pc_utils import skip_when_debug_key_disabled
from data import hot_key_def
from logic.gutils import hot_key_utils

class LobbyKeyboard(CtrlKeyboardBase):
    MOVE_HOTKEY_LIST = [
     hot_key_def.MOVE_FORWARD,
     hot_key_def.MOVE_LEFT,
     hot_key_def.MOVE_RIGHT,
     hot_key_def.MOVE_BACKWARD]

    def __init__(self):
        super(LobbyKeyboard, self).__init__()
        self._direction_keyboard_helper = DirectionKeyboardHelper()
        global_data.emgr.hot_key_conf_refresh_event += self.on_refresh_hot_key

    def _reset_key_map(self):
        self.key_up_func = {}
        self.key_down_func = {}
        move_vk_code_list = []
        for hotkey_name in self.MOVE_HOTKEY_LIST:
            move_vk_code_list.append(hot_key_utils.hot_key_func_to_hot_key(hotkey_name))

        for vk_code in move_vk_code_list:
            if vk_code is None or hot_key_utils.is_hot_key_unset_raw_by_code(vk_code):
                continue
            self.key_up_func[vk_code] = {0: ['move_key_func']}
            self.key_down_func[vk_code] = {0: ['move_key_func']}

        self.key_up_func[game.VK_B] = {0: ['print_animation']}
        return

    def on_before_install(self):
        self._reset_key_map()

    def destroy(self):
        global_data.emgr.hot_key_conf_refresh_event -= self.on_refresh_hot_key
        super(LobbyKeyboard, self).destroy()

    def on_uninstall(self):
        self._direction_keyboard_helper.reset()

    def on_refresh_hot_key(self):
        self.uninstall()
        self.install()

    @skip_when_debug_key_disabled
    def print_animation(self, msg, keycode):
        global_data.debug_ui = not global_data.debug_ui
        print(('test--VK_B--print_animation--global_data.debug_ui =', global_data.debug_ui))
        global_data.lobby_player.send_event('E_CHARACTER_ATTR', 'animator_info', True)

    def move_key_func(self, msg, keycode):
        if global_data.pc_ctrl_mgr:
            for hotkey_name in self.MOVE_HOTKEY_LIST:
                if global_data.pc_ctrl_mgr.is_hotkey_blocked(hotkey_name):
                    return

        if keycode == hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_FORWARD):
            keycode = game.VK_W
        elif keycode == hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_LEFT):
            keycode = game.VK_A
        elif keycode == hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_RIGHT):
            keycode = game.VK_D
        elif keycode == hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_BACKWARD):
            keycode = game.VK_S
        else:
            return
        rocker_ui = global_data.ui_mgr.get_ui('LobbyRockerUI')
        if global_data.is_pc_mode or rocker_ui and rocker_ui.panel.isVisible():
            cur_move_dir = self._direction_keyboard_helper.on_update_direction(msg, keycode)
            if cur_move_dir:
                translate = cur_move_dir
                if translate.length > 0:
                    global_data.emgr.trigger_lobby_player_move.emit(translate)
                else:
                    global_data.emgr.trigger_lobby_player_move_stop.emit()
            elif cur_move_dir is None:
                global_data.emgr.trigger_lobby_player_move_stop.emit()
        elif global_data.lobby_player:
            if global_data.lobby_player.ev_g_is_move():
                global_data.emgr.trigger_lobby_player_move_stop.emit()
        return
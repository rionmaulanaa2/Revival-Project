# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/ArtCheckKeyboard.py
from __future__ import absolute_import
from .LobbyKeyboard import LobbyKeyboard
from data import hot_key_def
from logic.gutils import hot_key_utils
import game

class ArtCheckKeyboard(LobbyKeyboard):
    MOVE_HOTKEY_LIST = [
     hot_key_def.MOVE_FORWARD,
     hot_key_def.MOVE_LEFT,
     hot_key_def.MOVE_RIGHT,
     hot_key_def.MOVE_BACKWARD]
    HOTKEY_2_KEYCODE = {hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_FORWARD): game.VK_W,
       hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_LEFT): game.VK_A,
       hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_RIGHT): game.VK_D,
       hot_key_utils.hot_key_func_to_hot_key(hot_key_def.MOVE_BACKWARD): game.VK_S
       }

    def move_key_func(self, msg, keycode):
        if global_data.pc_ctrl_mgr:
            for hotkey_name in self.MOVE_HOTKEY_LIST:
                if global_data.pc_ctrl_mgr.is_hotkey_blocked(hotkey_name):
                    return

        keycode = self.HOTKEY_2_KEYCODE.get(keycode, None)
        if keycode is None:
            return
        else:
            cur_move_dir = self._direction_keyboard_helper.on_update_direction(msg, keycode)
            if cur_move_dir:
                translate = cur_move_dir
                if translate.length > 0:
                    global_data.emgr.trigger_lobby_player_move.emit(translate)
                else:
                    global_data.emgr.trigger_lobby_player_move_stop.emit()
            elif cur_move_dir is None:
                global_data.emgr.trigger_lobby_player_move_stop.emit()
            return
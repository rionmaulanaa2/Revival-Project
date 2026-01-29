# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/HotkeyConfigKeyboard.py
from __future__ import absolute_import
from .CtrlKeyboardBase import CtrlKeyboardBase
import game
from logic.gutils import hot_key_utils
RECORD_RESULT_REPLACE = 1
RECORD_RESULT_UNBIND = 2
RECORD_RESULT_TOO_MUCH_KEYS = 3
RECORD_RESULT_UNEXPECTED = 4
RECORD_RESULT_ABORT = 5
RECORD_RESULT_BUFFER_EMPTY = 6
RECORD_RESULT_COMBINATION_FORBIDDEN = 7

class HotkeyConfigKeyboard(CtrlKeyboardBase):

    def __init__(self):
        super(HotkeyConfigKeyboard, self).__init__()
        self._is_registered = False
        self._recording_buffer = []
        self._recording_hotkey_name = None
        self._record_finish_cb = None
        self._conflict_against_vk_code_list_provider = None
        return

    def destroy(self):
        self.abort_recording()
        self._unregister_keys()
        self._recording_buffer = None
        self._recording_hotkey_name = None
        self._record_finish_cb = None
        self._conflict_against_vk_code_list_provider = None
        super(HotkeyConfigKeyboard, self).destroy()
        return

    def _register_keys(self):
        if self._is_registered:
            return
        else:
            self.add_key_handler(None, None, self._key_handler)
            self._is_registered = True
            return

    def _unregister_keys(self):
        if self._is_registered:
            self.remove_key_handler(None, None, self._key_handler)
            self._is_registered = False
        return

    def on_install(self):
        pass

    def on_uninstall(self):
        self.abort_recording()

    def set_record_finish_cb(self, finish_cb):
        self._record_finish_cb = finish_cb

    def set_conflict_against_vk_code_list_provider(self, provider):
        self._conflict_against_vk_code_list_provider = provider

    def start_recording(self, hotkey_name):
        if not hotkey_name:
            return False
        if not hot_key_utils.is_hotkey_configurable(hotkey_name):
            return False
        self._start_recording(hotkey_name)
        return True

    def abort_recording(self):
        if not self.is_recording():
            return
        self._finish_recording(RECORD_RESULT_ABORT)

    def _start_recording(self, hotkey_name):
        self._recording_hotkey_name = hotkey_name
        self.set_exclusive_keyboard_lock()
        global_data.escape_mgr_agent.block(self.__class__.__name__)

    @staticmethod
    def is_record_success(record_result):
        return record_result == RECORD_RESULT_REPLACE or record_result == RECORD_RESULT_UNBIND

    def feed_stream(self, msg, vk_code):
        if not self.is_recording():
            return
        if msg == game.MSG_KEY_DOWN or msg == game.MSG_MOUSE_DOWN:
            self._recording_buffer.append(vk_code)
            if len(self._recording_buffer) == 2:
                if not hot_key_utils.can_config_combination(self._recording_hotkey_name):
                    self._finish_recording(RECORD_RESULT_COMBINATION_FORBIDDEN)
                    return
                if not hot_key_utils.is_combine_start_key(self._recording_buffer[0]) or hot_key_utils.is_mouse_btn(vk_code) or hot_key_utils.is_combine_start_key(vk_code):
                    self._finish_recording(RECORD_RESULT_TOO_MUCH_KEYS)
                    return
            elif len(self._recording_buffer) > 2:
                self._finish_recording(RECORD_RESULT_TOO_MUCH_KEYS)
                return
        elif msg == game.MSG_KEY_UP or msg == game.MSG_MOUSE_UP:
            if vk_code == game.VK_ESCAPE:
                self._finish_recording(RECORD_RESULT_UNBIND)
                return
            if len(self._recording_buffer) == 0:
                self._finish_recording(RECORD_RESULT_BUFFER_EMPTY, 'Empty buffer "%s".' % self._recording_hotkey_name)
            else:
                if len(self._recording_buffer) == 1:
                    self._finish_recording(RECORD_RESULT_REPLACE)
                    return
                if len(self._recording_buffer) == 2:
                    if vk_code == self._recording_buffer[0] and not game.get_key_state(self._recording_buffer[1]) or vk_code == self._recording_buffer[1] and not game.get_key_state(self._recording_buffer[0]):
                        self._finish_recording(RECORD_RESULT_REPLACE)
                        return
                else:
                    self._finish_recording(RECORD_RESULT_UNEXPECTED, 'Unexpected buffer size %d when up.' % len(self._recording_buffer))
                    return

    def _finish_recording(self, result, result_info_str=None):
        old_recording_hotkey_name = self._recording_hotkey_name
        self._recording_hotkey_name = None
        self.unset_exclusive_keyboard_lock()
        global_data.escape_mgr_agent.unblock(self.__class__.__name__)
        old_recording_buffer = list(self._recording_buffer)
        del self._recording_buffer[:]
        conflict_hotkeys = None
        if result == RECORD_RESULT_REPLACE:
            conflict_hotkeys = hot_key_utils.get_conflict_hotkeys(old_recording_hotkey_name, old_recording_buffer, self._conflict_against_vk_code_list_provider)
        if callable(self._record_finish_cb):
            self._record_finish_cb(result, old_recording_hotkey_name, old_recording_buffer, conflict_hotkeys=conflict_hotkeys)
        self._log('_finish_recording', result, old_recording_hotkey_name, old_recording_buffer, conflict_hotkeys)
        if result_info_str:
            if result == RECORD_RESULT_UNEXPECTED:
                self._log_error(result_info_str)
            else:
                self._log(result_info_str)
        return

    def is_recording(self):
        return self._recording_hotkey_name is not None

    def _key_handler(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            if game.get_key_state(keycode):
                return
        if self.is_recording():
            self.feed_stream(msg, keycode)

    def _log(self, *args):
        if not global_data.is_inner_server:
            return

    def _log_error(self, *args):
        if not global_data.is_inner_server:
            return
        log_error(*args)
        output_str = ''
        for s in args:
            output_str += str(s) + ' '

        global_data.game_mgr.show_tip(output_str)
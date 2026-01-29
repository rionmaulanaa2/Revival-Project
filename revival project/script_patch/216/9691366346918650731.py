# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/KeyboardCtrl.py
from __future__ import absolute_import
import six
from .CtrlKeyboardBase import CtrlKeyboardBase
from common.cfg import confmgr
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook

class KeyboardCtrl(CtrlKeyboardBase):

    def __init__(self):
        self._is_registered = False
        self._need_cache_keycode = set((game.VK_W, game.VK_S, game.VK_A, game.VK_D))
        self.last_has_any_key = False
        self._cache_key_down_handler = []
        super(KeyboardCtrl, self).__init__()

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

    def register_keyboard_callback(self, keycode, msg, callback, hot_key_func_name):
        hot_key_conf = confmgr.get('c_hot_key_config')
        iPriority = hot_key_conf.get(hot_key_func_name, {}).get('cHotKeyPriority', 0)
        if msg == game.MSG_KEY_DOWN:
            self.key_down_func.setdefault(keycode, {})
            self.key_down_func[keycode].setdefault(iPriority, [])
            if callback in self.key_down_func[keycode][iPriority]:
                log_error('There is already the same keycode func for keycode: ', keycode, msg)
            self.key_down_func[keycode][iPriority].append(callback)
        elif msg == game.MSG_KEY_UP:
            self.key_up_func.setdefault(keycode, {})
            self.key_up_func[keycode].setdefault(iPriority, [])
            if callback in self.key_up_func[keycode][iPriority]:
                log_error('There is already the same keycode func for keycode: ', keycode, msg)
            self.key_up_func[keycode][iPriority].append(callback)
        else:
            log_error('unsupport keyboard register!', keycode, msg, callback)

    def unregister_keyboard_callback(self, keycode, msg, callback):
        key_func_map = {}
        has_any_key = False
        if msg == game.MSG_KEY_DOWN:
            key_func_map = self.key_down_func
            has_any_key = keycode == game_hook.ANY_KEY and game_hook.ANY_KEY in key_func_map
        elif msg == game.MSG_KEY_UP:
            key_func_map = self.key_up_func
        if keycode in key_func_map:
            del_iPriority_lst = []
            for iPriority, funcs in six.iteritems(key_func_map[keycode]):
                if callback in funcs:
                    key_func_map[keycode][iPriority].remove(callback)
                    del_iPriority_lst.append(iPriority)
                    break

            for iPriority in del_iPriority_lst:
                if not key_func_map[keycode][iPriority]:
                    del key_func_map[keycode][iPriority]

            if not key_func_map[keycode]:
                del key_func_map[keycode]
            if has_any_key:
                self._key_handler(game.MSG_KEY_UP, keycode)

    def trigger_key_handler(self, keycode, msg):
        key_func_map = {}
        if msg == game.MSG_KEY_DOWN:
            key_func_map = self.key_down_func
        elif msg == game.MSG_KEY_UP:
            key_func_map = self.key_up_func
        self.call_back_key_func(key_func_map, msg, keycode)

    def _key_handler(self, msg, keycode):
        if keycode == game.VK_ESCAPE:
            return
        key_func_map = {}
        if msg == game.MSG_KEY_DOWN:
            key_func_map = self.key_down_func
        elif msg == game.MSG_KEY_UP:
            key_func_map = self.key_up_func
        has_any_key = game_hook.ANY_KEY in key_func_map
        if has_any_key:
            super(KeyboardCtrl, self)._key_handler(msg, game_hook.ANY_KEY)
            game_hook.set_key_states(msg, game_hook.ANY_KEY)
            if msg == game.MSG_KEY_DOWN:
                self.cache_handler_during_any_key(keycode)
                self.last_has_any_key = has_any_key
                return
            self.clear_handler_during_any_key(keycode)
        elif self.last_has_any_key:
            for cache_keycode in self._cache_key_down_handler:
                game.key_states[cache_keycode] = False
                super(KeyboardCtrl, self)._key_handler(game.MSG_KEY_DOWN, cache_keycode)

        else:
            self._cache_key_down_handler = []
        self.last_has_any_key = has_any_key
        super(KeyboardCtrl, self)._key_handler(msg, keycode)

    def cache_handler_during_any_key(self, keycode):
        if keycode not in self._need_cache_keycode:
            return
        if self._cache_key_down_handler and self._cache_key_down_handler[-1] == keycode:
            return
        if keycode in self._cache_key_down_handler:
            self._cache_key_down_handler.remove(keycode)
        self._cache_key_down_handler.append(keycode)

    def clear_handler_during_any_key(self, keycode):
        if keycode not in self._need_cache_keycode:
            return
        if keycode in self._cache_key_down_handler:
            self._cache_key_down_handler.remove(keycode)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/CtrlKeyboardBase.py
from __future__ import absolute_import
import six_ex
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook

class CtrlKeyboardBase(object):
    EXCLUSIVE_KEYBOARD_INSTANCE_LOCK = None

    def __init__(self):
        self.key_up_func = {}
        self.key_down_func = {}
        self._force_disable = False
        self._is_enable = False
        self._is_install = False
        self._wrapped_handler_map = {}

    def destroy(self):
        self.disable()
        self.uninstall()
        self.key_down_func = {}
        self.key_up_func = {}
        self._is_enable = False
        self._is_install = False
        self._wrapped_handler_map.clear()

    def reset(self):
        self.key_down_func = {}
        self.key_up_func = {}

    def _register_keys(self):
        self.add_key_handler(game.MSG_KEY_DOWN, six_ex.keys(self.key_down_func), self._key_handler)
        self.add_key_handler(game.MSG_KEY_UP, six_ex.keys(self.key_up_func), self._key_handler)

    def _unregister_keys(self):
        self.remove_key_handler(game.MSG_KEY_DOWN, six_ex.keys(self.key_down_func), self._key_handler)
        self.remove_key_handler(game.MSG_KEY_UP, six_ex.keys(self.key_up_func), self._key_handler)

    def set_exclusive_keyboard_lock(self):
        CtrlKeyboardBase.EXCLUSIVE_KEYBOARD_INSTANCE_LOCK = self

    def unset_exclusive_keyboard_lock(self):
        if CtrlKeyboardBase.EXCLUSIVE_KEYBOARD_INSTANCE_LOCK == self:
            CtrlKeyboardBase.EXCLUSIVE_KEYBOARD_INSTANCE_LOCK = None
        return

    def add_key_handler(self, msg, key_codes, handler):

        def wrapped(*args, **kwargs):
            lock = CtrlKeyboardBase.EXCLUSIVE_KEYBOARD_INSTANCE_LOCK
            if lock is not None and lock != self:
                return
            else:
                handler(*args, **kwargs)
                return

        self._wrapped_handler_map[handler] = wrapped
        return game_hook.add_key_handler(msg, key_codes, wrapped)

    def remove_key_handler(self, msg, key_codes, handler):
        wrapped = None
        if handler in self._wrapped_handler_map:
            wrapped = self._wrapped_handler_map[handler]
            del self._wrapped_handler_map[handler]
        if wrapped is None:
            return
        else:
            return game_hook.remove_key_handler(msg, key_codes, wrapped)

    def install(self):
        if self._is_install:
            return
        self.on_before_install()
        self._register_keys()
        self._is_install = True
        self.on_install()

    def on_before_install(self):
        pass

    def on_install(self):
        pass

    def uninstall(self):
        if not self._is_install:
            return
        self._unregister_keys()
        self._is_install = False
        self.on_uninstall()

    def on_uninstall(self):
        pass

    def enable(self):
        if self._is_enable:
            return
        self._is_enable = True

    def disable(self):
        if not self._is_enable:
            return
        self._is_enable = False

    def force_disable(self):
        self._force_disable = True

    def cancel_force_disable(self):
        self._force_disable = False

    def _key_handler(self, msg, keycode):
        if not self._is_enable:
            return
        if self._force_disable:
            return
        early_ret = False
        if msg == game.MSG_KEY_DOWN:
            if game.get_key_state(keycode):
                return
            key_func_map = self.key_down_func
        elif msg == game.MSG_KEY_UP:
            key_func_map = self.key_up_func
        else:
            key_func_map = {}
        self.call_back_key_func(key_func_map, msg, keycode)

    def call_back_key_func(self, key_func_map, msg, keycode):
        funcs = key_func_map.get(keycode)
        if funcs:
            gds = global_data.game_mgr.gds
            if gds:
                gds.set_save_energy_mode(False)
            priorities = six_ex.keys(funcs)
            priorities.sort(reverse=True)
            for priority in priorities:
                is_break = False
                for func in funcs[priority]:
                    if type(func) is str:
                        func = getattr(self, func)
                    if callable(func):
                        res = func(msg, keycode)
                        if res is not False:
                            is_break = True

                if is_break:
                    break
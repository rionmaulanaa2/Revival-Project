# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/mouse/CtrlMouseBase.py
from __future__ import absolute_import
import six_ex
import game
import cc
from logic.vscene.parts.ctrl.VirtualCodeComplement import MOUSE_BUTTON_BACK, MOUSE_BUTTON_FORWARD

class CtrlMouseBase(object):

    def __init__(self):
        self.key_down_func = {}
        self.key_up_func = {}
        self._force_disable = False
        self._is_enable = False
        self._is_install = False
        self._cocos_mouse_listener = None
        self._down_keys = set()
        return

    def destroy(self):
        self._unregister_keys()
        self.key_down_func = {}
        self.key_up_func = {}
        self._down_keys.clear()

    def reset(self):
        self.key_down_func = {}
        self.key_up_func = {}

    def _register_keys(self):
        self.register_cocos_mouse_support()

    def _unregister_keys(self):
        import game3d
        self.unregister_cocos_mouse_support()
        self._down_keys.clear()

    def register_cocos_mouse_support(self):
        self.init_cocos_mouse_event()

    def unregister_cocos_mouse_support(self):
        if self._cocos_mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._cocos_mouse_listener)
            self._cocos_mouse_listener = None
        return

    def init_cocos_mouse_event(self):
        listener = cc.EventListenerMouse.create()
        listener.setOnMouseDownCallback(self.on_mouse_down)
        listener.setOnMouseUpCallback(self.on_mouse_up)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithFixedPriority(listener, 999999)
        self._cocos_mouse_listener = listener

    def on_mouse_down(self, event):
        mouse_type = event.getMouseButton()
        if mouse_type == 0:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_LEFT)
        elif mouse_type == 1:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_RIGHT)
        elif mouse_type == 2:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_MIDDLE)
        elif mouse_type == 3:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, MOUSE_BUTTON_BACK)
        elif mouse_type == 4:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, MOUSE_BUTTON_FORWARD)
        else:
            log_error('Unsupported Mouse KEY!', mouse_type)

    def on_mouse_up(self, event):
        mouse_type = event.getMouseButton()
        if mouse_type == 0:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_LEFT)
        elif mouse_type == 1:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_RIGHT)
        elif mouse_type == 2:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_MIDDLE)
        elif mouse_type == 3:
            self.on_mouse_msg(game.MSG_MOUSE_UP, MOUSE_BUTTON_BACK)
        elif mouse_type == 4:
            self.on_mouse_msg(game.MSG_MOUSE_UP, MOUSE_BUTTON_FORWARD)
        else:
            log_error('Unsupported Mouse KEY!', mouse_type)

    def install(self):
        if self._is_install:
            return
        self._register_keys()
        self._is_install = True

    def uninstall(self):
        if not self._is_install:
            return
        self._unregister_keys()
        self._is_install = False

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

    def get_key_state(self, keycode):
        return keycode in self._down_keys

    def on_mouse_msg(self, msg, keycode):
        if msg == game.MSG_MOUSE_DOWN:
            self._down_keys.add(keycode)
        else:
            if msg == game.MSG_MOUSE_UP:
                if keycode in self._down_keys:
                    self._down_keys.remove(keycode)
            if not self._is_enable:
                return
            if self._force_disable:
                return
        if msg == game.MSG_MOUSE_DOWN:
            key_func_map = self.key_down_func
        elif msg == game.MSG_MOUSE_UP:
            key_func_map = self.key_up_func
        else:
            key_func_map = {}
        self.call_back_key_func(key_func_map, msg, keycode)

    def call_back_key_func(self, key_func_map, msg, keycode):
        funcs = key_func_map.get(keycode)
        if funcs:
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
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/mouse/BattleMouse.py
from __future__ import absolute_import
import six
from .CtrlMouseBase import CtrlMouseBase
from common.cfg import confmgr
import game
from logic.vscene.parts.ctrl.KeyboardMouseOperations import KeyboardMouseOperations

class BattleMouse(CtrlMouseBase):

    def register_mouse_callback(self, keycode, msg, callback, hot_key_func_name):
        hot_key_conf = confmgr.get('c_hot_key_config')
        iPriority = hot_key_conf.get(hot_key_func_name, {}).get('cHotKeyPriority', 0)
        if msg == game.MSG_MOUSE_DOWN:
            self.key_down_func.setdefault(keycode, {})
            self.key_down_func[keycode].setdefault(iPriority, [])
            if callback in self.key_down_func[keycode][iPriority]:
                log_error('There is already the same keycode func for keycode: ', keycode, msg)
            self.key_down_func[keycode][iPriority].append(callback)
        elif msg == game.MSG_MOUSE_UP:
            self.key_up_func.setdefault(keycode, {})
            self.key_up_func[keycode].setdefault(iPriority, [])
            if callback in self.key_up_func[keycode][iPriority]:
                log_error('There is already the same keycode func for keycode: ', keycode, msg)
            self.key_up_func[keycode][iPriority].append(callback)
        else:
            log_error('unsupport mouse register!', keycode, msg, callback)

    def unregister_mouse_callback(self, keycode, msg, callback):
        key_func_map = {}
        if msg == game.MSG_MOUSE_DOWN:
            key_func_map = self.key_down_func
        elif msg == game.MSG_MOUSE_UP:
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
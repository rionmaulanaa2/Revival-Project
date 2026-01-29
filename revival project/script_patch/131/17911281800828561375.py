# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/CameraDirectionKeyboardHelper.py
from __future__ import absolute_import
import game
from logic.client.const import camera_const
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import try_claim_shortcut_functionality, try_unclaim_shortcut_functionality, movement_shortcut_names
from data import hot_key_def
from logic.vscene.parts.keyboard.DirectionKeyboardHelper import DirectionKeyboardHelper
import math3d
from logic.gutils import hot_key_utils

class CameraDirectionKeyboardHelper(object):

    def __init__(self):
        self._direction_keyboard_helper = DirectionKeyboardHelper()
        self._move_dir = None
        self._down_keys = set()
        return

    def destroy(self):
        self._down_keys.clear()
        self._direction_keyboard_helper.reset()
        self._direction_keyboard_helper = None
        return

    def reset(self):
        self._move_dir = None
        self._down_keys.clear()
        self._direction_keyboard_helper.reset()
        return

    def move_key_func(self, msg, keycode):
        vertical_direct = math3d.vector(0, 0, 0)
        if msg == game.MSG_KEY_DOWN:
            self._down_keys.add(keycode)
        elif keycode in self._down_keys:
            self._down_keys.remove(keycode)
        if game.VK_NUM_1 in self._down_keys:
            vertical_direct += math3d.vector(0, -1, 0)
        if game.VK_NUM_4 in self._down_keys:
            vertical_direct += math3d.vector(0, 1, 0)
        self._direction_keyboard_helper.on_update_direction(msg, keycode)
        md = self._direction_keyboard_helper.get_md_dir()
        if md is not None:
            hort_move_dir = camera_const.DIR_VECS[md]
            self._move_dir = hort_move_dir + vertical_direct
        else:
            self._move_dir = vertical_direct
        return self._move_dir

    def get_move_direction(self):
        return self._move_dir
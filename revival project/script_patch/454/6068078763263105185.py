# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/DirectionKeyboardHelper.py
from __future__ import absolute_import
import six_ex
import six
import game
from logic.client.const import camera_const
from logic.vscene.parts.ctrl.ShortcutFunctionalityMutex import try_claim_shortcut_functionality, try_unclaim_shortcut_functionality, movement_shortcut_names
from data import hot_key_def

class DirectionKeyboardHelper(object):

    def __init__(self):
        self._total_md = []
        self._cur_md_dir = None
        self._total_keys = []
        self._direction_key_map = {game.VK_W: (
                     camera_const.MOVE_DIR_0, hot_key_def.MOVE_FORWARD),
           game.VK_S: (
                     camera_const.MOVE_DIR_180, hot_key_def.MOVE_BACKWARD),
           game.VK_A: (
                     camera_const.MOVE_DIR_270, hot_key_def.MOVE_LEFT),
           game.VK_D: (
                     camera_const.MOVE_DIR_90, hot_key_def.MOVE_RIGHT)
           }
        return

    def reset(self):
        self._total_md = []
        self._total_keys = []
        self._cur_md_dir = None
        return

    def key_handler_hepler(self, msg, keycode, skip_claim_shortcut_logic=False):
        gamemap = self._direction_key_map
        if keycode in gamemap:
            md, shortcut_func_name = gamemap[keycode]
            exist = md in self._total_md
            if msg == game.MSG_KEY_DOWN:
                if exist:
                    return False
                if global_data.is_pc_mode:
                    if not skip_claim_shortcut_logic:
                        if not try_claim_shortcut_functionality((shortcut_func_name,), 'DirectionKeyboardHelper'):
                            return False
                        empty = len(self._total_md) == 0
                        if empty:
                            ui = global_data.ui_mgr.get_ui('MoveRockerUI')
                            if ui:
                                ui.stop_rocker(need_send=False)
                self._total_md.append(md)
            else:
                if global_data.is_pc_mode:
                    try_unclaim_shortcut_functionality((shortcut_func_name,), 'DirectionKeyboardHelper')
                if not exist:
                    return False
                self._total_md.remove(md)
            mds = list(self._total_md)
            if camera_const.MOVE_DIR_270 in mds and camera_const.MOVE_DIR_90 in mds:
                mds.remove(camera_const.MOVE_DIR_270)
                mds.remove(camera_const.MOVE_DIR_90)
            if camera_const.MOVE_DIR_0 in mds and camera_const.MOVE_DIR_180 in mds:
                mds.remove(camera_const.MOVE_DIR_0)
                mds.remove(camera_const.MOVE_DIR_180)
            self._total_keys = []
            for md in self._total_md:
                for key, value in six.iteritems(self._direction_key_map):
                    map_md, _ = value
                    if md == map_md:
                        self._total_keys.append(key)

            if mds:
                md = sum(mds)
                if camera_const.MOVE_DIR_0 in mds and camera_const.MOVE_DIR_270 in mds:
                    md += camera_const.MOVE_DIR_360
                md //= len(mds)
                self._cur_md_dir = md
                return True
            else:
                self._cur_md_dir = None
                return True

        return False

    def on_update_direction(self, msg, keycode):
        need_update = self.key_handler_hepler(msg, keycode)
        if need_update:
            if self._cur_md_dir is not None:
                return camera_const.DIR_VECS[self._cur_md_dir]
            else:
                return

        return False

    def get_md_dir(self):
        return self._cur_md_dir

    def get_total_keycodes(self):
        return self._total_keys

    def get_direction_keys(self):
        return six_ex.keys(self._direction_key_map)
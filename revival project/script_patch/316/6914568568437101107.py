# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCtrlSimple.py
from __future__ import absolute_import
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from . import ScenePart
from data.camera_state_const import OBSERVE_FREE_MODE
from logic.client.const import camera_const
from logic.client.const.camera_const import FREE_CAMERA_LIST

class PartCtrlSimple(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartCtrlSimple, self).__init__(scene, name)
        self._bind_unit = None
        self._down_reg_keys = [
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_G, game.VK_T, game.VK_R,
         game.VK_V, game.VK_ENTER, game.VK_F, game.VK_SPACE, game.VK_M, game.VK_N, game.VK_LEFT,
         game.VK_RIGHT, game.VK_UP, game.VK_DOWN, game.VK_1, game.VK_2, game.VK_SHIFT,
         game.VK_ALT, game.VK_Z, game.VK_Q]
        self._up_reg_keys = [game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_G, game.VK_T, game.VK_R, game.VK_SHIFT,
         game.VK_ALT, game.VK_Z, game.VK_Q, game.VK_SPACE]
        return

    def on_load(self):
        self.process_bind_events(True)

    def on_enter(self):
        self.register_keys()

    def on_bind(self, unit):
        self._bind_unit = unit

    def on_exit(self):
        self.on_bind(None)
        self.process_bind_events(False)
        return

    def process_bind_events(self, is_bind):
        emgr = global_data.emgr
        events = {'scene_player_setted_event': self.on_bind
           }
        if is_bind:
            emgr.bind_events(events)
        else:
            emgr.unbind_events(events)

    def register_keys(self):
        import game
        game_hook.add_key_handler(game.MSG_KEY_DOWN, self._down_reg_keys, self._key_handler)
        game_hook.add_key_handler(game.MSG_KEY_UP, self._up_reg_keys, self._key_handler)
        self._total_md = []
        self._cur_md_dir = None
        return

    def unregister_keys(self):
        import game
        game_hook.remove_key_handler(game.MSG_KEY_DOWN, self._down_reg_keys, self._key_handler)
        game_hook.remove_key_handler(game.MSG_KEY_UP, self._up_reg_keys, self._key_handler)
        self._total_md = []
        self._cur_md_dir = None
        return

    def _key_handler(self, msg, keycode):
        import game
        state_keys = [
         game.VK_SHIFT]
        gamemap = {game.VK_W: camera_const.MOVE_DIR_0,
           game.VK_S: camera_const.MOVE_DIR_180,
           game.VK_A: camera_const.MOVE_DIR_270,
           game.VK_D: camera_const.MOVE_DIR_90
           }
        player = self._bind_unit
        if msg == game.MSG_KEY_DOWN:
            if keycode in gamemap:
                global_data.keys[keycode] = True
            if keycode in state_keys:
                global_data.keys[keycode] = True
        elif msg == game.MSG_KEY_UP:
            if keycode in gamemap:
                global_data.keys[keycode] = False
            if keycode in state_keys:
                global_data.keys[keycode] = False
        if player is None:
            return
        else:
            from logic.gutils.pc_utils import can_run_debug_key_logic
            if not can_run_debug_key_logic():
                return
            if keycode in gamemap:
                md = gamemap[keycode]
                exist = md in self._total_md
                if msg == game.MSG_KEY_DOWN:
                    if exist:
                        return
                    self._total_md.append(md)
                else:
                    if not exist:
                        return
                    self._total_md.remove(md)
                mds = list(self._total_md)
                if camera_const.MOVE_DIR_270 in mds and camera_const.MOVE_DIR_90 in mds:
                    mds.remove(camera_const.MOVE_DIR_270)
                    mds.remove(camera_const.MOVE_DIR_90)
                if camera_const.MOVE_DIR_0 in mds and camera_const.MOVE_DIR_180 in mds:
                    mds.remove(camera_const.MOVE_DIR_0)
                    mds.remove(camera_const.MOVE_DIR_180)
                if mds:
                    md = sum(mds)
                    if camera_const.MOVE_DIR_0 in mds and camera_const.MOVE_DIR_270 in mds:
                        md += camera_const.MOVE_DIR_360
                    md /= len(mds)
                    self._cur_md_dir = md
                    move_dir = camera_const.DIR_VECS[md]
                    player.send_event('E_MOVE', move_dir)
                else:
                    player.send_event('E_MOVE_STOP')
            return

    def on_touch_slide(self, dx, dy, touches, touch_pos, adjust_sensitivity=True, need_check_speed=True):
        win_w, win_h = global_data.ui_mgr.slide_screen_size.width, global_data.ui_mgr.slide_screen_size.height
        dx *= 1.0 / win_h
        dy *= 1.0 / win_h
        self.rotate_camera(dx, dy)

    def rotate_camera(self, dx, dy, global_delta=True, input_src=camera_const.CAM_ROT_INPUT_SRC_SLIDE):
        import world
        scn = world.get_active_scene()
        com_camera = scn.get_com('PartCameraSimple')
        yaw_res = com_camera.yaw(dx)
        pitch_res = com_camera.pitch(dy * -1)
        cur_state = com_camera.get_cur_camera_state_type()
        player = self._bind_unit
        if cur_state not in FREE_CAMERA_LIST and cur_state != OBSERVE_FREE_MODE:
            if yaw_res:
                player.send_event('E_DELTA_YAW', yaw_res)
            if pitch_res:
                player.send_event('E_DELTA_PITCH', pitch_res)
            if global_delta:
                global_data.emgr.camera_delta_change_event.emit(yaw_res, pitch_res, input_src)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCubemapCapture.py
import time
import math3d
import render
import game3d
from . import ScenePart
WINDOW_SIZE = 1024

class CaptureArgs(object):

    def __init__(self, name, camera_forward, camera_up):
        self.name = name
        self.camera_forward = camera_forward
        self.camera_up = camera_up


g_cap_args_vec = [
 CaptureArgs('pos_z', math3d.vector(0, 0, 1), math3d.vector(0, 1, 0)),
 CaptureArgs('neg_z', math3d.vector(0, 0, -1), math3d.vector(0, 1, 0)),
 CaptureArgs('pos_x', math3d.vector(1, 0, 0), math3d.vector(0, 1, 0)),
 CaptureArgs('neg_x', math3d.vector(-1, 0, 0), math3d.vector(0, 1, 0)),
 CaptureArgs('pos_y', math3d.vector(0, 1, 0), math3d.vector(0, 0, -1)),
 CaptureArgs('neg_y', math3d.vector(0, -1, 0), math3d.vector(0, 0, 1))]

class PartCubemapCapture(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartCubemapCapture, self).__init__(scene, name, True)
        self._last_Frame_args = None
        self._frame_index = 0
        self._capturing = False
        self._last_forward = None
        global_data.block_render_info = True
        return

    def on_enter(self):
        game3d.set_window_size(WINDOW_SIZE, WINDOW_SIZE, 32, game3d.WINDOW_TYPE_NORMAL)
        active_camera = self.scene().active_camera
        active_camera.fov = 90
        active_camera.aspect = 1.0
        game3d.renderdoc_show_overlay(False)
        game3d.show_render_info(False)
        import cc
        cc.Director.getInstance().setDisplayStats(False)
        self.register_keys()

    def begin_capture(self):
        if not self._capturing:
            self._capturing = True
            timestamp = int(time.time())
            self._name = 'capture_%s_' % timestamp
            self._frame_index = 0
            self._last_Frame_args = None
            self._last_forward = self.scene().active_camera.transformation.forward
        return

    def get_next_frame_args(self):
        if self._capturing:
            if len(g_cap_args_vec) <= self._frame_index:
                return None
            return g_cap_args_vec[self._frame_index]
        else:
            return None

    def _capture_cb(self):
        self._frame_index += 1

    def on_update(self, dt):
        if self._capturing:
            next_frame_args = self.get_next_frame_args()
            if next_frame_args:
                if next_frame_args != self._last_Frame_args:
                    cam = self.scene().active_camera
                    cam.set_placement(cam.position, next_frame_args.camera_forward, next_frame_args.camera_up)
                    render.save_screen_to_file(self._name + next_frame_args.name + '.png', render.IFF_PNG, 0, True, self._capture_cb)
                self._last_Frame_args = next_frame_args
            else:
                self._capturing = False
                cam = self.scene().active_camera
                cam.set_placement(cam.position, self._last_forward, math3d.vector(0, 1, 0))
                global_data.game_mgr.show_tip('Finish Capture')

    def register_keys(self):
        import game
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_B,), self._key_handler)

    def unregister_keys(self):
        import game
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_B,), self._key_handler)

    def _key_handler(self, msg, keycode):
        import game
        if keycode == game.VK_B:
            self.begin_capture()
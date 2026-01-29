# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartWinTest.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import world
import weakref
import time
import math3d

class PartWinTest(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartWinTest, self).__init__(scene, name)
        self.move_dir = math3d.vector(0, 0, 0)
        self.speed_up = 1
        self.state = None
        self.need_update = True
        return

    def on_enter(self):
        self.register_keys()

    def register_keys(self):
        import game
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_U, game.VK_I, game.VK_H, game.VK_B,
         game.VK_M, game.VK_N), self._key_handler)
        game.add_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_U, game.VK_I, game.VK_H, game.VK_B,
         game.VK_M, game.VK_N), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    def unregister_keys(self):
        import game
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        game.remove_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def _key_handler(self, msg, keycode):
        print('key handler', msg, keycode)
        import game
        import math
        if msg == game.MSG_KEY_DOWN:
            self.state = keycode
        else:
            self.state = None
        return

    def on_update(self, dt):
        return
        import game
        camera = self.scene().active_camera
        gamemap = {game.VK_W: math3d.vector(0, 0, 1),
           game.VK_S: math3d.vector(0, 0, -1),
           game.VK_A: math3d.vector(-1, 0, 0),
           game.VK_D: math3d.vector(1, 0, 0),
           game.VK_R: math3d.vector(0, 1, 0),
           game.VK_F: math3d.vector(0, -1, 0)
           }
        fov_map = {game.VK_U: 5,
           game.VK_I: -5
           }
        rotatemap = {game.VK_H: (-1, 0),
           game.VK_B: (0, -1),
           game.VK_N: (1, 0),
           game.VK_M: (0, 1)
           }
        move_dir = math3d.vector(0, 0, 0)
        fov_mod = 0
        rotate_mod = (0, 0)
        if self.state and self.state in gamemap:
            move_dir = gamemap[self.state]
        if self.state and self.state in fov_map:
            fov_mod = fov_map[self.state]
        camera.slide(move_dir * (dt * 20))
        camera.fov = camera.fov + fov_mod * dt * 5
        rotate_matrix = camera.world_rotation_matrix
        if self.state and self.state in rotatemap:
            rotate_mod = rotatemap[self.state]
            rotate_y = math3d.matrix.make_rotation_y(rotate_mod[1] * dt)
            rotate_x = math3d.matrix.make_rotation_x(rotate_mod[0] * dt)
            rotate_matrix = rotate_matrix * rotate_x
            rotate_matrix = rotate_matrix * rotate_y
            camera.world_rotation_matrix = rotate_matrix

    def on_exit(self):
        self.unregister_keys()
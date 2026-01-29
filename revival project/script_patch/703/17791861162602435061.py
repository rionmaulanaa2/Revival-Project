# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCameraFreeFly.py
from __future__ import absolute_import
from __future__ import print_function
from . import PartTestBase
import math3d
import world
import game
import time
import logic.gevent
import render
import game3d
import random
import collision
import cython_test
from logic.gcommon.common_const import collision_const
from logic.gcommon.common_const.collision_const import TERRAIN_GROUP, GLASS_GROUP, WOOD_GROUP, METAL_GROUP, STONE_GROUP

class PartCameraFreeFly(PartTestBase.PartTestBase):
    GameMap = {game.VK_W: math3d.vector(0, 0, 1),
       game.VK_S: math3d.vector(0, 0, -1),
       game.VK_A: math3d.vector(-1, 0, 0),
       game.VK_D: math3d.vector(1, 0, 0),
       game.VK_R: math3d.vector(0, 1, 0),
       game.VK_F: math3d.vector(0, -1, 0)
       }

    def __init__(self, scene, name):
        super(PartCameraFreeFly, self).__init__(scene, name, True)
        self.cur_camera_state_type = None
        self.move_dir = math3d.vector(0, 0, 0)
        self.speed_up = 6
        self._is_touch_moving = False
        self._col = None
        global_data.game_mgr.remove_patch_ui()
        game3d.set_frame_rate(1000)
        global_data.is_inner_server = 1
        return

    def init_camera(self):
        self.cam = self.scene().active_camera
        self.cam.z_range = (0.01, 10000)

    def on_pre_load(self):
        self.scene().active_camera.set_placement(math3d.vector(0, 777, 0), math3d.vector(0.151197, 0.034526, 0.9879), math3d.vector(0, 1, 0))
        self.scene().active_camera.position = math3d.vector(0, 400, 0)
        self.scene().viewer_position = self.scene().active_camera.position
        self.tmp_time = time.time()

    def on_enter(self):
        self.register_keys()
        self.init_camera()
        game3d.show_render_info(True, 4, game3d.get_window_size()[1] - 15)
        game3d.set_frame_rate(1000)

    def _on_gtrace_timeout(self):
        import gtrace
        gtrace.stop('/sdcard/prof.gt')
        global_data.game_mgr.show_tip('Finished profile\xef\xbc\x8coutput result to /sdcard/prof.gt')
        from common.utils.timer import RELEASE
        return RELEASE

    def on_exit(self):
        self.unregister_keys()

    def on_touch_begin(self, touches):
        self._touch_moving_timer = global_data.game_mgr.get_logic_timer().register(func=self._begin_moving, interval=30, times=1)
        self._df = 0

    def on_touch_slide--- This code section failed: ---

 105       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'rotate_camera'
           6  LOAD_FAST             1  'dx'
           9  LOAD_CONST            1  0.01
          12  BINARY_MULTIPLY  
          13  LOAD_FAST             2  'dy'
          16  LOAD_CONST            1  0.01
          19  BINARY_MULTIPLY  
          20  CALL_FUNCTION_2       2 
          23  POP_TOP          

 106      24  LOAD_GLOBAL           1  'hasattr'
          27  LOAD_GLOBAL           2  'abs'
          30  CALL_FUNCTION_2       2 
          33  POP_JUMP_IF_FALSE   135  'to 135'

 107      36  LOAD_GLOBAL           2  'abs'
          39  LOAD_FAST             1  'dx'
          42  CALL_FUNCTION_1       1 
          45  LOAD_GLOBAL           2  'abs'
          48  LOAD_FAST             2  'dy'
          51  CALL_FUNCTION_1       1 
          54  BINARY_ADD       
          55  LOAD_FAST             0  'self'
          58  LOAD_ATTR             3  '_df'
          61  BINARY_ADD       
          62  STORE_FAST            5  'distance'

 108      65  LOAD_FAST             5  'distance'
          68  LOAD_CONST            3  10
          71  COMPARE_OP            4  '>'
          74  POP_JUMP_IF_FALSE   123  'to 123'
          77  LOAD_GLOBAL           1  'hasattr'
          80  LOAD_GLOBAL           4  'global_data'
          83  CALL_FUNCTION_2       2 
        86_0  COME_FROM                '74'
          86  POP_JUMP_IF_FALSE   123  'to 123'

 109      89  LOAD_GLOBAL           4  'global_data'
          92  LOAD_ATTR             5  'game_mgr'
          95  LOAD_ATTR             6  'get_logic_timer'
          98  CALL_FUNCTION_0       0 
         101  LOAD_ATTR             7  'unregister'
         104  LOAD_FAST             0  'self'
         107  LOAD_ATTR             8  '_touch_moving_timer'
         110  CALL_FUNCTION_1       1 
         113  POP_TOP          

 110     114  LOAD_FAST             0  'self'
         117  DELETE_ATTR           8  '_touch_moving_timer'
         120  JUMP_FORWARD          0  'to 123'
       123_0  COME_FROM                '120'

 111     123  LOAD_FAST             5  'distance'
         126  LOAD_FAST             0  'self'
         129  STORE_ATTR            3  '_df'
         132  JUMP_FORWARD          0  'to 135'
       135_0  COME_FROM                '132'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 30

    def on_touch_end--- This code section failed: ---

 114       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'global_data'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'

 115      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'get_logic_timer'
          21  CALL_FUNCTION_0       0 
          24  LOAD_ATTR             4  'unregister'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             5  '_touch_moving_timer'
          33  CALL_FUNCTION_1       1 
          36  POP_TOP          

 116      37  LOAD_FAST             0  'self'
          40  DELETE_ATTR           5  '_touch_moving_timer'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'

 117      46  LOAD_GLOBAL           6  'False'
          49  LOAD_FAST             0  'self'
          52  STORE_ATTR            7  '_is_touch_moving'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def _begin_moving--- This code section failed: ---

 120       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'global_data'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'

 121      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'get_logic_timer'
          21  CALL_FUNCTION_0       0 
          24  LOAD_ATTR             4  'unregister'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             5  '_touch_moving_timer'
          33  CALL_FUNCTION_1       1 
          36  POP_TOP          

 122      37  LOAD_FAST             0  'self'
          40  DELETE_ATTR           5  '_touch_moving_timer'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'

 123      46  LOAD_GLOBAL           6  'True'
          49  LOAD_FAST             0  'self'
          52  STORE_ATTR            7  '_is_touch_moving'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def rotate_camera(self, dx, dy):
        mat = math3d.matrix.make_rotation_y(dx)
        self.cam.rotation_matrix *= mat
        self.cam.rotate_x(dy * -0.5)

    def forward_camera(self, dx, dy):
        pass

    def register_keys(self):
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_P, game.VK_O), self._key_handler)
        game.add_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_P, game.VK_O), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    def unregister_keys(self):
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_P, game.VK_O), self._key_handler)
        game.remove_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN, game.VK_P, game.VK_O), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    def delay_destroy(self, model):
        model.set_mask_and_group(0, 0)
        model.destroy()

    def test_ragdoll(self, model, *args):
        self.scene().add_object(model)
        model.world_transformation = self.scene().active_camera.world_transformation
        model.physics_enable = True
        model.set_mask_and_group(collision_const.GROUP_CHARACTER_INCLUDE & ~collision_const.GROUP_CAMERA_COLL, collision_const.GROUP_CHARACTER_INCLUDE & ~collision_const.GROUP_CAMERA_COLL)
        model.set_no_mutual_ragdoll(True)
        model.enable_ccd(True)
        global_data.game_mgr.get_logic_timer().register(func=self.delay_destroy, args=(model,), interval=5, times=1, mode=2)

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def _key_handler(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            if keycode in self.GameMap and keycode not in self._total_md:
                self._total_md.add(keycode)
        elif keycode in self.GameMap and keycode in self._total_md:
            self._total_md.remove(keycode)
        elif game.VK_UP == keycode:
            self.speed_up += 60
            print('increase speed')
        elif game.VK_DOWN == keycode:
            print('down speed')
            self.speed_up = max(1, self.speed_up - 6)
        elif keycode == game.VK_P:
            is_show_col = not getattr(global_data, 'show_col', False)
            scene = world.get_active_scene()
            col_scn = scene.scene_col
            col_scn.drawing = is_show_col
            if is_show_col:
                col_scn.drawing_radius = 1000
                col_scn.drawing_center = scene.viewer_position
            global_data.show_col = is_show_col
        elif keycode == game.VK_O:
            if self._col is None:
                col = collision.col_object(collision.BOX, math3d.vector(1, 1, 1))
                self._col = col
            scene = self.scene()
            start_pos = self.cam.position
            end_pos = start_pos + self.cam.transformation.forward * 100
            ret = scene.scene_col.sweep_test(self._col, start_pos, end_pos)
            if ret[0]:
                print('dir', self.cam.transformation.forward)
                print('hit', ret)
            else:
                print('hit none')
        return

    def on_update(self, dt):
        if self._is_touch_moving:
            move_dir = math3d.vector(0, 0, 1)
        else:
            move_dir = math3d.vector(0, 0, 0)
            for keycode in self._total_md:
                move_dir += self.GameMap[keycode]

        if move_dir.length > 0.001:
            move_dir.normalize()
            self.cam.slide(move_dir * dt * 3.0 * self.speed_up)
            self.scene().viewer_position = self.cam.position
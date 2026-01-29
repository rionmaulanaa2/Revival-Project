# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCalcLumensManager.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from . import ScenePart
import math
import math3d
import world
import game
import game3d
import time
import render
import six.moves.cPickle
import collision
import os
import traceback
import struct
import shutil
from hdr_tool.hdr_sample_generator import HDRSampleGenerator
from hdr_tool.hdr_lumens_const import CHUNK_SIZE, LUMENS_DIR, LUMENS_COUNT_DIR, XRANGE, YRANGE
PADDING_LEVEL = {0: 208,
   1: 104,
   2: 52,
   3: 16
   }

class PartCalcLumensManager(ScenePart.ScenePart):
    GameMap = {game.VK_W: math3d.vector(0, 0, 1),
       game.VK_S: math3d.vector(0, 0, -1),
       game.VK_A: math3d.vector(-1, 0, 0),
       game.VK_D: math3d.vector(1, 0, 0),
       game.VK_R: math3d.vector(0, 1, 0),
       game.VK_F: math3d.vector(0, -1, 0)
       }
    DIR_MATRIX = [
     math3d.matrix.make_orient(math3d.vector(1, 0, 0), math3d.vector(0, 1, 0)),
     math3d.matrix.make_orient(math3d.vector(-1, 0, 0), math3d.vector(0, 1, 0)),
     math3d.matrix.make_orient(math3d.vector(0, 1, 0), math3d.vector(1, 0, 0)),
     math3d.matrix.make_orient(math3d.vector(0, -1, 0), math3d.vector(1, 0, 0)),
     math3d.matrix.make_orient(math3d.vector(0, 0, 1), math3d.vector(0, 1, 0)),
     math3d.matrix.make_orient(math3d.vector(0, 0, -1), math3d.vector(0, 1, 0)),
     math3d.matrix.make_orient(math3d.vector(0.74, 0.26, 0.61), math3d.vector(-0.2, 0.96, -0.17)),
     math3d.matrix.make_orient(math3d.vector(-0.69, 0.24, 0.68), math3d.vector(0.17, 0.97, -0.17)),
     math3d.matrix.make_orient(math3d.vector(-0.7, 0.21, -0.67), math3d.vector(0.16, 0.98, 0.15)),
     math3d.matrix.make_orient(math3d.vector(0.67, 0.27, -0.69), math3d.vector(-0.19, 0.96, 0.2))]

    def __init__(self, scene, name):
        super(PartCalcLumensManager, self).__init__(scene, name, True)
        self.cur_camera_state_type = None
        self.move_dir = math3d.vector(0, 0, 0)
        self.speed_up = 10
        self._is_touch_moving = False
        self.is_output_light = False
        self.clogic = None
        self.hdr_generator = HDRSampleGenerator()
        self.cur_x_index = None
        self.cur_z_index = None
        self.cur_y = None
        self.chunk_lights = {}
        self.all_load_chunk_lights = {}
        self.cur_factor = 1
        self.target_factor = 1
        global_data.emgr.scene_after_enter_event += self.init_lumens_manager
        return

    def on_enter(self):
        self.register_keys()
        self.init_camera()

    def init_lumens_manager(self):
        self.hdr_generator.init_scene(self.scene())
        global_data.game_mgr.scene.set_tone_factor(1)
        global_data.display_agent.set_post_effect_active('hdr', False)
        global_data.display_agent.set_post_effect_active('hdr_tonemap', False)
        global_data.display_agent.set_post_effect_active('CalcBright', True)
        render.set_end_of_frame(self.end_of_frame)
        render.end_of_frame = self.end_of_frame
        game3d.show_render_info(True, 0, 0)
        self.init_lumens_dir()
        self.gen_chunk()

    def init_lumens_dir(self):
        if not os.path.exists(LUMENS_DIR):
            os.makedirs(LUMENS_DIR)
        if not os.path.exists(LUMENS_COUNT_DIR):
            os.makedirs(LUMENS_COUNT_DIR)

    def on_exit(self):
        self.unregister_keys()

    def on_pre_load(self):
        self.scene().viewer_position = self.scene().active_camera.position

    def register_keys(self):
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        game.add_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    def unregister_keys(self):
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        game.remove_key_handler(game.MSG_KEY_UP, (
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_R, game.VK_F, game.VK_UP, game.VK_DOWN), self._key_handler)
        self._total_md = set()
        self.move_dir = math3d.vector(0, 0, 0)

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def _key_handler(self, msg, keycode):
        if msg == game.MSG_KEY_DOWN:
            if keycode in self.GameMap and keycode not in self._total_md:
                self._total_md.add(keycode)
        elif keycode in self.GameMap and keycode in self._total_md:
            self._total_md.remove(keycode)
        elif game.VK_UP == keycode:
            self.speed_up += 10
        elif game.VK_DOWN == keycode:
            self.speed_up = max(1, self.speed_up - 10)

    def init_camera(self):
        self.cam = self.scene().active_camera
        self.cam.transformation = self.scene().get_preset_camera('cam2')
        scn = self.scene()
        scn.landscape.set_LandscapeViewRange(100000)
        scn.landscape.set_LandscapeColRange(100000)
        scn.landscape.screen_space_error_bound = 150.0

    def on_touch_begin(self, touches):
        self._touch_moving_timer = global_data.game_mgr.get_logic_timer().register(func=self._begin_moving, interval=30, times=1)
        self._last_touch_location = touches[0].getLocation()

    def on_touch_slide--- This code section failed: ---

 185       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'rotate_camera'
           6  LOAD_FAST             1  'dx'
           9  LOAD_CONST            1  0.01
          12  BINARY_MULTIPLY  
          13  LOAD_FAST             2  'dy'
          16  LOAD_CONST            1  0.01
          19  BINARY_MULTIPLY  
          20  CALL_FUNCTION_2       2 
          23  POP_TOP          

 186      24  LOAD_GLOBAL           1  'hasattr'
          27  LOAD_GLOBAL           2  'getLocation'
          30  CALL_FUNCTION_2       2 
          33  POP_JUMP_IF_FALSE   125  'to 125'

 187      36  LOAD_FAST             3  'touches'
          39  LOAD_CONST            3  ''
          42  BINARY_SUBSCR    
          43  LOAD_ATTR             2  'getLocation'
          46  CALL_FUNCTION_0       0 
          49  LOAD_ATTR             3  'distance'
          52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             4  '_last_touch_location'
          58  CALL_FUNCTION_1       1 
          61  STORE_FAST            5  'distance'

 188      64  LOAD_FAST             5  'distance'
          67  LOAD_CONST            4  10
          70  COMPARE_OP            4  '>'
          73  POP_JUMP_IF_FALSE   125  'to 125'
          76  LOAD_GLOBAL           1  'hasattr'
          79  LOAD_GLOBAL           5  'global_data'
          82  CALL_FUNCTION_2       2 
        85_0  COME_FROM                '73'
          85  POP_JUMP_IF_FALSE   125  'to 125'

 189      88  LOAD_GLOBAL           5  'global_data'
          91  LOAD_ATTR             6  'game_mgr'
          94  LOAD_ATTR             7  'get_logic_timer'
          97  CALL_FUNCTION_0       0 
         100  LOAD_ATTR             8  'unregister'
         103  LOAD_FAST             0  'self'
         106  LOAD_ATTR             9  '_touch_moving_timer'
         109  CALL_FUNCTION_1       1 
         112  POP_TOP          

 190     113  LOAD_FAST             0  'self'
         116  DELETE_ATTR           9  '_touch_moving_timer'
         119  JUMP_ABSOLUTE       125  'to 125'
         122  JUMP_FORWARD          0  'to 125'
       125_0  COME_FROM                '122'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 30

    def on_touch_end--- This code section failed: ---

 193       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'global_data'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'

 194      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'get_logic_timer'
          21  CALL_FUNCTION_0       0 
          24  LOAD_ATTR             4  'unregister'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             5  '_touch_moving_timer'
          33  CALL_FUNCTION_1       1 
          36  POP_TOP          

 195      37  LOAD_FAST             0  'self'
          40  DELETE_ATTR           5  '_touch_moving_timer'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'

 196      46  LOAD_GLOBAL           0  'hasattr'
          49  LOAD_GLOBAL           2  'game_mgr'
          52  CALL_FUNCTION_2       2 
          55  POP_JUMP_IF_FALSE    67  'to 67'

 197      58  LOAD_FAST             0  'self'
          61  DELETE_ATTR           6  '_last_touch_location'
          64  JUMP_FORWARD          0  'to 67'
        67_0  COME_FROM                '64'

 198      67  LOAD_GLOBAL           7  'False'
          70  LOAD_FAST             0  'self'
          73  STORE_ATTR            8  '_is_touch_moving'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def _begin_moving--- This code section failed: ---

 201       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'global_data'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    46  'to 46'

 202      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'game_mgr'
          18  LOAD_ATTR             3  'get_logic_timer'
          21  CALL_FUNCTION_0       0 
          24  LOAD_ATTR             4  'unregister'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             5  '_touch_moving_timer'
          33  CALL_FUNCTION_1       1 
          36  POP_TOP          

 203      37  LOAD_FAST             0  'self'
          40  DELETE_ATTR           5  '_touch_moving_timer'
          43  JUMP_FORWARD          0  'to 46'
        46_0  COME_FROM                '43'

 204      46  LOAD_GLOBAL           6  'True'
          49  LOAD_FAST             0  'self'
          52  STORE_ATTR            7  '_is_touch_moving'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def rotate_camera(self, dx, dy):
        mat = math3d.matrix.make_rotation_y(dx)
        self.cam.rotation_matrix *= mat
        self.cam.rotate_x(dy * -0.5)

    def forward_camera(self, dx, dy):
        pass

    def end_of_frame(self):
        if self.is_output_light:
            self.is_output_light = False
            if self.cur_x_index is not None and self.cur_z_index is not None:
                if self.cur_y is not None:
                    if (
                     self.cur_x_index, self.cur_z_index) not in self.chunk_lights:
                        self.chunk_lights[self.cur_x_index, self.cur_z_index] = {}
                    if self.cur_y not in self.chunk_lights[self.cur_x_index, self.cur_z_index]:
                        self.chunk_lights[self.cur_x_index, self.cur_z_index][self.cur_y] = []
                    bright = render.get_cur_bright()
                    bright = 256 * bright / float(512 + bright)
                    self.chunk_lights[self.cur_x_index, self.cur_z_index][self.cur_y].append(bright)
        return

    def gen_chunk_logic(self):
        self.chunks = [ (x, y) for x in range(*XRANGE) for y in range(*YRANGE) ]
        level_count_list = [
         0, 0, 0, 0]
        scn = self.scene()
        if not scn:
            return
        else:
            for chunk_x, chunk_z in self.chunks:
                if os.path.exists('%s/%d_%d.lumen' % (LUMENS_DIR, chunk_x, chunk_z)):
                    continue
                center_x = chunk_x * CHUNK_SIZE
                center_z = chunk_z * CHUNK_SIZE
                cur_viewer_pos = math3d.vector(center_x, 1000, center_z)
                scn.viewer_position = cur_viewer_pos
                self.cam.world_position = cur_viewer_pos
                print('check scene node start-------------------------------------------------')
                print('chunk start', chunk_x, chunk_z)
                print(cur_viewer_pos, 'cur_viewer_pos')
                while not scn.check_scene_node(cur_viewer_pos) or scn.landscape.is_loading_detail_collision():
                    yield

                print('check scene node end--------------------------------------------------')
                self.chunk_lights = {}
                padding = self.hdr_generator.padding
                half_padding = self.hdr_generator.half_padding
                human_height = self.hdr_generator.human_height
                sample_range = self.hdr_generator.sample_range
                chunk_size = self.hdr_generator.chunk_size
                start_x = (chunk_x - 0.5) * chunk_size
                start_z = (chunk_z - 0.5) * chunk_size
                padding = 208
                self.chunk_lights = {}
                sample_points_y = self.hdr_generator.generate_chunk_sample_points(chunk_x, chunk_z, padding)
                sample_range = chunk_size / padding
                half_padding = padding / 2
                if not sample_points_y:
                    print(chunk_x, chunk_z, 'lumens not exist!!!')
                    continue
                for i in range(sample_range):
                    for j in range(sample_range):
                        heights = sample_points_y[i, j]
                        cur_x = start_x + i * padding + half_padding
                        cur_z = start_z + j * padding + half_padding
                        self.cur_x_index = i
                        self.cur_z_index = j
                        for height in heights:
                            self.cur_y = height
                            self.cam.position = math3d.vector(cur_x, self.cur_y + human_height, cur_z)
                            scn.viewer_position = math3d.vector(cur_x, self.cur_y + human_height, cur_z)
                            for k in range(10):
                                self.cam.rotation_matrix = self.DIR_MATRIX[k]
                                self.is_output_light = True
                                yield

                level = self.get_chunk_light_level(self.chunk_lights)
                level_count_list[level] += 1
                if level == 0:
                    self.save_chunk_lights(self.chunk_lights, chunk_x, chunk_z, padding)
                else:
                    padding = PADDING_LEVEL.get(level, 16)
                    self.chunk_lights = {}
                    sample_points_y = self.hdr_generator.generate_chunk_sample_points(chunk_x, chunk_z, padding)
                    sample_range = chunk_size / padding
                    half_padding = padding / 2
                    for i in range(sample_range):
                        for j in range(sample_range):
                            heights = sample_points_y[i, j]
                            cur_x = start_x + i * padding + half_padding
                            cur_z = start_z + j * padding + half_padding
                            self.cur_x_index = i
                            self.cur_z_index = j
                            for height in heights:
                                self.cur_y = height
                                self.cam.position = math3d.vector(cur_x, self.cur_y + human_height, cur_z)
                                scn.viewer_position = math3d.vector(cur_x, self.cur_y + human_height, cur_z)
                                for k in range(10):
                                    self.cam.rotation_matrix = self.DIR_MATRIX[k]
                                    self.is_output_light = True
                                    yield

                self.cur_x_index = None
                self.cur_z_index = None
                self.cur_y = None
                self.save_chunk_lights(self.chunk_lights, chunk_x, chunk_z, padding)
                self.chunk_lights = {}

            return

    def get_chunk_light_level(self, chunk_lights):
        dir_lights = [ [] for i in range(10) ]
        if chunk_lights:
            for i in range(52):
                for j in range(52):
                    if (
                     i, j) in chunk_lights:
                        same_y_height_lights = chunk_lights[i, j]
                        for y_lights in six.itervalues(same_y_height_lights):
                            for yl_i, yl in enumerate(y_lights):
                                dir_lights[yl_i].append(yl)

            ave_diff_list = []
            for i in range(len(dir_lights)):
                total_light = 0
                for light in dir_lights[i]:
                    total_light += light

                ave_light = total_light / len(dir_lights[i])
                total_diff = 0
                for light in dir_lights[i]:
                    total_diff += math.pow(light - ave_light, 2)

                ave_diff = total_diff / len(dir_lights)
                ave_diff_list.append(ave_diff)

            return self.calc_chunk_level(ave_diff_list)
        else:
            return None

    def calc_chunk_level(self, ave_diff_list):
        count_5 = 0
        count_50 = 0
        count_100 = 0
        count_1000 = 0
        for i, ave_diff in enumerate(ave_diff_list):
            if i == 2 or i == 3:
                continue
            if ave_diff <= 5:
                count_5 += 1
            elif ave_diff <= 50:
                count_50 += 1
            elif ave_diff <= 100:
                count_100 += 1
            else:
                count_1000 += 1

        if count_5 >= 6:
            return 0
        else:
            if count_5 + count_50 >= 6:
                return 1
            if count_5 + count_50 + count_100 >= 6:
                return 2
            return 3

    def save_chunk_lights(self, chunk_lights, chunk_x, chunk_z, padding):
        import struct
        xlength = self.hdr_generator.chunk_size / padding
        ylength = self.hdr_generator.chunk_size / padding
        f = open('%s/%d_%d.lumen' % (LUMENS_DIR, chunk_x, chunk_z), 'wb')
        f.write(struct.pack('<i', padding))
        f.write(struct.pack('<b', xlength))
        f.write(struct.pack('<b', ylength))
        for i in range(xlength):
            for j in range(ylength):
                same_xz_lights = chunk_lights[i, j]
                print(len(same_xz_lights))
                f.write(struct.pack('<b', len(same_xz_lights)))
                for y_height in same_xz_lights:
                    lights = same_xz_lights[y_height]
                    f.write(struct.pack('<f', y_height))
                    f.write(struct.pack('10B', *lights))

        print('save_chunk_lights')
        f.close()

    def load_chunk_light_by_index(self, x, y):
        import struct
        import os
        if not os.path.exists('%s/%d_%d.lumen' % (LUMENS_DIR, x, y)):
            return
        f = open('%s/%d_%d.lumen' % (LUMENS_DIR, x, y), 'rb')
        data = f.read()
        f.close()
        padding = struct.unpack('<i', data[:4])
        print(padding)
        data = data[4:]
        xlength, ylength = struct.unpack('<2b', data[:2])
        data = data[2:]
        wb_chunk_lights = {}
        for i in range(xlength):
            for j in range(ylength):
                wb_chunk_lights[i, j] = {}
                same_xz_length = struct.unpack('<b', data[:1])[0]
                data = data[1:]
                for k in range(same_xz_length):
                    yheight = struct.unpack('<f', data[:4])[0]
                    data = data[4:]
                    lights = struct.unpack('<10B', data[:10])
                    data = data[10:]
                    lights = [ light * 4.0 for light in lights ]
                    wb_chunk_lights[i, j][yheight] = lights

        self.all_load_chunk_lights[x, y] = wb_chunk_lights
        print(wb_chunk_lights)
        print(len(wb_chunk_lights))

    def gen_chunk(self):
        game3d.set_frame_rate(1000)
        self.clogic = self.gen_chunk_logic()

    def on_update(self, dt):
        if self._is_touch_moving:
            move_dir = math3d.vector(0, 0, 1)
        else:
            move_dir = math3d.vector(0, 0, 0)
            for keycode in self._total_md:
                move_dir += self.GameMap[keycode]

        if move_dir.length > 0.001:
            move_dir.normalize()
            self.cam.slide(move_dir * dt * 300.0)
            self.scene().viewer_position = self.cam.position
        if self.clogic:
            try:
                next(self.clogic)
            except StopIteration:
                self.clogic = None
            except Exception as err:
                print(err, '@@@@@@')
                self.clogic = None
                traceback.print_stack()

        return
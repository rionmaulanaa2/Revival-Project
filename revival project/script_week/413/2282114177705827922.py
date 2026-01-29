# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTest.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from . import PartTestBase
import math3d
import time

class PartTest(PartTestBase.PartTestBase):

    def __init__(self, scene, name):
        super(PartTest, self).__init__(scene, name)
        self.body0 = None
        self._tap_func = None
        return

    def on_pre_load(self):
        self.scene().active_camera.transformation = self.scene().get_preset_camera('cam')
        self.scene().viewer_position = self.scene().active_camera.position

    def test_character_h(self):
        import world
        scn = self.scene()

    def test_merge_tex(self):
        import world
        import math3d
        scn = self.scene()
        merge_info = world.model_merge_tex(1024, 0)
        merge_info.add_tex_param('Tex0')
        merge_info.add_tex_param('NormalMap')
        merge_info.add_tex_param('TexMetallic')
        merge_info.add_mesh_file('character/b_m_3001/b_m_3001_head.gim', 0)
        merge_info.add_mesh_file('character/b_m_3001/b_m_3001_body_upper.gim', 2)
        merge_info.add_mesh_file('character/b_m_3001/b_m_3001_body_lower.gim', 3)

        def cb(model, user_data, task):
            scn.add_object(model)

        world.create_model_async('character/b_m_3001/b_m_3001_head.gim', cb, None, 2, merge_info)
        return

    def test_merge_tex_manual(self):
        import world
        import math3d
        scn = self.scene()
        merge_info = world.model_merge_tex(1024, 0)
        merge_info.add_tex_param('Tex0')
        merge_info.add_tex_param('NormalMap')
        merge_info.add_tex_param('TexMetallic')
        merge_info.add_mesh_file('character/b_m_3001/b_m_3001_head.gim', 0)
        body = world.model('character/b_m_3001/b_m_3001_head.gim', scn, True, merge_info)
        body.add_mesh('character/b_m_3001/b_m_3001_body_upper.gim', 2)
        body.add_mesh('character/b_m_3001/b_m_3001_body_lower.gim', 3)
        body.add_mesh('character/b_m_3001/b_m_3001_hair.gim', 7)
        body.remove_mesh('character/b_m_3001/b_m_3001_hair.gim')
        body.add_mesh('character/b_m_3001/b_m_3001_hair.gim', 7)

    def test_shoot_collision(self):
        import world
        import math3d
        import game3d
        scn = world.get_active_scene()
        model = world.model('model_new\\mecha\\8006\\8006\\hit.gim', scn)
        model.enable_debugdraw(True, 2)
        window = game3d.get_window_size()
        draw_obj = [None]

        def tap(touch):
            lo = touch.getLocation()
            x, y = lo.x, window[1] - lo.y
            p, d = self.scene().active_camera.screen_to_world(x, y)
            print('touch', x, y)
            print('ray', p, d)
            print(model.hit_by_ray2(math3d.vector(0, 100, -400), math3d.vector(0, 0, 1000)))
            obj = world.primitives(scn)
            color = 65280
            obj.create_line([((p,), (p + d,), color)])
            if draw_obj[0]:
                draw_obj[0].destroy()
            draw_obj[0] = obj

        self._tap_func = tap
        scn.active_camera.set_placement(math3d.vector(0, 0, -400), math3d.vector(0, 0, 1), math3d.vector(0, 1, 0))
        return

    def test_new_character(self):
        import world
        import math3d
        scn = self.scene()
        scn.background_color = 2
        model = world.model('character/cs/cs.gim', scn)
        model.position = math3d.vector(0, -10, 30)

    def test_nothing(self):
        pass

    def test_springbone(self):
        import world
        scn = self.scene()
        model = world.model('character/11/2000/11_2000_hair_l.gim', scn)
        air_friction = 0.1
        damping = 0.97
        max_ratio = 1.0
        stiffness = 1.0
        anim = model.get_spring_anim(True)
        anim.set_physx_constants(air_friction, damping, 30, 1)
        for i in range(22, 30):
            anim.add_spring_anim('biped_bone{}'.format(i), max_ratio, stiffness, 1)

        anim.enable_physx()
        model.play_animation('emptyhand_run', -1.0, 16, 0, 1)

    def show_debug_scene_mark--- This code section failed: ---

 142       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'scene_debug_mark_list'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     24  'to 24'

 143      12  BUILD_LIST_0          0 
          15  LOAD_FAST             0  'self'
          18  STORE_ATTR            1  'scene_debug_mark_list'
          21  JUMP_FORWARD          0  'to 24'
        24_0  COME_FROM                '21'

 145      24  LOAD_CLOSURE          0  'color'
          30  LOAD_CONST               '<code_object _get_scene_world_mark_space_obj>'
          33  MAKE_CLOSURE_0        0 
          36  STORE_FAST            3  '_get_scene_world_mark_space_obj'

 160      39  LOAD_FAST             3  '_get_scene_world_mark_space_obj'
          42  CALL_FUNCTION_0       0 
          45  STORE_FAST            4  'scene_debug_mark'

 161      48  LOAD_FAST             1  'pos'
          51  LOAD_FAST             4  'scene_debug_mark'
          54  STORE_ATTR            2  'world_position'

 162      57  LOAD_GLOBAL           3  'True'
          60  LOAD_FAST             4  'scene_debug_mark'
          63  STORE_ATTR            4  'top_most'

 163      66  LOAD_FAST             0  'self'
          69  LOAD_ATTR             1  'scene_debug_mark_list'
          72  LOAD_ATTR             5  'append'
          75  LOAD_FAST             4  'scene_debug_mark'
          78  CALL_FUNCTION_1       1 
          81  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def clear_debug_scene_mark--- This code section failed: ---

 166       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'scene_debug_mark_list'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    54  'to 54'

 167      12  SETUP_LOOP           27  'to 42'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'scene_debug_mark_list'
          21  GET_ITER         
          22  FOR_ITER             16  'to 41'
          25  STORE_FAST            1  'scene_mark'

 168      28  LOAD_FAST             1  'scene_mark'
          31  LOAD_ATTR             2  'remove_from_parent'
          34  CALL_FUNCTION_0       0 
          37  POP_TOP          
          38  JUMP_BACK            22  'to 22'
          41  POP_BLOCK        
        42_0  COME_FROM                '12'

 169      42  BUILD_LIST_0          0 
          45  LOAD_FAST             0  'self'
          48  STORE_ATTR            1  'scene_debug_mark_list'
          51  JUMP_FORWARD          0  'to 54'
        54_0  COME_FROM                '51'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def test_sfx(self):
        import world
        import math3d
        from common.utils import timer
        scn = self.scene()
        scn.background_color = 3355443
        model = world.sfx('effect/fx/mecha/8004/8004_fx_shoot.sfx', scene=scn)
        model.position = math3d.vector(0, 10, 200)
        self.sfx = model
        global_data.game_mgr.get_logic_timer().register(func=self.restart_sfx, mode=timer.CLOCK, interval=1.0)

    def restart_sfx(self):
        self.sfx.restart()

    def tick(self):
        self.sfx.position = self.sfx.position + math3d.vector(110 * self.sign * (time.time() - self.last_time), 0, 0)
        self.last_time = time.time()
        if self.sign * self.sfx.position.x > 200.0:
            self.sign *= -1.0
            self.sfx.position.x *= -1.0
            self.sfx.shutdown()
            self.sfx.restart()

    def test_model(self):
        import world
        import game3d
        from common.utils import timer
        scn = self.scene()
        scn.background_color = 6250335
        model = world.model('model_new\\scene\\pve\\pve_02\\mesh\\pve_02_dixing\\pve_02_00_terrain.gim', scn)
        model.position = math3d.vector(-750, 0, 750)
        cam = scn.active_camera
        cam.set_placement(math3d.vector(0, 1000, -1000), math3d.vector(0, -1, 1), math3d.vector(0, 1, 0))
        light = world.light(world.LIGHT_TYPE_DIRECTION, scn)
        light.direction = math3d.vector(0, -1, 1)
        light.enable = True
        light.enable_lit = True
        light.intensity = 10

        def rotate_model():
            model.rotate_y(0.05)

        global_data.game_mgr.get_logic_timer().register(func=rotate_model, mode=timer.LOGIC)
        import game3d
        game3d.delay_exec(5000, lambda : game3d.exit())

    def test_code(self):
        from cython_mod_a import Mgr
        from cython_mod_b import ItemBase

        class ItemPatch(ItemBase):

            def __init__(self):
                self.name = 'Item Patch'
                self.id = 1

            def check(self):
                print('<<<<<<<', self.name)

        item_base = ItemBase()
        item = ItemPatch()
        mgr = Mgr()
        mgr.check(item_base)
        mgr.check(item)

    def on_enter(self):
        self.test_model()

    def on_exit(self):
        pass

    def on_touch_tap(self, touch):
        if self._tap_func:
            self._tap_func(touch)
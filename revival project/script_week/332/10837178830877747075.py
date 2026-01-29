# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMechaLightMapEditor.py
import os.path
import world
import math3d
from . import ScenePart
HOST_ROOT = 'E:\\work\\g93\\gameplay\\trunk\\src\\res\\'
MECHA_ROOT = 'model_new\\mecha'
BAKE_ANIM_LIST = {8001: [
        'shoot_f', 'thrust_f', 'missile_01'],
   8002: [
        'sword_jump_01', 'sword_aim_fire_03'],
   8003: [
        'air_hover', 'thrust_f', 'throw_02'],
   8004: [
        'jump_01', 'jump_01', 'shoot'],
   8005: [
        'shoot_idle', 'shoot_idle', 'transform_idle', 'shoot_idle'],
   8006: [
        'rush_start_idle', 'jump1', 'jump1', 'shoot'],
   8007: [
        'run_f', 'run_f'],
   8008: [
        'jump_01', ('build_shield', 0.4), 'shoot'],
   8009: [
        'huoliquankai_move_f', 'huoliquankai_move_f', 'shoot_m'],
   8010: [
        'transform_idle', 's_transform_idle', 'second_shoot02', 'shoot'],
   8011: [
        'j_run', 'j_vice_02', 'q_vice_02'],
   8012: [
        'jump02', 'shoot'],
   8013: [
        'charge'],
   8014: [
        'shoot', 'shoot'],
   8015: [
        'jump01', 'jump01', 'storm_loop_f'],
   8016: [
        'dash_f', 'blast_dash', 'shoot'],
   8017: [
        'ball_start02', 'shoot_r'],
   8018: [
        'jump_01', ('reload', 0.6)],
   8019: [
        'jump_01', 'pan_loop', 'shoot_idle', 'shd_shoot_idle'],
   8020: [
        'jump_01', 'trans_1', 'vice_02'],
   8021: [
        'shoot', 'vice_01'],
   8022: [
        'move_f', 'vice_02', 'transform_shoot', 'idle'],
   8023: [
        'snipe_jump_01', 'akimbo_shoot'],
   8024: [
        'dash_04', 'shoot2'],
   8025: [
        'move_f', 'shoot_f', 'pan_fire'],
   8026: [
        'dash_loop', ('shield_fire', 0.4), 'shield_loop'],
   8027: [
        'jump_01', 'shoot', 'vice_fire2'],
   8028: [
        'idle'],
   80281: [
         'rabt_jump_start', 'rabt_salvo_start'],
   8029: [
        'rifle_jump_01', 'rifle_idle'],
   8030: [
        'jump_02', 'vice_aim'],
   8031: [
        'jump_01', 'jump_reaper_01'],
   8032: [
        'shoot', 'shoot', 'shoot'],
   8033: [
        'jump01', 'shoot', 'trans_1'],
   8034: [
        'jump01', 'shoot', 'boom_loop'],
   8035: [
        'shoot_01'],
   8036: [
        'jump01', 'reload'],
   8037: [
        'jump_01', 'vice_loop', 'slash_01']
   }
MECHA_ID = 8013
SS = False
BAKER_SCENE_PATH = 'scene/bake_lighting/{}.scn'.format(MECHA_ID)
if SS:
    BAKER_SCENE_PATH = 'scene/bake_lighting/{}ss.scn'.format(MECHA_ID)
MECHA_ANIMS = BAKE_ANIM_LIST[MECHA_ID]

class PreviewUI(object):

    def __init__(self, tex):
        from cocosui import cc
        director = cc.Director.getInstance()
        ui_scene = director.getRunningScene()
        rt = cc.RenderTexture.createWithITexture(tex)
        sprite = rt
        ui_scene.addChild(sprite)
        sprite.setScale(0.125)
        sprite.setPosition(cc.Vec2(128, 128))
        self._rt = rt

    def save_to_file(self, path):
        from cocosui import cc

        def callback(*args):
            print 'Save to {} finished'.format(path)

        self._rt.saveToFile(path, cc.IMAGE_FORMAT_PNG, True, callback)


def gen_mecha_path--- This code section failed: ---

  96       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'os'
           9  STORE_FAST            1  'os'

  97      12  LOAD_CONST            1  -1
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  're'
          21  STORE_FAST            2  're'

  99      24  BUILD_LIST_0          0 
          27  STORE_FAST            3  'ret'

 100      30  BUILD_LIST_0          0 
          33  STORE_FAST            4  'dir_list'

 101      36  LOAD_CONST            2  '{}\\{}'
          39  LOAD_ATTR             2  'format'
          42  LOAD_GLOBAL           3  'HOST_ROOT'
          45  LOAD_GLOBAL           4  'MECHA_ROOT'
          48  BINARY_ADD       
          49  LOAD_FAST             0  'mid'
          52  CALL_FUNCTION_2       2 
          55  STORE_FAST            5  'root'

 102      58  SETUP_LOOP          318  'to 379'
          61  LOAD_FAST             1  'os'
          64  LOAD_ATTR             5  'listdir'
          67  LOAD_FAST             5  'root'
          70  CALL_FUNCTION_1       1 
          73  GET_ITER         
          74  FOR_ITER            301  'to 378'
          77  STORE_FAST            6  'dir_name'

 103      80  LOAD_FAST             2  're'
          83  LOAD_ATTR             6  'match'
          86  LOAD_CONST            3  '^{}(_skin_s)?'
          89  LOAD_ATTR             2  'format'
          92  LOAD_FAST             0  'mid'
          95  CALL_FUNCTION_1       1 
          98  LOAD_FAST             6  'dir_name'
         101  CALL_FUNCTION_2       2 
         104  POP_JUMP_IF_FALSE    74  'to 74'

 104     107  LOAD_FAST             1  'os'
         110  LOAD_ATTR             7  'path'
         113  LOAD_ATTR             8  'join'
         116  LOAD_FAST             5  'root'
         119  LOAD_FAST             6  'dir_name'
         122  CALL_FUNCTION_2       2 
         125  STORE_FAST            7  'full_dir'

 105     128  LOAD_FAST             1  'os'
         131  LOAD_ATTR             7  'path'
         134  LOAD_ATTR             9  'exists'
         137  LOAD_FAST             7  'full_dir'
         140  LOAD_CONST            4  '\\h.mesh'
         143  BINARY_ADD       
         144  CALL_FUNCTION_1       1 
         147  POP_JUMP_IF_FALSE   375  'to 375'

 106     150  LOAD_FAST             3  'ret'
         153  LOAD_ATTR            10  'append'
         156  LOAD_FAST             7  'full_dir'
         159  LOAD_GLOBAL          11  'len'
         162  LOAD_GLOBAL           3  'HOST_ROOT'
         165  CALL_FUNCTION_1       1 
         168  SLICE+1          
         169  LOAD_CONST            5  '\\l.gim'
         172  BINARY_ADD       
         173  LOAD_FAST             6  'dir_name'
         176  BUILD_TUPLE_2         2 
         179  CALL_FUNCTION_1       1 
         182  POP_TOP          

 107     183  LOAD_FAST             1  'os'
         186  LOAD_ATTR             7  'path'
         189  LOAD_ATTR             9  'exists'
         192  LOAD_FAST             7  'full_dir'
         195  LOAD_CONST            6  '\\textures'
         198  BINARY_ADD       
         199  CALL_FUNCTION_1       1 
         202  POP_JUMP_IF_FALSE   225  'to 225'

 108     205  LOAD_FAST             4  'dir_list'
         208  LOAD_ATTR            10  'append'
         211  LOAD_FAST             7  'full_dir'
         214  LOAD_CONST            6  '\\textures'
         217  BINARY_ADD       
         218  CALL_FUNCTION_1       1 
         221  POP_TOP          
         222  JUMP_ABSOLUTE       372  'to 372'

 109     225  LOAD_FAST             1  'os'
         228  LOAD_ATTR             7  'path'
         231  LOAD_ATTR             9  'exists'
         234  LOAD_FAST             7  'full_dir'
         237  LOAD_CONST            7  '\\texture'
         240  BINARY_ADD       
         241  CALL_FUNCTION_1       1 
         244  POP_JUMP_IF_FALSE   267  'to 267'

 110     247  LOAD_FAST             4  'dir_list'
         250  LOAD_ATTR            10  'append'
         253  LOAD_FAST             7  'full_dir'
         256  LOAD_CONST            7  '\\texture'
         259  BINARY_ADD       
         260  CALL_FUNCTION_1       1 
         263  POP_TOP          
         264  JUMP_ABSOLUTE       372  'to 372'

 111     267  LOAD_FAST             1  'os'
         270  LOAD_ATTR             7  'path'
         273  LOAD_ATTR             9  'exists'
         276  LOAD_FAST             7  'full_dir'
         279  LOAD_CONST            8  '\\texutres'
         282  BINARY_ADD       
         283  CALL_FUNCTION_1       1 
         286  POP_JUMP_IF_FALSE   309  'to 309'

 112     289  LOAD_FAST             4  'dir_list'
         292  LOAD_ATTR            10  'append'
         295  LOAD_FAST             7  'full_dir'
         298  LOAD_CONST            8  '\\texutres'
         301  BINARY_ADD       
         302  CALL_FUNCTION_1       1 
         305  POP_TOP          
         306  JUMP_ABSOLUTE       372  'to 372'

 113     309  CONTINUE              9  'to 9'
         312  COMPARE_OP            2  '=='
         315  POP_JUMP_IF_FALSE   338  'to 338'

 114     318  LOAD_FAST             4  'dir_list'
         321  LOAD_ATTR            10  'append'
         324  LOAD_FAST             7  'full_dir'
         327  LOAD_CONST            6  '\\textures'
         330  BINARY_ADD       
         331  CALL_FUNCTION_1       1 
         334  POP_TOP          
         335  JUMP_ABSOLUTE       372  'to 372'

 116     338  LOAD_CONST           10  '[Warn] no textures for {}'
         341  LOAD_ATTR             2  'format'
         344  LOAD_FAST             6  'dir_name'
         347  CALL_FUNCTION_1       1 
         350  PRINT_ITEM       
         351  PRINT_NEWLINE_CONT

 117     352  LOAD_FAST             4  'dir_list'
         355  LOAD_ATTR            10  'append'
         358  LOAD_FAST             7  'full_dir'
         361  LOAD_CONST            6  '\\textures'
         364  BINARY_ADD       
         365  CALL_FUNCTION_1       1 
         368  POP_TOP          
         369  JUMP_ABSOLUTE       375  'to 375'
         372  JUMP_BACK            74  'to 74'
         375  JUMP_BACK            74  'to 74'
         378  POP_BLOCK        
       379_0  COME_FROM                '58'

 119     379  LOAD_FAST             3  'ret'
         382  LOAD_FAST             4  'dir_list'
         385  BUILD_TUPLE_2         2 
         388  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `COMPARE_OP' instruction at offset 312


def gen_mecha_path_80281():
    import os
    import re
    ret = []
    dir_list = []
    root = '{}\\8028'.format(HOST_ROOT + MECHA_ROOT)
    for dir_name in os.listdir(root):
        if re.match('^{}(_skin_s)?'.format(8028), dir_name):
            full_dir = os.path.join(root, dir_name, 'rabbit')
            if os.path.exists(full_dir + '\\l.mesh'):
                ret.append((full_dir[len(HOST_ROOT):] + '\\l.gim', dir_name))
                if os.path.exists(full_dir + '\\textures'):
                    dir_list.append(full_dir + '\\textures')
                elif os.path.exists(full_dir + '\\texture'):
                    dir_list.append(full_dir + '\\texture')
                else:
                    os.makedirs(full_dir + '\\textures')
                    dir_list.append(full_dir + '\\textures')

    return (
     ret, dir_list)


if MECHA_ID == 80281:
    WORK_LIST, DIR_LIST = gen_mecha_path_80281()
else:
    WORK_LIST, DIR_LIST = gen_mecha_path(MECHA_ID)
LIGHT_MODEL_MAP = {}

def active_lights(scn, index):
    global LIGHT_MODEL_MAP
    for light in scn.get_light_group():
        light.enable = light.name.startswith(str(index) + '_')
        m = LIGHT_MODEL_MAP.get(light.name)
        if m:
            m.visible = light.enable


class Baker(object):

    def __init__(self):
        import render
        import math3d
        self._scn = world.scene()
        self._scn.load(BAKER_SCENE_PATH)
        self._scn.background_color = 0
        self._cam = self._scn.create_camera(True)
        self._tex = render.texture.create_empty(2048, 2048, render.PIXEL_FMT_A8R8G8B8, True)
        self._rt = render.create_render_target(self._tex, None, render.PIXEL_FMT_D24S8)
        self._ui = PreviewUI(self._tex)
        self._timer0 = global_data.game_mgr.get_fix_logic_timer().register(func=self.update)
        self._timer = global_data.game_mgr.get_render_timer().register(func=self.render)
        self._cam.set_placement(math3d.vector(0, 0, 300), math3d.vector(0, 0, -1), math3d.vector(0, 1, 0))
        self._model = None
        self._cur_anim = None
        self._start_anim_time = 0
        return

    def load_mecha(self, mid):
        file_path, file_name = WORK_LIST[mid]
        m = world.model(file_path, self._scn)
        if self._model:
            self._model.destroy()
        self._model = m
        self.prepare_material(self._model)
        self.play_animation(self._cur_anim, self._start_anim_time)

    def prepare_material(self, model):
        model.all_materials.set_technique(1, 'shader/draw_lightmap.nfx::TShader')
        model.all_materials.enable_write_alpha = True

    def update(self):
        self._scn.update()

    def render(self):
        self._scn.render(self._rt)

    def save(self, path):
        print 'try save to {}'.format(path)
        self._ui.save_to_file(path)

    def destroy(self):
        global_data.game_mgr.get_fix_logic_timer().unregister(self._timer0)
        global_data.game_mgr.get_render_timer().unregister(self._timer)

    def play_animation(self, anim, start_time):
        self._start_anim_time = start_time
        if self._model and anim:
            self._model.play_animation(anim, -1.0, world.TRANSIT_TYPE_DEFAULT, self._start_anim_time, 0)
            global_data.game_mgr.delay_exec(0.1, self._model.stop_animation)
        self._cur_anim = anim

    def active_light(self, idx):
        active_lights(self._scn, idx)


class PartMechaLightMapEditor(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartMechaLightMapEditor, self).__init__(scene, name)
        self._baker = None
        self._model = None
        self._cur_id = 0
        self._animation = ''
        self._animation_idx = 0
        self._animation_time = 0.9
        return

    def on_enter(self):
        self.scene().load(BAKER_SCENE_PATH)
        self._baker = Baker()
        self.register_keys()
        self._load_mecha(self._cur_id)
        self.scene().load_env('default_nx2_mobile2.xml')
        cam = self.scene().active_camera
        cam.set_placement(math3d.vector(0, 50, 200), math3d.vector(0, 0, -1), math3d.vector(0, 1, 0))
        for light in self.scene().get_light_group():
            mod = world.model('model_new/test/bone_sphere.gim', self.scene())
            mod.position = light.position
            mod.scale = math3d.vector(10, 10, 10)
            LIGHT_MODEL_MAP[light.name] = mod

    def on_exit(self):
        self._baker.destroy()

    def register_keys(self):
        import game
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_PAGEUP, game.VK_PAGEDOWN, game.VK_1, game.VK_2, game.VK_3, game.VK_4, game.VK_ENTER), self._key_handler)

    def unregister_keys(self):
        import game
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_PAGEUP, game.VK_PAGEDOWN, game.VK_1, game.VK_2, game.VK_3, game.VK_4, game.VK_ENTER), self._key_handler)

    def _key_handler(self, msg, keycode):
        import game
        if keycode in (game.VK_PAGEUP, game.VK_PAGEDOWN):
            old_mid = self._cur_id
            if keycode == game.VK_PAGEUP:
                self._cur_id -= 1
            if keycode == game.VK_PAGEDOWN:
                self._cur_id += 1
            max_id = len(WORK_LIST) - 1
            if self._cur_id < 0:
                self._cur_id = 0
            elif self._cur_id > max_id:
                self._cur_id = max_id
            if self._cur_id != old_mid:
                self._load_mecha(self._cur_id)
        if keycode in (game.VK_1, game.VK_2, game.VK_3, game.VK_4):
            idx = keycode - game.VK_1
            if idx < len(MECHA_ANIMS):
                self._animation = MECHA_ANIMS[idx]
                self._animation_time = 0.9
                if isinstance(self._animation, (tuple, list)):
                    self._animation, self._animation_time = self._animation
                self._animation_idx = idx
                self._update_animation()
                self._active_light(idx)
        if keycode == game.VK_ENTER:
            file_path, dir_name = WORK_LIST[self._cur_id]
            self._baker.save('{}\\lightmap_{}.png'.format(DIR_LIST[self._cur_id], self._animation_idx))

    def on_touch_slide(self, dx, dy, touches, touch_pos, *args):
        self._rotate_camera(dx * 0.01)

    def _rotate_camera(self, dx):
        mat = math3d.matrix.make_rotation_y(dx)
        self.scene().active_camera.transformation *= mat

    def _load_mecha(self, mid):
        self._baker.load_mecha(mid)
        if self._model:
            self._model.destroy()
        self._model = world.model(WORK_LIST[mid][0], self.scene())
        self._update_animation()

    def _update_animation(self):
        if self._model and self._animation:
            duration = self._model.get_anim_length(self._animation)
            start_time = duration * self._animation_time
            self._model.play_animation(self._animation, -1.0, world.TRANSIT_TYPE_DEFAULT, start_time, 0)
            global_data.game_mgr.delay_exec(0.1, self._model.stop_animation)
            self._baker.play_animation(self._animation, start_time)

    def _active_light(self, idx):
        active_lights(self.scene(), idx)
        self._baker.active_light(idx)
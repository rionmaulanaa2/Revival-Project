# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/gen_diffuse_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import six
from six.moves import range
import render
import weakref
import math
import math3d
import world
import game3d
from common.cfg import confmgr
from common.framework import Singleton
import cc
from logic.manager_agents.manager_decorators import sync_exec
s_diffuse_rt = None
MAP_RT_CONF = {'scn_bg_color': 0,
   'cam_fov': 30.0,
   'rt_width': 512,
   'rt_height': 512,
   'cam_euler': math3d.vector(0, math.pi, 0),
   'cam_pos': math3d.vector(0, 10, 55)
   }
WAIT_TICK_COUNT = 2
_T = lambda x: (
 x, game3d.calc_string_hash(x))
STR_NOL, HASH_NOL = _T('u_NdotL')

class DiffuseRenderTarget(Singleton):

    def init(self):
        self._diffuse_target = None
        self._cocos_rt = None
        self._render_finish_callback = None
        self._pass_0_models = []
        self._pass_1_models = []
        self._render_pass = []
        self._first_time = True
        self._delay_frame_count = WAIT_TICK_COUNT
        self._out_path = ''
        self.env_path = 'scene/scene_env_confs/bake_mecha_conf/default_nx2_mobile.xml'
        self.env_name = 'zhanshi'
        self.create_rt()
        return

    def get_rt_holder(self):
        return self._diffuse_target

    def get_cocos_rt(self):
        return self._cocos_rt

    def create_rt(self):
        self._setup_base_pass()
        self._setup_postprocess_pass()

    def start_render(self):
        self._start_render_next_frame()

    @sync_exec
    def _setup_base_pass(self):
        from common.uisys.render_target import RenderTargetHolder
        self._diffuse_target = RenderTargetHolder(None, None, MAP_RT_CONF, all_light=['dir_light'])
        self._diffuse_target2 = RenderTargetHolder(None, None, MAP_RT_CONF, all_light=['dir_light'])
        self._diffuse_target.tick_callback = self._diffuse_pass2
        self._diffuse_target2.tick_callback = self._postprocess_pass
        for rt in (self._diffuse_target, self._diffuse_target2):
            scn = rt.scn
            scn.enable_vlm = True
            scn.load_env_new(self.env_path)
            scn.background_color = 0
            rt.apply_conf(self.env_name)

        return

    def _setup_postprocess_pass(self):
        from common.uisys.render_target import RenderTargetHolder
        self._postprocess_target = RenderTargetHolder(None, None, MAP_RT_CONF, all_light=['dir_light'])
        self._postprocess_target.tick_callback = self._on_render_finished
        rt = cc.RenderTexture.createWithITexture(self._postprocess_target.tex)
        rt.retain()
        self._cocos_rt = rt
        model_path = confmgr.get('script_gim_ref')['gen_diffuse_test']
        model = world.model(model_path, None)
        self._postprocess_target.add_model(model)
        model.all_materials.set_texture('Tex0', self._diffuse_target.tex)
        model.all_materials.set_texture('Tex1', self._diffuse_target2.tex)
        rt_width = float(MAP_RT_CONF['rt_width'])
        rt_height = float(MAP_RT_CONF['rt_height'])
        model.all_materials.set_var('u_rtsize', (rt_width, rt_height, 1.0 / rt_width, 1.0 / rt_height))
        model.all_materials.enable_write_alpha = True
        return

    def create_diffuse(self, out_path, models, callback=None):
        for m in self._pass_0_models:
            m.destroy()

        for m in self._pass_1_models:
            m.destroy()

        self._pass_0_models = []
        self._pass_1_models = []
        self._render_finish_callback = callback
        self._out_path = out_path
        max_y = 0
        max_radius = 0
        for m, submesh_vec in six.iteritems(models):
            model_dark = world.model(m, None, False)
            for i in range(model_dark.get_socket_count()):
                for m in model_dark.get_socket_objects(i):
                    m.destroy()

            model_dark.all_materials.set_technique(1, 'shader/vbr_toon_mecha_nx2_mobile_gen_diffuse.nfx::TShader')
            model_dark.all_materials.set_var(HASH_NOL, STR_NOL, 0.0)
            model_dark.all_materials.enable_write_alpha = True
            for i in range(model_dark.get_submesh_count()):
                if i not in submesh_vec:
                    model_dark.set_submesh_visible(i, False)

            self._pass_0_models.append(model_dark)
            self._diffuse_target.add_model(model_dark, cast_shadow=False)
            max_y = max(model_dark.center_w.y, max_y)
            max_radius = max(model_dark.bounding_radius_w, max_radius)

        for m, submesh_vec in six.iteritems(models):
            model_bright = world.model(m, None, False)
            for i in range(model_dark.get_socket_count()):
                for m in model_dark.get_socket_objects(i):
                    m.destroy()

            model_bright.all_materials.set_technique(1, 'shader/vbr_toon_mecha_nx2_mobile_gen_diffuse.nfx::TShader')
            model_bright.all_materials.set_var(HASH_NOL, STR_NOL, 1.0)
            model_bright.all_materials.enable_write_alpha = True
            for i in range(model_bright.get_submesh_count()):
                if i not in submesh_vec:
                    model_bright.set_submesh_visible(i, False)

            self._pass_1_models.append(model_bright)
            self._diffuse_target2.add_model(model_bright, cast_shadow=False)

        cam_pos = math3d.vector(0, max_y, max_radius * 2.0)
        forward = math3d.vector(0, 0, 0) - cam_pos
        self._diffuse_target.camera.set_placement(cam_pos, forward, math3d.vector(0, 1, 0))
        self._diffuse_target2.camera.set_placement(cam_pos, forward, math3d.vector(0, 1, 0))
        self.start_render()
        return

    def _start_render_next_frame(self):
        self._delay_frame_count = WAIT_TICK_COUNT
        global_data.game_mgr.next_exec(self._diffuse_pass)

    def _diffuse_pass(self):
        self._diffuse_target.start_render_target()

    def _diffuse_pass2(self):
        self._delay_frame_count -= 1
        if self._delay_frame_count <= 0:
            self._diffuse_target.stop_render_target()
            self._diffuse_target2.start_render_target()
            self._delay_frame_count = WAIT_TICK_COUNT

    def _postprocess_pass(self):
        self._delay_frame_count -= 1
        if self._delay_frame_count <= 0:
            self._diffuse_target2.stop_render_target()
            self._postprocess_target.start_render_target()
            self._delay_frame_count = WAIT_TICK_COUNT

    def _on_render_finished(self):
        self._delay_frame_count -= 1
        if self._delay_frame_count > 0:
            return
        self._postprocess_target.stop_render_target()
        from common.utils.path import get_neox_dir
        import os.path
        self._cocos_rt.saveToFile(self._out_path, cc.IMAGE_FORMAT_PNG, True, self._on_save_file)

    def _on_save_file(self, *args):
        if self._first_time:
            self._first_time = False
            self.start_render()
        elif self._render_finish_callback:
            global_data.game_mgr.next_exec(self._render_finish_callback)
        print('save finish', self._out_path)


def gen_mecha_all():
    from common.utils.path import get_neox_dir
    import os
    prefix = get_neox_dir() + '/res/'
    prefix_len = len(prefix)
    dirpath = 'model_new/mecha'
    dirpath = prefix + dirpath
    all_mecha_skins = []
    for name in os.listdir(dirpath):
        mecha_dir = os.path.join(dirpath, name)
        if os.path.isdir(mecha_dir):
            for skin_dir in os.listdir(mecha_dir):
                skin_path = os.path.join(mecha_dir, skin_dir)
                all_mecha_skins.append(skin_path[prefix_len:])

    _gen_model_diffuse_list(all_mecha_skins)


def _gen_model_diffuse_list(paths):

    def callback():
        if paths:
            path = paths[0]
            del paths[0]
            gen_model_diffuse(path, callback)
        else:
            print('gen all finish.')

    callback()


def gen_model_diffuse--- This code section failed: ---

 251       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'os.path'
           9  STORE_DEREF           1  'os'

 252      12  LOAD_GLOBAL           1  'gen_model_diffuse_conf'
          15  LOAD_FAST             0  'path'
          18  CALL_FUNCTION_1       1 
          21  STORE_FAST            2  'diffuse_map'

 253      24  LOAD_FAST             2  'diffuse_map'
          27  POP_JUMP_IF_TRUE     60  'to 60'

 254      30  LOAD_GLOBAL           2  'print'
          33  LOAD_CONST            2  'no diffuse conf generated'
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          

 255      40  LOAD_DEREF            0  'callback'
          43  POP_JUMP_IF_FALSE    56  'to 56'

 256      46  LOAD_DEREF            0  'callback'
          49  CALL_FUNCTION_0       0 
          52  POP_TOP          
          53  JUMP_FORWARD          0  'to 56'
        56_0  COME_FROM                '53'

 257      56  LOAD_CONST            0  ''
          59  RETURN_END_IF    
        60_0  COME_FROM                '27'

 259      60  LOAD_GLOBAL           3  'DiffuseRenderTarget'
          63  CALL_FUNCTION_0       0 
          66  STORE_DEREF           2  'drt'

 261      69  LOAD_CONST            1  ''
          72  LOAD_CONST            3  ('get_neox_dir',)
          75  IMPORT_NAME           4  'common.utils.path'
          78  IMPORT_FROM           5  'get_neox_dir'
          81  STORE_FAST            3  'get_neox_dir'
          84  POP_TOP          

 264      85  LOAD_FAST             3  'get_neox_dir'
          88  CALL_FUNCTION_0       0 
          91  LOAD_CONST            4  '/res/'
          94  BINARY_ADD       
          95  LOAD_DEREF            1  'os'
          98  LOAD_ATTR             6  'path'
         101  LOAD_ATTR             7  'join'
         104  LOAD_ATTR             5  'get_neox_dir'
         107  CALL_FUNCTION_2       2 
         110  BINARY_ADD       
         111  STORE_DEREF           3  'dirpath'

 265     114  LOAD_DEREF            1  'os'
         117  LOAD_ATTR             6  'path'
         120  LOAD_ATTR             8  'exists'
         123  LOAD_DEREF            3  'dirpath'
         126  CALL_FUNCTION_1       1 
         129  POP_JUMP_IF_TRUE    198  'to 198'

 266     132  LOAD_FAST             3  'get_neox_dir'
         135  CALL_FUNCTION_0       0 
         138  LOAD_CONST            4  '/res/'
         141  BINARY_ADD       
         142  LOAD_DEREF            1  'os'
         145  LOAD_ATTR             6  'path'
         148  LOAD_ATTR             7  'join'
         151  LOAD_ATTR             6  'path'
         154  CALL_FUNCTION_2       2 
         157  BINARY_ADD       
         158  STORE_DEREF           3  'dirpath'

 267     161  LOAD_DEREF            1  'os'
         164  LOAD_ATTR             6  'path'
         167  LOAD_ATTR             8  'exists'
         170  LOAD_DEREF            3  'dirpath'
         173  CALL_FUNCTION_1       1 
         176  POP_JUMP_IF_TRUE    198  'to 198'

 268     179  LOAD_DEREF            1  'os'
         182  LOAD_ATTR             9  'mkdir'
         185  LOAD_DEREF            3  'dirpath'
         188  CALL_FUNCTION_1       1 
         191  POP_TOP          
         192  JUMP_ABSOLUTE       198  'to 198'
         195  JUMP_FORWARD          0  'to 198'
       198_0  COME_FROM                '195'

 271     198  LOAD_GLOBAL          10  'six_ex'
         201  LOAD_ATTR            11  'items'
         204  LOAD_FAST             2  'diffuse_map'
         207  CALL_FUNCTION_1       1 
         210  STORE_DEREF           4  'job_items'

 272     213  LOAD_CLOSURE          4  'job_items'
         216  LOAD_CLOSURE          1  'os'
         219  LOAD_CLOSURE          3  'dirpath'
         222  LOAD_CLOSURE          2  'drt'
         225  LOAD_CLOSURE          5  'chain_callback'
         228  LOAD_CLOSURE          0  'callback'
         234  LOAD_CONST               '<code_object chain_callback>'
         237  MAKE_CLOSURE_0        0 
         240  STORE_DEREF           5  'chain_callback'

 284     243  LOAD_DEREF            5  'chain_callback'
         246  CALL_FUNCTION_0       0 
         249  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 107


def gen_model_diffuse_conf(path):
    from common.utils.path import get_neox_dir
    import os
    import re
    import xml.etree.ElementTree as ET
    IGNORE_GIMS = {
     'empty.gim', 'hit.gim', 'h_glass.gim'}
    res_prefix = get_neox_dir() + '/res/'
    prefix_len = len(res_prefix)
    path = res_prefix + path
    total_diffuse_map = {}
    try:
        for root, _, filenames in os.walk(path):
            for f in filenames:
                if not f.endswith('.gim'):
                    continue
                if f.endswith('_low.gim'):
                    continue
                if f in IGNORE_GIMS:
                    continue
                if re.match('(.+_)?l(1|2|3)?\\.gim', f):
                    continue
                gim_ff = os.path.join(root, f)
                mtg_ff = gim_ff.replace('.gim', '.mtg')
                if not os.path.exists(mtg_ff):
                    continue
                gim_doc = ET.parse(gim_ff)
                mtg_doc = ET.parse(mtg_ff)
                diffuse_map = _get_submesh_diffuse(gim_doc, mtg_doc)
                for diffuse_path, submesh_vec in six.iteritems(diffuse_map):
                    l = total_diffuse_map.get(diffuse_path, {})
                    l[gim_ff[prefix_len:]] = submesh_vec
                    total_diffuse_map[diffuse_path] = l

    except:
        import traceback
        traceback.print_exc()
        print('[FAIL] generate {} failed.'.format(path))

    return total_diffuse_map


def _get_submesh_diffuse(gim_doc, mtg_doc):
    mtg_list = []
    INVALID_TEX = '????????'
    for node in mtg_doc.findall('./MaterialGroup/*/Material'):
        tech = node.find('./Technique').get('TechName')
        if 'mecha' in tech:
            mtg_list.append(node.find('./ParamTable/Tex0').get('Value'))
        else:
            mtg_list.append(INVALID_TEX)

    mtg_count = len(mtg_list)
    diffuse_map = {}
    for i, submesh in enumerate(gim_doc.findall('./SubMesh/*')):
        diffuse_id = int(submesh.get('MtlIdx'))
        if diffuse_id >= mtg_count:
            continue
        diffuse_path = mtg_list[diffuse_id]
        if diffuse_path not in diffuse_map:
            diffuse_map[diffuse_path] = []
        diffuse_map[diffuse_path].append(i)

    if INVALID_TEX in diffuse_map:
        del diffuse_map[INVALID_TEX]
    return diffuse_map


def gen_all_niudan():
    niudan_model = 'model_new/others/niudan/niudan_01.gim'
    niudan_tex_vec = [
     'model_new/scene/items/niudan/textures/niudan_red.tga',
     'model_new/scene/items/niudan/textures/niudan_blue.tga',
     'model_new/scene/items/niudan/textures/niudan_green.tga',
     'model_new/scene/items/niudan/textures/niudan_purple.tga',
     'model_new/scene/items/niudan/textures/niudan_yellow.tga',
     'model_new/scene/items/niudan/textures/niudan_cyan.tga']
    import shutil


def init_global_function():
    import six.moves.builtins
    six.moves.builtins.__dict__['gen_mecha_all'] = gen_mecha_all
    six.moves.builtins.__dict__['gen_model_diffuse'] = gen_model_diffuse
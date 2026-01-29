# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/gen_compress_texture_utils.py
from __future__ import absolute_import
from __future__ import print_function
import render
import math
import math3d
import world
import game3d
from common.cfg import confmgr
import cc
DEFAULT_RT_CONF = {'scn_bg_color': 4278190080L,
   'cam_fov': 50,
   'rt_width': 1024,
   'rt_height': 1024,
   'cam_euler': math3d.vector(360 / 180 * math.pi, 181.32 / 180 * math.pi, 0.52 / 180 * math.pi),
   'cam_pos': math3d.vector(-4, 11, 31)
   }

class DiffuseRenderTarget(object):

    def __init__(self, use_u32_tex=True, use_etc2_tex=True, size_scale=4, do_copy=False, do_save=False, use_main_camera=False, size=None):
        self._cocos_rt = None
        self._render_finish_callback = None
        self._render_count = 0
        self._render_count_limit = 2
        self.use_u32_tex = use_u32_tex
        self.use_etc2_tex = use_etc2_tex
        self.size_scale = size_scale
        self.do_copy = do_copy
        self.do_save = do_save
        self.use_main_camera = use_main_camera
        if not size:
            self._tex_size = (2048, 2048)
        else:
            self._tex_size = size
        self._src_path = ''
        self._out_path = ''
        self._model = None
        self._postprocess_target = None
        self._dst_texture = None
        self.create_rt()
        return

    def destroy(self):
        if self._cocos_rt:
            self._cocos_rt.release()
        self._cocos_rt = None
        if self._postprocess_target:
            self._postprocess_target.destroy()
        self._postprocess_target = None
        self._dst_texture = None
        self._src_path = ''
        self._out_path = ''
        return

    def get_rt_holder(self):
        return self._postprocess_target

    def get_cocos_rt(self):
        return self._cocos_rt

    def get_dst_texture(self):
        return self._dst_texture

    def get_scene(self):
        return self._postprocess_target.scn

    def create_rt(self):
        self._setup_postprocess_pass()

    def stop_render_target(self):
        self._postprocess_target.stop_render_target()

    def _setup_postprocess_pass(self):
        from common.uisys.render_target import RenderTargetHolder
        DEFAULT_RT_CONF['rt_width'] = int(float(self._tex_size[0]) / self.size_scale)
        DEFAULT_RT_CONF['rt_height'] = int(float(self._tex_size[1]) / self.size_scale)
        if self.use_u32_tex:
            self._postprocess_target = RenderTargetHolder(None, None, DEFAULT_RT_CONF, format=render.PIXEL_FMT_u_A32B32G32R32)
        else:
            self._postprocess_target = RenderTargetHolder(None, None, DEFAULT_RT_CONF, use_main_camera=self.use_main_camera, format=render.PIXEL_FMT_A8R8G8B8)
        self.create_dst_texture()
        self._postprocess_target.tick_callback = self._on_compress_pass
        return

    def create_dst_texture(self):
        if self.use_etc2_tex:
            self._dst_texture = render.texture.create_empty(self._tex_size[0], self._tex_size[1], render.PIXEL_FMT_ETC2_RGBA, False)
        else:
            self._dst_texture = render.texture.create_empty(self._tex_size[0], self._tex_size[1], render.PIXEL_FMT_A8R8G8B8, False)

    def create_diffuse(self, src_path, out_path, callback=None):
        self._src_path = src_path
        self._out_path = out_path
        self._render_finish_callback = callback
        if not self._model:
            if self.use_u32_tex:
                model_path = 'model_new/others/screen_effect/postprocess_mesh/fangxing_002.gim'
            else:
                model_path = 'model_new/others/screen_effect/postprocess_mesh/fangxing_003.gim'
            self._model = world.model(model_path, None)
            self._postprocess_target.add_model(self._model)
            self._model.all_materials.enable_write_alpha = True
        self._model.all_materials.set_texture('Tex0', self._src_path)
        tex_width = float(self._tex_size[0])
        tex_height = float(self._tex_size[1])
        self._model.all_materials.set_var('u_tex_size', (tex_width, tex_height, 1.0 / tex_width, 1.0 / tex_height))
        self._render_count = 0
        self._postprocess_target.start_render_target()
        return

    def create_landscape_diffuse(self, out_path, callback=None):
        self._out_path = out_path
        self._render_finish_callback = callback
        self._render_count = 0
        self._postprocess_target.start_render_target()

    def restart_render(self):
        self._render_count = 0
        self._postprocess_target.start_render_target()

    def _on_compress_pass(self):
        self._render_count += 1
        if self._render_count < self._render_count_limit:
            return
        if self.do_copy:
            global_data.game_mgr.next_exec(self._on_copy_pass)
        elif self.do_save:
            global_data.game_mgr.next_exec(self._on_render_save_callback)
        elif self._render_finish_callback:
            self._render_finish_callback()

    def _on_copy_pass(self):
        print('>>>>> _on_copy_pass', self._dst_texture)
        do_callback = True
        if self.do_copy:
            render.texture.copy_texture(self._postprocess_target.tex, self._dst_texture, 0, 0, 0, 0, 0, 0, 0, 0)
            self.do_copy = False
        if self.do_save:
            do_callback = False
            global_data.game_mgr.next_exec(self._on_render_save_callback)
        if do_callback:
            if self._render_finish_callback:
                self._render_finish_callback()

    def _on_render_save_callback(self):
        print('>>>>> _on_render_save_callback')
        if not self._cocos_rt:
            self._cocos_rt = cc.RenderTexture.createWithITexture(self._postprocess_target.tex)
            self._cocos_rt.retain()
        if self._cocos_rt and self.do_save:
            self._cocos_rt.saveToFile(self._out_path, cc.IMAGE_FORMAT_PNG, True, self._on_save_file)
            self.do_save = False
        elif self._render_finish_callback:
            self._render_finish_callback()

    def _on_save_file(self, *args):
        print('save finish', self._out_path)
        if self._render_finish_callback:
            self._render_finish_callback()


def gen_compress_texture(path, callback=None, use_u32_tex=True, use_etc2_tex=True, size_scale=4, do_copy=False, do_save=False):
    import os.path
    from common.utils.path import get_neox_dir
    drt = DiffuseRenderTarget(use_u32_tex=use_u32_tex, use_etc2_tex=use_etc2_tex, size_scale=size_scale, do_copy=False, do_save=do_save)
    dirpath = get_neox_dir() + '/res/'
    has_rendered = [
     False]
    job_items = ['character/11/2008/textures/11_2008_d.tga']

    def chain_callback():
        if has_rendered[0] and callback:
            drt.stop_render_target()
            callback(drt)
        if job_items:
            src_path = job_items.pop(0)
            out_path = os.path.splitext(os.path.basename(src_path))[0] + '_etc2.png'
            out_path = os.path.join(dirpath, out_path)
            drt.create_diffuse(src_path, out_path, chain_callback)
            has_rendered[0] = True
        else:
            print('end generated')

    chain_callback()


def test_compress_texture():
    from cocosui import cc
    drt = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=False, do_save=False)
    count = [
     0]

    def delay():
        render.texture.copy_texture(drt._postprocess_target.tex, drt._dst_texture, 0, 0, 0, 0, 0, 0, 500, 1000)
        rt = cc.Texture2D.createWithITexture(drt._dst_texture)
        sprite = cc.Sprite.createWithTexture(rt)
        ui = global_data.ui_mgr.create_simple_dialog('battle/empty')
        p = ui.panel
        p.addChild(sprite)
        sprite.setPosition(cc.Vec2(600, 375))
        sprite.setScale(0.7)

    def render_cb():
        print('>>> render_cb')
        drt.stop_render_target()
        delay()

    drt2 = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=False, do_save=False)

    def render_cb2():
        count[0] += 1
        if count[0] == 2:
            drt2.stop_render_target()
            drt.create_diffuse(drt2._postprocess_target.tex, '', render_cb)

    drt2.create_diffuse('character/11/2008/textures/11_2008_d.tga', '', render_cb2)
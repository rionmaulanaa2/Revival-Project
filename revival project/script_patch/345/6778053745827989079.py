# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/render_target.py
from __future__ import absolute_import
import six
import cc
import time
import world
import render
import math3d
import game3d
from common.utils import ui_utils
from common.framework import Singleton
import math
from logic.manager_agents.manager_decorators import sync_exec
from common.utilities import color_int, color_int_srgb
from common.cfg import confmgr
from logic.vscene import scene

class RenderTarget(Singleton):

    def init(self):
        self._render_timer_id = None
        self._logic_timer_id = None
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnected
        return

    def start_render_target_timer(self):
        if self._render_timer_id:
            tm = global_data.game_mgr.get_render_timer()
            if tm:
                tm.unregister(self._render_timer_id)
            else:
                return
        tm = global_data.game_mgr.get_render_timer()
        self._render_timer_id = tm.register(func=self.render_func)
        tm = global_data.game_mgr.get_post_logic_timer()
        self._logic_timer_id = tm.register(func=self.logic_func)

    def stop_render_target_timer(self):
        if not self._render_timer_id:
            return False
        else:
            tm = global_data.game_mgr.get_render_timer()
            if self._render_timer_id:
                tm.unregister(self._render_timer_id)
            tm = global_data.game_mgr.get_post_logic_timer()
            if self._logic_timer_id:
                tm.unregister(self._logic_timer_id)
            self._render_timer_id = None
            self._logic_timer_id = None
            return True

    def restart_render_target_timer(self):
        if self.stop_render_target_timer():
            self.start_render_target_timer()

    def render_func(self):
        stop_target_render_holder_list = []
        for target_render_holder in global_data.ui_mgr.render_target_holder_list:
            rt = target_render_holder.rt
            scn = target_render_holder.scn
            rt_conf = target_render_holder.conf
            vp = (0, 0, int(rt_conf['rt_width']), int(rt_conf['rt_height']), 0, 1.0)
            scn.render(rt, vp)
            if target_render_holder.render_tick_callback:
                target_render_holder.safe_render_tick()
            if target_render_holder.render_max_count > 0:
                target_render_holder.render_count += 1
                if target_render_holder.render_count >= target_render_holder.render_max_count:
                    stop_target_render_holder_list.append(target_render_holder)

        for target_render_holder in stop_target_render_holder_list:
            target_render_holder.stop_render_target()

    def logic_func(self):
        for target_render_holder in global_data.ui_mgr.render_target_holder_list:
            target_render_holder.tick()

    def on_finalize(self):
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnected
        render.on_device_restored = None
        self.stop_render_target_timer()
        return

    def on_login_reconnected(self, *args):
        self.restart_render_target_timer()


@sync_exec
def cocos_rt_render_wrapper--- This code section failed: ---

  96       0  LOAD_FAST             0  'rt'
           3  LOAD_ATTR             0  'begin'
           6  CALL_FUNCTION_0       0 
           9  POP_TOP          

  97      10  LOAD_GLOBAL           1  'hasattr'
          13  LOAD_GLOBAL           1  'hasattr'
          16  CALL_FUNCTION_2       2 
          19  POP_JUMP_IF_FALSE    95  'to 95'

  98      22  SETUP_LOOP           97  'to 122'
          25  LOAD_FAST             1  'obj_list'
          28  GET_ITER         
          29  FOR_ITER             59  'to 91'
          32  STORE_FAST            2  'obj'

  99      35  LOAD_GLOBAL           2  'isinstance'
          38  LOAD_FAST             2  'obj'
          41  LOAD_GLOBAL           3  'cc'
          44  LOAD_ATTR             4  'Node'
          47  CALL_FUNCTION_2       2 
          50  POP_JUMP_IF_FALSE    69  'to 69'

 100      53  LOAD_FAST             0  'rt'
          56  LOAD_ATTR             5  'addCommandsForNode'
          59  LOAD_FAST             2  'obj'
          62  CALL_FUNCTION_1       1 
          65  POP_TOP          
          66  JUMP_BACK            29  'to 29'

 102      69  LOAD_FAST             0  'rt'
          72  LOAD_ATTR             5  'addCommandsForNode'
          75  LOAD_FAST             2  'obj'
          78  LOAD_ATTR             6  'get'
          81  CALL_FUNCTION_0       0 
          84  CALL_FUNCTION_1       1 
          87  POP_TOP          
          88  JUMP_BACK            29  'to 29'
          91  POP_BLOCK        
        92_0  COME_FROM                '22'
          92  JUMP_FORWARD         27  'to 122'

 104      95  SETUP_LOOP           24  'to 122'
          98  LOAD_FAST             1  'obj_list'
         101  GET_ITER         
         102  FOR_ITER             16  'to 121'
         105  STORE_FAST            2  'obj'

 105     108  LOAD_FAST             2  'obj'
         111  LOAD_ATTR             7  'visit'
         114  CALL_FUNCTION_0       0 
         117  POP_TOP          
         118  JUMP_BACK           102  'to 102'
         121  POP_BLOCK        
       122_0  COME_FROM                '95'
       122_1  COME_FROM                '22'

 106     122  LOAD_FAST             0  'rt'
         125  LOAD_ATTR             8  'end'
         128  CALL_FUNCTION_0       0 
         131  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 16


class CocosRenderTarget(object):

    def __init__(self, panel, update_time=-1, size=None):
        self.panel = panel
        self._logic_timer_id = None
        self.rt = None
        self.neox_tex = None
        self.set_panel(panel)
        if not size:
            size = (
             ui_utils.s_designWidth, ui_utils.s_designHeight)
        tex = render.texture.create_empty(int(size[0]), int(size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        rt = cc.RenderTexture.createWithITexture(tex)
        rt.retain()
        self.rt = rt
        self.neox_tex = tex
        self.set_update_time(update_time)
        return

    def destroy(self):
        self.stop_timer()
        self.rt.release()
        self.rt = None
        self.neox_tex = None
        self.panel = None
        return

    def get_render_target(self):
        return self.rt

    def get_texture(self):
        return self.neox_tex

    def set_panel(self, panel):
        import device_compatibility
        self.panel = panel
        size = panel.getContentSize()
        old_design_size = global_data.ui_mgr.design_screen_size
        scale = min(old_design_size.width / size.width, old_design_size.height / size.height)
        if scale < 1:
            render_texture_size = (
             size.width * scale, size.height * scale)
        else:
            render_texture_size = (
             size.width, size.height)
        panel.setAnchorPoint(cc.Vec2(0, 0))
        if device_compatibility.IS_DX:
            panel.setScale(scale)
            panel.SetPosition(0, 0)
        else:
            panel.setScaleX(scale)
            panel.setScaleY(-scale)
            panel.SetPosition(0, size.height * scale)

    def set_update_time(self, update_time):
        if update_time >= 0:
            self._end_time = time.time() + update_time
        else:
            self._end_time = update_time
        self.start_timer()

    def start_timer(self):
        self.stop_timer()
        tm = global_data.game_mgr.get_post_logic_timer()
        self._logic_timer_id = tm.register(func=self.logic_func)

    def stop_timer(self):
        tm = global_data.game_mgr.get_post_logic_timer()
        if self._logic_timer_id:
            tm.unregister(self._logic_timer_id)
        self._logic_timer_id = None
        return

    @sync_exec
    def logic_func(self):
        if self._end_time > 0 and time.time() > self._end_time:
            self.stop_timer()
            return
        if not self.panel or not self.panel.isValid():
            return
        self.rt.begin()
        if hasattr(self.rt, 'addCommandsForNode'):
            self.rt.addCommandsForNode(self.panel.get())
        else:
            self.panel.visit()
        self.rt.end()


DEFAULT_RT_CONF = {'scn_bg_color': 16232035,
   'cam_fov': 50,
   'rt_width': 780,
   'rt_height': 780,
   'cam_euler': math3d.vector(360 / 180 * math.pi, 181.32 / 180 * math.pi, 0.52 / 180 * math.pi),
   'cam_pos': math3d.vector(-4, 11, 31)
   }

class RenderTargetHolder(object):

    def __init__(self, ui_obj, cocos_obj, conf=None, use_active_scene_light=False, all_light=None, use_main_camera=False, format=render.PIXEL_FMT_A8R8G8B8, scene_type=None):
        self.tex = None
        self.rt = None
        import weakref
        self.ui_obj = weakref.ref(ui_obj) if ui_obj else None
        self.cocos_obj = weakref.ref(cocos_obj) if cocos_obj else None
        self._valid = True
        self.conf = conf or DEFAULT_RT_CONF
        self._use_active_scene_light = use_active_scene_light
        self._all_lights_names = all_light
        self._use_main_camera = use_main_camera
        self._need_script_update = True
        self._main_light = None
        self.tick_callback = None
        self.render_tick_callback = None
        self.render_max_count = 0
        self.render_count = 0
        self._format = format
        self._scene_type = scene_type
        self.init_render_target()
        return

    def set_up_scene(self):
        if self._scene_type:
            scene_conf = confmgr.get('scenes', self._scene_type)
            self.scn = scene.Scene(self._scene_type, scene_conf, back_load=False, force_sync=True, notify_loading_ui=False)
        else:
            self.scn = world.scene()
            self.set_up_light()
        self.set_up_camera()
        self.set_scene_background_color(self.conf['scn_bg_color'])
        self.scn.set_background_visible(True)
        if hasattr(self.scn, 'enable_fx_target'):
            self.scn.enable_fx_target = False
        self._need_script_update = not hasattr(self.scn, 'enable_auto_update')
        if not self._need_script_update:
            self.scn.enable_auto_update(True)

    def get_light(self):
        return self._main_light

    def sync_main_camera(self):
        scn = global_data.game_mgr.scene
        main_cam = scn.active_camera
        self.camera.position = main_cam.position
        self.camera.world_rotation_matrix = main_cam.world_rotation_matrix
        self.camera.set_perspect(main_cam.fov, main_cam.aspect, *main_cam.z_range)

    def set_up_camera(self):
        if self._scene_type:
            self.camera = self.scn.active_camera
        else:
            self.camera = self.scn.create_camera(True)
        if self._use_main_camera:
            self.sync_main_camera()
            return
        self.camera.position = self.conf['cam_pos']
        if 'cam_forward' in self.conf:
            self.camera.world_rotation_matrix = math3d.matrix.make_orient(self.conf['cam_forward'], math3d.vector(0, 1, 0))
        elif 'cam_euler' in self.conf:
            self.camera.world_rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(self.conf['cam_euler']))

    def apply_conf(self, conf_name):
        if self.scn:
            conf = confmgr.get('c_env_config', 'light', conf_name, 'on_ground')
            if conf:
                if self._main_light:
                    self._main_light.intensity = conf['MainLightIntensity']
                    self._main_light.diffuse = color_int(*conf['MainLightColor'])
                if global_data.is_ue_model:
                    if getattr(self.scn, 'set_sky_light', None):
                        self.scn.set_sky_light(*[ int(x) for x in conf['SkyLightColor'] ])
                    if getattr(self.scn, 'set_sky_light_intensity', None):
                        self.scn.set_sky_light_intensity(float(conf['SkyLightIntensity']))
                    if getattr(self.scn, 'set_second_dir_light_enable', None):
                        self.scn.set_second_dir_light_enable(float(conf['SecondDirLightEnable']))
                        self.scn.set_second_dir_light_dir(*[ float(x) for x in conf['SecondDirLightDir'][:-1] ])
                        self.scn.set_second_dir_light_color(*[ float(x / 255) for x in conf['SecondDirLightColor'] ])
                        self.scn.set_second_dir_light_intensity(float(conf['SecondDirLightIntensity']))
                    self.scn.ambient_color = color_int(*conf['Ambient'])
                    skip_set = set(('MainLightIntensity', 'Ambient', 'MainLightColor',
                                    'SkyLightColor', 'SkyLightIntensity', 'SecondDirLightEnable',
                                    'SecondDirLightDir', 'SecondDirLightColor', 'SecondDirLightIntensity'))
                    for k, v in six.iteritems(conf):
                        if k in skip_set:
                            continue
                        if isinstance(v, list):
                            v = color_int(*v)
                        self.scn.set_global_uniform(k, v)

        return

    def set_up_light(self):
        active_scene = world.get_active_scene()
        if not active_scene:
            return
        if self._all_lights_names:
            for one_light_name in self._all_lights_names:
                one_src_light = active_scene.get_light(one_light_name)
                if one_src_light:
                    one_dest_light = self.scn.create_light(one_src_light.type)
                    one_dest_light.direction = one_src_light.direction
                    one_dest_light.ambient = one_src_light.ambient
                    one_dest_light.diffuse = one_src_light.diffuse
                    one_dest_light.specular = 4291611852L
                    center, radius = one_src_light.get_shadow_caster_info()
                    one_dest_light.set_shadow_caster_info(center, radius)
                    one_dest_light.shadow_quality = one_src_light.shadow_quality
                    one_dest_light.shadow_bias = one_src_light.shadow_bias
                    one_dest_light.intensity = one_src_light.intensity
                    one_dest_light.enable_lit = one_src_light.enable_lit
                    if not self._main_light:
                        self._main_light = one_dest_light

        if not self._main_light:
            main_light = self.scn.create_light(world.LIGHT_TYPE_DIRECTION)
            main_light.direction = math3d.vector(0.3, -0.2, -0.5)
            main_light.ambient = 4287664272L
            main_light.diffuse = 4292730333L
            main_light.specular = 4291611852L
            main_light.set_shadow_caster_info(1300, 0)
            main_light.shadow_quality = world.SHADOWMAP_QUALITY_HIGH
            main_light.shadow_bias = math3d.vector(0.2, 0.2, 0.2)
            main_light.intensity = 3.0
            main_light.enable_lit = True
            self._main_light = main_light

    def set_scene_background_color(self, color):
        if self.scn:
            self.scn.background_color = color
            self.scn.ambient_color = color

    def init_render_target(self):
        self.set_up_scene()
        target_width = self.conf['rt_width']
        target_height = self.conf['rt_height']
        self.tex = render.texture.create_empty(int(target_width), int(target_height), self._format, True)
        self.rt = render.create_render_target(self.tex, None, render.PIXEL_FMT_D24S8)
        self.setup_render_texture()
        if not self._use_main_camera:
            self.camera.set_perspect(self.conf['cam_fov'], float(target_width) / target_height, 5, 1000)
        return

    def setup_render_texture(self):
        import cc
        import game3d
        import device_compatibility
        from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
        from common.uisys.uielment.CCUIImageView import CCUIImageView
        from common.const.cocos_constant import ONE_MINUS_SRC_ALPHA, ONE
        if self.cocos_obj:
            sprit = self.cocos_obj() if 1 else None
            return sprit or None
        else:
            tex = cc.Texture2D.createWithITexture(self.tex)
            if type(sprit) == CCScale9Sprite:
                sprit.getSprite().setTexture(tex)
                sprit.getSprite().setBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
                sprit.getSprite().getTexture().setAntiAliasTexParameters()
            elif type(sprit) == CCUIImageView:
                sprit.getVirtualRenderer().getSprite().setTexture(tex)
                sprit.SetBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
                sprit.getVirtualRenderer().getSprite().getTexture().setAntiAliasTexParameters()
            else:
                sprit.setTexture(tex)
                sprit.setBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
                sprit.getTexture().setAntiAliasTexParameters()
            if device_compatibility.IS_DX:
                sprit.setFlippedY(False)
            else:
                sprit.setFlippedY(True)
            sprit.setVisible(True)
            return

    def add_model(self, model, pos=math3d.vector(0, 0, 0), rotation_matrix=math3d.matrix(), scale=math3d.vector(1, 1, 1), cast_shadow=True):
        model.position = pos
        model.scale = scale
        model.rotation_matrix = rotation_matrix
        model.visible = True
        model.set_enable_normal_update(True)
        model.cast_shadow = cast_shadow
        model.receive_shadow = True
        self.scn.add_object(model)

    def add_sfx(self, sfx, pos=math3d.vector(0, 0, 0), rotation_matrix=math3d.matrix(), scale=math3d.vector(1, 1, 1)):
        sfx.position = pos
        sfx.scale = scale
        sfx.world_rotation_matrix = rotation_matrix
        self.scn.add_object(sfx)

    def remove_object(self, obj):
        self.scn.remove_object(obj)

    def del_sfx(self, sfx):
        self.scn.remove_object(sfx)

    def del_model(self, model):
        self.scn.remove_object(model)
        model.clear_events()
        model.destroy()

    def destroy(self):
        self.camera = None
        self.stop_render_target()
        if self._scene_type is not None:
            self.scn.on_exit()
        self.scn.destroy()
        self.scn = None
        self.tex = None
        if self.rt is not None:
            render.release_render_target(self.rt)
        self.rt = None
        self._valid = False
        return

    def start_render_target(self, render_max_count=0):
        self.render_max_count = render_max_count
        self.render_count = 0
        global_data.ui_mgr.add_render_target_holder(self)

    def stop_render_target(self):
        global_data.ui_mgr.remove_render_target_holder(self)

    def tick(self):
        if self._need_script_update:
            self.scn.update()
        if self.tick_callback:
            self.tick_callback()

    @sync_exec
    def safe_render_tick(self):
        self.render_tick_callback()

    def set_track_camera(self, track_file, animation_name, socket, restore=True, event_callback=None):
        pass

    def rotate_camera(self, angle):
        pass

    def reset_camera(self):
        pass

    @sync_exec
    def set_new_env(self, env_path, env_conf):
        if not self.scn or not self.scn.valid or not env_path or not env_conf:
            return
        self.scn.load_env_new(env_path)
        self.apply_conf(env_conf)


from logic.gcommon.common_const import lobby_const
LOBBY_SCENE_JZ_REPLAY_MODEL_FILE = {lobby_const.LOBBY_SCENE_TYPE_WSJ: 'lobby_models_wsj_jz',
   lobby_const.LOBBY_SCENE_TYPE_SDJ: 'lobby_models_sdj_jz'
   }

class RenderTargetHolderLobbyMirr(RenderTargetHolder):

    def __init__(self, ui_obj, cocos_obj, conf=None, use_active_scene_light=False, all_light=None, use_main_camera=False, format=render.PIXEL_FMT_A8R8G8B8, scene_type=None):
        self.cur_scene_type = lobby_const.LOBBY_SCENE_TYPE_DEFAULT
        self.skin_lobby_models = {}
        self.default_lobby_models = []
        super(RenderTargetHolderLobbyMirr, self).__init__(ui_obj, cocos_obj, conf, use_active_scene_light, all_light, use_main_camera, format, scene_type)

    def init_default_models(self):
        for model in self.scn.get_models():
            self.default_lobby_models.append(model)

    def set_up_scene(self):
        super(RenderTargetHolderLobbyMirr, self).set_up_scene()
        self.init_default_models()

    def create_model_callback(self, model_info, model_list):
        scn = self.scn

        def callback(model):
            rotation = model_info.get('Rotation')
            if rotation:
                rot = math3d.matrix()
                rot.set_all(rotation)
                model.rotation_matrix = rot.rotation
            scale = model_info.get('Scale')
            if scale:
                model.scale = math3d.vector(*scale)
            lightmap_info = model_info.get('Lightmap')
            if lightmap_info:
                path = lightmap_info['LightmapPath']
                uv_ofs = lightmap_info['uv_ofs']
                uv_scale = lightmap_info['uv_scale']
                lightmap_scale = lightmap_info['lightmap_scale']
                lightmap_add = lightmap_info['lightmap_add']
                model.manual_apply_lightmap_ue(path, 2, uv_scale[0], uv_scale[1], uv_ofs[0], uv_ofs[1], lightmap_scale[0], lightmap_scale[1], lightmap_scale[2], lightmap_add[0], lightmap_add[1], lightmap_add[2], lightmap_add[3], True, '_sep_rgb')
            model_list.append(model)

        position = model_info['Position']
        global_data.model_mgr.create_model_in_scene(model_info['FilePath'], pos=math3d.vector(*position), on_create_func=callback, create_scene=scn)

    def replace_scene_models(self, lobby_scene_type):
        if self.cur_scene_type == lobby_scene_type:
            return
        scn = self.scn
        if self.cur_scene_type == lobby_const.LOBBY_SCENE_TYPE_DEFAULT:
            old_models = self.default_lobby_models
        else:
            old_models = self.skin_lobby_models.get(self.cur_scene_type, [])
        if lobby_scene_type == lobby_const.LOBBY_SCENE_TYPE_DEFAULT:
            new_models = self.default_lobby_models
        else:
            new_models = self.skin_lobby_models.get(lobby_scene_type, [])
            if not new_models:
                replace_model_infos = confmgr.get(LOBBY_SCENE_JZ_REPLAY_MODEL_FILE.get(lobby_scene_type), 'models', default={})
                for model_info in replace_model_infos:
                    self.create_model_callback(model_info, new_models)

                self.skin_lobby_models[lobby_scene_type] = new_models
        for model in old_models:
            model.visible = False

        for model in new_models:
            model.visible = True

        self.cur_scene_type = lobby_scene_type
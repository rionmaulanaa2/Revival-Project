# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartDecalCreator.py
from __future__ import absolute_import
from __future__ import print_function
from . import ScenePart
import world
import math3d
import game3d
import render
import math
from common.cfg import confmgr
from common.utils.cocos_utils import getScreenSize, getDesignScreenSize
from logic.vscene.parts.camera.camera_controller.model_decal_cam_ctrl import get_transform_by_sphere_param
from logic.gutils.scene_utils import is_in_lobby
from logic.gutils.dress_utils import get_mecha_model_h_path, get_mecha_model_lod_path
from logic.gutils.item_utils import get_lobby_item_belong_no
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from common.algorithm.resloader import LruResCache
from common.algorithm import resloader
from logic.gutils import skin_define_utils
from logic.manager_agents.manager_decorators import sync_exec
_HASH_TEX0 = game3d.calc_string_hash('Tex0')
_HASH_TEX1 = game3d.calc_string_hash('TexDecal')
_HASH_BASE_X = game3d.calc_string_hash('decal_mat_base_x')
_HASH_BASE_Y = game3d.calc_string_hash('decal_mat_base_y')
_HASH_DECAL_SIZE = game3d.calc_string_hash('decal_size')
STAGE_NONE = 0
STAGE_LOWER = 1
STAGE_UPPER = 2
STAGE_PREVIEW = 3
STAGE_PRE_LOADING = -1
STAGE_LOADING = -2
STAGE_LOADING_HIGH_QUALITY = -3
fov = 30.0
z_near = 1.0
z_far = 10000.0
import device_compatibility
RENDER_TARGET_FORMAT = render.PIXEL_FMT_A8R8G8B8 if device_compatibility.IS_DX else render.PIXEL_FMT_A4R4G4B4

class PartDecalCreator(ScenePart.ScenePart):
    INIT_EVENT = {'clear_decal_data': 'on_clear_decal_data',
       'select_preview_decal': 'on_select_preview_decal',
       'save_preview_decal': 'on_save_preview_decal',
       'add_preview_decal': 'on_add_preview_decal',
       'revert_preview_decal': 'on_revert_preview_decal',
       'del_preview_decal': 'on_del_preview_decal',
       'set_decal_model': 'on_set_model',
       'set_default_decal_data': 'on_set_default_decal_data',
       'exit_decal_scene': 'on_stop_preview_decal',
       'decal_image_change': 'on_decal_image_changed',
       'decal_position_change': 'on_decal_position_changed',
       'decal_rotation_change': 'on_decal_rotation_chagned',
       'decal_size_change': 'on_decal_size_changed',
       'load_decal_data': 'on_load_decal_data',
       'create_high_quality_decal': 'on_create_high_quality_decal',
       'get_decal_data': 'on_get_decal_data',
       'resolution_changed': 'on_resolution_changed',
       'get_decal_stage': 'on_get_decal_stage',
       'get_target_model': 'on_get_target_model'
       }

    def __init__(self, scene, name):
        super(PartDecalCreator, self).__init__(scene, name, True)
        self.init_parameters()

    def init_parameters(self):
        if not global_data.feature_mgr.is_support_model_decal():
            return
        else:
            self.camera = None
            self.events_binded = False
            self.decal_rt_size = 2048
            self.decal_target_size = 2048
            self.decal_rt = None
            self.merge_rt = None
            self.lower_tex = None
            self.preview_tex = None
            self.upper_tex = None
            self.result_tex = None
            self.merge_tex = None
            self.dummy_result_tex = None
            self.decal_scn = None
            self.target_model = None
            self.decal_model = None
            size = game3d.get_window_size()
            self.view_port = (0, 0, size[0], size[1], 0, 1.0)
            self._render_timer_id = None
            self._logic_timer_id = None
            self.decal_size = (150, 150)
            self.decal_scale = 1
            self.decal_position = (0, 0)
            self.decal_rotation = 0
            self.screen_size = getScreenSize()
            self.design_size = getDesignScreenSize()
            self.preview_tex_path = None
            self.decal_param = None
            self.preview_stage = STAGE_NONE
            self.cur_stage_done = False
            self.load_finished_cb = None
            self.cur_selected_idx = 0
            self.new_decal_unsaved = True
            self.cur_decal_data = []
            self.decal_data_list = []
            self.load_high_quality = False
            self.high_quality_decal_data_list = []
            self.high_quality_build_phase = -1
            self.is_collecting_data = True
            self.decal_shader_params = []
            self.lower_params = []
            self.upper_params = []
            self.center_pos = math3d.vector(0, 0, 0)
            self.is_in_lobby = False
            from common.utils import pc_platform_utils
            if pc_platform_utils.is_pc_hight_quality_simple():
                self.quality_config = 'PC'
            else:
                self.quality_config = 'Mobile_LowMem' if global_data.is_low_mem_mode else 'Mobile'
            self.logic_map = {STAGE_LOWER: self._process_lower_stage,
               STAGE_UPPER: self._process_upper_stage,
               STAGE_PREVIEW: self._process_preview_stage,
               STAGE_PRE_LOADING: self._process_pre_loading_state,
               STAGE_LOADING: self._process_loading_stage,
               STAGE_LOADING_HIGH_QUALITY: self._process_loading_high_quality_decal
               }
            self.is_processing_data = False
            max_val = 100 if global_data.battle is None else 20
            self._tex_cache = LruResCache(max_val)
            self.is_init_model_decal_render_targets = False
            self.debug_screen = None
            self.is_mumu_simulator = 'mumu' in global_data.deviceinfo.get_device_model_name() or global_data.channel.is_musdk()
            self._setup_decal_scene()
            return

    def on_get_decal_stage(self):
        if not global_data.feature_mgr.is_support_model_decal():
            return 0
        return self.preview_stage

    def on_get_target_model(self):
        return self.target_model

    def on_enter(self):
        log_error('NX709S_on_PartDecalCreator_enter')
        if not global_data.feature_mgr.is_support_model_decal():
            return
        self.is_in_lobby = is_in_lobby(self.scene().scene_type)
        depth_offset_map = {game3d.PLATFORM_IOS: 2e-05,
           game3d.PLATFORM_ANDROID: 6e-05,
           game3d.PLATFORM_WIN32: 4e-05
           }
        depth_offset = depth_offset_map.get(game3d.get_platform(), 0.0001)
        render.set_model_decal_depth_offset(depth_offset)
        self.dummy_result_tex = render.texture.create_empty(1, 1, RENDER_TARGET_FORMAT, True)
        log_error('NX709S_on_PartDecalCreator_enter_end')

    def on_exit(self):
        log_error('NX709S_on_PartDecalCreator_exit')
        if not global_data.feature_mgr.is_support_model_decal():
            return
        else:
            self.on_stop_preview_decal()
            self.on_clear_model()
            self._stop_render_target_timer()
            self._clear_decal_scene()
            self._clear_merge_scene()
            self._tex_cache.clear()
            self.is_processing_data = False
            render.reset_model_decal_tech()
            self.dummy_result_tex = None
            log_error('NX709S_on_PartDecalCreator_exit_end')
            return

    def on_pause(self, flag):
        pass

    def on_get_decal_data(self):
        return self.cur_decal_data

    def on_stop_preview_decal(self):
        if self.preview_stage == STAGE_PREVIEW:
            if self.new_decal_unsaved:
                self.on_del_preview_decal()
            else:
                self.on_revert_preview_decal(self.cur_selected_idx)

    def async_load_start(self, preview=False, high_quality=False):
        self.decal_textures = [
         None] * len(self.cur_decal_data)
        self.decal_shader_params = []

        def load_cb(tex, load_idx):
            self.decal_textures[load_idx] = tex
            if None in self.decal_textures:
                return
            else:
                if not self.decal_model:
                    self.process_data_end()
                    return
                for idx, param_data in enumerate(self.cur_decal_data):
                    decal_texture = self.decal_textures[idx]
                    decal_param = self._convert_to_shader_param(param_data[1:])
                    self.decal_shader_params.append([decal_texture, decal_param])
                    if preview:
                        self.lower_params.append([decal_texture, decal_param])

                self.decal_textures = []
                if preview:
                    self._next_stage()
                else:
                    self.load_high_quality = high_quality
                    self._start_pre_load_data()
                self._start_render_target_timer()
                return

        for load_idx, param_data in enumerate(self.cur_decal_data):
            tex_path = skin_define_utils.get_decal_path_by_item_id(param_data[0])
            self._create_texture_async(tex_path, load_cb, load_idx)

        return

    def on_load_decal_data(self, model, data, skin_id, load_cb, lod_level=0, is_avatar_model=False):
        if not data:
            return
        self.decal_data_list.append((model, data, skin_id, load_cb, lod_level, is_avatar_model))
        if not self.is_processing_data:
            self.process_next_decal_data()

    def on_create_high_quality_decal(self, model, data, skin_id, load_cb, lod_level=0):
        if device_compatibility.IS_DX or not data or game3d.get_render_device() == game3d.DEVICE_METAL or self.is_mumu_simulator:
            return
        self.high_quality_decal_data_list.append((model, data, skin_id, load_cb, lod_level))
        if not self.is_processing_data:
            self.process_next_high_quality_data()

    def process_next_decal_data(self):
        if not self.decal_data_list:
            self.process_data_end()
            return
        while True:
            model, data, skin_id, load_cb, lod_level, is_avatar_model = self.decal_data_list[0]
            del self.decal_data_list[0]
            if load_cb and data and model and model.valid:
                break
            if not self.decal_data_list:
                self.process_data_end()
                return

        self.is_processing_data = True
        lod0_size = 2048 if device_compatibility.IS_DX else 1024
        lod1_size = 1024 if device_compatibility.IS_DX else 512
        lod_quality = {-1: lod0_size,
           0: lod0_size,
           1: lod1_size,
           2: 256,
           3: 256
           }

        def start_decal_imp():
            size = lod_quality[lod_level]
            self.result_tex = render.texture.create_empty(size, size, RENDER_TARGET_FORMAT, True)
            self.load_finished_cb = load_cb
            self.cur_decal_data = data
            if self.result_tex:
                render.set_decal_dest_texture(self.result_tex)
            self._reset_stage()
            self.async_load_start()

        self.on_set_model(model, skin_id, start_decal_imp, lod_level, is_avatar_model)

    def process_next_high_quality_data(self):
        if not self.high_quality_decal_data_list:
            return
        while True:
            model, data, skin_id, load_cb, lod_level = self.high_quality_decal_data_list[0]
            del self.high_quality_decal_data_list[0]
            if data and load_cb and model and model.valid:
                break
            if not self.high_quality_decal_data_list:
                self.process_data_end()
                return

        self.is_processing_data = True

        def start_decal_imp():
            self.cur_decal_data = data
            self.load_finished_cb = load_cb
            self._reset_stage()
            self.async_load_start(high_quality=True)

        self.on_set_model(model, skin_id, start_decal_imp, lod_level)

    def on_clear_decal_data(self):
        self.cur_decal_data = []
        self.decal_shader_params = []
        self.lower_params = []
        self.upper_params = []
        self._show_model_decal(False)
        self._stop_render_target_timer()
        self._reset_stage()

    def on_select_preview_decal(self, idx):
        if idx >= len(self.cur_decal_data) or idx < 0:
            return
        self._reset_stage()
        self.lower_params = self.decal_shader_params[0:idx]
        self.upper_params = self.decal_shader_params[idx + 1:]
        decal_data = self.cur_decal_data[idx]
        item_id, param = decal_data[0], decal_data[1:]
        tex_path = skin_define_utils.get_decal_path_by_item_id(item_id)
        r, theta, phi = param[0], math.radians(param[1]), math.radians(param[2])
        global_data.emgr.set_decal_camera_param.emit(r, theta, phi)
        ndc_pos = self._data_pos_to_ndc_pos(*param[3:5])
        pos = self._ndc_pos_to_cocos_desgin_pos(*ndc_pos)
        rot = param[5]
        scale = param[6]
        global_data.emgr.set_preview_ui_by_param.emit(pos, rot, scale)
        self.decal_position = ndc_pos
        self.decal_rotation = rot
        self.decal_scale = scale
        self._on_update_decal_mat()
        self.cur_selected_idx = idx
        self.on_start_decal_preview(tex_path, next_tag=True)

    def on_revert_preview_decal(self, idx):
        if idx >= len(self.cur_decal_data) or idx < 0:
            return
        else:
            decal_data = self.cur_decal_data[idx]
            item_id, param = decal_data[0], decal_data[1:]
            r, theta, phi = param[0], math.radians(param[1]), math.radians(param[2])
            global_data.emgr.set_decal_camera_param.emit(r, theta, phi)
            self.lower_params = []
            self.upper_params = []
            render.set_decal_preview_texture(None)
            self._reset_stage()
            self.preview_uv_none = True
            self._reset_stage()
            self.async_load_start(preview=True)
            return

    def on_add_preview_decal(self, tex_path):
        if self.preview_stage != STAGE_NONE:
            return
        self.lower_params = self.decal_shader_params
        self.upper_params = []
        self.cur_selected_idx = len(self.lower_params)
        self.on_start_decal_preview(tex_path)
        self.new_decal_unsaved = True

    def on_del_preview_decal(self):
        if self.cur_selected_idx == 0 and len(self.cur_decal_data) <= 1:
            self.on_clear_decal_data()
            return
        else:
            if 0 <= self.cur_selected_idx < len(self.cur_decal_data):
                del self.cur_decal_data[self.cur_selected_idx]
            self.lower_params = []
            self.upper_params = []
            render.set_decal_preview_texture(None)
            self.preview_uv_none = True
            self._reset_stage()
            self.async_load_start(preview=True)
            self.new_decal_unsaved = False
            return

    def on_start_decal_preview(self, path, next_tag=True):
        self.preview_tex_path = path

        def load_cb(tex):
            render.set_decal_preview_texture(tex)
            self.preview_uv_none = False
            if next_tag:
                self._next_stage()
            self._start_render_target_timer()

        self._create_texture_async(path, load_cb)

    def on_save_preview_decal(self):
        self._reset_stage()
        self.decal_shader_params = []
        self.decal_shader_params.extend(self.lower_params)
        radius, theta, phi = global_data.emgr.get_decal_camera_param.emit()[0]
        base_x, base_y = self.decal_param
        euler = math3d.matrix_to_euler(self.camera.rotation_matrix)
        pos = self.camera.position
        if self.decal_model:
            model_scale = self.decal_model.scale.y
        else:
            model_scale = skin_define_utils.get_mecha_model_default_scale()
        cur_param = [
         self._tex_cache[self.preview_tex_path], (pos.x, pos.y, pos.z, euler.x, euler.y, euler.z, base_x[0], base_x[1], base_x[2], base_y[0], base_y[1], base_y[2], model_scale)]
        self.decal_shader_params.append(cur_param)
        self.decal_shader_params.extend(self.upper_params)
        posx, posy = self._ndc_pos_to_data_pos(*self.decal_position)
        item_id = skin_define_utils.get_decal_item_id_by_path(self.preview_tex_path)
        saved_decal_data = [item_id, radius, math.degrees(theta), math.degrees(phi), posx, posy, self.decal_rotation, self.decal_scale, model_scale]
        if self.cur_selected_idx >= len(self.cur_decal_data):
            self.cur_decal_data.append(saved_decal_data)
        else:
            self.cur_decal_data[self.cur_selected_idx] = saved_decal_data
        self._stop_render_target_timer()
        self.new_decal_unsaved = False

    def on_set_default_decal_data(self, data, extra_callback=None):
        if self.preview_stage != STAGE_NONE:
            return
        self.cur_decal_data = data
        self.preview_uv_none = True
        self.async_load_start(preview=True)
        if extra_callback and callable(extra_callback):
            extra_callback()

    def process_data_end(self):
        if self.decal_data_list:
            global_data.game_mgr.next_exec(lambda : self.process_next_decal_data())
        elif self.high_quality_decal_data_list:
            global_data.game_mgr.next_exec(lambda : self.process_next_high_quality_data())
        else:
            self.is_processing_data = False

    def on_set_model(self, active_model, skin_id=None, set_cb=None, lod_level=0, is_avatar_model=False):
        if global_data.battle is None and self.target_model == active_model:
            if set_cb:
                set_cb()
            return
        else:
            resloader.del_res_attr(self, 'decal_model')
            self.target_model = None
            self.decal_model = None
            self.decal_skin_id = int(skin_id)

            def load_cb(decal_model, data, *args):
                if not decal_model or not decal_model.valid:
                    self.process_data_end()
                    return
                else:
                    if not active_model or not active_model.valid:
                        self.process_data_end()
                        return
                    decal_model.position = math3d.vector(0, 0, 0)
                    decal_model.scale = active_model.scale
                    decal_model.show_ext_technique(render.EXT_TECH_MODEL_DECAL, True)
                    render.set_decal_preview_texture(None)
                    self.decal_scn and self.decal_scn.add_object(decal_model)
                    decal_model.play_animation(skin_define_utils.get_default_skin_define_anim(skin_id))
                    if global_data.battle is None:
                        max_val = 10 if 1 else 4
                        render.set_max_decal_perframe(max_val)
                        y = decal_model.scale.y * decal_model.bounding_box.y
                        belong_id = get_lobby_item_belong_no(skin_id)
                        mecha_id = mecha_lobby_id_2_battle_id(belong_id)
                        y_offset = confmgr.get('skin_define_camera').get(str(mecha_id), {}).get('iYOffset', None)
                        y_offset or log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
                    else:
                        y = y_offset
                    pos = math3d.vector(0, y, 0)
                    self.center_pos = pos
                    self.target_model = active_model
                    if set_cb:
                        set_cb()
                    return

            model_path = get_mecha_model_h_path(None, skin_id, False) if global_data.battle is None else get_mecha_model_lod_path(None, skin_id, lod_level, False)
            if global_data.decal_lod:
                model_path = get_mecha_model_h_path(None, skin_id)
                idx = model_path.find('h.gim')
                model_path = model_path[0:idx] + global_data.decal_lod
            resloader.load_res_attr(self, 'decal_model', model_path, load_cb, (model_path, 'decal_model'), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            return

    def on_clear_model--- This code section failed: ---

 547       0  LOAD_CONST            0  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  'target_model'

 548       9  LOAD_GLOBAL           2  'resloader'
          12  LOAD_ATTR             3  'del_res_attr'
          15  LOAD_ATTR             1  'target_model'
          18  CALL_FUNCTION_2       2 
          21  POP_TOP          
          22  LOAD_CONST            0  ''
          25  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 18

    def on_decal_image_changed(self, path):
        self.preview_tex_path = path

        def load_cb(tex):
            if self.decal_model and self.decal_model.valid:
                render.set_decal_preview_texture(tex)
                self.preview_uv_none = False

        self._create_texture_async(path, load_cb)

    def on_decal_position_changed(self, x, y):
        self.decal_position = self._cocos_desgin_pos_to_ndc_pos(x, y)
        self._on_update_decal_mat()

    def on_decal_rotation_chagned(self, angle):
        self.decal_rotation = angle
        self._on_update_decal_mat()

    def on_decal_size_changed(self, scale):
        self.decal_scale = scale
        self._on_update_decal_mat()

    def on_upload_decal_data(self):
        upload_data = []
        for data in self.cur_decal_data:
            upload_data.append(data[0:9])

        main_skin_id = skin_define_utils.get_main_skin_id(self.decal_skin_id)
        global_data.player.set_mecha_decal(main_skin_id, upload_data)

    def _convert_to_shader_param(self, param):
        radius, theta, phi = param[0], math.radians(param[1]), math.radians(param[2])
        model_scale = param[7]
        center_pos_y = model_scale * self.decal_model.bounding_box.y
        belong_id = get_lobby_item_belong_no(self.decal_skin_id)
        mecha_id = mecha_lobby_id_2_battle_id(belong_id)
        y_offset = confmgr.get('skin_define_camera').get(str(mecha_id), {}).get('iYOffset', None)
        if not y_offset:
            log_error('180.xlsx sheet.CameraY => current mecha_id not exit!!!')
        else:
            center_pos_y = y_offset
        pos, rot = get_transform_by_sphere_param(radius, theta, phi, math3d.vector(0, center_pos_y, 0))
        euler = math3d.matrix_to_euler(rot)
        self.decal_position = self._data_pos_to_ndc_pos(*param[3:5])
        self.decal_rotation = param[5]
        self.decal_scale = param[6]
        base_x, base_y = self._on_update_decal_mat()
        return (
         pos.x, pos.y, pos.z, euler.x, euler.y, euler.z, base_x[0], base_x[1], base_x[2], base_y[0], base_y[1], base_y[2], model_scale)

    def _on_update_decal_mat(self):
        x, y = self.decal_position
        phi = math.radians(self.decal_rotation)
        S = math3d.matrix()
        R = math3d.matrix()
        T = math3d.matrix()
        w, h = self.decal_size
        ds_w, ds_h = self.design_size.width, self.design_size.height
        decal_scale = (w * 1.0 / ds_w * self.decal_scale, h * 1.0 / ds_h * self.decal_scale)
        S.set_all(decal_scale[0], 0, 0, 0, 0, decal_scale[1], 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        T.set_all(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, x, y, 0, 1)
        ST = S * T
        ST.inverse()
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        R.set_all(cos_phi, -sin_phi, 0, 0, sin_phi, cos_phi, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        screen_to_decal = ST * R
        base_x = (
         screen_to_decal.get(0, 0), screen_to_decal.get(1, 0), screen_to_decal.get(3, 0))
        base_y = (screen_to_decal.get(0, 1), screen_to_decal.get(1, 1), screen_to_decal.get(3, 1))
        if self.decal_model and self.decal_model.valid:
            self.decal_model.set_ext_technique_var(render.EXT_TECH_MODEL_DECAL, _HASH_BASE_X, 'decal_mat_base_x', base_x)
            self.decal_model.set_ext_technique_var(render.EXT_TECH_MODEL_DECAL, _HASH_BASE_Y, 'decal_mat_base_y', base_y)
        self.decal_param = (base_x, base_y)
        return (
         base_x, base_y)

    def _cocos_desgin_pos_to_ndc_pos(self, x, y):
        x = x / self.design_size.width
        y = y / self.design_size.height
        return (
         2.0 * x - 1, 2.0 * y - 1)

    def _ndc_pos_to_cocos_desgin_pos(self, x, y):
        x = (x + 1.0) * 0.5 * self.design_size.width
        y = (y + 1.0) * 0.5 * self.design_size.height
        return (
         x, y)

    def _ndc_pos_to_data_pos(self, x, y):
        x = (x * self._aspect_ratio() + 4.0) * 0.5
        y = (y + 1.0) * 0.5
        return (
         x, y)

    def _data_pos_to_ndc_pos(self, x, y):
        return (
         (2.0 * x - 4.0) / self._aspect_ratio(), 2.0 * y - 1)

    def _start_pre_load_data(self):
        self.preview_stage = STAGE_PRE_LOADING

    def _start_load_data(self):
        if not self.decal_shader_params:
            return
        high_quality = self.load_high_quality
        self.preview_stage = STAGE_LOADING_HIGH_QUALITY if high_quality else STAGE_LOADING
        self.cur_stage_done = False
        self.high_quality_build_phase = 0
        self.is_collecting_data = True
        render.set_high_quality_build_phase(0 if high_quality else -1, True)

    def _update_camera(self):
        active_camera = global_data.game_mgr.scene.active_camera
        self.camera.position = active_camera.position
        self.camera.rotation_matrix = active_camera.rotation_matrix

    def _setup_decal_scene(self):
        self.decal_scn = world.scene()
        color = 0
        self.decal_scn.background_color = color
        self.decal_scn.ambient_color = color
        self.decal_scn.release_collision()
        self.camera = self.decal_scn.create_camera(True)
        self.camera.set_perspect(fov, self._aspect_ratio(), z_near, z_far)
        rotation = math3d.matrix.make_orient(math3d.vector(0, 0, 1), math3d.vector(0, 1, 0))
        self.camera.position = math3d.vector(0, 0, -100)
        self.camera.rotation_matrix = rotation
        self.decal_scn.set_background_visible(False)
        DecalSize = 2048 if global_data.battle is None else 1536
        DecalQualityConfig = {'PC': [
                DecalSize, DecalSize],
           'Mobile': [
                    DecalSize, DecalSize],
           'Mobile_LowMem': [
                           1024, 1024]
           }
        self.decal_rt_size, self.decal_target_size = DecalQualityConfig[self.quality_config]
        return

    def on_resolution_changed--- This code section failed: ---

 705       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'camera'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    55  'to 55'

 706      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'camera'
          18  JUMP_IF_FALSE_OR_POP    51  'to 51'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             1  'camera'
          27  LOAD_ATTR             2  'set_perspect'
          30  LOAD_GLOBAL           3  'fov'
          33  LOAD_FAST             0  'self'
          36  LOAD_ATTR             4  '_aspect_ratio'
          39  CALL_FUNCTION_0       0 
          42  LOAD_GLOBAL           5  'z_near'
          45  LOAD_GLOBAL           6  'z_far'
          48  CALL_FUNCTION_4       4 
        51_0  COME_FROM                '18'
          51  POP_TOP          
          52  JUMP_FORWARD          0  'to 55'
        55_0  COME_FROM                '52'

 707      55  LOAD_GLOBAL           7  'getScreenSize'
          58  CALL_FUNCTION_0       0 
          61  LOAD_FAST             0  'self'
          64  STORE_ATTR            8  'screen_size'

 708      67  LOAD_GLOBAL           9  'getDesignScreenSize'
          70  CALL_FUNCTION_0       0 
          73  LOAD_FAST             0  'self'
          76  STORE_ATTR           10  'design_size'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def init_model_decal_render_targets(self):
        if not self.is_init_model_decal_render_targets and self.is_in_lobby:
            final_size = self.decal_target_size
            self.merge_tex = render.texture.create_empty(int(final_size), int(final_size), RENDER_TARGET_FORMAT, True)
            self.preview_tex = render.texture.create_empty(int(final_size), int(final_size), RENDER_TARGET_FORMAT, True)
            self.lower_tex = render.texture.create_empty(int(final_size), int(final_size), RENDER_TARGET_FORMAT, True)
            self.upper_tex = render.texture.create_empty(int(final_size), int(final_size), RENDER_TARGET_FORMAT, True)
            render.init_model_decal_render_targets(self.lower_tex, self.preview_tex, self.upper_tex, self.merge_tex)
            self.is_init_model_decal_render_targets = True

    def _clear_decal_scene(self):
        self.camera = None
        if self.decal_scn:
            self.decal_scn.destroy()
            self.decal_scn = None
        if self.decal_rt:
            render.release_render_target(self.decal_rt)
            self.decal_rt = None
        return

    def _clear_merge_scene(self):
        self.upper_tex = None
        self.preview_tex = None
        self.lower_tex = None
        return

    def _create_rt(self, size):
        tex = render.texture.create_empty(int(size), int(size), RENDER_TARGET_FORMAT, True)
        if game3d.get_render_device() == game3d.DEVICE_METAL:
            rt = render.create_render_target(tex, None, render.PIXEL_FMT_D24S8)
        else:
            rt = render.create_render_target(tex, None, render.PIXEL_FMT_D16)
        return (rt, tex)

    def _aspect_ratio(self):
        size = game3d.get_window_size()
        return size[0] * 1.0 / size[1]

    def _render_func(self):
        if not self.decal_model or not self.decal_scn or self.preview_stage == STAGE_NONE:
            return
        if not self.decal_rt:
            self.decal_rt, _ = self._create_rt(self.decal_rt_size)
        self.decal_scn.render(self.decal_rt, self.view_port)
        if self.preview_stage == STAGE_PREVIEW and self.preview_uv_none:
            self._reset_stage()
            self._stop_render_target_timer()

    def _logic_func(self):
        if self.preview_stage == STAGE_NONE:
            return
        if self.preview_stage in self.logic_map:
            self.logic_map[self.preview_stage]()
        if self.preview_stage == STAGE_PREVIEW:
            self._update_camera()
        self.decal_scn and self.decal_scn.update()

    def _next_stage(self):
        self.preview_stage += 1
        self.cur_stage_done = False

    def _reset_stage(self):
        self.preview_stage = STAGE_NONE
        self.cur_stage_done = True

    @sync_exec
    def _process_lower_stage(self):
        self.init_model_decal_render_targets()
        render.enable_tile_model_decal(True)
        if self.cur_stage_done:
            if render.is_decal_finished():
                self._next_stage()
                render.push_decal_data_to_draw(None, ())
                if self.upper_params:
                    for tex, param in self.upper_params:
                        render.push_decal_data_to_draw(tex, param)

                render.set_decal_dest_texture(self.upper_tex)
        else:
            render.push_decal_data_to_draw(None, ())
            if self.lower_params:
                for tex, param in self.lower_params:
                    render.push_decal_data_to_draw(tex, param)

            render.set_decal_dest_texture(self.lower_tex)
            self.cur_stage_done = True
        return

    @sync_exec
    def _process_upper_stage(self):
        self.init_model_decal_render_targets()
        if render.is_decal_finished():
            self._next_stage()
            self._on_update_decal_mat()
            render.set_decal_dest_texture(self.preview_tex)

    @sync_exec
    def _process_preview_stage(self):
        if self.cur_stage_done:
            return
        self._show_model_decal(True)
        self._on_update_decal_mat()
        self.cur_stage_done = True

    @sync_exec
    def _process_pre_loading_state(self):
        self._start_load_data()

    @sync_exec
    def _process_loading_stage(self):
        render.enable_tile_model_decal(False)
        if self.cur_stage_done:
            if render.is_decal_finished():
                if self.load_finished_cb:
                    try:
                        self.load_finished_cb(self.result_tex)
                    except Exception as e:
                        print(e)

                    self.result_tex = None
                    self.load_finished_cb = None
                self._reset_stage()
                self._stop_render_target_timer()
                self.decal_shader_params = []
                self.process_data_end()
                if self.dummy_result_tex:
                    render.set_decal_dest_texture(self.dummy_result_tex)
        else:
            render.push_decal_data_to_draw(None, ())
            for tex, param in self.decal_shader_params:
                render.push_decal_data_to_draw(tex, param)

            self.cur_stage_done = True
        return

    @sync_exec
    def _process_loading_high_quality_decal(self):
        render.enable_tile_model_decal(True)
        if self.cur_stage_done:
            if render.is_decal_finished():
                self.cur_stage_done = False
                if self.high_quality_build_phase == 3:
                    if self.is_collecting_data:
                        self.is_collecting_data = False
                        self.high_quality_build_phase = 0
                        render.set_high_quality_build_phase(0, False)
                        return
                    if self.load_finished_cb:
                        results = render.get_high_quality_decal_texture()
                        self.load_finished_cb(results[0], results[1], self.decal_rt_size * 2)
                        self.load_finished_cb = None
                    self._reset_stage()
                    self._stop_render_target_timer()
                    self.decal_shader_params = []
                    self.high_quality_build_phase = -1
                    render.set_high_quality_build_phase(-1, True)
                    self.process_data_end()
                else:
                    self.high_quality_build_phase += 1
                    render.set_high_quality_build_phase(self.high_quality_build_phase, self.is_collecting_data)
        else:
            if self.high_quality_build_phase == 0:
                render.push_decal_data_to_draw(None, ())
            for tex, param in self.decal_shader_params:
                render.push_decal_data_to_draw(tex, param)

            self.cur_stage_done = True
        return

    def _show_model_decal(self, show):
        self.init_model_decal_render_targets()
        model = self.target_model
        if not model or not model.valid:
            return
        val = 'TRUE' if show else 'FALSE'
        model.all_materials.set_macro('DECAL_ENABLE', val)
        if self.merge_tex:
            model.all_materials.set_texture(_HASH_TEX1, 'TexDecal', self.merge_tex)
        global_data.game_mgr.next_exec(lambda : model.all_materials.rebuild_tech())

    def _start_render_target_timer(self):
        self._stop_render_target_timer()
        self._render_timer_id = global_data.game_mgr.get_render_timer().register(func=self._render_func)
        self._logic_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self._logic_func)

    def _stop_render_target_timer(self):
        if not self._render_timer_id:
            return False
        else:
            if self._render_timer_id:
                global_data.game_mgr.get_render_timer().unregister(self._render_timer_id)
            if self._logic_timer_id:
                global_data.game_mgr.get_post_logic_timer().unregister(self._logic_timer_id)
            self._render_timer_id = None
            self._logic_timer_id = None
            return

    def _create_texture_async(self, tex_path, create_cb, load_idx=None):
        if tex_path in self._tex_cache:
            if load_idx is None:
                create_cb(self._tex_cache[tex_path])
            else:
                create_cb(self._tex_cache[tex_path], load_idx)
            return
        else:

            def load_cb_idx(tex, idx):
                self._tex_cache[tex_path] = tex
                create_cb(tex, idx)

            def load_cb(tex):
                self._tex_cache[tex_path] = tex
                create_cb(tex)

            render.texture(tex_path, False, False, render.TEXTURE_TYPE_NORMAL, game3d.ASYNC_HIGH, load_cb if load_idx is None else load_cb_idx, load_idx)
            return

    def create_debug_tex(self):
        if self.debug_screen:
            return
        mod = world.model('model_new/test/010.gim', world.get_active_scene())
        mod.scale = math3d.vector(6, 6, 1)
        mod.position = math3d.vector(-15, 5, 0)
        mod.rotation_matrix = math3d.matrix.make_orient(math3d.vector(0, 0, -1), math3d.vector(0, 1, 0))
        mod.all_materials.set_texture(_HASH_TEX0, 'Tex0', self.merge_tex)
        mod = world.model('model_new/test/010.gim', world.get_active_scene())
        mod.scale = math3d.vector(6, 6, 1)
        mod.position = math3d.vector(15, 5, 0)
        mod.rotation_matrix = math3d.matrix.make_orient(math3d.vector(0, 0, -1), math3d.vector(0, 1, 0))
        mod.all_materials.set_texture(_HASH_TEX0, 'Tex0', self.preview_tex)
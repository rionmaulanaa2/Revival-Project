# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/ar/MechaARMainUI1.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
import os
import world
import render
import math3d
import game3d
from cocosui import cc
try:
    import ar
except:
    pass

from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
import common.utils.timer as timer
from common.framework import Functor
from logic.gutils.template_utils import init_common_choose_list
import copy
import time
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
import logic.gutils.dress_utils as dress_utils
from common.utils.redpoint_check_func import check_mecha_component_page_has_empty_slot, check_inscription_module_red_point
from logic.gutils import red_point_utils
import common.utils.cocos_utils as cocos_utils
from common.const.uiconst import UI_VKB_CLOSE
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data, load_model_decal_high_quality
import math
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mecha_skin_utils
import logic.gutils.role_head_utils as role_head_utils
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const import scene_const
from common.utilities import color_int
from ext_package.ext_decorator import has_skin_ext
from logic.manager_agents.manager_decorators import sync_exec
AR_TO_GAME_SCALE = 65
SHADER_VS = 'common/shader/cocosui/positiontexturecolor_nomvp.vs'
SHADER_PS_IOS = 'common/shader/cocosui/positiontexturecolor_nomvp_y_cbcr.ps'
SHADER_PS_ANDROID = 'common/shader/cocosui/positiontexturecolor_nomvp_yuv.ps'
PROGRAM_KEY = 'ar'
PROGRAM_KEY_ADD = 'ar_add'
APPKEY = 'AR0-84582cc5d96718ad31f3035ae4f1ba5af8daf4e94a9ee244bc86afc29945dcdc5ee0efcce8f4de98'
SECRET = '492beb1802c685111aeccd1592064d0ef9c38d4fb7cde4fc4d2cfbeae730d9cfb09c39a5e96f6e07'
TEST_PLATFORM = game3d.PLATFORM_WIN32
if game3d.get_platform() == game3d.PLATFORM_ANDROID:
    CONFIG = 'ar_scenes/0501/config'
    ASSETS = 'ar_scenes/0501/assets'
else:
    CONFIG = 'ar_scenes/0501_30fps/config'
    ASSETS = 'ar_scenes/0501_30fps/assets'
RT_WIDTH = 1280
RT_HEIGHT = 720
MAX_DIRECT_INTENSITY = 10
MAX_INDIRECT_INTENSITY = 10
MAX_ROTATE_RADIAN = math.pi * 2
MODEL_PATH = 'character/11/2000/l.gim'
BACKGROUND_UI_PATH = 'gui/ui_res_2/ar/bg.png'
BACKGROUND_MODEL_PATH = 'model_new/others/screen_effect/postprocess_mesh/ar_background.gim'
MAP_PATH = 'ar_map'
CHECK_FILE_DICT = {'assets/device_android_calib.json': 'assets/device_Android_calib.json',
   'assets/device_ios_calib.json': 'assets/device_iOS_calib.json',
   'assets/voc_orb1.yaml': '',
   'assets/voc_orb2.yaml': '',
   'config/config.json': ''
   }
EXCEPT_HIDE_UI_LIST = []
MAX_MECHA_NUM = 3
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
_HASH_light_info = game3d.calc_string_hash('light_info')
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
MAX_TRY_PERMISSION_TIMES = 5
SHOW_ACTION_DETAIL = 0
HIDE_ACTION_DETAIL = 1
FULL_SCREEN_WIDTH_HEIGHT_SCALE = 1.35
IGNORE_MECHA_IDS = [8023]
LIGHT_NAME = 'dir_light'

class MechaARMainUI1(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_ar'
    IS_FULLSCREEN = False
    MODEL_SCALE_TOUCH_SEN_FACTOR = 5000
    UI_VKB_TYPE = UI_VKB_CLOSE
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    BG_CONFIG_NAME = 'mech_display/bg_mech_ar1'
    UI_ACTION_EVENT = {'btn_scene_ui.OnDrag': '_on_btn_scene_ui_drag',
       'btn_scene_ui.OnEnd': '_on_btn_scene_ui_drag_end',
       'temp_btn_back.btn_back.OnClick': '_on_click_btn_back',
       'btn_hide.OnClick': 'on_click_hide',
       'btn_set.OnClick': 'on_click_set',
       'btn_choose.OnClick': 'on_click_set_shadow_visible',
       'btn_action_1.OnClick': 'on_click_action1',
       'btn_action_2.OnClick': 'on_click_action2',
       'btn_action_3.OnClick': 'on_click_action3',
       'temp__mecha_1.btn_choose.OnClick': 'on_click_choose_mecha1',
       'temp__mecha_2.btn_choose.OnClick': 'on_click_choose_mecha2',
       'temp__mecha_3.btn_choose.OnClick': 'on_click_choose_mecha3',
       'temp__mecha_1.btn_delete.OnClick': 'on_click_delete_mecha1',
       'temp__mecha_2.btn_delete.OnClick': 'on_click_delete_mecha2',
       'temp__mecha_3.btn_delete.OnClick': 'on_click_delete_mecha3',
       'temp_btn_replace.btn_common.OnClick': 'on_click_replace',
       'btn_chose_mode.OnClick': 'on_click_choose_mecha',
       'nd_screen_shot.btn_screen.OnClick': 'on_click_screen',
       'img_act_panel.btn_back.OnClick': 'on_click_shrink_action_list',
       'img_act_panel.btn_show.OnClick': 'on_click_unfold_action_list'
       }

    def test_draw_model1(self):
        if game3d.get_platform() != TEST_PLATFORM:
            return
        else:
            self.log('test--test_draw_model1--step1')
            import traceback
            traceback.print_stack()
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
            self.panel.nd_screen_shot.setVisible(True)
            self.panel.btn_set.setVisible(True)
            active_scene = self.scene
            old_camera = active_scene.active_camera
            camera_arg = {'aspect': old_camera.aspect,'fov': old_camera.fov,'z_range': old_camera.z_range,'transformation': old_camera.transformation,'projection_matrix': old_camera.projection_matrix,'look_at': old_camera.look_at}
            part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
            model_list = part_md.get_cur_model_list()
            ref_model = model_list[0].get_model()
            self.log(ref_model.cur_anim_name)
            ref_pos = ref_model.position
            ref_scale = ref_model.scale
            ref_world_rotation_matrix = ref_model.world_rotation_matrix
            ref_pos.x = ref_pos.x - 10
            anim_name = ref_model.cur_anim_name
            self.switch_scene()
            camera = self.scene.active_camera
            camera.aspect = camera_arg['aspect']
            camera.fov = camera_arg['fov']
            camera.z_range = camera_arg['z_range']
            camera.transformation = camera_arg['transformation']
            camera.projection_matrix = camera_arg['projection_matrix']
            camera.look_at = camera_arg['look_at']
            size = game3d.get_window_size()
            self.log('test--test_draw_model1--step2--size =', size)
            self.rt_width = size[0]
            self.rt_height = size[1]
            active_scene = world.get_active_scene()
            old_camera = active_scene.active_camera
            path = 'gui/ui_res_2/ar/ar_screen.jpg'
            background_model = world.model(BACKGROUND_MODEL_PATH, self.scene)
            background_model.all_materials.set_technique(1, 'shader/g93shader/rgb.nfx::TShader')
            background_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', path)
            background_model.all_materials.rebuild_tech()
            background_model.remove_from_parent()
            background_model.set_parent(self.scene.active_camera)
            self.log('test--test_draw_model1--step3--scene =', self.scene, '--BACKGROUND_MODEL_PATH =', BACKGROUND_MODEL_PATH)
            self.init_event()
            self.init_light_slider_value()
            self.hit_model_list = []
            self.shadow_model_list = []
            self._load_lod_mesh_task_dict = {}
            self._enter_display_sfx_list = []
            mecha_id, skin_id, shiny_weapon_id = self._default_mecha_info
            self._mecha_info_list[0] = self._default_mecha_info
            model_path = dress_utils.get_mecha_model_path(mecha_id, skin_id)
            submesh_path = dress_utils.get_mecha_model_h_path(mecha_id, skin_id)
            sub_mesh_path_list = [
             submesh_path]
            item_no = dress_utils.get_mecha_skin_item_no(mecha_id, skin_id)
            hit_model = world.model(model_path, self.scene)
            self.log('test--test_draw_model1--step4--scene =', self.scene)
            self.hit_model_list.append(hit_model)
            for res_path in sub_mesh_path_list:
                global_data.model_mgr.create_mesh_async(None, res_path, hit_model)

            hit_model.position = ref_pos
            hit_model.scale = ref_scale
            hit_model.world_rotation_matrix = ref_world_rotation_matrix
            self.log('test--test_draw_model1--step1--model_path =', model_path, '--sub_mesh_path_list =', sub_mesh_path_list, '--scene =', self.scene)
            mecha_skin_utils.load_skin_model_and_effect_for_ar(hit_model, skin_id, shiny_weapon_id)
            mecha_skin_utils.register_socket_res_auto_refresh(hit_model, skin_id)
            hit_model.all_materials.enable_write_alpha = True
            hit_model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 1.0)
            self.play_show_anim(hit_model, mecha_id)
            decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(item_no)), [])
            color_dict = global_data.player.get_mecha_color().get(str(item_no), {})
            decal_lod = 0
            if decal_list:
                self.load_decal_data(hit_model, item_no, decal_list, decal_lod=decal_lod)
            if color_dict:
                self.load_color_data(hit_model, item_no, color_dict)
            hit_model.play_animation(anim_name)
            self.log('test--test_draw_model1--step1--ref_scale =', ref_scale, '--model_path =', model_path, '--submesh_path =', submesh_path)
            return

    def test_draw_model(self):
        if game3d.get_platform() != TEST_PLATFORM:
            return
        else:
            self.test_draw_model1()
            return
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
            self.panel.nd_screen_shot.setVisible(True)
            self.panel.btn_set.setVisible(True)
            part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
            model_list = part_md.get_cur_model_list()
            ref_model = model_list[0].get_model()
            self.log(ref_model.cur_anim_name)
            ref_pos = ref_model.position
            ref_scale = ref_model.scale
            ref_world_rotation_matrix = ref_model.world_rotation_matrix
            ref_pos.x = ref_pos.x - 10
            anim_name = ref_model.cur_anim_name
            active_scene = world.get_active_scene()
            old_camera = active_scene.active_camera
            camera_arg = {'aspect': old_camera.aspect,'fov': old_camera.fov,'z_range': old_camera.z_range,'transformation': old_camera.transformation,'projection_matrix': old_camera.projection_matrix,'look_at': old_camera.look_at}
            self.switch_scene()
            camera = self.scene.active_camera
            camera.aspect = camera_arg['aspect']
            camera.fov = camera_arg['fov']
            camera.z_range = camera_arg['z_range']
            camera.transformation = camera_arg['transformation']
            camera.projection_matrix = camera_arg['projection_matrix']
            camera.look_at = camera_arg['look_at']
            self.hit_model_list = []
            self.shadow_model_list = []
            self._load_lod_mesh_task_dict = {}
            self._enter_display_sfx_list = []
            mecha_id, skin_id, shiny_weapon_id = self._default_mecha_info
            self._mecha_info_list[0] = self._default_mecha_info
            model_path = dress_utils.get_mecha_model_path(mecha_id, skin_id)
            submesh_path = dress_utils.get_mecha_model_h_path(mecha_id, skin_id)
            sub_mesh_path_list = [
             submesh_path]
            item_no = dress_utils.get_mecha_skin_item_no(mecha_id, skin_id)
            hit_model = world.model(model_path, self.scene)
            self.hit_model_list.append(hit_model)
            for res_path in sub_mesh_path_list:
                global_data.model_mgr.create_mesh_async(None, res_path, hit_model)

            hit_model.position = ref_pos
            hit_model.scale = ref_scale
            hit_model.world_rotation_matrix = ref_world_rotation_matrix
            self.log('test--test_draw_model--step1--model_path =', model_path, '--sub_mesh_path_list =', sub_mesh_path_list, '--scene =', self.scene)
            mecha_skin_utils.load_skin_model_and_effect_for_ar(hit_model, skin_id, shiny_weapon_id)
            mecha_skin_utils.register_socket_res_auto_refresh(hit_model, skin_id)
            hit_model.all_materials.enable_write_alpha = True
            hit_model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 1.0)
            self.play_show_anim(hit_model, mecha_id)
            decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(item_no)), [])
            color_dict = global_data.player.get_mecha_color().get(str(item_no), {})
            decal_lod = 0
            if decal_list:
                self.load_decal_data(hit_model, item_no, decal_list, decal_lod=decal_lod)
            if color_dict:
                self.load_color_data(hit_model, item_no, color_dict)
            active_scene = world.get_active_scene()
            old_camera = active_scene.active_camera
            self.init_event()
            self.init_light_slider_value()
            hit_model.play_animation(anim_name)
            self.log('test--test_draw_model--step1--ref_scale =', ref_scale, '--model_path =', model_path, '--submesh_path =', submesh_path)
            return

    def test_error_sfx(self):
        sfx_path = 'effect/fx/mecha/8012/8012_ar.sfx'
        model = self.hit_model_list[0]
        socket = 'fx_penhuokou_ar'
        self.log('test--test_error_sfx--step1--len(hit_model_list)', len(self.hit_model_list))
        self.log('test--test_error_sfx--step2--sfx_path =', sfx_path, '--socket =', socket, '--model.filename =', model.filename)
        global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket, duration=0, on_create_func=self.create_error_display_sfx_callback)

    def init_light_slider_value(self):
        conf = confmgr.get('c_env_config', 'light', 'ar_mecha', 'on_ground')
        toon_indirect_intensity = 1
        if conf:
            toon_indirect_intensity = conf['ToonIndirectIntensity']
        light_item_1 = self.panel.pnl_up.temp_up.GetItem(0)
        percent = toon_indirect_intensity / MAX_INDIRECT_INTENSITY
        percent = min(percent, 1)
        percent = max(percent, 0)
        light_item_1.slider.setPercent(percent * 100)
        active_scene = world.get_active_scene()
        light = self.scene.get_light(LIGHT_NAME)
        light_item_2 = self.panel.pnl_up.temp_up_2.GetItem(0)
        percent = light.intensity / MAX_DIRECT_INTENSITY
        percent = min(percent, 1)
        percent = max(percent, 0)
        light_item_2.slider.setPercent(percent * 100)
        light_item_3 = self.panel.pnl_mid.temp_mid_level.GetItem(0)
        rotation_matrix = light.world_rotation_matrix
        yaw = math.fmod(rotation_matrix.yaw, MAX_ROTATE_RADIAN)
        if yaw < 0:
            yaw += MAX_ROTATE_RADIAN
        percent = yaw / MAX_ROTATE_RADIAN
        percent = min(percent, 1)
        percent = max(percent, 0)
        light_item_3.slider.setPercent(percent * 100)
        light_item_4 = self.panel.pnl_mid.temp_mid_vertical.GetItem(0)
        pitch = math.fmod(rotation_matrix.pitch, MAX_ROTATE_RADIAN)
        if pitch < 0:
            pitch += MAX_ROTATE_RADIAN
        self.log('test--init_light_slider_value--step1--yaw =', yaw, '--pitch =', pitch)
        percent = pitch / MAX_ROTATE_RADIAN
        percent = min(percent, 1)
        percent = max(percent, 0)
        light_item_4.slider.setPercent(percent * 100)

    def create_error_display_sfx_callback(self, sfx, *args):
        print(('test--create_error_display_sfx_callback--sfx.filename =', sfx.filename))

    def test_camera(self, position=None, scale=None, anim_name=None):
        part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
        model_list = part_md.get_cur_model_list()
        ref_model = model_list[0].get_model()
        self.log(ref_model.cur_anim_name)
        ref_pos = ref_model.position
        ref_scale = ref_model.scale
        ref_world_rotation_matrix = ref_model.world_rotation_matrix
        if position:
            if isinstance(position, (tuple, list)):
                position = math3d.vector(*position)
            ref_pos = position
        if scale:
            ref_scale = math3d.vector(scale, scale, scale)
        hit_model = self.hit_model_list[0]
        hit_model.position = ref_pos
        hit_model.scale = ref_scale
        hit_model.world_rotation_matrix = ref_world_rotation_matrix
        self.log('test--test_camera--step1--ref_pos =', ref_pos, '--ref_scale =', ref_scale, '--ref_model.scale =', ref_model.scale)
        mecha_skin_utils.clear_specific_skin_anim_model_and_effect(hit_model, hit_model.cur_anim_name)
        mecha_skin_utils.check_exit_anim_refresh_socket_res_appearance(hit_model, hit_model.cur_anim_name, directly_refresh=True)
        if anim_name:
            hit_model.play_animation(anim_name)
            mecha_skin_utils.check_enter_anim_refresh_socket_res_appearance(hit_model, anim_name, directly_refresh=True)

    def on_finish_load_scene(self, *args):
        if not self.is_valid():
            return
        self.log('test--on_finish_load_scene--step1')
        self.scene.enable_tonemap(False)
        self.scene.enable_vlm = True
        self.load_env_new_sync()

    @sync_exec
    def load_env_new_sync(self):
        self.scene.load_env_new('scene/scene_env_confs/default_nx2_mobile.xml')
        self.apply_conf('ar_mecha')

    def apply_conf(self, conf_name):
        scene = self.scene
        if not scene:
            return
        else:
            conf = confmgr.get('c_env_config', 'light', conf_name, 'on_ground')
            if not conf:
                return
            light = self.scene.get_light(LIGHT_NAME)
            if light:
                light.intensity = conf['MainLightIntensity']
                light.diffuse = color_int(*conf['MainLightColor'])
            if global_data.is_ue_model:
                if getattr(scene, 'set_sky_light', None):
                    scene.set_sky_light(*[ int(x) for x in conf['SkyLightColor'] ])
                if getattr(scene, 'set_sky_light_intensity', None):
                    scene.set_sky_light_intensity(float(conf['SkyLightIntensity']))
                if getattr(scene, 'set_second_dir_light_enable', None):
                    scene.set_second_dir_light_enable(float(conf['SecondDirLightEnable']))
                    scene.set_second_dir_light_dir(*[ float(x) for x in conf['SecondDirLightDir'][:-1] ])
                    scene.set_second_dir_light_color(*[ float(x / 255) for x in conf['SecondDirLightColor'] ])
                    scene.set_second_dir_light_intensity(float(conf['SecondDirLightIntensity']))
                scene.ambient_color = color_int(*conf['Ambient'])
                skip_set = set(('MainLightIntensity', 'Ambient', 'MainLightColor',
                                'SkyLightColor', 'SkyLightIntensity', 'SecondDirLightEnable',
                                'SecondDirLightDir', 'SecondDirLightColor', 'SecondDirLightIntensity'))
                for k, v in six.iteritems(conf):
                    if k in skip_set:
                        continue
                    if isinstance(v, list):
                        v = color_int(*v)
                    scene.set_global_uniform(k, v)

            return

    def switch_scene(self):
        active_scene = world.get_active_scene()
        src_light = active_scene.get_light(LIGHT_NAME)
        self.log('test--on_init_panel--step1--old_scene =', self.scene, '--src_light =', src_light)
        world_rotation_matrix = src_light.world_rotation_matrix
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_AR, finish_callback=self.on_finish_load_scene)
        dest_light = self.scene.get_light(LIGHT_NAME)
        dest_light.world_rotation_matrix = world_rotation_matrix
        self.log('test--switch_scene--step2--new_scene =', self.scene, '--dest_light =', dest_light)

    def on_init_panel(self, *args, **kargs):
        if game3d.get_platform() != TEST_PLATFORM:
            self.switch_scene()
        from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
        self._screen_capture_helper = ScreenFrameHelper()
        self._ar_timer_id = None
        self._check_permission_timer_id = None
        self._is_shadow_visible = True
        self._check_permission_times = 0
        self._plane_visible_timer_id = None
        self._is_any_plane_visible = False
        self.session = None
        self._load_lod_mesh_task_dict = {}
        self.action_conf = copy.deepcopy(confmgr.get('skin_define_action'))
        self.no_action_tag = True
        self.on_frame_cb_log = 0
        self.on_anchor_added_cb_log = 1
        self.on_anchor_updated_cb_log = 0
        self.start_time = time.time()
        self.panel.lab_place.SetString(609389)
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self._double_touch_prev_len = 0.0
        self._default_mecha_info = None
        self._mecha_drag_pos_list = [ None for index in range(MAX_MECHA_NUM) ]
        self._mecha_info_list = [ None for index in range(MAX_MECHA_NUM) ]
        self.hit_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        self.shadow_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        self.cur_euler_rot_list = [ math3d.vector(0, 0, 0) for index in range(MAX_MECHA_NUM) ]
        self.target_euler_rot_list = [ math3d.vector(0, 0, 0) for index in range(MAX_MECHA_NUM) ]
        self._cur_scale_list = [ 1 for index in range(MAX_MECHA_NUM) ]
        self._min_scale_list = [ 1 for index in range(MAX_MECHA_NUM) ]
        self._max_scale_list = [ 1 for index in range(MAX_MECHA_NUM) ]
        self._select_model_index = -1
        self._all_mecha_lst = []
        self._open_mecha_lst = [8001]
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._enter_display_sfx_list = []
        self._show_choose_mecha_list = False
        self._all_light = []
        self._is_drag_model = False
        self._show_action_detail_type = SHOW_ACTION_DETAIL
        self.background_model = None
        self.rotateMode = None
        self.panel.btn_chose_mode.SetText(609391)
        self.hide_main_ui()
        self.init_event()
        self.init_touch_event()
        if game3d.get_platform() == TEST_PLATFORM:
            self._ar_timer_id = global_data.game_mgr.register_logic_timer(self.update, interval=1, times=-1, mode=timer.LOGIC)
            return
        else:
            self.setup()
            self.init_open_lst()
            self.panel.temp_scene.PlayAnimation('show')
            return

    def init_touch_event(self):
        layer = self.get_layer()
        layer.BindMethod('OnClick', self.on_click_base_layer)
        layer.BindMethod('OnBegin', self._on_rotate_drag_begin)
        layer.BindMethod('OnDrag', self._on_rotate_drag)
        layer.BindMethod('OnEnd', self._on_rotate_drag_end)

        @self.panel.nd_slider.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent()
            percent = val / 100.0
            self.log('test--OnPercentageChanged--val =', val, '--slider =', slider)
            self.one_model_percent_change(percent)

        self.panel.pnl_up.temp_up.SetInitCount(1)
        self.panel.pnl_up.temp_up_2.SetInitCount(1)
        self.panel.pnl_mid.temp_mid_level.SetInitCount(1)
        self.panel.pnl_mid.temp_mid_vertical.SetInitCount(1)
        light_item_1 = self.panel.pnl_up.temp_up.GetItem(0)

        @light_item_1.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent()
            percent = val / 100.0
            self.on_indirect_light_intensity_percent_change(percent)

        @light_item_1.minute.unique_callback()
        def OnClick(btn, touch):
            val = light_item_1.slider.getPercent()
            if val <= 0:
                return
            val -= 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_1.slider.setPercent(val)
            percent = val / 100.0
            self.on_indirect_light_intensity_percent_change(percent)

        @light_item_1.plus.unique_callback()
        def OnClick(btn, touch):
            val = light_item_1.slider.getPercent()
            if val >= 100:
                return
            val += 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_1.slider.setPercent(val)
            percent = val / 100.0
            self.on_indirect_light_intensity_percent_change(percent)

        light_item_2 = self.panel.pnl_up.temp_up_2.GetItem(0)

        @light_item_2.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent()
            percent = val / 100.0
            self.on_direct_light_intensity_percent_change(percent)

        @light_item_2.minute.unique_callback()
        def OnClick(btn, touch):
            val = light_item_2.slider.getPercent()
            if val <= 0:
                return
            val -= 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_2.slider.setPercent(val)
            percent = val / 100.0
            self.on_direct_light_intensity_percent_change(percent)

        @light_item_2.plus.unique_callback()
        def OnClick(btn, touch):
            val = light_item_2.slider.getPercent()
            if val >= 100:
                return
            val += 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_2.slider.setPercent(val)
            percent = val / 100.0
            self.on_direct_light_intensity_percent_change(percent)

        light_item_3 = self.panel.pnl_mid.temp_mid_level.GetItem(0)

        @light_item_3.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent()
            percent = val / 100.0
            self.on_light_rotate_y_percent_change(percent)

        @light_item_3.minute.unique_callback()
        def OnClick(btn, touch):
            val = light_item_3.slider.getPercent()
            if val <= 0:
                return
            val -= 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_3.slider.setPercent(val)
            percent = val / 100.0
            self.on_light_rotate_y_percent_change(percent)

        @light_item_3.plus.unique_callback()
        def OnClick(btn, touch):
            val = light_item_3.slider.getPercent()
            if val >= 100:
                return
            val += 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_3.slider.setPercent(val)
            percent = val / 100.0
            self.on_light_rotate_y_percent_change(percent)

        light_item_4 = self.panel.pnl_mid.temp_mid_vertical.GetItem(0)

        @light_item_4.slider.unique_callback()
        def OnPercentageChanged(ctrl, slider):
            val = slider.getPercent()
            percent = val / 100.0
            self.on_light_rotate_x_percent_change(percent)

        @light_item_4.minute.unique_callback()
        def OnClick(btn, touch):
            val = light_item_4.slider.getPercent()
            if val <= 0:
                return
            val -= 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_4.slider.setPercent(val)
            percent = val / 100.0
            self.on_light_rotate_x_percent_change(percent)

        @light_item_4.plus.unique_callback()
        def OnClick(btn, touch):
            val = light_item_4.slider.getPercent()
            if val >= 100:
                return
            val += 1
            val = min(val, 100)
            val = max(val, 0)
            light_item_4.slider.setPercent(val)
            percent = val / 100.0
            self.on_light_rotate_x_percent_change(percent)

    def get_layer(self):
        return self.get_bg_panel().panel.layer

    def on_finalize_panel(self):
        self.log('test--MechaARMainUI1.on_finalize_panel--step1')
        self.scene.enable_tonemap(True)
        self.process_event(False)
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        self._mecha_conf = None
        if self._ar_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._ar_timer_id)
            self._ar_timer_id = None
        if self._check_permission_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._check_permission_timer_id)
            self._check_permission_timer_id = None
        self._check_permission_times = 0
        if self._plane_visible_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._plane_visible_timer_id)
            self._plane_visible_timer_id = None
        self.log('test--MechaARMainUI1.on_finalize_panel--step2--session =', self.session)
        if self.session is not None:
            self.stop_ar()
        self.clear_model()
        self.clear_enter_display_sfx()
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        self.log('test--MechaARMainUI1.on_finalize_panel--step4')
        return

    def init_open_lst(self):
        if not global_data.player:
            self.close()
            return
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            self._open_mecha_lst = []
            self._all_mecha_lst = []
            for mecha_id in mecha_open_info['opened_order']:
                if mecha_id in IGNORE_MECHA_IDS:
                    continue
                self._all_mecha_lst.append(mecha_id)
                if global_data.player.has_item_by_no(battle_id_to_mecha_lobby_id(mecha_id)):
                    self._open_mecha_lst.append(mecha_id)

        self._all_mecha_lst = sorted(self._all_mecha_lst, key=lambda x: (x not in self._open_mecha_lst, x))

    def clear_enter_display_sfx(self):
        for sfx in self._enter_display_sfx_list:
            global_data.sfx_mgr.remove_sfx(sfx)

        self._enter_display_sfx_list = []

    def get_mecha_select_effect_id(self, mecha_id):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
        mecha_item = global_data.player.get_item_by_no(mecha_item_id)
        select_sfx = None
        if mecha_item:
            select_sfx = mecha_item.get_sfx()
        mecha_effect_id = select_sfx or six_ex.keys(conf)[0]
        return mecha_effect_id

    def get_main_and_sub_model(self, model):
        model_file_list = []
        model_file_list.append(model.filename)
        mesh_count = model.get_submesh_count()
        if hasattr(model, 'get_submesh_filename'):
            for mesh_idx in range(0, mesh_count):
                file_name = model.get_submesh_filename(mesh_idx)
                mesh_name = model.get_submesh_name(mesh_idx)
                model_file_list.append((mesh_name, file_name))

        return model_file_list

    def init_action_list(self, model_index):
        mecha_id, skin_id, shiny_weapon_id = self._mecha_info_list[model_index]
        ar_item_config = confmgr.get('lobby_model_display_conf', 'ArDisplayAnim', 'Content', str(mecha_id), default={})
        action_list = []
        for index in range(1, 10):
            key = 'anim_' + str(index)
            one_config = ar_item_config.get(key, None)
            self.log('test--init_action_list--step1--index =', index, '--key =', key, '--one_config =', one_config)
            if not one_config:
                continue
            action_list.append(one_config)

        self.log('test--init_action_list--step2--mecha_id =', mecha_id, '--len(action_list) =', len(action_list), '--action_list =', action_list, '--ar_item_config =', ar_item_config)
        if not action_list:
            print(('[Error] test--ArDisplayAnim table not config--mecha_id =', mecha_id))
            import traceback
            traceback.print_stack()
            return
        else:
            self.no_action_tag = False
            action_option = [ {'anim': action[0],'name': action[1],'is_play_last_frame': index < 3} for index, action in enumerate(action_list) ]
            for index in range(1, 3):
                key = 'pos_' + str(index)
                one_config = ar_item_config.get(key, None)
                if not one_config:
                    continue
                goods_id, name_id = one_config
                is_have_item = global_data.player.has_item_by_no(goods_id)
                anim_name = confmgr.get('lobby_item', str(goods_id), 'res')
                one_action_option = {'anim': anim_name,'name': name_id,'is_play_last_frame': False,'is_have_item': is_have_item}
                self.log('test--init_action_list--step3--index =', index, '--is_have_item =', is_have_item, '--key =', key, '--one_config =', one_config)
                if not is_have_item:
                    one_action_option['icon'] = 'gui/ui_res_2/mech_display/icon_ar_lock.png'
                action_option.append(one_action_option)

            call_anim = ar_item_config['call_anim']

            def call_back--- This code section failed: ---

 865       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'hit_model_list'
           6  LOAD_DEREF            1  'model_index'
           9  BINARY_SUBSCR    
          10  STORE_FAST            1  'model'

 866      13  LOAD_FAST             1  'model'
          16  POP_JUMP_IF_TRUE     23  'to 23'

 867      19  LOAD_CONST            0  ''
          22  RETURN_END_IF    
        23_0  COME_FROM                '16'

 869      23  LOAD_FAST             1  'model'
          26  LOAD_ATTR             1  'cur_anim_name'
          29  LOAD_DEREF            2  'call_anim'
          32  COMPARE_OP            2  '=='
          35  POP_JUMP_IF_FALSE    80  'to 80'
          38  LOAD_FAST             1  'model'
          41  LOAD_ATTR             2  'is_anim_at_end'
          44  UNARY_NOT        
        45_0  COME_FROM                '35'
          45  POP_JUMP_IF_FALSE    80  'to 80'

 870      48  LOAD_DEREF            0  'self'
          51  LOAD_ATTR             3  'log'
          54  LOAD_CONST            1  'test--call_back--step1--index ='
          57  LOAD_CONST            2  '--cur_anim_name ='
          60  LOAD_DEREF            2  'call_anim'
          63  LOAD_CONST            3  '--is_anim_at_end ='
          66  LOAD_FAST             1  'model'
          69  LOAD_ATTR             2  'is_anim_at_end'
          72  CALL_FUNCTION_6       6 
          75  POP_TOP          

 871      76  LOAD_CONST            0  ''
          79  RETURN_END_IF    
        80_0  COME_FROM                '45'

 873      80  LOAD_DEREF            0  'self'
          83  LOAD_ATTR             3  'log'
          86  LOAD_CONST            4  'test--call_back--step2--index ='
          89  LOAD_CONST            2  '--cur_anim_name ='
          92  LOAD_DEREF            2  'call_anim'
          95  LOAD_CONST            3  '--is_anim_at_end ='
          98  LOAD_FAST             1  'model'
         101  LOAD_ATTR             2  'is_anim_at_end'
         104  CALL_FUNCTION_6       6 
         107  POP_TOP          

 874     108  LOAD_DEREF            3  'action_option'
         111  LOAD_FAST             0  'index'
         114  BINARY_SUBSCR    
         115  STORE_FAST            2  'action'

 875     118  LOAD_FAST             2  'action'
         121  LOAD_ATTR             4  'get'
         124  LOAD_CONST            5  'is_have_item'
         127  LOAD_GLOBAL           5  'True'
         130  CALL_FUNCTION_2       2 
         133  STORE_FAST            3  'is_have_item'

 876     136  LOAD_DEREF            0  'self'
         139  LOAD_ATTR             3  'log'
         142  LOAD_CONST            6  'test--call_back--step4--index ='
         145  LOAD_CONST            7  '--is_have_item ='
         148  LOAD_FAST             3  'is_have_item'
         151  LOAD_CONST            8  '--action ='
         154  LOAD_FAST             2  'action'
         157  LOAD_CONST            2  '--cur_anim_name ='
         160  LOAD_DEREF            2  'call_anim'
         163  LOAD_CONST            3  '--is_anim_at_end ='
         166  LOAD_FAST             1  'model'
         169  LOAD_ATTR             2  'is_anim_at_end'
         172  CALL_FUNCTION_10     10 
         175  POP_TOP          

 877     176  LOAD_FAST             3  'is_have_item'
         179  POP_JUMP_IF_TRUE    208  'to 208'

 878     182  LOAD_GLOBAL           6  'global_data'
         185  LOAD_ATTR             7  'game_mgr'
         188  LOAD_ATTR             8  'show_tip'
         191  LOAD_GLOBAL           9  'get_text_by_id'
         194  LOAD_CONST            9  906652
         197  CALL_FUNCTION_1       1 
         200  CALL_FUNCTION_1       1 
         203  POP_TOP          

 879     204  LOAD_CONST            0  ''
         207  RETURN_END_IF    
       208_0  COME_FROM                '179'

 881     208  LOAD_FAST             2  'action'
         211  LOAD_CONST           10  'anim'
         214  BINARY_SUBSCR    
         215  STORE_FAST            4  'anim'

 883     218  LOAD_FAST             2  'action'
         221  LOAD_CONST           11  'is_play_last_frame'
         224  BINARY_SUBSCR    
         225  STORE_FAST            5  'is_play_last_frame'

 884     228  LOAD_FAST             1  'model'
         231  LOAD_ATTR            10  'get_anim_length'
         234  LOAD_FAST             4  'anim'
         237  CALL_FUNCTION_1       1 
         240  STORE_FAST            6  'anim_time'

 885     243  LOAD_CONST           12  ''
         246  STORE_FAST            7  'init_time'

 886     249  LOAD_GLOBAL          11  'world'
         252  LOAD_ATTR            12  'PLAY_FLAG_LOOP'
         255  STORE_FAST            8  'loop'

 887     258  LOAD_FAST             5  'is_play_last_frame'
         261  POP_JUMP_IF_FALSE   282  'to 282'

 888     264  LOAD_FAST             6  'anim_time'
         267  STORE_FAST            7  'init_time'

 889     270  LOAD_GLOBAL          11  'world'
         273  LOAD_ATTR            13  'PLAY_FLAG_NO_LOOP'
         276  STORE_FAST            8  'loop'
         279  JUMP_FORWARD          0  'to 282'
       282_0  COME_FROM                '279'

 891     282  LOAD_GLOBAL          14  'mecha_skin_utils'
         285  LOAD_ATTR            15  'clear_specific_skin_anim_model_and_effect'
         288  LOAD_FAST             1  'model'
         291  LOAD_FAST             1  'model'
         294  LOAD_ATTR             1  'cur_anim_name'
         297  CALL_FUNCTION_2       2 
         300  POP_TOP          

 892     301  LOAD_GLOBAL          14  'mecha_skin_utils'
         304  LOAD_ATTR            16  'check_exit_anim_refresh_socket_res_appearance'
         307  LOAD_FAST             1  'model'
         310  LOAD_FAST             1  'model'
         313  LOAD_ATTR             1  'cur_anim_name'
         316  LOAD_CONST           13  'directly_refresh'
         319  LOAD_GLOBAL           5  'True'
         322  CALL_FUNCTION_258   258 
         325  POP_TOP          

 894     326  LOAD_DEREF            0  'self'
         329  LOAD_ATTR             3  'log'
         332  LOAD_CONST            4  'test--call_back--step2--index ='
         335  LOAD_CONST           14  '--anim ='
         338  LOAD_FAST             4  'anim'
         341  LOAD_CONST           15  '--model.filename ='
         344  LOAD_FAST             1  'model'
         347  LOAD_ATTR            17  'filename'
         350  CALL_FUNCTION_6       6 
         353  POP_TOP          

 895     354  LOAD_FAST             1  'model'
         357  LOAD_ATTR            18  'play_animation'
         360  LOAD_FAST             4  'anim'
         363  LOAD_CONST           16  -1
         366  LOAD_GLOBAL          11  'world'
         369  LOAD_ATTR            19  'TRANSIT_TYPE_DEFAULT'
         372  LOAD_FAST             7  'init_time'
         375  LOAD_FAST             8  'loop'
         378  CALL_FUNCTION_5       5 
         381  POP_TOP          

 896     382  LOAD_GLOBAL          14  'mecha_skin_utils'
         385  LOAD_ATTR            20  'check_enter_anim_refresh_socket_res_appearance'
         388  LOAD_FAST             1  'model'
         391  LOAD_FAST             4  'anim'
         394  LOAD_CONST           13  'directly_refresh'
         397  LOAD_GLOBAL           5  'True'
         400  CALL_FUNCTION_258   258 
         403  POP_TOP          

 897     404  LOAD_DEREF            0  'self'
         407  LOAD_ATTR            21  'shadow_model_list'
         410  LOAD_DEREF            1  'model_index'
         413  BINARY_SUBSCR    
         414  POP_JUMP_IF_FALSE   455  'to 455'

 898     417  LOAD_DEREF            0  'self'
         420  LOAD_ATTR            21  'shadow_model_list'
         423  LOAD_DEREF            1  'model_index'
         426  BINARY_SUBSCR    
         427  LOAD_ATTR            18  'play_animation'
         430  LOAD_FAST             4  'anim'
         433  LOAD_CONST           16  -1
         436  LOAD_GLOBAL          11  'world'
         439  LOAD_ATTR            19  'TRANSIT_TYPE_DEFAULT'
         442  LOAD_FAST             7  'init_time'
         445  LOAD_FAST             8  'loop'
         448  CALL_FUNCTION_5       5 
         451  POP_TOP          
         452  JUMP_FORWARD          0  'to 455'
       455_0  COME_FROM                '452'

 900     455  LOAD_GLOBAL          22  'getattr'
         458  LOAD_DEREF            0  'self'
         461  LOAD_ATTR            23  'panel'
         464  LOAD_CONST           17  'btn_action_'
         467  LOAD_GLOBAL          24  'str'
         470  LOAD_DEREF            1  'model_index'
         473  LOAD_CONST           18  1
         476  BINARY_ADD       
         477  CALL_FUNCTION_1       1 
         480  BINARY_ADD       
         481  LOAD_CONST            0  ''
         484  CALL_FUNCTION_3       3 
         487  STORE_FAST            9  'btn_action'

 901     490  LOAD_DEREF            0  'self'
         493  LOAD_ATTR             3  'log'
         496  LOAD_CONST           19  'test--call_back--model_index ='
         499  LOAD_DEREF            1  'model_index'
         502  LOAD_CONST           20  '--index ='
         505  LOAD_CONST           14  '--anim ='
         508  LOAD_FAST             4  'anim'
         511  LOAD_CONST           15  '--model.filename ='
         514  LOAD_FAST             1  'model'
         517  LOAD_ATTR            17  'filename'
         520  LOAD_CONST           21  '--model_file_list ='
         523  LOAD_DEREF            0  'self'
         526  LOAD_ATTR            26  'get_main_and_sub_model'
         529  LOAD_FAST             1  'model'
         532  CALL_FUNCTION_1       1 
         535  CALL_FUNCTION_10     10 
         538  POP_TOP          

 902     539  LOAD_FAST             9  'btn_action'
         542  POP_JUMP_IF_FALSE   565  'to 565'

 903     545  LOAD_FAST             9  'btn_action'
         548  LOAD_ATTR            27  'SetText'
         551  LOAD_FAST             2  'action'
         554  LOAD_CONST           22  'name'
         557  BINARY_SUBSCR    
         558  CALL_FUNCTION_1       1 
         561  POP_TOP          
         562  JUMP_FORWARD          0  'to 565'
       565_0  COME_FROM                '562'

 904     565  LOAD_DEREF            0  'self'
         568  LOAD_ATTR             3  'log'
         571  LOAD_CONST           23  'test--call_back--anim ='
         574  LOAD_FAST             4  'anim'
         577  LOAD_CONST           15  '--model.filename ='
         580  LOAD_FAST             1  'model'
         583  LOAD_ATTR            17  'filename'
         586  LOAD_CONST           14  '--anim ='
         589  LOAD_FAST             4  'anim'
         592  CALL_FUNCTION_6       6 
         595  POP_TOP          
         596  LOAD_CONST            0  ''
         599  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_6' instruction at offset 72

            def close_callback():
                self.hide_action_list(model_index)

            action_list_node = getattr(self.panel, 'actione_list_' + str(model_index + 1), None)
            if not action_list_node:
                log_error('test--init_action_list--step1--action_list_node None--model_index =', model_index)
                return
            max_height = None
            if model_index == 2:
                max_height = 191
            self.log('test--init_action_list--model_index =', model_index, '--max_height =', max_height)
            init_common_choose_list(action_list_node, action_option, callback=call_back, max_height=max_height, close_cb=close_callback)
            model = self.hit_model_list[model_index]
            if model:
                loop = world.PLAY_FLAG_NO_LOOP
                init_time = 0
                model.play_animation(call_anim, -1, world.TRANSIT_TYPE_DEFAULT, init_time, loop)
                model.register_anim_key_event(call_anim, 'end', lambda *args: call_back(0))
                if self.shadow_model_list[model_index]:
                    self.shadow_model_list[model_index].play_animation(call_anim, -1, world.TRANSIT_TYPE_DEFAULT, init_time, loop)
            return

    def init_model_data(self, model_info, mecha_id, skin_id, shiny_weapon_id):
        if not has_skin_ext():
            from logic.gutils.dress_utils import get_mecha_default_fashion
            default_skin_id = get_mecha_default_fashion(mecha_id)
            if int(skin_id) != int(default_skin_id):
                skin_id = default_skin_id
                shiny_weapon_id = -1
                global_data.game_mgr.show_tip(344)
        self._default_mecha_info = (
         mecha_id, skin_id, shiny_weapon_id)
        self.test_draw_model()

    def get_mecha_num(self):
        num = 0
        for one_mecha_info in self._mecha_info_list:
            if one_mecha_info:
                num += 1

        return num

    def get_empty_mecha_index(self):
        for index, one_mecha_info in enumerate(self._mecha_info_list):
            if not one_mecha_info:
                return index

        return -1

    def copy_npk_file_to_document_path(self):
        from common.utils.path import copy_res_file_to_document, check_document_file_exist
        all_dirs = [
         'ar_scenes/0501', 'ar_scenes/0502', 'ar_scenes/0501_30fps']
        for dir_path in all_dirs:
            file_path = dir_path + '/config/config.json'
            is_find_file = check_document_file_exist(file_path)
            self.log('test--copy_npk_file_to_document_path--step1--is_find_file =', is_find_file, '--file_path =', file_path)
            if not is_find_file:
                for src_path, dest_path in six_ex.items(CHECK_FILE_DICT):
                    if not dest_path:
                        dest_path = src_path
                    one_src_file_path = dir_path + '/' + src_path
                    one_dest_file_path = dir_path + '/' + dest_path
                    self.log('test--copy_npk_file_to_document_path--step2--one_src_file_path =', one_src_file_path, '--one_dest_file_path =', one_dest_file_path)
                    copy_res_file_to_document(one_src_file_path, one_dest_file_path)

    def setup(self):
        self.log('test--MechaARMainUI1.setup--step1')
        self.copy_npk_file_to_document_path()
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        self.log('GL View Size: %s', view.getVisibleSize())
        designSize = view.getDesignResolutionSize()
        self.plane_dict = {}
        self.model_dict = {}
        self.face_coord = None
        self.session = None
        self.ar_type = None
        self.ar_width = 0
        self.ar_height = 0
        self._ar_timer_id = None
        self.clear_model()
        self.platform = game3d.get_platform()
        rotateMode = game3d.get_rotation()
        if rotateMode == 0:
            self.rotateMode = 1
        elif rotateMode == 90:
            self.rotateMode = 3
        elif rotateMode == 180:
            self.rotateMode = 2
        elif rotateMode == 270:
            self.rotateMode = 4
        else:
            self.rotateMode = 1
        self.is_support = ar.is_support_ar()
        self.log('Check AR Support: %s', self.is_support)
        self.start_config(CONFIG, ASSETS)
        self._ar_timer_id = global_data.game_mgr.register_logic_timer(self.update, interval=1, times=-1, mode=timer.LOGIC)
        return

    def add_model(self, model, pos=math3d.vector(0, 0, 0), rotation_matrix=math3d.matrix(), scale=math3d.vector(1, 1, 1), cast_shadow=True):
        scene = self.scene
        if not scene or not scene.valid:
            return
        model.position = pos
        model.scale = scale
        model.rotation_matrix = rotation_matrix
        model.visible = True
        model.set_enable_normal_update(True)
        model.cast_shadow = cast_shadow
        model.receive_shadow = True
        scene.add_object(model)

    def del_model(self, model):
        scene = self.scene
        if not scene or not scene.valid:
            return
        if not model or not model.valid:
            return
        scene.remove_object(model)
        model.clear_events()
        model.destroy()

    def remove_object(self, obj):
        scene = self.scene
        if not scene or not scene.valid:
            return
        if not obj or not obj.valid:
            return
        scene.remove_object(obj)

    def clear_model(self):
        for index, model in enumerate(self.hit_model_list):
            if not model:
                continue
            mecha_skin_utils.clear_skin_anim_sfx_func_cache(model)
            mecha_skin_utils.clear_skin_model_and_effect(model)
            mecha_skin_utils.unregister_socket_res_auto_refresh(model)
            self.del_model(model)

        self.hit_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        self.sub_model_lists = [ [] for index in range(MAX_MECHA_NUM) ]
        self.sfx_id_maps = [ {} for index in range(MAX_MECHA_NUM) ]
        for model in self.shadow_model_list:
            if not model:
                continue
            self.del_model(model)

        self.shadow_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        for task_handle in six_ex.values(self._load_lod_mesh_task_dict):
            if task_handle:
                task_handle.cancel()

        self._load_lod_mesh_task_dict.clear()
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_plane_visible_event': self.update_plane_visible,
           'ar_test_model_preview_effect_event': self.test_model_preview_effect,
           'ar_test_camera_event': self.test_camera
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_plane_visible(self, visible):
        self.log('test--update_plane_visible--visible =', visible, '--len(plane_dict) =', len(self.plane_dict))
        for plane, edge_point_list in six_ex.values(self.plane_dict):
            plane.visible = visible

    def start_config(self, config_path, asset_path):
        size = game3d.get_window_size()
        self.log('test--start_config--config_path =%s,--asset_path =%s', config_path, asset_path)
        self.log('test--start_config--step1--size =', size)
        self.rt_width = size[0]
        self.rt_height = size[1]
        if self.session is not None:
            self.stop_ar()
        self.init_ar()
        return

    def check_permission_is_allowed_tick(self, *args):
        self.log('test--check_permission_is_allowed_tick--step1')
        if ar.check_and_request_permission():
            self.log('test--check_permission_is_allowed_tick--step2')
            self._check_permission_timer_id = None
            self._check_permission_times = 0
            self.init_ar()
            return timer.RELEASE
        else:
            self.log('test--check_permission_is_allowed_tick--step3--_check_permission_times =', self._check_permission_times)
            if self._check_permission_times >= MAX_TRY_PERMISSION_TIMES:
                self._check_permission_timer_id = None
                self._check_permission_times = 0
                global_data.game_mgr.show_tip(get_text_by_id(609394))
                return timer.RELEASE
            self._check_permission_times += 1
            return

    def check_plane_visible_tick(self, *args):
        self.log('test--check_plane_visible_tick--step1')
        if not self.plane_dict:
            self.log('test--check_plane_visible_tick--step2')
            self._plane_visible_timer_id = None
            return timer.RELEASE
        else:
            if not self.scene or not self.scene.valid:
                self._plane_visible_timer_id = None
                return timer.RELEASE
            camera = self.scene.active_camera
            if not camera:
                self._plane_visible_timer_id = None
                return timer.RELEASE
            is_any_plane_visible = False
            screen_width = global_data.really_window_size[0]
            screen_height = global_data.really_window_size[1]
            for identifier, one_plane_info in six.iteritems(self.plane_dict):
                if is_any_plane_visible:
                    break
                plane, edge_point_list = one_plane_info
                if not plane or not plane.valid:
                    continue
                world_transformation = plane.world_transformation
                for index, one_point in enumerate(edge_point_list):
                    world_position = one_point * world_transformation
                    x, y = camera.world_to_screen(world_position)
                    if x >= 0 and x <= screen_width and y >= 0 and y <= screen_height:
                        self.log('test--check_plane_visible_tick--step3--identifier =', identifier, '--index =', index, '--x =', x, '--screen_width =', screen_width, '--y =', y, '--screen_height =', screen_height)
                        is_any_plane_visible = True
                        break

            self.log('test--check_plane_visible_tick--step4--is_any_plane_visible =', is_any_plane_visible)
            if self._is_any_plane_visible != is_any_plane_visible:
                self._is_any_plane_visible = is_any_plane_visible
                self.log('test--check_plane_visible_tick--step5--is_any_plane_visible =', is_any_plane_visible, '--plane_dict =', self.plane_dict)
                if is_any_plane_visible:
                    self.panel.lab_place.SetString(609385)
                else:
                    self.panel.lab_place.SetString(609389)
            return

    def init_ar(self):
        if not self.is_support:
            return
        if not ar.check_and_request_permission():
            if self._check_permission_timer_id:
                global_data.game_mgr.unregister_logic_timer(self._check_permission_timer_id)
            self._check_permission_timer_id = global_data.game_mgr.register_logic_timer(self.check_permission_is_allowed_tick, interval=1, times=-1, mode=timer.CLOCK)
            return
        self.log('Start ARSession...')
        self.session = ar.ar_session()
        self.log('Register: %s %s', APPKEY, SECRET)
        self.session.register(APPKEY, SECRET)
        self.log('Setup Callbacks...')
        self.session.on_frame_callback = self.on_frame_cb
        self.session.on_error_callback = self.on_error_cb
        self.session.on_anchor_added_callback = self.on_anchor_added_cb
        self.session.on_anchor_updated_callback = self.on_anchor_updated_cb
        self.session.on_anchor_removed_callback = self.on_anchor_removed_cb
        self.session.on_face_callback = self.on_face_cb
        self.session.on_gesture_callback = self.on_gesture_cb
        self.session.on_save_map_callback = self.on_save_map_cb
        self.session.on_load_map_callback = self.on_load_map_cb
        abs_config = os.path.join(game3d.get_doc_dir(), CONFIG)
        abs_assets = os.path.join(game3d.get_doc_dir(), ASSETS)
        self.log('Init ARSession Config Path: %s %s', abs_config, abs_assets)
        self.session.init(abs_config, abs_assets)

    def stop_ar(self):
        self.log('test--stop_ar--step1--******')
        self.session.stop()
        self.session = None
        self.log('Clear Camera Texture & Scene Texture...')
        if self.background_model and self.background_model.valid:
            self.background_model.remove_from_parent()
        self.background_model = None
        self.log('Clear AR Scene...')
        for one_plane_info in six.itervalues(self.plane_dict):
            plane, edge_point_list = one_plane_info
            self.remove_object(plane)

        self.plane_dict.clear()
        self._is_any_plane_visible = False
        for model in six.itervalues(self.model_dict):
            self.del_model(model)

        self.model_dict.clear()
        self.clear_model()
        return

    def is_in_plane(self, world_pos):
        for one_plane_info in six_ex.values(self.plane_dict):
            plane, edge_point_list = one_plane_info
            world_transformation = plane.world_transformation
            plane_position = plane.position
            x_range = [None, None]
            z_range = [None, None]
            for index, one_point in enumerate(edge_point_list):
                world_position = one_point * world_transformation
                if x_range[0] is None:
                    x_range[0] = world_position.x
                else:
                    x_range[0] = min(x_range[0], world_position.x)
                if x_range[1] is None:
                    x_range[1] = world_position.x
                else:
                    x_range[1] = max(x_range[1], world_position.x)
                if z_range[0] is None:
                    z_range[0] = world_position.z
                else:
                    z_range[0] = min(z_range[0], world_position.z)
                if z_range[1] is None:
                    z_range[1] = world_position.z
                else:
                    z_range[1] = max(z_range[1], world_position.z)
                if world_pos.x < x_range[0] or world_pos.x > x_range[1] or world_pos.z < z_range[0] or world_pos.z > z_range[1]:
                    continue
                return True

        return False

    def round_model_pos(self, pos):
        convert_pos = self.get_nearest_plane_point(pos)
        self.log('test--round_model_pos--step1--pos =', pos, '--convert_pos =', convert_pos)
        return convert_pos

    def hit_test(self, x, z, is_select, is_end_touch, neox_x, neox_y):
        if not self.plane_dict:
            self.log('test--hit_test--step1')
            return
        else:
            anchor_data = self.session.get_hit_test_result(x, z)
            self.log('test--hit_test--step1--Get Hit Test Result: (%s,%s) %s', x, z, anchor_data)
            self.log('test--hit_test--step1--Get Hit Test Result: x=', x, '--z =', z, '--anchor_data =', anchor_data, '--len(plane_dict) =', len(self.plane_dict), '--_is_any_plane_visible =', self._is_any_plane_visible, '--_select_model_index =', self._select_model_index)
            if anchor_data is not None:
                self.log('test--hit_test: %s, %s, %s, %s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
                self.log('test--hit_test.rotation: %s', anchor_data.rotation)
                self.log('test--hit_test.center: %s', anchor_data.center)
                self.log('test--hit_test.extent: %s', anchor_data.extent)
                pos = self.get_hittest_pos(anchor_data)
                pos = self.round_model_pos(pos)
                if not pos:
                    self.log('test--hit_test--step2')
                    return
                self.log('test--hit_test--step2--pos =%s', pos)
                self.log('test--hit_test--step3--x= ', x, '--z =', z, '--pos =', pos, '--get_mecha_num =', self.get_mecha_num(), '--_select_model_index =', self._select_model_index)
                if self.get_mecha_num() <= 0:
                    self._mecha_info_list[0] = self._default_mecha_info
                    self.show_model(self._select_model_index)
                self.log('test--hit_test--step1--x =', x, '--z =', z, '--pos =', pos)
                model = self.hit_model_list[self._select_model_index]
                self.log('test--hit_test--step4--_select_model_index =', self._select_model_index, '--model =', model)
                if model:
                    self.hit_model_list[self._select_model_index].position = pos
                    self.auto_scale_model(self._select_model_index)
                else:
                    self._mecha_info_list[self._select_model_index] = None
            elif self._select_model_index > 0:
                self.log('test--hit_test--step5--is_select =', is_select, '--_select_model_index =', self._select_model_index)
                if is_select:
                    self.log('test--hit_test--step4--x =', x, '--z =', z, '--hit_model_list[0].position =', self.hit_model_list[0].position)
                    self.hit_model_list[self._select_model_index].position = self.hit_model_list[0].position
            elif self.get_mecha_num() <= 0 and is_end_touch and self._is_any_plane_visible:
                camera = self.scene.active_camera
                hit_world_pos, view_dir = camera.screen_to_world(neox_x, neox_y)
                nearest_pos = self.round_model_pos(hit_world_pos)
                self.log('test--hit_test--step6--nearest_pos =', nearest_pos, '--_select_model_index =', self._select_model_index)
                if nearest_pos:
                    if self.get_mecha_num() <= 0:
                        self._mecha_info_list[0] = self._default_mecha_info
                    self.show_model(self._select_model_index)
                    model = self.hit_model_list[self._select_model_index]
                    self.log('test--hit_test--step7--_select_model_index =', self._select_model_index, '--model =', model)
                    if model:
                        self.hit_model_list[self._select_model_index].position = nearest_pos
                        self.auto_scale_model(self._select_model_index)
                    else:
                        self._mecha_info_list[self._select_model_index] = None
            return

    def auto_scale_model(self, index):
        return
        model = self.hit_model_list[index]
        self.log('test--auto_scale_model--step0--model =', model)
        if not model or not model.valid:
            return
        camera = self.scene.active_camera
        if not camera:
            return
        MODEL_SCALE_STEP = 0.01
        screen_width = global_data.really_window_size[0]
        screen_height = global_data.really_window_size[1]
        cur_scale = self._cur_scale_list[index]
        init_bounding_box = model.bones_bounding_box
        while cur_scale > 0:
            position = model.world_position
            bounding_box = init_bounding_box * cur_scale
            min_y = position.y
            min_position = position - bounding_box
            min_position.y = min_y
            max_position = position + bounding_box
            min_screen_x, min_screen_y = camera.world_to_screen(min_position)
            is_out_screen = False
            if min_screen_x < 0 or min_screen_x > screen_width or min_screen_y < 0 or min_screen_y > screen_height:
                is_out_screen = True
            max_screen_x = 0
            max_screen_y = 0
            if not is_out_screen:
                max_screen_x, max_screen_y = camera.world_to_screen(max_position)
                if max_screen_x < 0 or max_screen_x > screen_width or max_screen_y < 0 or max_screen_y > screen_height:
                    is_out_screen = True
            if is_out_screen:
                self.log('test--auto_scale_model--step1--cur_scale =', cur_scale, '--bounding_box =', bounding_box)
                cur_scale -= MODEL_SCALE_STEP
                model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)
                continue
            break

        if cur_scale <= 0:
            self.log('test--auto_scale_model--step2--index =', index, '--new_scale =', cur_scale)
            cur_scale = self._cur_scale_list[index]
        self.log('test--auto_scale_model--step3--index =', index, '--new_scale =', cur_scale, '--old_scale =', self._cur_scale_list[index])
        self._cur_scale_list[index] = cur_scale
        model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)

    def get_nearest_plane_point(self, hit_world_pos):
        camera = self.scene.active_camera
        if not camera:
            return
        else:
            screen_width = global_data.really_window_size[0]
            screen_height = global_data.really_window_size[1]
            nearest_pos = None
            nearest_dist_sqr = 0
            bg_layer = self.get_layer()
            ui_center_pos = bg_layer.ConvertToWorldSpacePercentage(50, 50)
            for one_plane_info in six_ex.values(self.plane_dict):
                plane, edge_point_list = one_plane_info
                edge_point_list = list(edge_point_list)
                edge_point_list.append(math3d.vector(0, 0, 0))
                world_transformation = plane.world_transformation
                for index, one_point in enumerate(edge_point_list):
                    world_position = one_point * world_transformation
                    x, y = camera.world_to_screen(world_position)
                    if x >= 0 and x <= screen_width and y >= 0 and y <= screen_height:
                        cx, cy = cocos_utils.neox_pos_to_cocos(x, y)
                        one_ui_pos = ccp(cx, cy)
                        diff_ui_pos = one_ui_pos
                        diff_ui_pos.subtract(ui_center_pos)
                        cur_dist_sqr = diff_ui_pos.getLength()
                        if not nearest_pos or cur_dist_sqr < nearest_dist_sqr:
                            nearest_pos = world_position
                            nearest_dist_sqr = cur_dist_sqr

            return nearest_pos

    def get_camera_model_vertical_dist(self, model):
        camera = self.scene.active_camera
        camera_world_rotation_matrix = camera.world_rotation_matrix
        forward = camera_world_rotation_matrix.forward
        camera_world_position = camera.world_position
        model_world_position = model.world_position
        dist_vec = model_world_position - camera_world_position
        self.log('test--get_camera_model_vertical_dist--forward.length =', forward.length)
        return dist_vec.dot(forward)

    def show_model(self, index):
        mecha_info = self._mecha_info_list[index]
        self.log('test--show_model--index =', index, '--mecha_info =', mecha_info)
        if not mecha_info:
            return
        else:
            mecha_id, skin_id, shiny_weapon_id = self._mecha_info_list[index]
            if not has_skin_ext():
                from logic.gutils.dress_utils import get_mecha_default_fashion
                default_skin_id = get_mecha_default_fashion(mecha_id)
                if int(skin_id) != int(default_skin_id):
                    skin_id = default_skin_id
                    shiny_weapon_id = -1
            model_path = dress_utils.get_mecha_model_path(mecha_id, skin_id)
            submesh_path = dress_utils.get_mecha_model_h_path(mecha_id, skin_id)
            sub_mesh_path_list = [submesh_path]
            item_no = dress_utils.get_mecha_skin_item_no(mecha_id, skin_id)
            self.log('test--show_model--step1--index =', index, '--mecha_id =', mecha_id, '--skin_id =', skin_id, '--model_path =', model_path, '--sub_mesh_path_list =', sub_mesh_path_list)
            if self.hit_model_list[index]:
                res_path = self.hit_model_list[index].filename
                if res_path in self._load_lod_mesh_task_dict:
                    del self._load_lod_mesh_task_dict[res_path]
                self.log('test--show_model--step2--error model--index =', index, '--model =', self.hit_model_list[index], '--model.filename =', self.hit_model_list[index].filename)
                mecha_skin_utils.clear_skin_anim_sfx_func_cache(self.hit_model_list[index])
                mecha_skin_utils.clear_skin_model_and_effect(self.hit_model_list[index])
                mecha_skin_utils.unregister_socket_res_auto_refresh(self.hit_model_list[index])
                self.del_model(self.hit_model_list[index])
                self.hit_model_list[index] = None
            hit_model = world.model(model_path, None)
            self.add_model(hit_model)
            mecha_skin_utils.load_skin_model_and_effect_for_ar(hit_model, skin_id, shiny_weapon_id)
            mecha_skin_utils.register_socket_res_auto_refresh(hit_model, skin_id)
            hit_model.pickable = True
            self.hit_model_list[index] = hit_model
            for res_path in sub_mesh_path_list:
                task_handle = global_data.model_mgr.create_mesh_async(None, res_path, self.hit_model_list[index], Functor(self.on_load_mesh_completed, res_path))
                self._load_lod_mesh_task_dict[res_path] = task_handle

            self.log('test--show_model--step1--index =', index, '--model_path =', model_path, '--sub_mesh_path_list =', sub_mesh_path_list)
            ar_item_config = confmgr.get('lobby_model_display_conf', 'ArItem', 'Content', str(item_no), default={})
            default_min_scale = 0.1
            default_init_scale = 0.3
            cur_scale = ar_item_config.get('model_default_scale', default_init_scale)
            self._cur_scale_list[index] = cur_scale
            self._min_scale_list[index] = ar_item_config.get('model_min_scale', default_min_scale)
            self._max_scale_list[index] = ar_item_config.get('model_max_scale', 1)
            self.reset_rotate_model(index)
            self.log('test--show_model--step2--item_no =', item_no, '--cur_scale =', cur_scale, '--model_path =', model_path)
            hit_model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)
            hit_model.all_materials.enable_write_alpha = True
            hit_model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 1.0)
            decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(item_no)), [])
            color_dict = global_data.player.get_mecha_color().get(str(item_no), {})
            decal_lod = 0
            self.log('test--show_model--step3--decal_list =', decal_list)
            if decal_list:
                self.load_decal_data(hit_model, item_no, decal_list, decal_lod=decal_lod)
            if color_dict:
                self.load_color_data(hit_model, item_no, color_dict)
            self.panel.lab_place.setVisible(False)
            camera = self.scene.active_camera
            forward = -camera.world_rotation_matrix.forward
            yaw = forward.yaw
            mat = math3d.matrix.make_rotation_y(yaw)
            self.log('test--show_model--step2--mat.yaw =', mat.yaw, '--ori_forward.yaw =', camera.world_rotation_matrix.forward.yaw)
            self.cur_euler_rot_list[index] = math3d.matrix_to_euler(mat)
            self.target_euler_rot_list[index] = self.cur_euler_rot_list[index]
            hit_model.world_rotation_matrix = mat
            all_visible_node = [self.panel.temp_btn_replace, self.panel.nd_screen_shot, self.panel.btn_chose_mode]
            for one_node in all_visible_node:
                one_node.setVisible(True)

            self.add_panel_shadow(index, hit_model, item_no)
            self.init_action_list(index)
            self.show_action_btn(index)
            self.play_show_anim(hit_model, mecha_id)
            self.panel.btn_hide.setVisible(True)
            self.panel.btn_set.setVisible(True)
            self.panel.img_act_panel.setVisible(True)
            return

    def add_panel_shadow(self, index, model, item_no):
        self.log('test--add_panel_shadow--step1--model.filename =', model.filename)
        light = self.scene.get_light(LIGHT_NAME)
        if not light:
            self.log('test--add_panel_shadow--step2--dir_light =None--get_light_count =', self.scene.get_light_count())
            import traceback
            traceback.print_stack()
            return
        else:
            height = model.world_position.y
            model_path = model.filename.replace('empty.gim', 'l3.gim')
            if self.shadow_model_list[index]:
                model = self.shadow_model_list[index]
                self.del_model(model)
            shadow_model = world.model(model_path, None)
            self.shadow_model_list[index] = shadow_model
            shadow_model.visible = self._is_shadow_visible
            item_conf = confmgr.get('lobby_item', str(item_no))
            if item_conf:
                remove_socket_list = item_conf.get('remove_socket_list', [])
                global_data.model_mgr.remove_model_socket(shadow_model, remove_socket_list)
            shadow_model.set_parent(model)
            shadow_model.position = math3d.vector(0, 0, 0)
            shadow_model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
            shadow_model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
            shadow_model.all_materials.enable_write_alpha = True
            shadow_model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 1.0)
            direction = light.direction
            shadow_model.all_materials.set_var(_HASH_light_info, 'light_info', (direction.x, direction.y, direction.z, height))
            socket_count = shadow_model.get_socket_count()
            self.log('test--add_panel_shadow--step3--shadow_model.filename =', shadow_model.filename, '--shadow_model.visible =', shadow_model.visible, '--socket_count =', socket_count)
            for i in range(socket_count):
                socket_object_count = shadow_model.get_socket_obj_count(i)
                cur_socket_name = shadow_model.get_socket_name(i)
                for i in range(socket_object_count):
                    shadow_model.set_socket_bound_obj_active(cur_socket_name, i, False, False)

            return

    def load_decal_data(self, model, item_no, decal_list, avatar_data=False, decal_lod=0):
        skin_id = item_no
        if model and skin_id:
            if avatar_data:
                decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), [])
            elif decal_list and len(decal_list[0]) < 9:
                decal_list = decal_utils.decode_decal_list(decal_list)
            load_model_decal_data(model, skin_id, decal_list, decal_lod)

    def load_high_quality_model_decal(self, model, item_no, decal_list):
        skin_id = item_no
        if model and skin_id and decal_list:
            load_model_decal_high_quality(model, skin_id, decal_list)
            model = skin_id = decal_list = None
        return

    def load_color_data(self, model, item_no, color_dict, avatar_data=False):
        skin_id = item_no
        if model and skin_id:
            if avatar_data:
                color_dict = global_data.player.get_mecha_color().get(str(skin_id), {})
            elif color_dict and isinstance(color_dict, dict):
                color_dict = decal_utils.decode_color(color_dict)
            load_model_color_data(model, skin_id, color_dict)

    def play_show_anim(self, model, mecha_id):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        select_sfx = self.get_mecha_select_effect_id(mecha_id)
        display_enter_config = conf.get(str(select_sfx), {})
        self.log('test--play_show_anim--select_sfx =', select_sfx, '--display_enter_config =', display_enter_config)
        sound_name = display_enter_config.get('cSfxSoundName', '')
        self.change_model_preview_effect(model, display_enter_config['lobbyCallOutSfxPath'], sound_name)

    def test_model_preview_effect--- This code section failed: ---

1633       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'log'
           6  LOAD_CONST            1  'test--test_model_preview_effect--step1--hit_model_list ='
           9  LOAD_FAST             0  'self'
          12  LOAD_ATTR             1  'hit_model_list'
          15  CALL_FUNCTION_2       2 
          18  POP_TOP          

1634      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             1  'hit_model_list'
          25  POP_JUMP_IF_TRUE     32  'to 32'

1635      28  LOAD_CONST            0  ''
          31  RETURN_END_IF    
        32_0  COME_FROM                '25'

1637      32  LOAD_FAST             3  'create_sfx'
          35  POP_JUMP_IF_FALSE    51  'to 51'

1638      38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             2  'test_error_sfx'
          44  CALL_FUNCTION_0       0 
          47  POP_TOP          
          48  JUMP_FORWARD          0  'to 51'
        51_0  COME_FROM                '48'

1640      51  SETUP_LOOP          180  'to 234'
          54  LOAD_GLOBAL           3  'enumerate'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             1  'hit_model_list'
          63  CALL_FUNCTION_1       1 
          66  GET_ITER         
          67  FOR_ITER            163  'to 233'
          70  UNPACK_SEQUENCE_2     2 
          73  STORE_FAST            4  'index'
          76  STORE_FAST            5  'hit_model'

1641      79  LOAD_FAST             5  'hit_model'
          82  POP_JUMP_IF_FALSE    67  'to 67'
          85  LOAD_FAST             5  'hit_model'
          88  LOAD_ATTR             4  'valid'
        91_0  COME_FROM                '82'
          91  POP_JUMP_IF_FALSE    67  'to 67'

1642      94  LOAD_FAST             2  'scale'
          97  POP_JUMP_IF_FALSE   127  'to 127'

1643     100  LOAD_GLOBAL           5  'math3d'
         103  LOAD_ATTR             6  'vector'
         106  LOAD_FAST             2  'scale'
         109  LOAD_FAST             2  'scale'
         112  LOAD_FAST             2  'scale'
         115  CALL_FUNCTION_3       3 
         118  LOAD_FAST             5  'hit_model'
         121  STORE_ATTR            7  'scale'
         124  JUMP_FORWARD          0  'to 127'
       127_0  COME_FROM                '124'

1645     127  LOAD_FAST             1  'position'
         130  POP_JUMP_IF_FALSE   184  'to 184'

1646     133  LOAD_GLOBAL           8  'isinstance'
         136  LOAD_FAST             1  'position'
         139  LOAD_GLOBAL           9  'tuple'
         142  LOAD_GLOBAL          10  'list'
         145  BUILD_TUPLE_2         2 
         148  CALL_FUNCTION_2       2 
         151  POP_JUMP_IF_FALSE   172  'to 172'

1647     154  LOAD_GLOBAL           5  'math3d'
         157  LOAD_ATTR             6  'vector'
         160  LOAD_FAST             1  'position'
         163  CALL_FUNCTION_VAR_0     0 
         166  STORE_FAST            1  'position'
         169  JUMP_FORWARD          0  'to 172'
       172_0  COME_FROM                '169'

1649     172  LOAD_FAST             1  'position'
         175  LOAD_FAST             5  'hit_model'
         178  STORE_ATTR           11  'position'
         181  JUMP_FORWARD          0  'to 184'
       184_0  COME_FROM                '181'

1651     184  LOAD_FAST             0  'self'
         187  LOAD_ATTR             0  'log'
         190  LOAD_CONST            2  'test--test_model_preview_effect--step1--index ='
         193  LOAD_FAST             4  'index'
         196  LOAD_CONST            3  '--hit_model.position ='
         199  LOAD_FAST             5  'hit_model'
         202  LOAD_ATTR            11  'position'
         205  LOAD_CONST            4  '--hit_model.scale ='
         208  LOAD_FAST             5  'hit_model'
         211  LOAD_ATTR             7  'scale'
         214  LOAD_CONST            5  '--hit_model.filename ='
         217  LOAD_FAST             5  'hit_model'
         220  LOAD_ATTR            12  'filename'
         223  CALL_FUNCTION_8       8 
         226  POP_TOP          
         227  JUMP_BACK            67  'to 67'
         230  JUMP_BACK            67  'to 67'
         233  POP_BLOCK        
       234_0  COME_FROM                '51'

1653     234  SETUP_LOOP          139  'to 376'
         237  LOAD_GLOBAL          13  'six'
         240  LOAD_ATTR            14  'iteritems'
         243  LOAD_GLOBAL          15  'getattr'
         246  LOAD_GLOBAL           6  'vector'
         249  BUILD_MAP_0           0 
         252  CALL_FUNCTION_3       3 
         255  CALL_FUNCTION_1       1 
         258  GET_ITER         
         259  FOR_ITER            113  'to 375'
         262  UNPACK_SEQUENCE_2     2 
         265  STORE_FAST            6  'identifier'
         268  STORE_FAST            7  'one_plane_info'

1654     271  LOAD_FAST             7  'one_plane_info'
         274  UNPACK_SEQUENCE_2     2 
         277  STORE_FAST            8  'plane'
         280  STORE_FAST            9  'edge_point_list'

1655     283  LOAD_FAST             8  'plane'
         286  LOAD_ATTR            16  'world_transformation'
         289  STORE_FAST           10  'world_transformation'

1656     292  BUILD_LIST_0          0 
         295  STORE_FAST           11  'world_edge_point_list'

1657     298  SETUP_LOOP           49  'to 350'
         301  LOAD_GLOBAL           3  'enumerate'
         304  LOAD_FAST             9  'edge_point_list'
         307  CALL_FUNCTION_1       1 
         310  GET_ITER         
         311  FOR_ITER             35  'to 349'
         314  UNPACK_SEQUENCE_2     2 
         317  STORE_FAST            4  'index'
         320  STORE_FAST           12  'one_point'

1658     323  LOAD_FAST            12  'one_point'
         326  LOAD_FAST            10  'world_transformation'
         329  BINARY_MULTIPLY  
         330  STORE_FAST           13  'world_position'

1659     333  LOAD_FAST            11  'world_edge_point_list'
         336  LOAD_ATTR            17  'append'
         339  LOAD_FAST            12  'one_point'
         342  CALL_FUNCTION_1       1 
         345  POP_TOP          
         346  JUMP_BACK           311  'to 311'
         349  POP_BLOCK        
       350_0  COME_FROM                '298'

1661     350  LOAD_FAST             0  'self'
         353  LOAD_ATTR             0  'log'
         356  LOAD_CONST            7  'test--test_model_preview_effect--step2--plane ='
         359  LOAD_FAST             8  'plane'
         362  LOAD_CONST            8  '--world_edge_point_list ='
         365  LOAD_FAST            11  'world_edge_point_list'
         368  CALL_FUNCTION_4       4 
         371  POP_TOP          
         372  JUMP_BACK           259  'to 259'
         375  POP_BLOCK        
       376_0  COME_FROM                '234'

1663     376  LOAD_FAST             0  'self'
         379  LOAD_ATTR             0  'log'
         382  LOAD_CONST            9  'test--test_model_preview_effect--step3--aspect ='
         385  LOAD_FAST             0  'self'
         388  LOAD_ATTR            18  'scene'
         391  LOAD_ATTR            19  'active_camera'
         394  LOAD_ATTR            20  'aspect'
         397  LOAD_CONST           10  '--fov ='
         400  LOAD_FAST             0  'self'
         403  LOAD_ATTR            18  'scene'
         406  LOAD_ATTR            19  'active_camera'
         409  LOAD_ATTR            21  'fov'
         412  LOAD_CONST           11  '--z_range ='
         415  LOAD_FAST             0  'self'
         418  LOAD_ATTR            18  'scene'
         421  LOAD_ATTR            19  'active_camera'
         424  LOAD_ATTR            22  'z_range'
         427  LOAD_CONST           12  '--look_at ='
         430  LOAD_FAST             0  'self'
         433  LOAD_ATTR            18  'scene'
         436  LOAD_ATTR            19  'active_camera'
         439  LOAD_ATTR            23  'look_at'
         442  LOAD_CONST           13  '--transformation ='
         445  LOAD_FAST             0  'self'
         448  LOAD_ATTR            18  'scene'
         451  LOAD_ATTR            19  'active_camera'
         454  LOAD_ATTR            24  'transformation'
         457  LOAD_CONST           14  '--projection_matrix ='
         460  LOAD_FAST             0  'self'
         463  LOAD_ATTR            18  'scene'
         466  LOAD_ATTR            19  'active_camera'
         469  LOAD_ATTR            25  'projection_matrix'
         472  CALL_FUNCTION_12     12 
         475  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 255

    def change_model_preview_effect(self, model, sfx_path, sfx_sound_name=None):
        if not model:
            return
        self.log('test--change_model_preview_effect--sfx_path =', sfx_path, '--sfx_sound_name =', sfx_sound_name)
        global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_zhaohuan', duration=0, on_create_func=self.create_enter_display_sfx_callback)
        if sfx_sound_name:
            global_data.sound_mgr.play_ui_sound(sfx_sound_name)

    def create_enter_display_sfx_callback(self, sfx, *args):
        self._enter_display_sfx_list.append(sfx)
        if hasattr(sfx, 'enable_write_alpha'):
            sfx.enable_write_alpha(True)

    def show_action_btn(self, index):
        btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
        mecha_photo_node = getattr(self.panel, 'temp__mecha_' + str(index + 1), None)
        if not btn_action or not mecha_photo_node:
            log_error('test--show_action_btn--step1--index =', index, '--btn_action =', btn_action, '--mecha_photo_node =', mecha_photo_node)
            return
        else:
            self.log('test--show_action_btn--step2--index =', index, '--no_action_tag =', self.no_action_tag, '--btn_action =', btn_action)
            if self.no_action_tag:
                btn_action.setVisible(False)
                mecha_photo_node.setVisible(False)
            else:
                mecha_id, skin_id, shiny_weapon_id = self._mecha_info_list[index]
                self.panel.img_act_panel.setVisible(True)
                frame_item_no = None
                role_head_utils.init_mecha_head(mecha_photo_node.temp__mecha, frame_item_no, mecha_id)
                btn_action.setVisible(True)
                mecha_photo_node.setVisible(True)
            return

    def hide_action_btn(self, index):
        btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
        mecha_photo_node = getattr(self.panel, 'temp__mecha_' + str(index + 1), None)
        if not btn_action or not mecha_photo_node:
            log_error('test--hide_action_btn--step1--btn_action None--index =', index)
            return
        else:
            self.log('test--hide_action_btn--step2--index =', index, '--btn_action =', btn_action, '--no_action_tag =', self.no_action_tag)
            btn_action.setVisible(False)
            mecha_photo_node.setVisible(False)
            return

    def show_action_list(self, index):
        btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
        if not btn_action:
            log_error('test--show_action_list--step1--btn_action None--index =', index)
            return
        else:
            actione_list = getattr(self.panel, 'actione_list_' + str(index + 1), None)
            if not actione_list:
                log_error('test--show_action_list--step2--actione_list None--index =', index)
                return
            actione_list.setVisible(True)
            btn_action.img_icon.setRotation(180)
            return

    def hide_action_list(self, index):
        btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
        if not btn_action:
            log_error('test--hide_action_list--step1--btn_action None--index =', index)
            return
        else:
            actione_list = getattr(self.panel, 'actione_list_' + str(index + 1), None)
            if not actione_list:
                log_error('test--hide_action_list--step2--actione_list None--index =', index)
                return
            actione_list.setVisible(False)
            btn_action.img_icon.setRotation(0)
            return

    def on_click_shrink_action_list(self, *args):
        self.shrink_action_list()

    def shrink_action_list(self):
        self._show_action_detail_type = HIDE_ACTION_DETAIL
        self.panel.PlayAnimation('panel_disappear')
        for index, _ in enumerate(self._mecha_info_list):
            btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
            if btn_action:
                btn_action.setVisible(False)

        self.log('test--shrink_action_list')
        return

    def on_click_unfold_action_list(self, *args):
        self._show_action_detail_type = SHOW_ACTION_DETAIL
        self.panel.PlayAnimation('panel_show')
        self.panel.img_act_panel.setVisible(True)
        for index, one_mecha_info in enumerate(self._mecha_info_list):
            btn_action = getattr(self.panel, 'btn_action_' + str(index + 1), None)
            if btn_action and one_mecha_info:
                btn_action.setVisible(True)

        return

    def on_click_screen(self, *args):
        hide_list = [
         self.panel.lab_description, self.panel.img_act_panel, self.panel.nd_screen_shot, self.panel.temp_btn_back, self.panel.temp_btn_replace, self.panel.nd_choose, self.panel.btn_chose_mode, self.panel.btn_scene_ui, self.panel.nd_slider, self.panel.btn_hide, self.panel.btn_set, self.panel.nd_set_pnl]
        all_item_pre_fix_name = [
         'btn_action_', 'actione_list_', 'temp__mecha_']
        for index in range(MAX_MECHA_NUM):
            for name in all_item_pre_fix_name:
                one_icon = getattr(self.panel, name + str(index + 1), None)
                hide_list.append(one_icon)

        actual_hide_list = []
        for one_node in hide_list:
            if one_node.isVisible():
                actual_hide_list.append(one_node)

        self.panel.lab_description.setVisible(True)
        if self._screen_capture_helper:
            ui_names = [
             self.__class__.__name__]

            def cb(*args):
                if not self.panel:
                    return
                for one_node in actual_hide_list:
                    one_node.setVisible(True)

            for one_node in actual_hide_list:
                one_node.setVisible(False)

            def share_cb(*args):
                self.log('test--share_cb--player =', global_data.player)
                if global_data.player:
                    global_data.player.share_activity('share_ar')

            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb, head_nd_name='nd_player_info_1', share_inform_func=share_cb)
        return

    def on_click_choose_mecha(self, *args):
        self._show_choose_mecha_list = not self._show_choose_mecha_list
        self.panel.nd_choose.setVisible(self._show_choose_mecha_list)
        if self._show_choose_mecha_list:
            self.panel.PlayAnimation('change')
            self.refresh_mecha_list()
            self.shrink_action_list()
        else:
            self.hide_mecha_list()

    def hide_mecha_list(self):
        self.panel.StopAnimation('change')
        self._show_choose_mecha_list = False
        self.panel.nd_choose.setVisible(False)

    def refresh_mecha_list(self):
        has_red_point = False
        self.panel.list_rank_list.SetInitCount(len(self._all_mecha_lst))
        all_item = self.panel.list_rank_list.GetAllItem()
        cur_show_mecha_list = []
        for one_mecha_info in self._mecha_info_list:
            if not one_mecha_info:
                continue
            mecha_id, skin_id, shiny_weapon_id = one_mecha_info
            cur_show_mecha_list.append(mecha_id)

        for index, ui_item in enumerate(all_item):
            mecha_id = self._all_mecha_lst[index]
            conf = self._mecha_conf[str(mecha_id)]
            img_path = 'gui/ui_res_2/mech_display/img_mech%s.png' % mecha_id
            ui_item.mech_head.SetDisplayFrameByPath('', img_path)
            ui_item.lab_mech_name.SetString(conf.get('name_mecha_text_id', ''))
            has_empty_slot = check_mecha_component_page_has_empty_slot(mecha_id)
            has_module_red_p = check_inscription_module_red_point(mecha_id)
            has_single_red_point = has_empty_slot or has_module_red_p
            if has_single_red_point:
                has_red_point = True
            red_point_utils.show_red_point_template(ui_item.temp_red, has_single_red_point)
            ui_item.mech_head_shade.SetDisplayFrameByPath('', img_path)
            ui_item.img_lock.setVisible(mecha_id not in self._open_mecha_lst)
            ui_item.img_choose.setVisible(mecha_id in cur_show_mecha_list)

            @ui_item.btn_shose_mech.callback()
            def OnBegin(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                return True

            @ui_item.btn_shose_mech.callback()
            def OnEnd(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                pass

            @ui_item.btn_shose_mech.callback()
            def OnCancel(btn, touch, mecha_id=mecha_id, ui_item=ui_item):
                pass

            @ui_item.btn_shose_mech.callback()
            def OnClick(btn, touch, mecha_id=mecha_id):
                self.hide_mecha_list()
                self.select_mecha(mecha_id)

    def cancel_mecha_index(self, index):
        self._mecha_info_list[index] = None
        model = self.hit_model_list[index]
        mecha_skin_utils.clear_skin_anim_sfx_func_cache(model)
        mecha_skin_utils.clear_skin_model_and_effect(model)
        mecha_skin_utils.unregister_socket_res_auto_refresh(model)
        self.del_model(model)
        self.hit_model_list[index] = None
        model = self.shadow_model_list[index]
        if model:
            self.del_model(model)
            self.shadow_model_list[index] = None
        self.cur_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self.target_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self._cur_scale_list[index] = 1
        self._min_scale_list[index] = 1
        self._max_scale_list[index] = 1
        self.log('test--cancel_mecha_index--step1--index =', index)
        self.hide_action_list(index)
        self.hide_action_btn(index)
        self.log('test--cancel_mecha_index--index =', index, '--get_mecha_num =', self.get_mecha_num())
        if self.get_mecha_num() <= 0:
            self.panel.img_act_panel.setVisible(False)
            self.panel.btn_hide.setVisible(False)
            self.panel.btn_set.setVisible(False)
            self.panel.nd_set_pnl.setVisible(False)
            self.panel.btn_scene_ui.setVisible(False)
            self.panel.nd_slider.setVisible(False)
            self.reset_ar_scene()
            self._select_model_index = -1
        elif self._select_model_index == index:
            self._select_model_index = -1
            self.panel.btn_scene_ui.setVisible(False)
            self.panel.nd_slider.setVisible(False)
        return

    def select_mecha(self, select_mecha_id):
        if select_mecha_id not in self._open_mecha_lst:
            return
        mecha_index = -1
        for index, one_mecha_info in enumerate(self._mecha_info_list):
            if not one_mecha_info:
                continue
            mecha_id, skin_id, shiny_weapon_id = one_mecha_info
            if mecha_id == select_mecha_id:
                mecha_index = index
                break

        self.log('test--select_mecha--step1--mecha_index =', mecha_index, '--get_mecha_num =', self.get_mecha_num(), '--_mecha_info_list =', self._mecha_info_list)
        if mecha_index >= 0:
            self.cancel_mecha_index(mecha_index)
            return
        if self.get_mecha_num() >= MAX_MECHA_NUM:
            global_data.game_mgr.show_tip(get_text_by_id(609390))
            return
        self.add_mecha_on_scene(select_mecha_id)

    def add_mecha_on_scene(self, select_mecha_id):
        first_model = None
        for one_model in self.hit_model_list:
            if one_model:
                first_model = one_model
                break

        rotation_matrix = first_model.world_rotation_matrix
        right_dir = rotation_matrix.right
        if not right_dir.is_zero:
            right_dir.normalize()
        left_dir = right_dir * math3d.matrix.make_rotation_y(-math.pi)
        if not left_dir.is_zero:
            left_dir.normalize()
        dest_pos = first_model.position
        offset = 0.35 * AR_TO_GAME_SCALE
        if self.get_mecha_num() == 1:
            dest_pos = dest_pos + left_dir * offset
        else:
            dest_pos = dest_pos + right_dir * offset
        skin_list_cnf = mecha_skin_utils.get_show_skin_list(select_mecha_id)
        skin_id = skin_list_cnf[0]
        dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(select_mecha_id)
        shiny_weapon_id = dress_utils.get_mecha_dress_shiny_weapon_id(select_mecha_id)
        if dressed_clothing_id is not None:
            if dressed_clothing_id in skin_list_cnf:
                skin_id = dressed_clothing_id
        mecha_index = self.get_empty_mecha_index()
        self._mecha_info_list[mecha_index] = (select_mecha_id, skin_id, shiny_weapon_id)
        self.show_model(mecha_index)
        dest_pos = self.check_mecha_pos_valid(first_model.position, dest_pos)
        self.hit_model_list[mecha_index].position = dest_pos
        self.log('test--add_mecha_on_scene--select_mecha_id =', select_mecha_id, '--hit_model_list[-1].position =', self.hit_model_list[-1].position, '--hit_model_list[-2].position =', self.hit_model_list[-2].position)
        return

    def check_mecha_pos_valid(self, ref_pos, dest_pos):
        for plane, edge_point_list in six_ex.values(self.plane_dict):
            plane_position = plane.position
            min_position = plane_position + edge_point_list[0]
            max_position = plane_position + edge_point_list[-1]
            if ref_pos.x < min_position.x or ref_pos.x > max_position.x:
                continue
            if ref_pos.z < min_position.z or ref_pos.z > max_position.z:
                continue
            if dest_pos.x < min_position.x or dest_pos.x > max_position.x or dest_pos.z < min_position.z or dest_pos.z > max_position.z:
                move_dir = dest_pos - ref_pos
                offset = move_dir.length
                min_x_dist = abs(dest_pos.x - min_position.x)
                max_x_dist = abs(dest_pos.x - max_position.x)
                dir_x = 1
                if min_x_dist > max_x_dist:
                    dir_x = min_position.x - dest_pos.x
                else:
                    dir_x = max_position.x - dest_pos.x
                min_z_dist = abs(dest_pos.z - min_position.z)
                max_z_dist = abs(dest_pos.z - max_position.z)
                dir_x = 1
                if min_z_dist > max_z_dist:
                    dir_z = min_position.z - dest_pos.z
                else:
                    dir_z = max_position.z - dest_pos.z
                adjust_move_dir = math3d.vector(dir_x, 0, dir_z)
                self.log('test--add_mecha_on_scene--check_mecha_pos_valid--adjust_move_dir =', adjust_move_dir)
                if not adjust_move_dir.is_zero:
                    adjust_move_dir.normalize()
                adjust_move_dir = adjust_move_dir * offset
                return ref_pos + adjust_move_dir

        return dest_pos

    def on_click_replace(self, *args):
        for index, one_mecha_info in enumerate(self._mecha_info_list):
            if not one_mecha_info:
                continue
            self.cancel_mecha_index(index)

        self.log('test--on_click_replace')
        self.reset_ar_scene()
        self.start_config(CONFIG, ASSETS)

    def reset_ar_scene(self):
        for index in range(MAX_MECHA_NUM):
            self.hide_action_list(index)
            self.hide_action_btn(index)

        self.clear_model()
        self.panel.lab_place.setVisible(True)
        all_visible_node = [self.panel.temp_btn_replace, self.panel.nd_screen_shot, self.panel.btn_chose_mode, self.panel.nd_choose, self.panel.btn_scene_ui, self.panel.nd_slider]
        for one_node in all_visible_node:
            one_node.setVisible(False)

    def on_click_test(self, *args):
        self.start_time = time.time()
        self.log('test--on_click_test')

    def on_click_action1(self, *args):
        self.on_click_action(0)

    def on_click_action2(self, *args):
        self.on_click_action(1)

    def on_click_action3(self, *args):
        self.on_click_action(2)

    def on_click_action(self, index):
        if self._show_action_detail_type == HIDE_ACTION_DETAIL:
            return
        else:
            if self.no_action_tag:
                return
            actione_list = getattr(self.panel, 'actione_list_' + str(index + 1), None)
            if not actione_list:
                log_error('test--on_click_action--step1--actione_list None--index =', index)
                return
            if actione_list.isVisible():
                self.hide_action_list(index)
            else:
                self.show_action_list(index)
            return

    def on_click_choose_mecha1(self, *args):
        self.on_click_choose_scene_mecha(0)

    def on_click_choose_mecha2(self, *args):
        self.on_click_choose_scene_mecha(1)

    def on_click_choose_mecha3(self, *args):
        self.on_click_choose_scene_mecha(2)

    def on_click_choose_scene_mecha(self, index):
        self._select_model_index = index
        self.panel.btn_scene_ui.setVisible(True)
        self.panel.nd_slider.setVisible(True)
        self.update_model_arrow_pos()
        self.update_slider_percent()

    def update_slider_percent(self):
        if self._select_model_index < 0:
            return
        index = self._select_model_index
        cur_scale = self._cur_scale_list[index]
        min_scale = self._min_scale_list[index]
        max_scale = self._max_scale_list[index]
        denominator = max_scale - min_scale
        if denominator <= 0:
            self.log('test--update_slider_percent--step2--index =', index, '--denominator =', denominator, '--max_scale =', max_scale, '--min_scale =', min_scale)
            return
        percent = (cur_scale - min_scale) / denominator
        self.log('test--update_slider_percent--step3--_select_model_index =', index, '--percent =', percent, '--cur_scale =', cur_scale, '--max_scale =', max_scale, '--min_scale =', min_scale)
        percent = min(percent, 1)
        percent = max(percent, 0)
        self.panel.nd_slider.slider.setPercent(percent * 100)

    def on_light_rotate_y_percent_change(self, percent):
        light = self.scene.get_light(LIGHT_NAME)
        rotation_matrix = light.world_rotation_matrix
        old_yaw = rotation_matrix.yaw
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_y(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix
        self.log('test--on_light_rotate_y_percent_change--step1--cur_value =', cur_value, '--old_yaw =', old_yaw, '--percent =', percent)

    def on_light_rotate_x_percent_change(self, percent):
        light = self.scene.get_light(LIGHT_NAME)
        rotation_matrix = light.world_rotation_matrix
        old_pitch = rotation_matrix.pitch
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_x(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix
        self.log('test--on_light_rotate_x_percent_change--step1--cur_value =', cur_value, '--old_pitch =', old_pitch, '--percent =', percent)

    def on_light_rotate_z_percent_change(self, percent):
        light = self.scene.get_light(LIGHT_NAME)
        rotation_matrix = light.world_rotation_matrix
        old_roll = rotation_matrix.roll
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_z(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix
        self.log('test--on_light_rotate_z_percent_change--step1--cur_value =', cur_value, '--old_roll =', old_roll, '--percent =', percent)

    def on_direct_light_intensity_percent_change(self, percent):
        min_value = 0
        max_value = MAX_DIRECT_INTENSITY
        cur_value = min_value + (max_value - min_value) * percent
        light = self.scene.get_light(LIGHT_NAME)
        light.intensity = cur_value
        self.log('test--on_direct_light_intensity_percent_change--step1--cur_value =', cur_value, '--percent =', percent)

    def on_indirect_light_intensity_percent_change(self, percent):
        min_value = 0
        max_value = MAX_INDIRECT_INTENSITY
        cur_value = min_value + (max_value - min_value) * percent
        light = self.scene.get_light(LIGHT_NAME)
        self.log('test--on_indirect_light_intensity_percent_change--step1--cur_value =', cur_value, '--light.intensity =', light.intensity)
        self.scene.set_global_uniform('ToonIndirectIntensity', cur_value)

    def one_model_percent_change(self, percent):
        if self._select_model_index < 0:
            return
        index = self._select_model_index
        cur_scale = self._min_scale_list[index] + (self._max_scale_list[index] - self._min_scale_list[index]) * percent
        self._cur_scale_list[index] = cur_scale
        self._cur_scale_list[index] = max(self._cur_scale_list[index], self._min_scale_list[index])
        self._cur_scale_list[index] = min(self._cur_scale_list[index], self._max_scale_list[index])
        self.log('test--one_model_percent_change--step1--_select_model_index =', index, '--percent =', percent, '--cur_scale =', cur_scale, '--max_scale =', self._max_scale_list[index], '--min_scale =', self._min_scale_list[index])
        hit_model = self.hit_model_list[index]
        if hit_model and hit_model.valid:
            hit_model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)

    def on_click_delete_mecha1(self, *args):
        self.cancel_mecha_index(0)

    def on_click_delete_mecha2(self, *args):
        self.cancel_mecha_index(1)

    def on_click_delete_mecha3(self, *args):
        self.cancel_mecha_index(2)

    def on_load_mesh_completed(self, res_path, model):
        self.log('test--on_load_mesh_completed--res_path =', res_path, '--model.filename =', model.filename)
        if res_path in self._load_lod_mesh_task_dict:
            del self._load_lod_mesh_task_dict[res_path]

    def setup_ar_scene(self):
        self.log('Setup AR Scene...')
        self.ar_type = self.session.get_current_ar_type()
        if self.ar_type == ar.AR_INSIGHT:
            self.log('test--setup_ar_scene--Current AR Type: InsightAR')
        elif self.ar_type == ar.AR_ARCORE:
            self.log('test--setup_ar_scene--Current AR Type: ARCore')
        elif self.ar_type == ar.AR_ARKIT:
            self.log('test--setup_ar_scene--Current AR Type: ARKit')
        else:
            self.log('test--setup_ar_scene--Current AR Type: Unknown')
        self.log('Setup Camera Texture...')
        self.setup_cam_texture()
        if self.ar_width == 0 or self.ar_height == 0:
            return
        if not self.background_model:
            return
        self.log('Setup AR Scene RenderTarget...')
        from common.uisys.uielment.CCSprite import CCSprite
        self.init_light_slider_value()
        self.log('Create AR Scene and Render to RenderTarget...')

    def is_portrait(self):
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        designSize = view.getDesignResolutionSize()
        if designSize.width >= designSize.height:
            return False
        return True

    def create_ploy(self):
        return
        size = game3d.get_window_size()
        self.log('test--create_ploy--step1--size =', size, '--rt_width =', self.rt_width, '--rt_height =', self.rt_height, '--ar_width =', self.ar_width, '--ar_height =', self.ar_height, '--is_portrait =', self.is_portrait())
        device_name = global_data.deviceinfo.get_device_model_name()
        realY = 1.0
        theRatio = 1.0 * self.rt_width / self.rt_height
        selfRatio = 1.0 * self.ar_width / self.ar_height
        if abs(selfRatio - theRatio) < 0.01:
            realU = 1.0
            realV = 1.0
        elif selfRatio < theRatio:
            needHeight = self.ar_width / theRatio
            realU = 1.0
            realV = needHeight / self.ar_height
        else:
            needWidth = self.ar_height / theRatio
            realU = needWidth / self.ar_width
            realV = 1.0
        if 'ipad' in device_name:
            realY = 0.8
            realU = 0.8
            realV = 0.8
        pos_z = 0
        self.log('test--create_ploy--step2--device_name =', device_name, '--rotateMode =', self.rotateMode, '--realU =', realU, '--realV =', realV, '--pos_z =', pos_z)
        if self.rotateMode == 3:
            self.primitive1.create_poly4([
             (
              (
               math3d.vector(-1, realY, pos_z), 0, realV),
              (
               math3d.vector(1, realY, pos_z), realU, realV),
              (
               math3d.vector(1, -realY, pos_z), realU, 0),
              (
               math3d.vector(-1, -realY, pos_z), 0, 0),
              16773292)])
        elif rotateMode == 1:
            self.primitive1.create_poly4([
             (
              (
               math3d.vector(-1, realY, pos_z), 0, 0),
              (
               math3d.vector(1, realY, pos_z), 0, realV),
              (
               math3d.vector(1, -realY, pos_z), realU, realV),
              (
               math3d.vector(-1, -realY, pos_z), realU, 0),
              16773292)])
        else:
            self.primitive1.create_poly4([
             (
              (
               math3d.vector(-1, realY, pos_z), realU, 0),
              (
               math3d.vector(1, realY, pos_z), 0, 0),
              (
               math3d.vector(1, -realY, pos_z), 0, realV),
              (
               math3d.vector(-1, -realY, pos_z), realU, realV),
              16773292)])

    def setup_cam_texture(self):
        self.background_model = world.model(BACKGROUND_MODEL_PATH, self.scene)
        self.log('test--setup_cam_texture--step1--active_camera =', self.scene.active_camera, '--background_model =', self.background_model)
        self.background_model.remove_from_parent()
        self.background_model.set_parent(self.scene.active_camera)
        if self.platform == game3d.PLATFORM_ANDROID:
            self.setup_cam_texture_android()
        elif self.platform == game3d.PLATFORM_IOS:
            self.setup_cam_texture_ios()
        else:
            return
        if not self.background_model:
            self.log('[Error] test--setup_cam_texture--background_model =', self.background_model)
            return

    def setup_cam_texture_android(self):
        data_provider = self.session.fetch_cam_data_provider()
        if data_provider is None:
            self.log('Error: fetch camera data provider failed.')
            return
        else:
            nx_tex = render.texture('', False, False, 0, False, None, None, 0, 0, False, data_provider)
            self.log('Camera Tex Size: %s', nx_tex.size)
            self.log('test--setup_cam_texture_android--step1--ar_type =', self.ar_type, '--AR_INSIGHT =', ar.AR_INSIGHT, '--AR_ARCORE =', ar.AR_ARCORE, '--nx_tex.size =', nx_tex.size, '--global_data.really_window_size =', global_data.really_window_size, '--design_screen_size =', global_data.ui_mgr.design_screen_size)
            shader_path = ''
            if self.ar_type == ar.AR_INSIGHT:
                shader_path = 'shader/g93shader/rgb.nfx::TShader'
            elif self.ar_type == ar.AR_ARCORE:
                shader_path = 'shader/built_in/dyntex/yuv_to_rgb.nfx::TShader'
            else:
                self.log('Unknown AR Type: %s', self.ar_type)
                return
            self.background_model.all_materials.set_technique(1, shader_path)
            self.background_model.all_materials.set_texture('Tex0', nx_tex)
            self.background_model.all_materials.rebuild_tech()
            self.ar_width = data_provider.size[0]
            self.ar_height = data_provider.size[1]
            return

    def setup_cam_texture_ios(self):
        y_provider = self.session.fetch_cam_y_data_provider()
        uv_provider = self.session.fetch_cam_uv_data_provider()
        if y_provider is None or uv_provider is None:
            self.log('Error: fetch camera data provider failed.')
            return
        else:
            nx_y_tex = render.texture('', False, False, render.TEXTURE_TYPE_UNKNOWN, False, None, None, 0, 0, False, y_provider)
            self.log('Camera Y Tex Size: %s', nx_y_tex.size)
            nx_uv_tex = render.texture('', False, False, render.TEXTURE_TYPE_UNKNOWN, False, None, None, 0, 0, False, uv_provider)
            self.log('Camera UV Tex Size: %s', nx_uv_tex.size)
            self.log('test--setup_cam_texture_ios--step1--get_render_device =', game3d.get_render_device(), '--DEVICE_METAL =', game3d.DEVICE_METAL)
            shader_path = ''
            if game3d.get_render_device() == game3d.DEVICE_METAL:
                shader_path = 'shader/g93shader/yuv_to_rgb_soft_l8.nfx::TShader'
            else:
                shader_path = 'shader/g93shader/yuv_to_rgb_soft_r8.nfx::TShader'
            self.background_model.all_materials.set_technique(1, shader_path)
            self.background_model.all_materials.set_texture('Tex0', nx_y_tex)
            self.background_model.all_materials.set_texture('Tex1', nx_uv_tex)
            self.background_model.all_materials.rebuild_tech()
            self.log('test--setup_cam_texture_ios--step1--ar_type =', self.ar_type, '--AR_INSIGHT =', ar.AR_INSIGHT, '--AR_ARCORE =', ar.AR_ARCORE, '--nx_y_tex.size =', nx_y_tex.size, '--global_data.really_window_size =', global_data.really_window_size, '--design_screen_size =', global_data.ui_mgr.design_screen_size)
            self.log('test--setup_cam_texture_ios--nx_y_tex.size =', nx_y_tex.size, '--y_provider.size =', y_provider.size, '--uv_provider.size =', uv_provider.size)
            self.ar_width = y_provider.size[0]
            self.ar_height = y_provider.size[1]
            return

    def on_frame_cb(self, session, state, reason, timestamp, cam_pose, cam_param):
        if state == ar.STATE_INIT_FAIL:
            self.panel.lab_place.SetString(609130)
            self.panel.lab_description.setVisible(False)
            return
        else:
            if self.on_frame_cb_log:
                self.log('test--on_frame_cb--step1--state =', state, '--reason =', reason, '--timestamp=', timestamp, '--primitive =', self.background_model, '--scene =', self.scene, '--STATE_DETECTING =', ar.STATE_DETECTING, '--STATE_TRACKING =', ar.STATE_TRACKING)
                self.log('on_frame_cb.cam_pose: %s %s', cam_pose.center, cam_pose.quaternion)
                self.log('on_frame_cb.cam_param: %s %s %s %s', cam_param.orientation, cam_param.focal_length, cam_param.fov, cam_param.proj_mtx)
            center = list(cam_pose.center)
            center[0] = center[0] * AR_TO_GAME_SCALE
            center[1] = center[1] * AR_TO_GAME_SCALE
            center[2] = center[2] * AR_TO_GAME_SCALE
            self.log('test--on_frame_cb--step2--state =', state, '--reason =', reason, '--timestamp=', timestamp, '--scene =', self.scene, '--STATE_DETECTING =', ar.STATE_DETECTING, '--STATE_TRACKING =', ar.STATE_TRACKING)
            if (state == ar.STATE_DETECTING or state == ar.STATE_TRACKING) and self.background_model is None:
                self.log('test--on_frame_cb--step3--state =', state, '--reason =', reason, '--timestamp=', timestamp, '--scene =', self.scene, '--STATE_DETECTING =', ar.STATE_DETECTING, '--STATE_TRACKING =', ar.STATE_TRACKING)
                self.on_frame_cb_log = 0
                self.setup_ar_scene()
                self.setup_camera_param(cam_param)
            if self.background_model is None:
                return
            if state != ar.STATE_TRACKING and state != ar.STATE_TRACK_LIMITED:
                return
            camera_pos = math3d.vector(*center)
            camera_rot = math3d.rotation(*cam_pose.quaternion)
            self.log('test--on_frame_cb--step1--camera_pos =', camera_pos, '--get_forward =', camera_rot.get_forward(), '--get_up =', camera_rot.get_up())
            camera = self.scene.active_camera
            camera.set_placement(camera_pos, camera_rot.get_forward(), camera_rot.get_up())
            self.log('Camera LookAt: %s %s', camera_rot.get_forward(), camera_rot.get_up())
            return

    def setup_camera_param(self, cam_param):
        if not self.scene or not self.scene.active_camera:
            return
        rt_ratio = self.rt_width / self.rt_height
        ar_ratio = self.ar_width / self.ar_height
        if ar_ratio < rt_ratio:
            focal = 0.5 / math.tan(math.radians(cam_param.fov[0] / 2.0)) * self.rt_width
            fov_y = math.degrees(math.atan(0.5 / focal * self.rt_height)) * 2
            aspect = 1.0 * self.rt_width / self.rt_height
            z_min = 1
            z_max = 20000
            self.log('Camera focal: %s, %s', focal, cam_param.focal_length * AR_TO_GAME_SCALE)
        else:
            fov_y = cam_param.fov[1]
            aspect = 1.0 * self.rt_width / self.rt_height
            z_min = 1
            z_max = 20000
        self.log('Camera Param: ar_ratio=%s, rt_ratio=%s, fov_y =%s, aspect=%s, z_min=%s, z_max=%s', ar_ratio, rt_ratio, fov_y, aspect, z_min, z_max)
        self.scene.active_camera.set_perspect(fov_y, aspect, z_min, z_max)
        self.log('test--setup_camera_param--step1--fov_y =', fov_y, '--aspect =', aspect, '--z_min =', z_min, '--z_max =', z_max, '--rt_width =', self.rt_width, '--rt_height =', self.rt_height)

    def on_error_cb(self, session, err_code, err_msg):
        self.log('on_error_cb: %s, %s', err_code, err_msg)

    def make_plane_edge_points(self, w, h):
        edge_point_list = [
         math3d.vector(-0.5 * w, 0, -0.5 * h), math3d.vector(-0.5 * w, 0, 0.5 * h), math3d.vector(0.5 * w, 0, -0.5 * h), math3d.vector(0.5 * w, 0, 0.5 * h)]
        return edge_point_list

    def on_anchor_added_cb(self, session, anchor_data):
        if self.on_anchor_added_cb_log:
            self.log('test--on_anchor_added_cb: identifier=%s, type=%s, alignment=%s, is_valid=%s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
            self.log('test--on_anchor_added_cb.rotation: %s', anchor_data.rotation)
            self.log('test--on_anchor_added_cb.center: %s', anchor_data.center)
            self.log('test--on_anchor_added_cb.extent: %s', anchor_data.extent)
        if self.start_time > 0:
            cur_time = time.time()
            pass_time = cur_time - self.start_time
            self.start_time = 0
            self.log('test--on_anchor_added_cb--step1--pass_time =%s', pass_time)
        self.log('test--on_anchor_added_cb--step2--anchor_data.type =', anchor_data.type, '--ar.ANCHOR_PLANE =', ar.ANCHOR_PLANE, '--ar.ANCHOR_MARKER_2D =', ar.ANCHOR_MARKER_2D)
        if anchor_data.type == ar.ANCHOR_PLANE:
            self.log('test--on_anchor_added_cb--step2--type(anchor_data.center) =', type(anchor_data.center), '--len(anchor_data.center) =', len(anchor_data.center), '--type(anchor_data.rotation) =', type(anchor_data.rotation), '--len(anchor_data.rotation) =', len(anchor_data.rotation), '--anchor_data.rotation =', anchor_data.rotation)
            pos, rot = self.get_plane_pos_rot(anchor_data)
            w = anchor_data.extent[0] * AR_TO_GAME_SCALE
            h = anchor_data.extent[2] * AR_TO_GAME_SCALE
            plane = self.make_plane(w, h)
            self.panel.temp_scene.StopAnimation('show')
            self.panel.temp_scene.nd_reticle.setVisible(False)
            plane.position = pos
            edge_point_list = self.make_plane_edge_points(w, h)
            self.log('test--on_anchor_added_cb--step3--width =', w, '--height =', h, '--anchor_data.extent =', anchor_data.extent, '--ar_type =', self.ar_type, '--plane =', type(plane), '--type(plane.rotation_matrix) =', type(plane.rotation_matrix))
            if self.ar_type == ar.AR_ARCORE:
                plane.rotation_matrix = rot
            elif self.ar_type == ar.AR_ARKIT:
                plane.rotation_matrix = rot
            self.plane_dict[anchor_data.identifier] = (plane, edge_point_list)
            if not self._plane_visible_timer_id:
                self._plane_visible_timer_id = global_data.game_mgr.register_logic_timer(self.check_plane_visible_tick, interval=1, times=-1, mode=timer.CLOCK)
            self.log('[==TEST==] Plane Added: %s, %s', pos, rot)
        elif anchor_data.type == ar.ANCHOR_MARKER_2D:
            pos, rot = self.get_anchor_pos_rot(anchor_data)
            model = world.model(MODEL_PATH, None)
            self.add_model(model)
            model.scale = math3d.vector(0.0005, 0.0005, 0.0005)
            model.position = math3d.vector(pos)
            model.rotation_matrix = rot
            self.model_dict[anchor_data.identifier] = model
        return

    def on_anchor_updated_cb(self, session, anchor_data):
        if self.on_anchor_updated_cb_log:
            self.log('on_anchor_updated_cb: %s, %s, %s, %s', anchor_data.identifier, anchor_data.type, anchor_data.alignment, anchor_data.is_valid)
            self.log('on_anchor_updated_cb.extent: %s', anchor_data.extent)
            if self.start_time > 0:
                cur_time = time.time()
                pass_time = cur_time - self.start_time
                self.start_time = 0
                self.log('test--on_anchor_updated_cb--step1--pass_time =%s', pass_time)
        if anchor_data.type == ar.ANCHOR_PLANE:
            if anchor_data.identifier not in self.plane_dict:
                return
            pos, rot = self.get_plane_pos_rot(anchor_data)
            plane, edge_point_list = self.plane_dict[anchor_data.identifier]
            plane.position = pos
            if self.ar_type == ar.AR_ARCORE:
                plane.rotation_matrix = rot
            elif self.ar_type == ar.AR_ARKIT:
                plane.rotation_matrix = rot
            w = anchor_data.extent[0] * AR_TO_GAME_SCALE
            h = anchor_data.extent[2] * AR_TO_GAME_SCALE
            vertex = [
             (
              -0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
             (
              -0.5 * w, 0, 0.5 * h, 4294901760L, 0, 0),
             (
              0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
             (
              0.5 * w, 0, -0.5 * h, 4278255360L, 0, 0),
             (
              -0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0),
             (
              0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0)]
            for i, v in enumerate(vertex):
                plane.set_vert(i, v[0], v[1], v[2], v[3], v[4], v[5])

            edge_point_list = self.make_plane_edge_points(w, h)
            self.plane_dict[anchor_data.identifier] = (plane, edge_point_list)
            self.log('[==TEST==] Plane Updated: %s, %s', pos, rot)
        if anchor_data.type == ar.ANCHOR_MARKER_2D:
            if anchor_data.identifier not in self.model_dict:
                return
            pos, rot = self.get_anchor_pos_rot(anchor_data)
            pos = self.round_model_pos(pos)
            model = self.model_dict[anchor_data.identifier]
            model.position = pos
            model.rotation_matrix = rot

    def on_anchor_removed_cb(self, session, anchor_data):
        self.log('test--on_anchor_removed_cb--step1: %s', anchor_data.identifier)
        if anchor_data.type == ar.ANCHOR_PLANE:
            if anchor_data.identifier not in self.plane_dict:
                return
            plane_info = self.plane_dict.pop(anchor_data.identifier, None)
            plane, edge_point_list = plane_info
            self.remove_object(plane)
        if anchor_data.type == ar.ANCHOR_MARKER_2D:
            if anchor_data.identifier not in self.model_dict:
                return
            model = self.model_dict.pop(anchor_data.identifier, None)
            self.del_model(model)
        return

    def on_face_cb(self, session, status, count, faces):
        pass

    def on_gesture_cb(self, session, status, count, gestures):
        pass

    def on_save_map_cb(self, session, result, path):
        self.log('on_save_map_cb: %s %s', result, path)

    def on_load_map_cb(self, session, result, path):
        self.log('on_load_map_cb: %s %s', result, path)

    def get_hittest_pos(self, anchor_data):
        if self.ar_type == ar.AR_INSIGHT:
            return math3d.vector(anchor_data.center[0], anchor_data.center[1], anchor_data.center[2]) * AR_TO_GAME_SCALE
        if self.ar_type == ar.AR_ARCORE:
            return math3d.vector(anchor_data.center[0], anchor_data.center[1], anchor_data.center[2]) * AR_TO_GAME_SCALE
        if self.ar_type == ar.AR_ARKIT:
            return math3d.vector(anchor_data.center[0], anchor_data.center[1], anchor_data.center[2]) * AR_TO_GAME_SCALE

    def get_plane_pos_rot(self, anchor_data):
        rot = math3d.rotation(anchor_data.rotation[0], anchor_data.rotation[1], anchor_data.rotation[2], anchor_data.rotation[3])
        return (
         math3d.vector(anchor_data.center[0], anchor_data.center[1], anchor_data.center[2]) * AR_TO_GAME_SCALE, math3d.rotation_to_matrix(rot))

    def get_anchor_pos_rot(self, anchor_data):
        rot = math3d.rotation(anchor_data.rotation[0], anchor_data.rotation[1], anchor_data.rotation[2], anchor_data.rotation[3])
        return (
         math3d.vector(anchor_data.center[0], anchor_data.center[1], anchor_data.center[2]) * AR_TO_GAME_SCALE, math3d.rotation_to_matrix(rot))

    def get_pose_pos_rot(self, pose, cam_mtx):
        quaternion = pose[:4]
        position = pose[4:]
        pos = math3d.vector(*position)
        rot = math3d.rotation(*quaternion)
        matrix = math3d.rotation_to_matrix(rot)
        matrix.translation = pos
        matrix = matrix * cam_mtx
        return (
         matrix.translation, matrix.rotation)

    def make_model(self):
        pass

    def make_plane(self, w, h):
        plane = world.primitives(self.scene)
        vetex = [
         (
          (
           -0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0),
          (
           -0.5 * w, 0, 0.5 * h, 4294901760L, 0, 0),
          (
           0.5 * w, 0, -0.5 * h, 4294901760L, 0, 0)),
         (
          (
           0.5 * w, 0, -0.5 * h, 4278255360L, 0, 0),
          (
           -0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0),
          (
           0.5 * w, 0, 0.5 * h, 4278255360L, 0, 0))]
        plane.create_poly3(vetex)
        plane.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        plane.visible = False
        return plane

    def make_coord_axis(self):
        coord = world.primitives(self.scene)
        vertex = [
         (
          (0, 0, 0, 4294901760L, 0, 0),
          (1.0, 0, 0, 4294901760L, 0, 0)),
         (
          (0, 0, 0, 4278255360L, 0, 0),
          (0, 1.0, 0, 4278255360L, 0, 0)),
         (
          (0, 0, 0, 4278190335L, 0, 0),
          (0, 0, 1.0, 4278190335L, 0, 0))]
        coord.create_line(vertex)
        coord.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        return coord

    def make_point_coord(self):
        coord = world.primitives(self.scene)
        vertex = [
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (1.0, 0, 0, 4278190080L, 0, 0)),
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (0, 1.0, 0, 4278190080L, 0, 0)),
         (
          (0, 0, 0, 4278190080L, 0, 0),
          (0, 0, 1.0, 4278190080L, 0, 0))]
        coord.create_line(vertex)
        coord.set_texture(0, render.texture(BACKGROUND_UI_PATH))
        coord.scale = math3d.vector(0.01, 0.01, 0.01)
        coord.visible = False
        return coord

    def _on_click_btn_back(self, *args):
        self.log('test--_on_click_btn_back')
        self.close()

    def on_click_hide(self, *args):
        self.panel.nd_content.setVisible(False)

    def on_click_set(self, *args):
        self.panel.nd_set_pnl.setVisible(not self.panel.nd_set_pnl.isVisible())

    def on_click_set_shadow_visible(self, *args):
        self._is_shadow_visible = not self._is_shadow_visible
        self.panel.btn_choose.SetSelect(not self._is_shadow_visible)
        for one_model in self.shadow_model_list:
            if one_model:
                one_model.visible = self._is_shadow_visible

    def on_click_base_layer(self, obj, touch):
        self.log('test--on_click_base_layer--step1--nd_content.isVisible =', self.panel.nd_content.isVisible())
        if self.panel.nd_content.isVisible():
            return
        self.panel.nd_content.setVisible(True)

    def _on_rotate_drag_begin(self, layer, touch):
        if len(self._nd_touch_IDs) >= 2:
            self.log('test--_on_rotate_drag_begin--step1--len(_nd_touch_IDs) =', len(self._nd_touch_IDs))
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        self.log('test--_on_rotate_drag_begin--touch_wpos =', touch_wpos, '--touch_wpos.x =', touch_wpos.x, '--len(self._nd_touch_IDs) =', len(self._nd_touch_IDs))
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            pts = six_ex.values(self._nd_touch_poses)
            self._double_touch_prev_len = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        is_select = len(self._nd_touch_IDs) <= 1
        self.log('test--_on_rotate_drag_begin--step2')
        self.check_hit_ar_plane(layer, touch, is_select=is_select)
        return True

    def reset_rotate_model(self, index):
        self.cur_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self.target_euler_rot_list[index] = math3d.vector(0, 0, 0)

    def rotate_model(self, index, rotate_times):
        target_euler_rot = self.target_euler_rot_list[index]
        self.target_euler_rot_list[index] = math3d.vector(0, target_euler_rot.y + rotate_times * math.pi * 2, 0)
        self.log('test--rotate_model--index =', index)

    def _on_btn_scene_ui_drag(self, layer, touch):
        self.on_move_btn_scene_ui(layer, touch)
        self._is_drag_model = True

    def _on_rotate_drag--- This code section failed: ---

2766       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'get_mecha_num'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  ''
          12  COMPARE_OP            1  '<='
          15  POP_JUMP_IF_FALSE    44  'to 44'

2767      18  LOAD_FAST             0  'self'
          21  LOAD_ATTR             1  'log'
          24  LOAD_CONST            2  'test--_on_rotate_drag--step1--get_mecha_num ='
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             0  'get_mecha_num'
          33  CALL_FUNCTION_0       0 
          36  CALL_FUNCTION_2       2 
          39  POP_TOP          

2768      40  LOAD_CONST            0  ''
          43  RETURN_END_IF    
        44_0  COME_FROM                '15'

2770      44  LOAD_GLOBAL           2  'game3d'
          47  LOAD_ATTR             3  'get_platform'
          50  CALL_FUNCTION_0       0 
          53  LOAD_GLOBAL           4  'TEST_PLATFORM'
          56  COMPARE_OP            2  '=='
          59  POP_JUMP_IF_FALSE   121  'to 121'

2771      62  LOAD_FAST             2  'touch'
          65  LOAD_ATTR             5  'getDelta'
          68  CALL_FUNCTION_0       0 
          71  STORE_FAST            3  'delta_pos'

2772      74  LOAD_CONST            1  ''
          77  STORE_FAST            4  'model_index'

2773      80  LOAD_FAST             0  'self'
          83  LOAD_ATTR             6  'rotate_model'
          86  LOAD_FAST             4  'model_index'
          89  LOAD_FAST             3  'delta_pos'
          92  LOAD_ATTR             7  'x'
          95  UNARY_NEGATIVE   
          96  LOAD_GLOBAL           8  'ROTATE_FACTOR'
          99  BINARY_DIVIDE    
         100  CALL_FUNCTION_2       2 
         103  POP_TOP          

2774     104  LOAD_FAST             0  'self'
         107  LOAD_ATTR             1  'log'
         110  LOAD_CONST            3  'test--_on_rotate_drag--step2'
         113  CALL_FUNCTION_1       1 
         116  POP_TOP          

2775     117  LOAD_CONST            0  ''
         120  RETURN_END_IF    
       121_0  COME_FROM                '59'

2778     121  LOAD_FAST             2  'touch'
         124  LOAD_ATTR             9  'getId'
         127  CALL_FUNCTION_0       0 
         130  STORE_FAST            5  'tid'

2779     133  LOAD_FAST             2  'touch'
         136  LOAD_ATTR            10  'getLocation'
         139  CALL_FUNCTION_0       0 
         142  STORE_FAST            6  'touch_wpos'

2780     145  LOAD_FAST             5  'tid'
         148  LOAD_FAST             0  'self'
         151  LOAD_ATTR            11  '_nd_touch_IDs'
         154  COMPARE_OP            7  'not-in'
         157  POP_JUMP_IF_FALSE   164  'to 164'

2781     160  LOAD_CONST            0  ''
         163  RETURN_END_IF    
       164_0  COME_FROM                '157'

2783     164  LOAD_FAST             0  'self'
         167  LOAD_ATTR            12  'check_hit_ar_plane'
         170  LOAD_FAST             1  'layer'
         173  LOAD_FAST             2  'touch'
         176  CALL_FUNCTION_2       2 
         179  POP_TOP          

2785     180  LOAD_FAST             0  'self'
         183  LOAD_ATTR            13  '_select_model_index'
         186  STORE_FAST            4  'model_index'

2786     189  LOAD_FAST             0  'self'
         192  LOAD_ATTR             1  'log'
         195  LOAD_CONST            4  'test--_on_rotate_drag--step1--len(_nd_touch_IDs) ='
         198  LOAD_GLOBAL          14  'len'
         201  LOAD_FAST             0  'self'
         204  LOAD_ATTR            11  '_nd_touch_IDs'
         207  CALL_FUNCTION_1       1 
         210  CALL_FUNCTION_2       2 
         213  POP_TOP          

2787     214  LOAD_FAST             4  'model_index'
         217  LOAD_CONST            1  ''
         220  COMPARE_OP            0  '<'
         223  POP_JUMP_IF_FALSE   230  'to 230'

2788     226  LOAD_CONST            0  ''
         229  RETURN_END_IF    
       230_0  COME_FROM                '223'

2789     230  LOAD_GLOBAL          14  'len'
         233  LOAD_FAST             0  'self'
         236  LOAD_ATTR            11  '_nd_touch_IDs'
         239  CALL_FUNCTION_1       1 
         242  LOAD_CONST            5  1
         245  COMPARE_OP            2  '=='
         248  POP_JUMP_IF_FALSE   290  'to 290'

2790     251  LOAD_FAST             2  'touch'
         254  LOAD_ATTR             5  'getDelta'
         257  CALL_FUNCTION_0       0 
         260  STORE_FAST            3  'delta_pos'

2792     263  LOAD_FAST             0  'self'
         266  LOAD_ATTR             6  'rotate_model'
         269  LOAD_FAST             4  'model_index'
         272  LOAD_FAST             3  'delta_pos'
         275  LOAD_ATTR             7  'x'
         278  UNARY_NEGATIVE   
         279  LOAD_GLOBAL           8  'ROTATE_FACTOR'
         282  BINARY_DIVIDE    
         283  CALL_FUNCTION_2       2 
         286  POP_TOP          
         287  JUMP_FORWARD        386  'to 676'

2794     290  LOAD_GLOBAL          14  'len'
         293  LOAD_FAST             0  'self'
         296  LOAD_ATTR            11  '_nd_touch_IDs'
         299  CALL_FUNCTION_1       1 
         302  LOAD_CONST            6  2
         305  COMPARE_OP            5  '>='
         308  POP_JUMP_IF_FALSE   676  'to 676'

2795     311  LOAD_CONST            0  ''
         314  RETURN_VALUE     

2796     315  LOAD_FAST             6  'touch_wpos'
         318  LOAD_FAST             0  'self'
         321  LOAD_ATTR            15  '_nd_touch_poses'
         324  LOAD_FAST             5  'tid'
         327  STORE_SUBSCR     

2797     328  LOAD_GLOBAL          16  'six_ex'
         331  LOAD_ATTR            17  'values'
         334  LOAD_FAST             0  'self'
         337  LOAD_ATTR            15  '_nd_touch_poses'
         340  CALL_FUNCTION_1       1 
         343  STORE_FAST            7  'pts'

2798     346  LOAD_GLOBAL          18  'cc'
         349  LOAD_ATTR            19  'Vec2'
         352  LOAD_FAST             7  'pts'
         355  LOAD_CONST            1  ''
         358  BINARY_SUBSCR    
         359  CALL_FUNCTION_1       1 
         362  STORE_FAST            8  'vec'

2799     365  LOAD_FAST             8  'vec'
         368  LOAD_ATTR            20  'subtract'
         371  LOAD_FAST             7  'pts'
         374  LOAD_CONST            5  1
         377  BINARY_SUBSCR    
         378  CALL_FUNCTION_1       1 
         381  POP_TOP          

2800     382  LOAD_FAST             8  'vec'
         385  LOAD_ATTR            21  'getLength'
         388  CALL_FUNCTION_0       0 
         391  STORE_FAST            9  'cur_dist'

2802     394  LOAD_FAST             9  'cur_dist'
         397  LOAD_FAST             0  'self'
         400  LOAD_ATTR            22  '_double_touch_prev_len'
         403  BINARY_SUBTRACT  
         404  STORE_FAST           10  'delta'

2803     407  LOAD_FAST            10  'delta'
         410  STORE_FAST           11  'init_delta'

2804     413  LOAD_FAST             9  'cur_dist'
         416  LOAD_FAST             0  'self'
         419  STORE_ATTR           22  '_double_touch_prev_len'

2806     422  LOAD_FAST            10  'delta'
         425  LOAD_FAST             0  'self'
         428  LOAD_ATTR            23  'MODEL_SCALE_TOUCH_SEN_FACTOR'
         431  BINARY_DIVIDE    
         432  STORE_FAST           10  'delta'

2807     435  LOAD_FAST             0  'self'
         438  LOAD_ATTR            24  '_cur_scale_list'
         441  LOAD_FAST             4  'model_index'
         444  BINARY_SUBSCR    
         445  LOAD_FAST            10  'delta'
         448  BINARY_ADD       
         449  LOAD_FAST             0  'self'
         452  LOAD_ATTR            24  '_cur_scale_list'
         455  LOAD_FAST             4  'model_index'
         458  STORE_SUBSCR     

2808     459  LOAD_GLOBAL          25  'max'
         462  LOAD_FAST             0  'self'
         465  LOAD_ATTR            24  '_cur_scale_list'
         468  LOAD_FAST             4  'model_index'
         471  BINARY_SUBSCR    
         472  LOAD_FAST             0  'self'
         475  LOAD_ATTR            26  '_min_scale_list'
         478  LOAD_FAST             4  'model_index'
         481  BINARY_SUBSCR    
         482  CALL_FUNCTION_2       2 
         485  LOAD_FAST             0  'self'
         488  LOAD_ATTR            24  '_cur_scale_list'
         491  LOAD_FAST             4  'model_index'
         494  STORE_SUBSCR     

2809     495  LOAD_GLOBAL          27  'min'
         498  LOAD_FAST             0  'self'
         501  LOAD_ATTR            24  '_cur_scale_list'
         504  LOAD_FAST             4  'model_index'
         507  BINARY_SUBSCR    
         508  LOAD_FAST             0  'self'
         511  LOAD_ATTR            28  '_max_scale_list'
         514  LOAD_FAST             4  'model_index'
         517  BINARY_SUBSCR    
         518  CALL_FUNCTION_2       2 
         521  LOAD_FAST             0  'self'
         524  LOAD_ATTR            24  '_cur_scale_list'
         527  LOAD_FAST             4  'model_index'
         530  STORE_SUBSCR     

2810     531  LOAD_FAST             0  'self'
         534  LOAD_ATTR             1  'log'
         537  LOAD_CONST            7  'test--_on_rotate_drag--step2--model_index ='
         540  LOAD_FAST             0  'self'
         543  LOAD_ATTR            13  '_select_model_index'
         546  LOAD_CONST            8  '--delta ='
         549  LOAD_FAST            10  'delta'
         552  LOAD_CONST            9  '--init_delta ='
         555  LOAD_FAST            11  'init_delta'
         558  LOAD_CONST           10  '--MODEL_SCALE_TOUCH_SEN_FACTOR ='
         561  LOAD_FAST             0  'self'
         564  LOAD_ATTR            23  'MODEL_SCALE_TOUCH_SEN_FACTOR'
         567  LOAD_CONST           11  '--_cur_scale ='
         570  LOAD_FAST             0  'self'
         573  LOAD_ATTR            24  '_cur_scale_list'
         576  LOAD_FAST             4  'model_index'
         579  BINARY_SUBSCR    
         580  LOAD_CONST           12  '--max_scale ='
         583  LOAD_FAST             0  'self'
         586  LOAD_ATTR            28  '_max_scale_list'
         589  LOAD_FAST             4  'model_index'
         592  BINARY_SUBSCR    
         593  CALL_FUNCTION_12     12 
         596  POP_TOP          

2811     597  LOAD_FAST             0  'self'
         600  LOAD_ATTR            29  'hit_model_list'
         603  LOAD_FAST             4  'model_index'
         606  BINARY_SUBSCR    
         607  STORE_FAST           12  'hit_model'

2812     610  LOAD_FAST            12  'hit_model'
         613  POP_JUMP_IF_FALSE   676  'to 676'
         616  LOAD_FAST            12  'hit_model'
         619  LOAD_ATTR            30  'valid'
       622_0  COME_FROM                '613'
         622  POP_JUMP_IF_FALSE   676  'to 676'

2813     625  LOAD_GLOBAL          31  'math3d'
         628  LOAD_ATTR            32  'vector'
         631  LOAD_FAST             0  'self'
         634  LOAD_ATTR            24  '_cur_scale_list'
         637  LOAD_FAST             4  'model_index'
         640  BINARY_SUBSCR    
         641  LOAD_FAST             0  'self'
         644  LOAD_ATTR            24  '_cur_scale_list'
         647  LOAD_FAST             4  'model_index'
         650  BINARY_SUBSCR    
         651  LOAD_FAST             0  'self'
         654  LOAD_ATTR            24  '_cur_scale_list'
         657  LOAD_FAST             4  'model_index'
         660  BINARY_SUBSCR    
         661  CALL_FUNCTION_3       3 
         664  LOAD_FAST            12  'hit_model'
         667  STORE_ATTR           33  'scale'
         670  JUMP_ABSOLUTE       676  'to 676'
         673  JUMP_FORWARD          0  'to 676'
       676_0  COME_FROM                '673'
       676_1  COME_FROM                '287'

Parse error at or near `LOAD_GLOBAL' instruction at offset 328

    def _on_btn_scene_ui_drag_end(self, layer, touch):
        self.on_move_btn_scene_ui(layer, touch)
        self.update_model_arrow_pos()
        self._is_drag_model = False
        self._mecha_drag_pos_list[self._select_model_index] = None
        return

    def on_move_btn_scene_ui(self, layer, touch):
        if self.get_mecha_num() <= 0:
            return
        else:
            if not self.session:
                return
            model = self.hit_model_list[self._select_model_index]
            if not model:
                return
            location = touch.getLocation()
            self.panel.btn_scene_ui.setPosition(location)
            ar_pos = self.convert_touch_location_to_ar_pos(location)
            if not ar_pos:
                return
            x, z = ar_pos
            anchor_data = self.session.get_hit_test_result(x, z)
            if anchor_data is None:
                self.log('test--on_move_btn_scene_ui--step1')
                return
            pos = self.get_hittest_pos(anchor_data)
            if not pos:
                self.log('test--on_move_btn_scene_ui--step2--pos =', pos)
                return
            last_pos = self._mecha_drag_pos_list[self._select_model_index]
            self._mecha_drag_pos_list[self._select_model_index] = pos
            if not last_pos:
                return
            diff_vec = pos - last_pos
            position = model.position
            new_position = position + diff_vec
            self.log('test--on_move_btn_scene_ui--step3--location =', location, '--ar_pos =', ar_pos, '--diff_vec.length =', diff_vec.length, '--new_position =', pos, '--old_position =', position)
            model.position = pos
            return

    def _on_rotate_drag_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]
        self.check_hit_ar_plane(layer, touch, is_end_touch=True)

    def convert_touch_location_to_ar_pos(self, location):
        neox_x, neox_y = cocos_utils.cocos_pos_to_neox(location.x, location.y)
        bg_layer = self.get_layer()
        location = bg_layer.convertToNodeSpace(location)
        x = location.x
        z = location.y
        self.log('test--convert_touch_location_to_ar_pos--step1--location =', location, '--neox_x =', neox_x, '--neox_y =', neox_y)
        if x < 0 or z < 0 or x > self.rt_width or z > self.rt_height:
            return
        z = self.ar_height - (z + abs(self.ar_height - self.rt_height) / 2)
        x = x + abs(self.ar_width - self.rt_width) / 2
        self.log('test--Touch Ended: x: %s, z: %s', x, z)
        x /= self.ar_width
        z /= self.ar_height
        scale = bg_layer.getScale()
        if scale > 1:
            x *= scale
            z *= scale
        x = min(x, 1)
        z = min(z, 1)
        return (
         x, z)

    def check_hit_ar_plane(self, layer, touch, is_select=False, is_end_touch=False, is_update_pos=False):
        if self.session is None or not self.background_model:
            return True
        else:
            location = touch.getLocation()
            ar_pos = self.convert_touch_location_to_ar_pos(location)
            if not ar_pos:
                return
            x, z = ar_pos
            neox_x, neox_y = cocos_utils.cocos_pos_to_neox(location.x, location.y)
            self.log('test--check_hit_ar_plane--step1--is_select =', is_select, '--_default_mecha_info =', self._default_mecha_info, '--get_mecha_num =', self.get_mecha_num(), '--len(_nd_touch_IDs) =', len(self._nd_touch_IDs), '--hit_model_list =', self.hit_model_list)
            if is_select:
                if self.get_mecha_num() <= 0:
                    self._select_model_index = 0
                else:
                    pick_result = self.scene.pick(neox_x, neox_y)
                    select_model_index = -1
                    self.log('test--check_hit_ar_plane--step2--neox_x =', neox_x, '--neox_y =', neox_y, '--pick_result =', pick_result)
                    if pick_result and pick_result[0]:
                        pick_model = pick_result[0]
                        self.log('test--check_hit_ar_plane--step3--pick_model =', pick_model, '--hit_model_list =', self.hit_model_list)
                        for index, one_model in enumerate(self.hit_model_list):
                            if one_model == pick_model:
                                select_model_index = index
                                break

                    if select_model_index < 0 and self.panel.btn_scene_ui.isVisible():
                        pass
                    else:
                        self._select_model_index = select_model_index
                    self.log('test--check_hit_ar_plane--step1--_select_model_index =', self._select_model_index, '--hit_pos =', (neox_x, neox_y), '--model.world_position =', self.hit_model_list[0] and self.hit_model_list[0].world_position or None)
                    if self._select_model_index >= 0:
                        self.panel.btn_scene_ui.setVisible(True)
                        self.panel.nd_slider.setVisible(True)
            have_no_mecha = self.get_mecha_num() <= 0
            self.log('test--check_hit_ar_plane--step2--have_no_mecha =', have_no_mecha, '--is_update_pos =', is_update_pos)
            if (have_no_mecha or is_update_pos) and self._select_model_index >= 0:
                self.hit_test(x, z, is_select, is_end_touch, neox_x, neox_y)
            if is_select or have_no_mecha:
                self.log('test--check_hit_ar_plane--step3--is_select =', is_select, '--have_no_mecha =', have_no_mecha)
                self.update_model_arrow_pos()
                self.update_slider_percent()
            return

    def update_model_arrow_pos(self):
        model = self.hit_model_list[self._select_model_index]
        if not model or not model.valid:
            return
        neox_2d_pos = self.scene.active_camera.world_to_screen(model.position)
        cocos_2d_pos = cocos_utils.neox_pos_to_cocos(*neox_2d_pos)
        self.panel.btn_scene_ui.setPosition(*cocos_2d_pos)

    def update(self, *args):
        for index, hit_model in enumerate(self.hit_model_list):
            if hit_model and hit_model.valid:
                cur_euler_rot = self.cur_euler_rot_list[index]
                cur_euler_rot.intrp(cur_euler_rot, self.target_euler_rot_list[index], 0.2)
                self.cur_euler_rot_list[index] = cur_euler_rot
                hit_model.world_rotation_matrix = math3d.euler_to_matrix(cur_euler_rot)
                if index == 0:
                    self.log('test--update--index =', index, '--cur_euler_rot =', cur_euler_rot, '--target_euler_rot =', self.target_euler_rot_list[index], '--hit_model.position =', hit_model.position, '--hit_model.scale =', hit_model.scale, '--hit_model.filename =', hit_model.filename)

        if self.panel.btn_scene_ui.isVisible() and not self._nd_touch_IDs and not self._is_drag_model:
            self.update_model_arrow_pos()

    def get_point_cloud_pos(self, points, i):
        return math3d.vector(points[i * 3], points[i * 3 + 1], points[i * 3 + 2])

    def on_key_msg(self, msg, key_code):
        pass

    def log(self, *args):
        if not global_data.print_ar_log:
            return
        msg = [
         '[NxAR-Python]']
        for elem in args:
            msg.append(str(elem))

        print(' '.join(msg))
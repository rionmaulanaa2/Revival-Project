# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/ar/MechaARMainUI.py
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
from cocosui import cc, ccui
try:
    import ar
except:
    pass

import C_file
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
from common.const.uiconst import UI_TYPE_MESSAGE
import common.utils.timer as timer
from common.framework import Functor
from logic.gutils.template_utils import init_common_choose_list
import copy
import time
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
import math
from logic.gutils import mecha_utils
from logic.gutils import item_utils
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
import logic.gutils.dress_utils as dress_utils
from logic.gutils import lobby_model_display_utils
from common.utils.redpoint_check_func import check_mecha_component_page_has_empty_slot, check_inscription_module_red_point
from logic.gutils import red_point_utils
from logic.gutils import mecha_skin_utils
import common.utils.cocos_utils as cocos_utils
from common.const.uiconst import UI_VKB_CLOSE
import logic.comsys.effect.ui_effect as ui_effect
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data, load_model_decal_high_quality
import math
from logic.vscene import scene
from common.uisys.render_target import RenderTargetHolder
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
import common.const.cocos_constant as cocos_constant
from common.const.neox_cocos_constant import COCOMATE_BLEND_2_HAL_BLEND_FACTOR, BLENDOP_ADD, BLEND_ONE, BLEND_INVSRCALPHA
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import mecha_skin_utils
import logic.gutils.role_head_utils as role_head_utils
from common.utils.cocos_utils import ccp
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
CAM_RT_CONF = {'scn_bg_color': 0,
   'cam_fov': 60.0,
   'rt_width': RT_WIDTH,
   'rt_height': RT_HEIGHT,
   'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
   'cam_pos': math3d.vector(0, 0, 0)
   }
MODEL_PATH = 'character/11/2000/l.gim'
BACKGROUND_UI_PATH = 'gui/ui_res_2/ar/bg.png'
GESTURES = ('FIST', 'THUMB', 'INDEX', 'LSHAPE', 'VSHAPE', 'OK', 'PALM', 'HEART', 'ROCK',
            'DHEART')
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
MAX_TRY_PERMISSION_TIMES = 5
SHOW_ACTION_DETAIL = 0
HIDE_ACTION_DETAIL = 1
FULL_SCREEN_WIDTH_HEIGHT_SCALE = 1.35
IGNORE_MECHA_IDS = [
 8023]

class MechaARMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_ar'
    IS_FULLSCREEN = False
    MODEL_SCALE_TOUCH_SEN_FACTOR = 5000
    UI_VKB_TYPE = UI_VKB_CLOSE
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    BG_CONFIG_NAME = 'mech_display/bg_mech_ar'
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

    def test_draw_model(self):
        if game3d.get_platform() != TEST_PLATFORM:
            return
        else:
            self.scene_rt = None
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
            self.panel.nd_screen_shot.setVisible(True)
            self.panel.btn_set.setVisible(True)
            sz = self.get_scene_rt_ui().getContentSize()
            CAM_RT_CONF = {'scn_bg_color': 0,
               'cam_fov': 60.0,
               'rt_width': sz.width,
               'rt_height': sz.height,
               'cam_euler': math3d.vector(0 / 180 * math.pi, 0 / 180 * math.pi, 0 / 180 * math.pi),
               'cam_pos': math3d.vector(0, 0, 0)
               }
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
            hit_model = world.model(model_path, None)
            self.hit_model_list.append(hit_model)
            for res_path in sub_mesh_path_list:
                global_data.model_mgr.create_mesh_async(None, res_path, hit_model)

            all_lights_names = [
             'dir_light']
            self.scene_rt = RenderTargetHolder(None, self.get_scene_rt_ui(), CAM_RT_CONF, True, all_lights_names)
            self.scene_rt.scn.set_macros({'AR_MECHA': '1'})
            self.scene_rt.camera.z_range = (1, 20000)
            self.scene_rt.scn.enable_vlm = True
            self.scene_rt.scn.load_env_new('scene/scene_env_confs/default_nx2_mobile.xml')
            self.scene_rt.apply_conf('ar_mecha')
            self.scene_rt.scn.background_color = 0
            self.scene_rt.start_render_target()
            scene_rt_ui = self.get_scene_rt_ui()
            if hasattr(scene_rt_ui, 'setBlendState'):
                scene_rt_ui.setBlendState(True, COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_ONE), COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_INVSRCALPHA), BLENDOP_ADD)
            self.scene_rt.add_model(hit_model)
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
            self.scene_rt.camera.aspect = old_camera.aspect
            self.scene_rt.camera.fov = old_camera.fov
            self.scene_rt.camera.z_range = old_camera.z_range
            self.scene_rt.camera.transformation = old_camera.transformation
            self.scene_rt.camera.projection_matrix = old_camera.projection_matrix
            self.scene_rt.camera.look_at = old_camera.look_at
            light = self.scene_rt.get_light()
            old_parent = light.get_parent()
            src_light = active_scene.get_light(all_lights_names[0])
            light.world_rotation_matrix = src_light.world_rotation_matrix
            part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
            model_list = part_md.get_cur_model_list()
            ref_model = model_list[0].get_model()
            ref_pos = ref_model.position
            ref_scale = ref_model.scale
            ref_world_rotation_matrix = ref_model.world_rotation_matrix
            ref_pos.x = ref_pos.x - 10
            hit_model.position = ref_pos
            hit_model.scale = ref_scale
            hit_model.world_rotation_matrix = ref_world_rotation_matrix
            anim_name = ref_model.cur_anim_name
            hit_model.play_animation(anim_name)
            print(('test--test_draw_model--step1--ref_scale =', ref_scale, '--model_path =', model_path, '--submesh_path =', submesh_path))
            forward = -self.scene_rt.camera.world_rotation_matrix.forward
            yaw = forward.yaw
            mat = math3d.matrix.make_rotation_y(yaw)
            sfx_path = 'effect/fx/robot/robot_01/robot01_call_03.sfx'
            self.init_event()
            self.init_light_slider_value()

            def test_model():
                print(('test--hit_model.anim_time =', hit_model.anim_time, '--max_anim_time =', anim_time, '--is_playing =', hit_model.is_playing, '--is_anim_at_end =', hit_model.is_anim_at_end))

            return

    def test_error_sfx(self):
        sfx_path = 'effect/fx/mecha/8012/8012_ar.sfx'
        model = self.hit_model_list[0]
        socket = 'fx_penhuokou_ar'
        print(('test--test_error_sfx--step1--len(hit_model_list)', len(self.hit_model_list)))
        print(('test--test_error_sfx--step2--sfx_path =', sfx_path, '--socket =', socket, '--model.filename =', model.filename))
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
        light = self.scene_rt.get_light()
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
        percent = pitch / MAX_ROTATE_RADIAN
        percent = min(percent, 1)
        percent = max(percent, 0)
        light_item_4.slider.setPercent(percent * 100)

    def create_error_display_sfx_callback(self, sfx, *args):
        print(('test--create_error_display_sfx_callback--sfx.filename =', sfx.filename))

        def test_error_sfx_warn():
            print(('test--test_error_sfx_warn--cur_time =', sfx.cur_time))
            import traceback
            traceback.print_stack()

    def test_camera(self, position=None, scale=None, anim_name=None):
        part_md = global_data.game_mgr.scene.get_com('PartModelDisplay')
        model_list = part_md.get_cur_model_list()
        ref_model = model_list[0].get_model()
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
        print(('test--test_camera--step1--ref_pos =', ref_pos, '--ref_scale =', ref_scale, '--ref_model.scale =', ref_model.scale))
        mecha_skin_utils.clear_specific_skin_anim_model_and_effect(hit_model, hit_model.cur_anim_name)
        mecha_skin_utils.check_exit_anim_refresh_socket_res_appearance(hit_model, hit_model.cur_anim_name, directly_refresh=True)
        if anim_name:
            hit_model.play_animation(anim_name)
            mecha_skin_utils.check_enter_anim_refresh_socket_res_appearance(hit_model, anim_name, directly_refresh=True)

    def on_init_panel(self, *args, **kargs):
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
        self.cc_sprite = None
        self.action_conf = copy.deepcopy(confmgr.get('skin_define_action'))
        self.no_action_tag = True
        self.on_frame_cb_log = 1
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
            self.get_scene_rt_ui().setOpacity(0)
            self.get_scene_rt_ui().setLocalZOrder(100)
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
        panel = self.get_bg_panel().panel
        if not panel:
            return
        return panel.layer

    def get_scene_rt_ui(self):
        return self.get_bg_panel().panel.scene_rt

    def on_finalize_panel(self):
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        self._mecha_conf = None
        self.show_main_ui()
        self.process_event(False)
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
        if self.session is not None:
            self.stop_ar()
        self.clear_model()
        if self.scene_rt:
            self.scene_rt.destroy()
            self.scene_rt = None
        self.clear_enter_display_sfx()
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
            if not one_config:
                continue
            action_list.append(one_config)

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
                if not is_have_item:
                    one_action_option['icon'] = 'gui/ui_res_2/mech_display/icon_ar_lock.png'
                action_option.append(one_action_option)

            call_anim = ar_item_config['call_anim']

            def call_back--- This code section failed: ---

 796       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'hit_model_list'
           6  LOAD_DEREF            1  'model_index'
           9  BINARY_SUBSCR    
          10  STORE_FAST            1  'model'

 797      13  LOAD_FAST             1  'model'
          16  POP_JUMP_IF_TRUE     23  'to 23'

 798      19  LOAD_CONST            0  ''
          22  RETURN_END_IF    
        23_0  COME_FROM                '16'

 800      23  LOAD_FAST             1  'model'
          26  LOAD_ATTR             1  'cur_anim_name'
          29  LOAD_DEREF            2  'call_anim'
          32  COMPARE_OP            2  '=='
          35  POP_JUMP_IF_FALSE    52  'to 52'
          38  LOAD_FAST             1  'model'
          41  LOAD_ATTR             2  'is_anim_at_end'
          44  UNARY_NOT        
        45_0  COME_FROM                '35'
          45  POP_JUMP_IF_FALSE    52  'to 52'

 802      48  LOAD_CONST            0  ''
          51  RETURN_END_IF    
        52_0  COME_FROM                '45'

 805      52  LOAD_DEREF            3  'action_option'
          55  LOAD_FAST             0  'index'
          58  BINARY_SUBSCR    
          59  STORE_FAST            2  'action'

 806      62  LOAD_FAST             2  'action'
          65  LOAD_ATTR             3  'get'
          68  LOAD_CONST            1  'is_have_item'
          71  LOAD_GLOBAL           4  'True'
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            3  'is_have_item'

 808      80  LOAD_FAST             3  'is_have_item'
          83  POP_JUMP_IF_TRUE    112  'to 112'

 809      86  LOAD_GLOBAL           5  'global_data'
          89  LOAD_ATTR             6  'game_mgr'
          92  LOAD_ATTR             7  'show_tip'
          95  LOAD_GLOBAL           8  'get_text_by_id'
          98  LOAD_CONST            2  906652
         101  CALL_FUNCTION_1       1 
         104  CALL_FUNCTION_1       1 
         107  POP_TOP          

 810     108  LOAD_CONST            0  ''
         111  RETURN_END_IF    
       112_0  COME_FROM                '83'

 812     112  LOAD_FAST             2  'action'
         115  LOAD_CONST            3  'anim'
         118  BINARY_SUBSCR    
         119  STORE_FAST            4  'anim'

 814     122  LOAD_FAST             2  'action'
         125  LOAD_CONST            4  'is_play_last_frame'
         128  BINARY_SUBSCR    
         129  STORE_FAST            5  'is_play_last_frame'

 815     132  LOAD_FAST             1  'model'
         135  LOAD_ATTR             9  'get_anim_length'
         138  LOAD_FAST             4  'anim'
         141  CALL_FUNCTION_1       1 
         144  STORE_FAST            6  'anim_time'

 816     147  LOAD_CONST            5  ''
         150  STORE_FAST            7  'init_time'

 817     153  LOAD_GLOBAL          10  'world'
         156  LOAD_ATTR            11  'PLAY_FLAG_LOOP'
         159  STORE_FAST            8  'loop'

 818     162  LOAD_FAST             5  'is_play_last_frame'
         165  POP_JUMP_IF_FALSE   186  'to 186'

 819     168  LOAD_FAST             6  'anim_time'
         171  STORE_FAST            7  'init_time'

 820     174  LOAD_GLOBAL          10  'world'
         177  LOAD_ATTR            12  'PLAY_FLAG_NO_LOOP'
         180  STORE_FAST            8  'loop'
         183  JUMP_FORWARD          0  'to 186'
       186_0  COME_FROM                '183'

 823     186  LOAD_GLOBAL          13  'mecha_skin_utils'
         189  LOAD_ATTR            14  'clear_specific_skin_anim_model_and_effect'
         192  LOAD_FAST             1  'model'
         195  LOAD_FAST             1  'model'
         198  LOAD_ATTR             1  'cur_anim_name'
         201  CALL_FUNCTION_2       2 
         204  POP_TOP          

 824     205  LOAD_GLOBAL          13  'mecha_skin_utils'
         208  LOAD_ATTR            15  'check_exit_anim_refresh_socket_res_appearance'
         211  LOAD_FAST             1  'model'
         214  LOAD_FAST             1  'model'
         217  LOAD_ATTR             1  'cur_anim_name'
         220  LOAD_CONST            6  'directly_refresh'
         223  LOAD_GLOBAL           4  'True'
         226  CALL_FUNCTION_258   258 
         229  POP_TOP          

 826     230  LOAD_GLOBAL          16  'print'
         233  LOAD_CONST            7  'test--call_back--step2--index ='
         236  LOAD_CONST            8  '--anim ='
         239  LOAD_FAST             4  'anim'
         242  LOAD_CONST            9  '--model.filename ='
         245  LOAD_FAST             1  'model'
         248  LOAD_ATTR            17  'filename'
         251  BUILD_TUPLE_6         6 
         254  CALL_FUNCTION_1       1 
         257  POP_TOP          

 827     258  LOAD_FAST             1  'model'
         261  LOAD_ATTR            18  'play_animation'
         264  LOAD_FAST             4  'anim'
         267  LOAD_CONST           10  -1
         270  LOAD_GLOBAL          10  'world'
         273  LOAD_ATTR            19  'TRANSIT_TYPE_DEFAULT'
         276  LOAD_FAST             7  'init_time'
         279  LOAD_FAST             8  'loop'
         282  CALL_FUNCTION_5       5 
         285  POP_TOP          

 828     286  LOAD_GLOBAL          13  'mecha_skin_utils'
         289  LOAD_ATTR            20  'check_enter_anim_refresh_socket_res_appearance'
         292  LOAD_FAST             1  'model'
         295  LOAD_FAST             4  'anim'
         298  LOAD_CONST            6  'directly_refresh'
         301  LOAD_GLOBAL           4  'True'
         304  CALL_FUNCTION_258   258 
         307  POP_TOP          

 829     308  LOAD_DEREF            0  'self'
         311  LOAD_ATTR            21  'shadow_model_list'
         314  LOAD_DEREF            1  'model_index'
         317  BINARY_SUBSCR    
         318  POP_JUMP_IF_FALSE   359  'to 359'

 830     321  LOAD_DEREF            0  'self'
         324  LOAD_ATTR            21  'shadow_model_list'
         327  LOAD_DEREF            1  'model_index'
         330  BINARY_SUBSCR    
         331  LOAD_ATTR            18  'play_animation'
         334  LOAD_FAST             4  'anim'
         337  LOAD_CONST           10  -1
         340  LOAD_GLOBAL          10  'world'
         343  LOAD_ATTR            19  'TRANSIT_TYPE_DEFAULT'
         346  LOAD_FAST             7  'init_time'
         349  LOAD_FAST             8  'loop'
         352  CALL_FUNCTION_5       5 
         355  POP_TOP          
         356  JUMP_FORWARD          0  'to 359'
       359_0  COME_FROM                '356'

 832     359  LOAD_GLOBAL          22  'getattr'
         362  LOAD_DEREF            0  'self'
         365  LOAD_ATTR            23  'panel'
         368  LOAD_CONST           11  'btn_action_'
         371  LOAD_GLOBAL          24  'str'
         374  LOAD_DEREF            1  'model_index'
         377  LOAD_CONST           12  1
         380  BINARY_ADD       
         381  CALL_FUNCTION_1       1 
         384  BINARY_ADD       
         385  LOAD_CONST            0  ''
         388  CALL_FUNCTION_3       3 
         391  STORE_FAST            9  'btn_action'

 834     394  LOAD_FAST             9  'btn_action'
         397  POP_JUMP_IF_FALSE   420  'to 420'

 835     400  LOAD_FAST             9  'btn_action'
         403  LOAD_ATTR            26  'SetText'
         406  LOAD_FAST             2  'action'
         409  LOAD_CONST           13  'name'
         412  BINARY_SUBSCR    
         413  CALL_FUNCTION_1       1 
         416  POP_TOP          
         417  JUMP_FORWARD          0  'to 420'
       420_0  COME_FROM                '417'
         420  LOAD_CONST            0  ''
         423  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 254

            def close_callback():
                self.hide_action_list(model_index)

            action_list_node = getattr(self.panel, 'actione_list_' + str(model_index + 1), None)
            if not action_list_node:
                log_error('test--init_action_list--step1--action_list_node None--model_index =', model_index)
                return
            max_height = None
            if model_index == 2:
                max_height = 191
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
        from ext_package.ext_decorator import has_skin_ext
        if not has_skin_ext():
            from logic.gutils.dress_utils import get_mecha_default_fashion
            default_skin_id = get_mecha_default_fashion(mecha_id)
            if int(skin_id) != int(default_skin_id):
                shiny_weapon_id = -1
                skin_id = default_skin_id
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
            print(('test--copy_npk_file_to_document_path--step1--is_find_file =', is_find_file, '--file_path =', file_path))
            if not is_find_file:
                for src_path, dest_path in six_ex.items(CHECK_FILE_DICT):
                    if not dest_path:
                        dest_path = src_path
                    one_src_file_path = dir_path + '/' + src_path
                    one_dest_file_path = dir_path + '/' + dest_path
                    print(('test--copy_npk_file_to_document_path--step2--one_src_file_path =', one_src_file_path, '--one_dest_file_path =', one_dest_file_path))
                    copy_res_file_to_document(one_src_file_path, one_dest_file_path)

    def setup(self):
        print('test--MechaARMainUI.setup--step1')
        self.copy_npk_file_to_document_path()
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        self.log('GL View Size: %s', view.getVisibleSize())
        designSize = view.getDesignResolutionSize()
        self.view_w = view.getVisibleSize().width
        self.view_h = view.getVisibleSize().height
        self.view_center = cc.Vec2(self.view_w / 2, self.view_h / 2)
        self.plane_dict = {}
        self.model_dict = {}
        self.cached_tex = None
        self.face_coord = None
        self.session = None
        self.ar_type = None
        self.ar_width = 0
        self.ar_height = 0
        self._ar_timer_id = None
        self.clear_model()
        self.platform = game3d.get_platform()
        self.is_support = ar.is_support_ar()
        self.log('Check AR Support: %s', self.is_support)
        self.scene_rt = None
        self.start_config(CONFIG, ASSETS)
        self._ar_timer_id = global_data.game_mgr.register_logic_timer(self.update, interval=1, times=-1, mode=timer.LOGIC)
        return

    def clear_model(self):
        for index, model in enumerate(self.hit_model_list):
            if not model:
                continue
            mecha_skin_utils.clear_skin_anim_sfx_func_cache(model)
            mecha_skin_utils.clear_skin_model_and_effect(model)
            mecha_skin_utils.unregister_socket_res_auto_refresh(model)
            self.scene_rt.del_model(model)

        self.hit_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        for model in self.shadow_model_list:
            if not model:
                continue
            self.scene_rt.del_model(model)

        self.shadow_model_list = [ None for index in range(MAX_MECHA_NUM) ]
        for task_handle in six_ex.values(self._load_lod_mesh_task_dict):
            if task_handle:
                task_handle.cancel()

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
        for plane, edge_point_list in six_ex.values(self.plane_dict):
            plane.visible = visible

    def start_config(self, config_path, asset_path):
        self.log('test--start_config--config_path =%s,--asset_path =%s', config_path, asset_path)
        self.rt_width = RT_WIDTH
        self.rt_height = RT_HEIGHT
        if self.session is not None:
            self.stop_ar()
        self.init_ar()
        return

    def check_permission_is_allowed_tick(self, *args):
        if ar.check_and_request_permission():
            self._check_permission_timer_id = None
            self._check_permission_times = 0
            self.init_ar()
            return timer.RELEASE
        else:
            if self._check_permission_times >= MAX_TRY_PERMISSION_TIMES:
                self._check_permission_timer_id = None
                self._check_permission_times = 0
                global_data.game_mgr.show_tip(get_text_by_id(609394))
                return timer.RELEASE
            self._check_permission_times += 1
            return

    def check_plane_visible_tick(self, *args):
        if not self.plane_dict:
            self._plane_visible_timer_id = None
            return timer.RELEASE
        else:
            if not self.scene_rt:
                self._plane_visible_timer_id = None
                return timer.RELEASE
            camera = self.scene_rt.camera
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
                world_transformation = plane.world_transformation
                for index, one_point in enumerate(edge_point_list):
                    world_position = one_point * world_transformation
                    x, y = camera.world_to_screen(world_position)
                    if x >= 0 and x <= screen_width and y >= 0 and y <= screen_height:
                        is_any_plane_visible = True
                        break

            if self._is_any_plane_visible != is_any_plane_visible:
                self._is_any_plane_visible = is_any_plane_visible
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
        bg_layer = self.get_layer()
        if bg_layer:
            bg_layer.removeChild(self.cc_sprite)
        self.cc_sprite = None
        if self.cached_tex:
            for tex in self.cached_tex:
                tex.release()

        self.cached_tex = None
        self.log('Clear AR Scene...')
        for one_plane_info in six.itervalues(self.plane_dict):
            plane, edge_point_list = one_plane_info
            if self.scene_rt:
                self.scene_rt.remove_object(plane)

        self._is_any_plane_visible = False
        for model in six.itervalues(self.model_dict):
            if self.scene_rt:
                self.scene_rt.del_model(model)

        self.clear_model()
        if self.scene_rt:
            self.scene_rt.destroy()
            self.scene_rt = None
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
        return convert_pos

    def hit_test(self, x, z, is_select, is_end_touch, neox_x, neox_y):
        if not self.plane_dict:
            return
        else:
            anchor_data = self.session.get_hit_test_result(x, z)
            if anchor_data is not None:
                pos = self.get_hittest_pos(anchor_data)
                pos = self.round_model_pos(pos)
                if not pos:
                    return
                if self.get_mecha_num() <= 0:
                    self._mecha_info_list[0] = self._default_mecha_info
                    self.show_model(self._select_model_index)
                model = self.hit_model_list[self._select_model_index]
                if model:
                    self.hit_model_list[self._select_model_index].position = pos
                    self.auto_scale_model(self._select_model_index)
                else:
                    self._mecha_info_list[self._select_model_index] = None
            elif self._select_model_index > 0:
                if is_select:
                    self.hit_model_list[self._select_model_index].position = self.hit_model_list[0].position
            elif self.get_mecha_num() <= 0 and is_end_touch and self._is_any_plane_visible:
                hit_world_pos, view_dir = self.scene_rt.camera.screen_to_world(neox_x, neox_y)
                nearest_pos = self.round_model_pos(hit_world_pos)
                if nearest_pos:
                    if self.get_mecha_num() <= 0:
                        self._mecha_info_list[0] = self._default_mecha_info
                    self.show_model(self._select_model_index)
                    model = self.hit_model_list[self._select_model_index]
                    print(('test--hit_test--step7--_select_model_index =', self._select_model_index, '--model =', model))
                    if model:
                        self.hit_model_list[self._select_model_index].position = nearest_pos
                        self.auto_scale_model(self._select_model_index)
                    else:
                        self._mecha_info_list[self._select_model_index] = None
            return

    def auto_scale_model(self, index):
        return
        model = self.hit_model_list[index]
        if not model or not model.valid:
            return
        camera = self.scene_rt.camera
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
                print(('test--auto_scale_model--step1--cur_scale =', cur_scale, '--bounding_box =', bounding_box))
                cur_scale -= MODEL_SCALE_STEP
                model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)
                continue
            break

        if cur_scale <= 0:
            print(('test--auto_scale_model--step2--index =', index, '--new_scale =', cur_scale))
            cur_scale = self._cur_scale_list[index]
        print(('test--auto_scale_model--step3--index =', index, '--new_scale =', cur_scale, '--old_scale =', self._cur_scale_list[index]))
        self._cur_scale_list[index] = cur_scale
        model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)

    def get_nearest_plane_point(self, hit_world_pos):
        camera = self.scene_rt.camera
        if not camera:
            return
        else:
            screen_width = global_data.really_window_size[0]
            screen_height = global_data.really_window_size[1]
            nearest_pos = None
            nearest_dist_sqr = 0
            scale = self.cc_sprite.getScale()
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
        camera_world_rotation_matrix = self.scene_rt.camera.world_rotation_matrix
        forward = camera_world_rotation_matrix.forward
        camera_world_position = self.scene_rt.camera.world_position
        model_world_position = model.world_position
        dist_vec = model_world_position - camera_world_position
        return dist_vec.dot(forward)

    def show_model(self, index):
        mecha_info = self._mecha_info_list[index]
        if not mecha_info:
            return
        else:
            mecha_id, skin_id, shiny_weapon_id = self._mecha_info_list[index]
            model_path = dress_utils.get_mecha_model_path(mecha_id, skin_id)
            submesh_path = dress_utils.get_mecha_model_h_path(mecha_id, skin_id)
            sub_mesh_path_list = [submesh_path]
            item_no = dress_utils.get_mecha_skin_item_no(mecha_id, skin_id)
            print(('test--show_model--step1--index =', index, '--mecha_id =', mecha_id, '--skin_id =', skin_id, '--shiny_weapon_id =', shiny_weapon_id, '--model_path =', model_path, '--sub_mesh_path_list =', sub_mesh_path_list))
            if self.hit_model_list[index]:
                res_path = self.hit_model_list[index].filename
                if res_path in self._load_lod_mesh_task_dict:
                    del self._load_lod_mesh_task_dict[res_path]
                mecha_skin_utils.clear_skin_anim_sfx_func_cache(self.hit_model_list[index])
                mecha_skin_utils.clear_skin_model_and_effect(self.hit_model_list[index])
                mecha_skin_utils.unregister_socket_res_auto_refresh(self.hit_model_list[index])
                self.scene_rt.del_model(self.hit_model_list[index])
                self.hit_model_list[index] = None
            hit_model = world.model(model_path, None)
            self.scene_rt.add_model(hit_model)
            mecha_skin_utils.load_skin_model_and_effect_for_ar(hit_model, skin_id, shiny_weapon_id)
            mecha_skin_utils.register_socket_res_auto_refresh(hit_model, skin_id)
            hit_model.pickable = True
            self.hit_model_list[index] = hit_model
            for res_path in sub_mesh_path_list:
                task_handle = global_data.model_mgr.create_mesh_async(None, res_path, self.hit_model_list[index], Functor(self.on_load_mesh_completed, res_path))
                self._load_lod_mesh_task_dict[res_path] = task_handle

            ar_item_config = confmgr.get('lobby_model_display_conf', 'ArItem', 'Content', str(item_no), default={})
            default_min_scale = 0.1
            default_init_scale = 0.3
            cur_scale = ar_item_config.get('model_default_scale', default_init_scale)
            self._cur_scale_list[index] = cur_scale
            self._min_scale_list[index] = ar_item_config.get('model_min_scale', default_min_scale)
            self._max_scale_list[index] = ar_item_config.get('model_max_scale', 1)
            self.reset_rotate_model(index)
            hit_model.scale = math3d.vector(cur_scale, cur_scale, cur_scale)
            hit_model.all_materials.enable_write_alpha = True
            hit_model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 1.0)
            decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(item_no)), [])
            color_dict = global_data.player.get_mecha_color().get(str(item_no), {})
            decal_lod = 0
            if decal_list:
                self.load_decal_data(hit_model, item_no, decal_list, decal_lod=decal_lod)
            if color_dict:
                self.load_color_data(hit_model, item_no, color_dict)
            self.panel.lab_place.setVisible(False)
            forward = -self.scene_rt.camera.world_rotation_matrix.forward
            yaw = forward.yaw
            mat = math3d.matrix.make_rotation_y(yaw)
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
        light = self.scene_rt.get_light()
        if not light:
            print(('test--add_panel_shadow--step2--dir_light =None--get_light_count =', self.scene_rt.scn.get_light_count()))
            import traceback
            traceback.print_stack()
            return
        else:
            height = model.world_position.y
            model_path = model.filename.replace('empty.gim', 'l3.gim')
            if self.shadow_model_list[index]:
                model = self.shadow_model_list[index]
                self.scene_rt.del_model(model)
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
        sound_name = display_enter_config.get('cSfxSoundName', '')
        self.change_model_preview_effect(model, display_enter_config['lobbyCallOutSfxPath'], sound_name)

    def test_model_preview_effect--- This code section failed: ---

1520       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'hit_model_list'
           6  POP_JUMP_IF_TRUE     13  'to 13'

1521       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

1523      13  LOAD_FAST             3  'create_sfx'
          16  POP_JUMP_IF_FALSE    32  'to 32'

1524      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             1  'test_error_sfx'
          25  CALL_FUNCTION_0       0 
          28  POP_TOP          
          29  JUMP_FORWARD          0  'to 32'
        32_0  COME_FROM                '29'

1526      32  SETUP_LOOP          180  'to 215'
          35  LOAD_GLOBAL           2  'enumerate'
          38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             0  'hit_model_list'
          44  CALL_FUNCTION_1       1 
          47  GET_ITER         
          48  FOR_ITER            163  'to 214'
          51  UNPACK_SEQUENCE_2     2 
          54  STORE_FAST            4  'index'
          57  STORE_FAST            5  'hit_model'

1527      60  LOAD_FAST             5  'hit_model'
          63  POP_JUMP_IF_FALSE    48  'to 48'
          66  LOAD_FAST             5  'hit_model'
          69  LOAD_ATTR             3  'valid'
        72_0  COME_FROM                '63'
          72  POP_JUMP_IF_FALSE    48  'to 48'

1528      75  LOAD_FAST             2  'scale'
          78  POP_JUMP_IF_FALSE   108  'to 108'

1529      81  LOAD_GLOBAL           4  'math3d'
          84  LOAD_ATTR             5  'vector'
          87  LOAD_FAST             2  'scale'
          90  LOAD_FAST             2  'scale'
          93  LOAD_FAST             2  'scale'
          96  CALL_FUNCTION_3       3 
          99  LOAD_FAST             5  'hit_model'
         102  STORE_ATTR            6  'scale'
         105  JUMP_FORWARD          0  'to 108'
       108_0  COME_FROM                '105'

1531     108  LOAD_FAST             1  'position'
         111  POP_JUMP_IF_FALSE   165  'to 165'

1532     114  LOAD_GLOBAL           7  'isinstance'
         117  LOAD_FAST             1  'position'
         120  LOAD_GLOBAL           8  'tuple'
         123  LOAD_GLOBAL           9  'list'
         126  BUILD_TUPLE_2         2 
         129  CALL_FUNCTION_2       2 
         132  POP_JUMP_IF_FALSE   153  'to 153'

1533     135  LOAD_GLOBAL           4  'math3d'
         138  LOAD_ATTR             5  'vector'
         141  LOAD_FAST             1  'position'
         144  CALL_FUNCTION_VAR_0     0 
         147  STORE_FAST            1  'position'
         150  JUMP_FORWARD          0  'to 153'
       153_0  COME_FROM                '150'

1535     153  LOAD_FAST             1  'position'
         156  LOAD_FAST             5  'hit_model'
         159  STORE_ATTR           10  'position'
         162  JUMP_FORWARD          0  'to 165'
       165_0  COME_FROM                '162'

1537     165  LOAD_GLOBAL          11  'print'
         168  LOAD_CONST            1  'test--test_model_preview_effect--step1--index ='
         171  LOAD_FAST             4  'index'
         174  LOAD_CONST            2  '--hit_model.position ='
         177  LOAD_FAST             5  'hit_model'
         180  LOAD_ATTR            10  'position'
         183  LOAD_CONST            3  '--hit_model.scale ='
         186  LOAD_FAST             5  'hit_model'
         189  LOAD_ATTR             6  'scale'
         192  LOAD_CONST            4  '--hit_model.filename ='
         195  LOAD_FAST             5  'hit_model'
         198  LOAD_ATTR            12  'filename'
         201  BUILD_TUPLE_8         8 
         204  CALL_FUNCTION_1       1 
         207  POP_TOP          
         208  JUMP_BACK            48  'to 48'
         211  JUMP_BACK            48  'to 48'
         214  POP_BLOCK        
       215_0  COME_FROM                '32'

1539     215  SETUP_LOOP          139  'to 357'
         218  LOAD_GLOBAL          13  'six'
         221  LOAD_ATTR            14  'iteritems'
         224  LOAD_GLOBAL          15  'getattr'
         227  LOAD_GLOBAL           5  'vector'
         230  BUILD_MAP_0           0 
         233  CALL_FUNCTION_3       3 
         236  CALL_FUNCTION_1       1 
         239  GET_ITER         
         240  FOR_ITER            113  'to 356'
         243  UNPACK_SEQUENCE_2     2 
         246  STORE_FAST            6  'identifier'
         249  STORE_FAST            7  'one_plane_info'

1540     252  LOAD_FAST             7  'one_plane_info'
         255  UNPACK_SEQUENCE_2     2 
         258  STORE_FAST            8  'plane'
         261  STORE_FAST            9  'edge_point_list'

1541     264  LOAD_FAST             8  'plane'
         267  LOAD_ATTR            16  'world_transformation'
         270  STORE_FAST           10  'world_transformation'

1542     273  BUILD_LIST_0          0 
         276  STORE_FAST           11  'world_edge_point_list'

1543     279  SETUP_LOOP           49  'to 331'
         282  LOAD_GLOBAL           2  'enumerate'
         285  LOAD_FAST             9  'edge_point_list'
         288  CALL_FUNCTION_1       1 
         291  GET_ITER         
         292  FOR_ITER             35  'to 330'
         295  UNPACK_SEQUENCE_2     2 
         298  STORE_FAST            4  'index'
         301  STORE_FAST           12  'one_point'

1544     304  LOAD_FAST            12  'one_point'
         307  LOAD_FAST            10  'world_transformation'
         310  BINARY_MULTIPLY  
         311  STORE_FAST           13  'world_position'

1545     314  LOAD_FAST            11  'world_edge_point_list'
         317  LOAD_ATTR            17  'append'
         320  LOAD_FAST            12  'one_point'
         323  CALL_FUNCTION_1       1 
         326  POP_TOP          
         327  JUMP_BACK           292  'to 292'
         330  POP_BLOCK        
       331_0  COME_FROM                '279'

1547     331  LOAD_GLOBAL          11  'print'
         334  LOAD_CONST            6  'test--test_model_preview_effect--step2--plane ='
         337  LOAD_FAST             8  'plane'
         340  LOAD_CONST            7  '--world_edge_point_list ='
         343  LOAD_FAST            11  'world_edge_point_list'
         346  BUILD_TUPLE_4         4 
         349  CALL_FUNCTION_1       1 
         352  POP_TOP          
         353  JUMP_BACK           240  'to 240'
         356  POP_BLOCK        
       357_0  COME_FROM                '215'

1549     357  LOAD_GLOBAL          11  'print'
         360  LOAD_CONST            8  'test--test_model_preview_effect--step3--aspect ='
         363  LOAD_FAST             0  'self'
         366  LOAD_ATTR            18  'scene_rt'
         369  LOAD_ATTR            19  'camera'
         372  LOAD_ATTR            20  'aspect'
         375  LOAD_CONST            9  '--fov ='
         378  LOAD_FAST             0  'self'
         381  LOAD_ATTR            18  'scene_rt'
         384  LOAD_ATTR            19  'camera'
         387  LOAD_ATTR            21  'fov'
         390  LOAD_CONST           10  '--z_range ='
         393  LOAD_FAST             0  'self'
         396  LOAD_ATTR            18  'scene_rt'
         399  LOAD_ATTR            19  'camera'
         402  LOAD_ATTR            22  'z_range'
         405  LOAD_CONST           11  '--look_at ='
         408  LOAD_FAST             0  'self'
         411  LOAD_ATTR            18  'scene_rt'
         414  LOAD_ATTR            19  'camera'
         417  LOAD_ATTR            23  'look_at'
         420  LOAD_CONST           12  '--transformation ='
         423  LOAD_FAST             0  'self'
         426  LOAD_ATTR            18  'scene_rt'
         429  LOAD_ATTR            19  'camera'
         432  LOAD_ATTR            24  'transformation'
         435  LOAD_CONST           13  '--projection_matrix ='
         438  LOAD_FAST             0  'self'
         441  LOAD_ATTR            18  'scene_rt'
         444  LOAD_ATTR            19  'camera'
         447  LOAD_ATTR            25  'projection_matrix'
         450  BUILD_TUPLE_12       12 
         453  CALL_FUNCTION_1       1 
         456  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 236

    def change_model_preview_effect(self, model, sfx_path, sfx_sound_name=None):
        if not model:
            return
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
        self.scene_rt.del_model(model)
        self.hit_model_list[index] = None
        model = self.shadow_model_list[index]
        if model:
            self.scene_rt.del_model(model)
            self.shadow_model_list[index] = None
        self.cur_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self.target_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self._cur_scale_list[index] = 1
        self._min_scale_list[index] = 1
        self._max_scale_list[index] = 1
        self.hide_action_list(index)
        self.hide_action_btn(index)
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
        if dressed_clothing_id is not None:
            if dressed_clothing_id in skin_list_cnf:
                skin_id = dressed_clothing_id
        mecha_index = self.get_empty_mecha_index()
        self._mecha_info_list[mecha_index] = (select_mecha_id, skin_id, 0)
        self.show_model(mecha_index)
        dest_pos = self.check_mecha_pos_valid(first_model.position, dest_pos)
        self.hit_model_list[mecha_index].position = dest_pos
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
        print('test--on_click_test')

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
            print(('test--update_slider_percent--step2--index =', index, '--denominator =', denominator, '--max_scale =', max_scale, '--min_scale =', min_scale))
            return
        percent = (cur_scale - min_scale) / denominator
        percent = min(percent, 1)
        percent = max(percent, 0)
        self.panel.nd_slider.slider.setPercent(percent * 100)

    def on_light_rotate_y_percent_change(self, percent):
        light = self.scene_rt.get_light()
        rotation_matrix = light.world_rotation_matrix
        old_yaw = rotation_matrix.yaw
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_y(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix

    def on_light_rotate_x_percent_change(self, percent):
        light = self.scene_rt.get_light()
        rotation_matrix = light.world_rotation_matrix
        old_pitch = rotation_matrix.pitch
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_x(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix

    def on_light_rotate_z_percent_change(self, percent):
        light = self.scene_rt.get_light()
        rotation_matrix = light.world_rotation_matrix
        old_roll = rotation_matrix.roll
        min_value = 0
        max_value = MAX_ROTATE_RADIAN
        cur_value = min_value + (max_value - min_value) * percent
        mat = math3d.matrix.make_rotation_z(cur_value)
        rotation_matrix.rotation = mat
        light.world_rotation_matrix = rotation_matrix
        print(('test--on_light_rotate_z_percent_change--step1--cur_value =', cur_value, '--old_roll =', old_roll, '--percent =', percent))

    def on_direct_light_intensity_percent_change(self, percent):
        min_value = 0
        max_value = MAX_DIRECT_INTENSITY
        cur_value = min_value + (max_value - min_value) * percent
        light = self.scene_rt.get_light()
        light.intensity = cur_value

    def on_indirect_light_intensity_percent_change(self, percent):
        min_value = 0
        max_value = MAX_INDIRECT_INTENSITY
        cur_value = min_value + (max_value - min_value) * percent
        light = self.scene_rt.get_light()
        self.scene_rt.scn.set_global_uniform('ToonIndirectIntensity', cur_value)

    def one_model_percent_change(self, percent):
        if self._select_model_index < 0:
            return
        index = self._select_model_index
        cur_scale = self._min_scale_list[index] + (self._max_scale_list[index] - self._min_scale_list[index]) * percent
        self._cur_scale_list[index] = cur_scale
        self._cur_scale_list[index] = max(self._cur_scale_list[index], self._min_scale_list[index])
        self._cur_scale_list[index] = min(self._cur_scale_list[index], self._max_scale_list[index])
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
        if res_path in self._load_lod_mesh_task_dict:
            del self._load_lod_mesh_task_dict[res_path]

    def on_set_back_sprite_opacity(self):
        if not self.panel:
            return
        self.get_scene_rt_ui().setOpacity(255)

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
        else:
            if not self.cc_sprite:
                return
            self.log('Setup AR Scene RenderTarget...')
            from common.uisys.uielment.CCSprite import CCSprite
            all_lights_names = [
             'dir_light']
            sz = self.get_scene_rt_ui().getContentSize()
            scale = self.cc_sprite.getScale()
            if scale > 1:
                self.get_scene_rt_ui().setScale(scale)
            CAM_RT_CONF['rt_width'] = sz.width
            CAM_RT_CONF['rt_height'] = sz.height
            self.scene_rt = RenderTargetHolder(None, self.get_scene_rt_ui(), CAM_RT_CONF, True, all_lights_names)
            self.scene_rt.scn.set_macros({'AR_MECHA': '1'})
            global_data.game_mgr.register_logic_timer(self.on_set_back_sprite_opacity, interval=3, times=1, mode=timer.LOGIC)
            self.scene_rt.scn.enable_vlm = True
            self.load_env_new_sync()
            self.log('Create Scene RenderTarget: %s', self.scene_rt.rt)
            self.scene_rt.scn.background_color = 0
            self.scene_rt.start_render_target()
            scene_rt_ui = self.get_scene_rt_ui()
            if scene_rt_ui and hasattr(scene_rt_ui, 'setBlendState'):
                scene_rt_ui.setBlendState(True, COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_ONE), COCOMATE_BLEND_2_HAL_BLEND_FACTOR(BLEND_INVSRCALPHA), BLENDOP_ADD)
            active_scene = world.get_active_scene()
            old_camera = active_scene.active_camera
            self.scene_rt.camera.aspect = old_camera.aspect
            self.scene_rt.camera.fov = old_camera.fov
            self.scene_rt.camera.z_range = old_camera.z_range
            self.scene_rt.camera.transformation = old_camera.transformation
            self.scene_rt.camera.projection_matrix = old_camera.projection_matrix
            self.scene_rt.camera.look_at = old_camera.look_at
            light = self.scene_rt.get_light()
            old_parent = light.get_parent()
            src_light = active_scene.get_light(all_lights_names[0])
            world_rotation_matrix = src_light.world_rotation_matrix
            light.world_rotation_matrix = world_rotation_matrix
            self.init_light_slider_value()
            self.log('Create AR Scene and Render to RenderTarget...')
            return

    @sync_exec
    def load_env_new_sync(self):
        self.scene_rt.scn.load_env_new('scene/scene_env_confs/default_nx2_mobile.xml')
        self.scene_rt.apply_conf('ar_mecha')

    def setup_cam_texture(self):
        if self.platform == game3d.PLATFORM_ANDROID:
            self.setup_cam_texture_android()
        elif self.platform == game3d.PLATFORM_IOS:
            self.setup_cam_texture_ios()
        else:
            return
        if not self.cc_sprite:
            print(('[Error] test--setup_cam_texture--cc_sprite =', self.cc_sprite))
            return
        content_size = self.get_layer().getContentSize()
        self.cc_sprite.setPosition(cc.Vec2(content_size.width / 2.0, content_size.height / 2.0))
        self.cc_sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))

    def setup_cam_texture_android(self):
        data_provider = self.session.fetch_cam_data_provider()
        if data_provider is None:
            self.log('Error: fetch camera data provider failed.')
            return
        else:
            nx_tex = render.texture('', False, False, 0, False, None, None, 0, 0, False, data_provider)
            bg_layer = self.get_layer()
            bg_layer_size = bg_layer.getContentSize()
            max_scale = max(bg_layer_size.width / nx_tex.size[0], bg_layer_size.height / nx_tex.size[1])
            min_scale = min(bg_layer_size.width / nx_tex.size[0], bg_layer_size.height / nx_tex.size[1])
            scale = 1
            if max_scale < FULL_SCREEN_WIDTH_HEIGHT_SCALE:
                scale = max_scale
            else:
                scale = min_scale
            cc_tex = cc.Texture2D.createWithITexture(nx_tex)
            self.cc_sprite = cc.Sprite.createWithTexture(cc_tex)
            self.cc_sprite.setScale(scale)
            self.get_layer().addChild(self.cc_sprite)
            if self.ar_type == ar.AR_INSIGHT:
                content_size = self.cc_sprite.getContentSize()
            elif self.ar_type == ar.AR_ARCORE:
                content_size = self.cc_sprite.getContentSize()
                self.cc_sprite.setScale(-1, -1)
                gl_pg = ui_effect.get_GLProgram(PROGRAM_KEY, 'positiontexturecolor_nomvp', 'positiontexturecolor_nomvp_yuv')
                pg_state = ui_effect.get_gl_program_state(self.cc_sprite, PROGRAM_KEY, gl_pg)
                self.cc_sprite.setGLProgramState(pg_state)
            else:
                self.log('Unknown AR Type: %s', ar_type)
                return
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
            bg_layer = self.get_layer()
            bg_layer_size = bg_layer.getContentSize()
            max_scale = max(bg_layer_size.width / nx_y_tex.size[0], bg_layer_size.height / nx_y_tex.size[1])
            min_scale = min(bg_layer_size.width / nx_y_tex.size[0], bg_layer_size.height / nx_y_tex.size[1])
            scale = 1
            if max_scale < FULL_SCREEN_WIDTH_HEIGHT_SCALE:
                scale = max_scale
            else:
                scale = min_scale
            cc_y_tex = cc.Texture2D.createWithITexture(nx_y_tex)
            cc_uv_tex = cc.Texture2D.createWithITexture(nx_uv_tex)
            self.cc_sprite = cc.Sprite.createWithTexture(cc_y_tex)
            gl_pg = ui_effect.get_GLProgram(PROGRAM_KEY, 'positiontexturecolor_nomvp', 'positiontexturecolor_nomvp_y_cbcr')
            pg_state = ui_effect.get_gl_program_state(self.cc_sprite, PROGRAM_KEY, gl_pg)
            pg_state.setUniformTexture('CC_Texture0', cc_y_tex)
            pg_state.setUniformTexture('CC_Texture2', cc_uv_tex)
            self.cc_sprite.setGLProgramState(pg_state)
            cc_y_tex.retain()
            cc_uv_tex.retain()
            self.cached_tex = (cc_y_tex, cc_uv_tex)
            self.cc_sprite.setScale(scale)
            self.get_layer().addChild(self.cc_sprite)
            self.cc_sprite.setPosition(self.view_center)
            self.cc_sprite.setContentSize(cc.Size(self.rt_width, self.rt_height))
            self.cc_sprite.setTextureRect(cc.Rect(0, 0, self.rt_width, self.rt_height))
            print(('test--setup_cam_texture_ios--nx_y_tex.size =', nx_y_tex.size, '--y_provider.size =', y_provider.size, '--uv_provider.size =', uv_provider.size))
            content_size = self.cc_sprite.getContentSize()
            self.ar_width = y_provider.size[0]
            self.ar_height = y_provider.size[1]
            return

    def on_frame_cb(self, session, state, reason, timestamp, cam_pose, cam_param):
        if self.on_frame_cb_log:
            print(('test--on_frame_cb--step1--state =', state, '--reason =', reason, '--timestamp=', timestamp, '--scene_rt =', self.scene_rt, '--STATE_DETECTING =', ar.STATE_DETECTING, '--STATE_TRACKING =', ar.STATE_TRACKING))
            self.log('on_frame_cb.cam_pose: %s %s', cam_pose.center, cam_pose.quaternion)
            self.log('on_frame_cb.cam_param: %s %s %s %s', cam_param.orientation, cam_param.focal_length, cam_param.fov, cam_param.proj_mtx)
        center = list(cam_pose.center)
        center[0] = center[0] * AR_TO_GAME_SCALE
        center[1] = center[1] * AR_TO_GAME_SCALE
        center[2] = center[2] * AR_TO_GAME_SCALE
        if (state == ar.STATE_DETECTING or state == ar.STATE_TRACKING) and self.scene_rt is None:
            print(('test--on_frame_cb--step3--state =', state, '--reason =', reason, '--timestamp=', timestamp, '--scene_rt =', self.scene_rt, '--STATE_DETECTING =', ar.STATE_DETECTING, '--STATE_TRACKING =', ar.STATE_TRACKING))
            self.on_frame_cb_log = 0
            self.setup_ar_scene()
            self.setup_camera_param(cam_param)
        if self.scene_rt is None:
            return
        else:
            if state != ar.STATE_TRACKING and state != ar.STATE_TRACK_LIMITED:
                return
            camera_pos = math3d.vector(*center)
            camera_rot = math3d.rotation(*cam_pose.quaternion)
            self.scene_rt.camera.set_placement(camera_pos, camera_rot.get_forward(), camera_rot.get_up())
            return

    def setup_camera_param(self, cam_param):
        if not self.scene_rt or not self.scene_rt.camera:
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
        self.scene_rt.camera.set_perspect(fov_y, aspect, z_min, z_max)
        print(('test--setup_camera_param--step1--fov_y =', fov_y, '--aspect =', aspect, '--z_min =', z_min, '--z_max =', z_max))

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
        if anchor_data.type == ar.ANCHOR_PLANE:
            pos, rot = self.get_plane_pos_rot(anchor_data)
            w = anchor_data.extent[0] * AR_TO_GAME_SCALE
            h = anchor_data.extent[2] * AR_TO_GAME_SCALE
            plane = self.make_plane(w, h)
            self.panel.temp_scene.StopAnimation('show')
            self.panel.temp_scene.nd_reticle.setVisible(False)
            plane.position = pos
            edge_point_list = self.make_plane_edge_points(w, h)
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
            self.scene_rt.add_model(model)
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
            self.scene_rt.remove_object(plane)
        if anchor_data.type == ar.ANCHOR_MARKER_2D:
            if anchor_data.identifier not in self.model_dict:
                return
            model = self.model_dict.pop(anchor_data.identifier, None)
            self.scene_rt.del_model(model)
        return

    def on_face_cb(self, session, status, count, faces):
        pass

    def on_gesture_cb(self, session, status, count, gestures):
        pass

    def on_save_map_cb(self, session, result, path):
        self.log('on_save_map_cb: %s %s', result, path)
        print('on_save_map_cb:', result, path)

    def on_load_map_cb(self, session, result, path):
        self.log('on_load_map_cb: %s %s', result, path)
        print('on_load_map_cb:', result, path)

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
        plane = world.primitives(self.scene_rt.scn)
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
        coord = world.primitives(self.scene_rt.scn)
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
        coord = world.primitives(self.scene_rt.scn)
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
        if self.panel.nd_content.isVisible():
            return
        self.panel.nd_content.setVisible(True)

    def _on_rotate_drag_begin(self, layer, touch):
        if len(self._nd_touch_IDs) >= 2:
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            pts = six_ex.values(self._nd_touch_poses)
            self._double_touch_prev_len = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        is_select = len(self._nd_touch_IDs) <= 1
        self.check_hit_ar_plane(layer, touch, is_select=is_select)
        return True

    def reset_rotate_model(self, index):
        self.cur_euler_rot_list[index] = math3d.vector(0, 0, 0)
        self.target_euler_rot_list[index] = math3d.vector(0, 0, 0)

    def rotate_model(self, index, rotate_times):
        target_euler_rot = self.target_euler_rot_list[index]
        self.target_euler_rot_list[index] = math3d.vector(0, target_euler_rot.y + rotate_times * math.pi * 2, 0)

    def _on_btn_scene_ui_drag(self, layer, touch):
        self.on_move_btn_scene_ui(layer, touch)
        self._is_drag_model = True

    def _on_rotate_drag--- This code section failed: ---

2660       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'get_mecha_num'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  ''
          12  COMPARE_OP            1  '<='
          15  POP_JUMP_IF_FALSE    22  'to 22'

2662      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

2664      22  LOAD_GLOBAL           1  'game3d'
          25  LOAD_ATTR             2  'get_platform'
          28  CALL_FUNCTION_0       0 
          31  LOAD_GLOBAL           3  'TEST_PLATFORM'
          34  COMPARE_OP            2  '=='
          37  POP_JUMP_IF_FALSE    86  'to 86'

2665      40  LOAD_FAST             2  'touch'
          43  LOAD_ATTR             4  'getDelta'
          46  CALL_FUNCTION_0       0 
          49  STORE_FAST            3  'delta_pos'

2666      52  LOAD_CONST            1  ''
          55  STORE_FAST            4  'model_index'

2667      58  LOAD_FAST             0  'self'
          61  LOAD_ATTR             5  'rotate_model'
          64  LOAD_FAST             4  'model_index'
          67  LOAD_FAST             3  'delta_pos'
          70  LOAD_ATTR             6  'x'
          73  UNARY_NEGATIVE   
          74  LOAD_GLOBAL           7  'ROTATE_FACTOR'
          77  BINARY_DIVIDE    
          78  CALL_FUNCTION_2       2 
          81  POP_TOP          

2669      82  LOAD_CONST            0  ''
          85  RETURN_END_IF    
        86_0  COME_FROM                '37'

2672      86  LOAD_FAST             2  'touch'
          89  LOAD_ATTR             8  'getId'
          92  CALL_FUNCTION_0       0 
          95  STORE_FAST            5  'tid'

2673      98  LOAD_FAST             2  'touch'
         101  LOAD_ATTR             9  'getLocation'
         104  CALL_FUNCTION_0       0 
         107  STORE_FAST            6  'touch_wpos'

2674     110  LOAD_FAST             5  'tid'
         113  LOAD_FAST             0  'self'
         116  LOAD_ATTR            10  '_nd_touch_IDs'
         119  COMPARE_OP            7  'not-in'
         122  POP_JUMP_IF_FALSE   129  'to 129'

2675     125  LOAD_CONST            0  ''
         128  RETURN_END_IF    
       129_0  COME_FROM                '122'

2677     129  LOAD_FAST             0  'self'
         132  LOAD_ATTR            11  'check_hit_ar_plane'
         135  LOAD_FAST             1  'layer'
         138  LOAD_FAST             2  'touch'
         141  CALL_FUNCTION_2       2 
         144  POP_TOP          

2679     145  LOAD_FAST             0  'self'
         148  LOAD_ATTR            12  '_select_model_index'
         151  STORE_FAST            4  'model_index'

2681     154  LOAD_FAST             4  'model_index'
         157  LOAD_CONST            1  ''
         160  COMPARE_OP            0  '<'
         163  POP_JUMP_IF_FALSE   170  'to 170'

2682     166  LOAD_CONST            0  ''
         169  RETURN_END_IF    
       170_0  COME_FROM                '163'

2683     170  LOAD_GLOBAL          13  'len'
         173  LOAD_FAST             0  'self'
         176  LOAD_ATTR            10  '_nd_touch_IDs'
         179  CALL_FUNCTION_1       1 
         182  LOAD_CONST            2  1
         185  COMPARE_OP            2  '=='
         188  POP_JUMP_IF_FALSE   230  'to 230'

2684     191  LOAD_FAST             2  'touch'
         194  LOAD_ATTR             4  'getDelta'
         197  CALL_FUNCTION_0       0 
         200  STORE_FAST            3  'delta_pos'

2686     203  LOAD_FAST             0  'self'
         206  LOAD_ATTR             5  'rotate_model'
         209  LOAD_FAST             4  'model_index'
         212  LOAD_FAST             3  'delta_pos'
         215  LOAD_ATTR             6  'x'
         218  UNARY_NEGATIVE   
         219  LOAD_GLOBAL           7  'ROTATE_FACTOR'
         222  BINARY_DIVIDE    
         223  CALL_FUNCTION_2       2 
         226  POP_TOP          
         227  JUMP_FORWARD        320  'to 550'

2688     230  LOAD_GLOBAL          13  'len'
         233  LOAD_FAST             0  'self'
         236  LOAD_ATTR            10  '_nd_touch_IDs'
         239  CALL_FUNCTION_1       1 
         242  LOAD_CONST            3  2
         245  COMPARE_OP            5  '>='
         248  POP_JUMP_IF_FALSE   550  'to 550'

2689     251  LOAD_CONST            0  ''
         254  RETURN_VALUE     

2690     255  LOAD_FAST             6  'touch_wpos'
         258  LOAD_FAST             0  'self'
         261  LOAD_ATTR            14  '_nd_touch_poses'
         264  LOAD_FAST             5  'tid'
         267  STORE_SUBSCR     

2691     268  LOAD_GLOBAL          15  'six_ex'
         271  LOAD_ATTR            16  'values'
         274  LOAD_FAST             0  'self'
         277  LOAD_ATTR            14  '_nd_touch_poses'
         280  CALL_FUNCTION_1       1 
         283  STORE_FAST            7  'pts'

2692     286  LOAD_GLOBAL          17  'cc'
         289  LOAD_ATTR            18  'Vec2'
         292  LOAD_FAST             7  'pts'
         295  LOAD_CONST            1  ''
         298  BINARY_SUBSCR    
         299  CALL_FUNCTION_1       1 
         302  STORE_FAST            8  'vec'

2693     305  LOAD_FAST             8  'vec'
         308  LOAD_ATTR            19  'subtract'
         311  LOAD_FAST             7  'pts'
         314  LOAD_CONST            2  1
         317  BINARY_SUBSCR    
         318  CALL_FUNCTION_1       1 
         321  POP_TOP          

2694     322  LOAD_FAST             8  'vec'
         325  LOAD_ATTR            20  'getLength'
         328  CALL_FUNCTION_0       0 
         331  STORE_FAST            9  'cur_dist'

2696     334  LOAD_FAST             9  'cur_dist'
         337  LOAD_FAST             0  'self'
         340  LOAD_ATTR            21  '_double_touch_prev_len'
         343  BINARY_SUBTRACT  
         344  STORE_FAST           10  'delta'

2697     347  LOAD_FAST            10  'delta'
         350  STORE_FAST           11  'init_delta'

2698     353  LOAD_FAST             9  'cur_dist'
         356  LOAD_FAST             0  'self'
         359  STORE_ATTR           21  '_double_touch_prev_len'

2700     362  LOAD_FAST            10  'delta'
         365  LOAD_FAST             0  'self'
         368  LOAD_ATTR            22  'MODEL_SCALE_TOUCH_SEN_FACTOR'
         371  BINARY_DIVIDE    
         372  STORE_FAST           10  'delta'

2701     375  LOAD_FAST             0  'self'
         378  LOAD_ATTR            23  '_cur_scale_list'
         381  LOAD_FAST             4  'model_index'
         384  BINARY_SUBSCR    
         385  LOAD_FAST            10  'delta'
         388  BINARY_ADD       
         389  LOAD_FAST             0  'self'
         392  LOAD_ATTR            23  '_cur_scale_list'
         395  LOAD_FAST             4  'model_index'
         398  STORE_SUBSCR     

2702     399  LOAD_GLOBAL          24  'max'
         402  LOAD_FAST             0  'self'
         405  LOAD_ATTR            23  '_cur_scale_list'
         408  LOAD_FAST             4  'model_index'
         411  BINARY_SUBSCR    
         412  LOAD_FAST             0  'self'
         415  LOAD_ATTR            25  '_min_scale_list'
         418  LOAD_FAST             4  'model_index'
         421  BINARY_SUBSCR    
         422  CALL_FUNCTION_2       2 
         425  LOAD_FAST             0  'self'
         428  LOAD_ATTR            23  '_cur_scale_list'
         431  LOAD_FAST             4  'model_index'
         434  STORE_SUBSCR     

2703     435  LOAD_GLOBAL          26  'min'
         438  LOAD_FAST             0  'self'
         441  LOAD_ATTR            23  '_cur_scale_list'
         444  LOAD_FAST             4  'model_index'
         447  BINARY_SUBSCR    
         448  LOAD_FAST             0  'self'
         451  LOAD_ATTR            27  '_max_scale_list'
         454  LOAD_FAST             4  'model_index'
         457  BINARY_SUBSCR    
         458  CALL_FUNCTION_2       2 
         461  LOAD_FAST             0  'self'
         464  LOAD_ATTR            23  '_cur_scale_list'
         467  LOAD_FAST             4  'model_index'
         470  STORE_SUBSCR     

2705     471  LOAD_FAST             0  'self'
         474  LOAD_ATTR            28  'hit_model_list'
         477  LOAD_FAST             4  'model_index'
         480  BINARY_SUBSCR    
         481  STORE_FAST           12  'hit_model'

2706     484  LOAD_FAST            12  'hit_model'
         487  POP_JUMP_IF_FALSE   550  'to 550'
         490  LOAD_FAST            12  'hit_model'
         493  LOAD_ATTR            29  'valid'
       496_0  COME_FROM                '487'
         496  POP_JUMP_IF_FALSE   550  'to 550'

2707     499  LOAD_GLOBAL          30  'math3d'
         502  LOAD_ATTR            31  'vector'
         505  LOAD_FAST             0  'self'
         508  LOAD_ATTR            23  '_cur_scale_list'
         511  LOAD_FAST             4  'model_index'
         514  BINARY_SUBSCR    
         515  LOAD_FAST             0  'self'
         518  LOAD_ATTR            23  '_cur_scale_list'
         521  LOAD_FAST             4  'model_index'
         524  BINARY_SUBSCR    
         525  LOAD_FAST             0  'self'
         528  LOAD_ATTR            23  '_cur_scale_list'
         531  LOAD_FAST             4  'model_index'
         534  BINARY_SUBSCR    
         535  CALL_FUNCTION_3       3 
         538  LOAD_FAST            12  'hit_model'
         541  STORE_ATTR           32  'scale'
         544  JUMP_ABSOLUTE       550  'to 550'
         547  JUMP_FORWARD          0  'to 550'
       550_0  COME_FROM                '547'
       550_1  COME_FROM                '227'

Parse error at or near `LOAD_GLOBAL' instruction at offset 268

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
                return
            pos = self.get_hittest_pos(anchor_data)
            if not pos:
                return
            last_pos = self._mecha_drag_pos_list[self._select_model_index]
            self._mecha_drag_pos_list[self._select_model_index] = pos
            if not last_pos:
                return
            diff_vec = pos - last_pos
            position = model.position
            new_position = position + diff_vec
            model.position = new_position
            return

    def _on_rotate_drag_end(self, layer, touch):
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]
        self.check_hit_ar_plane(layer, touch, is_end_touch=True)

    def convert_touch_location_to_ar_pos(self, location):
        neox_x, neox_y = cocos_utils.cocos_pos_to_neox(location.x, location.y)
        location = self.cc_sprite.convertToNodeSpace(location)
        x = location.x
        z = location.y
        if x < 0 or z < 0 or x > self.rt_width or z > self.rt_height:
            return
        z = self.ar_height - (z + abs(self.ar_height - self.rt_height) / 2)
        x = x + abs(self.ar_width - self.rt_width) / 2
        x /= self.ar_width
        z /= self.ar_height
        scale = self.cc_sprite.getScale()
        if scale > 1:
            x *= scale
            z *= scale
        x = min(x, 1)
        z = min(z, 1)
        return (
         x, z)

    def check_hit_ar_plane(self, layer, touch, is_select=False, is_end_touch=False, is_update_pos=False):
        if self.session is None or not self.cc_sprite:
            return True
        else:
            location = touch.getLocation()
            ar_pos = self.convert_touch_location_to_ar_pos(location)
            if not ar_pos:
                return
            x, z = ar_pos
            neox_x, neox_y = cocos_utils.cocos_pos_to_neox(location.x, location.y)
            if is_select:
                if self.get_mecha_num() <= 0:
                    self._select_model_index = 0
                else:
                    pick_result = self.scene_rt.scn.pick(neox_x, neox_y)
                    select_model_index = -1
                    if pick_result and pick_result[0]:
                        pick_model = pick_result[0]
                        for index, one_model in enumerate(self.hit_model_list):
                            if one_model == pick_model:
                                select_model_index = index
                                break

                    if select_model_index < 0 and self.panel.btn_scene_ui.isVisible():
                        pass
                    else:
                        self._select_model_index = select_model_index
                    if self._select_model_index >= 0:
                        self.panel.btn_scene_ui.setVisible(True)
                        self.panel.nd_slider.setVisible(True)
            have_no_mecha = self.get_mecha_num() <= 0
            if (have_no_mecha or is_update_pos) and self._select_model_index >= 0:
                self.hit_test(x, z, is_select, is_end_touch, neox_x, neox_y)
            if is_select or have_no_mecha:
                self.update_model_arrow_pos()
                self.update_slider_percent()
            return

    def update_model_arrow_pos(self):
        model = self.hit_model_list[self._select_model_index]
        if not model:
            return
        neox_2d_pos = self.scene_rt.camera.world_to_screen(model.position)
        cocos_2d_pos = cocos_utils.neox_pos_to_cocos(*neox_2d_pos)
        self.panel.btn_scene_ui.setPosition(*cocos_2d_pos)

    def update(self, *args):
        for index, hit_model in enumerate(self.hit_model_list):
            if hit_model and hit_model.valid:
                cur_euler_rot = self.cur_euler_rot_list[index]
                cur_euler_rot.intrp(cur_euler_rot, self.target_euler_rot_list[index], 0.2)
                self.cur_euler_rot_list[index] = cur_euler_rot
                hit_model.world_rotation_matrix = math3d.euler_to_matrix(cur_euler_rot)

        if self.panel.btn_scene_ui.isVisible() and not self._nd_touch_IDs and not self._is_drag_model:
            self.update_model_arrow_pos()

    def get_point_cloud_pos(self, points, i):
        return math3d.vector(points[i * 3], points[i * 3 + 1], points[i * 3 + 2])

    def on_key_msg(self, msg, key_code):
        pass

    def log(self, msg, *args):
        print('[NxAR-Python] %s' % (msg % args,))
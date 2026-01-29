# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartModelDisplay.py
from __future__ import absolute_import
from __future__ import print_function
import exception_hook
import six
from six.moves import range
import re
import game3d
import math3d
import world
import math
import time
import C_file
from . import ScenePart
from common.cfg import confmgr
from common.algorithm import resloader
from logic.gutils import dress_utils
from logic.gutils.mecha_skin_utils import MechaSocketResAgent, get_mecha_force_shiny_weapon_id
from logic.gutils.role_skin_utils import load_improved_skin_model_and_effect, clear_trigger_at_intervals_res, get_skin_improved_sfx_item_id, get_improve_skin_body_path, get_improve_skin_head_id, clear_role_skin_model_and_effect, load_normal_skin_model_and_effect, load_role_skin_model_for_shadow
from logic.gutils.role_skin_utils import load_glide_model_effect_and_model, clear_glide_model_effect_and_model, get_glide_effect_socket_data
from logic.gutils import item_utils as iutils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_PET_SKIN, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN
from logic.gutils import interaction_utils
import weakref
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from common.framework import Functor
from common.utils.timer import CLOCK, RELEASE, LOGIC
from logic.gcommon.common_const.scene_const import LOBBY_EYE_ADAPT_FACTOR
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gutils.dress_utils import get_mecha_weapon_model_path, FORCE_USE_H_MECHA, get_mecha_model_h_path
from logic.gutils import lobby_model_display_utils
from logic.gutils import mecha_utils
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import get_main_skin_id, load_model_decal_data, load_model_color_data, load_model_decal_high_quality
from logic.gcommon.common_const.scene_const import SCENE_SKIN_DEFINE
import logic.client.const.lobby_model_display_const as lobby_model_display_const
from ext_package.ext_decorator import has_skin_ext, ext_do_nothing_when_not_default_skin, ext_do_nothing_when_no_skin_ext, ext_do_nothing_when_no_skin_ext_v2, ext_remind
from logic.manager_agents.manager_decorators import sync_exec
_HASH_light_info = game3d.calc_string_hash('light_info')
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
MECHA_PATH_PATTERN = re.compile('(.*)model_new/mecha/(\\d+)')
import random
import os
from common.utils import pc_platform_utils
import render
NO_HEAD_MODEL = [
 'character/13/2011/parts/h_head.gim',
 'character/32/2001/parts/h_head.gim',
 'character/19/2002_skin_s1/parts/h_head.gim',
 'character/13/2012/parts/h_head.gim',
 'character/13/2012_skin_s1/parts/h_head.gim',
 'character/13/2012_skin_s2/parts/h_head.gim',
 'character/15/2014/parts/h_head.gim',
 'character/30/2002/parts/h_head.gim',
 'character/30/2002_skin_s1/parts/h_head.gim',
 'character/30/2002_skin_s2/parts/h_head.gim']
MODEL_NEED_OUTLINE = (
 '8021_skin_s01',)

def is_model_need_outline(model_path):
    for model in MODEL_NEED_OUTLINE:
        if model in model_path:
            return True

    return False


def enable_outline--- This code section failed: ---

  85       0  LOAD_GLOBAL           0  'pc_platform_utils'
           3  LOAD_ATTR             1  'set_multi_pass_outline'
           6  LOAD_ATTR             1  'set_multi_pass_outline'
           9  LOAD_GLOBAL           2  'True'
          12  CALL_FUNCTION_257   257 
          15  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 12


class CLobbyModel(object):

    def __init__(self, parent, dict_data={}, **kwargs):
        self.parent = parent
        self.show_anim_name = None
        self.move_ani_name = None
        self.end_anim_name = None
        self.end_anim_name_loop_time = 0
        self.cur_end_anim_name_loop_time = 0
        self.is_play_show_anim = False
        self._load_mesh_task = None
        self.create_callback = kwargs.get('create_callback', None)
        self._load_cb = kwargs.get('load_callback', None)
        self.loaded_human_res_callback = kwargs.get('loaded_human_res_callback', None)
        self.show_box_name = kwargs.get('show_box_name', 'box_name')
        self.real_box_name = kwargs.get('real_box_name', None)
        self.support_mirror = kwargs.get('support_mirror', True)
        self.is_render_target_model = kwargs.get('is_render_target_model', False)
        self.need_correct_show_anim_phase = kwargs.get('need_correct_show_anim_phase', False)
        self.init_parameters()
        self.is_human = False
        self.is_mecha = False
        self.mecha_socket_res_agent = None
        self.cur_sound_id = None
        self.show_anim_sound_dict = {}
        self.cur_loop_sound_id = None
        self.cur_loop_sound_cover_bgm = False
        self._load_body_mesh_task = None
        self.hit_model = None
        self.sfx_model = None
        self.sfx_model_alone = True
        self._cur_anim_args = None
        self.improved_head = False
        self.shadow_model_path = ''
        self.shadow_model = None
        self.shadow_mecha_socket_res_agent = None
        self.shadow_model_sub_model_list = []
        self.shadow_model_sub_model_visible = False
        self.head_pendant_type = None
        self.head_pendant_type_new = None
        self.head_res_path = None
        self.head_res_path_new = None
        self.head_sfx = None
        self.had_loaded_head_pendant = None
        self.pendant_socket_name = None
        self.pendant_socket_name_new = None
        self.pendant_socket_res_path = None
        self.pendant_socket_res_path_new = None
        self.pendant_random_anim_list = None
        self.bag_model_path = None
        self.bag_socket_name = None
        self.bag_model_path2 = None
        self.bag_socket_name2 = None
        self.is_same_gis = False
        self.had_loaded_bag = False
        self.had_loaded_bag2 = False
        self.model_data = dict_data
        display_item_no = dict_data.get('item_no')
        self.item_type = iutils.get_lobby_item_type(display_item_no)
        self.ext_can_show_model = iutils.ext_can_show_model(display_item_no, self.item_type)
        self._show_extra_socket_objs = True
        self._show_sockets = {}
        self._showing_socket = ''
        self._assure_socket = dict_data.get('assure_socket', None)
        self.allow_rotate = True
        self.emoji_model = None
        self.emoji_model_id = None
        self.emoji_sfx_id = None
        self.emoji_update_timer_id = None
        self.emoji_auto_close = False
        self.emoji_close_callback = None
        self._trk_player = None
        self._model_trk_player = None
        self._model_trk_init_position = None
        self._model_trk_init_rotation = None
        self._model_trk_callback = None
        self.by_model_trk = False
        self.chuchang_sfx_list = []
        self.chuchang_sfx_timer_list = []
        self.anim_screen_sfx_list = []
        self.anim_screen_sfx_timer_list = []
        self.original_scale_before_change = -1
        self._bond_temp_sfxes = []
        self.temp_bond_effect_info = {}
        self.by_mecha_chuchang = dict_data.get('by_mecha_chuchang', False)
        self._is_reflect = kwargs.get('is_reflect', True)
        self.other_pendant_model_dict = {}
        self.other_pendant_model_loaded_dict = {}
        self.other_pendant_model_socket_model_name_dict = {}
        self.other_pendant_model_sub_mesh_model_name_dict = {}
        self.on_change_display_model(dict_data)
        self.init_event()
        self.need_decal = False
        self.need_color = False
        self.cur_model = None
        self.cur_skin_id = None
        self.cur_decal_list = None
        self.head_pendant_random_anim_timer = None
        self.head_pendant_anim_index = 0
        self.head_pendant_model = None
        self.cur_play_anim_idx = 0
        self.human_init_load_count = 0
        self.human_init_loaded_count = 0
        self.auto_rotate_duration = 0
        self._extra_model_load_task_dict = {}
        self._model_loaded_callback = None
        self.is_mute = False
        return

    def destroy(self):
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        if self._model_trk_player:
            self._model_trk_player.on_exit()
            self._model_trk_player = None
        self.model_trk_init_position = None
        self.model_trk_init_rotation = None
        self._model_trk_callback = None
        self.parent = None
        self.clear_spring_anim()
        self.remove_emoji()
        if self.mecha_socket_res_agent:
            self.mecha_socket_res_agent.destroy()
            self.mecha_socket_res_agent = None
        if self.shadow_mecha_socket_res_agent:
            self.shadow_mecha_socket_res_agent.destroy()
            self.shadow_mecha_socket_res_agent = None
        self.clear_skin_model_and_effect()
        self.clear_chuchang_sfx()
        self.clear_model()
        self.process_event(False)
        self.stop_cur_sound()
        self.stop_cur_loop_sound()
        self.loaded_human_res_callback = None
        self.clear_extra_model_load_tasks()
        self._model_loaded_callback = None
        return

    def do_loaded_human_res_callback(self):
        if self.loaded_human_res_callback:
            self.loaded_human_res_callback()

    def remove_emoji(self):
        if self.emoji_model_id:
            if self.emoji_close_callback and callable(self.emoji_close_callback):
                self.emoji_close_callback()
                self.emoji_close_callback = None
            interaction_utils.remove_emoji(self.emoji_model_id, self.emoji_sfx_id, self.emoji_update_timer_id)
            self.emoji_model_id = None
            self.emoji_model = None
            self.emoji_sfx_id = None
            self.emoji_update_timer_id = None
        return

    def stop_cur_loop_sound(self):
        if self.cur_loop_sound_id is not None:
            global_data.sound_mgr.stop_playing_id(self.cur_loop_sound_id)
            self.cur_loop_sound_id = None
        if self.cur_loop_sound_cover_bgm:
            global_data.sound_mgr.set_music_volume(global_data.sound_mgr.get_music_volume())
        return

    def stop_cur_sound(self):
        if self.cur_sound_id is not None:
            global_data.sound_mgr.stop_playing_id(self.cur_sound_id)
            self.cur_sound_id = None
        return

    def clear_skin_model_and_effect(self):
        model = self.get_model()
        if model:
            if self.is_human:
                clear_role_skin_model_and_effect(model, clear_trigger_interval=True)
        if self.shadow_model and self.shadow_model.valid:
            if self.is_human:
                clear_role_skin_model_and_effect(self.shadow_model, clear_trigger_interval=True)
            for sub_shadow_model in self.shadow_model_sub_model_list:
                self.shadow_model.unbind(sub_shadow_model)

        self.shadow_model_sub_model_list = []
        self.shadow_model_sub_model_visible = False

    def clear_chuchang_sfx(self):
        for sfx_id in self.anim_screen_sfx_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.anim_screen_sfx_list = []
        for timer_id in self.anim_screen_sfx_timer_list:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self.anim_screen_sfx_timer_list = []
        for sfx_id in self.chuchang_sfx_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.chuchang_sfx_list = []
        for timer_id in self.chuchang_sfx_timer_list:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self.chuchang_sfx_timer_list = []

    def clear_improved_head(self):
        self.change_head_model(None, None, None, None, None)
        self.improved_head = False
        return

    def init_parameters(self):
        self._model = None
        self._model_id = None
        self.cur_euler_rot = math3d.vector(0, 0, 0)
        self.target_euler_rot = math3d.vector(0, 0, 0)
        self.model_pos = math3d.vector(0, 0, 0)
        self.last_model_pos = math3d.vector(0, 0, 0)
        self.is_slerp = False
        self.mode_center_pos = math3d.vector(0, 0, 0)
        self.off_euler_rot = [0, 0, 0]
        self.off_euler_rot_mtx = None
        self.sub_mesh_names = []
        self.socket_model_names = []
        self.off_position_cache = None
        return

    def init_event(self):
        if self.is_render_target_model:
            return
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'rotate_model_automatically': self.rotate_model_automatically,
           'rotate_model_display': self.rotate_model,
           'rotate_model_display_by_euler': self.rotate_model_by_euler,
           'load_high_quality_decal': self.load_high_quality_model_decal,
           'display_quality_change': self.on_display_quality_change,
           'set_model_display_rotate_euler': self.set_model_rotate_euler
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def get_mirror_reflect_enable--- This code section failed: ---

 361       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'parent'
           6  POP_JUMP_IF_FALSE    43  'to 43'
           9  LOAD_FAST             1  'quality'
          12  LOAD_CONST            1  1
          15  COMPARE_OP            4  '>'
          18  JUMP_IF_FALSE_OR_POP    46  'to 46'
          21  LOAD_GLOBAL           1  'lobby_model_display_utils'
          24  LOAD_ATTR             2  'is_scene_surpport_reflect'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             0  'parent'
          33  LOAD_ATTR             3  'get_scene_content_type'
          36  CALL_FUNCTION_0       0 
          39  CALL_FUNCTION_1       1 
          42  RETURN_END_IF    
        43_0  COME_FROM                '18'
        43_1  COME_FROM                '6'
          43  LOAD_GLOBAL           4  'False'
          46  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `RETURN_END_IF' instruction at offset 42

    def on_display_quality_change(self, quality):
        if global_data.is_ue_model:
            mirror_reflect = self.get_mirror_reflect_enable(quality)
            if self._model:
                self._model.mirror_reflect = mirror_reflect

    def clear_model(self):
        if self.sfx_model:
            self.sfx_model.destroy()
        self.sfx_model = None
        if self.mecha_socket_res_agent:
            self.mecha_socket_res_agent.destroy()
            self.mecha_socket_res_agent = None
        if self._model and self._model.valid:
            self._model.destroy()
        if self._model_id is not None:
            global_data.model_mgr.remove_model_by_id(self._model_id)
        self._model_id = None
        self._model = None
        if self.shadow_model and self.shadow_model.valid:
            if self.shadow_mecha_socket_res_agent:
                self.shadow_mecha_socket_res_agent.destroy()
                self.shadow_mecha_socket_res_agent = None
            self.shadow_model.destroy()
            self.shadow_model = None
        if self.hit_model and self.hit_model.valid:
            self.hit_model.destroy()
            self.hit_model = None
        for sub_mesh in self.sub_mesh_names:
            resloader.del_res_attr(self, sub_mesh)

        self.sub_mesh_names = []
        for socket_model in self.socket_model_names:
            resloader.del_res_attr(self, socket_model, True)
            setattr(self, socket_model, None)

        self.head_pendant_model = None
        if self.head_pendant_random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.head_pendant_random_anim_timer)
            self.head_pendant_random_anim_timer = None
        self.socket_model_names = []
        return

    def hide_model(self):
        model = self.get_model()
        if model:
            if model.visible:
                model.visible = False
            if self.mecha_socket_res_agent:
                self.mecha_socket_res_agent.set_follow_model_visible_without_record(False)

    def show_model(self):
        model = self.get_model()
        if model:
            if not model.visible:
                model.visible = True
            if self.mecha_socket_res_agent:
                self.mecha_socket_res_agent.refresh_res_visible()
            if self.shadow_model:
                if self.shadow_mecha_socket_res_agent:
                    self.shadow_mecha_socket_res_agent.refresh_res_visible()
                if not self.shadow_model_sub_model_visible:
                    for sub_model in self.shadow_model_sub_model_list:
                        sub_model.visible = False

    def set_is_mute(self, is_mute):
        self.is_mute = is_mute

    def set_skin_follow_res_visible(self, visible):
        if self.mecha_socket_res_agent:
            self.mecha_socket_res_agent.set_follow_model_visible_without_record(visible)

    def get_model(self):
        if self._model and self._model.valid:
            return self._model
        else:
            return None

    def get_hit_model(self):
        if self.hit_model and self.hit_model.valid:
            return self.hit_model
        else:
            return None

    def get_sfx_model(self):
        if self.sfx_model and self.sfx_model.valid:
            return self.sfx_model
        else:
            return None

    def get_view_flag(self):
        if self.parent:
            return self.parent._view_flag
        else:
            return False

    def get_cam_look_at_position(self, default=None):
        raw_model = self.get_model()
        if not raw_model:
            return default
        return math3d.vector(raw_model.world_position.x, raw_model.world_position.y + raw_model.bounding_box.y / 2.0 * raw_model.scale.y, raw_model.world_position.z)

    @ext_do_nothing_when_not_default_skin
    def on_change_display_model(self, dict_data={}):
        mpath = dict_data.get('mpath')
        if not mpath:
            return
        else:
            if self.item_type in (L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN):
                self.is_human = True
            elif self.item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN):
                self.is_mecha = True
                if self.mecha_socket_res_agent is None:
                    self.mecha_socket_res_agent = MechaSocketResAgent()
                if self.shadow_mecha_socket_res_agent is None:
                    self.shadow_mecha_socket_res_agent = MechaSocketResAgent()
            scene = world.get_active_scene()
            improved_skin_sfx_id = dict_data.get('improved_skin_sfx_id')
            sub_mesh_path_list = dict_data.get('sub_mesh_path_list', [])
            if improved_skin_sfx_id and self.is_human:
                if not mpath.endswith('empty.gim'):
                    mpath = get_improve_skin_body_path(improved_skin_sfx_id) or mpath
                else:
                    sub_mesh_path_list[0] = get_improve_skin_body_path(improved_skin_sfx_id, lod='l') or sub_mesh_path_list[0]
            if self.is_mecha:
                shiny_weapon_id = dict_data.get('shiny_weapon_id', None)
                shiny_preview = dict_data.get('shiny_preview', None)
                if shiny_preview:
                    shiny_weapon_id = shiny_preview if 1 else shiny_weapon_id
                    if shiny_weapon_id:
                        skin_id = dict_data.get('skin_id', None)
                        mecha_item_id = iutils.get_lobby_item_belong_no(skin_id)
                        mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
                        if not confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'second_model_dir'):
                            sub_mesh_path_list[0] = dress_utils.get_mecha_model_h_path(None, skin_id, shiny_weapon_id=shiny_weapon_id)
                if scene.is_hdr_enable and scene._get_scene_data('hdr_config', 'default') in ('zhanshi_human',
                                                                                              'zhanshi_mecha'):
                    hdr_config = dict_data.get('hdr_config', '')
                    env_config = dict_data.get('env_config', '')
                    if hdr_config:
                        conf_hdr = hdr_config
                    else:
                        conf_hdr = 'zhanshi_human' if self.is_human else 'zhanshi_mecha'
                    if env_config:
                        conf_env = (
                         env_config, 'on_ground')
                    else:
                        conf_env = (
                         'zhanshi' if self.is_human else 'zhanshi_mecha', 'on_ground')
                    scene.set_bloom_c_env(conf_hdr)
                    scene.setup_env_light_info(*conf_env)
                light_dir = dict_data.get('light_dir')

                @sync_exec
                def change_light_dir(light_dir=light_dir, scene=scene):
                    if not scene or not scene.valid:
                        return
                    scene.change_realtime_shadow_light_dir(math3d.vector(*light_dir))

                if light_dir:
                    change_light_dir()
                self.shadow_model_path = mpath
                if self.is_human and self.shadow_model_path.endswith('empty.gim'):
                    self.shadow_model_path = self.shadow_model_path.replace('empty.gim', 'l3.gim')
            self.cur_model_data = dict_data
            self._model_id = global_data.model_mgr.create_model(mpath, mesh_path_list=sub_mesh_path_list, on_create_func=Functor(self.on_load_model_complete, dict_data))
            if dict_data.get('ignore_chuchang_sfx', False) or self.is_human:
                chuchang_sfx = confmgr.get('role_info', 'RoleSkin', 'Content', str(dict_data.get('skin_id', None)), 'chuchang_sfx', default={})
            else:
                chuchang_sfx = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(dict_data.get('skin_id', None)), 'chuchang_sfx', default={})
            if chuchang_sfx:
                chuchang_sfx_list = chuchang_sfx.get(dict_data.get('show_anim'), [])
                if chuchang_sfx_list:
                    box_position = None
                    if self.real_box_name:
                        box_name = self.real_box_name if 1 else self.parent.scene_data.get(self.show_box_name)
                        if box_name:
                            box_position = self.parent.get_box_position(box_name)
                        if not box_position:
                            return
                        off_position = math3d.vector(*dict_data.get('off_position', [0, 0, 0]))
                        if self.by_mecha_chuchang:
                            sfx_position = math3d.vector(0, 0, 0) + off_position
                        else:
                            sfx_position = box_position + off_position
                        delay_sfx_list = []
                        immediate_sfx_list = []
                        for sfx in chuchang_sfx_list:
                            if type(sfx) == dict:
                                delay_sfx_list.append(sfx)
                            else:
                                immediate_sfx_list.append(sfx)

                        if immediate_sfx_list:
                            self.chuchang_sfx_list = dress_utils.play_chuchang_sfx(immediate_sfx_list, sfx_position)
                        if delay_sfx_list:
                            timer_regist_func = global_data.game_mgr.register_logic_timer

                            def create_sfx(sfx_list):
                                self.chuchang_sfx_list.extend(dress_utils.play_chuchang_sfx(sfx_list, sfx_position))

                            for sfx in delay_sfx_list:
                                self.chuchang_sfx_timer_list.append(timer_regist_func(func=create_sfx, args=[sfx['sfx_list']], interval=sfx['delay'], times=1, mode=CLOCK))

            return

    def _end_show_anim(self, *args):
        self.allow_rotate = True
        model = self.get_model()
        if not model:
            return False
        else:
            if not self.end_anim_name:
                return False
            if not model.has_anim(self.end_anim_name):
                self.end_anim_name = 'stand_idle'
                if not model.has_anim(self.end_anim_name):
                    return False
            if not self._show_extra_socket_objs:
                self.show_extra_socket_objs(True)
            self.hide_sockets_after_show_anim()
            loop = self.model_data.get('force_end_ani_loop', False)
            transit_time = 0 if global_data.book_gesture_no_transit_time else 300
            SKIN_SKIP_TRANSIT = {
             201002056}
            skin_id = self.model_data.get('skin_id', None)
            if skin_id in SKIN_SKIP_TRANSIT:
                transit_time = 0
            if self.end_anim_name_loop_time:
                self.cur_end_anim_name_loop_time = self.cur_end_anim_name_loop_time + 1
                self.play_animation(model, self.end_anim_name, transit_time, world.TRANSIT_TYPE_DELAY, 0, False)
                try:
                    model.register_anim_key_event(self.end_anim_name, 'end', self.loop_end_show_anim)
                except TypeError:
                    pass

                if self.move_ani_name:
                    model.register_anim_key_event(self.move_ani_name, 'end', self.loop_end_show_anim)
            else:
                if loop:
                    self.play_animation(model, self.end_anim_name, transit_time, world.TRANSIT_TYPE_DELAY, 0, loop)
                else:
                    self.play_animation(model, self.end_anim_name, transit_time, world.TRANSIT_TYPE_DELAY)
                if '8009_skin_s01' in model.filename and model.has_anim_event(self.end_anim_name, 'loop_point'):

                    def replay_the_anim(model, anim_name, event_name):
                        if anim_name != self.end_anim_name:
                            return
                        self.play_animation(model, self.end_anim_name, 1000, world.TRANSIT_TYPE_IMM)

                    model.register_anim_key_event(self.end_anim_name, 'loop_point', replay_the_anim)
            return True

    def loop_end_show_anim(self, *args):
        model = self.get_model()
        if not model:
            return False
        transit_time = 0 if global_data.book_gesture_no_transit_time else 300
        if self.cur_end_anim_name_loop_time > self.end_anim_name_loop_time:
            self.cur_end_anim_name_loop_time = 0
            if self.move_ani_name:
                self.play_animation(model, self.move_ani_name, transit_time, world.TRANSIT_TYPE_DELAY, 0, False)
        else:
            self.cur_end_anim_name_loop_time = self.cur_end_anim_name_loop_time + 1
            self.play_animation(model, self.end_anim_name, transit_time, world.TRANSIT_TYPE_DELAY, 0, False)

    def end_show_anim(self, *args):
        if self.zoom_in_camera == lobby_model_display_const.CHANGE_CAMERA_MODE_CALLBACK_ON_END_ANIM:
            if self.play_show_anim_callback:
                self.play_show_anim_callback()
        if self.item_type == L_ITEM_YTPE_VEHICLE_SKIN:
            self.init_spring_anim()
        if self.end_ani_list and not self.model_data.get('is_bond_tag') and not self.model_data.get('mpath', '').endswith('empty.gim'):
            if not self.play_end_anim_list():
                return
        elif not self._end_show_anim():
            return
        if self.show_anim_name != self.end_anim_name:
            self.init_spring_anim()
        model = self.get_model()
        try:
            model.unregister_event(self.end_show_anim, 'end', self.show_anim_name)
        except Exception as e:
            import traceback
            import exception_hook
            msg = 'PartModelDisplay line:543, def end_show_anim \n'
            msg += 'self.end_show_anim: %s \n' % str(self.end_show_anim)
            msg += 'self.show_anim_name: %s \n' % str(self.show_anim_name)
            msg += 'stack: \n'
            msg += str(traceback.format_stack())
            msg += 'exception: \n'
            msg += str(e)
            exception_hook.post_error(msg)

        global_data.emgr.display_model_end_show_anim.emit()

    def add_to_mirror(self):
        model = self.get_model()
        if not model:
            return
        else:
            if not self.support_mirror:
                return
            path = self.model_data.get('mpath')
            sub_mesh_path_list = self.model_data.get('sub_mesh_path_list')
            if sub_mesh_path_list:
                path = sub_mesh_path_list[0]
            item_no = self.model_data.get('item_no', None)
            remove_socket_list = None
            if item_no:
                item_conf = confmgr.get('lobby_item', str(item_no))
                if item_conf:
                    remove_socket_list = item_conf.get('remove_socket_list', [])
            global_data.emgr.add_model_to_mirror.emit(model, path, remove_socket_list)
            return

    def play_end_anim_list(self, *args):
        self.allow_rotate = True
        model = self.get_model()
        if not model:
            return False
        if self.cur_play_anim_idx >= len(self.end_ani_list):
            self.cur_play_anim_idx = 0
        transit_time = 0 if global_data.book_gesture_no_transit_time else 300
        anim_info = self.end_ani_list[self.cur_play_anim_idx]
        self.play_animation(model, anim_info['anim'], transit_time, world.TRANSIT_TYPE_DELAY, 0, False)
        try:
            model.unregister_event(self.play_end_anim_list, anim_info['trigger'], anim_info['anim'])
            model.register_anim_key_event(anim_info['anim'], anim_info['trigger'], self.play_end_anim_list)
        except TypeError:
            pass

        self.cur_play_anim_idx += 1
        return True

    def play_bond_effect(self, role_id, dialog_id):
        block_anim_and_sfx = confmgr.get('ui_animate_sound', 'block_anim_and_sfx', 'Content', str(role_id), 'skins', default=[])
        if self.model_data.get('skin_id', None) in block_anim_and_sfx:
            return
        else:
            model = self.get_model()
            if not model:
                return
            dialog_conf = confmgr.get('role_dialog_config', 'role_{}_dialog'.format(role_id), 'Content', str(dialog_id), default={})
            animate_sound_map = confmgr.get('ui_animate_sound', str(role_id), 'Content', str(dialog_conf.get('anim_sound_id', '')), default={})
            if not animate_sound_map:
                return
            voice_info = dialog_conf.get('voice', {})
            sfx_info = dialog_conf.get('sfx', {})
            self.clear_bond_sfxes()
            self.unregister_bond_effect_event()
            anim_info = {}
            anim_name = animate_sound_map['anima']
            self.temp_bond_effect_info[anim_name] = anim_info
            for trigger, info in six.iteritems(voice_info):
                if trigger not in anim_info:
                    anim_info[trigger] = []
                anim_info[trigger].append(info)

            for trigger, info in six.iteritems(sfx_info):
                if trigger not in anim_info:
                    anim_info[trigger] = []
                anim_info[trigger].append(info)

            model.unregister_event(self._end_show_anim, 'end', anim_name)
            for trigger, info_list in six.iteritems(anim_info):
                model.register_anim_key_event(anim_name, trigger, self.on_bond_anim_callback, info_list)

            model.register_anim_key_event(anim_name, 'end', self._end_show_anim)
            self.play_animation(model, anim_name, -1, world.TRANSIT_TYPE_DELAY, 0, world.PLAY_FLAG_NO_LOOP)
            return

    def unregister_bond_effect_event(self):
        if not self.temp_bond_effect_info:
            return
        model = self.get_model()
        if not model:
            return
        for anim_name, anim_info in six.iteritems(self.temp_bond_effect_info):
            for trigger, info in six.iteritems(anim_info):
                model.unregister_event(self.on_bond_anim_callback, trigger, anim_name)

        self.temp_bond_effect_info = {}

    def clear_bond_sfxes(self):
        for sfx in self._bond_temp_sfxes:
            global_data.sfx_mgr.shutdown_sfx(sfx)

    def on_bond_anim_callback(self, model, anim_name, trigger, info_list):
        for i, info in enumerate(info_list):
            if type(info) == list:
                if not model.has_socket(info[0]):
                    continue

                def create_cb(sfx):
                    self._bond_temp_sfxes.append(sfx)

                try:
                    global_data.sfx_mgr.create_sfx_on_model(info[1], model, info[0], on_create_func=create_cb)
                except:
                    log_error('on_bond_anim_callback socket error!', 'model: {} socket:{} sfx:{}'.format(model.filename, info[0], info[1]))

            else:
                global_data.emgr.play_voice_by_uid.emit('HumanVoice', info)

    def play_show_anim(self, show_anim_ban_rotate=True):
        model = self.get_model()
        if not model or not model.valid:
            return
        else:
            if self.create_callback:
                self.create_callback(model)
            if not model or not model.valid:
                return
            if self._is_reflect:
                self.add_to_mirror()
            if not self.is_play_show_anim:
                return
            if self.is_human and not G_IS_NA_PROJECT:
                self.is_play_show_anim = False
            mecha_pose = self.model_data.get('mecha_pose', None)
            if mecha_pose:
                kwargs = {}
                skin_id = self.model_data.get('skin_id', None)
                if skin_id:
                    kwargs['skin_id'] = get_main_skin_id(skin_id)
                self.show_anim_name = iutils.get_lobby_item_res_path(mecha_pose, **kwargs)
                self.end_anim_name = iutils.get_lobby_item_res_path(mecha_pose, **kwargs)
            try:
                if not model.has_anim(self.show_anim_name):
                    self.show_anim_name = 'stand_idle'
                    if not model.has_anim(self.show_anim_name):
                        self.end_show_anim()
                        return
            except Exception as e:
                import traceback
                import exception_hook
                msg = 'PartModelDisplay line:723, def show_anim \n'
                msg += 'self.end_anim_name: %s \n' % str(self.end_anim_name)
                msg += 'self.show_anim_name: %s \n' % str(self.show_anim_name)
                msg += 'callback: %s \n' % str(self.create_callback)
                msg += 'stack: \n'
                msg += str(traceback.format_stack())
                msg += 'exception: \n'
                msg += str(e)
                exception_hook.post_error(msg)
                return

            if show_anim_ban_rotate and self.show_anim_name != self.end_anim_name:
                self.allow_rotate = False
            else:
                self.init_spring_anim()
            model.cache_animation(self.show_anim_name, world.CACHE_ANIM_ALWAYS)
            self.play_animation(model, self.show_anim_name)
            if self.chuchang_trk:
                self._trk_player = CameraTrkPlayer()
                self._trk_player.auto_play_track(self.chuchang_trk, None, finish_callback=self.play_show_anim_callback)
            if self.model_trk:
                self.play_model_trk(self.model_trk, callback=self._model_trk_callback)
            if self.end_show_anim:
                model.unregister_event(self.end_show_anim, 'end', self.show_anim_name)
                model.register_anim_key_event(self.show_anim_name, 'end', self.end_show_anim)
            if hasattr(self.parent, 'trigger_bw_effect'):
                model.unregister_event(self.parent.trigger_bw_effect, 'trigger_bw_effect', self.show_anim_name)
                model.register_anim_key_event(self.show_anim_name, 'trigger_bw_effect', self.parent.trigger_bw_effect)
            if hasattr(self.parent, 'restore_bw_effect'):
                model.unregister_event(self.parent.restore_bw_effect, 'restore_bw_effect', self.show_anim_name)
                model.register_anim_key_event(self.show_anim_name, 'restore_bw_effect', self.parent.restore_bw_effect)
            if self.show_anim_name == 'stand_show_20_2001':
                objlist = [
                 model]
                socketlist = ['head', 'gj_qunzi', 'weapon']
                for socket_name in socketlist:
                    objs = model.get_socket_objects(socket_name)
                    if objs:
                        objlist.append(objs[0])

                for sub_model in objlist:
                    sub_model.all_materials.set_technique(1, 'shader/vbr_toon_nx2_mobile.nfx::TShader')
                    sub_model.all_materials.set_macro('TEX_DISSOLVE_ENABLE', 'TRUE')
                    sub_model.all_materials.set_macro('CALC_FOG_ENABLE', 'FALSE')
                    sub_model.all_materials.rebuild_tech()

            mpath = self.cur_model_data.get('mpath')
            if mpath.find('/8007/') > 0 and self.show_anim_name == 'shopshow01':
                global_data.game_mgr.delay_exec(1.4, lambda : self.set_model_alpha(model))
            return

    @ext_do_nothing_when_not_default_skin
    def play_specific_anim(self, anim_name, is_back_to_end_show_anim=True, *args):
        if self.bag_model_path and not self.had_loaded_bag:
            return
        if self.bag_model_path2 and not self.had_loaded_bag2:
            return
        model = self.get_model()
        if not model:
            return
        if not model.has_anim(anim_name):
            if self.mecha_socket_res_agent:
                self.mecha_socket_res_agent.check_exit_anim_appearance(model.cur_anim_name)
            if self.shadow_model and self.shadow_model.valid:
                if self.shadow_mecha_socket_res_agent:
                    self.shadow_mecha_socket_res_agent.check_exit_anim_appearance(self.shadow_model.cur_anim_name)
            return
        self.play_animation(model, anim_name, *args)
        if is_back_to_end_show_anim:
            model.unregister_event(self.end_show_anim, 'end', anim_name)
            model.register_anim_key_event(anim_name, 'end', self.end_show_anim)

    @ext_do_nothing_when_not_default_skin
    def end_specific_anim(self, anim_name, is_back_to_end_show_anim=True, *args):
        if not anim_name:
            anim_name = self.end_anim_name or 'stand_idle'
        init_time = 10000000
        if not args:
            args = [
             0, -1, init_time, 0, 1.0]
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        self.play_specific_anim(anim_name, is_back_to_end_show_anim, *args)
        return

    def on_track_update_camera(self, *args):
        if not self._trk_player:
            return
        transform, fov = self._trk_player.on_track_update()
        translation = transform.translation
        if self._trk_player._camera_init_position:
            translation = self._trk_player._camera_init_position + transform.translation
        rotation = transform.rotation
        yaw = math.degrees(rotation.yaw)
        roll = math.degrees(rotation.roll)
        roll = -roll
        euler = math3d.vector(roll, yaw, roll)
        rotation = math3d.euler_to_matrix(euler)
        if self._trk_player._camera_init_rotation:
            rotation = self._trk_player._camera_init_rotation * rotation
        global_data.emgr.change_model_display_scene_cam_trans.emit(translation, rotation, False)
        if self._trk_player._is_finish:
            return RELEASE

    def on_track_update_model(self, *args):
        import common.utils.timer as timer
        if not self._model_trk_player:
            return timer.RELEASE
        model = self.get_model()
        if not model:
            return
        transform, fov = self._model_trk_player.on_track_update()
        translation = transform.translation
        if self._model_trk_init_position:
            translation = self._model_trk_init_position + transform.translation
        rotation = transform.rotation
        kan_rot = rotation
        model.world_position = translation
        model.rotation_matrix = kan_rot
        if self._model_trk_player._is_finish:
            self.cur_euler_rot = math3d.matrix_to_euler(rotation)
            self.target_euler_rot = self.cur_euler_rot
            inverse_rot_mtx = math3d.matrix(self.off_euler_rot_mtx)
            inverse_rot_mtx.inverse()
            self.cur_euler_rot = math3d.matrix_to_euler(inverse_rot_mtx * math3d.euler_to_matrix(self.target_euler_rot))
            self.target_euler_rot = self.cur_euler_rot
            if self.is_slerp:
                self.last_model_pos = translation + self.mode_center_pos * self._model.rotation_matrix
                self.model_pos = self.last_model_pos
            else:
                self.last_model_pos = translation + self.mode_center_pos * self._model.rotation_matrix
                self.model_pos = self.last_model_pos
            return timer.RELEASE

    def set_model_cast_shadow(self, model):
        result = global_data.emgr.get_lobby_scene_type_event.emit()
        scene_type = ''
        if result:
            scene_type = result[0]
        is_cast_shadow = lobby_model_display_utils.is_scene_surpport_rel_shadow(scene_type)
        model.cast_shadow = is_cast_shadow

    def change_model_off_position(self, off_position=[
 0, 0, 0], is_slerp=False):
        model = self.get_model()
        if not model:
            self.off_position_cache = (
             off_position, is_slerp)
            return
        else:
            box_position = None
            if self.real_box_name:
                box_name = self.real_box_name if 1 else self.parent.scene_data.get(self.show_box_name)
                if box_name:
                    box_position = self.parent.get_box_position(box_name)
                if not box_position:
                    return
                self.is_slerp = is_slerp
                off_position = math3d.vector(*off_position)
                if is_slerp or self.by_mecha_chuchang:
                    model.world_position = math3d.vector(0, 0, 0) + off_position
                else:
                    model.world_position = box_position + off_position
            self.model_pos = box_position + off_position
            return

    def check_glide(self, model, item_no):
        if confmgr.get('lobby_item', str(item_no), 'belong_id', default=None) == 1051668:
            if model.has_socket('tail_l') and model.has_socket('tail_r'):
                socket_objects = model.get_socket_objects('tail_l') + model.get_socket_objects('tail_r')
                for obj in socket_objects:
                    obj.visible = False

            elif model.has_socket('fx_root'):
                glide_h_model = model.get_socket_obj('fx_root')
                if glide_h_model.has_socket('tail_l') and glide_h_model.has_socket('tail_r'):
                    socket_objects = glide_h_model.get_socket_objects('tail_l') + glide_h_model.get_socket_objects('tail_r')
                    for obj in socket_objects:
                        obj.visible = False

        return

    def _load_improved_skin_model_and_effect(self, model, improved_skin_sfx_id, need_clear, load_head=False):
        need_clear and self.clear_skin_model_and_effect()
        lod_level = 'l' if self.model_data.get('is_l_model', False) else 'h'
        load_improved_skin_model_and_effect(model, improved_skin_sfx_id, auto_load_trigger_at_intervals_res=True, lod_level=lod_level)
        head_id = get_improve_skin_head_id(improved_skin_sfx_id)
        clear_head = self.improved_head and not head_id
        if clear_head:
            self.clear_improved_head()
        self.improved_head = bool(head_id)
        if load_head and head_id:
            head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list = dress_utils.get_pendant_head_path(head_id, self.model_data['skin_id'])
            self.change_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list)
        self.init_spring_anim()

    def on_load_model_complete(self, data, model, *args):
        if not self.parent:
            self.clear_model()
            return
        else:
            self.is_slerp = False
            self._model = model
            scn = self.parent.scene()
            if not scn:
                self.clear_model()
                return
            if not self.parent.scene_data and not self.real_box_name:
                self.clear_model()
                return
            box_position = None
            if self.real_box_name:
                box_name = self.real_box_name if 1 else self.parent.scene_data.get(self.show_box_name)
                if box_name:
                    box_position = self.parent.get_box_position(box_name)
                if not box_position:
                    self.clear_model()
                    return
                scn.add_object(model)
                model.all_materials.set_macro('TOP_LIGHT_ENABLE', 'TRUE')
                model.all_materials.set_macro('BACK_LIGHT_ENABLE', 'TRUE')
                model.all_materials.rebuild_tech()
                off_position = math3d.vector(*data.get('off_position', [0, 0, 0]))
                if self.by_mecha_chuchang:
                    model.world_position = math3d.vector(0, 0, 0) + off_position
                else:
                    model.world_position = box_position + off_position
                self.set_model_cast_shadow(model)
                model.receive_shadow = True
                if self.is_human or is_model_need_outline(model.filename):
                    enable_outline(model)
                if self.is_human:
                    self.init_human_model()
                else:
                    self.add_panel_shadow()
                    self.load_emoji(False)
                if self.model_data.get('show_sfx_model', False):
                    self.add_sfx_model()
                scale = data.get('model_scale', 1)
                if self.by_mecha_chuchang:
                    scale = 1
                rot_dx, rot_dy, rot_dz = data.get('off_euler_rot', [0, 0, 0])
                self.off_euler_rot_mtx = math3d.euler_to_matrix(math3d.vector(math.pi * rot_dx / 180, math.pi * rot_dy / 180, math.pi * rot_dz / 180))
                self._model.rotation_matrix = self.off_euler_rot_mtx
                model.scale = math3d.vector(scale, scale, scale)
                self.by_mecha_chuchang or mecha_utils.check_need_flip(model)
            self.model_pos = box_position + off_position
            follow_center_pos = data.get('follow_center_pos')
            if follow_center_pos:
                self.mode_center_pos = (model.center + math3d.vector(*follow_center_pos)) * scale
            else:
                self.mode_center_pos = math3d.vector(0, 0, 0)
            self.reset_rotate_model()
            self.show_anim_name = data.get('show_anim', None)
            self.end_anim_name = data.get('end_anim', None)
            self.end_ani_list = data.get('end_ani_list', None)
            self.end_anim_name_loop_time = data.get('end_anim_loop_time', 0)
            self.move_ani_name = data.get('move_anim', None)
            self.chuchang_trk = data.get('chuchang_trk', None)
            self.model_trk = data.get('model_trk', None)
            self.is_play_show_anim = self.show_anim_name is not None
            self.play_show_anim_callback = data.get('play_show_anim_callback', None)
            self.zoom_in_camera = data.get('zoom_in_camera', 0)
            sub_mesh_path_list = data.get('sub_mesh_path_list')
            if sub_mesh_path_list:
                submesh_cnt = model.get_submesh_count()
                for index in range(submesh_cnt):
                    model.set_submesh_hitmask(index, world.HIT_SKIP)

            if self.is_human:
                improved_skin_sfx_id = data.get('improved_skin_sfx_id', None)
                if improved_skin_sfx_id:
                    self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, False)
            else:
                if self.is_mecha:
                    skin_id = data.get('skin_id')
                    if skin_id:
                        shiny_preview = data.get('shiny_preview', None)
                        shiny_weapon_id = data.get('shiny_weapon_id', None)
                        shiny_weapon_id = shiny_preview if shiny_preview else shiny_weapon_id
                        self.mecha_socket_res_agent.load_skin_model_and_effect(model, skin_id, shiny_weapon_id)
                        self._fix_shadow_follow_model_res_appearance()
                self.show_model()
                self.play_show_anim(data.get('show_anim_ban_rotate', True))
            if not model or not model.valid:
                return
            self.socket_model = socket_model = data.get('socket_model')
            if socket_model:
                for socket_name, model_conf in six.iteritems(socket_model):
                    if type(model_conf) not in (list, tuple):
                        model_conf = [
                         model_conf]
                    for model_conf_ in model_conf:
                        res_type = 'MODEL'
                        if type(model_conf_) in (dict,):
                            model_path = model_conf_.get('model_path', '')
                            res_type = model_conf_.get('res_type', 'MODEL')
                        else:
                            model_path = model_conf_
                        socket_model_name = 'socket_model_%s' % socket_name
                        self.socket_model_names.append(socket_model_name)
                        resloader.load_res_attr(self, socket_model_name, model_path, self.on_load_socket_model_complete, (
                         socket_name, model_conf_), res_type=res_type, priority=game3d.ASYNC_HIGH)

            item_no = data.get('item_no')
            if item_no and not global_data.battle:
                self.register_sound(item_no)
                self.register_loop_sound(item_no)
            self.check_glide(model, item_no)
            if model.visible:
                self.play_show_anim(data.get('show_anim_ban_rotate', True))
                if self.need_correct_show_anim_phase:
                    for model_obj in self.parent.model_objs:
                        if model_obj is self:
                            continue
                        other_model = model_obj.get_model()
                        if other_model and model_obj.show_anim_name:
                            anim_ctrl = other_model.get_anim_ctrl(world.ANIM_TYPE_SKELETAL)
                            self_anim_ctrl = model.get_anim_ctrl(world.ANIM_TYPE_SKELETAL)
                            self_anim_ctrl.set_anim_time(anim_ctrl.get_anim_time(self.show_anim_name), self.show_anim_name)
                            break

            global_data.emgr.lobby_high_model_changed.emit(model)
            global_data.game_mgr.delay_exec(0.2, lambda : global_data.emgr.lobby_high_model_changed_for_editor.emit(model))
            if self.item_type == L_ITEM_YTPE_VEHICLE_SKIN:
                self.load_weapon_model()
            self.set_model_alpha(model)
            self.update_rt_model_status(model)
            if self._assure_socket is not None:
                model.get_socket_obj(self._assure_socket)
            decal_list = data.get('decal_list', {})
            decal_lod = data.get('decal_lod', 0)
            if decal_list:
                self.load_decal_data(decal_list, decal_lod=decal_lod)
            self.need_decal = len(decal_list) > 0
            color_dict = data.get('color_dict', {})
            if color_dict:
                self.load_color_data(color_dict)
            self.need_color = len(color_dict) > 0
            if global_data.is_ue_model:
                model.mirror_reflect = self.get_mirror_reflect_enable(global_data.game_mgr.gds.get_actual_quality())
            self.set_model_alpha(model)
            model.set_cam_effect_enable(True)
            if self._load_cb:
                self._load_cb(self)
            self.on_update(0)
            if self.off_position_cache:
                self.change_model_off_position(*self.off_position_cache)
                self.off_position_cache = None
            return

    def get_mecha_config(self, key):
        item_id = self.model_data.get('item_no')
        item_id = iutils.get_lobby_item_belong_no(item_id)
        mecha_id = mecha_lobby_id_2_battle_id(item_id)
        mecha_conf = confmgr.get('mecha_conf', key, 'Content')
        mechainfo = mecha_conf.get(str(mecha_id))
        if mechainfo:
            mechainfo['mecha_id'] = mecha_id
        return mechainfo

    def load_weapon_model(self):
        mecha_model = self.get_model()
        if not mecha_model:
            return
        else:
            mechainfo = self.get_mecha_config('MechaConfig')
            if not mechainfo:
                return
            add_gun_model = mechainfo.get('add_gun_model', 0)
            if not add_gun_model:
                return
            gun_ids = mechainfo.get('guns', None)
            if not gun_ids:
                return
            weap_fiream_res_conf = confmgr.get('firearm_res_config', str(gun_ids[0]), default={})
            if not weap_fiream_res_conf:
                return
            res_path = weap_fiream_res_conf.get('cRes', None)
            if not res_path:
                return
            path = get_mecha_weapon_model_path(mechainfo['mecha_id'], self.model_data.get('item_no'))
            if path:
                res_path = path
            bind_point = weap_fiream_res_conf.get('cBindPoint', None)
            if bind_point:
                global_data.model_mgr.create_model(res_path, on_create_func=self._weapon_model_load_callback)
            else:
                self._load_body_mesh_task = global_data.model_mgr.create_mesh_async(self._load_body_mesh_task, res_path, mecha_model, self._weapon_model_load_callback)
            return

    def _weapon_model_load_callback(self, weapon_model):
        mecha_model = self.get_model()
        if not mecha_model:
            return
        else:
            mechainfo = self.get_mecha_config('MechaConfig')
            if not mechainfo:
                return
            gun_ids = mechainfo.get('guns', None)
            if not gun_ids:
                return
            weap_fiream_res_conf = confmgr.get('firearm_res_config', str(gun_ids[0]), default={})
            if not weap_fiream_res_conf:
                return
            bind_point = weap_fiream_res_conf.get('cBindPoint', None)
            if bind_point:
                mecha_model.bind(bind_point, weapon_model)
            return

    def add_collision(self):
        if not self.is_human:
            return
        else:
            model = self.get_model()
            if not model:
                return
            if not self.hit_model:
                role_id = self.model_data.get('role_id')
                hit_model = world.model('character/11/hit/hit_lobby.gim', None)
                hit_model.set_parent(self.get_model())
                hit_model.inherit_flag &= ~world.INHERIT_VISIBLE
                hit_model.visible = False
                if self._cur_anim_args:
                    hit_model.play_animation(*self._cur_anim_args)
                self.hit_model = hit_model
            return

    @ext_do_nothing_when_not_default_skin
    def load_emoji(self, is_human=True):
        model = self.get_model()
        if not model:
            return
        else:
            emoji_id = self.model_data.get('emoji_id', None)
            mecha_skin_no = self.model_data.get('mecha_skin_no', None)
            if emoji_id:
                self.emoji_model_id = interaction_utils.load_emoji(weakref.ref(model), emoji_id, self.on_create_emoji_cb, is_human, mecha_skin_no)
                emoji_duraction = interaction_utils.get_emoji_duration(emoji_id)
                if self.emoji_auto_close:
                    self.emoji_update_timer_id = global_data.game_mgr.register_logic_timer(self.play_emoji_close, emoji_duraction, times=1, mode=CLOCK)
            return

    def init_human_model(self):
        model = self.get_model()
        model.visible = False
        self.load_head_model(is_init=True)
        self.bag_model_path = self.model_data.get('bag_model_path')
        self.bag_socket_name = self.model_data.get('bag_socket_name')
        self.load_bag_model(self.bag_model_path, self.bag_socket_name, is_init=True)
        self.bag_model_path2 = self.model_data.get('bag_model_path2')
        self.bag_socket_name2 = self.model_data.get('bag_socket_name2')
        self.load_bag_model(self.bag_model_path2, self.bag_socket_name2, is_init=True)
        self.init_other_pendant_model()

    def on_create_emoji_cb(self, emoji_model):
        self.emoji_model = emoji_model
        interaction_utils.set_material_type(self.emoji_model, 'mall_display')
        self.play_emoji_open()
        self.set_emoji_properties()

    def set_emoji_properties(self):
        emoji_scale = self.model_data.get('emoji_scale', None)
        if emoji_scale:
            _HASH_scale = game3d.calc_string_hash('Scale')
            self.emoji_model.all_materials.set_var(_HASH_scale, 'Scale', emoji_scale)
        emoji_offset_y = self.model_data.get('emoji_offset_y', None)
        if emoji_offset_y:
            self.emoji_model.position = math3d.vector(0, emoji_offset_y, 0)
        return

    def play_emoji_open(self):
        bind_model = self.get_model()
        emoji_id = self.model_data.get('emoji_id')
        interaction_utils.play_emoji_open(self.emoji_model, bind_model, not self.is_mecha, emoji_id, self.play_emoji_idle)
        self.emoji_sfx_id = interaction_utils.play_emoji_sfx_open(bind_model, not self.is_mecha, emoji_id, 'mall_display')

    def play_emoji_idle(self, *args):
        global_data.sfx_mgr.remove_sfx_by_id(self.emoji_sfx_id)
        bind_model = self.get_model()
        emoji_id = self.model_data.get('emoji_id')
        interaction_utils.play_emoji_idle(self.emoji_model, bind_model, not self.is_mecha, emoji_id)
        self.emoji_sfx_id = interaction_utils.play_emoji_sfx_idle(bind_model, not self.is_mecha, emoji_id, 'mall_display')

    def play_emoji_close(self):
        global_data.sfx_mgr.remove_sfx_by_id(self.emoji_sfx_id)
        if self.emoji_model and self.emoji_model.valid:
            interaction_utils.play_emoji_close(self.emoji_model, Functor(self.delay_remove_emoji_by_id, self.emoji_model_id))

    def delay_remove_emoji_by_id(self, emoji_id, *args):

        def cb():
            if self.emoji_model_id == emoji_id:
                self.remove_emoji()

        game3d.delay_exec(1, cb)

    def load_head_model--- This code section failed: ---

1465       0  LOAD_GLOBAL           0  'has_skin_ext'
           3  CALL_FUNCTION_0       0 
           6  POP_JUMP_IF_TRUE    165  'to 165'

1466       9  LOAD_CONST            0  ''
          12  LOAD_FAST             0  'self'
          15  STORE_ATTR            2  'head_pendant_type_new'

1467      18  LOAD_CONST            0  ''
          21  LOAD_FAST             0  'self'
          24  STORE_ATTR            3  'head_res_path_new'

1468      27  LOAD_CONST            0  ''
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            4  'pendant_socket_name_new'

1469      36  LOAD_CONST            0  ''
          39  LOAD_FAST             0  'self'
          42  STORE_ATTR            5  'pendant_socket_res_path_new'

1470      45  LOAD_CONST            0  ''
          48  LOAD_FAST             0  'self'
          51  STORE_ATTR            6  'pendant_random_anim_list'

1472      54  LOAD_FAST             0  'self'
          57  LOAD_ATTR             7  'ext_can_show_model'
          60  POP_JUMP_IF_FALSE   324  'to 324'

1473      63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             8  'model_data'
          69  LOAD_ATTR             9  'get'
          72  LOAD_CONST            1  'pendant_socket_res_path'
          75  CALL_FUNCTION_1       1 
          78  STORE_FAST            8  'pendant_socket_res_path_new'

1474      81  LOAD_FAST             8  'pendant_socket_res_path_new'
          84  POP_JUMP_IF_FALSE   162  'to 162'
          87  LOAD_GLOBAL          10  'C_file'
          90  LOAD_ATTR            11  'find_res_file'
          93  LOAD_FAST             8  'pendant_socket_res_path_new'
          96  LOAD_CONST            2  ''
          99  CALL_FUNCTION_2       2 
       102_0  COME_FROM                '84'
         102  POP_JUMP_IF_FALSE   162  'to 162'

1475     105  LOAD_FAST             8  'pendant_socket_res_path_new'
         108  LOAD_FAST             0  'self'
         111  STORE_ATTR            5  'pendant_socket_res_path_new'

1476     114  LOAD_FAST             0  'self'
         117  LOAD_ATTR             8  'model_data'
         120  LOAD_ATTR             9  'get'
         123  LOAD_CONST            3  'pendant_socket_name'
         126  CALL_FUNCTION_1       1 
         129  LOAD_FAST             0  'self'
         132  STORE_ATTR            4  'pendant_socket_name_new'

1477     135  LOAD_FAST             0  'self'
         138  LOAD_ATTR             8  'model_data'
         141  LOAD_ATTR             9  'get'
         144  LOAD_CONST            4  'pendant_random_anim_list'
         147  CALL_FUNCTION_1       1 
         150  LOAD_FAST             0  'self'
         153  STORE_ATTR            6  'pendant_random_anim_list'
         156  JUMP_ABSOLUTE       162  'to 162'
         159  JUMP_ABSOLUTE       324  'to 324'
         162  JUMP_FORWARD        159  'to 324'

1479     165  LOAD_FAST             6  'by_change'
         168  POP_JUMP_IF_FALSE   219  'to 219'

1480     171  LOAD_FAST             1  'head_pendant_type'
         174  LOAD_FAST             0  'self'
         177  STORE_ATTR            2  'head_pendant_type_new'

1481     180  LOAD_FAST             2  'head_res_path'
         183  LOAD_FAST             0  'self'
         186  STORE_ATTR            3  'head_res_path_new'

1482     189  LOAD_FAST             3  'pendant_socket_name'
         192  LOAD_FAST             0  'self'
         195  STORE_ATTR            4  'pendant_socket_name_new'

1483     198  LOAD_FAST             4  'pendant_socket_res_path'
         201  LOAD_FAST             0  'self'
         204  STORE_ATTR            5  'pendant_socket_res_path_new'

1484     207  LOAD_FAST             5  'pendant_random_anim_list'
         210  LOAD_FAST             0  'self'
         213  STORE_ATTR            6  'pendant_random_anim_list'
         216  JUMP_FORWARD        105  'to 324'

1486     219  LOAD_FAST             0  'self'
         222  LOAD_ATTR             8  'model_data'
         225  LOAD_ATTR             9  'get'
         228  LOAD_CONST            5  'head_pendant_type'
         231  CALL_FUNCTION_1       1 
         234  LOAD_FAST             0  'self'
         237  STORE_ATTR            2  'head_pendant_type_new'

1487     240  LOAD_FAST             0  'self'
         243  LOAD_ATTR             8  'model_data'
         246  LOAD_ATTR             9  'get'
         249  LOAD_CONST            6  'head_res_path'
         252  CALL_FUNCTION_1       1 
         255  LOAD_FAST             0  'self'
         258  STORE_ATTR            3  'head_res_path_new'

1488     261  LOAD_FAST             0  'self'
         264  LOAD_ATTR             8  'model_data'
         267  LOAD_ATTR             9  'get'
         270  LOAD_CONST            3  'pendant_socket_name'
         273  CALL_FUNCTION_1       1 
         276  LOAD_FAST             0  'self'
         279  STORE_ATTR            4  'pendant_socket_name_new'

1489     282  LOAD_FAST             0  'self'
         285  LOAD_ATTR             8  'model_data'
         288  LOAD_ATTR             9  'get'
         291  LOAD_CONST            1  'pendant_socket_res_path'
         294  CALL_FUNCTION_1       1 
         297  LOAD_FAST             0  'self'
         300  STORE_ATTR            5  'pendant_socket_res_path_new'

1490     303  LOAD_FAST             0  'self'
         306  LOAD_ATTR             8  'model_data'
         309  LOAD_ATTR             9  'get'
         312  LOAD_CONST            4  'pendant_random_anim_list'
         315  CALL_FUNCTION_1       1 
         318  LOAD_FAST             0  'self'
         321  STORE_ATTR            6  'pendant_random_anim_list'
       324_0  COME_FROM                '216'
       324_1  COME_FROM                '162'

1492     324  LOAD_FAST             0  'self'
         327  LOAD_ATTR             3  'head_res_path_new'
         330  LOAD_CONST            0  ''
         333  COMPARE_OP            8  'is'
         336  POP_JUMP_IF_FALSE   527  'to 527'

1493     339  LOAD_FAST             0  'self'
         342  LOAD_ATTR             8  'model_data'
         345  LOAD_ATTR             9  'get'
         348  LOAD_CONST            7  'mpath'
         351  CALL_FUNCTION_1       1 
         354  STORE_FAST            9  'mpath'

1494     357  LOAD_FAST             9  'mpath'
         360  LOAD_ATTR            12  'find'
         363  LOAD_CONST            8  '.gim'
         366  CALL_FUNCTION_1       1 
         369  LOAD_CONST            9  1
         372  BINARY_SUBTRACT  
         373  STORE_FAST           10  'index'

1495     376  LOAD_FAST            10  'index'
         379  LOAD_CONST           10  -1
         382  COMPARE_OP            3  '!='
         385  POP_JUMP_IF_FALSE   507  'to 507'

1497     388  LOAD_FAST             9  'mpath'
         391  LOAD_FAST            10  'index'
         394  BINARY_SUBSCR    
         395  STORE_FAST           11  'lod_level'

1498     398  LOAD_FAST            11  'lod_level'
         401  LOAD_CONST           11  'y'
         404  COMPARE_OP            2  '=='
         407  POP_JUMP_IF_FALSE   459  'to 459'

1499     410  LOAD_CONST           12  'empty'
         413  STORE_FAST           11  'lod_level'

1500     416  LOAD_FAST             0  'self'
         419  LOAD_ATTR             8  'model_data'
         422  LOAD_CONST           13  'sub_mesh_path_list'
         425  BINARY_SUBSCR    
         426  LOAD_CONST           14  ''
         429  BINARY_SUBSCR    
         430  STORE_FAST           12  'mesh_path'

1501     433  LOAD_FAST            12  'mesh_path'
         436  LOAD_FAST            12  'mesh_path'
         439  LOAD_ATTR            12  'find'
         442  LOAD_CONST            8  '.gim'
         445  CALL_FUNCTION_1       1 
         448  LOAD_CONST            9  1
         451  BINARY_SUBTRACT  
         452  BINARY_SUBSCR    
         453  STORE_FAST           13  'mesh_lod_level'
         456  JUMP_FORWARD          6  'to 465'

1503     459  LOAD_FAST            11  'lod_level'
         462  STORE_FAST           13  'mesh_lod_level'
       465_0  COME_FROM                '456'

1504     465  LOAD_FAST             9  'mpath'
         468  LOAD_ATTR            13  'replace'
         471  LOAD_CONST           15  '{}.gim'
         474  LOAD_ATTR            14  'format'
         477  LOAD_FAST            11  'lod_level'
         480  CALL_FUNCTION_1       1 
         483  LOAD_CONST           16  'parts/{}_head.gim'
         486  LOAD_ATTR            14  'format'
         489  LOAD_FAST            13  'mesh_lod_level'
         492  CALL_FUNCTION_1       1 
         495  CALL_FUNCTION_2       2 
         498  LOAD_FAST             0  'self'
         501  STORE_ATTR            3  'head_res_path_new'
         504  JUMP_ABSOLUTE       527  'to 527'

1506     507  LOAD_GLOBAL          15  'log_error'
         510  LOAD_CONST           17  '\xe4\xbc\xa0\xe8\xbf\x9b\xe6\x9d\xa5\xe4\xba\x86\xe4\xb8\xaa\xe4\xbb\x80\xe4\xb9\x88\xe9\xac\xbc\xef\xbc\x9a %s'
         513  LOAD_FAST             9  'mpath'
         516  BUILD_TUPLE_1         1 
         519  BINARY_MODULO    
         520  CALL_FUNCTION_1       1 
         523  POP_TOP          
         524  JUMP_FORWARD          0  'to 527'
       527_0  COME_FROM                '524'

1509     527  LOAD_CONST           18  'head'
         530  STORE_FAST           14  'socket_name'

1510     533  LOAD_CONST           19  'socket_model_%s'
         536  LOAD_FAST            14  'socket_name'
         539  BINARY_MODULO    
         540  STORE_FAST           15  'socket_model_name'

1511     543  LOAD_FAST             0  'self'
         546  LOAD_ATTR            16  'socket_model_names'
         549  LOAD_ATTR            17  'append'
         552  LOAD_FAST            15  'socket_model_name'
         555  CALL_FUNCTION_1       1 
         558  POP_TOP          

1513     559  LOAD_FAST             0  'self'
         562  LOAD_ATTR             3  'head_res_path_new'
         565  LOAD_GLOBAL          18  'NO_HEAD_MODEL'
         568  COMPARE_OP            6  'in'
         571  POP_JUMP_IF_FALSE   586  'to 586'

1514     574  LOAD_CONST           20  'invalidres/model.gim'
         577  LOAD_FAST             0  'self'
         580  STORE_ATTR            3  'head_res_path_new'
         583  JUMP_FORWARD          0  'to 586'
       586_0  COME_FROM                '583'

1516     586  LOAD_GLOBAL          19  'resloader'
         589  LOAD_ATTR            20  'load_res_attr'

1517     592  LOAD_FAST             0  'self'

1518     595  LOAD_FAST            15  'socket_model_name'

1519     598  LOAD_FAST             0  'self'
         601  LOAD_ATTR             3  'head_res_path_new'

1520     604  LOAD_FAST             0  'self'
         607  LOAD_ATTR            21  'on_load_pendant_model_complete'

1521     610  LOAD_FAST             6  'by_change'
         613  LOAD_FAST            14  'socket_name'
         616  LOAD_FAST             0  'self'
         619  LOAD_ATTR             3  'head_res_path_new'
         622  BUILD_TUPLE_3         3 
         625  LOAD_CONST           21  'res_type'

1522     628  LOAD_CONST           22  'MODEL'
         631  LOAD_CONST           23  'priority'

1523     634  LOAD_GLOBAL          22  'game3d'
         637  LOAD_ATTR            23  'ASYNC_HIGH'
         640  CALL_FUNCTION_517   517 
         643  POP_TOP          

1525     644  LOAD_FAST             7  'is_init'
         647  POP_JUMP_IF_FALSE   668  'to 668'

1526     650  LOAD_FAST             0  'self'
         653  DUP_TOP          
         654  LOAD_ATTR            24  'human_init_load_count'
         657  LOAD_CONST            9  1
         660  INPLACE_ADD      
         661  ROT_TWO          
         662  STORE_ATTR           24  'human_init_load_count'
         665  JUMP_FORWARD          0  'to 668'
       668_0  COME_FROM                '665'

1529     668  LOAD_FAST             0  'self'
         671  LOAD_ATTR             5  'pendant_socket_res_path_new'
         674  POP_JUMP_IF_FALSE   917  'to 917'

1530     677  LOAD_FAST             0  'self'
         680  LOAD_ATTR             5  'pendant_socket_res_path_new'
         683  LOAD_ATTR            25  'endswith'
         686  LOAD_CONST           24  '.sfx'
         689  CALL_FUNCTION_1       1 
         692  POP_JUMP_IF_FALSE   757  'to 757'

1531     695  LOAD_CONST            0  ''
         698  RETURN_VALUE     

1532     699  LOAD_FAST             0  'self'
         702  LOAD_ATTR            26  'get_model'
         705  CALL_FUNCTION_0       0 
         708  STORE_FAST           16  'model'

1533     711  LOAD_GLOBAL          27  'global_data'
         714  LOAD_ATTR            28  'sfx_mgr'
         717  LOAD_ATTR            29  'create_sfx_on_model'

1534     720  LOAD_FAST             0  'self'
         723  LOAD_ATTR             5  'pendant_socket_res_path_new'
         726  LOAD_FAST            16  'model'
         729  LOAD_FAST             0  'self'
         732  LOAD_ATTR             4  'pendant_socket_name_new'
         735  LOAD_CONST           25  'duration'
         738  LOAD_CONST           14  ''
         741  LOAD_CONST           26  'on_create_func'
         744  LOAD_FAST             0  'self'
         747  LOAD_ATTR            30  'create_head_sfx_callback'
         750  CALL_FUNCTION_515   515 
         753  POP_TOP          
         754  JUMP_FORWARD        133  'to 890'

1536     757  LOAD_CONST           19  'socket_model_%s'
         760  LOAD_FAST             0  'self'
         763  LOAD_ATTR             4  'pendant_socket_name_new'
         766  BINARY_MODULO    
         767  STORE_FAST           15  'socket_model_name'

1537     770  LOAD_FAST            15  'socket_model_name'
         773  LOAD_FAST             0  'self'
         776  LOAD_ATTR            16  'socket_model_names'
         779  COMPARE_OP            6  'in'
         782  POP_JUMP_IF_FALSE   804  'to 804'

1538     785  LOAD_GLOBAL          19  'resloader'
         788  LOAD_ATTR            31  'del_res_attr'
         791  LOAD_FAST             0  'self'
         794  LOAD_FAST            15  'socket_model_name'
         797  CALL_FUNCTION_2       2 
         800  POP_TOP          
         801  JUMP_FORWARD          0  'to 804'
       804_0  COME_FROM                '801'

1539     804  LOAD_FAST             0  'self'
         807  LOAD_ATTR            16  'socket_model_names'
         810  LOAD_ATTR            17  'append'
         813  LOAD_FAST            15  'socket_model_name'
         816  CALL_FUNCTION_1       1 
         819  POP_TOP          

1540     820  LOAD_GLOBAL          19  'resloader'
         823  LOAD_ATTR            20  'load_res_attr'

1541     826  LOAD_FAST             0  'self'

1542     829  LOAD_FAST            15  'socket_model_name'

1543     832  LOAD_FAST             0  'self'
         835  LOAD_ATTR             5  'pendant_socket_res_path_new'

1544     838  LOAD_FAST             0  'self'
         841  LOAD_ATTR            32  'on_load_head_pendant_model_complete'

1545     844  LOAD_FAST             6  'by_change'
         847  LOAD_FAST             0  'self'
         850  LOAD_ATTR             4  'pendant_socket_name_new'
         853  LOAD_FAST             0  'self'
         856  LOAD_ATTR             5  'pendant_socket_res_path_new'
         859  BUILD_TUPLE_3         3 
         862  LOAD_CONST           21  'res_type'

1546     865  LOAD_CONST           22  'MODEL'
         868  LOAD_CONST           23  'priority'

1547     871  LOAD_GLOBAL          22  'game3d'
         874  LOAD_ATTR            23  'ASYNC_HIGH'
         877  CALL_FUNCTION_517   517 
         880  POP_TOP          

1548     881  LOAD_GLOBAL          33  'False'
         884  LOAD_FAST             0  'self'
         887  STORE_ATTR           34  'had_loaded_head_pendant'
       890_0  COME_FROM                '754'

1549     890  LOAD_FAST             7  'is_init'
         893  POP_JUMP_IF_FALSE   917  'to 917'

1550     896  LOAD_FAST             0  'self'
         899  DUP_TOP          
         900  LOAD_ATTR            24  'human_init_load_count'
         903  LOAD_CONST            9  1
         906  INPLACE_ADD      
         907  ROT_TWO          
         908  STORE_ATTR           24  'human_init_load_count'
         911  JUMP_ABSOLUTE       917  'to 917'
         914  JUMP_FORWARD          0  'to 917'
       917_0  COME_FROM                '914'
         917  LOAD_CONST            0  ''
         920  RETURN_VALUE     

Parse error at or near `LOAD_GLOBAL' instruction at offset 711

    def create_head_sfx_callback(self, sfx, *args):
        self.head_sfx = sfx
        self.do_loaded_human_res_callback()

    @ext_do_nothing_when_no_skin_ext
    def change_head_model(self, head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list=None):
        socket_model_name = 'socket_model_head'
        resloader.del_res_attr(self, socket_model_name, True)
        setattr(self, socket_model_name, None)
        if self.head_pendant_random_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self.head_pendant_random_anim_timer)
            self.head_pendant_random_anim_timer = None
        self.head_pendant_model = None
        if self.head_sfx:
            global_data.sfx_mgr.remove_sfx(self.head_sfx)
            self.head_sfx = None
        if self.pendant_socket_res_path and self.pendant_socket_res_path.endswith('.gim'):
            socket_model_name = 'socket_model_%s' % self.pendant_socket_name
            resloader.del_res_attr(self, socket_model_name, True)
            setattr(self, socket_model_name, None)
        self.load_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list, True)
        return

    @ext_do_nothing_when_no_skin_ext
    def change_bag_model(self, pendant_id, socket_name, path, bag_socket_name2=None, bag_model_path2=None, anim_data=None):
        self.del_bag_model(self.bag_model_path, self.bag_socket_name)
        self.del_bag_model(self.bag_model_path2, self.bag_socket_name2)
        show_anim = None
        end_anim = None
        if anim_data:
            show_anim = anim_data['show_anim']
            end_anim = anim_data['end_anim']
        item_data = confmgr.get('lobby_item', str(self.model_data.get('item_no')), default={})
        show_anim = show_anim or item_data['first_ani_name']
        if not anim_data or not anim_data['use_skin_show_anim']:
            if pendant_id is not None and pendant_id != 0:
                new_data = confmgr.get('lobby_item', str(pendant_id), default={})
                if new_data.get('first_ani_name'):
                    show_anim = new_data.get('first_ani_name') if 1 else show_anim
        end_anim = end_anim or item_data['end_ani_name']
        if not anim_data or not anim_data['use_skin_end_anim']:
            if pendant_id is not None and pendant_id != 0:
                new_data = confmgr.get('lobby_item', str(pendant_id), default={})
                if new_data.get('end_ani_name'):
                    end_anim = new_data.get('end_ani_name') if 1 else end_anim
        self.bag_model_path = path
        self.bag_socket_name = socket_name
        self.load_bag_model(self.bag_model_path, self.bag_socket_name)
        self.bag_model_path2 = bag_model_path2
        self.bag_socket_name2 = bag_socket_name2
        self.load_bag_model(self.bag_model_path2, self.bag_socket_name2)
        if self.bag_model_path:
            self.had_loaded_bag = False
        if self.bag_model_path2:
            self.had_loaded_bag2 = False
        if self.bag_model_path is None and self.bag_model_path2 is None and (self.show_anim_name != show_anim or self.end_anim_name != end_anim):
            self.show_anim_name = show_anim
            self.end_anim_name = end_anim
            self.play_show_anim()
        else:
            self.show_anim_name = show_anim
            self.end_anim_name = end_anim
        return

    def del_bag_model(self, res_path, socket_name):
        model = self.get_model()
        if not model or not model.valid:
            return
        else:
            if socket_name:
                socket_model_name = 'socket_model_%s' % socket_name
                resloader.del_res_attr(self, socket_model_name, True)
                setattr(self, socket_model_name, None)
                if socket_model_name in self.socket_model_names:
                    self.socket_model_names.remove(socket_model_name)
                self.unbind_model(model, socket_name, res_path)
                self.unbind_model(self.shadow_model, socket_name, res_path)
            elif res_path is not None:
                model.remove_mesh(res_path)
                sub_mesh = 'sub_mesh_%s' % socket_name
                resloader.del_res_attr(self, sub_mesh)

                def set_alpha_callback():
                    if model and model.valid:
                        self.set_model_alpha(model)
                        enable_outline(model)

                global_data.game_mgr.register_logic_timer(set_alpha_callback, interval=1, times=15, mode=LOGIC)
            return

    @ext_do_nothing_when_no_skin_ext_v2
    def load_bag_model(self, res_path=None, socket_name=None, is_init=False):
        if res_path is None:
            return
        else:
            is_bind = False
            if socket_name:
                if not self.model_data.get('is_l_model', False):
                    is_bind = True
                else:
                    is_bind = not bool(self.model_data.get('bag_pendant_l_same_gis', False))
            if is_bind:
                socket_model_name = 'socket_model_%s' % socket_name
                self.socket_model_names.append(socket_model_name)
                resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_bag_pendant_model_complete, (
                 res_path, socket_name), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            else:
                sub_mesh = 'sub_mesh_%s' % socket_name
                self.sub_mesh_names.append(sub_mesh)
                resloader.load_res_attr(self, sub_mesh, res_path, self.on_load_bag_pendant_model_complete, (
                 res_path, socket_name), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            if is_init:
                self.human_init_load_count += 1
            return

    def unbind_model(self, model, socket_name, sub_file_name=None):
        if model is not None:
            model_list = []
            try:
                model_list = model.get_socket_objects(socket_name)
            except ValueError as e:
                msg = "Model {} doesn't have socket {} ".format(model.filename, socket_name)
                exception_hook.post_stack(msg)
                return

            if not sub_file_name:
                if len(model_list) > 0:
                    part_model = model_list[0]
                    model.unbind(part_model)
                    part_model.destroy()
            else:
                for m in model_list:
                    p1 = os.path.normpath(sub_file_name).replace('\\', '/')
                    p2 = os.path.normpath(m.filename).replace('\\', '/')
                    if p1 == p2:
                        model.unbind(m)
                        m.destroy()
                        return

                log_error('unbind model failed!', model, socket_name, sub_file_name, [ m.filename for m in model_list ])
        return

    def init_spring_anim(self):
        if self.model_data and self.model_data.get('is_bond_tag'):
            return
        self.clear_spring_anim()
        model = self.get_model()
        file_name = dress_utils.get_file_name(model)
        if not file_name:
            return
        data_file = file_name + '_h'
        data = confmgr.get(data_file)
        conf = data._conf
        if not conf:
            return
        scale = model.scale.x
        if abs(scale - 1) > 0.2:
            return
        part_models = dress_utils.init_spring_anim(model, conf)
        if part_models:
            for part_model in part_models:
                part_model.get_spring_anim(True).enable_physx()

    def clear_spring_anim(self):
        model = self.get_model()
        file_name = dress_utils.get_file_name(model)
        if not file_name:
            return
        data_file = file_name + '_h'
        data = confmgr.get(data_file)
        conf = data._conf
        if not conf:
            return
        dress_utils.clear_spring_anim(model, conf)

    def register_loop_sound(self, item_no):
        loop_sound_info = confmgr.get('ui_animate_sound', 'display_loop_sound', 'Content', str(item_no), default=None)
        if not loop_sound_info:
            return
        else:
            audio_event = loop_sound_info.get('event_name', 'Play_ui_shopshow')
            switch_group = loop_sound_info.get('switch_group_name', 'ui_shopshow')
            switch_name = loop_sound_info['switch_name']
            self.cur_loop_sound_cover_bgm = loop_sound_info.get('cover_bgm', False)
            sound_mgr = global_data.sound_mgr
            if self.cur_loop_sound_id:
                sound_mgr.stop_playing_id(self.cur_loop_sound_id)
                self.cur_loop_sound_id = None
            loop_sound_obj = sound_mgr.get_display_loop_obj()
            sound_mgr.set_switch(switch_group, switch_name, loop_sound_obj)
            self.cur_loop_sound_id = sound_mgr.post_event_2d_non_opt(audio_event, loop_sound_obj)
            if self.cur_loop_sound_cover_bgm:
                if self.cur_loop_sound_id:
                    sound_mgr.set_music_volume(0)
            return

    def register_sound(self, item_no):
        from common.cfg import confmgr
        item_data = confmgr.get('lobby_item', str(item_no))
        item_type = item_data.get('type')
        item_belong_id = item_data.get('belong_id')
        cnf_id = item_no
        if item_type == L_ITEM_TYPE_ROLE_SKIN:
            cnf_id = item_belong_id
        elif item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN):
            mecha_item_id = item_no
            if item_type == L_ITEM_TYPE_MECHA_SKIN:
                mecha_item_id = item_belong_id
            cnf_id = mecha_lobby_id_2_battle_id(mecha_item_id)
        elif item_type == L_ITEM_TYPE_PET_SKIN:
            cnf_id = item_no
        model = self.get_model()
        animate_sound_map = confmgr.get('ui_animate_sound', str(cnf_id), default=None)
        if animate_sound_map:
            for _, datas in six.iteritems(animate_sound_map['Content']):
                anima = datas['anima']
                show_socket = datas.get('show_socket', '')
                if show_socket and anima not in self._show_sockets:
                    self._show_sockets[anima] = show_socket
                    model.get_socket_obj(show_socket, 0)
                if not datas.get('switch_name', None):
                    continue
                event = datas.get('event', 'show')
                audio_event = datas.get('event_name', 'Play_ui_shopshow')
                switch_group = datas.get('switch_group_name', 'ui_shopshow')
                switch_name = datas['switch_name']
                is_show_anim = datas.get('is_show_anim', 0)
                cover_bgm = datas.get('cover_bgm', 0)
                vo = datas.get('vo_param', [0, 0])
                if is_show_anim:
                    self.show_anim_sound_dict[anima] = [
                     audio_event, switch_group, switch_name, cover_bgm, vo]
                elif model.has_anim_event(anima, event):
                    callback_data = [
                     audio_event, switch_group, switch_name, cover_bgm, vo]
                    model.register_anim_key_event(anima, event, self.on_animate_sound, callback_data)

        return

    def on_animate_sound(self, p_model, anima, event, data):
        model = self.get_model()
        if not model:
            return
        else:
            if self.is_mute:
                return
            sound_mgr = global_data.sound_mgr
            audio_event, switch_group, swtich_name, cover_bgm, vo = data
            if self.cur_sound_id and (not vo[0] or not vo[1]):
                sound_mgr.stop_playing_id(self.cur_sound_id)
                self.cur_sound_id = None

            def call_back(*args):
                sound_mgr.set_music_volume(sound_mgr.get_music_volume())

            if swtich_name:
                sound_mgr.set_switch(switch_group, swtich_name, sound_mgr.get_ui_obj())
            if vo[0] and vo[1]:
                global_data.game_voice_mgr.play_voice_by_uid(vo[0], vo[1])
                return
            if cover_bgm:
                self.cur_sound_id = sound_mgr.post_event_2d(audio_event, None, callback=call_back)
                if self.cur_sound_id:
                    sound_mgr.set_music_volume(0)
            else:
                self.cur_sound_id = sound_mgr.post_event_2d_non_opt(audio_event, None)
            return

    def load_decal_data(self, decal_list, avatar_data=False, decal_lod=0):
        if self.model_data.get('second_model_tag', False):
            return
        else:
            model = self.get_model()
            skin_id = self.model_data.get('item_no', None)
            if model and skin_id:
                if avatar_data:
                    decal_list = global_data.player.get_mecha_decal().get(str(get_main_skin_id(skin_id)), [])
                elif decal_list and len(decal_list[0]) < 9:
                    decal_list = decal_utils.decode_decal_list(decal_list)
                load_model_decal_data(model, skin_id, decal_list, decal_lod)
                self.cur_model, self.cur_skin_id, self.cur_decal_list = model, skin_id, decal_list
            return

    def load_high_quality_model_decal(self):
        if self.model_data.get('second_model_tag', False):
            return
        else:
            if self.cur_model and self.cur_skin_id and self.cur_decal_list:
                load_model_decal_high_quality(self.cur_model, self.cur_skin_id, self.cur_decal_list)
                self.cur_model = self.cur_skin_id = self.cur_decal_list = None
            return

    def load_color_data(self, color_dict, avatar_data=False):
        model = self.get_model()
        skin_id = self.model_data.get('item_no', None)
        if model and skin_id:
            if avatar_data:
                color_dict = global_data.player.get_mecha_color().get(str(skin_id), {})
            elif color_dict and isinstance(color_dict, dict):
                color_dict = decal_utils.decode_color(color_dict)
            load_model_color_data(model, skin_id, color_dict)
        return

    def update_is_same_gis(self):
        role_id = self.model_data.get('role_id')
        self.is_same_gis = self.model_data.get('is_l_model', False)
        sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex')
        if sex == 0 or role_id in (111, ):
            self.is_same_gis = True

    def on_load_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        else:
            model = self.get_model()
            if not model:
                return
            socket_model_name = 'socket_model_head'
            if socket_model_name in self.socket_model_names:
                self.socket_model_names.remove(socket_model_name)
            if self.head_res_path:
                if self.is_same_gis:
                    model.remove_mesh(self.head_res_path)
                    if self.shadow_model:
                        if self.is_human:
                            self.shadow_model.all_materials.set_technique(1, 'shader/vbr_toon.nfx::TShader')
                        self.shadow_model.remove_mesh(self.head_res_path)
                else:
                    self.unbind_model(model, 'head', self.head_res_path)
                    self.unbind_model(self.shadow_model, 'head', self.head_res_path)
            if self.pendant_socket_res_path and self.pendant_socket_res_path.endswith('.gim'):
                if not self.pendant_socket_name or self.model_data.get('is_l_model', False) and self.model_data.get('head_pendant_l_same_gis', 0):
                    model.remove_mesh(self.pendant_socket_res_path)
                else:
                    socket_model_name = 'socket_model_%s' % self.pendant_socket_name
                    if socket_model_name in self.socket_model_names:
                        self.socket_model_names.remove(socket_model_name)
                    self.unbind_model(model, self.pendant_socket_name, self.pendant_socket_res_path)
                    self.unbind_model(self.shadow_model, self.pendant_socket_name, self.pendant_socket_res_path)
            by_change_head, socket_name, res_path = data
            load_model.visible = model.visible
            self.update_is_same_gis()
            if self.is_same_gis:
                if res_path != 'invalidres/model.gim':
                    model.add_mesh(res_path)
                self.set_model_alpha(model)
                enable_outline(model)
            else:
                model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
                if self._cur_anim_args is not None:
                    cur_anim = self._cur_anim_args[0]
                    if load_model.has_anim(cur_anim):
                        load_model.play_animation(cur_anim)
                self.set_model_alpha(load_model)
                enable_outline(load_model)
            self.set_model_cast_shadow(load_model)
            load_model.receive_shadow = False
            part_socket = [
             'hair']
            for socket in part_socket:
                part_model = model.get_socket_obj(socket, 0)
                if part_model:
                    self.set_model_alpha(part_model)
                    self.set_model_cast_shadow(part_model)
                    part_model.receive_shadow = True
                    enable_outline(part_model)
                    self.set_model_alpha(part_model)

            if self.pendant_socket_res_path_new and self.pendant_socket_res_path_new.endswith('.sfx'):
                model = self.get_model()
                global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path_new, model, self.pendant_socket_name_new, duration=0, on_create_func=self.create_head_sfx_callback)
            self.head_pendant_type = self.head_pendant_type_new
            self.head_res_path = self.head_res_path_new
            if by_change_head:
                self.add_human_panel_shadow()
            else:
                self.add_panel_shadow()
                self.play_show_anim()
                self.load_emoji()
            self.update_rt_model_status(load_model)
            self.do_loaded_human_res_callback()
            self.check_all_human_socket_and_pendant_loaded()
            improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
            skin_id = self.model_data.get('item_no', None)
            if improved_skin_sfx_id:
                self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, True)
            else:
                if self.model_data.get('is_l_model', None):
                    load_normal_skin_model_and_effect(model, skin_id, 'l')
                else:
                    load_normal_skin_model_and_effect(model, skin_id, 'h')
                if self.show_anim_name == self.end_anim_name:
                    self.init_spring_anim()
            return

    def update_rt_model_status(self, model):
        if self.is_render_target_model:
            socket_count = model.get_socket_count()
            for i in range(socket_count):
                socket_object_count = model.get_socket_obj_count(i)
                cur_socket_name = model.get_socket_name(i)
                for j in range(socket_object_count):
                    socket_model = model.get_socket_obj(cur_socket_name, j)
                    if hasattr(socket_model, 'get_socket_objects'):
                        self.set_model_alpha(socket_model)

    def _play_head_pendant_model_anim(self):
        if not self.pendant_random_anim_list:
            self.head_pendant_random_anim_timer = None
            return RELEASE
        else:
            if not self.head_pendant_model or not self.head_pendant_model.valid:
                self.head_pendant_random_anim_timer = None
                return RELEASE
            anim_name, min_duration, max_duration = self.pendant_random_anim_list[self.head_pendant_anim_index * 3:self.head_pendant_anim_index * 3 + 3]
            self.head_pendant_anim_index = (self.head_pendant_anim_index + 1) % 2
            duration = random.uniform(min_duration, max_duration)
            self.head_pendant_model.play_animation(anim_name)
            self.head_pendant_random_anim_timer = global_data.game_mgr.register_logic_timer(self._play_head_pendant_model_anim, interval=duration, times=1, mode=CLOCK)
            return

    def on_load_head_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        else:
            model = self.get_model()
            if not model:
                return
            by_change_head, socket_name, res_path = data
            if res_path != self.pendant_socket_res_path_new:
                return
            load_model.visible = model.visible
            if self.pendant_socket_res_path_new in ('character/20/2000/h_hat.gim',
                                                    'character/16/2000/h_hair.gim'):
                load_model.follow_same_bone_model(model)
            is_l_model = self.model_data.get('is_l_model', False)
            if not socket_name or is_l_model and self.model_data.get('head_pendant_l_same_gis', 0):
                model.add_mesh(res_path)
                enable_outline(model)
                self.set_model_alpha(model)
            else:
                model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
                if self.is_render_target_model:
                    self.update_rt_model_status(load_model)
                    self.set_model_alpha(load_model)
                enable_outline(load_model)
            self.had_loaded_head_pendant = True
            self.set_model_cast_shadow(load_model)
            load_model.receive_shadow = True
            if self.pendant_socket_res_path_new and self.pendant_socket_res_path_new.endswith('.sfx'):
                model = self.get_model()
                global_data.sfx_mgr.create_sfx_on_model(self.pendant_socket_res_path_new, model, self.pendant_socket_name_new, duration=0, on_create_func=self.create_head_sfx_callback)
            self.pendant_socket_name = self.pendant_socket_name_new
            self.pendant_socket_res_path = self.pendant_socket_res_path_new
            self.do_loaded_human_res_callback()
            self.head_pendant_model = load_model
            self.head_pendant_anim_index = 0
            self._play_head_pendant_model_anim()
            self.play_show_anim()
            improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
            if improved_skin_sfx_id:
                self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, True)
            self.check_all_human_socket_and_pendant_loaded()
            return

    def on_load_bag_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        else:
            model = self.get_model()
            if not model:
                return
            res_path, socket_name = data
            if res_path == self.bag_model_path:
                self.had_loaded_bag = True
            else:
                self.had_loaded_bag2 = True
            load_model.visible = model.visible
            is_bind = False
            if socket_name:
                if not self.model_data.get('is_l_model', False):
                    is_bind = True
                else:
                    is_bind = not bool(self.model_data.get('bag_pendant_l_same_gis', False))
            if is_bind:
                model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
                if self.is_render_target_model:
                    self.set_model_alpha(load_model)
                enable_outline(load_model)
            else:
                model.add_mesh(load_model.filename)
                enable_outline(model)
            self.set_model_cast_shadow(load_model)
            load_model.receive_shadow = True
            improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
            if improved_skin_sfx_id:
                self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, True)
            self.play_show_anim()
            self.set_model_alpha(model)
            self.do_loaded_human_res_callback()
            self.check_all_human_socket_and_pendant_loaded()
            return

    def on_load_socket_model_complete(self, load_model, socket_name_and_model_conf, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        else:
            socket_name, model_conf = socket_name_and_model_conf
            bind_type = world.BIND_TYPE_DEFAULT
            scale = None
            if type(model_conf) in (dict,):
                bind_type = model_conf.get('bind_type', world.BIND_TYPE_DEFAULT)
                scale = model_conf.get('scale', None)
            model = self.get_model()
            if not model:
                return
            model.bind(socket_name, load_model, bind_type)
            if scale:
                load_model.scale = math3d.vector(scale, scale, scale)
            if self.is_render_target_model:
                pc_platform_utils.set_model_write_alpha(load_model, True, 1.0)
            return

    def check_all_human_socket_and_pendant_loaded(self):
        self.human_init_loaded_count += 1
        if self.human_init_loaded_count >= self.human_init_load_count:
            model = self.get_model()

            def set_model_visible(model=model):
                if not model or not model.valid:
                    return
                else:
                    model.visible = True
                    if self._model_loaded_callback:
                        self._model_loaded_callback()
                        self._model_loaded_callback = None
                    return

            global_data.game_mgr.next_exec(set_model_visible)

    def reset_rotate_model(self):
        if self.by_mecha_chuchang:
            return
        model = self.get_model()
        if not model:
            return
        if self.get_view_flag():
            self.cur_euler_rot = math3d.vector(0, 0, 0)
            self.target_euler_rot = math3d.vector(0, 0, 0)
            model.rotation_matrix = self.off_euler_rot_mtx * math3d.euler_to_matrix(math3d.vector(0, 0, 0))
        else:
            self.cur_euler_rot = self.get_model_euler_rotate(0)
            self.target_euler_rot = math3d.vector(self.cur_euler_rot.x, self.cur_euler_rot.y, self.cur_euler_rot.z)
            model.rotation_matrix = self.off_euler_rot_mtx * math3d.euler_to_matrix(self.cur_euler_rot)

    def rotate_model_automatically(self, round_count, duration=5, acc_duration=1, dec_duration=1, is_right_dir=True):
        self.auto_rotate_radians = math.pi * 2 * round_count
        self.auto_rotate_duration = duration
        self.auto_rotate_acc_duration = acc_duration
        self.auto_rotate_begin_dec_time = duration - dec_duration
        self.auto_rotate_dir = -1 if is_right_dir else 1
        self.auto_rotate_speed = self.auto_rotate_radians / (duration - acc_duration * 0.5 - dec_duration * 0.5)
        self.auto_rotate_acc_speed = self.auto_rotate_speed / acc_duration
        self.auto_rotate_dec_speed = self.auto_rotate_speed / dec_duration
        self.auto_rotate_passed_time = 0

    def rotate_model(self, rotate_times):
        if not self.allow_rotate:
            return
        self.target_euler_rot = math3d.vector(0, self.target_euler_rot.y + rotate_times * math.pi * 2, 0)

    def rotate_model_by_euler(self, euler=None):
        if not self.allow_rotate:
            return
        if euler:
            euler = math3d.vector(math.pi * euler.x / 180, math.pi * euler.y / 180, math.pi * euler.z / 180)
        else:
            if type(self.off_euler_rot) == list:
                return
            euler = math3d.matrix_to_euler(self.off_euler_rot)
        if abs(euler.length - self.target_euler_rot.length) < 0.1:
            return
        self.target_euler_rot = euler
        rot_y = int(self.cur_euler_rot.y * 180) % 360 / 180
        self.cur_euler_rot = math3d.vector(0, rot_y, 0)

    def set_model_rotate_euler(self, euler):
        if not self.allow_rotate:
            return
        if euler:
            euler = math3d.vector(math.pi * euler.x / 180, math.pi * euler.y / 180, math.pi * euler.z / 180)
        else:
            if type(self.off_euler_rot) == list:
                return
            euler = math3d.matrix_to_euler(self.off_euler_rot)
        self.target_euler_rot = euler
        self.cur_euler_rot = euler

    def get_model_euler_rotate(self, index):
        euler_rot = math3d.vector(0, confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'mecha%d' % index, 'yaw'), 0)
        return euler_rot

    def on_update(self, dt):
        if self.by_mecha_chuchang:
            return
        if self.by_model_trk:
            return
        model = self.get_model()
        if model and self.get_view_flag():
            if self.auto_rotate_duration > 0:
                last_update_time = self.auto_rotate_passed_time
                self.auto_rotate_passed_time += dt
                if self.auto_rotate_passed_time > self.auto_rotate_duration:
                    self.auto_rotate_passed_time = self.auto_rotate_duration
                if self.auto_rotate_passed_time < self.auto_rotate_acc_duration:
                    begin_speed = self.auto_rotate_acc_speed * last_update_time
                    cur_frame_rotate_radians = begin_speed * dt + self.auto_rotate_acc_speed * 0.5 * dt * dt
                    self.target_euler_rot.y += cur_frame_rotate_radians * self.auto_rotate_dir
                elif self.auto_rotate_passed_time < self.auto_rotate_begin_dec_time:
                    if last_update_time < self.auto_rotate_acc_duration:
                        cur_frame_rotate_radians = 0
                        acc_duration = self.auto_rotate_acc_duration - last_update_time
                        begin_speed = self.auto_rotate_acc_speed * last_update_time
                        cur_frame_rotate_radians += begin_speed * acc_duration + self.auto_rotate_acc_speed * 0.5 * acc_duration * acc_duration
                        cur_frame_rotate_radians += self.auto_rotate_speed * (self.auto_rotate_passed_time - self.auto_rotate_acc_duration)
                    else:
                        cur_frame_rotate_radians = self.auto_rotate_speed * dt
                    self.target_euler_rot.y += cur_frame_rotate_radians * self.auto_rotate_dir
                else:
                    if last_update_time < self.auto_rotate_begin_dec_time:
                        cur_frame_rotate_radians = self.auto_rotate_speed * (self.auto_rotate_begin_dec_time - last_update_time)
                        dec_duration = self.auto_rotate_passed_time - self.auto_rotate_begin_dec_time
                        cur_frame_rotate_radians += self.auto_rotate_speed * dec_duration - self.auto_rotate_dec_speed * 0.5 * dec_duration * dec_duration
                        self.target_euler_rot.y += cur_frame_rotate_radians * self.auto_rotate_dir
                    else:
                        dec_time = self.auto_rotate_passed_time - self.auto_rotate_begin_dec_time
                        begin_speed = self.auto_rotate_speed - self.auto_rotate_dec_speed * dec_time
                        cur_frame_rotate_radians = begin_speed * dt - self.auto_rotate_dec_speed * 0.5 * dt * dt
                        self.target_euler_rot.y += cur_frame_rotate_radians * self.auto_rotate_dir
                    if self.auto_rotate_passed_time >= self.auto_rotate_duration:
                        self.auto_rotate_duration = 0
                self.cur_euler_rot = self.target_euler_rot
            else:
                self.cur_euler_rot.intrp(self.cur_euler_rot, self.target_euler_rot, 0.2)
            try:
                self._model.rotation_matrix = self.off_euler_rot_mtx * math3d.euler_to_matrix(self.cur_euler_rot)
            except TypeError as e:
                from exception_hook import post_stack
                post_stack('Matrix Error:{},local values \t\t\t\toff_euler_rot_mtx={}, cur_euler_rot={}'.format(e, self.off_euler_rot_mtx, self.cur_euler_rot))

            if self.is_slerp:
                self.last_model_pos.intrp(self.last_model_pos, self.model_pos, 0.1)
                self._model.world_position = self.last_model_pos - self.mode_center_pos * self._model.rotation_matrix
            else:
                self._model.world_position = self.model_pos - self.mode_center_pos * self._model.rotation_matrix
                self.last_model_pos = self.model_pos
            if self.sfx_model_alone and self.sfx_model:
                self.sfx_model.rotation_matrix = self._model.rotation_matrix
                self.sfx_model.world_position = self._model.world_position
            global_data.emgr.mirror_model_change_pos_rotation.emit(model)

    def play_animation(self, model, *args):
        if self.item_type in (L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN):
            skin_id = self.model_data.get('item_no', None)
            anim_screen_sfx = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), 'anim_screen_sfx', default={})
            if anim_screen_sfx:
                screen_sfx_list = anim_screen_sfx.get(args[0], [])
                if screen_sfx_list:
                    delay_sfx_list = []
                    immediate_sfx_list = []
                    for sfx in screen_sfx_list:
                        if type(sfx) == dict:
                            delay_sfx_list.append(sfx)
                        else:
                            immediate_sfx_list.append(sfx)

                    if immediate_sfx_list:
                        self.anim_screen_sfx_list = dress_utils.play_anim_screen_sfx(immediate_sfx_list)
                    if delay_sfx_list:
                        timer_regist_func = global_data.game_mgr.register_logic_timer

                        def create_sfx(sfx_list):
                            self.anim_screen_sfx_list.extend(dress_utils.play_anim_screen_sfx(sfx_list))

                        for sfx in delay_sfx_list:
                            self.anim_screen_sfx_timer_list.append(timer_regist_func(func=create_sfx, args=[sfx['sfx_list']], interval=sfx['delay'], times=1, mode=CLOCK))

        self._cur_anim_args = args
        if model == self.get_model():
            if self._showing_socket:
                model.set_socket_bound_obj_active(self._showing_socket, 0, False, False)
                self._showing_socket = ''
            show_socket = self._show_sockets.get(self._cur_anim_args[0], '')
            if show_socket:
                self._showing_socket = show_socket
                model.set_socket_bound_obj_active(show_socket, 0, True, True)
                obj = model.get_socket_obj(show_socket, 0)
                if obj:
                    obj.visible = True
        if self.mecha_socket_res_agent:
            self.mecha_socket_res_agent.cache_animation(args[0], world.CACHE_ANIM_ALWAYS)
            self.mecha_socket_res_agent.play_animation(*args)
        else:
            model.cache_animation(args[0], world.CACHE_ANIM_ALWAYS)
            model.play_animation(*args)
        if self.shadow_model:
            if self.shadow_mecha_socket_res_agent:
                self.shadow_mecha_socket_res_agent.play_animation(*args)
            else:
                self.shadow_model.play_animation(*args)
        if self.hit_model:
            self.hit_model.play_animation(*args)
        if self.sfx_model:
            self.sfx_model.play_animation(*args)
        socket_model_name = 'socket_model_head'
        socket_model = getattr(self, socket_model_name, None)
        if socket_model and socket_model.valid:
            socket_model.play_animation(*args)
        socket_model_name = 'socket_model_%s' % self.pendant_socket_name
        socket_model = getattr(self, socket_model_name, None)
        if socket_model and socket_model.valid:
            socket_model.play_animation(*args)
        if self.head_pendant_model and not self.head_pendant_random_anim_timer:
            if self.head_pendant_model.valid:
                self.head_pendant_model.play_animation(*args)
        if self.bag_socket_name:
            socket_model_name = 'socket_model_%s' % self.bag_socket_name
            socket_model = getattr(self, socket_model_name, None)
            if socket_model and socket_model.valid:
                socket_model.play_animation(*args)
        if self._cur_anim_args[0] in self.show_anim_sound_dict:
            self.on_animate_sound(None, None, None, self.show_anim_sound_dict[self._cur_anim_args[0]])
        global_data.emgr.mirror_model_play_animation.emit(model, *args)
        return

    def add_sfx_model(self):
        if self.sfx_model:
            return
        else:
            model = self.get_model()
            if not model:
                return
            path = self.model_data.get('mpath')
            sub_mesh_path_list = self.model_data.get('sub_mesh_path_list')
            if sub_mesh_path_list:
                path = sub_mesh_path_list[0]
            self.sfx_model = world.model(path, None)
            self.sfx_model.visible = False
            for i in range(self.sfx_model.get_socket_count()):
                for m in self.sfx_model.get_socket_objects(i):
                    m.destroy()

            if self.sfx_model_alone:
                self.parent.scene().add_object(self.sfx_model)
                model_scale = self.model_data.get('model_scale', 1.0)
                self.sfx_model.scale = math3d.vector(model_scale, model_scale, model_scale)
            else:
                self.sfx_model.set_parent(model)
                self.sfx_model.position = math3d.vector(0, 0, 0)
            self.sfx_model.follow_same_bone_model(model)
            m = re.match(MECHA_PATH_PATTERN, path)
            str_mecha_id = ''
            uv_tex_list = []
            if m:
                str_mecha_id = m.group(2)
                default_skin_id = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(str_mecha_id), 'skins', default=[])[0]
                uv_tex_list = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(default_skin_id), 'uv_texture', default=[])
            sfx_path = 'effect/fx/mecha/shuxing/shuxingtisheng_01.sfx'

            def create_cb(sfx):
                self.sfx_model.visible = False
                mecha_utils.check_need_flip(self.sfx_model)
                count = self.sfx_model.get_submesh_count()
                tex_count = len(uv_tex_list)
                for i in range(count):
                    mat = self.sfx_model.get_sub_material(i)
                    if i < tex_count:
                        index = i if 1 else tex_count - 1
                        if index >= 0:
                            uv_tex_path = uv_tex_list[index]
                        else:
                            uv_tex_path = 'textures/black_empty.png'
                        mat.set_texture(game3d.calc_string_hash('_UV_Tex'), '_UV_Tex', uv_tex_path)
                        mat.set_var(game3d.calc_string_hash('vertex_color_mask'), 'vertex_color_mask', (0.0,
                                                                                                        0.0,
                                                                                                        0.0,
                                                                                                        1.0))

                self.sfx_model.visible = True

            global_data.sfx_mgr.create_sfx_for_model(sfx_path, self.sfx_model, on_create_func=create_cb)
            return

    def operate_sfx_model(self, info):
        from logic.gcommon.const import MECHA_PART_MAP, MECHA_PART_HEAD
        if not self.sfx_model:
            return
        if 'vertex_color_mask' in info:
            self.sfx_model.all_materials.set_var(game3d.calc_string_hash('vertex_color_mask'), 'vertex_color_mask', info['vertex_color_mask'])
            model = self.get_model()
            if model:
                path = self.model_data.get('mpath')
                sub_mesh_path_list = self.model_data.get('sub_mesh_path_list')
                if sub_mesh_path_list:
                    path = sub_mesh_path_list[0]
                m = re.match(MECHA_PATH_PATTERN, path)
                str_mecha_id = ''
                if m:
                    str_mecha_id = m.group(2)
                    if str_mecha_id == '8001':
                        if info['vertex_color_mask'] == MECHA_PART_MAP[MECHA_PART_HEAD]:
                            self.sfx_model.render_level = 0
                        else:
                            self.sfx_model.render_level = -1

    @staticmethod
    def shadowing_model--- This code section failed: ---

2526       0  LOAD_FAST             0  'model'
           3  LOAD_ATTR             0  'all_materials'
           6  LOAD_ATTR             1  'set_technique'
           9  LOAD_CONST            1  1
          12  LOAD_CONST            2  'shader/plane_shadow.nfx::TShader'
          15  CALL_FUNCTION_2       2 
          18  POP_TOP          

2527      19  LOAD_FAST             0  'model'
          22  LOAD_ATTR             2  'set_rendergroup_and_priority'
          25  LOAD_GLOBAL           3  'world'
          28  LOAD_ATTR             4  'RENDER_GROUP_TRANSPARENT'
          31  LOAD_CONST            3  10
          34  CALL_FUNCTION_2       2 
          37  POP_TOP          

2528      38  LOAD_GLOBAL           5  'hasattr'
          41  LOAD_GLOBAL           4  'RENDER_GROUP_TRANSPARENT'
          44  CALL_FUNCTION_2       2 
          47  POP_JUMP_IF_FALSE    66  'to 66'

2529      50  LOAD_FAST             0  'model'
          53  LOAD_ATTR             6  'set_inherit_parent_shaderctrl'
          56  LOAD_GLOBAL           7  'False'
          59  CALL_FUNCTION_1       1 
          62  POP_TOP          
          63  JUMP_FORWARD          0  'to 66'
        66_0  COME_FROM                '63'

2530      66  LOAD_FAST             0  'model'
          69  LOAD_ATTR             0  'all_materials'
          72  LOAD_ATTR             8  'set_var'
          75  LOAD_GLOBAL           9  '_HASH_light_info'
          78  LOAD_CONST            5  'light_info'
          81  LOAD_FAST             1  'light_info'
          84  CALL_FUNCTION_3       3 
          87  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 44

    def add_panel_shadow--- This code section failed: ---

2533       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'by_mecha_chuchang'
           6  POP_JUMP_IF_FALSE    13  'to 13'

2534       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

2535      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             1  'parent'
          19  LOAD_ATTR             2  'scene'
          22  CALL_FUNCTION_0       0 
          25  STORE_FAST            1  'scn'

2536      28  LOAD_FAST             1  'scn'
          31  LOAD_ATTR             3  'get_light'
          34  LOAD_CONST            1  'dir_light'
          37  CALL_FUNCTION_1       1 
          40  STORE_FAST            2  'light'

2537      43  LOAD_FAST             2  'light'
          46  POP_JUMP_IF_TRUE     53  'to 53'

2538      49  LOAD_CONST            0  ''
          52  RETURN_END_IF    
        53_0  COME_FROM                '46'

2539      53  LOAD_GLOBAL           4  'global_data'
          56  LOAD_ATTR             5  'emgr'
          59  LOAD_ATTR             6  'get_lobby_scene_type_event'
          62  LOAD_ATTR             7  'emit'
          65  CALL_FUNCTION_0       0 
          68  STORE_FAST            3  'result'

2540      71  LOAD_CONST            2  ''
          74  STORE_FAST            4  'scene_type'

2541      77  LOAD_FAST             3  'result'
          80  POP_JUMP_IF_FALSE    96  'to 96'

2542      83  LOAD_FAST             3  'result'
          86  LOAD_CONST            3  ''
          89  BINARY_SUBSCR    
          90  STORE_FAST            4  'scene_type'
          93  JUMP_FORWARD         15  'to 111'

2544      96  LOAD_GLOBAL           4  'global_data'
          99  LOAD_ATTR             8  'game_mgr'
         102  LOAD_ATTR             2  'scene'
         105  LOAD_ATTR             9  'scene_type'
         108  STORE_FAST            4  'scene_type'
       111_0  COME_FROM                '93'

2546     111  LOAD_GLOBAL          10  'lobby_model_display_utils'
         114  LOAD_ATTR            11  'is_scene_surpport_pnl_shadow'
         117  LOAD_FAST             4  'scene_type'
         120  CALL_FUNCTION_1       1 
         123  STORE_FAST            5  'is_cast_shadow'

2547     126  LOAD_FAST             5  'is_cast_shadow'
         129  POP_JUMP_IF_TRUE    136  'to 136'

2548     132  LOAD_CONST            0  ''
         135  RETURN_END_IF    
       136_0  COME_FROM                '129'

2549     136  LOAD_FAST             0  'self'
         139  LOAD_ATTR            12  'get_model'
         142  CALL_FUNCTION_0       0 
         145  STORE_FAST            6  'model'

2550     148  LOAD_FAST             6  'model'
         151  POP_JUMP_IF_TRUE    158  'to 158'

2551     154  LOAD_CONST            0  ''
         157  RETURN_END_IF    
       158_0  COME_FROM                '151'

2552     158  LOAD_FAST             0  'self'
         161  LOAD_ATTR            13  'model_data'
         164  LOAD_ATTR            14  'get'
         167  LOAD_CONST            4  'hide_shadow'
         170  LOAD_GLOBAL          15  'False'
         173  CALL_FUNCTION_2       2 
         176  STORE_FAST            7  'hide_shadow'

2553     179  LOAD_FAST             7  'hide_shadow'
         182  POP_JUMP_IF_FALSE   189  'to 189'

2554     185  LOAD_CONST            0  ''
         188  RETURN_END_IF    
       189_0  COME_FROM                '182'

2555     189  LOAD_FAST             6  'model'
         192  LOAD_ATTR            16  'world_position'
         195  LOAD_ATTR            17  'y'
         198  STORE_FAST            8  'height'

2558     201  LOAD_FAST             0  'self'
         204  LOAD_ATTR            18  'item_type'
         207  LOAD_GLOBAL          19  'L_ITEM_TYPE_GUN'
         210  LOAD_GLOBAL          20  'L_ITME_TYPE_GUNSKIN'
         213  LOAD_GLOBAL          21  'L_ITEM_YTPE_VEHICLE'
         216  LOAD_GLOBAL          22  'L_ITEM_YTPE_VEHICLE_SKIN'
         219  LOAD_GLOBAL          23  'L_ITEM_TYPE_PET_SKIN'
         222  BUILD_TUPLE_5         5 
         225  COMPARE_OP            6  'in'
         228  POP_JUMP_IF_FALSE   265  'to 265'

2559     231  LOAD_FAST             0  'self'
         234  LOAD_ATTR            13  'model_data'
         237  LOAD_ATTR            14  'get'
         240  LOAD_CONST            5  'ignore_shadow_down_offset'
         243  CALL_FUNCTION_1       1 
         246  POP_JUMP_IF_TRUE    265  'to 265'

2560     249  LOAD_FAST             8  'height'
         252  LOAD_CONST            6  10.0
         255  INPLACE_SUBTRACT 
         256  STORE_FAST            8  'height'
         259  JUMP_ABSOLUTE       265  'to 265'
         262  JUMP_FORWARD          0  'to 265'
       265_0  COME_FROM                '262'

2562     265  LOAD_FAST             2  'light'
         268  LOAD_ATTR            24  'direction'
         271  STORE_FAST            9  'direction'

2563     274  LOAD_FAST             9  'direction'
         277  LOAD_ATTR            25  'x'
         280  LOAD_FAST             9  'direction'
         283  LOAD_ATTR            17  'y'
         286  LOAD_FAST             9  'direction'
         289  LOAD_ATTR            26  'z'
         292  LOAD_FAST             8  'height'
         295  BUILD_TUPLE_4         4 
         298  STORE_FAST           10  'light_info'

2565     301  LOAD_FAST             0  'self'
         304  LOAD_ATTR            27  'get_low_model_path'
         307  CALL_FUNCTION_0       0 
         310  STORE_FAST           11  'model_path'

2567     313  LOAD_GLOBAL          28  'world'
         316  LOAD_ATTR            29  'model'
         319  LOAD_FAST             0  'self'
         322  LOAD_ATTR            30  'shadow_model_path'
         325  LOAD_CONST            0  ''
         328  CALL_FUNCTION_2       2 
         331  LOAD_FAST             0  'self'
         334  STORE_ATTR           32  'shadow_model'

2568     337  LOAD_FAST            11  'model_path'
         340  LOAD_FAST             0  'self'
         343  LOAD_ATTR            30  'shadow_model_path'
         346  COMPARE_OP            3  '!='
         349  POP_JUMP_IF_FALSE   371  'to 371'

2569     352  LOAD_FAST             0  'self'
         355  LOAD_ATTR            32  'shadow_model'
         358  LOAD_ATTR            33  'add_mesh'
         361  LOAD_FAST            11  'model_path'
         364  CALL_FUNCTION_1       1 
         367  POP_TOP          
         368  JUMP_FORWARD          0  'to 371'
       371_0  COME_FROM                '368'

2571     371  LOAD_FAST             0  'self'
         374  LOAD_ATTR            13  'model_data'
         377  LOAD_ATTR            14  'get'
         380  LOAD_CONST            7  'add_sub_mesh_to_shadow'
         383  LOAD_GLOBAL          15  'False'
         386  CALL_FUNCTION_2       2 
         389  POP_JUMP_IF_FALSE   455  'to 455'

2572     392  LOAD_FAST             0  'self'
         395  LOAD_ATTR            13  'model_data'
         398  LOAD_ATTR            14  'get'
         401  LOAD_CONST            8  'sub_mesh_path_list'
         404  CALL_FUNCTION_1       1 
         407  STORE_FAST           12  'sub_mesh_list'

2573     410  LOAD_FAST            12  'sub_mesh_list'
         413  POP_JUMP_IF_FALSE   455  'to 455'

2574     416  SETUP_LOOP           33  'to 452'
         419  LOAD_FAST            12  'sub_mesh_list'
         422  GET_ITER         
         423  FOR_ITER             22  'to 448'
         426  STORE_FAST           13  'sub_mesh_path'

2575     429  LOAD_FAST             0  'self'
         432  LOAD_ATTR            32  'shadow_model'
         435  LOAD_ATTR            33  'add_mesh'
         438  LOAD_FAST            13  'sub_mesh_path'
         441  CALL_FUNCTION_1       1 
         444  POP_TOP          
         445  JUMP_BACK           423  'to 423'
         448  POP_BLOCK        
       449_0  COME_FROM                '416'
         449  JUMP_ABSOLUTE       455  'to 455'
         452  JUMP_FORWARD          0  'to 455'
       455_0  COME_FROM                '452'

2577     455  LOAD_GLOBAL          34  'getattr'
         458  LOAD_GLOBAL           9  'scene_type'
         461  LOAD_CONST            0  ''
         464  CALL_FUNCTION_3       3 
         467  STORE_FAST           14  'socket_model'

2578     470  LOAD_FAST            14  'socket_model'
         473  POP_JUMP_IF_FALSE   744  'to 744'

2579     476  SETUP_LOOP          265  'to 744'
         479  LOAD_FAST            14  'socket_model'
         482  LOAD_ATTR            35  'iteritems'
         485  CALL_FUNCTION_0       0 
         488  GET_ITER         
         489  FOR_ITER            248  'to 740'
         492  UNPACK_SEQUENCE_2     2 
         495  STORE_FAST           15  'socket_name'
         498  STORE_FAST           16  'model_conf'

2580     501  LOAD_GLOBAL          36  'type'
         504  LOAD_FAST            16  'model_conf'
         507  CALL_FUNCTION_1       1 
         510  LOAD_GLOBAL          37  'list'
         513  LOAD_GLOBAL          38  'tuple'
         516  BUILD_TUPLE_2         2 
         519  COMPARE_OP            7  'not-in'
         522  POP_JUMP_IF_FALSE   537  'to 537'

2581     525  LOAD_FAST            16  'model_conf'
         528  BUILD_LIST_1          1 
         531  STORE_FAST           16  'model_conf'
         534  JUMP_FORWARD          0  'to 537'
       537_0  COME_FROM                '534'

2582     537  SETUP_LOOP          197  'to 737'
         540  LOAD_FAST            16  'model_conf'
         543  GET_ITER         
         544  FOR_ITER            189  'to 736'
         547  STORE_FAST           17  'model_conf_'

2583     550  LOAD_CONST           10  'MODEL'
         553  STORE_FAST           18  'res_type'

2584     556  LOAD_GLOBAL          15  'False'
         559  STORE_FAST           19  'ignore_on_shadow'

2585     562  LOAD_GLOBAL          36  'type'
         565  LOAD_FAST            17  'model_conf_'
         568  CALL_FUNCTION_1       1 
         571  LOAD_GLOBAL          39  'dict'
         574  BUILD_TUPLE_1         1 
         577  COMPARE_OP            6  'in'
         580  POP_JUMP_IF_FALSE   640  'to 640'

2586     583  LOAD_FAST            17  'model_conf_'
         586  LOAD_ATTR            14  'get'
         589  LOAD_CONST           11  'model_path'
         592  LOAD_CONST            2  ''
         595  CALL_FUNCTION_2       2 
         598  STORE_FAST           11  'model_path'

2587     601  LOAD_FAST            17  'model_conf_'
         604  LOAD_ATTR            14  'get'
         607  LOAD_CONST           12  'res_type'
         610  LOAD_CONST           10  'MODEL'
         613  CALL_FUNCTION_2       2 
         616  STORE_FAST           18  'res_type'

2588     619  LOAD_FAST            17  'model_conf_'
         622  LOAD_ATTR            14  'get'
         625  LOAD_CONST           13  'ignore_on_shadow'
         628  LOAD_GLOBAL          15  'False'
         631  CALL_FUNCTION_2       2 
         634  STORE_FAST           19  'ignore_on_shadow'
         637  JUMP_FORWARD          6  'to 646'

2590     640  LOAD_FAST            17  'model_conf_'
         643  STORE_FAST           11  'model_path'
       646_0  COME_FROM                '637'

2591     646  LOAD_FAST            19  'ignore_on_shadow'
         649  POP_JUMP_IF_FALSE   658  'to 658'

2592     652  CONTINUE            544  'to 544'
         655  JUMP_FORWARD          0  'to 658'
       658_0  COME_FROM                '655'

2593     658  LOAD_CONST           14  'socket_model_%s'
         661  LOAD_FAST            15  'socket_name'
         664  BINARY_MODULO    
         665  STORE_FAST           20  'socket_model_name'

2594     668  LOAD_FAST             0  'self'
         671  LOAD_ATTR            40  'socket_model_names'
         674  LOAD_ATTR            41  'append'
         677  LOAD_FAST            20  'socket_model_name'
         680  CALL_FUNCTION_1       1 
         683  POP_TOP          

2595     684  LOAD_GLOBAL          42  'resloader'
         687  LOAD_ATTR            43  'load_res_attr'

2596     690  LOAD_FAST             0  'self'

2597     693  LOAD_FAST            20  'socket_model_name'

2598     696  LOAD_FAST            11  'model_path'

2599     699  LOAD_FAST             0  'self'
         702  LOAD_ATTR            44  'on_load_socket_model_complete'

2600     705  LOAD_FAST            15  'socket_name'
         708  LOAD_FAST            17  'model_conf_'
         711  BUILD_TUPLE_2         2 
         714  LOAD_CONST           12  'res_type'

2601     717  LOAD_FAST            18  'res_type'
         720  LOAD_CONST           15  'priority'

2602     723  LOAD_GLOBAL          45  'game3d'
         726  LOAD_ATTR            46  'ASYNC_HIGH'
         729  CALL_FUNCTION_517   517 
         732  POP_TOP          
         733  JUMP_BACK           544  'to 544'
         736  POP_BLOCK        
       737_0  COME_FROM                '537'
         737  JUMP_BACK           489  'to 489'
         740  POP_BLOCK        
       741_0  COME_FROM                '476'
         741  JUMP_FORWARD          0  'to 744'
       744_0  COME_FROM                '476'

2605     744  BUILD_LIST_0          0 
         747  STORE_FAST           21  'weapon_sub_model_list'

2606     750  LOAD_FAST             0  'self'
         753  LOAD_ATTR            18  'item_type'
         756  LOAD_GLOBAL          19  'L_ITEM_TYPE_GUN'
         759  LOAD_GLOBAL          20  'L_ITME_TYPE_GUNSKIN'
         762  BUILD_TUPLE_2         2 
         765  COMPARE_OP            6  'in'
         768  POP_JUMP_IF_FALSE   851  'to 851'

2607     771  LOAD_GLOBAL          10  'lobby_model_display_utils'
         774  LOAD_ATTR            47  'get_weapon_socket_models'
         777  LOAD_FAST             0  'self'
         780  LOAD_ATTR            30  'shadow_model_path'
         783  CALL_FUNCTION_1       1 
         786  STORE_FAST           22  'danjia_path'

2608     789  LOAD_FAST            22  'danjia_path'
         792  POP_JUMP_IF_FALSE   851  'to 851'

2609     795  LOAD_GLOBAL          28  'world'
         798  LOAD_ATTR            29  'model'
         801  LOAD_FAST            22  'danjia_path'
         804  LOAD_CONST            0  ''
         807  CALL_FUNCTION_2       2 
         810  STORE_FAST           23  'danjia_model'

2610     813  LOAD_FAST             0  'self'
         816  LOAD_ATTR            32  'shadow_model'
         819  LOAD_ATTR            48  'bind'
         822  LOAD_CONST           16  'danjia'
         825  LOAD_FAST            23  'danjia_model'
         828  CALL_FUNCTION_2       2 
         831  POP_TOP          

2611     832  LOAD_FAST            21  'weapon_sub_model_list'
         835  LOAD_ATTR            41  'append'
         838  LOAD_FAST            23  'danjia_model'
         841  CALL_FUNCTION_1       1 
         844  POP_TOP          
         845  JUMP_ABSOLUTE       851  'to 851'
         848  JUMP_FORWARD          0  'to 851'
       851_0  COME_FROM                '848'

2613     851  LOAD_FAST             0  'self'
         854  LOAD_ATTR            13  'model_data'
         857  LOAD_ATTR            14  'get'
         860  LOAD_CONST           17  'item_no'
         863  LOAD_CONST            0  ''
         866  CALL_FUNCTION_2       2 
         869  STORE_FAST           24  'item_no'

2614     872  LOAD_FAST            24  'item_no'
         875  POP_JUMP_IF_FALSE   954  'to 954'

2615     878  LOAD_GLOBAL          49  'confmgr'
         881  LOAD_ATTR            14  'get'
         884  LOAD_CONST           18  'lobby_item'
         887  LOAD_GLOBAL          50  'str'
         890  LOAD_FAST            24  'item_no'
         893  CALL_FUNCTION_1       1 
         896  CALL_FUNCTION_2       2 
         899  STORE_FAST           25  'item_conf'

2616     902  LOAD_FAST            25  'item_conf'
         905  POP_JUMP_IF_FALSE   954  'to 954'

2617     908  LOAD_FAST            25  'item_conf'
         911  LOAD_ATTR            14  'get'
         914  LOAD_CONST           19  'remove_socket_list'
         917  BUILD_LIST_0          0 
         920  CALL_FUNCTION_2       2 
         923  STORE_FAST           26  'remove_socket_list'

2618     926  LOAD_GLOBAL           4  'global_data'
         929  LOAD_ATTR            51  'model_mgr'
         932  LOAD_ATTR            52  'remove_model_socket'
         935  LOAD_FAST             0  'self'
         938  LOAD_ATTR            32  'shadow_model'
         941  LOAD_FAST            26  'remove_socket_list'
         944  CALL_FUNCTION_2       2 
         947  POP_TOP          
         948  JUMP_ABSOLUTE       954  'to 954'
         951  JUMP_FORWARD          0  'to 954'
       954_0  COME_FROM                '951'

2619     954  LOAD_FAST             0  'self'
         957  LOAD_ATTR            32  'shadow_model'
         960  LOAD_ATTR            53  'set_parent'
         963  LOAD_FAST             6  'model'
         966  CALL_FUNCTION_1       1 
         969  POP_TOP          

2620     970  LOAD_GLOBAL          54  'math3d'
         973  LOAD_ATTR            55  'vector'
         976  LOAD_CONST            3  ''
         979  LOAD_CONST            3  ''
         982  LOAD_CONST            3  ''
         985  CALL_FUNCTION_3       3 
         988  LOAD_FAST             0  'self'
         991  LOAD_ATTR            32  'shadow_model'
         994  STORE_ATTR           56  'position'

2622     997  LOAD_FAST             0  'self'
        1000  LOAD_ATTR            57  'is_mecha'
        1003  POP_JUMP_IF_FALSE  1116  'to 1116'

2623    1006  LOAD_FAST             0  'self'
        1009  LOAD_ATTR            13  'model_data'
        1012  LOAD_ATTR            14  'get'
        1015  LOAD_CONST           20  'skin_id'
        1018  CALL_FUNCTION_1       1 
        1021  LOAD_FAST             0  'self'
        1024  LOAD_ATTR            13  'model_data'
        1027  LOAD_ATTR            14  'get'
        1030  LOAD_CONST           21  'shiny_weapon_id'
        1033  CALL_FUNCTION_1       1 
        1036  ROT_TWO          
        1037  STORE_FAST           27  'skin_id'
        1040  STORE_FAST           28  'shiny_weapon_id'

2624    1043  LOAD_FAST             0  'self'
        1046  LOAD_ATTR            58  'shadow_mecha_socket_res_agent'
        1049  LOAD_ATTR            59  'load_skin_model_and_effect'
        1052  LOAD_FAST             0  'self'
        1055  LOAD_ATTR            32  'shadow_model'
        1058  LOAD_FAST            27  'skin_id'
        1061  LOAD_FAST            28  'shiny_weapon_id'
        1064  LOAD_CONST           22  'skip_sfx_creation'
        1067  LOAD_GLOBAL          60  'True'
        1070  CALL_FUNCTION_259   259 
        1073  POP_TOP          

2625    1074  SETUP_LOOP           39  'to 1116'
        1077  LOAD_FAST             0  'self'
        1080  LOAD_ATTR            58  'shadow_mecha_socket_res_agent'
        1083  LOAD_ATTR            61  'model_res_list'
        1086  GET_ITER         
        1087  FOR_ITER             22  'to 1112'
        1090  STORE_FAST           29  'model_res'

2626    1093  LOAD_FAST             0  'self'
        1096  LOAD_ATTR            62  'shadowing_model'
        1099  LOAD_FAST            29  'model_res'
        1102  LOAD_FAST            10  'light_info'
        1105  CALL_FUNCTION_2       2 
        1108  POP_TOP          
        1109  JUMP_BACK          1087  'to 1087'
        1112  POP_BLOCK        
      1113_0  COME_FROM                '1074'
        1113  JUMP_FORWARD          0  'to 1116'
      1116_0  COME_FROM                '1074'

2629    1116  LOAD_FAST             0  'self'
        1119  LOAD_ATTR            63  'head_res_path'
        1122  JUMP_IF_FALSE_OR_POP  1131  'to 1131'
        1125  LOAD_FAST             0  'self'
        1128  LOAD_ATTR            64  'is_same_gis'
      1131_0  COME_FROM                '1122'
        1131  POP_JUMP_IF_TRUE   1304  'to 1304'

2630    1134  LOAD_FAST             0  'self'
        1137  LOAD_ATTR            32  'shadow_model'
        1140  LOAD_ATTR            65  'all_materials'
        1143  LOAD_ATTR            66  'set_technique'
        1146  LOAD_CONST           23  1
        1149  LOAD_CONST           24  'shader/plane_shadow.nfx::TShader'
        1152  CALL_FUNCTION_2       2 
        1155  POP_TOP          

2631    1156  LOAD_FAST             0  'self'
        1159  LOAD_ATTR            32  'shadow_model'
        1162  LOAD_ATTR            67  'set_rendergroup_and_priority'
        1165  LOAD_GLOBAL          28  'world'
        1168  LOAD_ATTR            68  'RENDER_GROUP_TRANSPARENT'
        1171  LOAD_CONST           25  10
        1174  CALL_FUNCTION_2       2 
        1177  POP_TOP          

2632    1178  LOAD_GLOBAL          69  'hasattr'
        1181  LOAD_FAST             0  'self'
        1184  LOAD_ATTR            32  'shadow_model'
        1187  LOAD_CONST           26  'set_inherit_parent_shaderctrl'
        1190  CALL_FUNCTION_2       2 
        1193  POP_JUMP_IF_FALSE  1215  'to 1215'

2633    1196  LOAD_FAST             0  'self'
        1199  LOAD_ATTR            32  'shadow_model'
        1202  LOAD_ATTR            70  'set_inherit_parent_shaderctrl'
        1205  LOAD_GLOBAL          15  'False'
        1208  CALL_FUNCTION_1       1 
        1211  POP_TOP          
        1212  JUMP_FORWARD          0  'to 1215'
      1215_0  COME_FROM                '1212'

2635    1215  SETUP_LOOP           86  'to 1304'
        1218  LOAD_FAST            21  'weapon_sub_model_list'
        1221  GET_ITER         
        1222  FOR_ITER             75  'to 1300'
        1225  STORE_FAST           30  'sub_model'

2636    1228  LOAD_FAST            30  'sub_model'
        1231  LOAD_ATTR            65  'all_materials'
        1234  LOAD_ATTR            66  'set_technique'
        1237  LOAD_CONST           23  1
        1240  LOAD_CONST           24  'shader/plane_shadow.nfx::TShader'
        1243  CALL_FUNCTION_2       2 
        1246  POP_TOP          

2637    1247  LOAD_FAST            30  'sub_model'
        1250  LOAD_ATTR            67  'set_rendergroup_and_priority'
        1253  LOAD_GLOBAL          28  'world'
        1256  LOAD_ATTR            68  'RENDER_GROUP_TRANSPARENT'
        1259  LOAD_CONST           25  10
        1262  CALL_FUNCTION_2       2 
        1265  POP_TOP          

2638    1266  LOAD_GLOBAL          69  'hasattr'
        1269  LOAD_FAST            30  'sub_model'
        1272  LOAD_CONST           26  'set_inherit_parent_shaderctrl'
        1275  CALL_FUNCTION_2       2 
        1278  POP_JUMP_IF_FALSE  1222  'to 1222'

2639    1281  LOAD_FAST            30  'sub_model'
        1284  LOAD_ATTR            70  'set_inherit_parent_shaderctrl'
        1287  LOAD_GLOBAL          15  'False'
        1290  CALL_FUNCTION_1       1 
        1293  POP_TOP          
        1294  JUMP_BACK          1222  'to 1222'
        1297  JUMP_BACK          1222  'to 1222'
        1300  POP_BLOCK        
      1301_0  COME_FROM                '1215'
        1301  JUMP_FORWARD          0  'to 1304'
      1304_0  COME_FROM                '1215'

2641    1304  LOAD_FAST             0  'self'
        1307  LOAD_ATTR            32  'shadow_model'
        1310  LOAD_ATTR            65  'all_materials'
        1313  LOAD_ATTR            71  'set_var'
        1316  LOAD_GLOBAL          72  '_HASH_light_info'
        1319  LOAD_CONST           27  'light_info'
        1322  LOAD_FAST            10  'light_info'
        1325  CALL_FUNCTION_3       3 
        1328  POP_TOP          

2642    1329  SETUP_LOOP           36  'to 1368'
        1332  LOAD_FAST            21  'weapon_sub_model_list'
        1335  GET_ITER         
        1336  FOR_ITER             28  'to 1367'
        1339  STORE_FAST           30  'sub_model'

2643    1342  LOAD_FAST            30  'sub_model'
        1345  LOAD_ATTR            65  'all_materials'
        1348  LOAD_ATTR            71  'set_var'
        1351  LOAD_GLOBAL          72  '_HASH_light_info'
        1354  LOAD_CONST           27  'light_info'
        1357  LOAD_FAST            10  'light_info'
        1360  CALL_FUNCTION_3       3 
        1363  POP_TOP          
        1364  JUMP_BACK          1336  'to 1336'
        1367  POP_BLOCK        
      1368_0  COME_FROM                '1329'

2645    1368  LOAD_FAST            21  'weapon_sub_model_list'
        1371  LOAD_FAST             0  'self'
        1374  STORE_ATTR           73  'shadow_model_sub_model_list'

2646    1377  LOAD_FAST            21  'weapon_sub_model_list'
        1380  POP_JUMP_IF_FALSE  1402  'to 1402'

2647    1383  LOAD_FAST            21  'weapon_sub_model_list'
        1386  LOAD_CONST            3  ''
        1389  BINARY_SUBSCR    
        1390  LOAD_ATTR            74  'visible'
        1393  LOAD_FAST             0  'self'
        1396  STORE_ATTR           75  'shadow_model_sub_model_visible'
        1399  JUMP_FORWARD          0  'to 1402'
      1402_0  COME_FROM                '1399'

2650    1402  LOAD_FAST             0  'self'
        1405  LOAD_ATTR            32  'shadow_model'
        1408  LOAD_ATTR            76  'get_socket_count'
        1411  CALL_FUNCTION_0       0 
        1414  STORE_FAST           31  'socket_count'

2651    1417  SETUP_LOOP          104  'to 1524'
        1420  LOAD_GLOBAL          77  'range'
        1423  LOAD_FAST            31  'socket_count'
        1426  CALL_FUNCTION_1       1 
        1429  GET_ITER         
        1430  FOR_ITER             90  'to 1523'
        1433  STORE_FAST           32  'i'

2652    1436  LOAD_FAST             0  'self'
        1439  LOAD_ATTR            32  'shadow_model'
        1442  LOAD_ATTR            78  'get_socket_obj_count'
        1445  LOAD_FAST            32  'i'
        1448  CALL_FUNCTION_1       1 
        1451  STORE_FAST           33  'socket_object_count'

2653    1454  LOAD_FAST             0  'self'
        1457  LOAD_ATTR            32  'shadow_model'
        1460  LOAD_ATTR            79  'get_socket_name'
        1463  LOAD_FAST            32  'i'
        1466  CALL_FUNCTION_1       1 
        1469  STORE_FAST           34  'cur_socket_name'

2654    1472  SETUP_LOOP           45  'to 1520'
        1475  LOAD_GLOBAL          77  'range'
        1478  LOAD_FAST            33  'socket_object_count'
        1481  CALL_FUNCTION_1       1 
        1484  GET_ITER         
        1485  FOR_ITER             31  'to 1519'
        1488  STORE_FAST           32  'i'

2655    1491  LOAD_FAST             0  'self'
        1494  LOAD_ATTR            32  'shadow_model'
        1497  LOAD_ATTR            80  'set_socket_bound_obj_active'
        1500  LOAD_FAST            34  'cur_socket_name'
        1503  LOAD_FAST            32  'i'
        1506  LOAD_GLOBAL          15  'False'
        1509  LOAD_GLOBAL          15  'False'
        1512  CALL_FUNCTION_4       4 
        1515  POP_TOP          
        1516  JUMP_BACK          1485  'to 1485'
        1519  POP_BLOCK        
      1520_0  COME_FROM                '1472'
        1520  JUMP_BACK          1430  'to 1430'
        1523  POP_BLOCK        
      1524_0  COME_FROM                '1417'

2657    1524  LOAD_FAST             0  'self'
        1527  LOAD_ATTR            13  'model_data'
        1530  LOAD_ATTR            14  'get'
        1533  LOAD_CONST           17  'item_no'
        1536  LOAD_CONST            0  ''
        1539  CALL_FUNCTION_2       2 
        1542  STORE_FAST           24  'item_no'

2658    1545  LOAD_FAST             0  'self'
        1548  LOAD_ATTR            81  'is_human'
        1551  POP_JUMP_IF_FALSE  1792  'to 1792'
        1554  LOAD_FAST            24  'item_no'
      1557_0  COME_FROM                '1551'
        1557  POP_JUMP_IF_FALSE  1792  'to 1792'

2659    1560  LOAD_GLOBAL          82  'load_role_skin_model_for_shadow'
        1563  LOAD_FAST             0  'self'
        1566  LOAD_ATTR            32  'shadow_model'
        1569  LOAD_FAST            24  'item_no'
        1572  LOAD_FAST            10  'light_info'
        1575  CALL_FUNCTION_3       3 
        1578  POP_TOP          

2660    1579  LOAD_GLOBAL          49  'confmgr'
        1582  LOAD_ATTR            14  'get'
        1585  LOAD_CONST           28  'role_info'
        1588  LOAD_CONST           29  'RoleSkin'
        1591  LOAD_CONST           30  'Content'
        1594  LOAD_GLOBAL          50  'str'
        1597  LOAD_FAST            24  'item_no'
        1600  CALL_FUNCTION_1       1 
        1603  LOAD_CONST           31  'socket_obj_shadow_sockets'
        1606  LOAD_CONST           32  'default'
        1609  BUILD_LIST_0          0 
        1612  CALL_FUNCTION_261   261 
        1615  STORE_FAST           35  'socket_obj_shadow_sockets'

2661    1618  SETUP_LOOP          171  'to 1792'
        1621  LOAD_FAST            35  'socket_obj_shadow_sockets'
        1624  GET_ITER         
        1625  FOR_ITER            160  'to 1788'
        1628  STORE_FAST           15  'socket_name'

2662    1631  LOAD_FAST             0  'self'
        1634  LOAD_ATTR            32  'shadow_model'
        1637  LOAD_ATTR            83  'get_socket_obj'
        1640  LOAD_FAST            15  'socket_name'
        1643  LOAD_CONST            3  ''
        1646  CALL_FUNCTION_2       2 
        1649  STORE_FAST           14  'socket_model'

2663    1652  LOAD_FAST            14  'socket_model'
        1655  POP_JUMP_IF_TRUE   1664  'to 1664'

2664    1658  CONTINUE           1625  'to 1625'
        1661  JUMP_FORWARD          0  'to 1664'
      1664_0  COME_FROM                '1661'

2665    1664  LOAD_FAST            14  'socket_model'
        1667  LOAD_ATTR            65  'all_materials'
        1670  LOAD_ATTR            66  'set_technique'
        1673  LOAD_CONST           23  1
        1676  LOAD_CONST           24  'shader/plane_shadow.nfx::TShader'
        1679  CALL_FUNCTION_2       2 
        1682  POP_TOP          

2666    1683  LOAD_FAST            14  'socket_model'
        1686  LOAD_ATTR            67  'set_rendergroup_and_priority'
        1689  LOAD_GLOBAL          28  'world'
        1692  LOAD_ATTR            68  'RENDER_GROUP_TRANSPARENT'
        1695  LOAD_CONST           25  10
        1698  CALL_FUNCTION_2       2 
        1701  POP_TOP          

2667    1702  LOAD_GLOBAL          60  'True'
        1705  LOAD_FAST            14  'socket_model'
        1708  STORE_ATTR           74  'visible'

2669    1711  LOAD_GLOBAL          69  'hasattr'
        1714  LOAD_FAST            14  'socket_model'
        1717  LOAD_CONST           26  'set_inherit_parent_shaderctrl'
        1720  CALL_FUNCTION_2       2 
        1723  POP_JUMP_IF_FALSE  1742  'to 1742'

2670    1726  LOAD_FAST            14  'socket_model'
        1729  LOAD_ATTR            70  'set_inherit_parent_shaderctrl'
        1732  LOAD_GLOBAL          15  'False'
        1735  CALL_FUNCTION_1       1 
        1738  POP_TOP          
        1739  JUMP_FORWARD          0  'to 1742'
      1742_0  COME_FROM                '1739'

2672    1742  LOAD_FAST            14  'socket_model'
        1745  LOAD_ATTR            65  'all_materials'
        1748  LOAD_ATTR            71  'set_var'
        1751  LOAD_GLOBAL          72  '_HASH_light_info'
        1754  LOAD_CONST           27  'light_info'
        1757  LOAD_FAST             9  'direction'
        1760  LOAD_ATTR            25  'x'
        1763  LOAD_FAST             9  'direction'
        1766  LOAD_ATTR            17  'y'
        1769  LOAD_FAST             9  'direction'
        1772  LOAD_ATTR            26  'z'
        1775  LOAD_FAST             8  'height'
        1778  BUILD_TUPLE_4         4 
        1781  CALL_FUNCTION_3       3 
        1784  POP_TOP          
        1785  JUMP_BACK          1625  'to 1625'
        1788  POP_BLOCK        
      1789_0  COME_FROM                '1618'
        1789  JUMP_FORWARD          0  'to 1792'
      1792_0  COME_FROM                '1618'

2673    1792  LOAD_FAST             0  'self'
        1795  LOAD_ATTR            81  'is_human'
        1798  POP_JUMP_IF_FALSE  1814  'to 1814'

2674    1801  LOAD_FAST             0  'self'
        1804  LOAD_ATTR            84  'add_human_panel_shadow'
        1807  CALL_FUNCTION_0       0 
        1810  POP_TOP          
        1811  JUMP_FORWARD          0  'to 1814'
      1814_0  COME_FROM                '1811'
        1814  LOAD_CONST            0  ''
        1817  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 464

    def add_human_panel_shadow(self):
        if not self.shadow_model or not self.shadow_model.valid:
            return
        else:
            scn = self.parent.scene()
            light = scn.get_light('dir_light')
            if not light:
                return
            direction = light.direction
            model = self.get_model()
            if not model:
                return
            height = model.world_position.y
            if self.head_res_path is not None:
                if self.is_same_gis:
                    if self.head_res_path != 'invalidres/model.gim':
                        self.shadow_model.add_mesh(self.head_res_path)
                    self.shadow_model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
                    self.shadow_model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
                    if hasattr(self.shadow_model, 'set_inherit_parent_shaderctrl'):
                        self.shadow_model.set_inherit_parent_shaderctrl(False)
                else:
                    head_model = world.model(self.head_res_path, None)
                    self.shadow_model.bind('head', head_model)
                    self.set_panel_shadow(head_model, direction, height)
                    hair_model = head_model.get_socket_obj('hair', 0)
                    if hair_model:
                        self.set_panel_shadow(hair_model, direction, height)
            part_models = [
             'hair']
            for part in part_models:
                head_shadow_model = self.shadow_model.get_socket_obj(part, 0)
                if head_shadow_model:
                    self.set_panel_shadow(head_shadow_model, direction, height)

            socket_objs = self.shadow_model.get_all_objects_on_sockets()
            for socket_obj in socket_objs:
                if isinstance(socket_obj, world.sfx):
                    socket_obj.visible = False

            return

    def set_panel_shadow(self, model, direction, height):
        if self.item_type in (L_ITEM_TYPE_GUN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE, L_ITEM_YTPE_VEHICLE_SKIN):
            height -= 10.0
        model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
        model.all_materials.set_var(_HASH_light_info, 'light_info', (direction.x, direction.y, direction.z, height))
        model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
        if hasattr(model, 'set_inherit_parent_shaderctrl'):
            model.set_inherit_parent_shaderctrl(False)

    def all_mesh_operation_done_callback(self):
        scn = self.parent.scene()
        light = scn.get_light('dir_light')
        if light:
            if self.shadow_model:
                model = self.get_model()
                direction = light.direction
                light_info = (direction.x, direction.y, direction.z, model.world_position.y)
                self.shadowing_model(self.shadow_model, light_info)
                self.shadow_mecha_socket_res_agent.resume_cur_anim_appearance()

    def _fix_shadow_follow_model_res_appearance(self):
        if self.mecha_socket_res_agent and self.shadow_mecha_socket_res_agent:
            model_res_map, shadow_model_res_map = self.mecha_socket_res_agent.model_res_map, self.shadow_mecha_socket_res_agent.model_res_map
            model_res_index = 0
            for key in self.shadow_mecha_socket_res_agent.get_follow_model_res_keys():
                for shadow_model_res in shadow_model_res_map[key]:
                    while shadow_model_res.filename != model_res_map[key][model_res_index].filename:
                        model_res_index += 1

                    shadow_model_res.remove_from_parent()
                    shadow_model_res.set_parent(model_res_map[key][model_res_index])
                    shadow_model_res.position = math3d.vector(0, 0, 0)

            self.shadow_mecha_socket_res_agent.stop_follow_model_res_agent()

    @ext_do_nothing_when_no_skin_ext
    def show_shiny_weapon_sfx(self, skin_id, shiny_id):
        model = self.get_model()
        self.clear_chuchang_sfx()
        if self.mecha_socket_res_agent and model:
            self.mecha_socket_res_agent.clear_skin_model_and_effect()
            self.mecha_socket_res_agent.load_skin_model_and_effect(model, skin_id, shiny_id)
            self.mecha_socket_res_agent.resume_cur_anim_appearance()
        if self.shadow_mecha_socket_res_agent and self.shadow_model:
            self.shadow_mecha_socket_res_agent.set_all_mesh_operation_done_callback(self.all_mesh_operation_done_callback)
            scn = self.parent.scene()
            light = scn.get_light('dir_light')
            if light:
                direction = light.direction
                light_info = (direction.x, direction.y, direction.z, model.world_position.y)
                self.shadow_model.all_materials.set_technique(1, 'shader/vbr_toon.nfx::TShader')
                self.shadow_mecha_socket_res_agent.clear_skin_model_and_effect()
                self.shadow_mecha_socket_res_agent.load_skin_model_and_effect(self.shadow_model, skin_id, shiny_id, skip_sfx_creation=True)
                for model_res in self.shadow_mecha_socket_res_agent.model_res_list:
                    self.shadowing_model(model_res, light_info)

        self._fix_shadow_follow_model_res_appearance()

    @ext_do_nothing_when_no_skin_ext
    def refresh_mecha_skin_res_appearance(self):
        model = self.get_model()
        self.clear_chuchang_sfx()
        if self.mecha_socket_res_agent and model:
            self.mecha_socket_res_agent.clear_skin_model_and_effect()
            skin_id = self.model_data.get('skin_id')
            if skin_id:
                shiny_preview = self.model_data.get('shiny_preview', None)
                shiny_weapon_id = self.model_data.get('shiny_weapon_id', None)
                shiny_weapon_id = shiny_preview if shiny_preview else shiny_weapon_id
                self.mecha_socket_res_agent.load_skin_model_and_effect(model, skin_id, shiny_weapon_id)
                self.mecha_socket_res_agent.resume_cur_anim_appearance()
        return

    @ext_do_nothing_when_no_skin_ext
    def show_skin_improved_sfx(self, flag):
        self.clear_skin_model_and_effect()
        self.clear_chuchang_sfx()
        if self.improved_head:
            self.clear_improved_head()
        improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
        if improved_skin_sfx_id and not flag:
            self.model_data.pop('improved_skin_sfx_id')
        elif improved_skin_sfx_id is None and flag:
            improved_skin_sfx_id = get_skin_improved_sfx_item_id(self.model_data['skin_id'])
            self.model_data['improved_skin_sfx_id'] = improved_skin_sfx_id
        model = self.get_model()
        if flag:
            if model:
                self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, False, load_head=True)
        elif model:
            load_normal_skin_model_and_effect(model, self.model_data.get('item_no'), 'h')
        return

    def check_get_improved_pendant_id(self, skin_id, pendant_id):
        improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
        if improved_skin_sfx_id:
            return dress_utils.get_improve_pendant_id(skin_id, pendant_id) or pendant_id
        else:
            return pendant_id
            return

    @ext_do_nothing_when_no_skin_ext
    def show_extra_socket_objs(self, flag):
        if not self.is_human:
            return
        else:
            item_no = self.model_data.get('item_no', None)
            if not item_no:
                return
            self._show_extra_socket_objs = flag
            host_models = [
             self.get_model(), self.shadow_model]
            if self.sfx_model:
                host_models.append(self.sfx_model)
            extra_sockets = confmgr.get('role_info', 'RoleSkin', 'Content', str(item_no), 'extra_sockets', default=[])
            for socket_name in extra_sockets:
                for model in host_models:
                    if not model:
                        continue
                    socket_model = model.get_socket_obj(socket_name, 0)
                    if not socket_model:
                        continue
                    if not flag:
                        socket_model.visible = False
                    else:
                        socket_model.visible = True

            return

    @ext_do_nothing_when_no_skin_ext
    def hide_sockets_after_show_anim(self):
        if not self.is_human:
            return
        else:
            item_no = self.model_data.get('item_no', None)
            if not item_no:
                return
            host_model = [
             self.get_model(), self.shadow_model]
            hide_sockets_list = confmgr.get('role_info', 'RoleSkin', 'Content', str(item_no), 'hide_sockets_after_show', default=[])
            for hide_model in host_model:
                if not hide_model:
                    continue
                for socket_name in hide_sockets_list:
                    socket_model = hide_model.get_socket_obj(socket_name, 0)
                    if not socket_model:
                        return
                    socket_model.visible = False

            return

    def get_low_model_path(self):
        model_path = self.shadow_model_path
        if self.item_type in (L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN):
            for special_name in FORCE_USE_H_MECHA:
                if str(special_name) in model_path:
                    model_path = self.shadow_model_path.replace('empty.gim', 'h.gim')
                else:
                    model_path = self.shadow_model_path.replace('empty.gim', 'l3.gim')

        return model_path

    def on_pause(self, flag):
        if flag:
            self.stop_cur_sound()
            self.stop_cur_loop_sound()
            model = self.get_model()
            if model and self.mecha_socket_res_agent:
                self.mecha_socket_res_agent.check_exit_anim_appearance(model.cur_anim_name)
            if self.shadow_model and self.shadow_model.valid and self.shadow_mecha_socket_res_agent:
                self.shadow_mecha_socket_res_agent.check_exit_anim_appearance(self.shadow_model.cur_anim_name)

    def get_socket_model_name(self, res_path, socket_name, name_base):
        socket_model_name = name_base + socket_name + str(random.randint(1, 1000))
        if socket_model_name in self.socket_model_names:
            return self.get_socket_model_name(res_path, socket_name, name_base)
        else:
            return socket_model_name

    def get_sub_mesh_model_name(self, res_path, socket_name, name_base):
        sub_mesh_name = name_base + socket_name + str(random.randint(1, 1000))
        if sub_mesh_name in self.sub_mesh_names:
            return self.get_sub_mesh_model_name(res_path, socket_name, name_base + str(random.randint(1, 1000)))
        else:
            return sub_mesh_name

    def check_other_pendant_head_model(self, head_pendant_type, head_res_path):
        if head_res_path == self.head_res_path:
            return
        raise NotImplementedError('Changing head by other pendant is unsupported')

    @ext_do_nothing_when_no_skin_ext_v2
    def init_other_pendant_model(self):
        self.del_other_pendant_models()
        self.other_pendant_model_dict = {}
        self.other_pendant_model_loaded_dict = {}
        other_pendant_model_dict_list = self.model_data.get('pendant_data_list', [])
        if not other_pendant_model_dict_list:
            return
        for pendant_data in other_pendant_model_dict_list:
            res_path = pendant_data.get('res_path')
            socket_name = pendant_data.get('socket_name')
            self.other_pendant_model_dict[res_path] = pendant_data
            self.other_pendant_model_loaded_dict[res_path] = False
            self.load_other_pendant_model(res_path, socket_name, pendant_data, is_init=True)

    @ext_do_nothing_when_no_skin_ext
    def load_other_pendant_model(self, res_path=None, socket_name=None, pendant_data=None, is_init=False):
        self.update_is_same_gis()
        if res_path is None:
            return
        else:
            head_pendant_l_same_gis = False
            if pendant_data:
                head_pendant_l_same_gis = pendant_data.get('head_pendant_l_same_gis', False)
            if socket_name and not (head_pendant_l_same_gis and self.is_same_gis):
                socket_model_name = self.get_socket_model_name(res_path, socket_name, 'socket_model_pendant_')
                self.socket_model_names.append(socket_model_name)
                self.other_pendant_model_socket_model_name_dict[res_path] = [socket_model_name, socket_name]
                resloader.load_res_attr(self, socket_model_name, res_path, self.on_load_other_pendant_model_complete, (
                 res_path, socket_name, head_pendant_l_same_gis), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            else:
                sub_mesh = self.get_sub_mesh_model_name(res_path, str(socket_name), 'sub_mesh_pendant_')
                self.sub_mesh_names.append(sub_mesh)
                self.other_pendant_model_sub_mesh_model_name_dict[res_path] = sub_mesh
                resloader.load_res_attr(self, sub_mesh, res_path, self.on_load_other_pendant_model_complete, (
                 res_path, socket_name, head_pendant_l_same_gis), res_type='MODEL', priority=game3d.ASYNC_HIGH)
            if is_init:
                self.human_init_load_count += 1
            return

    def on_load_other_pendant_model_complete(self, load_model, data, *args):
        if not load_model.valid:
            load_model.destroy()
            return
        else:
            model = self.get_model()
            if not model:
                return
            res_path, socket_name, head_pendant_l_same_gis = data
            self.other_pendant_model_loaded_dict[res_path] = True
            load_model.visible = model.visible
            self.play_show_anim()
            if socket_name and not (head_pendant_l_same_gis and self.is_same_gis):
                model.bind(socket_name, load_model, world.BIND_TYPE_ALL)
                if self._cur_anim_args is not None:
                    cur_anim = self._cur_anim_args[0]
                    if load_model.has_anim(cur_anim):
                        load_model.play_animation(cur_anim)
                if self.is_render_target_model:
                    self.set_model_alpha(load_model)
                enable_outline(load_model)
            else:
                model.add_mesh(load_model.filename)
                enable_outline(model)
                self.set_model_alpha(model)
            self.set_model_cast_shadow(load_model)
            load_model.receive_shadow = True
            improved_skin_sfx_id = self.model_data.get('improved_skin_sfx_id', None)
            if improved_skin_sfx_id:
                self._load_improved_skin_model_and_effect(model, improved_skin_sfx_id, True)
            self.do_loaded_human_res_callback()
            self.check_all_human_socket_and_pendant_loaded()
            return

    @ext_do_nothing_when_no_skin_ext
    def change_other_pendant_model(self, pendant_id_list, pendant_data_list, head_pendant_type, head_res_path, anim_data=None):
        if not self.get_model():
            self.model_data['pendant_data_list'] = pendant_data_list
            return
        else:
            deleted_res_path_list = self.del_other_pendant_models(pendant_data_list)
            for del_res_path in deleted_res_path_list:
                if del_res_path in self.other_pendant_model_dict:
                    self.other_pendant_model_dict.pop(del_res_path)
                if del_res_path in self.other_pendant_model_loaded_dict:
                    self.other_pendant_model_loaded_dict.pop(del_res_path)

            show_anim = None
            end_anim = None
            if anim_data:
                show_anim = anim_data['show_anim']
                end_anim = anim_data['end_anim']
            item_data = confmgr.get('lobby_item', str(self.model_data.get('item_no')), default={})
            if not show_anim:
                show_anim = item_data['first_ani_name']
                if not anim_data or not anim_data['use_skin_show_anim']:
                    for pendant_id in pendant_id_list:
                        if pendant_id is not None and pendant_id != 0:
                            new_data = confmgr.get('lobby_item', str(pendant_id), default={})
                            show_anim = new_data.get('first_ani_name') if new_data.get('first_ani_name') else show_anim
                            if show_anim:
                                break

            if not end_anim:
                end_anim = item_data['end_ani_name']
                if not anim_data or not anim_data['use_skin_end_anim']:
                    for pendant_id in pendant_id_list:
                        if pendant_id is not None and pendant_id != 0:
                            new_data = confmgr.get('lobby_item', str(pendant_id), default={})
                            end_anim = new_data.get('end_ani_name') if new_data.get('end_ani_name') else end_anim
                            if end_anim:
                                break

            for pendant_data in pendant_data_list:
                res_path = pendant_data.get('res_path')
                socket_name = pendant_data.get('socket_name')
                if res_path not in self.other_pendant_model_dict:
                    self.other_pendant_model_dict[res_path] = pendant_data
                    self.other_pendant_model_loaded_dict[res_path] = False
                    self.load_other_pendant_model(res_path, socket_name, pendant_data)

            return

    def del_other_pendant_models(self, remain_pendent_list=()):
        remain_dict = {}
        for data in remain_pendent_list:
            remain_dict[data.get('res_path')] = data.get('socket_name')

        model = self.get_model()
        del_keys = []
        for res_path, socket_info in six.iteritems(self.other_pendant_model_socket_model_name_dict):
            socket_model_name, socket_name = socket_info
            if not socket_model_name:
                continue
            if res_path in remain_dict and remain_dict[res_path] == socket_name:
                continue
            resloader.del_res_attr(self, socket_model_name, True)
            setattr(self, socket_model_name, None)
            if socket_model_name in self.socket_model_names:
                self.socket_model_names.remove(socket_model_name)
            self.unbind_model(model, socket_name, res_path)
            self.unbind_model(self.shadow_model, socket_name, res_path)
            del_keys.append(res_path)

        for del_key in del_keys:
            self.other_pendant_model_socket_model_name_dict.pop(del_key)

        del_meshes = []
        for res_path, sub_mesh_name in six.iteritems(self.other_pendant_model_sub_mesh_model_name_dict):
            if res_path in remain_dict:
                continue
            model.remove_mesh(res_path)
            del_meshes.append(res_path)
            resloader.del_res_attr(self, sub_mesh_name)

        def set_alpha_callback():
            if model and model.valid:
                self.set_model_alpha(model)
                enable_outline(model)

        global_data.game_mgr.register_logic_timer(set_alpha_callback, interval=1, times=15, mode=LOGIC)
        for del_mesh in del_meshes:
            self.other_pendant_model_sub_mesh_model_name_dict.pop(del_mesh)

        return del_keys + del_meshes

    def set_model_alpha(self, model):
        pc_platform_utils.set_display_model_alpha(model, self.is_render_target_model)

    def play_model_trk(self, model_trk, callback=None, reset_init_transform=False, revert=False, time_scale=1.0, is_additive=False):
        self.model_trk = model_trk
        self._model_trk_callback = callback

        def wrapper_callback():
            self.by_model_trk = False
            if self._model_trk_callback:
                self._model_trk_callback()
                self._model_trk_callback = None
            return

        model = self.get_model()
        if not model:
            return
        else:
            if self.model_trk:
                if not self._model_trk_player:
                    self._model_trk_player = CameraTrkPlayer()
                if reset_init_transform:
                    self._model_trk_init_position = None
                    self._model_trk_init_rotation = None
                if not self._model_trk_init_position:
                    self._model_trk_init_position = self.model_pos
                    self._model_trk_init_rotation = math3d.matrix_to_rotation(self.off_euler_rot_mtx)
                self.by_model_trk = True
                self._model_trk_player.auto_play_track(self.model_trk, None, revert, time_scale, is_additive, update_callback=self.on_track_update_model, finish_callback=wrapper_callback)
            return

    def set_extra_model_load_task_id(self, tag, task_id):
        self._extra_model_load_task_dict[tag] = task_id

    def get_extra_model_load_task_id(self, tag):
        return self._extra_model_load_task_dict.get(tag)

    def clear_extra_model_load_tasks(self):
        for tag, task_id in six.iteritems(self._extra_model_load_task_dict):
            if task_id:
                global_data.model_mgr.remove_model_by_id(task_id)

        self._extra_model_load_task_dict = {}

    def register_display_loaded_callback(self, callback):
        self._model_loaded_callback = callback


class PartModelDisplay(ScenePart.ScenePart):
    ENTER_EVENT = {'change_model_display_control_type': 'on_change_model_display_control_type',
       'change_model_display_scene_info': 'on_change_display_scene',
       'close_model_display_scene': 'on_close_model_display_scene',
       'change_model_display_scene_item': 'on_change_display_model',
       'change_model_display_scene_item_ex': 'on_change_display_model_ex',
       'change_model_display_scene_item_customized': 'on_change_display_model_customized',
       'add_model_display_scene_item': 'on_add_display_model',
       'change_model_display_emoji': 'on_change_display_model_emoji',
       'change_model_display_anim': 'on_change_display_model_anim',
       'change_model_display_anim_directly': 'on_change_display_model_anim_directly',
       'to_model_display_end_anim_directly': 'on_to_end_anim_directly',
       'change_model_display_head': 'on_change_display_model_head',
       'change_model_display_bag': 'on_change_display_model_bag',
       'change_model_display_suit': 'on_change_display_model_suit',
       'change_display_model_other_pendant': 'on_change_display_model_other_pendant',
       'reset_rotate_model_display': 'reset_rotate_model',
       'change_model_preview_effect': 'change_model_preview_effect',
       'change_model_display_scene_tag_effect': 'change_scene_sfx_tag_effect',
       'show_shiny_weapon_sfx': 'show_shiny_weapon_sfx',
       'refresh_mecha_skin_res_appearance': 'refresh_mecha_skin_res_appearance',
       'show_skin_improved_sfx': 'show_skin_improved_sfx',
       'check_add_model_to_mirror': 'one_check_add_model_to_mirror',
       'lobby_set_models_visible_event': 'set_models_visible',
       'lobby_set_models_is_mute_event': 'set_models_is_mute',
       'touch_model_part': 'touch_model_part',
       'play_bond_effect_by_index': 'play_bond_effect_by_index',
       'show_extra_socket_objs': 'show_extra_socket_objs',
       'operate_sfx_model': 'operate_sfx_model',
       'refresh_model_decal_data': 'on_refresh_model_decal_data',
       'refresh_model_color_data': 'on_refresh_model_color_data',
       'update_jiemian_scene_content': 'on_update_jiemian_scene_content',
       'change_model_display_off_position': 'on_change_display_model_off_position',
       'resolution_changed': 'on_resolution_changed',
       'set_is_play_show_anim': 'on_set_is_play_show_anim',
       'handle_skin_define_model': 'on_handle_skin_define_model',
       'clear_enter_display_sfx': 'clear_enter_display_sfx',
       'change_glide_sfx_tag_effect_event': 'change_glide_sfx_tag_effect',
       'unbind_model_sockets_object_event': 'unbind_model_sockets_object',
       'clear_glide_sfx_tag_effect_event': 'clear_glide_sfx_tag_effect',
       'shutdown_glide_sfx_tag_effect_event': 'shutdown_glide_sfx_tag_effect',
       'add_glide_sfx_for_lobby_model_event': 'add_glide_model_for_lobby_model',
       'clear_glide_sfx_for_lobby_model_event': 'clear_glide_model_for_lobby_model',
       'play_model_display_track_event': 'play_model_track',
       'register_display_loaded_callback': 'on_register_display_loaded_callback',
       'get_model_display_scene': 'on_get_model_display_scene'
       }

    def __init__(self, scene, name):
        super(PartModelDisplay, self).__init__(scene, name, True)
        self._view_flag = True
        self.save_cam_transform_mat = math3d.matrix()
        self._enter_display_sfx_list = []
        self._scene_tag_sfx_list = {}
        self._parachute_tag_sfx_list = {}
        self.model_objs = []
        self._model_control_type = None
        self._scene_content_type = None
        self._last_vlm_value = None
        self.init_parameters()
        return

    def on_get_model_display_scene(self):
        return self.scene

    def init_parameters(self):
        self.scene_data = {}
        self.model_data = []
        self.model_objs = []
        self.force_refresh = True
        self.events_binded = False
        self.cached_model_tech = {}

    def print_model_info(self):
        all_model_paths = []
        for one_model_obj in self.model_objs:
            model = one_model_obj._model
            if not model or not model.valid:
                continue
            all_model_paths.append((model, model.filename))

        print(('test--print_model_info--len(model_objs) =', len(self.model_objs), '--len(all_model_paths) =', len(all_model_paths), '--all_model_paths =', all_model_paths))

    def on_enter(self):
        import render
        render.enable_dynamic_culling(False)
        scn = self.scene()
        scn.set_adapt_factor(LOBBY_EYE_ADAPT_FACTOR)
        if global_data.is_ue_model and global_data.feature_mgr.is_dynamic_ue_env_config():
            self.scene().load_env('default_nx2_mobile.xml')
            self.scene().viewer_position = math3d.vector(0, 0, 0)

    def on_exit(self):
        self.clear_enter_display_sfx()
        self.clear_model_display_scene_tag_effect()
        self.clear_models()

    def on_pause(self, flag):
        for obj in self.model_objs:
            obj.process_event(not flag)
            obj.on_pause(flag)

        if not flag and self.model_objs:
            if not global_data.player:
                return
            need_update_skin_define = global_data.player.get_need_update_skin_define()
            if need_update_skin_define:
                self.on_refresh_avatar_model_custom_skin()

    def on_close_model_display_scene(self):
        if global_data.player is None:
            return
        else:
            self.clear_enter_display_sfx()
            self.clear_models()
            return

    def set_models_visible(self, visible, index=-1):
        if index != -1:
            if index < len(self.model_objs):
                if visible:
                    self.model_objs[index].show_model()
                else:
                    self.model_objs[index].hide_model()
        else:
            for obj in self.model_objs:
                if visible:
                    obj.show_model()
                else:
                    obj.hide_model()

    def set_models_is_mute(self, is_mute, index=-1):
        if index != -1:
            if index < len(self.model_objs):
                self.model_objs[index].set_is_mute(is_mute)
        else:
            for obj in self.model_objs:
                obj.set_is_mute(is_mute)

    def clear_models(self):
        for obj in self.model_objs:
            obj.destroy()

        self.model_objs = []
        global_data.emgr.add_model_to_mirror.emit(None)
        self.cached_model_tech = {}
        return

    def on_update_jiemian_scene_content(self, scene_type, scene_content_type):
        self._scene_content_type = scene_content_type

    def get_scene_content_type(self):
        return self._scene_content_type

    def on_change_model_display_control_type(self, control_type):
        self._model_control_type = control_type

    def change_model_preview_effect(self, sfx_path, sfx_sound_name=None):
        scn = self.scene()
        if not scn:
            return
        else:
            model = None
            if self.model_objs:
                model = self.model_objs[0].get_model()
            if not model:
                return
            self.clear_enter_display_sfx()
            global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_zhaohuan', duration=0, on_create_func=self.create_enter_display_sfx_callback, on_remove_func=self._on_remove_enter_sfx)
            if sfx_sound_name:
                global_data.sound_mgr.play_ui_sound(sfx_sound_name)
            return

    def clear_enter_display_sfx(self):
        for sfx in self._enter_display_sfx_list:
            global_data.sfx_mgr.remove_sfx(sfx)

        self._enter_display_sfx_list = []

    def create_enter_display_sfx_callback(self, sfx, *args):
        from logic.gutils.mecha_utils import NEED_MODIFY_SCALE
        self._enter_display_sfx_list.append(sfx)
        if self.model_objs:
            model = self.model_objs[0]
            model.show_model()
            model.set_skin_follow_res_visible(False)
            for field in NEED_MODIFY_SCALE:
                if field in model._model.filename:
                    scale = model._model.scale.y
                    sfx.scale = math3d.vector(scale, scale, scale)
                    break

    def _on_remove_enter_sfx(self, *args):
        if self.model_objs:
            self.model_objs[0].set_skin_follow_res_visible(True)

    @ext_do_nothing_when_no_skin_ext
    def show_shiny_weapon_sfx(self, skin_id, shiny_id, last_shiny_id=None, index=-1):
        scn = self.scene()
        if not scn:
            return
        else:
            if not self.model_data:
                return
            if index != -1:
                self.model_objs[index].show_shiny_weapon_sfx(skin_id, shiny_id)
            else:
                mecha_item_id = iutils.get_lobby_item_belong_no(skin_id)
                mecha_id = mecha_lobby_id_2_battle_id(mecha_item_id)
                if not confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'second_model_dir'):
                    need_clear_model = False
                    for i in range(len(self.model_data)):
                        model_path = get_mecha_model_h_path(None, skin_id, shiny_weapon_id=shiny_id)
                        if model_path != get_mecha_model_h_path(None, skin_id, shiny_weapon_id=last_shiny_id):
                            self.model_data[i]['shiny_weapon_id'] = shiny_id
                            self.model_data[i]['shiny_preview'] = shiny_id
                            self.model_data[i]['sub_mesh_path_list'][0] = model_path
                            need_clear_model = True

                    if need_clear_model:
                        self.clear_models()
                        self.on_change_display_model(self.model_data, model_control_type=self._model_control_type)
                        return
                for model_obj in self.model_objs:
                    model_obj.show_shiny_weapon_sfx(skin_id, shiny_id)

            return

    @ext_do_nothing_when_no_skin_ext
    def refresh_mecha_skin_res_appearance(self, index=-1):
        scn = self.scene()
        if not scn:
            return
        if not self.model_data:
            return
        if index != -1:
            self.model_objs[index].refresh_mecha_skin_res_appearance()
        else:
            for model_obj in self.model_objs:
                model_obj.refresh_mecha_skin_res_appearance()

    @ext_do_nothing_when_no_skin_ext
    def show_skin_improved_sfx(self, flag, index=-1):
        scn = self.scene()
        if not scn:
            return
        else:
            if not self.model_data:
                return
            need_refresh_model = False
            for model_data in self.model_data:
                improved_skin_sfx_id = get_skin_improved_sfx_item_id(model_data['skin_id'])
                if get_improve_skin_body_path(improved_skin_sfx_id):
                    need_refresh_model = True
                    if flag:
                        model_data['improved_skin_sfx_id'] = improved_skin_sfx_id
                    else:
                        model_data['improved_skin_sfx_id'] = None
                    head_id = get_improve_skin_head_id(improved_skin_sfx_id)
                    if head_id:
                        if flag:
                            head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list = dress_utils.get_pendant_head_path(head_id, model_data['skin_id'])
                        else:
                            head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list = (None,
                                                                                                                                        None,
                                                                                                                                        None,
                                                                                                                                        None,
                                                                                                                                        None)
                        model_data['head_pendant_type'] = head_pendant_type
                        model_data['head_res_path'] = head_res_path
                        model_data['pendant_socket_name'] = pendant_socket_name
                        model_data['pendant_socket_res_path'] = pendant_socket_res_path
                        model_data['pendant_random_anim_list'] = pendant_random_anim_list

            if need_refresh_model:
                self.clear_models()
                self.on_change_display_model(self.model_data, model_control_type=self._model_control_type)
                return
            if index != -1:
                self.model_objs[index].show_skin_improved_sfx(flag)
            else:
                for model_obj in self.model_objs:
                    model_obj.show_skin_improved_sfx(flag)

            return

    def change_model_camera(self, flag):
        scn = self.scene()
        if not scn:
            return
        active_cam = scn.active_camera
        self._view_flag = flag
        if flag:
            self.save_cam_transform_mat = active_cam.transformation
        else:
            active_cam.transformation = self.save_cam_transform_mat
            self.on_change_display_scene({})
        self.reset_rotate_model()

    def on_change_display_scene(self, scene_data):
        from logic.gutils.CameraHelper import get_adaptive_camera_fov
        scene = self.scene()
        if not scene:
            return
        camera = scene.active_camera
        fov = scene_data.get('fov', 30)
        new_fov, aspect = get_adaptive_camera_fov(fov)
        if self.scene_data == scene_data:
            if global_data.game_mgr.scene.get_type() == SCENE_SKIN_DEFINE:
                return
            if new_fov != camera.fov:
                camera.fov = new_fov
                camera.aspect = aspect
            return
        self.force_refresh = True
        self.scene_data = scene_data
        if not scene_data:
            return
        if global_data.game_mgr.scene.get_type() == SCENE_SKIN_DEFINE:
            camera.fov = 30
            return
        camera.fov = new_fov
        camera.aspect = aspect

    def on_resolution_changed(self):
        if self.scene_data:
            self.on_change_display_scene(self.scene_data)

    def one_check_add_model_to_mirror(self, *args):
        if not self.model_objs:
            return
        for one_obj in self.model_objs:
            one_obj.add_to_mirror()

    def on_change_display_model(self, model_data, **kwargs):
        model_control_type = kwargs.get('model_control_type', None)
        if self._model_control_type is not None and model_control_type != self._model_control_type:
            return
        else:
            if self.model_data == model_data and self.model_objs and not self.force_refresh:
                if model_data is None:
                    return
                create_callback = kwargs.get('create_callback', None)
                is_play_show_anim = False
                if len(model_data) > 0:
                    is_play_show_anim = model_data[0].get('show_anim', None) is not None
                if is_play_show_anim:
                    for one_model_obj in self.model_objs:
                        one_model_obj.create_callback = create_callback
                        one_model_obj.play_show_anim()

                return
            self.force_refresh = False
            self.model_data = model_data
            self.clear_models()
            if not model_data:
                return
            for data in model_data:
                obj = CLobbyModel(self, data, **kwargs)
                self.model_objs.append(obj)

            return

    def on_refresh_model_decal_data(self, decal_list):
        if len(self.model_objs) > 0:
            self.model_objs[0].load_decal_data(decal_list)

    def on_refresh_model_color_data(self, color_dict):
        if len(self.model_objs) > 0:
            self.model_objs[0].load_color_data(color_dict)

    def on_refresh_avatar_model_custom_skin(self):
        if self.model_objs[0].need_decal:
            self.model_objs[0].load_decal_data({}, True)
        if self.model_objs[0].need_color:
            self.model_objs[0].load_color_data(None, True)
        return

    def on_change_display_model_ex(self, model_data, second_model_data, **kwargs):
        self.clear_models()
        self.on_change_display_model(model_data, auto_fix_vlm=False, **kwargs)
        for data in second_model_data:
            obj = CLobbyModel(self, data, show_box_name='second_box_name', **kwargs)
            self.model_objs.append(obj)

    def on_change_display_model_customized(self, models_data, boxes_names, support_mirror, need_correct_show_anim_phase=False, **kwargs):
        if len(models_data) != len(boxes_names):
            log_error('Different model_data length from box_name in showing models')
            return
        self.clear_models()
        for i, model_data in enumerate(models_data):
            for data in model_data:
                obj = CLobbyModel(self, data, real_box_name=boxes_names[i], support_mirror=support_mirror[i], need_correct_show_anim_phase=need_correct_show_anim_phase, **kwargs)
                self.model_objs.append(obj)

    def _fix_vlm_macro(self, models_data):
        use_vlm = '1'
        for model_data in models_data:
            path = model_data[0].get('mpath')
            if path is None:
                continue
            if 'mecha' not in path:
                use_vlm = '1'
                break

        if use_vlm == self._last_vlm_value:
            return
        else:
            self._last_vlm_value = use_vlm
            self.scene().set_macros({'USE_VLM': use_vlm})
            return

    def on_add_display_model(self, model_data, box_name, support_mirror, **kwargs):
        obj = CLobbyModel(self, model_data, real_box_name=box_name, support_mirror=support_mirror, **kwargs)
        self.model_objs.append(obj)

    def on_change_display_model_emoji(self, emoji_id=None, index=-1, emoji_auto_close=False, emoji_close_callback=None):
        if index != -1:
            self.model_objs[index].remove_emoji()
            self.model_objs[index].model_data['emoji_id'] = emoji_id
            self.model_objs[index].emoji_auto_close = emoji_auto_close
            self.model_objs[index].emoji_close_callback = emoji_close_callback
            self.model_objs[index].load_emoji()
        else:
            for model_obj in self.model_objs:
                model_obj.remove_emoji()
                model_obj.model_data['emoji_id'] = emoji_id
                model_obj.emoji_auto_close = emoji_auto_close
                model_obj.emoji_close_callback = emoji_close_callback
                model_obj.load_emoji()

    def on_change_display_model_anim(self, gesture_id=None, index=-1):
        animation_name = interaction_utils.get_gesture_action_name(gesture_id)
        if animation_name is None:
            return
        else:
            if index != -1:
                self.model_objs[index].play_specific_anim(animation_name)
            else:
                for obj in self.model_objs:
                    obj.play_specific_anim(animation_name)

            return

    def on_change_display_model_anim_directly(self, animation_name=None, index=-1, **kwargs):
        if animation_name is None:
            return
        else:
            is_back_to_end_show_anim = kwargs.get('is_back_to_end_show_anim', False)
            animation_args = kwargs.get('anim_arg', [])
            if index != -1:
                self.model_objs[index].play_specific_anim(animation_name, is_back_to_end_show_anim, *animation_args)
            else:
                for obj in self.model_objs:
                    obj.play_specific_anim(animation_name, is_back_to_end_show_anim, *animation_args)

            return

    def on_to_end_anim_directly(self, animation_name=None, index=-1, **kwargs):
        print('on_to_end_anim_directly', animation_name, index, kwargs)
        is_back_to_end_show_anim = kwargs.get('is_back_to_end_show_anim', False)
        animation_args = kwargs.get('anim_arg', [])
        if index != -1:
            self.model_objs[index].end_specific_anim(animation_name, is_back_to_end_show_anim)
        else:
            for obj in self.model_objs:
                obj.end_specific_anim(animation_name, is_back_to_end_show_anim, *animation_args)

    def on_change_display_model_head(self, head_id=None, skin_id=None, index=-1):
        if not self.model_objs:
            return
        if index != -1:
            head_id = self.model_objs[index].check_get_improved_pendant_id(skin_id, head_id)
        else:
            head_id = self.model_objs[0].check_get_improved_pendant_id(skin_id, head_id)
        head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list = dress_utils.get_pendant_head_path(head_id, skin_id)
        if index != -1:
            self.model_objs[index].change_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list)
        else:
            for obj in self.model_objs:
                obj.change_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, pendant_random_anim_list)

    def on_change_display_model_bag(self, bag_id=None, skin_id=None, index=-1):
        if not self.model_objs:
            return
        if index != -1:
            bag_id = self.model_objs[index].check_get_improved_pendant_id(skin_id, bag_id)
        else:
            bag_id = self.model_objs[0].check_get_improved_pendant_id(skin_id, bag_id)
        model_path, socket_name, anim_data = dress_utils.get_pendant_bag_path(bag_id, skin_id)
        if index != -1:
            self.model_objs[index].change_bag_model(bag_id, socket_name, model_path, anim_data=anim_data)
        else:
            for obj in self.model_objs:
                obj.change_bag_model(bag_id, socket_name, model_path, anim_data=anim_data)

    @ext_do_nothing_when_no_skin_ext
    def on_change_display_model_suit(self, suit_id=None, skin_id=None, index=-1):
        if not self.model_objs:
            return
        if index != -1:
            suit_id = self.model_objs[index].check_get_improved_pendant_id(skin_id, suit_id)
        else:
            suit_id = self.model_objs[0].check_get_improved_pendant_id(skin_id, suit_id)
        head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path, bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2, anim_data = dress_utils.get_pendant_suit_path(suit_id, skin_id)
        if index != -1:
            self.model_objs[index].change_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path)
            self.model_objs[index].change_bag_model(suit_id, bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2, anim_data=anim_data)
        else:
            for obj in self.model_objs:
                obj.change_head_model(head_pendant_type, head_res_path, pendant_socket_name, pendant_socket_res_path)
                obj.change_bag_model(suit_id, bag_socket_name, bag_model_path, bag_socket_name2, bag_model_path2, anim_data=anim_data)

    def on_change_display_model_other_pendant(self, other_pendant_list=None, skin_id=None, index=-1):
        if not self.model_objs:
            return
        if index != -1:
            other_pendant_list = [ self.model_objs[index].check_get_improved_pendant_id(skin_id, pid) for pid in other_pendant_list if pid ]
        else:
            other_pendant_list = [ self.model_objs[0].check_get_improved_pendant_id(skin_id, pid) for pid in other_pendant_list if pid ]
        head_pendant_type, head_res_path, pendant_data_list = dress_utils.get_pendant_other_list_path(other_pendant_list, skin_id)
        anim_data = dress_utils.get_pendant_other_list_anim(other_pendant_list, skin_id)
        if index != -1:
            self.model_data[index]['pendant_data_list'] = pendant_data_list
            self.model_objs[index].change_other_pendant_model(other_pendant_list, pendant_data_list, head_pendant_type, head_res_path, anim_data=anim_data)
        else:
            for idx, obj in enumerate(self.model_objs):
                self.model_data[idx]['pendant_data_list'] = pendant_data_list
                obj.change_other_pendant_model(other_pendant_list, pendant_data_list, head_pendant_type, head_res_path, anim_data=anim_data)

    def reset_rotate_model(self):
        for obj in self.model_objs:
            obj.reset_rotate_model()

    def touch_model_part(self, x, y):
        from logic.gcommon.const import COLOR_MASK, COLOR_PART_MAP, LEG_COLOR, HIT_PART_BODY
        if not self.model_objs:
            return
        camera = self.scene().active_camera
        _, view_dir = camera.screen_to_world(x, y)
        view_dir.normalize()
        lobby_model = self.model_objs[0]
        lobby_model.add_collision()
        hit_model = lobby_model.get_hit_model()
        if not hit_model:
            return -1
        subresult = hit_model.hit_by_ray2(camera.world_position, view_dir * 100)
        if not subresult[0]:
            return -1
        color = subresult[2] if subresult[2] else HIT_PART_BODY
        color = color & COLOR_MASK
        color = color if color in COLOR_PART_MAP else LEG_COLOR
        return COLOR_PART_MAP[color]

    def play_bond_effect_by_index(self, index, role_id, dialog_id):
        if index >= len(self.model_objs):
            return
        lobby_model = self.model_objs[index]
        lobby_model.play_bond_effect(role_id, dialog_id)

    def show_extra_socket_objs(self, index, flag):
        if index >= len(self.model_objs):
            return
        lobby_model = self.model_objs[index]
        lobby_model.show_extra_socket_objs(flag)

    def operate_sfx_model(self, index, info):
        if index >= len(self.model_objs):
            return
        lobby_model = self.model_objs[index]
        lobby_model.operate_sfx_model(info)

    def on_update(self, dt):
        for obj in self.model_objs:
            obj.on_update(dt)

    def get_box_position(self, box_name):
        pos = None
        if box_name:
            if self._scene_content_type:
                content_cnf = confmgr.get('scene_content_config', str(self._scene_content_type))
                if content_cnf:
                    box_info = content_cnf.get('box').get(box_name)
                    if box_info:
                        box_pos = [ float(x) for x in box_info.split(',') ]
                        pos = math3d.vector(*box_pos)
                    else:
                        log_error('box position error, %s %s' % (self._scene_content_type, box_name))
            if not pos:
                m = self.scene().get_model(box_name)
                if m:
                    pos = m.position
        return pos

    def change_scene_sfx_tag_effect(self, sfx_path, sfx_sound_name=None, tag='normal', pos=None, **kwargs):
        scn = self.scene()
        if not scn:
            return
        else:
            self.clear_scene_tag_sfx(tag)
            if not sfx_path:
                return
            if not pos:
                box_name = self.scene_data.get('box_name', '')
                pos = self.get_box_position(box_name)
            if not pos:
                pos = math3d.vector(0, 0, 0)
            offset = kwargs.get('offset', None)
            if offset and type(offset) in [list, tuple]:
                pos += math3d.vector(offset[0], offset[1], offset[2])

            def tag_create_scene_sfx_callback(sfx, tag=tag):
                sfx_scale = kwargs.get('sfx_scale')
                if sfx_scale is not None:
                    sfx.scale = math3d.vector(sfx_scale, sfx_scale, sfx_scale)
                    cam = world.get_active_scene().active_camera
                    sfx.world_rotation_matrix = cam.world_rotation_matrix
                return

            sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=tag_create_scene_sfx_callback)
            self.create_scene_sfx_callback(sfx_id, tag)
            if sfx_sound_name:
                global_data.sound_mgr.play_ui_sound(sfx_sound_name)
            return

    def clear_scene_tag_sfx(self, tag):
        self._scene_tag_sfx_list.setdefault(tag, [])
        tag_list = self._scene_tag_sfx_list.get(tag, [])
        for sfx_id in tag_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._scene_tag_sfx_list[tag] = []

    def create_scene_sfx_callback(self, sfx_id, tag, *args):
        self._scene_tag_sfx_list.setdefault(tag, [])
        self._scene_tag_sfx_list[tag].append(sfx_id)

    def clear_model_display_scene_tag_effect(self):
        for tag in six.iterkeys(self._scene_tag_sfx_list):
            self.clear_scene_tag_sfx(tag)

    def change_glide_sfx_tag_effect(self, skin_id, glide_fx_id, sfx_sound_name=None, tag='normal', **kwargs):
        scn = self.scene()
        if not scn:
            return
        if not glide_fx_id:
            return
        self.clear_glide_sfx_tag_effect()
        sockets_data = get_glide_effect_socket_data(skin_id, glide_fx_id, key='permanent_res_info_display')
        for obj in self.model_objs:
            model = obj.get_model()
            if not model:
                continue

            def create_glide_sfx_callback(sub_sfx):
                if kwargs.get('alpha_percent') is not None:
                    alpha_percent = kwargs.get('alpha_percent')
                else:
                    percent_key = 'frd_alpha'
                    alpha_percent = confmgr.get('glide_effect_conf', 'GlideSkinInfo', 'Content', str(glide_fx_id), percent_key, default=0.4)
                if sub_sfx:
                    if global_data.glide_sfx_alpha_percent:
                        sub_sfx.alpha_percent = global_data.glide_sfx_alpha_percent
                    else:
                        sub_sfx.alpha_percent = alpha_percent
                return

            load_glide_model_effect_and_model(model, sockets_data, callback=create_glide_sfx_callback)

        if sfx_sound_name:
            global_data.sound_mgr.play_ui_sound(sfx_sound_name)

    def unbind_model_sockets_object(self, sockets, opt_sockets=()):
        scn = self.scene()
        if not scn:
            return
        if not sockets:
            return

        def unbind_model_socket(sub_model, socket):
            if sub_model.has_socket(socket):
                bound_models = sub_model.get_socket_objects(socket)
                if bound_models:
                    for bound_model in bound_models:
                        sub_model.unbind(bound_model)
                        bound_model.destroy()

        for obj in self.model_objs:
            model = obj.get_model()
            if not model:
                continue
            for socket in sockets:
                if not model.has_socket(socket):
                    for opt_socket in opt_sockets:
                        if model.has_socket(opt_socket):
                            socket_models = model.get_socket_objects(opt_socket)
                            if socket_models:
                                sub_model = socket_models[0]
                                unbind_model_socket(sub_model, socket)

                else:
                    unbind_model_socket(model, socket)

    def clear_glide_sfx_tag_effect(self, tag=None):
        scn = self.scene()
        if not scn:
            return
        for obj in self.model_objs:
            model = obj.get_model()
            if not model:
                continue
            clear_glide_model_effect_and_model(model)

    def shutdown_glide_sfx_tag_effect(self, tag=None):
        scn = self.scene()
        if not scn:
            return
        from logic.gutils.role_skin_utils import get_glide_model_effect_and_model
        for obj in self.model_objs:
            model = obj.get_model()
            if not model:
                continue
            sub_model_list, sub_sfx_list = get_glide_model_effect_and_model(model)
            for sub_sfx_id in sub_sfx_list:
                sub_sfx = global_data.sfx_mgr.get_sfx_by_id(sub_sfx_id)
                if sub_sfx:
                    sub_sfx.shutdown(False)

    def add_glide_model_for_lobby_model(self, glide_skin_id, glide_fx_id, glide_socket, tag='normal', **kwargs):
        scn = self.scene()
        if not scn:
            return
        if not glide_fx_id:
            return
        model_data = lobby_model_display_utils.get_lobby_model_data(glide_skin_id)
        if not model_data:
            return
        glide_res_path = model_data[0].get('mpath', '')
        glide_tag = 'glide'

        def on_load_glide_model(glide_mode):
            obj_model = obj.get_model()
            if not obj_model:
                return
            obj_model.bind(glide_socket, glide_mode)
            glide_mode.position = math3d.vector(0, 0, 0)
            anim_name = 'glide_move_f'
            glide_mode.play_animation(anim_name, -1.0, 0, 0.0, world.PLAY_FLAG_DEF_LOOP)
            sockets_data = get_glide_effect_socket_data(glide_skin_id, glide_fx_id, key='permanent_res_info')
            self._add_glide_effect_helper(glide_mode, glide_fx_id, sockets_data)

        def process_on_role_model(role_model, obj):
            if not role_model.has_socket(glide_socket):
                return
            glide_model_id = obj.get_extra_model_load_task_id(glide_tag)
            if glide_model_id:
                binded_glide_model = global_data.model_mgr.get_model_by_id(glide_model_id)
                if binded_glide_model:
                    if binded_glide_model.get_file_path() != glide_res_path:
                        clear_glide_model_effect_and_model(binded_glide_model)
                        global_data.model_mgr.remove_model_by_id(glide_model_id)
                        loaded_model_id = global_data.model_mgr.create_model(glide_res_path, on_create_func=on_load_glide_model)
                        obj.set_extra_model_load_task_id(glide_tag, loaded_model_id)
                else:
                    global_data.model_mgr.remove_model_by_id(glide_model_id)
                    loaded_model_id = global_data.model_mgr.create_model(glide_res_path, on_create_func=on_load_glide_model)
                    obj.set_extra_model_load_task_id(glide_tag, loaded_model_id)
            else:
                socket_models = role_model.get_socket_objects(glide_socket)
                for socket_model in socket_models:
                    clear_glide_model_effect_and_model(socket_model)
                    role_model.unbind(socket_model)

                loaded_model_id = global_data.model_mgr.create_model(glide_res_path, on_create_func=on_load_glide_model)

        for idx, obj in enumerate(self.model_objs):
            model = obj.get_model()
            if not model:
                continue
            process_on_role_model(model, obj)

    def _add_glide_effect_helper(self, model, glide_fx_id, sockets_data, **kwargs):

        def create_glide_sfx_callback(sub_sfx):
            if kwargs.get('alpha_percent') is not None:
                alpha_percent = kwargs.get('alpha_percent')
            else:
                percent_key = 'frd_alpha'
                alpha_percent = confmgr.get('glide_effect_conf', 'GlideSkinInfo', 'Content', str(glide_fx_id), percent_key, default=0.4)
            if sub_sfx:
                if global_data.glide_sfx_alpha_percent:
                    sub_sfx.alpha_percent = global_data.glide_sfx_alpha_percent
                else:
                    sub_sfx.alpha_percent = alpha_percent
            return

        clear_glide_model_effect_and_model(model)
        load_glide_model_effect_and_model(model, sockets_data, callback=create_glide_sfx_callback)

    def clear_glide_model_for_lobby_model(self):
        glide_tag = 'glide'
        for idx, obj in enumerate(self.model_objs):
            model = obj.get_model()
            if not model:
                continue
            glide_model_id = obj.get_extra_model_load_task_id(glide_tag)
            if glide_model_id:
                binded_glide_model = global_data.model_mgr.get_model_by_id(glide_model_id)
                if binded_glide_model:
                    clear_glide_model_effect_and_model(binded_glide_model)

    def get_cur_model_list(self):
        return self.model_objs

    def on_change_display_model_off_position(self, off_position=[
 0, 0, 0], is_slerp=False):
        for obj in self.model_objs:
            obj.change_model_off_position(off_position, is_slerp)

    def on_set_is_play_show_anim(self, index=-1):
        if index != -1 and index < len(self.model_objs):
            self.model_objs[index].is_play_show_anim = False
        else:
            for model_obj in self.model_objs:
                model_obj.is_play_show_anim = False

    def on_handle_skin_define_model(self, anim, index=-1, **kwargs):
        if index >= len(self.model_objs):
            return
        self.reset_rotate_model()
        self.set_models_visible(False)
        self.on_set_is_play_show_anim(index)
        self.model_objs[index].show_model()
        self.on_change_display_model_anim_directly(anim, index, **kwargs)

    def trigger_bw_effect(self, *args):
        self.switch_all_visible_model_technique('shader/vertex_color.nfx::TShader')

    def restore_bw_effect(self, *args):
        self.restore_alll_visible_model_technique()

    def switch_all_visible_model_technique(self, new_tech):
        scn = self.scene()
        if not scn:
            return
        all_visible_model = scn.get_all_visible_models()
        for model in all_visible_model:
            for idx in range(model.all_materials.count):
                key = str(model) + str(idx)
                if key in six.iterkeys(self.cached_model_tech):
                    continue
                material = model.all_materials.get_at(idx)
                if not material:
                    continue
                self.cached_model_tech[key] = material.get_technique_name()
                material.set_technique(render.TECH_TYPE_EFFECT, new_tech)
                material.rebuild_tech()

    def restore_alll_visible_model_technique(self):
        scn = self.scene()
        if not scn:
            return
        all_visible_model = scn.get_all_visible_models()
        for model in all_visible_model:
            for idx in range(model.all_materials.count):
                key = str(model) + str(idx)
                if key not in six.iterkeys(self.cached_model_tech):
                    continue
                material = model.all_materials.get_at(idx)
                if not material:
                    continue
                material.set_technique(render.TECH_TYPE_EFFECT, self.cached_model_tech[key])
                material.rebuild_tech()
                del self.cached_model_tech[key]

    def editor_load_model(self, model_path, scale=1, offset=[0, 0, 0], anim=None):
        if type(offset) not in (list, tuple) or len(offset) != 3:
            offset = [
             0, 0, 0]
        model_data = [
         {'mpath': model_path,
            'model_scale': scale,
            'off_position': offset,
            'show_anim': anim
            }]
        self.on_change_display_model(model_data)

    def play_model_track(self, model_trk, callback=None, reset_init_transform=False, revert=False, time_scale=1.0, is_additive=False):
        for model_obj in self.model_objs:
            model_obj.play_model_trk(model_trk, callback, reset_init_transform, revert, time_scale, is_additive)

    def on_register_display_loaded_callback(self, callback):
        for model_obj in self.model_objs:
            model_obj.register_display_loaded_callback(callback)
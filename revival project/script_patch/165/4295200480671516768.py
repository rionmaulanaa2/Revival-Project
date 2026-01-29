# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaModel.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import math3d
import world
import render
import game3d
from .ComAnimatorAppearance import ComAnimatorAppearance
from common.cfg import confmgr
import math
import random
import copy
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE, CHARACTER_LERP_DIR_YAWS
from logic.gutils import mecha_utils
from logic.gutils import get_on_mecha_utils
from logic.gcommon.common_const import robot_animation_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from common.utils.timer import CLOCK
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon import time_utility
import time
from logic.gutils.dress_utils import get_mecha_model_path
from logic.gcommon.item.item_const import FASHION_POS_SUIT, MECHA_FASHION_KEY
from logic.gutils.mecha_skin_utils import MechaSocketResAgent, is_ss_level_skin, get_accurate_mecha_skin_info_from_fasion_data
from logic.gutils.sfx_utils import get_sfx_scale_by_length_spr
from logic.gcommon.common_utils import decal_utils
from logic.gutils.skin_define_utils import load_model_color_data, load_model_decal_data
from logic.gutils.item_utils import get_item_rare_degree
from logic.gcommon.item.item_const import RARE_DEGREE_5
from logic.gcommon.common_const.ui_operation_const import QUALITY_MECHA_EFFECT_LEVEL_KEY, MECHA_EFFECT_LEVEL_ULTRA
from logic.comsys.archive.archive_manager import ArchiveManager
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils import model_utils
from logic.gutils.firearm_sfx_mapping_utils import check_sfx_mapping_initialized, decode_sfx_info
from ext_package.ext_decorator import has_skin_ext
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
import logic.gcommon.common_utils.bcast_utils as bcast
_HASH_shotsig = game3d.calc_string_hash('shot_sig')
HIGH_QUALITY_DIST_SQR = (25 * NEOX_UNIT_SCALE) ** 2
DECAL_LOAD_DIST_SQR = (150 * NEOX_UNIT_SCALE) ** 2
SHARE_MECHA_MOUNT_ANIM_NAME = {8011: 'j_mount'
   }
UNINITIALIZED = 0
INVISIBLE = 1
VISIBLE = 2
MODEL_SHADER_CTRL_SET_ENABLE = hasattr(world.model, 'set_inherit_parent_shaderctrl')
DEFAULT_TWIST_END_BONE = 'biped head'
MECHA_UP_BODY_TWIST_END_BONE = {8025: 'biped spine'
   }
SUGGEST_IMPROVE_MECHA_EFFECT_LEVEL_CD_SECONDS = time_utility.ONE_DAY_SECONDS * 15

class ComMechaModel(ComAnimatorAppearance):
    SUB_COMPONENT_DIR_PATH = 'client.com_mecha_appearance'
    BIND_EVENT = ComAnimatorAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_AIM_POSITION': 'get_aim_position',
       'G_MECHA_ID': 'get_mecha_id',
       'G_MECHA_FASHION_ID': 'get_mecha_fashion_id',
       'G_MECHA_SHINY_WEAPON_ID': 'get_mecha_shiny_weapon_id',
       'G_MECHA_SKIN_AND_SHINY_WEAPON_ID': 'get_mecha_skin_and_shiny_weapon_id',
       'G_MECHA_HIT_POS': 'get_mecha_hit_pos',
       'G_IS_AVATAR': 'is_avatar',
       'G_IS_CREATOR': 'is_creator',
       'G_CREATOR': 'get_creator',
       'G_MECHA_CONFIG': 'get_mecha_config',
       'G_CHECK_OFF_POS': 'check_off_pos_valid',
       'G_CHECK_ENTER_CONSOLOE_ZONE': 'on_check_enter_zone',
       'E_HIT_BLOOD_SFX': 'on_be_hited',
       'E_FIGHT_CAP_UPGRADE_SFX': 'on_fight_capacity_update',
       'E_ON_JOIN_MECHA': 'on_join_mecha',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_NOTIFY_PASSENGER_LEAVE': 'on_notify_leave',
       'E_DEATH': ('on_die', 10),
       'E_FORCE_HIDE_MECHA_MODEL': 'force_hide_mecha_model',
       'E_SHOW_SUB_MESH': 'on_show_sub_mesh',
       'E_HIDE_SUB_MESH': 'on_hide_sub_mesh',
       'E_SHOW_OUTLINE': 'be_hit_outline_display',
       'E_MECHA_LOD_LOADED_FIRST': ('on_load_lod_complete', 10),
       'E_MECHA_LOD_LOADED': ('on_load_lod_complete_refresh', 10),
       'E_NOTIFY_BOARD': 'notify_share_board',
       'G_SELECT_SFX': 'get_select_sfx',
       'E_CHANGE_MECHA_FASHION': 'change_mecha_fashion',
       'E_GM_RESCALE_TARGET': 'gm_rescale_mecha_model',
       'E_DUMP_ALL_STATE': 'dump_all_state',
       'G_CHAR_SIZE_TO_COL_SIZE': 'get_char_size_to_col_size',
       'G_MODEL_OFFSET_Y': 'get_model_offset_y',
       'E_TRANS_CREATE_MECHA_TO_SHARE_NOTIFY': 'on_trans_to_share',
       'G_MECHA_ORIGINAL_MODEL': 'get_mecha_original_model',
       'G_MECHA_SECOND_MODEL': 'get_mecha_second_model',
       'G_MECHA_ORIGINAL_ANIMATOR': 'get_mecha_original_animator',
       'G_MECHA_SECOND_ANIMATOR': 'get_mecha_second_animator',
       'E_SWITCH_MECHA_MODEL': 'on_switch_mecha_model',
       'E_ENABLE_SYNC': ('on_enable_sync', 99),
       'E_REFRESH_MECHA_MODEL': 'refresh_mecha_model',
       'E_ADD_VISIBLE_IN_THIS_FRAME_CHANGED_CALLBACK': 'on_add_visible_in_this_frame_changed_callback'
       })

    def __init__(self):
        super(ComMechaModel, self).__init__()
        self._passenger = None
        self._creator = None
        self._call_sfx = None
        self._smooth_outline_timer_id = None
        self._height = None
        self._trigger_size = None
        self._boarding_circle_sfx = None
        self._share_simui = None
        self._share_simui_id = None
        self._time = time.time()
        self._mecha_sfx = None
        self.sd.ref_is_mecha = True
        self._decal_load_timer = None
        self._decal_high_quality = None
        self._original_empty_model = None
        self._second_empty_model = None
        self._original_animator = None
        self._second_animator = None
        self.get_model_path_func = None
        self.sd.ref_second_model_dir = ''
        self.sd.ref_using_second_model = False
        self.sub_mesh_show = None
        return

    def init_from_dict(self, unit_obj, bdict):
        self._lod_load_complete = False
        self.force_hide_model = False
        self.sd.ref_mecha_id = bdict.get('mecha_id', '8001')
        self._creator = bdict.get('creator', None)
        self._share = bdict.get('share', None)
        self._born_time = bdict.get('born_time', 0)
        self._mecha_fashion_id, self._mecha_shiny_wp_id = get_accurate_mecha_skin_info_from_fasion_data(self.sd.ref_mecha_id, bdict.get(MECHA_FASHION_KEY, {}))
        self._skin_sfx_visible_cache = {}
        self.sd.ref_socket_res_agent = MechaSocketResAgent()
        self._skin_model_and_effect_loaded = False
        self._mecha_sfx = bdict.get('mecha_sfx', None)
        self.mecha_custom_skin = bdict.get('mecha_custom_skin', {})
        decal_list = self.mecha_custom_skin.get('decal', [])
        self._mecha_decal_list = decal_utils.decode_decal_list(decal_list)
        color_dict = self.mecha_custom_skin.get('color', {})
        self._mecha_color_dict = decal_utils.decode_color(color_dict)
        self.suggest_improve_mecha_effect_level_setting_archive_data = ArchiveManager().get_archive_data('suggest_improve_mecha_effect_level_setting')
        mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        mechainfo = mecha_conf[str(self.sd.ref_mecha_id)]
        self.SUB_COMPONENT = ['ComLodMecha']
        if self.is_avatar():
            self.SUB_COMPONENT.append('ComMechaNewAimHelper')
        self.SUB_COMPONENT.extend(mechainfo.get('component', []))
        super(ComMechaModel, self).init_from_dict(unit_obj, bdict)
        check_sfx_mapping_initialized()
        self._refresh_get_model_path_func()
        self.visible_in_this_frame_changed_callbacks = []
        return

    def _refresh_get_model_path_func(self):
        if global_data.force_mecha_empty_model_path:
            self.get_model_path_func = self.get_model_path_in_editor
        else:
            self.get_model_path_func = self.get_model_path

    def on_init_complete(self):
        if self.ev_g_is_avatar():

            def leave_skate():
                if global_data.player.logic:
                    global_data.player.logic.send_event('E_LEAVE_SKATE_INTERACTION_ZONE')

            global_data.game_mgr.register_logic_timer(leave_skate, 3, times=1, mode=CLOCK)

    def get_select_sfx(self):
        return (
         self._mecha_sfx,)

    def get_mecha_config(self, key):
        mecha_id = self.sd.ref_mecha_id
        if not mecha_id:
            return
        mecha_conf = confmgr.get('mecha_conf', key, 'Content')
        mechainfo = mecha_conf[str(mecha_id)]
        if not mechainfo:
            print('[error] test--mecha_id =', mecha_id, '--not exist')
            return
        return mechainfo

    def get_char_size_to_col_size(self):
        from logic.gcommon.cdata import state_physic_arg
        physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
        mecha_id = self.sd.ref_mecha_id or 8001
        physic_conf = physic_conf[str(mecha_id)]
        skin_width = state_physic_arg.padding * NEOX_UNIT_SCALE
        width = physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2
        total_height = physic_conf['character_size'][1] * NEOX_UNIT_SCALE
        character_height = total_height - width * 2.0 - skin_width * 2.0
        return (
         width, character_height * 2)

    def get_model_dir_path(self):
        model_filename = None
        model = self.ev_g_model()
        if model:
            model_filename = model.filename
        if not model_filename:
            return
        else:
            model_filename = model_filename.replace('\\', '/')
            name_list = model_filename.split('/')
            dir_path = None
            for index, name in enumerate(name_list):
                if name == 'robot':
                    dir_path = '/'.join(name_list[:index + 1])
                    break

            return dir_path

    def destroy(self):
        self.suggest_improve_mecha_effect_level_setting_archive_data = None
        self.get_model_path_func = None
        model_utils.unbind_owner_from_vehicle(self, self._creator)
        super(ComMechaModel, self).destroy()
        return

    def on_model_destroy(self):
        if self.visible_in_this_frame_changed_callbacks:
            self.model.is_visible_in_this_frame_changed_callback = None
            self.visible_in_this_frame_changed_callbacks = []
        self.on_notify_leave()
        if self.scene:
            self.scene.enable_smooth_outline(False, self.unit_obj.id)
        if self._share:
            global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        if self._boarding_circle_sfx:
            global_data.sfx_mgr.remove_sfx(self._boarding_circle_sfx)
            self._boarding_circle_sfx = None
        if self.ev_g_force_lobby_outline():
            self.send_event('E_FORCE_LOBBY_OUTLINE', False)
        if self.ev_g_force_shader_lod_level() is not None:
            self.send_event('E_FORCE_SHADER_LOD', None)
        self._skin_model_and_effect_loaded = False
        self.sd.ref_socket_res_agent.destroy()
        self.sd.ref_socket_res_agent = None
        if self.sd.ref_using_second_model:
            self._original_empty_model.destroy()
            self._second_empty_model = None
            self._original_animator.destroy()
            self._second_animator = None
        elif self._second_empty_model:
            self._second_empty_model.destroy()
            self._second_empty_model = None
            self._second_animator.destroy()
            self._second_animator = None
        self._original_empty_model = None
        self._original_animator = None
        if self._call_sfx:
            global_data.sfx_mgr.remove_sfx(self._call_sfx)
            self._call_sfx = None
        if self._share_simui:
            self._share_simui.destroy()
            self._share_simui = None
            self._share_simui_id = None
        if self._decal_load_timer:
            global_data.game_mgr.unregister_logic_timer(self._decal_load_timer)
            self._decal_load_timer = None
        super(ComMechaModel, self).on_model_destroy()
        return

    def _ensure_second_model_ready(self, mecha_id, original_path):
        if self._second_empty_model:
            self._second_empty_model.destroy()
            self._second_animator.destroy()
        self.sd.ref_second_model_dir = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'second_model_dir')
        if self.sd.ref_second_model_dir:
            index = original_path.rfind('/')
            second_model_path = original_path[:index] + '/' + self.sd.ref_second_model_dir + original_path[index:]
            self._second_empty_model = world.model(second_model_path, global_data.game_mgr.scene)
            self._update_model_attributes(self._second_empty_model, True)
            self._second_empty_model.visible = False
            from common.animate import animator
            xml_path = self.get_xml_path()
            self._second_animator = animator.Animator(self._second_empty_model, xml_path, self.unit_obj)
            try:
                self._second_animator.Load(False)
            except Exception as e:
                mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
                mechainfo = mecha_conf[str(self.sd.ref_mecha_id)]
                model_path = mechainfo['model_path']
                print('test--Animator.Load ERROR:', str(e), '--xml_path =', xml_path, '--model_path =', model_path, '--model.filename =', self._second_empty_model.filename)
                import exception_hook
                exception_hook.traceback_uploader()

    def get_model_path(self, mecha_id, mecha_fashion_id):
        return get_mecha_model_path(mecha_id, mecha_fashion_id)

    def get_model_path_in_editor(self, mecha_id, mecha_fashion_id):
        if global_data.force_mecha_empty_model_path and self.ev_g_is_avatar():
            return str(global_data.force_mecha_empty_model_path)
        else:
            return get_mecha_model_path(mecha_id, mecha_fashion_id)

    def get_model_info(self, unit_obj, bdict):
        position = bdict.get('position', (0, 390, -95)) or (0, 390, -95)
        pos = math3d.vector(*position)
        path = self.get_model_path_func(self.sd.ref_mecha_id, self._mecha_fashion_id)
        self._ensure_second_model_ready(self.sd.ref_mecha_id, path)
        return (
         path, None, (pos, path))

    def get_model_offset_y(self):
        from logic.gutils.dress_utils import get_mecha_model_offset_y
        return -get_mecha_model_offset_y(self._mecha_fashion_id)

    def get_xml_path(self):
        xml_path = 'animator_conf/mecha/mecha.xml'
        if not global_data.feature_mgr.is_support_set_animator_blend_node_children_parameter_position() and str(self.sd.ref_mecha_id) == '8032':
            xml_path = 'animator_conf/mecha/mecha_8032.xml'
        return xml_path

    def _set_model_visible(self, visible):
        model = self.model
        if not model:
            return
        model.visible = visible and not self.force_hide_model
        self.sd.ref_socket_res_agent.refresh_res_visible()

    def force_hide_mecha_model(self, flag):
        self.force_hide_model = flag

    def _update_model_attributes(self, model, is_second_model):
        model.set_enable_lerp_dir_light(True)
        model.set_lerp_dir_light_yaws(CHARACTER_LERP_DIR_YAWS)
        if self.ev_g_is_avatar():
            model.shader_lod_type = world.SHADER_LOD_TYPE_PLAYER
        else:
            model.shader_lod_type = world.SHADER_LOD_TYPE_CHAR
        if hasattr(model, 'can_skip_update'):
            model.can_skip_update = False
        if global_data.enable_other_model_shadowmap or self.ev_g_is_avatar():
            model.cast_shadow = True
            model.receive_shadow = True
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            if model.get_submesh_name(i) != 'hit':
                model.set_submesh_hitmask(i, world.HIT_SKIP)

        mecha_utils.check_need_scale(model, self.sd.ref_mecha_id, self._mecha_fashion_id, is_second_model)
        mecha_utils.check_need_flip(model)

    def on_load_model_complete(self, model, user_data):
        from common.animate import animator
        xml_path = self.get_xml_path()
        self._animator = animator.Animator(model, xml_path, self.unit_obj)
        try:
            self._animator.Load(False)
        except Exception as e:
            mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
            mechainfo = mecha_conf[str(self.sd.ref_mecha_id)]
            model_path = mechainfo['model_path']
            print('test--Animator.Load ERROR:', str(e), '--xml_path =', xml_path, '--model_path =', model_path, '--model.filename =', model.filename)
            import exception_hook
            exception_hook.traceback_uploader()

        self._original_animator = self._animator
        self._original_empty_model = model
        self._update_model_attributes(model, False)
        if self._second_empty_model and self.ev_g_is_using_second_model():
            self.sd.ref_using_second_model = True
            self._second_empty_model.position = self._model.position
            self._model = self._second_empty_model
            self._animator = self._second_animator
        self.on_load_animator_complete(user_data)
        self._set_model_visible(True)
        pos, path = user_data
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(math3d.vector(pos.x, pos.y, pos.z), True)
        else:
            self.send_event('E_POSITION', math3d.vector(pos.x, pos.y, pos.z))
        self.send_event('E_HUMAN_MODEL_LOADED', self.model, user_data)
        self.send_event('E_ENABLE_WATER_UPDATE', True)
        self._set_model_visible(False)
        global_data.emgr.mecha_init_event.emit(self.unit_obj)

    def on_load_lod_complete(self):
        self._lod_load_complete = True
        if not self.sd.ref_is_refreshing_whole_model:
            self.notify_passenger_board()
        self.on_init_share_mecha()
        if self.sd.ref_is_refreshing_whole_model:
            self.sd.ref_is_refreshing_whole_model = False
        if self._mecha_color_dict:
            load_model_color_data(self.model, self._mecha_fashion_id, self._mecha_color_dict)
        if self._mecha_decal_list:
            self.manage_decal_data()
        if self.ev_g_is_avatar():
            self.sd.ref_finish_load_lod_model = True
            self.send_event('E_INIT_SPRING_ANI')

    def on_load_lod_complete_refresh(self, owner_model, lod_res_path):
        if self.sub_mesh_show:
            submesh_name_list, show = self.sub_mesh_show
            if show:
                self.on_show_submesh(submesh_name_list)
            else:
                self.on_hide_submesh(submesh_name_list)

    def manage_decal_data(self):

        def update_decal_data(force=False):
            if not global_data.cam_lplayer or not global_data.player:
                return
            player_pos = global_data.cam_lplayer.ev_g_position()
            mecha_pos = self.ev_g_position()
            if player_pos and mecha_pos:
                dist = player_pos - mecha_pos
            else:
                return
            need_decal = dist.length_sqr < DECAL_LOAD_DIST_SQR
            if not need_decal:
                return
            is_avatar = self.is_avatar()
            quality_level = global_data.game_mgr.gds.get_actual_quality()
            support_high_quality = quality_level >= 2 or quality_level == 1 and self.ev_g_is_campmate(global_data.player.logic.ev_g_camp_id())
            need_high_quality = is_avatar or support_high_quality and dist.length_sqr < HIGH_QUALITY_DIST_SQR
            if self._decal_high_quality == need_high_quality and not force:
                return
            self._decal_high_quality = need_high_quality
            lod_level = 0 if is_avatar else 1
            if self._original_empty_model:
                load_model_decal_data(self._original_empty_model, self._mecha_fashion_id, self._mecha_decal_list, lod_level, is_avatar, create_high_quality_decal=need_high_quality)

        update_decal_data(force=True)
        if not self.is_avatar():
            self._decal_load_timer = global_data.game_mgr.register_logic_timer(update_decal_data, 1, times=-1, mode=CLOCK)

    def _load_skin_model_and_effect(self):
        if self._skin_model_and_effect_loaded:
            return
        self.sd.ref_socket_res_agent.load_skin_model_and_effect(self.model, self._mecha_fashion_id, self._mecha_shiny_wp_id, is_avatar=self.is_avatar(), is_in_battle=True, need_listen_anim_enter_leave=False)
        self._skin_model_and_effect_loaded = True
        self.send_event('E_ON_SKIN_SUB_MODEL_LOADED')

    def _clear_skin_model_and_effect(self, ignore_model_res_clearing=False, need_clear_model_ref=False):
        self.sd.ref_socket_res_agent.clear_skin_model_and_effect(ignore_model_res_clearing, need_clear_model_ref)
        self._skin_model_and_effect_loaded = False

    def add_share_mecha_trigger(self):
        physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
        if not self.sd.ref_mecha_id:
            return
        physic_conf = physic_conf[str(self.sd.ref_mecha_id)]
        width = physic_conf['character_size'][0] * NEOX_UNIT_SCALE / 2
        height = physic_conf['character_size'][1] * NEOX_UNIT_SCALE
        self._height = height
        self._trigger_size = math3d.vector(width, height, width) * 3
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner(), need_update_console_pos=True)

    def on_init_share_mecha(self):
        if not self._share:
            return
        self.add_share_mecha_trigger()
        ani_name = SHARE_MECHA_MOUNT_ANIM_NAME.get(self.sd.ref_mecha_id, 'mount')
        if self.model.has_anim('enter_share_mecha'):
            ani_name = 'enter_share_mecha'
        if time_utility.get_server_time() - self._born_time < 1 and not self.sd.ref_is_refreshing_whole_model:

            def create_cb():
                if not self or not self.is_valid():
                    return
                self.send_event('E_POST_ACTION', ani_name, 2, 1, timeScale=0)
                self.show_boarding_circle(True)
                self._load_skin_model_and_effect()
                self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.set_follow_model_visible_without_record(False)
                global_data.emgr.mecha_boarded_event.emit(self.unit_obj)

            def remove_cb():
                if not self or not self.is_valid():
                    return
                self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.set_follow_model_visible_without_record(True)

            mecha_utils.create_summon_sfx(self, self.model, self._mecha_sfx, create_cb, delte_finish_cb=remove_cb)
        else:
            self._set_model_visible(True)
            passenger_info = self.ev_g_passenger_info()
            if len(passenger_info) <= 0:
                self.send_event('E_POST_ACTION', ani_name, 2, 1, timeScale=0)
                self.show_boarding_circle(True)
                self._load_skin_model_and_effect()
                com = self.unit_obj.get_com('ComCharacter')
                if com:
                    com.try_deactivate()
            elif self.sd.ref_is_refreshing_whole_model:
                self.send_event('E_POST_ACTION', ani_name, 2, 1, timeScale=0)
                self._load_skin_model_and_effect()

    def play_board_anim(self, player, pos):
        if MODEL_SHADER_CTRL_SET_ENABLE:
            self._load_skin_model_and_effect()
        if self.ev_g_is_avatar() and self.unit_obj.__class__.__name__ == 'LMecha':
            rare_degree = get_item_rare_degree(self._mecha_fashion_id, weapon_sfx_item=self._mecha_shiny_wp_id)
            if rare_degree >= RARE_DEGREE_5:
                if global_data.player.get_setting_2(QUALITY_MECHA_EFFECT_LEVEL_KEY) != MECHA_EFFECT_LEVEL_ULTRA:
                    last_suggest_time = self.suggest_improve_mecha_effect_level_setting_archive_data.get('last_suggest_time', 0)
                    cur_time = time_utility.get_server_time()
                    if cur_time - last_suggest_time >= SUGGEST_IMPROVE_MECHA_EFFECT_LEVEL_CD_SECONDS:
                        global_data.game_mgr.show_tip(get_text_by_id(860452))
                        self.suggest_improve_mecha_effect_level_setting_archive_data['last_suggest_time'] = cur_time
                        self.suggest_improve_mecha_effect_level_setting_archive_data.save()

        def create_cb():
            if not self or not self.is_valid():
                return
            player.send_event('E_ON_ACTION_ENTER_MECHA', self.unit_obj.id)
            self.send_event('E_ON_ACTION_ENTER_MECHA')
            self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.set_follow_model_visible_without_record(False)
            global_data.emgr.mecha_boarded_event.emit(self.unit_obj)

        def delete_finish_cb():
            if not MODEL_SHADER_CTRL_SET_ENABLE:
                self._load_skin_model_and_effect()
            self.send_event('E_ON_ACTION_MECHA_FINISH')
            self.sd.ref_socket_res_agent and self.sd.ref_socket_res_agent.set_follow_model_visible_without_record(True)

        mecha_utils.create_summon_sfx(self, self.model, self._mecha_sfx, create_cb, delte_finish_cb=delete_finish_cb, mecha_id=self.sd.ref_mecha_id)

    def gen_board_check_callback(self, passenger, mecha_id):

        def cb():
            if not passenger.logic:
                return
            l_psg = passenger.logic
            if l_psg.ev_g_in_mecha() or l_psg.ev_g_death():
                return
            if not self.unit_obj:
                return
            psg_info = self.ev_g_passenger_info() or {}
            if passenger.id not in psg_info:
                return
            passenger.logic.send_event('E_ON_JOIN_MECHA', mecha_id, True)

        return cb

    def notify_passenger_board(self):
        passenger_info = self.ev_g_passenger_info()
        if len(passenger_info) <= 0:
            if not self._share:
                self._set_model_visible(False)
            return
        if self.unit_obj.get_owner().mecha_robot:
            self._set_model_visible(True)
        for passenger_id in six.iterkeys(passenger_info):
            passenger = EntityManager.getentity(passenger_id)
            if not passenger or not passenger.logic:
                if self.unit_obj.get_owner().mecha_robot:
                    self._load_skin_model_and_effect()
                continue
            passenger.logic.send_event('E_SET_BIND_MECHA_TYPE', self.sd.ref_mecha_id, self.unit_obj.get_owner().is_share())
            if passenger.logic.ev_g_need_play_join_anim():
                self.send_event('E_ENABLE_BEHAVIOR')
                pos = self.ev_g_position()
                self.play_board_anim(passenger.logic, pos)
                global_data.game_mgr.delay_exec(1.5, self.gen_board_check_callback(passenger, self.unit_obj.id))
            else:
                self._set_model_visible(True)
                self._load_skin_model_and_effect()
                passenger.logic.send_event('E_ON_JOIN_MECHA', self.unit_obj.id, True)

    def notify_share_board(self, passenger):
        passenger.send_event('E_ON_ACTION_ENTER_MECHA', self.unit_obj.id)
        self.send_event('E_RESET_STATE', mecha_status_config.MC_STAND)
        self.send_event('E_ON_ACTION_ENTER_MECHA')
        self.send_event('E_CLEAR_TWIST_PITCH')
        self.show_boarding_circle(False)
        self.send_event('E_ON_ACTION_MECHA_FINISH')

    def show_boarding_circle(self, show):
        bat = self.unit_obj.get_battle()
        if bat and bat.is_in_settle_celebrate_stage():
            return
        else:
            if show:
                if not self._boarding_circle_sfx:
                    if not self.model or not self.model.valid:
                        return

                    def create_cb(sfx, *args):
                        if self and self.is_valid():
                            self._boarding_circle_sfx = sfx
                        else:
                            global_data.sfx_mgr.remove_sfx(sfx)

                    global_data.sfx_mgr.create_sfx_in_scene('effect/fx/robot/common/kongtou_big.sfx', self.model.position, duration=-1, on_create_func=create_cb)
            elif self._boarding_circle_sfx:
                global_data.sfx_mgr.remove_sfx(self._boarding_circle_sfx)
                self._boarding_circle_sfx = None
            self._create_share_ui(show)
            return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def _create_share_ui(self, show):
        if show:
            if self._share_simui:
                self._share_simui.visible = True
                return
            model = self.ev_g_model()
            if model:
                self._share_simui = world.simuiobject(render.texture('gui/ui_res_2/simui/icon_getin_mech.png'))
                image_id = self._share_simui.add_image_ui(0, 0, 58, 55, 0, 0)
                self._share_simui_id = image_id
                self._share_simui.set_ui_align(image_id, 0.5, 0.5)
                self._share_simui.set_ui_fill_z(image_id, True)
                self._share_simui.set_parent(model)
                self._share_simui.visible = True
                self._share_simui.inherit_flag = world.INHERIT_TRANSLATION
                self._share_simui.position = math3d.vector(0, self._height, 0)
                self.need_update = True
        else:
            if self._share_simui:
                self._share_simui.visible = False
            self.need_update = False

    def on_load_animator_complete(self, *args):
        super(ComMechaModel, self).on_load_animator_complete(*args)
        self.add_camera_trigger_events()
        self.reset_animtor()
        self.preload_animation()
        animator = self.get_animator()
        if animator:
            is_avatar = self.is_avatar()
            animator.set_is_mainplayer(is_avatar)
            if self.sd.ref_mecha_id in MECHA_UP_BODY_TWIST_END_BONE:
                animator.find(robot_animation_const.TURN_Y_UP_BODY_NOD_NAME).endBone = MECHA_UP_BODY_TWIST_END_BONE[self.sd.ref_mecha_id]

    def reset_animtor(self):
        self.send_event('E_TWIST_YAW', 0)
        self.send_event('E_TWIST_PITCH', 0)

    def preload_animation(self):
        animtor = self.get_animator()
        if animtor and animtor.SupportFillEmptyAnim():
            return
        model = self.ev_g_model()
        if model and global_data.enable_mecha_cache_animation:
            try:
                from logic.gcommon.common_utils import status_utils
                data = status_utils.get_behavior_config(str(self.sd.ref_mecha_id))
                behavior_info = data.get_behavior(str(self.sd.ref_mecha_id))
                self.preload_animation_from_cnf(behavior_info)
                buff_info = data.behavior.get('buff')
                self.preload_animation_from_cnf(buff_info)
            except Exception as e:
                print('====Mecha preload_animation: Failed!')

    def preload_animation_from_cnf(self, cnf):
        if cnf:
            for sid, info in six.iteritems(cnf):
                preload_anim = info.get('preload_anim')
                if preload_anim:
                    action_param = info.get('action_param')
                    if action_param:
                        if isinstance(action_param, tuple):
                            time_stamp, action_info = action_param
                            clip_name = action_info[0]
                            dir_count = action_info[2]
                            self.preload_animation_by_dir(clip_name, dir_count)
                        elif isinstance(action_param, list):
                            for param_item in action_param:
                                time_stamp, action_info = param_item
                                clip_name = action_info[0]
                                dir_count = action_info[2]
                                self.preload_animation_by_dir(clip_name, dir_count)

                    custom_param = info.get('custom_param')
                    if custom_param:
                        shoot_anim_info = custom_param.get('shoot_anim')
                        if shoot_anim_info:
                            clip_name = shoot_anim_info[0]
                            dir_count = shoot_anim_info[2]
                            self.preload_animation_by_dir(clip_name, dir_count)

    def preload_animation_by_dir(self, clip_name, dir_count):
        model = self.ev_g_model()
        from logic.gcommon.component.client.com_character_ctrl.ComAnimMgr import DIR_SUFIX
        sufix_list = DIR_SUFIX[dir_count]
        for sufix_name in sufix_list:
            dir_clip_name = clip_name + sufix_name
            model.cache_animation(dir_clip_name, world.CACHE_ANIM_ALWAYS)

    def change_mecha_fashion(self, fashion):
        old_mecha_fashion_id = self._mecha_fashion_id
        if not has_skin_ext():
            from logic.gutils.dress_utils import get_mecha_default_fashion
            default_fashion = get_mecha_default_fashion(self.sd.ref_mecha_id)
            fashion[MECHA_FASHION_KEY] = {FASHION_POS_SUIT: default_fashion}
        self._mecha_fashion_id, mecha_shiny_wp_id = get_accurate_mecha_skin_info_from_fasion_data(self.sd.ref_mecha_id, fashion.get(MECHA_FASHION_KEY, {}))
        self._mecha_sfx = fashion.get('mecha_sfx', None)
        if old_mecha_fashion_id == self._mecha_fashion_id and mecha_shiny_wp_id == self._mecha_shiny_wp_id:
            return
        else:
            if self.model:
                if self._mecha_shiny_wp_id != mecha_shiny_wp_id:
                    self._mecha_shiny_wp_id = mecha_shiny_wp_id
                self._clear_skin_model_and_effect(need_clear_model_ref=True)
                path = get_mecha_model_path(self.sd.ref_mecha_id, self._mecha_fashion_id)
                old_is_ss = is_ss_level_skin(old_mecha_fashion_id)
                cur_is_ss = is_ss_level_skin(self._mecha_fashion_id)
                if not old_is_ss and not cur_is_ss:
                    self.send_event('E_REFRESH_MODEL')
                else:
                    self.send_event('E_BEGIN_REFRESH_WHOLE_MODEL')
                    self._lod_load_complete = False
                    self.refresh_empty_model(path)
            return

    def get_mecha_id(self):
        return self.sd.ref_mecha_id

    def get_mecha_fashion_id(self):
        return self._mecha_fashion_id

    def get_mecha_shiny_weapon_id(self):
        return self._mecha_shiny_wp_id

    def get_mecha_skin_and_shiny_weapon_id(self):
        return (
         self._mecha_fashion_id, self._mecha_shiny_wp_id)

    def get_aim_position(self):
        if self.model:
            socket = self.model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
            if socket:
                return socket.translation
        return None

    def get_mecha_hit_pos(self):
        if self.model and self.model.valid:
            if random.random() < 0.2:
                hit_bone = robot_animation_const.BONE_HEAD_NAME
            elif random.random() < 0.6:
                hit_bone = robot_animation_const.BONE_SPINE_NAME
            else:
                bone_list = [
                 robot_animation_const.BONE_LEFT_FOOT_NAME,
                 robot_animation_const.BONE_RIGHT_FOOT_NAME,
                 robot_animation_const.BONE_LEFT_HAND_NAME,
                 robot_animation_const.BONE_RIGHT_HAND_NAME]
                val = random.random()
                list_len = len(bone_list)
                val = int(math.floor(val * list_len))
                val = len(bone_list) - 1 if val > len(bone_list) - 1 else val
                hit_bone = bone_list[val]
            bone_mat = self.model.get_bone_matrix(hit_bone, world.SPACE_TYPE_WORLD)
            if bone_mat:
                return bone_mat.translation
            else:
                return self.ev_g_position() + math3d.vector(0, 3 * NEOX_UNIT_SCALE, 0)

        else:
            return self.ev_g_position() + math3d.vector(0, 3 * NEOX_UNIT_SCALE, 0)

    def is_avatar(self):
        if self._share:
            passenger_info = self.ev_g_passenger_info()
            has_passenger = bool(global_data.player and passenger_info and global_data.player.id in six.iterkeys(passenger_info))
            is_own_control = global_data.player and global_data.player.logic and self.unit_obj and global_data.player.logic.ev_g_control_target() == self.unit_obj.get_owner()
            return has_passenger or is_own_control
        else:
            return global_data.player and self._creator == global_data.player.id

    def is_creator(self, pid):
        return self._creator == pid

    def get_creator(self):
        return EntityManager.getentity(self._creator)

    def on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        self.be_hit_outline_display()
        if check_need_ignore_effect_behind_camera(shot_type, end_pos):
            return
        else:
            sfx_distance_scale = None
            if kwargs.get('trigger_is_self', False):
                player_vect = end_pos - begin_pos
                length_sqr = player_vect.length_sqr
                sfx_distance_scale = get_sfx_scale_by_length_spr(length_sqr)
            if shot_type:
                ext_dict = kwargs.get('ext_dict', {})
                hit_sfx_code = ext_dict.get('hit_sfx_code', 0)
                if hit_sfx_code:
                    hit_sfx_path, hit_sfx_code = decode_sfx_info(hit_sfx_code)
                    if hit_sfx_path:

                        def create_cb(sfx):
                            if hit_sfx_code:
                                sfx.scale = math3d.vector(hit_sfx_code, hit_sfx_code, hit_sfx_code)
                            elif sfx_distance_scale:
                                sfx.scale = math3d.vector(sfx_distance_scale, sfx_distance_scale, sfx_distance_scale)

                        ex_data = {}
                        camp_diff_param = confmgr.get('firearm_res_config', str(shot_type), 'cExtraParam', 'camp_diff', default=0)
                        if camp_diff_param and 'trigger_camp_id' in ext_dict and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_camp_id() != ext_dict['trigger_camp_id']:
                            if type(camp_diff_param) == str:
                                hit_sfx_path = camp_diff_param
                            else:
                                ex_data['need_diff_process'] = True
                        global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path, end_pos, on_create_func=create_cb, duration=0.5, int_check_type=CREATE_SRC_SIMPLE, ex_data=ex_data)
                        return
            hit_sfx_path = 'effect/fx/robot/common/robot_shouji.sfx'

            def create_cb(sfx):
                if sfx_distance_scale:
                    sfx.scale = math3d.vector(sfx_distance_scale, sfx_distance_scale, sfx_distance_scale)

            global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path, end_pos, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            return

    @execute_by_mode(True, ())
    def be_hit_outline_display(self, *args):
        return
        if not self.scene:
            return
        else:
            if global_data.player.logic.ev_g_is_campmate(self.unit_obj.ev_g_camp_id()):
                return
            if self._smooth_outline_timer_id:
                return
            model = self.ev_g_model()
            if model:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, True)
                self.scene.enable_smooth_outline(True, self.unit_obj.id)
                tm = global_data.game_mgr.get_logic_timer()
                if self._smooth_outline_timer_id:
                    tm.unregister(self._smooth_outline_timer_id)
                    self._smooth_outline_timer_id = None
                self._smooth_outline_timer_id = tm.register(func=lambda unit_id=self.unit_obj.id: self.close_smooth_outline(unit_id), interval=10.0, times=1, mode=CLOCK)
            return

    def close_smooth_outline(self, unit_id):
        if not self.scene:
            return
        else:
            model = self.ev_g_model()
            if model:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, False)
            if self._smooth_outline_timer_id:
                tm = global_data.game_mgr.get_logic_timer()
                tm.unregister(self._smooth_outline_timer_id)
                self._smooth_outline_timer_id = None
            self.scene.enable_smooth_outline(False, unit_id)
            return

    def on_fight_capacity_update(self):
        if global_data.mecha and self.unit_obj == global_data.mecha.logic:
            global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'achievement_level1'))
        self.show_level_up_mecha_sfx()
        self.show_level_up_screen_sfx()

    def show_level_up_mecha_sfx(self):
        model = self.model
        if model and model.valid:
            effect = model.get_socket_obj('fx_root', 0)
            if effect:
                effect.restart()
            else:
                model.set_socket_bound_obj_active('fx_root', 0, True)

    def show_level_up_screen_sfx(self):
        import math3d
        if global_data.player:
            if global_data.player.id == self.unit_obj.sd.ref_driver_id:
                size = global_data.really_sfx_window_size
                scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

                def create_cb(sfx):
                    sfx.scale = scale

                sfx_path = 'effect/fx/robot/robot_qishi/qishi_levelup.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_cb)

    def check_off_pos_valid(self, player_id, *args, **kwargs):
        return (False, self.ev_g_position())

    def on_join_mecha(self):
        passenger = self.ev_g_passenger_info()
        self._passenger = copy.copy(passenger)

    def on_post_join_mecha(self):
        if hasattr(get_on_mecha_utils, 'on_join_mecha_{}'.format(self.sd.ref_mecha_id)):
            join_handle = getattr(get_on_mecha_utils, 'on_join_mecha_{}'.format(self.sd.ref_mecha_id))
            join_handle(self)

    def on_notify_leave(self, show=True, delay=0):
        passenger_models = []
        if self._passenger and len(self._passenger) > 0:
            for passenger_id in six.iterkeys(self._passenger):
                entity = EntityManager.getentity(passenger_id)
                if not entity:
                    continue
                entity = entity.logic
                if not entity or not entity.is_valid():
                    continue
                if entity.ev_g_control_target() != self.unit_obj.get_owner():
                    continue
                passenger_models.append(entity.ev_g_model())

                def cb(*args):
                    if entity and entity.is_valid():
                        entity.send_event('E_ON_LEAVE_MECHA')
                        if show:
                            entity.send_event('E_SHOW_MODEL')
                        global_data.emgr.mecha_leaved_event.emit(self.unit_obj, entity)

                if delay > 0 and global_data.game_mgr.is_background_resumed():
                    global_data.game_mgr.delay_exec(delay, cb)
                    if entity.id == global_data.player.id:
                        ui = global_data.ui_mgr.show_ui('MechaWarningUI', 'logic.comsys.mecha_ui')
                        if ui:
                            ui.enter_screen()
                else:
                    cb()

        if not self._share and not self.ev_g_death():
            self.sd.ref_socket_res_agent.set_follow_model_visible_without_record(False)
            self._clear_skin_model_and_effect(ignore_model_res_clearing=True)
            global_data.game_mgr.delay_exec(1, lambda : mecha_utils.create_call_up_sfx(self, self.model, self._mecha_sfx, mecha_id=self.sd.ref_mecha_id, passenger_models=passenger_models))
        if self._share and self.sd.ref_hp > 0:
            self.show_boarding_circle(True)
        return passenger_models

    def on_die(self, *args):
        passenger_models = self.on_notify_leave(True, 1)
        if self._share:
            self.show_boarding_circle(False)
        if not self.ev_g_execute():
            global_data.game_mgr.delay_exec(4, lambda : mecha_utils.create_call_up_sfx(self, self.model, self._mecha_sfx, passenger_models=passenger_models))
        if self._share:
            global_data.emgr.scene_del_console.emit(self.unit_obj.id)

    def on_show_sub_mesh(self, sub_mesh_name_list, need_sync=True):
        self.sd.ref_socket_res_agent.set_sub_mesh_visible(sub_mesh_name_list, True)
        for sub_mesh_name in sub_mesh_name_list:
            self.sd.ref_socket_res_agent.set_sfx_res_visible(True, sub_mesh_name)

        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_SHOW_SUB_MESH, (sub_mesh_name_list,)), True, False, True)

    def on_hide_sub_mesh(self, sub_mesh_name_list, need_sync=True):
        self.sd.ref_socket_res_agent.set_sub_mesh_visible(sub_mesh_name_list, False)
        for sub_mesh_name in sub_mesh_name_list:
            self.sd.ref_socket_res_agent.set_sfx_res_visible(False, sub_mesh_name)

        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_HIDE_SUB_MESH, (sub_mesh_name_list,)), True, False, True)

    def is_mecha(self):
        return True

    def on_check_enter_zone(self, pos):
        if self.ev_g_is_full_seat():
            return (False, None)
        else:
            if self.sd.ref_hp <= 0:
                return (False, None)
            model = self.model
            if model and model.valid:
                lpos = pos - model.position
                size = self._trigger_size
                if size.z > lpos.z > -size.z and size.y > abs(lpos.y):
                    if size.x > lpos.x > -size.x:
                        return (True, lpos.length)
            return (
             False, None)

    def tick(self, delta):
        if self._share_simui and self._share_simui.valid:
            model = self.model
            if model and model.valid:
                pos = model.position
                dist = self.scene.active_camera.position - pos
                dist = dist.length / NEOX_UNIT_SCALE
                max_dist = 300
                scale = (max_dist - dist) / max_dist * 0.7
                self._share_simui.set_ui_scale(self._share_simui_id, scale, scale)

    def gm_rescale_mecha_model(self, scl_xyz):
        model = self.ev_g_model()
        if not model:
            return
        f_scl_xyz = float(scl_xyz)
        model.scale = math3d.vector(f_scl_xyz, f_scl_xyz, f_scl_xyz)

    def dump_all_state(self):
        from logic.gcommon.common_const import anticheat_const
        result_data = {'anim_state': self.ev_g_animator_state_desc(),'physx_state': self.ev_g_all_physx_state_desc(),'logic_state': self.ev_g_all_logic_state_desc()}
        global_data.player.respon_detect_client([(anticheat_const.DETECT_TYPE_HUMAN_STATE, result_data)])
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            print('test--dump_all_state--result_data =', result_data)

    def on_trans_to_share(self):
        self._share = True
        self.add_share_mecha_trigger()

    def get_mecha_original_model(self):
        return self._original_empty_model

    def get_mecha_second_model(self):
        return self._second_empty_model

    def get_mecha_original_animator(self):
        return self._original_animator

    def get_mecha_second_animator(self):
        return self._second_animator

    def on_switch_mecha_model(self, use_second_model):
        if not self._original_empty_model or not self._second_empty_model:
            return
        if self.sd.ref_using_second_model ^ use_second_model:
            self._set_model_visible(False)
            self._clear_skin_model_and_effect()
            if use_second_model:
                model = self._second_empty_model
                animator = self._second_animator
            else:
                model = self._original_empty_model
                animator = self._original_animator
            model.position = self._model.position
            self._model = model
            if self.is_zhujue:
                self.do_set_zhujue(self._model)
            if hasattr(model, 'decal_recievable'):
                self._model.decal_recievable = False
            self._set_model_visible(True)
            self._animator = animator
            self._load_skin_model_and_effect()
            self.sd.ref_using_second_model = use_second_model
            self.send_event('E_SWITCH_MODEL', model)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SWITCH_MECHA_MODEL, (use_second_model,)], True)

    def on_enable_sync(self, enable):
        if self.ev_g_is_avatar() and enable:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SWITCH_MECHA_MODEL, (self.sd.ref_using_second_model,)], True)

    def refresh_mecha_model(self):
        if self.model and self._skin_model_and_effect_loaded:
            self._clear_skin_model_and_effect()
            self._refresh_get_model_path_func()
            if global_data.force_mecha_empty_model_path != self.model.filename.replace('\\', '/'):
                self.send_event('E_BEGIN_REFRESH_WHOLE_MODEL')
                self._lod_load_complete = False
                path = self.get_model_path_func(self.sd.ref_mecha_id, self._mecha_fashion_id)
                self.refresh_empty_model(path)
                self._set_model_visible(True)
                self._load_skin_model_and_effect()
            else:
                self._load_skin_model_and_effect()

    def on_visible_in_this_frame_changed(self, visible):
        for callback in self.visible_in_this_frame_changed_callbacks:
            callback(visible)

    def on_add_visible_in_this_frame_changed_callback(self, callback):
        pass
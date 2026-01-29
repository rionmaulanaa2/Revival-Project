# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanAppearance.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import math3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from .ComAnimatorAppearance import ComAnimatorAppearance
from logic.gcommon.common_const import water_const
from logic.gcommon.const import DEFAULT_ROLE_ID, CHARACTER_LERP_DIR_YAWS
from logic.client.const import game_mode_const
from ...cdata import status_config
import game3d
from common.cfg import confmgr
import logic.gcommon.item.item_const as item_const
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.const import SEX_MALE, SEX_FEMALE
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.sfx_utils import get_dead_sfx_scale_by_length_spr
from logic.client.const.camera_const import POSTURE_STAND, POSTURE_SQUAT, POSTURE_GROUND, POSTURE_SWIM, POSTURE_JUMP
import common.utils.timer as timer
from common.utils.anticheat_utils import AnticheatUtils
from logic.gutils import character_action_utils
from logic.gutils.role_skin_utils import get_skin_trigger_at_intervals_res_info
from logic.gcommon.common_const.character_anim_const import *
from data import animation_event
from common.utils.timer import CLOCK
from logic.gcommon.cdata.status_config import desc_2_num
from logic.gutils.client_unit_tag_utils import register_unit_tag
FIGHT_STATE_DURATION = 2.0
IN_MECHA_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans', 'LMechaRobot'))

class ComHumanAppearance(ComAnimatorAppearance):
    DEFAULT_XML = animation_const.DEFAULT_XML
    PLAY_GUN_ANIMATION_HAND_ACTION = set([animation_const.HAND_STATE_GET_NEW_GUN, animation_const.HAND_STATE_LOAD, animation_const.HAND_STATE_ADD_BULLET])
    DYNAMIC_MASK_BONE_CLIP = animation_const.DYNAMIC_MASK_BONE_CLIP
    IS_PRE_LOAD_CLIP = False
    RELOAD_STATE = set([status_config.ST_RELOAD, status_config.ST_RELOAD_LOOP])
    SUB_COMPONENT_DIR_PATH = 'client.com_human_appearance'
    SUB_COMPONENT = [
     'ComLodWeapon', 'ComWeaponAnimation', 'ComLodHuman', 'ComEjection', 'ComSprayMaker', 'ComHumanSound']
    NEW_FRAMEWORK_COMS = [
     'ComHumanBehavior', 'ComAnimMgr', 'ComInput']
    DEFAULT_SUBMESH = (
     item_const.DRESS_POS_HAND, item_const.DRESS_POS_BOTTOMS, item_const.DRESS_POS_HAIR, item_const.DRESS_POS_BODICE, item_const.DRESS_POS_FACE)
    TRANSMIT_STATE_MAP = {animation_const.STATE_STAND: {animation_const.STATE_DOWN: animation_const.STATE_STAND_TO_DOWN
                                     },
       animation_const.STATE_JUMP: {animation_const.STATE_DOWN: animation_const.STATE_STAND_TO_DOWN
                                    },
       animation_const.STATE_DOWN: {animation_const.STATE_STAND: animation_const.STATE_DOWN_TO_STAND
                                    }
       }
    POSTURE_STATUS_MAP = {animation_const.STATE_STAND: POSTURE_STAND,
       animation_const.STATE_SQUAT: POSTURE_SQUAT,
       animation_const.STATE_CRAWL: POSTURE_GROUND,
       animation_const.STATE_SWIM: POSTURE_SWIM,
       animation_const.STATE_SKATE: POSTURE_STAND,
       animation_const.STATE_JUMP: POSTURE_JUMP
       }
    SEX_TO_ID = {SEX_MALE: '11',
       SEX_FEMALE: '12'
       }
    BIND_EVENT = ComAnimatorAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CTRL_STAND': 'stand',
       'E_RESET_STATE': 'reset_state',
       'E_CTRL_SQUAT': 'squat',
       'E_CANCEL_LOOK_CONSOLE': 'cancel_look_console',
       'E_CTRL_LOOK_CONSOLE': 'look_console',
       'E_DEFEATED': ('_defeated', 10),
       'G_POSTURE': 'get_posture_status',
       'G_ROLE_ID': 'get_role_id',
       'G_SEX': 'get_sex',
       'G_DRESS_STYLE': 'get_dress_style',
       'E_PLANE': 'hide_model',
       'E_SWITCH_STATUS': 'switch_to_status',
       'E_ON_CONTROL_TARGET_CHANGE': '_on_control_target_change',
       'G_APPEARANCE_IN_STAND': 'get_appearance_in_stand',
       'G_APPEARANCE_IN_SQUAT': 'get_appearance_in_squat',
       'G_APPEARANCE_IN_CRAWL': 'get_appearance_in_ground',
       'G_APPEARANCE_IN_SKATE': 'get_appearance_in_skate',
       'G_ANIM_STATE': '_get_anim_state',
       'G_NO_TRANSIT_ANIM_STATE': 'get_no_transit_anim_state',
       'E_ACTION_SET_EMPTY_HAND': 'set_empty_hand',
       'G_IS_STAND': 'is_stand',
       'G_IS_CROUCH': 'is_crouch',
       'E_SET_HAND_IK': 'set_hand_ik',
       'E_SET_FOOT_IK': 'set_foot_ik',
       'G_IS_HAVE_GUN': 'get_is_have_gun',
       'G_GET_REAL_CLIP': 'get_real_clip',
       'G_CONVERT_STR_TO_ANIM_LIST': 'convert_str_to_anim_list',
       'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': 'on_leave_state',
       'G_IS_IN_MECHA': 'is_in_mecha',
       'G_IS_RELOAD': 'is_reload',
       'G_IS_AVATAR': '_is_avatar',
       'E_AIM_MODEL_LOADED': '_accum_sfx_bind_to_camera',
       'E_AIM_MODEL_DESTROYED_BEGIN': '_accum_sfx_bind_to_weapon_model',
       'E_QUIT_AIM': ('_update_accum_sfx_pos', 99),
       'E_SET_IS_HAVE_GUN': '_set_is_have_gun',
       'E_FIGHT_CAP_UPGRADE_SFX': '_fight_capacity_up',
       'G_IS_HUMAN': 'is_human',
       'E_TEST_MOTORCYCLE': 'test_motorcycle',
       'E_STOP_TEST_MOTORCYCLE': 'stop_test_motorcycle',
       'E_ROTATE_MOTORCYCLE_MODEL': 'rotate_motorcycle_model',
       'G_VEHICLE_STATE': 'get_vehicle_state'
       })
    BIND_LOAD_FINISH_EVENT = ComAnimatorAppearance.BIND_LOAD_FINISH_EVENT.copy()
    BIND_LOAD_FINISH_EVENT.update({'E_CTRL_ACCUMULATE': 'on_accumulate',
       'G_AIM_POSITION': 'get_aim_position',
       'G_MODEL_RIGHT': '_get_right_dir',
       'G_GET_INVALID_BONE_INFO': 'get_invalid_bone_info',
       'E_DUMP_ALL_STATE': 'dump_all_state'
       })

    def __init__(self):
        super(ComHumanAppearance, self).__init__()
        self._is_dead = False
        self._current_posture_state = animation_const.STATE_STAND
        self._role_id = DEFAULT_ROLE_ID
        self._style = None
        self._dressed_clothing_id = None
        self._improved_skin_sfx_id = None
        self._show_improved_skin_sfx_states = set()
        self._remove_improved_skin_sfx_states = set()
        self._sub_model_list = []
        self._skin_sfx_list = []
        self._skin_timer_list = []
        self._trigger_at_intervals_sfx_info = {}
        self._in_fight_state = False
        self._fight_state_count_down = 0.0
        self._avatar_event_registered = False
        self._state_idx = animation_const.STATE_STAND
        self._no_transit_state_idx = self._state_idx
        self._hand_action = animation_const.HAND_STATE_NONE
        self._is_have_gun = 1
        self._accumulate_sfx = None
        self._is_accumulate = False
        self._delay_exec_id = None
        self._need_check_anim = False
        self._is_use_new_ik = False
        human_bone_info = confmgr.get('anti_cheat_params_config', 'check_param_config', 'Content', 'human_bone', 'param_value', default={'scale': 3,'height': 2.7})
        self._max_bone_scale = human_bone_info['scale']
        self._max_bone_height = human_bone_info['height']
        self.check_bone_timer_id = 0
        self._motor_model = None
        self.sd.ref_dressed_clothing_id = None
        return

    def get_all_animtion_event(self):
        sex = self.get_sex()
        char_id = self.SEX_TO_ID[sex]
        animtion_event = animation_event.all_animtion_event[char_id]
        return animtion_event

    def get_bone_valid_scale(self):
        return (
         0, self._max_bone_scale)

    def get_bone_valid_translation(self):
        return math3d.vector(self._max_bone_height / 2.0 * NEOX_UNIT_SCALE, self._max_bone_height * NEOX_UNIT_SCALE, self._max_bone_height / 2.0 * NEOX_UNIT_SCALE)

    def check_valid_bone_tick(self, *args):
        if self.ev_g_get_state(status_config.ST_MECHA_BOARDING):
            return
        invalid_bone_scale_info = self.get_bone_invalid_scale()
        invalid_bone_translation_info = self.get_bone_invalid_translation()
        invalid_bone_info = invalid_bone_scale_info
        if invalid_bone_translation_info:
            invalid_bone_info.update(invalid_bone_translation_info)

    def get_invalid_bone_info(self, *args):
        if self.ev_g_get_state(status_config.ST_MECHA_BOARDING):
            return
        invalid_bone_scale_info = self.get_bone_invalid_scale()
        invalid_bone_translation_info = self.get_bone_invalid_translation()
        invalid_bone_info = invalid_bone_scale_info
        if invalid_bone_translation_info:
            invalid_bone_info.update(invalid_bone_translation_info)
        return invalid_bone_info

    def get_vehicle_state(self, control_target=None, default_state=status_config.ST_MECHA_DRIVER):
        if not control_target:
            control_target = player.ev_g_control_target()
        if not control_target or not control_target.logic:
            return
        else:
            if control_target.logic.__class__.__name__ != 'LMotorcycle':
                return default_state
            seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
            if seat_index == 0:
                return status_config.ST_MECHA_DRIVER
            if seat_index == 1:
                return status_config.ST_VEHICLE_GUNNER
            return status_config.ST_VEHICLE_PASSENGER

    def is_human(self):
        return True

    def _get_anim_state(self):
        return self.current_posture_state

    def get_no_transit_anim_state(self):
        return self._no_transit_state_idx

    @property
    def current_posture_state(self):
        return self._current_posture_state

    @current_posture_state.setter
    def current_posture_state(self, value):
        self._current_posture_state = value

    def get_model_info(self, unit_obj, bdict):
        from logic.gcommon.item.item_const import DRESS_POS_FACE, DEFAULT_STYLE, LOD_L
        from logic.gutils import dress_utils
        self._style = bdict.get('style', DEFAULT_STYLE)
        position = bdict.get('position', (0, 390, -95)) or (0, 390, -95)
        pos = math3d.vector(*position)
        dress_dict = None
        from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
        self._dressed_clothing_id = bdict.get('fashion', {}).get(FASHION_POS_SUIT)
        self.sd.ref_dressed_clothing_id = self._dressed_clothing_id
        path = dress_utils.get_role_model_path(self._role_id, self._dressed_clothing_id)
        self._improved_skin_sfx_id = bdict.get('fashion', {}).get(FASHION_POS_WEAPON_SFX, None)
        self._show_improved_skin_sfx_states = set()
        self._remove_improved_skin_sfx_states = set()
        if self._improved_skin_sfx_id:
            conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(self._improved_skin_sfx_id), default={})
            for state in conf.get('trigger_states', []):
                if state in desc_2_num:
                    self._show_improved_skin_sfx_states.add(desc_2_num[state])

            for state in conf.get('remove_states', []):
                if state in desc_2_num:
                    self._remove_improved_skin_sfx_states.add(desc_2_num[state])

        self._position = pos
        return (
         path, None, (pos, dress_dict))

    def init_from_dict(self, unit_obj, bdict):
        if global_data.is_local_editor_mode:
            self.SUB_COMPONENT[2] = 'ComArtCheckLodHuman'
        super(ComHumanAppearance, self).init_from_dict(unit_obj, bdict)
        for comp_name in self.NEW_FRAMEWORK_COMS:
            com_obj = self.unit_obj.add_com(comp_name, 'client.com_character_ctrl')
            com_obj.init_from_dict(self.unit_obj, bdict)

        self._is_dead = bdict.get('is_dead', False) or bdict.get('is_defeated', False)
        self._is_in_mecha = bdict.get('is_in_mecha')
        self._role_id = bdict.get('role_id', DEFAULT_ROLE_ID)
        self.init_rotate()

    def init_rotate(self, *args):
        if self.sd.ref_is_avatar:
            f_pitch = self.ev_g_attr_get('head_pitch', 0)
            if f_pitch is not None:
                global_data.emgr.fireEvent('camera_set_pitch_event', f_pitch)
                self.send_event('E_CAM_PITCH', f_pitch)
            f_yaw = self.ev_g_attr_get('human_yaw', 0)
            global_data.emgr.fireEvent('camera_set_yaw_event', f_yaw)
        return

    def on_init_complete(self):
        anim_state = self.ev_g_attr_get('human_state')
        if anim_state in (animation_const.STATE_DRIVE,) and not self._is_in_mecha:
            self._need_check_anim = True
            anim_state = animation_const.STATE_STAND
        if anim_state in (animation_const.STATE_JUMP, animation_const.STATE_SQUAT_HELP, animation_const.STATE_CLIMB, animation_const.STATE_ROLL,
         animation_const.STATE_PARACHUTE, animation_const.STATE_ENTER_MECHA, animation_const.STATE_RUSH):
            anim_state = animation_const.STATE_STAND
        if self._is_dead:
            anim_state = animation_const.STATE_DIE
        if anim_state == animation_const.STATE_SWIM:
            if not self.ev_g_is_in_water_area():
                anim_state = animation_const.STATE_STAND
        logic_state = animation_const.ANIM_STATE_TO_LOGIC_STATE.get(anim_state, status_config.ST_STAND)
        if not self.ev_g_status_try_trans(logic_state):
            return
        if anim_state:
            self.current_posture_state = anim_state
        self.check_animation()
        for comp_name in self.NEW_FRAMEWORK_COMS:
            com_obj = self.unit_obj.get_com(comp_name)
            com_obj.on_init_complete()

    def destroy(self):
        if self._avatar_event_registered:
            self.unregist_event('E_FIRE', self.enter_fight_state)
            self.unregist_event('E_ON_HIT', self.enter_fight_state)
            self._avatar_event_registered = False
        super(ComHumanAppearance, self).destroy()

    def on_model_destroy(self):
        for sfx_id in self._skin_sfx_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._skin_sfx_list = []
        for timer_id in self._skin_timer_list:
            global_data.game_mgr.unregister_logic_timer(timer_id)

        self._skin_timer_list = []
        if self.ev_g_force_lobby_outline():
            self.send_event('E_FORCE_LOBBY_OUTLINE', False)
        if self.ev_g_force_shader_lod_level() is not None:
            self.send_event('E_FORCE_SHADER_LOD', None)
        if self.model and self.model.valid:
            for sub_model in self._sub_model_list:
                self.model.unbind(sub_model)

        self._sub_model_list = []
        super(ComHumanAppearance, self).on_model_destroy()
        if self.check_bone_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.check_bone_timer_id)
            self.check_bone_timer_id = 0
        self.unbind_model('ballon')
        self.unbind_model('root')
        if self._accumulate_sfx:
            global_data.sfx_mgr.remove_sfx(self._accumulate_sfx)
            self._accumulate_sfx = None
        if self._delay_exec_id:
            game3d.cancel_delay_exec(self._delay_exec_id)
            self._delay_exec_id = None
        return

    def dump_all_state(self):
        from logic.gcommon.common_const import anticheat_const
        result_data = {'anim_state': self.ev_g_animator_state_desc(),'physx_state': self.ev_g_all_physx_state_desc(),'logic_state': self.ev_g_all_logic_state_desc()}
        global_data.player.respon_detect_client([(anticheat_const.DETECT_TYPE_HUMAN_STATE, result_data)])
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            print('test--dump_all_state--result_data =', result_data)

    def get_real_clip(self, clip_name):
        if clip_name.startswith(animation_const.STAND_REPLACE_PREFIX):
            new_prefix = animation_const.STAND_REPLACE_PREFIX
            if self.is_crouch():
                new_prefix = animation_const.CROUCH_REPLACE_PREFIX
            else:
                new_prefix = animation_const.STAND_REPLACE_PREFIX
            if new_prefix != animation_const.STAND_REPLACE_PREFIX:
                clip_name = clip_name.replace(animation_const.STAND_REPLACE_PREFIX, new_prefix, 1)
        return clip_name

    def get_role_id(self):
        return self._role_id

    def get_sex(self):
        sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(self._role_id), 'sex') or SEX_MALE
        return sex

    def get_dress_style(self):
        return self._style

    def convert_str_to_anim_list(self, desc):
        import data.weapon_action_config as weapon_action_config
        return weapon_action_config.convert_to_list(desc)

    def get_hand_action(self):
        return self._hand_action

    def set_hand_action(self, hand_action, force=False):
        old_hand_action = self.get_hand_action()
        if not force:
            if hand_action == old_hand_action:
                return
        if old_hand_action in self.PLAY_GUN_ANIMATION_HAND_ACTION and hand_action not in self.PLAY_GUN_ANIMATION_HAND_ACTION:
            self.send_event('E_CHANGE_WEAPON_IDLE')
        if hand_action == animation_const.HAND_STATE_LOAD:
            weapon_load_type = animation_const.WEAPON_LOAD_FROM_IDLE
            if old_hand_action == animation_const.HAND_STATE_ADD_BULLET:
                weapon_load_type = animation_const.WEAPON_LOAD_FROM_ADD_BULLET
            self.send_event('E_SET_WEAPON_LOAD_TYPE', weapon_load_type)
        self._hand_action = hand_action
        part_enable = hand_action != animation_const.HAND_STATE_NONE
        if not part_enable:
            action_id = self.ev_g_weapon_action_id()
            if not (action_id == animation_const.WEAPON_TYPE_SHIELD and self.ev_g_is_jump()):
                self.send_event('E_EXIT_WEAPON_ACTION')
        self.set_hand_ik()

    def set_foot_ik(self):
        if not self.sd.ref_is_avatar or self._is_use_new_ik:
            return
        enable_foot_ik_list = (
         animation_const.STATE_SKATE,)
        is_enable_foot_ik = self.current_posture_state in enable_foot_ik_list
        self.send_event('S_FOOT_IK_ENABLE', is_enable_foot_ik)

    def set_hand_ik(self):
        return
        if self.ev_g_is_in_any_state((
         status_config.ST_DOWN, status_config.ST_PICK, status_config.ST_EMPTY_HAND,
         status_config.ST_HELP, status_config.ST_USE_ITEM, status_config.ST_PARACHUTE, status_config.ST_SKATE_MOVE, status_config.ST_SKATE_BRAKE,
         status_config.ST_ROLL, status_config.ST_SKATE, status_config.ST_CLIMB, status_config.ST_SHOOT, status_config.ST_AIM,
         status_config.ST_RUSH)) or self.ev_g_is_jump():
            self.send_event('S_GUN_IK_ENABLE', False)
        else:
            weapon_type = self.ev_g_weapon_type()
            if weapon_type == animation_const.WEAPON_TYPE_DOUBLE:
                self.send_event('S_GUN_IK_ENABLE', False)
                return
        hand_action = self.get_hand_action()
        disable_hand_ik_list = (
         animation_const.HAND_STATE_GET_NEW_GUN,
         animation_const.HAND_STATE_ADD_BULLET,
         animation_const.HAND_STATE_LOAD,
         animation_const.HAND_STATE_USE_ITEM)
        if hand_action in disable_hand_ik_list:
            self.send_event('S_GUN_IK_ENABLE', False)
        else:
            cur_weapon_pos = self.sd.ref_wp_bar_cur_pos
            if self.ev_g_is_gun_pos(cur_weapon_pos):
                weapon_data = self.sd.ref_wp_bar_mp_weapons.get(cur_weapon_pos)
                if weapon_data:
                    weapon_id = weapon_data.get_item_id()
                    action_id = confmgr.get('firearm_res_config', str(weapon_id), 'iActionType')
                    is_enable_ik = self.ev_g_is_action_enable_hand_ik(action_id)
                    self.send_event('S_GUN_IK_ENABLE', is_enable_ik)
                else:
                    self.send_event('S_GUN_IK_ENABLE', False)

    def _set_is_have_gun(self, is_have_gun):
        self._is_have_gun = is_have_gun
        self.send_event('E_CHANGE_GUN_STATE')

    def get_is_have_gun(self):
        return self._is_have_gun

    def set_empty_hand(self, is_empty):
        if is_empty:
            self.ev_g_status_try_trans(status_config.ST_EMPTY_HAND)
        else:
            self.ev_g_cancel_state(status_config.ST_EMPTY_HAND)
        is_have_gun = 1
        if is_empty:
            is_have_gun = 0
            self.send_event('E_ACTION_IS_SHOOT', 0)
        self._set_is_have_gun(is_have_gun)
        self.send_event('E_CHANGE_SPEED')
        self.set_hand_ik()

    def remove_unused_old_submesh(self, model):
        if not model:
            return
        for submesh_name in six_ex.values(item_const.MESH_CONF):
            if submesh_name not in self.DEFAULT_SUBMESH:
                model.remove_mesh(submesh_name)

    def _register_trigger_at_intervals_sfx_timer(self, interval):

        def load_sfx():
            if self._in_fight_state:
                return
            else:
                cur_state = self.ev_g_cur_state()
                if cur_state is None:
                    cur_state = set()
                if not self._show_improved_skin_sfx_states & cur_state:
                    return
                self.send_event('E_CREATE_MODEL_EFFECT', self._trigger_at_intervals_sfx_info, is_sync=True)
                return

        interval = global_data.artist_debug_interval or interval if 1 else global_data.artist_debug_interval
        timer_id = global_data.game_mgr.register_logic_timer(load_sfx, interval=interval, times=-1, mode=CLOCK)
        load_sfx()
        return timer_id

    def on_load_model_complete(self, model, user_data):
        super(ComHumanAppearance, self).on_load_model_complete(model, user_data)
        model.set_submesh_visible('empty', False)
        model.world_rotation_matrix.set_identity()
        scale = confmgr.get('role_info', 'RoleSkin', 'Content', str(self._dressed_clothing_id), 'battle_model_scale', default=None)
        if not scale:
            scale = confmgr.get('role_info', 'RoleInfo', 'Content', str(self._role_id), 'battle_model_scale')
        scale = scale or 1
        model.scale = math3d.vector(scale, scale, scale)
        self._is_use_new_ik = getattr(model, 'get_ik_mgr', False)
        pos, dress_dict = user_data
        pos = math3d.vector(self._position)
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(math3d.vector(pos.x, pos.y, pos.z), True)
        else:
            self.send_event('E_POSITION', math3d.vector(pos.x, pos.y, pos.z))
        self._set_state_idx(self.current_posture_state)
        self.set_no_transit_status(self.current_posture_state)
        if self.model:
            self.model.set_enable_lerp_dir_light(True)
            self.model.set_lerp_dir_light_yaws(CHARACTER_LERP_DIR_YAWS)
            if self.is_unit_obj_type('LAvatar'):
                self.model.shader_lod_type = world.SHADER_LOD_TYPE_PLAYER
            else:
                self.model.shader_lod_type = world.SHADER_LOD_TYPE_CHAR
        if hasattr(self.model, 'can_skip_update'):
            self.model.can_skip_update = False
        self.send_event('E_HUMAN_MODEL_LOADED', model, user_data)
        self.send_event('E_ENABLE_WATER_UPDATE', True)
        self.send_event('E_CHARACTER_ATTR', 'position', pos)
        self.send_event('E_CHARACTER_ATTR', 'reset_phys_attr', None)
        if self._improved_skin_sfx_id and self.sd.ref_is_avatar:
            if not self._avatar_event_registered:
                self.regist_event('E_FIRE', self.enter_fight_state)
                self.regist_event('E_ON_HIT', self.enter_fight_state)
                self._avatar_event_registered = True
            trigger_at_intervals_res_info = get_skin_trigger_at_intervals_res_info(self._improved_skin_sfx_id)
            if trigger_at_intervals_res_info:
                for res_info in trigger_at_intervals_res_info:
                    socket_list = res_info['socket_list']
                    res_path = res_info['res_path']
                    if res_path not in self._trigger_at_intervals_sfx_info:
                        self._trigger_at_intervals_sfx_info[res_path] = socket_list
                    else:
                        self._trigger_at_intervals_sfx_info[res_path].extend(socket_list)
                    interval = res_info['interval']
                    if res_path.endswith('.sfx'):
                        self._skin_timer_list.append(self._register_trigger_at_intervals_sfx_timer(interval))

        if self.ev_g_ctrl_mecha() is not None:
            model.visible = False
        if self._is_dead or self.ev_g_is_pure_mecha() is True:
            self.hide_model()
        self.set_foot_ik()
        return

    def check_animation(self):
        if self._need_check_anim:
            self._need_check_anim = False
            self.do_sync_action_status()

    def change_character_attr(self, name, *arg):
        super(ComHumanAppearance, self).change_character_attr(name, *arg)
        if name == 'animator_info':
            print(('test--ComHumanAppearance.change_character_attr--current_posture_state =', animation_const.STATE_DESC.get(self.current_posture_state, self.current_posture_state), '--unit_obj =', self.unit_obj))

    def on_load_animator_complete(self, *args):
        from logic.gcommon.common_utils.parachute_utils import STAGE_PLANE
        if self._is_in_mecha and not self.ev_g_in_mecha('MechaTrans') or self.sd.ref_parachute_stage == STAGE_PLANE:
            self.model_visible = False
        else:
            self.model_visible = True
        super(ComHumanAppearance, self).on_load_animator_complete(*args)
        self._set_state_idx(self.current_posture_state)
        self.set_hand_action(self._hand_action, force=True)
        self._set_is_have_gun(self._is_have_gun)
        self.preload_animation()
        if self.is_unit_obj_type('LAvatar'):
            self.add_camera_trigger_events()
        animator = self.get_animator()
        if not animator:
            return
        is_avatar = self._is_avatar()
        animator.set_is_mainplayer(is_avatar)

    def preload_animation(self):
        if ComHumanAppearance.IS_PRE_LOAD_CLIP:
            return
        ComHumanAppearance.IS_PRE_LOAD_CLIP = True
        import data.pick_clip_config as pick_clip_config
        import data.weapon_action_config as weapon_action_config
        model = self.get_model()
        if model and global_data.enable_cache_animation:
            for clip_name in six_ex.values(pick_clip_config.pick_type_clip_conf):
                model.cache_animation(clip_name, world.CACHE_ANIM_ALWAYS)

        if global_data.enable_cache_animation:
            for vary_animation in six_ex.values(weapon_action_config.weapon_type_2_action):
                for animation in six_ex.values(vary_animation):
                    if isinstance(animation, (list, tuple)):
                        for clip_name in animation:
                            self.preload_one_animation(clip_name)

                    else:
                        clip_name = animation
                        self.preload_one_animation(clip_name)

    def preload_one_animation(self, clip_name):
        if not global_data.enable_cache_animation:
            return
        model = self.get_model()
        if not model:
            return
        model.cache_animation(clip_name, world.CACHE_ANIM_ALWAYS)
        if clip_name.startswith(animation_const.STAND_REPLACE_PREFIX):
            clip_name = clip_name.replace(animation_const.STAND_REPLACE_PREFIX, animation_const.CROUCH_REPLACE_PREFIX, 1)
            model.cache_animation(clip_name, world.CACHE_ANIM_ALWAYS)

    def is_stand(self):
        return self.ev_g_is_in_any_state(character_action_utils.STAND_STATE)

    def is_crouch(self):
        return self.ev_g_is_in_any_state(character_action_utils.CROUCH_STATE)

    def _get_right_dir(self):
        if not self._model or not self._model.valid:
            return
        return self._model.world_rotation_matrix.right

    def get_transmit_status(self, new_state):
        transmit_dict = ComHumanAppearance.TRANSMIT_STATE_MAP.get(self.current_posture_state)
        if not transmit_dict:
            return None
        else:
            return transmit_dict.get(new_state)

    def look_console(self, *args):
        self.squat()

    def cancel_look_console(self, *args):
        self.stand(ignore_col=True)

    def get_model_dir_path(self):
        model_filename = None
        if self.model:
            model_filename = self.model.filename
        if not model_filename:
            return
        else:
            model_filename = model_filename.replace('\\', '/')
            name_list = model_filename.split('/')
            dir_path = None
            for index, name in enumerate(name_list):
                if name == 'character':
                    dir_path = '/'.join(name_list[:index + 2])
                    break

            return dir_path

    def reset_state(self, *args, **kwargs):
        self.stand()
        self.send_event('E_HAND_ACTION', animation_const.HAND_STATE_NONE)
        self.send_event('E_MOVE_STOP')

    def stand(self, *args, **kwargs):
        is_move = kwargs.get('is_move', False)
        if is_move:
            return
        ignore_col = False
        if kwargs:
            ignore_col = kwargs.get('ignore_col', False)
        is_avatar = self.sd.ref_is_avatar
        if is_avatar and not ignore_col:
            if not (self.ev_g_is_in_any_state((status_config.ST_SWIM, status_config.ST_CLIMB, status_config.ST_PARACHUTE)) or self.ev_g_is_jump()):
                if not self.ev_g_can_stand():
                    self.send_event('E_SHOW_MESSAGE', get_text_local_content(18017))
                    return
        if not self.ev_g_trans_status(status_config.ST_STAND, sync=True):
            return

    def _defeated(self, revive_time, killer_id, *args):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_KING):
            return
        killer_info = args[0]
        kill_effect_id = killer_info.get('reply_data', {}).get('killer_info', {}).get('kill_effect', 0)
        self.send_event('E_DEFEAT', killer_id, kill_effect_id)

    def squat(self, **kwargs):
        is_move = kwargs.get('is_move', False)
        if is_move:
            return
        else:
            water_status = self.sd.ref_water_status
            if water_status is None:
                water_status = 0
            if water_status >= water_const.WATER_MID_LEVEL:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                text = get_text_by_id(18115)
                self.send_event('E_SHOW_MESSAGE', text)
                return
            if not self.ev_g_trans_status(status_config.ST_CROUCH, sync=True):
                return
            self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
            return

    def set_no_transit_status(self, status):
        if status > animation_const.STATE_TRANSIT_MIN:
            status = animation_const.TRANSIT_STATUS_TO_FINAL_STATUS.get(status, animation_const.STATE_STAND)
        self._no_transit_state_idx = status
        self.send_event('E_CHANGE_ANIM_STATE')

    def _set_state_idx(self, status):
        self.current_posture_state = status
        if self._animator:
            self.set_no_transit_status(status)

    def switch_to_status(self, status, is_sync=True):
        if status == animation_const.STATE_STAND:
            if self.ev_g_get_state(status_config.ST_DOWN):
                return
        if not self._is_avatar() and self.current_posture_state == status:
            return
        else:
            logic_state = animation_const.ANIM_STATE_TO_LOGIC_STATE.get(status, None)
            self._set_state_idx(status)
            if self.current_posture_state == animation_const.STATE_PARACHUTE:
                self.send_event('E_END_PARACHUTING')
            if is_sync:
                self.do_sync_action_status()
            self.send_event('E_CHANGE_SPEED')
            self.set_hand_ik()
            self.set_foot_ik()
            return

    def do_sync_action_status(self):
        self.send_event('E_ACTION_SYNC_STATUS', self.current_posture_state)

    def get_posture_status(self):
        return ComHumanAppearance.POSTURE_STATUS_MAP.get(self.current_posture_state)

    def reset(self):
        super(ComHumanAppearance, self).reset()
        self.send_event('E_STAND')
        self.send_event('E_CLEAR_TWIST')

    def get_appearance_in_stand(self):
        return self.current_posture_state == animation_const.STATE_STAND

    def get_appearance_in_squat(self):
        return self.current_posture_state == animation_const.STATE_SQUAT

    def get_appearance_in_ground(self):
        return self.current_posture_state == animation_const.STATE_CRAWL

    def get_appearance_in_skate(self):
        return self.current_posture_state == animation_const.STATE_SKATE

    def get_aim_position(self):
        if not self._model or not self._model.valid:
            return None
        else:
            matrix = self._model.get_bone_matrix(animation_const.BONE_SPINE2_NAME, world.SPACE_TYPE_WORLD)
            if matrix:
                return matrix.translation
            return None

    def is_in_mecha(self):
        control_target = self.ev_g_control_target()
        return control_target and control_target.logic and control_target.logic.MASK & IN_MECHA_TAG_VALUE

    def is_reload(self):
        return self.ev_g_is_in_any_state(self.RELOAD_STATE)

    def _fight_capacity_up(self):
        if self.model and self.model.valid:
            effect = self.model.get_socket_obj('fx_root', 0)
            if effect:
                effect.restart()
            else:
                self.model.set_socket_bound_obj_active('fx_root', 0, True)
            size = global_data.really_sfx_window_size
            scale = math3d.vector(size[0] / 1280.0, size[1] / 720.0, 1.0)

            def create_cb(sfx):
                sfx.scale = scale

            sfx_path = 'effect/fx/robot/robot_qishi/qishi_levelup.sfx'
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, on_create_func=create_cb)

    def _is_avatar(self):
        return self.sd.ref_is_avatar

    def on_accumulate(self, flag):
        if self._accumulate_sfx:
            global_data.sfx_mgr.remove_sfx(self._accumulate_sfx)
            self._accumulate_sfx = None
        self._is_accumulate = flag
        if flag:
            self.send_event('E_ACTION_IS_SHOOT', 1)
            self.create_accumulate_sfx()
        else:
            self.send_event('E_ACTION_IS_SHOOT', 0)
        self.send_event('E_CHANGE_SPEED')
        return

    def create_accumulate_sfx(self):
        self._delay_exec_id = None
        if not self._is_accumulate:
            return
        else:
            weapon_model = self.ev_g_get_weapon_model()
            fire_pos = self.ev_g_get_fire_pos()

            def call_back(sfx):
                if self.is_valid() and self._is_accumulate:
                    if self._accumulate_sfx:
                        global_data.sfx_mgr.remove_sfx(self._accumulate_sfx)
                    fire_pos = self.ev_g_get_fire_pos()
                    if fire_pos:
                        sfx.position = fire_pos
                    self._accumulate_sfx = sfx
                    self._on_accum_sfx_created()
                else:
                    global_data.sfx_mgr.remove_sfx(sfx)

            if weapon_model and fire_pos:
                sfx_path = 'effect/fx/robot/robot_02/diancipao_xuli.sfx'
                global_data.sfx_mgr.create_sfx_for_model(sfx_path, weapon_model, fire_pos, on_create_func=call_back)
            else:
                self._delay_exec_id = game3d.delay_exec(500, self.create_accumulate_sfx)
            return

    def _enter_states(self, new_state):
        if new_state in self._remove_improved_skin_sfx_states:
            self.send_event('E_REMOVE_MODEL_EFFECT', self._trigger_at_intervals_sfx_info)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_REMOVE_MODEL_EFFECT, (self._trigger_at_intervals_sfx_info,)), True)

    def on_leave_state(self, leave_state, new_st=None):
        if status_config.ST_WEAPON_ACCUMULATE == leave_state:
            self.send_event('E_ACTION_IS_SHOOT', 0)
            if self._accumulate_sfx:
                global_data.sfx_mgr.remove_sfx(self._accumulate_sfx)
                self._accumulate_sfx = None
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_CTRL_ACCUMULATE, (False,)), True, False, True)
        return

    def _on_accum_sfx_created(self):
        if self._accumulate_sfx is None or not self._accumulate_sfx.valid:
            return
        else:
            cam_player = global_data.cam_lplayer
            cam_model = global_data.cam_model
            if cam_model and cam_model.valid and cam_player and cam_player == self.unit_obj:
                self._bind_sfx_to_camera()
                return
            self._bind_accum_sfx()
            return

    def _accum_sfx_bind_to_camera(self):
        cam_player = global_data.cam_lplayer
        cam_model = global_data.cam_model
        if cam_model and cam_model.valid and cam_player and cam_player == self.unit_obj:
            self._bind_sfx_to_camera()
            return
        self._bind_accum_sfx()

    def _accum_sfx_bind_to_weapon_model(self):
        self._bind_accum_sfx()

    def _bind_sfx_to_camera(self):
        if self._accumulate_sfx is None or not self._accumulate_sfx.valid:
            return
        else:
            scene = world.get_active_scene()
            cam = scene.active_camera
            if self._accumulate_sfx.get_parent():
                self._accumulate_sfx.remove_from_parent()
            if not self._accumulate_sfx.get_parent():
                self._accumulate_sfx.set_parent(cam)
            self._accumulate_sfx.position = math3d.vector(0, -10, 80)
            self._accumulate_sfx.visible = True
            return

    def _bind_accum_sfx(self):
        if not self._accumulate_sfx or not self._accumulate_sfx.valid:
            return
        model = self.ev_g_get_weapon_model()
        if model and model.valid:
            if self._accumulate_sfx.get_parent():
                self._accumulate_sfx.remove_from_parent()
            if not self._accumulate_sfx.get_parent():
                self._accumulate_sfx.set_parent(model)
            self._update_accum_sfx_pos()

    def _update_accum_sfx_pos(self):
        cam_player = global_data.cam_lplayer
        cam_model = global_data.cam_model
        if cam_model and cam_model.valid and cam_player and cam_player == self.unit_obj:
            return
        if not self._accumulate_sfx or not self._accumulate_sfx.valid:
            return
        fire_pos = self.ev_g_get_fire_pos()
        if not fire_pos:
            return
        transform_matrix = self._accumulate_sfx.transformation
        self._accumulate_sfx.world_transformation = transform_matrix
        self._accumulate_sfx.visible = True

    def enter_fight_state(self, *args):
        if not self._improved_skin_sfx_id:
            return
        self._in_fight_state = True
        self._fight_state_count_down = FIGHT_STATE_DURATION
        self.need_update = True

    def tick(self, dt):
        self._fight_state_count_down -= dt
        if self._fight_state_count_down <= 0.0:
            self._in_fight_state = False
            self.need_update = False
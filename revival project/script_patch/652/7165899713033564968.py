# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/SkateLogic.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import time
import math
import world
import math3d
import collision
from .StateBase import StateBase
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.cdata import status_config
from logic.gcommon.common_const import water_const
import logic.gcommon.common_utils.bcast_utils as bcast
import common.utils.timer as timer
import logic.gcommon.common_const.collision_const as collision_const
from logic.gcommon.component.client.com_character_ctrl.ComAnimMgr import DEFAULT_ANIM_NAME
from logic.gcommon.common_const.character_anim_const import *
from logic.gutils import character_action_utils
import logic.gutils.move_utils as move_utils
from logic.gcommon.cdata import speed_physic_arg
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.building_const import SKATE_BOUNDING_BOX_TUPLE
from logic.gcommon import editor
from ext_package.ext_decorator import has_skin_ext
from logic.gutils.dress_utils import init_spring_anim, get_file_name
from common.cfg import confmgr
HAS_SKATE_WEAPON_TYPE = set([animation_const.WEAPON_TYPE_BAZOOKA, animation_const.WEAPON_TYPE_SHIELD, animation_const.WEAPON_TYPE_DOUBLE, animation_const.WEAPON_TYPE_FROZEN, animation_const.WEAPON_TYPE_NORMAL, animation_const.WEAPON_TYPE_SNIPER_RIFLE, animation_const.WEAPON_TYPE_FLAMER])
ROLE_ID_POSTFIX = {12: 12,
   14: 12}
ROLE_ANIM_WITH_POST_FIX = {}
BRAKE_TIME = 1
TURN_X_FULL_BODY_NODE = 'turn_x_full_body'
SKATE_ACTION_CONFIG = {animation_const.SKATE_ACTION_NONE: 'SKATE_ACTION_NONE',
   animation_const.SKATE_ACTION_BOARD: 'SKATE_ACTION_BOARD',
   animation_const.SKATE_ACTION_PREPARE_MOVE: 'SKATE_ACTION_PREPARE_MOVE',
   animation_const.SKATE_ACTION_MOVE: 'SKATE_ACTION_MOVE',
   animation_const.SKATE_ACTION_BRAKE: 'SKATE_ACTION_BRAKE',
   animation_const.SKATE_ACTION_JUMP: 'SKATE_ACTION_JUMP',
   animation_const.SKATE_ACTION_LEAVE: 'SKATE_ACTION_LEAVE',
   animation_const.SKATE_ACTION_TURN_LEFT: 'SKATE_ACTION_TURN_LEFT',
   animation_const.SKATE_ACTION_TURN_RIGHT: 'SKATE_ACTION_TURN_RIGHT'
   }
BIND_WEAPON_PREFIX_CONFIG = {animation_const.WEAPON_TYPE_SHIELD: 'shield_'
   }
SKATE_BOUNDING_BOX = math3d.vector(SKATE_BOUNDING_BOX_TUPLE[0], SKATE_BOUNDING_BOX_TUPLE[1], SKATE_BOUNDING_BOX_TUPLE[2])

@editor.state_exporter({('min_trigger_brake_move_duration', 'param'): {'zh_name': '\xe6\x9c\x80\xe5\xb0\x8f\xe4\xbd\xbf\xe7\x94\xa8brake\xe5\x8a\xa8\xe4\xbd\x9c\xe7\x9a\x84\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4'},('skate_run_f', 'meter'): {'zh_name': '\xe6\xbb\x91\xe6\x9d\xbf\xe5\x89\x8d\xe8\xbf\x9b\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                              },
   ('skate_run_b', 'meter'): {'zh_name': '\xe6\xbb\x91\xe6\x9d\xbf\xe5\x90\x8e\xe9\x80\x80\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                              },
   ('skate_run_lr', 'meter'): {'zh_name': '\xe6\xbb\x91\xe6\x9d\xbf\xe4\xbe\xa7\xe6\xbb\x91\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                               },
   ('skate_move_fire', 'meter'): {'zh_name': '\xe6\xbb\x91\xe6\x9d\xbf\xe7\xa7\xbb\xe5\x8a\xa8\xe5\xbc\x80\xe6\x9e\xaa\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                                  },
   ('skate_move_reload_f', 'meter'): {'zh_name': '\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe5\x89\x8d\xe8\xbf\x9b\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                                      },
   ('skate_move_reload_b', 'meter'): {'zh_name': '\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe5\x90\x8e\xe9\x80\x80\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                                      },
   ('skate_move_reload_lr', 'meter'): {'zh_name': '\xe6\x8d\xa2\xe5\xbc\xb9\xe6\x97\xb6\xe4\xbe\xa7\xe7\xa7\xbb\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                                       },
   ('skate_move_aim', 'meter'): {'zh_name': '\xe6\xbb\x91\xe6\x9d\xbf\xe5\xbc\x80\xe9\x95\x9c\xe7\xa7\xbb\xe5\x8a\xa8\xe9\x80\x9f\xe5\xba\xa6','min_val': 0,'max_val': 100,'post_setter': lambda self: self.update_skate_speed()
                                 }
   })
class Skate(StateBase):
    BIND_EVENT = {'G_SKATE_MODEL': '_get_skate_model',
       'G_SKATE_ANIMATOR': 'get_skate_animator',
       'G_ATTACHABLE_ENTITY_ID': '_get_attach_entity_id',
       'E_SUCCESS_BOARD': '_success_board',
       'E_LEAVE_ATTACHABLE_ENTITY': '_leave_skate',
       'E_SKATE_ON_GROUND_FINISH': '_on_ground_finish',
       'E_CHANGE_ANIM_MOVE_DIR': 'change_anim_move_dir',
       'G_SKATE_ACTION': 'get_skate_action',
       'E_SET_SHAKE_ACTION': 'set_skate_action',
       'E_ACTION_SKATE_MOVE_STOP': '_move_stop',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_CHARACTER_ATTR': '_change_character_attr',
       'E_ENTER_STATE': 'enter_states',
       'E_LEAVE_STATE': 'leave_states',
       'E_CHANGE_SKATE_JUMP_STATE': '_change_jump_state',
       'E_CANCEL_SKATE_STATE': '_cancel_skate_state',
       'E_HIT_BLOOD_SFX': '_show_skate_hurt',
       'E_PLAY_SKATE_WATER_EFFECT': '_play_skate_water_effect',
       'E_CHANGE_WATER_INFO': '_set_water_status',
       'E_CHANGE_WATER_EFFECT_ARGS': 'change_water_effect_args',
       'E_NOTIFY_MOVE_STATE_CHANGE': 'on_change_move_state',
       'E_SKATE_FIRE': 'fire',
       'E_CHANGE_SKATE_IDLE': 'change_skate_idle',
       'E_CHANGE_SKATE_MOVE': 'change_skate_move',
       'E_CHANGE_SHOOT_STATE': 'change_skate_move',
       'E_CHANGE_WEAPON_MODEL': 'change_weapon',
       'E_ROCK_STOP': 'on_rocker_stop',
       'G_POSTFIX_ROLE_ID': 'get_postfix_role_id',
       'E_QUIT_RIGHT_AIM': 'quit_right_aim',
       'G_CHECK_FRONT_WINDOW': 'check_front_window'
       }
    DEFAULT_XML = 'animator_conf/skate.xml'
    IK_ID_MAP = {12: 12,13: 11,14: 12,15: 11,16: 11,22: 11}
    MIN_SWIM_EVENT_PASS_TIME = 0.2
    WATER_EFFECT_PATH = 'effect/fx/water/sheshui_shen.sfx'
    DO_NOT_PLAY_SKATE_STATUS = (
     status_config.ST_DOWN, status_config.ST_HELP)
    SKATE_ROCK_FAST_SPEED_MAX_YAW = move_utils.SKATE_ROCK_FAST_SPEED_MAX_YAW
    SKATE_ROCK_MEDIUM_SPEED_MAX_YAW = move_utils.SKATE_ROCK_MEDIUM_SPEED_MAX_YAW

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(Skate, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self._skate_model = None
        self._weapon_pos = 0
        self._skate_animator = None
        self._entity_id = 0
        self._table_id = 0
        self._col_obj = None
        self._skate_state = animation_const.SKATE_ACTION_NONE
        self._board_timer = None
        self._start_move_time = 0
        self._water_status = water_const.WATER_NONE
        self._water_effect_interval = 0.5
        self._water_effect_dist = 4.5
        self._water_effect_duration = 0.8
        self._last_effect_pos = None
        self._cur_pos = None
        self._clock = 0
        self._can_move_fire = False
        self._delay_fire_timer_id = None
        self._last_fire_timer = 0
        self._ik_mgr = None
        self._left_foot_ik = None
        self._left_socket_name = None
        self._right_foot_ik = None
        self._right_socket_name = None
        self._dir_x = 0
        self._dir_y = 0
        self._anim_duration = 0
        self.need_update = False
        self.tick_interval = self.custom_param.get('tick_interval', 0.2)
        self._soft_part_models = []
        self._soft_bone_param = {}
        self.min_trigger_brake_move_duration = self.custom_param.get('min_trigger_brake_move_duration', 2)
        self.skate_run_f = self.custom_param.get('skate_run_f', 7) * NEOX_UNIT_SCALE
        self.skate_run_b = self.custom_param.get('skate_run_b', 7) * NEOX_UNIT_SCALE
        self.skate_run_lr = self.custom_param.get('skate_run_lr', 7) * NEOX_UNIT_SCALE
        self.skate_move_fire = self.custom_param.get('skate_move_fire', 7) * NEOX_UNIT_SCALE
        self.skate_move_reload_f = self.custom_param.get('skate_move_reload_f', 7) * NEOX_UNIT_SCALE
        self.skate_move_reload_b = self.custom_param.get('skate_move_reload_b', 7) * NEOX_UNIT_SCALE
        self.skate_move_reload_lr = self.custom_param.get('skate_move_reload_lr', 7) * NEOX_UNIT_SCALE
        self.skate_move_aim = self.custom_param.get('skate_move_aim', 7) * NEOX_UNIT_SCALE
        return

    def on_init_complete(self):
        super(Skate, self).on_init_complete()
        self.update_skate_speed()

    def destroy(self):
        super(Skate, self).destroy()
        self._unload_res()
        self.cancel_board_timer()

    def update_skate_speed(self):
        self.send_event('E_SKATE_SPEED', 'skate_run_f', self.skate_run_f)
        self.send_event('E_SKATE_SPEED', 'skate_run_b', self.skate_run_b)
        self.send_event('E_SKATE_SPEED', 'skate_run_lr', self.skate_run_lr)
        self.send_event('E_SKATE_SPEED', 'skate_move_fire', self.skate_move_fire)
        self.send_event('E_SKATE_SPEED', 'skate_move_reload_f', self.skate_move_reload_f)
        self.send_event('E_SKATE_SPEED', 'skate_move_reload_b', self.skate_move_reload_b)
        self.send_event('E_SKATE_SPEED', 'skate_move_reload_lr', self.skate_move_reload_lr)
        self.send_event('E_SKATE_SPEED', 'skate_move_aim', self.skate_move_aim)

    def _change_character_attr(self, name, *arg):
        if not self.is_active:
            return
        if name == 'animator_info':
            only_active = arg[0]
            if self._skate_animator:
                enabled_ik = False
                if self._ik_mgr:
                    enabled_ik = self._ik_mgr.enabled
                human_model = self.ev_g_model()
                right_skate_socket_mat = self.skate_model.get_socket_matrix(self._right_socket_name, world.SPACE_TYPE_WORLD)
                right_end_bone_name = 'biped r thigh'
                right_end_bone_mat = human_model.get_bone_matrix(right_end_bone_name, world.SPACE_TYPE_WORLD)
                left_skate_socket_mat = self.skate_model.get_socket_matrix(self._left_socket_name, world.SPACE_TYPE_WORLD)
                left_end_bone_name = 'biped l thigh'
                left_end_bone_mat = human_model.get_bone_matrix(left_end_bone_name, world.SPACE_TYPE_WORLD)
                print(('test--Skate--animator_info--only_active =', only_active, '--enabled_ik =', enabled_ik, '--right_skate_socket_mat.translation =', right_skate_socket_mat.translation, '--right_skate_socket_mat.rotation =', right_skate_socket_mat.rotation, '--right_end_bone_mat.translation =', right_end_bone_mat.translation, '--right_end_bone_mat.rotation =', right_end_bone_mat.rotation, '--left_skate_socket_mat.translation =', left_skate_socket_mat.translation, '--left_skate_socket_mat.rotation =', left_skate_socket_mat.rotation, '--left_end_bone_mat.translation =', left_end_bone_mat.translation, '--left_end_bone_mat.rotation =', left_end_bone_mat.rotation, '--_skate_state =', SKATE_ACTION_CONFIG[self._skate_state], '--_ik_mgr =', self._ik_mgr, '--skate_model.filename =', self.skate_model.filename, '--self.unit_obj =', self.unit_obj))
                self._skate_animator.print_info(active=only_active)
        elif name == 'debug_skate_foot_bind_point':
            model = self.skate_model
            left_foot_matrix = model.get_socket_matrix('left_foot', world.SPACE_TYPE_WORLD)
            right_foot_matrix = model.get_socket_matrix('right_foot', world.SPACE_TYPE_WORLD)
            print('test--left_foot_matrix =', left_foot_matrix)
            print('test--right_foot_matrix =', right_foot_matrix)
            begin_pos_list = ((left_foot_matrix.translation, 255), (right_foot_matrix.translation, 65280))
            line_list = []
            for begin_pos, color in begin_pos_list:
                end_pos = begin_pos + math3d.vector(0, 5, 0)
                one_line_info = (begin_pos, end_pos, color)
                line_list.append(one_line_info)

            self.send_event('E_DRAW_LINE', line_list)

    def on_load_animator_complete(self, *args):
        human_model = self.ev_g_model()
        if not human_model:
            return
        else:
            if not self._ik_mgr and getattr(human_model, 'get_ik_mgr', None):
                self._ik_mgr = human_model.get_ik_mgr()
                SKATE_FOOT_IK_PRIOTY = 100
                self._left_foot_ik = self._ik_mgr.create_two_bone_ik('left_foot', 'biped l foot', SKATE_FOOT_IK_PRIOTY)
                self._right_foot_ik = self._ik_mgr.create_two_bone_ik('right_foot', 'biped r foot', SKATE_FOOT_IK_PRIOTY)
                self._ik_mgr.enabled = False
            all_attachable = self.ev_g_all_attachable()
            if all_attachable:
                if self.ev_g_status_try_trans(status_config.ST_SKATE):
                    for entity_id, data in six.iteritems(all_attachable):
                        table_id = data['atch_id']
                        self._success_board(entity_id, table_id)

            return

    def on_change_move_state(self, *args, **kwargs):
        if not self.is_active:
            return
        move_action = self.ev_g_move_state()
        if move_action == animation_const.MOVE_STATE_TURN_LEFT:
            self.set_skate_action(animation_const.SKATE_ACTION_TURN_LEFT)
        elif move_action == animation_const.MOVE_STATE_TURN_RIGHT:
            self.set_skate_action(animation_const.SKATE_ACTION_TURN_RIGHT)
        if move_action != animation_const.MOVE_STATE_STAND:
            if move_action not in (animation_const.MOVE_STATE_TURN_LEFT, animation_const.MOVE_STATE_TURN_RIGHT):
                self.send_event('E_SKATE_CHANGE_DIR_SOUND')

    def get_skate_animator(self):
        return self._skate_animator

    def _get_attach_entity_id(self):
        return self._entity_id

    def _set_water_status(self, water_height, water_status):
        self._water_status = water_status
        if self.is_active and (self._water_status != water_const.WATER_NONE or self.ev_g_is_in_water_area()):
            self.need_update = True
        elif self.skate_model:
            self.need_update = False

    def change_water_effect_args(self, dist, duration, interval):
        self._water_effect_dist = dist
        self._water_effect_duration = duration
        self._water_effect_interval = interval

    def tick_check_board(self):
        if not self.ev_g_status_try_trans(status_config.ST_SKATE):
            return
        else:
            self._board_timer = None
            self._do_board()
            return timer.RELEASE
            return

    def _success_board(self, entity_id, table_id):
        if self.skate_model:
            self._end_leave()
        self._entity_id = entity_id
        self._table_id = table_id
        is_swim = self.ev_g_get_state(status_config.ST_SWIM)
        if not self.ev_g_status_try_trans(status_config.ST_SKATE):
            if is_swim:
                self.send_event('E_STOP_SWIM')
                self._water_status = self.sd.ref_water_status
            self.cancel_board_timer()
            self._board_timer = global_data.game_mgr.register_logic_timer(self.tick_check_board, 1)
            return
        self._do_board()
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_SHIELD:
            self.send_event('E_CHANGE_WEAPON_IDLE')

    def _get_skate_model(self):
        return self.skate_model

    def init_ik(self):
        model = self.ev_g_model()
        if not model:
            return
        if not self._ik_mgr:
            return
        self._ik_mgr.enabled = True
        self.change_weapon()

    def init_soft_bone(self):
        if not self.sd.ref_is_avatar:
            return
        if not self.skate_model:
            return
        file_name = get_file_name(self.skate_model)
        soft_bone_param = confmgr.get(file_name)
        if not soft_bone_param:
            return
        part_models = init_spring_anim(self.skate_model, soft_bone_param)
        self._soft_part_models = six_ex.keys(part_models)
        self._soft_bone_param = soft_bone_param

    def change_weapon(self, *args):
        model = self.ev_g_model()
        if not model:
            return
        if not self._ik_mgr or not self._ik_mgr.enabled:
            return
        skate_model = self.skate_model
        role_id = self.ev_g_role_id()
        role_id_map = self.IK_ID_MAP.get(role_id, 11)
        action_id = self.ev_g_weapon_action_id()
        weapon_prefix = BIND_WEAPON_PREFIX_CONFIG.get(action_id, '')
        left_socket_name = weapon_prefix + 'left_foot_' + str(role_id_map)
        self._left_foot_ik.set_target(skate_model, world.BIND_TYPE_SOCKET, left_socket_name)
        self._left_socket_name = left_socket_name
        right_socket_name = weapon_prefix + 'right_foot_' + str(role_id_map)
        self._right_foot_ik.set_target(skate_model, world.BIND_TYPE_SOCKET, right_socket_name)
        self._right_socket_name = right_socket_name

    def _create_skate_bind_collision(self):
        collision_type = collision.BOX
        skate_model = self.skate_model
        bounding_box = SKATE_BOUNDING_BOX
        mask = collision_const.GROUP_SKATE_INCLUDE | collision_const.GROUP_GRENADE
        group = collision_const.GROUP_SKATE_INCLUDE | collision_const.GROUP_SHOOTUNIT
        mass = 0
        self._col_obj = collision.col_object(collision_type, bounding_box, mask, group, mass)
        scene = world.get_active_scene()
        if scene:
            scene.scene_col.add_object(self._col_obj)
        skate_model.bind_col_obj(self._col_obj, 'bone001')
        global_data.emgr.scene_add_common_shoot_obj.emit(self._col_obj.cid, self.unit_obj)

    def _init_skate_collision(self):
        bounding_box = SKATE_BOUNDING_BOX
        width = collision_const.CHARACTER_STAND_WIDTH
        height = collision_const.CHARACTER_STAND_HEIGHT + bounding_box.y * 2
        self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height)
        character = self.sd.ref_character
        if character:
            character_offset_x = collision_const.STAND_MODEL_OFFSET_X
            character_down_height = collision_const.STAND_MODEL_OFFSET_Y + character.getPadding()
            character.setXOffset(-character_offset_x)
            character.setYOffset(-character_down_height)

    def check_before_window_by_offset(self, check_base_pos, forward_vect, forward_offset, draw_line=False):
        scn = world.get_active_scene()
        group_climb_check = collision_const.GROUP_CLIMB_CHECK
        WINDOW_CHECK_HEIGHT = 2.0 * NEOX_UNIT_SCALE
        chect_begin = check_base_pos + forward_vect * forward_offset
        up_vect = math3d.vector(0.0, 1.0, 0.0)
        check_end = chect_begin + up_vect * WINDOW_CHECK_HEIGHT
        up_result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
        if draw_line:
            pos_list = [
             chect_begin, check_end]
            global_data.emgr.scene_draw_line_event.emit(pos_list, alive_time=100, color=16711680)
        down_vect = math3d.vector(0.0, -1.0, 0.0)
        check_end = chect_begin + down_vect * WINDOW_CHECK_HEIGHT
        down_result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
        if draw_line:
            pos_list = [
             chect_begin, check_end]
            global_data.emgr.scene_draw_line_event.emit(pos_list, alive_time=100, color=16711680)
        if up_result[0] and down_result[0]:
            distance = (up_result[1] - down_result[1]).length
            if draw_line:
                pos_list = [
                 down_result[1], math3d.vector(down_result[1].x + 300, down_result[1].y, down_result[1].z)]
                global_data.emgr.scene_draw_line_event.emit(pos_list, alive_time=100, color=16711680)
            if distance / NEOX_UNIT_SCALE < 2.0:
                return True
        return False

    def check_front_window(self):
        if global_data.player and global_data.player.logic and self.sd.ref_character:
            player_pos = global_data.player.logic.ev_g_foot_position()
            if not player_pos:
                return False
            model_yaw = global_data.player.logic.ev_g_yaw()
            forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
            WINDOWSILL_HEIGHT = 1.5 * NEOX_UNIT_SCALE
            check_base_pos = player_pos + math3d.vector(0, WINDOWSILL_HEIGHT, 0)
            forward = 0
            while forward < 3:
                forward += 0.2
                if self.check_before_window_by_offset(check_base_pos, forward_vect, forward * NEOX_UNIT_SCALE, False):
                    return True

        return False

    def check_before_window(self):
        if global_data.player and global_data.player.logic and self.sd.ref_character:
            if self.ev_g_get_state(status_config.ST_JUMP_1) or self.ev_g_get_state(status_config.ST_JUMP_2):
                player_pos = global_data.player.logic.ev_g_foot_position()
                if not player_pos:
                    return
                if self.sd.ref_character.getHeight() <= 13.0:
                    return
                model_yaw = global_data.player.logic.ev_g_yaw()
                forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
                WINDOWSILL_HEIGHT = 1.2 * NEOX_UNIT_SCALE
                check_base_pos = player_pos + math3d.vector(0, WINDOWSILL_HEIGHT, 0)
                WINDOWSILL_FORWARD_1 = 0.2 * NEOX_UNIT_SCALE
                WINDOWSILL_FORWARD_2 = 0.4 * NEOX_UNIT_SCALE
                if self.check_before_window_by_offset(check_base_pos, forward_vect, WINDOWSILL_FORWARD_1) or self.check_before_window_by_offset(check_base_pos, forward_vect, WINDOWSILL_FORWARD_2):
                    self.sd.ref_character.setHeight(12.8)

    def check_on_window_by_offset(self, player_pos, forward_vect, forward_offset):
        scn = world.get_active_scene()
        group_climb_check = collision_const.GROUP_CLIMB_CHECK
        WINDOW_HEIGHT = 2.0 * NEOX_UNIT_SCALE
        chect_begin = player_pos + math3d.vector(0, WINDOW_HEIGHT / 2, 0) + forward_vect * forward_offset
        up_vect = math3d.vector(0.0, 1.0, 0.0)
        check_end = chect_begin + up_vect * (WINDOW_HEIGHT / 2 + 0.3)
        up_result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
        down_vect = math3d.vector(0.0, -1.0, 0.0)
        check_end = chect_begin + down_vect * (WINDOW_HEIGHT / 2 + 0.3)
        down_result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
        if up_result[0] and down_result[0]:
            return True
        else:
            return False

    def check_on_window(self):
        if global_data.player and global_data.player.logic:
            player_pos = global_data.player.logic.ev_g_foot_position()
            if not player_pos:
                return False
            model_yaw = global_data.player.logic.ev_g_yaw()
            forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
            back_vect = math3d.vector(-forward_vect.x, 0.0, -forward_vect.z)
            up_vect = math3d.vector(0, 1, 0)
            left_vect = forward_vect.cross(up_vect)
            right_vect = math3d.vector(-left_vect.x, 0.0, -left_vect.z)
            dir_vects = [forward_vect, back_vect, left_vect, right_vect]
            WINDOWSILL_FORWARD_1 = 0.2 * NEOX_UNIT_SCALE
            WINDOWSILL_FORWARD_2 = 0.4 * NEOX_UNIT_SCALE
            for dir_vect in dir_vects:
                if self.check_on_window_by_offset(player_pos, dir_vect, WINDOWSILL_FORWARD_1) or self.check_on_window_by_offset(player_pos, dir_vect, WINDOWSILL_FORWARD_2):
                    return True

            return False
        else:
            return False

    def enter_states(self, new_state):
        if not self.is_active:
            return
        if self.ev_g_is_jump():
            if self._ik_mgr:
                self._ik_mgr.enabled = False
        if new_state == status_config.ST_JUMP_1:
            pass
        elif new_state == status_config.ST_JUMP_2:
            self._change_jump_state(animation_const.JUMP_STATE_IN_AIR)
        elif new_state == status_config.ST_JUMP_3:
            self._change_jump_state(animation_const.JUMP_STATE_FALL_GROUND)
            if global_data.enable_skate_cross_window:
                if self.check_on_window():
                    character = self.sd.ref_character
                    if character:
                        character.setHeight(12.8)
                else:
                    bounding_box = SKATE_BOUNDING_BOX
                    width = collision_const.CHARACTER_STAND_WIDTH
                    height = collision_const.CHARACTER_STAND_HEIGHT + bounding_box.y * 2
                    self.send_event('E_RECREATE_CHARACTER', width, height, 0)
        elif new_state == status_config.ST_SHOOT:
            if not self.ev_g_get_state(status_config.ST_SKATE_MOVE) and not self.ev_g_get_state(status_config.ST_SKATE_BRAKE) and self.ev_g_get_state(status_config.ST_MOVE) and self.ev_g_get_state(status_config.ST_SKATE):
                self.set_skate_action(animation_const.SKATE_ACTION_NONE)
                self.send_event('E_MOVE_STOP')
        elif new_state == status_config.ST_MOVE:
            skate_state = self.get_skate_action()
            rocker_dir = self.sd.ref_rocker_dir
            if skate_state == animation_const.SKATE_ACTION_NONE and rocker_dir and not rocker_dir.is_zero:
                self._set_move_dir(rocker_dir.x, rocker_dir.z)

    def leave_states(self, leave_state, new_state=None):
        if leave_state == status_config.ST_SKATE_BRAKE:
            if self.ev_g_get_state(status_config.ST_SKATE) and self.ev_g_get_state(status_config.ST_MOVE):
                self.ev_g_status_try_trans(status_config.ST_SKATE_MOVE)
            if new_state in (status_config.ST_JUMP_1, status_config.ST_JUMP_2):
                self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        elif leave_state == status_config.ST_JUMP_3:
            skate_state = self.get_skate_action()
            rocker_dir = self.sd.ref_rocker_dir
            if skate_state == animation_const.SKATE_ACTION_JUMP and (not rocker_dir or rocker_dir.is_zero):
                self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        elif leave_state == self.status_config.ST_TURN:
            self._end_turn()
        elif leave_state == self.sid:
            if self.is_active:
                self.send_event('E_LEAVE_ATTACHABLE_ENTITY')
            if self._water_status == water_const.WATER_DEEP_LEVEL:
                water_height = self.ev_g_water_height()
                self.send_event('E_START_SWIM', water_height)
        if self.is_active:
            if not self.ev_g_is_jump():
                if self._ik_mgr:
                    self._ik_mgr.enabled = True

    def _end_turn(self, *args):
        if not self.is_active:
            return
        skate_state = self.get_skate_action()
        if skate_state != animation_const.SKATE_ACTION_TURN_LEFT and skate_state != animation_const.SKATE_ACTION_TURN_RIGHT:
            return
        self.set_skate_action(animation_const.SKATE_ACTION_NONE)

    def _show_skate_hurt(self, from_pos, target_pos, shot_type, **kwargs):
        dmg_parts = kwargs.get('dmg_parts', None)
        if not dmg_parts:
            return
        else:
            from logic.gcommon.const import HIT_PART_SKATE
            for part in dmg_parts:
                if part == HIT_PART_SKATE:
                    skate_model = self.skate_model
                    if skate_model:
                        global_data.emgr.model_hitted_effect_event.emit(skate_model, from_pos, target_pos)
                    return

            return

    def _change_jump_state(self, *args):
        if not self.is_active:
            return
        self.set_skate_action(animation_const.SKATE_ACTION_JUMP)

    def get_postfix_role_id(self):
        role_id = self.ev_g_role_id()
        postfix_id = ROLE_ID_POSTFIX.get(role_id)
        return postfix_id

    def check_clip_need_postfix(self, action_key, clip_list):
        skate_model = self.skate_model
        if not skate_model:
            return clip_list
        else:
            if not clip_list:
                return
            if not action_key:
                return clip_list
            action_id = self.ev_g_weapon_action_id()
            role_id = self.ev_g_role_id()
            postfix_id = ROLE_ID_POSTFIX.get(role_id)
            if postfix_id:
                cache_clip_list = ROLE_ANIM_WITH_POST_FIX.setdefault(postfix_id, {}).setdefault(action_id, {}).setdefault(action_key, None)
                if not cache_clip_list:
                    new_clip_name = clip_list[0] + '_' + str(postfix_id)
                    if not skate_model.has_anim(new_clip_name):
                        return clip_list
                    cache_clip_list = list(clip_list)
                    for index, clip_name in enumerate(cache_clip_list):
                        clip_name = clip_name + '_' + str(postfix_id)
                        cache_clip_list[index] = clip_name

                    ROLE_ANIM_WITH_POST_FIX.setdefault(postfix_id, {}).setdefault(action_id, {}).setdefault(action_key, cache_clip_list)
                clip_list = cache_clip_list
            return clip_list

    def change_skate_idle(self):
        if not self.is_active:
            return
        self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        self._begin_skate_idle()

    def _begin_skate_idle(self):
        action_key = 'skate_idle'
        clip_list = self.ev_g_weapon_action_list(action_key)
        timeScale = 1
        blend_time = 0.2
        self.send_event('E_POST_ACTION', clip_list[0], LOW_BODY, 1, loop=True, blend_time=blend_time, timeScale=timeScale, force_upate_anim=False)
        weapon_type = self.ev_g_weapon_type()
        is_shoot = self.ev_g_action_is_shoot()
        if is_shoot and weapon_type != animation_const.WEAPON_TYPE_BAZOOKA:
            clip_name, _, _ = character_action_utils.get_idle_clip(self, self.status_config.ST_STAND)
            self.send_event('E_POST_ACTION', clip_name, LOWER_UP_BODY, 1, loop=True, blend_time=0.2, force_upate_anim=False)
        else:
            self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)
        clip_list = self.check_clip_need_postfix(action_key, clip_list)
        clip_name = clip_list[0]
        self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, 1, loop=True, blend_time=blend_time, ignore_sufix=True, timeScale=timeScale, force_upate_anim=False)

    def quit_right_aim(self, *args):
        self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)

    def _begin_skate_move(self):
        action_key = 'skate_stand_move'
        is_shoot = self.ev_g_action_is_shoot()
        if is_shoot:
            action_key = 'skate_stand_shoot_move'
        clip_list = self.ev_g_weapon_action_list(action_key)
        dir_type = len(clip_list)
        loop = True
        clip_name = clip_list[0][:-3]
        blend_time = 0.2
        time_scale = 1
        self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, blend_time=blend_time, timeScale=time_scale)
        if self.ev_g_get_state(self.status_config.ST_RIGHT_AIM):
            self.send_event('E_POST_ACTION', clip_name, LOWER_UP_BODY, dir_type, loop=loop, blend_time=blend_time, timeScale=time_scale)
        role_id = self.ev_g_role_id()
        postfix_id = ROLE_ID_POSTFIX.get(role_id, 0)
        self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, dir_type, loop=loop, blend_time=blend_time, timeScale=time_scale, postfix_id=postfix_id)

    def change_skate_move(self):
        if not self.is_active:
            return
        if self.ev_g_is_jump():
            return
        if self._skate_state not in (animation_const.SKATE_ACTION_PREPARE_MOVE, animation_const.SKATE_ACTION_MOVE, animation_const.SKATE_ACTION_BRAKE):
            if self.sd.ref_lower_up_body_anim and not self.ev_g_is_jump() and not self.ev_g_action_is_shoot():
                self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)
            return
        weapon_type = self.ev_g_weapon_type()
        is_shoot = self.ev_g_action_is_shoot()
        action_key = 'skate_stand_move'
        if self.ev_g_action_is_shoot():
            action_key = 'skate_stand_shoot_move'
        clip_list = self.ev_g_weapon_action_list(action_key)
        clip_name = clip_list[0][:-3]
        dir_type = len(clip_list)
        role_id = self.ev_g_role_id()
        postfix_id = ROLE_ID_POSTFIX.get(role_id, 0)
        self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, dir_type, loop=True, blend_time=0.2, timeScale=1, postfix_id=postfix_id)

    def fire(self, *args):
        now_time = time.time()
        if self._delay_fire_timer_id:
            pass_time = now_time - self._last_fire_timer
            skate_move_delay_fire_time = 0.2
            if pass_time > skate_move_delay_fire_time:
                if self._delay_fire_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self._delay_fire_timer_id)
                    self._delay_fire_timer_id = None
            else:
                return
        self._last_fire_timer = now_time
        if self.ev_g_get_state(status_config.ST_SKATE_BRAKE):
            skate_move_delay_fire_time = 0.2
            self._delay_fire_timer_id = global_data.game_mgr.register_logic_timer(self.delay_fire_tick, skate_move_delay_fire_time, times=1, mode=timer.CLOCK)
        else:
            self.delay_fire_tick()
        return

    def delay_fire_tick(self, *args):
        self._delay_fire_timer_id = None
        fire_rocker_ui = global_data.ui_mgr.get_ui('FireRockerUI')
        if fire_rocker_ui and fire_rocker_ui.is_rocker_enable:
            fire_rocker_ui.check_start_shot()
        fight_left_shot_ui = global_data.ui_mgr.get_ui('FightLeftShotUI')
        if fight_left_shot_ui and fight_left_shot_ui.is_rocker_enable:
            fight_left_shot_ui.check_start_shot()
        return

    def set_skate_anim_state(self, *args):
        self._skate_animator.SetFloat('dir_x', self._dir_x)
        self._skate_animator.SetFloat('dir_y', self._dir_y)

    def board_skate(self, *args):
        if not self._skate_animator:
            from common.animate import animator
            self._skate_animator = animator.Animator(self.skate_model, self.DEFAULT_XML, self.unit_obj)
            self._skate_animator.Load(False)
        self.set_skate_anim_state(*args)
        skate_model = self.skate_model
        model = self.ev_g_model()
        bind_point = 'skate'
        if model:
            skate_model.remove_from_parent()
            model.bind(bind_point, skate_model)
            offset = math3d.vector(0, -2 * SKATE_BOUNDING_BOX.y, 0)
            self.send_event('E_FEED_SFX_OFFSET', offset)
        self.send_event('E_BOARD_SKATE_FINISHED', self.skate_model)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CTRL_SKATE, ()], False)
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_SKATE)
        self.set_skate_action(animation_const.SKATE_ACTION_BOARD)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.update_player_pos, 0.1)
        else:
            self.regist_event('E_POSITION', self.update_player_pos)

    def _skate_model_load_callback(self, skate_model, *args):
        self._unload_res()
        if self.ev_g_get_state(self.sid):
            self._skate_model = skate_model
            self._create_skate_bind_collision()
            self.board_skate()
            self._init_skate_collision()
            self.init_ik()
            self.init_soft_bone()
            if self._skate_model and hasattr(self._skate_model, 'cast_shadow'):
                self._skate_model.cast_shadow = True
        else:
            skate_model.destroy()

    def _load_skate_model(self):
        building_conf = confmgr.get('c_building_res', str(self._table_id))
        if not building_conf:
            print('[error]c_building_res get id = ', self._table_id, ' c_building_res fail')
            return
        else:
            model_path = building_conf['ResPath']
            all_attachable = self.ev_g_all_attachable()
            if all_attachable and has_skin_ext():
                data = all_attachable.get(self._entity_id)
                if data:
                    from logic.gcommon.item.item_const import FASHION_POS_SUIT
                    fashion_id = data.get('fashion', {}).get(FASHION_POS_SUIT, None)
                    if fashion_id != None:
                        from logic.gutils import dress_utils
                        clothing_path = dress_utils.get_vehicle_res(fashion_id)
                        if clothing_path != None:
                            model_path = clothing_path
            self.ev_g_load_model(model_path, self._skate_model_load_callback)
            return

    def _do_board(self):
        self._load_skate_model()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SUCCESS_BOARD, (self._entity_id, self._table_id)], False)
        if not self.sd.ref_is_robot:
            com = self.unit_obj.add_com('ComSkateCam', 'client')
            if com:
                com.init_from_dict(self.unit_obj, {})
        self.send_event('E_BOARD_SKATE')
        if self._water_status != water_const.WATER_NONE:
            self.send_event('E_MOVE_TO_WATER_SURFACE')
        from logic.units.LAvatar import LAvatar
        if isinstance(self.unit_obj, LAvatar):
            if global_data.ui_mgr.get_ui('AttachableDriveUI'):
                global_data.ui_mgr.close_ui('AttachableDriveUI')
            global_data.ui_mgr.show_ui('AttachableDriveUI', 'logic.comsys.control_ui')
            if self._water_status != water_const.WATER_NONE or self.ev_g_is_in_water_area():
                self.need_update = True
            self._cur_pos = self.ev_g_position()
            self._last_effect_pos = self._cur_pos
            if self.ev_g_get_state(status_config.ST_RUN):
                self.send_event('E_DISABLE_STATE', status_config.ST_RUN)
                self.send_event('E_ACTIVE_STATE', status_config.ST_MOVE)

    def change_anim_move_dir(self, dir_x, dir_y, *args):
        if not self.ev_g_get_state(self.sid):
            return
        if not self.is_active:
            self._dir_x = dir_x
            self._dir_y = dir_y
            return
        if abs(dir_x) <= 0.01:
            dir_x = 0
        elif dir_x >= 0.99:
            dir_x = 1
        elif dir_x <= -0.99:
            dir_x = -1
        if abs(dir_y) <= 0.01:
            dir_y = 0
        elif dir_y >= 0.99:
            dir_y = 1
        elif dir_y <= -0.99:
            dir_y = -1
        self._set_move_dir(dir_x, dir_y)
        old_dir_x = self._dir_x
        old_dir_y = self._dir_y
        self._dir_x = dir_x
        self._dir_y = dir_y
        old_rock_yaw = math.atan2(old_dir_x, old_dir_y)
        old_rock_yaw = abs(old_rock_yaw)
        cur_rock_yaw = math.atan2(dir_x, dir_y)
        cur_rock_yaw = abs(cur_rock_yaw)
        is_change_speed = old_rock_yaw >= self.SKATE_ROCK_FAST_SPEED_MAX_YAW and cur_rock_yaw < self.SKATE_ROCK_FAST_SPEED_MAX_YAW or cur_rock_yaw >= self.SKATE_ROCK_FAST_SPEED_MAX_YAW and old_rock_yaw < self.SKATE_ROCK_FAST_SPEED_MAX_YAW
        if not is_change_speed:
            is_change_speed = old_rock_yaw >= self.SKATE_ROCK_MEDIUM_SPEED_MAX_YAW and cur_rock_yaw < self.SKATE_ROCK_MEDIUM_SPEED_MAX_YAW or cur_rock_yaw >= self.SKATE_ROCK_MEDIUM_SPEED_MAX_YAW and old_rock_yaw < self.SKATE_ROCK_MEDIUM_SPEED_MAX_YAW
        if is_change_speed:
            self.send_event('E_CHANGE_SPEED')
            self.send_event('E_SKATE_CHANGE_SPEED')

    def _set_move_dir(self, dir_x, dir_y):
        skate_state = self.get_skate_action()
        if self._skate_animator:
            self._skate_animator.SetFloat('dir_x', dir_x)
            self._skate_animator.SetFloat('dir_y', dir_y)
        if skate_state != animation_const.SKATE_ACTION_PREPARE_MOVE:
            move_dir = self.ev_g_eight_dir(dir_x, dir_y)
            if move_dir != 0:
                if not self.ev_g_is_jump():
                    self.send_event('E_SWITCH_STATUS', animation_const.STATE_SKATE)
                if skate_state in (animation_const.SKATE_ACTION_NONE, animation_const.SKATE_ACTION_BOARD, animation_const.SKATE_ACTION_BRAKE):
                    self._start_move_time = time.time()
                    self.set_skate_action(animation_const.SKATE_ACTION_PREPARE_MOVE)

    def exit(self, enter_states):
        super(Skate, self).exit(enter_states)
        self.send_event('E_SET_SKATE_BRAKING', False)
        self.send_event('E_CLEAR_UP_BODY_ANIM', part=LOWER_UP_BODY)
        self._unload_res()
        self.clear_timer()
        self.clear_soft_bone()

    def _cancel_skate_state(self, *args):
        self._end_leave()
        self.clear_timer()
        self.clear_soft_bone()

    def clear_timer(self):
        self.unit_obj.del_com('ComSkateCam')
        if self.ev_g_is_avatar():
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.update_player_pos)
            else:
                self.unregist_event('E_POSITION', self.update_player_pos)
            if global_data.ui_mgr.get_ui('AttachableDriveUI'):
                global_data.ui_mgr.close_ui('AttachableDriveUI')
        self.cancel_board_timer()

    def clear_soft_bone(self):
        if not self._soft_part_models:
            return
        for part_model in self._soft_part_models:
            if part_model and part_model.valid:
                part_model.get_spring_anim(True).clear_spring_anim()

        self._soft_part_models = []

    def update_player_pos(self, pos):
        character = self.sd.ref_character
        if not character:
            return
        rot = 0
        if not self.ev_g_is_jump():
            rot = character.getAndCalcBodySlope()
            self._cur_pos = pos
        if self._skate_animator:
            turn_full_body_node = self._skate_animator.find(TURN_X_FULL_BODY_NODE)
            if turn_full_body_node:
                degree = math.degrees(rot)
                MAX_DEGREE = 70
                if degree > MAX_DEGREE:
                    degree = MAX_DEGREE
                elif degree < -MAX_DEGREE:
                    degree = -MAX_DEGREE
                turn_full_body_node.twistAngle = degree

    def update(self, dt):
        if global_data.enable_skate_cross_window:
            self.check_before_window()
        last_anim_duration = self._anim_duration
        super(Skate, self).update(dt)
        self.play_skate_water_effect_tick(dt)
        self._anim_duration -= dt
        if last_anim_duration > 0 and self._anim_duration <= 0:
            if self._skate_state == animation_const.SKATE_ACTION_BOARD:
                self._end_board()
            elif self._skate_state == animation_const.SKATE_ACTION_PREPARE_MOVE:
                self._end_prepare_move()
            elif self._skate_state == animation_const.SKATE_ACTION_BRAKE:
                self._end_brake()
        rocker_dir = self.sd.ref_rocker_dir
        if self._skate_state == animation_const.SKATE_ACTION_MOVE and (not rocker_dir or rocker_dir.is_zero) and not self.ev_g_is_jump():
            self.send_event('E_ACTION_SKATE_MOVE_STOP')

    def on_rocker_stop(self):
        if self.ev_g_is_jump():
            return
        if self._skate_state == animation_const.SKATE_ACTION_PREPARE_MOVE or self._skate_state == animation_const.SKATE_ACTION_MOVE:
            self.send_event('E_ACTION_SKATE_MOVE_STOP')

    def _end_board(self, *args):
        skate_state = self.get_skate_action()
        if skate_state != animation_const.SKATE_ACTION_BOARD:
            return
        move_state = self.ev_g_move_state()
        if move_state == animation_const.MOVE_STATE_STAND:
            self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        else:
            self.set_skate_action(animation_const.SKATE_ACTION_PREPARE_MOVE)

    def _end_prepare_move(self, *args):
        skate_state = self.get_skate_action()
        if skate_state != animation_const.SKATE_ACTION_PREPARE_MOVE:
            return
        move_state = self.ev_g_move_state()
        if self.ev_g_get_state(status_config.ST_STAND):
            self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        else:
            self.set_skate_action(animation_const.SKATE_ACTION_MOVE)

    def _end_brake(self, *args):
        skate_state = self.get_skate_action()
        if self.ev_g_get_state(status_config.ST_SKATE_BRAKE):
            self.ev_g_cancel_state(status_config.ST_SKATE_BRAKE)
        if skate_state != animation_const.SKATE_ACTION_BRAKE:
            return
        self.send_event('E_MOVE_STOP', True)
        self.set_skate_action(animation_const.SKATE_ACTION_NONE)

    @property
    def skate_model(self):
        if self._skate_model:
            model = self._skate_model
            if model and model.valid:
                return model
        return None

    def play_skate_water_effect_tick(self, dt):
        if not self.need_update:
            return
        self._clock += dt
        if not self._cur_pos or not self._last_effect_pos:
            return
        if not self.ev_g_is_in_water_area():
            self.need_update = False
            return
        if (self._cur_pos - self._last_effect_pos).length >= self._water_effect_dist:
            self.play_skate_water_effect(self.WATER_EFFECT_PATH, self._water_effect_duration)
            self._clock = 0
        elif self._clock >= self._water_effect_interval:
            self.play_skate_water_effect(self.WATER_EFFECT_PATH, self._water_effect_interval - 0.05)
            self._clock = 0

    def play_skate_water_effect(self, res_path, duration=0.3):
        model = self.ev_g_model()
        if not model:
            return
        position = math3d.vector(model.world_position)
        if not position:
            return
        self._last_effect_pos = self._cur_pos
        water_height = global_data.player.logic.ev_g_cur_water_height()
        position.y = water_height
        self._play_skate_water_effect(res_path, position, duration)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_SKATE_WATER_EFFECT, (res_path, (position.x, position.y, position.z), duration)], False)

    def _play_skate_water_effect(self, res_path, position, duration=0.3):
        if type(position) in (tuple, list):
            position = math3d.vector(position[0], position[1], position[2])
        global_data.sfx_mgr.create_sfx_in_scene(res_path, position, duration=duration)

    def _leave_skate(self, *args):
        if not self.is_active:
            return
        self.cancel_board_timer()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_LEAVE_ATTACHABLE_ENTITY, ()], False)
        if not self.ev_g_is_in_any_state(self.DO_NOT_PLAY_SKATE_STATUS):
            self.send_event('E_SWITCH_STATUS', animation_const.STATE_SKATE)
        self._end_leave()
        self.unit_obj.del_com('ComSkateCam')
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.update_player_pos)
        else:
            self.unregist_event('E_POSITION', self.update_player_pos)
        self.send_event('E_FEED_SFX_OFFSET', math3d.vector(0, 0, 0))
        if not self.sd.ref_is_robot:
            global_data.ui_mgr.close_ui('AttachableDriveUI')

    def get_skate_action(self):
        return self._skate_state

    def set_skate_action(self, skate_state):
        if not self.is_active:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SET_SHAKE_ACTION, (skate_state,)], False)
        self.send_event('E_ON_AIM_SPEAD')
        old_skate_state = self._skate_state
        self._skate_state = skate_state
        if self.ev_g_is_jump():
            return
        clip_name = DEFAULT_ANIM_NAME
        action_key = ''
        time_scale = 1
        logic_time_scale = 1
        blend_time = 0.2
        if skate_state == animation_const.SKATE_ACTION_NONE:
            self._begin_skate_idle()
            if old_skate_state == animation_const.SKATE_ACTION_BRAKE:
                blend_time = 0
        elif skate_state == animation_const.SKATE_ACTION_BOARD:
            action_key = 'skate_board'
        elif skate_state == animation_const.SKATE_ACTION_PREPARE_MOVE:
            action_key = 'skate_prepare_move'
            blend_time = 0.2
        elif skate_state == animation_const.SKATE_ACTION_MOVE:
            self._begin_skate_move()
        elif skate_state == animation_const.SKATE_ACTION_BRAKE:
            action_key = 'skate_brake'
        elif skate_state == animation_const.SKATE_ACTION_LEAVE:
            action_key = 'skate_leave'
        elif skate_state == animation_const.SKATE_ACTION_TURN_LEFT:
            clip_name = 'skate_turn_l'
            self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, 1, blend_time=0.2, timeScale=1)
        elif skate_state == animation_const.SKATE_ACTION_TURN_RIGHT:
            clip_name = 'skate_turn_r'
            self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, 1, blend_time=0.2, timeScale=1)
        if old_skate_state != self._skate_state:
            if old_skate_state == animation_const.SKATE_ACTION_BRAKE:
                self.send_event('E_SET_SKATE_BRAKING', False)
            elif self._skate_state == animation_const.SKATE_ACTION_BRAKE:
                spd_key = move_utils.get_skate_move_speed_key(self)
                if spd_key:
                    max_speed = getattr(speed_physic_arg, spd_key)
                    brake_duration = abs(max_speed / speed_physic_arg.skate_stop)
                else:
                    brake_duration = 1.0
                self.send_event('E_SET_SKATE_BRAKING', True, brake_duration)
        if action_key:
            clip_list = self.ev_g_weapon_action_list(action_key)
            dir_type = 1
            loop = False
            if len(clip_list) > 1:
                dir_type = len(clip_list)
                loop = True
                clip_name = clip_list[0][:-3]
            else:
                clip_name = clip_list[0]
                self._anim_duration = self.ev_g_get_anim_length(clip_name) * logic_time_scale
                if skate_state == animation_const.SKATE_ACTION_BRAKE:
                    time_scale = self._anim_duration / BRAKE_TIME
                    self._anim_duration = BRAKE_TIME
            self.send_event('E_POST_ACTION', clip_name, LOW_BODY, dir_type, loop=loop, blend_time=blend_time, timeScale=time_scale)
            if skate_state in (animation_const.SKATE_ACTION_BRAKE, animation_const.SKATE_ACTION_PREPARE_MOVE):
                self.send_event('E_SET_SMOOTH_SPEED', LOW_BODY_SELECT, 0.4)
            role_id = self.ev_g_role_id()
            postfix_id = ROLE_ID_POSTFIX.get(role_id, 0)
            self.send_event('E_POST_BIND_OBJ_ACTION', BIND_OBJ_TYPE_SKATE, clip_name, dir_type, loop=loop, blend_time=blend_time, timeScale=time_scale, postfix_id=postfix_id)

    def _move_stop(self):
        if not self.is_active:
            return
        skate_state = self.get_skate_action()
        cur_speed = self.sd.ref_cur_speed
        move_pass_time = time.time() - self._start_move_time
        if skate_state == animation_const.SKATE_ACTION_MOVE and move_pass_time >= self.min_trigger_brake_move_duration and cur_speed > 0:
            self.set_skate_action(animation_const.SKATE_ACTION_BRAKE)
            self.ev_g_status_try_trans(status_config.ST_SKATE_BRAKE)
            self.send_event('E_UPDATE_STATUS_TIME', status_config.ST_SKATE_BRAKE)
        else:
            if skate_state == animation_const.SKATE_ACTION_MOVE:
                self.set_skate_action(animation_const.SKATE_ACTION_NONE)
            self.send_event('E_MOVE_STATE', animation_const.MOVE_STATE_STAND)
            self.send_event('E_MOVE_STOP', True)

    def _on_ground_finish(self):
        self.send_event('E_SWITCH_STATUS', animation_const.STATE_SKATE)
        move_state = self.ev_g_move_state()
        rocker_dir = self.sd.ref_rocker_dir
        if rocker_dir and not rocker_dir.is_zero and self.ev_g_status_check_pass(self.status_config.ST_SKATE_MOVE):
            self.set_skate_action(animation_const.SKATE_ACTION_MOVE)
        else:
            skate_state = self.get_skate_action()
            move_dir = self.ev_g_get_walk_direction()
            move_pass_time = time.time() - self._start_move_time
            if skate_state == animation_const.SKATE_ACTION_MOVE and move_pass_time >= self.min_trigger_brake_move_duration and move_dir and not move_dir.is_zero:
                self.set_skate_action(animation_const.SKATE_ACTION_BRAKE)
                self.ev_g_status_try_trans(status_config.ST_SKATE_BRAKE)
                self.send_event('E_UPDATE_STATUS_TIME', status_config.ST_SKATE_BRAKE)
            else:
                self.set_skate_action(animation_const.SKATE_ACTION_NONE)

    def _end_leave(self, *args):
        skate_model = self.skate_model
        self.send_event('E_LEAVE_SKATE')
        self.ev_g_cancel_state(self.sid)
        model_position = self.ev_g_model_position()
        chect_begin = model_position
        check_end = chect_begin + math3d.vector(0, -50, 0)
        self._start_move_time = 0
        scene = world.get_active_scene()
        result = scene.scene_col.hit_by_ray(chect_begin, check_end, 0, -1, collision_const.TERRAIN_GROUP | collision_const.WOOD_GROUP | collision_const.STONE_GROUP, collision.EQUAL_FILTER, False)
        skate_position = model_position
        if result[0]:
            cobj = result[5]
            if skate_model:
                bounding_box = math3d.vector(0, 0, 0)
                if skate_model:
                    bounding_box = SKATE_BOUNDING_BOX
                skate_position = result[1]
                skate_position.y += bounding_box.y
        if self._water_status != water_const.WATER_DEEP_LEVEL:
            self.send_event('E_RESET_GRAVITY')
        self.send_event('E_TRY_DETACH', self._entity_id, (skate_position.x, skate_position.y, skate_position.z))
        self._entity_id = 0
        model = self.ev_g_model()
        if self.skate_model and model:
            model.unbind(self.skate_model)
        self._unload_res()
        if not self.ev_g_is_in_any_state(self.DO_NOT_PLAY_SKATE_STATUS):
            if self.ev_g_status_check_pass(self.status_config.ST_STAND) and not self.ev_g_defeated():
                self.send_event('E_CTRL_STAND')
        self.set_skate_action(animation_const.SKATE_ACTION_NONE)
        width = collision_const.CHARACTER_STAND_WIDTH
        height = collision_const.CHARACTER_STAND_HEIGHT
        self.send_event('E_RESIZE_DRIVER_CHARACTER', width, height)
        self.send_event('E_MOVE_STOP', True)
        self.need_update = False
        self.send_event('E_LEAVE_SKATE_FINISH')

    def cancel_board_timer(self):
        if self._board_timer:
            global_data.game_mgr.unregister_logic_timer(self._board_timer)
            self._board_timer = None
        return

    def _destroy_collision(self):
        if self._col_obj:
            skate_model = self.skate_model
            if skate_model:
                skate_model.unbind_col_obj(self._col_obj)
            global_data.emgr.scene_remove_common_shoot_obj.emit(self._col_obj.cid)
            scene = world.get_active_scene()
            if scene:
                scene.scene_col.remove_object(self._col_obj)
            self._col_obj = None
        return

    def _unload_res(self):
        if self._skate_animator:
            self._skate_animator.destroy()
            self._skate_animator = None
        self._destroy_collision()
        skate_model = self.skate_model
        if self._ik_mgr:
            human_model = self.ev_g_model()
            if human_model:
                self._ik_mgr.enabled = False
                self._left_foot_ik.set_target(None)
                self._right_foot_ik.set_target(None)
        if skate_model:
            skate_model.destroy()
            skate_model = None
        return
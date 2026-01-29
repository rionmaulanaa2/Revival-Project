# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/robot_animation_const.py
from __future__ import absolute_import
_reload_all = True
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_const.animation_const import FRAMES_PER_SECOND, SECONDS_PER_FRAME, ENABLE_FULL_BODY_BONE, ENABLE_UP_BODY_BONE
from logic.gcommon.common_const.animation_const import TURN_X_UP_BODY_NODE_NAME, TURN_Y_UP_BODY_NOD_NAME
from ..cdata import mecha_status_config
BONE_HEAD_NAME = 'biped head'
BONE_SPINE_NAME = 'biped spine'
BONE_RIGHT_HAND_NAME = 'biped r hand'
BONE_LEFT_HAND_NAME = 'biped l hand'
BONE_RIGHT_FOOT_NAME = 'biped r foot'
BONE_LEFT_FOOT_NAME = 'biped l foot'
BONE_LEFT_CLAVIS = 'biped l clavicle'
BONE_RIGHT_CLAVIS = 'biped r clavicle'
BONE_BIPED_NAME = 'biped'
BONE_SWORD_NAME = 'biped_bone18'
DELAY_KEEP_WALK_TIME = animation_const.DELAY_KEEP_WALK_TIME
DEFAULT_XML = 'animator_conf/robot.xml'
STATE_STAND = 1
STATE_JUMP = 2
STATE_DIE = 3
STATE_RUSH = 4
STATE_BOARDING = 5
STATE_LEAVING = 6
STATE_TRANSFORM_TO_MECHA = 7
STATE_TRANSFORM_TO_VEHICLE = 8
STATE_VEHICLE_STAND = 9
STATE_DASH = 10
STATE_SWORD_CORE = 11
STATE_EXECUTE = 12
STATE_IMMOBILIZED = 13
STATE_HOVER = 14
STATE_TRANSIT_MIN = 100
MOVE_STATE_WALK = animation_const.MOVE_STATE_WALK
MOVE_STATE_RUN = animation_const.MOVE_STATE_RUN
MOVE_STATE_STAND = animation_const.MOVE_STATE_STAND
MOVE_STATE_TURN_LEFT = animation_const.MOVE_STATE_TURN_LEFT
MOVE_STATE_TURN_RIGHT = animation_const.MOVE_STATE_TURN_RIGHT
MOVE_STATE_TURN_AROUND = 5
HAND_STATE_NONE = 0
HAND_STATE_ADD_BULLET = 1
HAND_STATE_MAIN_FIRE = 2
HAND_STATE_SECOND_FIRE = 3
HAND_STATE_MELEE = 4
HAND_STATE_SHOOT_IDLE = 5
HAND_STATE_HEAVY_MELEE = 6
HAND_STATE_PREPARE_THROW_BOMB = 7
HAND_STATE_READY_FOR_THROW_BOMB = 8
HAND_STATE_THROW_BOMB = 9
HAND_STATE_THROW_BOMB_FINISH = 10
HAND_STATE_HITED = 16
JUMP_STATE_UP = 0
JUMP_STATE_IN_AIR = 1
JUMP_STATE_FALL_GROUND = 2
JUMP_STATE_UP_2 = 3
RUSH_STATE_PREPARE = 0
RUSH_STATE_MOVE = 1
RUSH_STATE_STOP = 2
MOVE_STAGE_START = 0
MOVE_STAGE_STABLE = 1
MOVE_STAGE_BRAKE = 2
STOP_STAGE_STATIC = 0
STOP_STAGE_BRAKE = 1
TURN_X_UP_BODY_NODE_DICT = {STATE_STAND: TURN_X_UP_BODY_NODE_NAME,STATE_JUMP: TURN_X_UP_BODY_NODE_NAME,STATE_HOVER: TURN_X_UP_BODY_NODE_NAME}
TURN_Y_UP_BODY_NODE_DICT = {STATE_STAND: TURN_Y_UP_BODY_NOD_NAME,STATE_JUMP: TURN_Y_UP_BODY_NOD_NAME}
TURN_BODY_NODES = (
 TURN_Y_UP_BODY_NOD_NAME, TURN_X_UP_BODY_NODE_NAME)
BEGIN_JUMP_UP_EVENT = 'begin_jump_up'
END_JUMP_UP_EVENT = 'end_jump_up'
BEGIN_FALL_GROUND_EVENT = 'begin_fall_ground'
END_FALL_GROUND_EVENT = 'end_fall_ground'
BEGIN_FIRE_EVENT = 'begin_fire'
BEGIN_ROCKET_EVENT = 'begin_rocket'
END_ROCKET_EVENT = 'end_rocket'
BEGIN_ADD_BULLET_EVENT = 'begin_add_bullet'
END_ADD_BULLET_EVENT = 'end_add_bullet'
MAIN_WEAPON_ATTACK_END = 'main_weapon_attack_end'
BEGIN_MOVE_START_EVENT = 'begin_move_start'
BEGIN_MOVE_STOP_EVENT = 'begin_move_stop'
END_RUSH_PREPARE_EVENT = 'end_rush_prepare'
BEGIN_RUSH_MOVE_EVENT = 'begin_rush_move'
END_RUSH_MOVE_EVENT = 'end_rush_move'
DEACTIVE_RUSH_MOVE_EVENT = 'deactive_rush_move'
END_RUSH_STOP_EVENT = 'end_rush_stop'
END_DASH = 'end_dash'
END_HITED_EVENT = 'end_hited'
END_DIE_EVENT = 'end_die'
END_MOVE_EVENT = 'end_move'
END_TURN_EVENT = 'end_turn'
END_MOVE_START_EVENT = 'end_move_start'
END_TURN_AROUND_EVENT = 'end_turn_around'
END_ENTER_MECHA_EVENT = 'end_enter_mecha'
END_LEAVE_MECHA_EVENT = 'end_leave_mecha'
SWORD_PREPARE_BEGIN = 'prepare_begin'
SWORD_PREPARE_EXIT = 'prepare_exit'
SWORD_PREPARE_END = 'prepare_end'
SWORD_FIRE_BEGIN = 'begin_sword_energy'
SWORD_FIRE_EXIT = 'exit_sword_energy'
SWORD_FIRE_END = 'end_sword_energy'
SWORD_POST_EIXT = 'exit_post'
THROW_OUT_EIXT = 'end_throw_out'
END_THROW = 'end_throw'
SWORD_CORE_END = 'end_sword_core'
END_TRANSFORM_TO_MECHA_EVENT = 'end_transform_to_mecha'
END_TRANSFORM_TO_VEHICLE_EVENT = 'end_transform_to_vehicle'
BEGIN_EXECUTE = 'begin_excute'
END_EXECUTE = 'end_excute'
EXIT_ATTACK_EVENT = 'exit_attack'
END_ATTACK_EVENT = 'end_attack'
EXIT_HEAVY_ATTACK_EVENT = 'exit_heavy_attack'
END_HEAVY_ATTACK_EVENT = 'end_heavy_attack'
OX_DASH_HIT_EXIT = 'dash_hit_exit'
OX_DASH_MISS_EXIT = 'dash_miss_exit'
OX_DASH_DEACTIVE = 'dash_deactive'
STAND_NODE_NAME = 'stand'
DIE_NODE_NAME = 'die'
JUMP_ROOT_NODE_NAME = 'jump.full_body'
RUSH_NODE_NAME = 'rush'
ATTACK_NODE_NAME = 'attack'
HEAVY_ATTACK_NODE_NAME = 'heavy_attack'
JUMP_UP_NODE_NAME = 'jump_on_up'
JUMP_IN_AIR_NODE_NAME = 'jump_in_air'
JUMP_FALL_GROUND_NODE_NAME = 'jump_fall_ground'
STABLE_MOVE_NODE_NAME = 'stand.walk'
STABLE_RUN_NODE_NAME = 'stand.run'
SHOOT_MOVE_NODE_NAME = 'stand.move.shoot'
ADD_BULLET_ROOT_NODE_NAME = 'add_bullet'
FIRE_ROOT_NODE_NAME = 'fire'
MAIN_FIRE_ROOT_NODE_NAME = 'main_weapon_fire'
SHOOT_IDLE_ROOT_NODE_NAME = 'shoot_idle'
TURN_AROUND_NODE_NAME = 'turn_around'
DASH_NODE_NAME = 'dash'
LEFT_WEAPON_TRIGGER = 'action_gun_l'
RIGHT_WEAPON_TRIGGER = 'action_gun'
MOVE_FRONT_SUFFIX_SET = {
 '_f', 'fl', 'fr'}
MOVE_BACK_SUFFIX_SET = {'_b', 'bl', 'br'}
MOVE_CLIP_DICT = {animation_const.SOUND_TYPE_WALK: {'common': {
                                              'move_fl', 'move_fr', 'move_f', 'move_bl', 'move_br', 'move_b', 'turnleft_90', 'turnright_90'},
                                     '8002': {
                                            'move_start', 'move_start_f', 'move_start_fr', 'move_start_fl', 'move_start_b', 'move_start_br', 'move_start_bl',
                                            'sword_aim_move_f', 'sword_aim_move_fr', 'sword_aim_move_fl'},
                                     '8004': {
                                            'move_walk_fl', 'move_walk_fr', 'move_walk_f', 'move_walk_bl', 'move_walk_br', 'move_walk_b'},
                                     '8005': {
                                            'shockwave_move_f', 'shockwave_move_fr', 'shockwave_move_fl',
                                            'shockwave_move_b', 'shockwave_move_bl', 'shockwave_move_br'},
                                     '8017': {
                                            'aim_bl', 'aim_br', 'aim_l', 'aim_r', 'aim_fl', 'aim_fr', 'aim_b_l', 'aim_b_r', 'aim_f_l', 'aim_f_r', 'aim_l2r', 'aim_r2l'},
                                     '8019': {
                                            'shd_move_b', 'shd_move_bl', 'shd_move_br', 'shd_move_f', 'shd_move_fl', 'shd_move_fr'},
                                     '8020': {
                                            'ball_move_b', 'ball_move_bl', 'ball_move_br', 'ball_move_f', 'ball_move_fl', 'ball_move_fr'},
                                     '8021': {
                                            'move_l', 'move_r', 'move_s02_f', 'move_s02_fl', 'move_s02_fr', 'move_s02_b', 'move_s02_bl', 'move_s02_br',
                                            'move_s02_l', 'move_s02_r'},
                                     '8023': {
                                            'akimbo_move_b', 'akimbo_move_bl', 'akimbo_move_br', 'akimbo_move_f', 'akimbo_move_fl', 'akimbo_move_fr',
                                            'snipe_aim_b', 'snipe_aim_bl', 'snipe_aim_br', 'snipe_aim_f', 'snipe_aim_fl', 'snipe_aim_fr',
                                            'akimbo_turnleft_90', 'akimbo_turnright_90', 'snipe_turnleft_90', 'snipe_turnright_90'},
                                     '8024': {
                                            'c4_loop_b', 'c4_loop_f', 'c4_loop_br', 'c4_loop_bl', 'c4_loop_fl', 'c4_loop_fr'},
                                     '8026': {
                                            'turnleft_90', 'turnright_90'},
                                     '8028': {
                                            'rabt_run', 'rabt_run_b', 'rabt_run_bl', 'rabt_run_br', 'rabt_run_f', 'rabt_run_fl', 'rabt_run_fr'},
                                     '8029': {
                                            'rifle_aim_b', 'rifle_aim_br', 'rifle_aim_bl', 'rifle_aim_f', 'rifle_aim_fr', 'rifle_aim_fl', 'shotgun_aim_bl',
                                            'shotgun_aim_b', 'shotgun_aim_br', 'shotgun_aim_f', 'shotgun_aim_fl', 'shotgun_aim_fr'},
                                     '8034': {
                                            'dash_move_b', 'dash_move_bl', 'dash_move_br', 'dash_move_f', 'dash_move_fl', 'dash_move_fr'},
                                     '8035': {
                                            'run_stop'}
                                     },
   animation_const.SOUND_TYPE_RUN: {'common': {
                                             'run', 'run_f', 'run_fl', 'run_fr', 'run_b', 'run_bl', 'run_br'},
                                    '8002': {
                                           'sword_core_run'},
                                    '8003': {
                                           'run_s03'},
                                    '8004': {
                                           'run_01'},
                                    '8011': {
                                           'q_run'},
                                    '8014': {
                                           'sword_run_f'},
                                    '8017': {
                                           'run_stop'},
                                    '8019': {
                                           'shd_run'},
                                    '8020': {
                                           'run_s02'},
                                    '8021': {
                                           'dash_move_b', 'dash_move_bl', 'dash_move_br', 'dash_move_f',
                                           'dash_move_fl', 'dash_move_fr', 'dash_move_r', 'dash_move_l'},
                                    '8023': {
                                           'akimbo_run', 'snipe_run'},
                                    '8029': {
                                           'shotgun_run'},
                                    '8032': {
                                           'charge_f', 'charge_fr', 'charge_fl'},
                                    '8036': {
                                           'move_vice_f', 'move_vice_fr', 'move_vice_fl', 'move_vice_br', 'move_vice_bl', 'move_vice_b'}
                                    }
   }
MOVE_NODE_LIST = ('stand.prepare.move', 'stand.shoot.move')
sound_name_map = {animation_const.SOUND_TYPE_WALK: 'walk',
   animation_const.SOUND_TYPE_RUN: 'run'
   }
RUN_NODES = {animation_const.SOUND_TYPE_WALK: ('stand.walk.empty_hand', 'stand.walk.have_gun'),
   animation_const.SOUND_TYPE_RUN: ('stand.run_forward.have_gun.single', 'stand.run_forward.have_gun.double')
   }
SHOOT_CLIPS = ((7, 'robot_rifle_shoot'), )
MELEE_CLIPS = ('sword_attack_01', 'sword_attack_02', 'sword_attack_03', 'sword_attack_04')
HEAVY_MELEE_CLIP = 'heavy_cut'
MELEE_CUT_RUSH_CLIP = 'cut_rush'
DYNAMIC_MASK_BONE_CLIP = {'robot_rocket': ({'param': {'move_action': MOVE_STATE_STAND},'subtree': ENABLE_FULL_BODY_BONE}, {'param': {'move_action': (MOVE_STATE_WALK, MOVE_STATE_RUN)},'subtree': ENABLE_UP_BODY_BONE})}
ANIM_STATE_TO_LOGIC_STATE = {STATE_STAND: mecha_status_config.MC_STAND,
   STATE_DIE: mecha_status_config.MC_STAND
   }
THROW_SRC_NODE_CLIPNAMES = {STATE_STAND: {'pull_ring': 'throw_01',
                 'continue_bomb': 'throw_02',
                 'throw_out': 'throw_03',
                 'throw_finish': 'throw_04'
                 },
   STATE_HOVER: {'pull_ring': 'air_throw_01',
                 'continue_bomb': 'air_throw_02',
                 'throw_out': 'air_throw_03',
                 'throw_finish': 'air_throw_04'
                 }
   }
SEVEN_DIR_SHOOT_CLIPS = [
 'shoot_bl', 'shoot_fl', 'shoot_b', 'shoot_o', 'shoot_f', 'shoot_br', 'shoot_fr']
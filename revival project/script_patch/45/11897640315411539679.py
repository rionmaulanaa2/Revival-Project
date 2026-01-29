# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/animation_const.py
from __future__ import absolute_import
_reload_all = True
from logic.gcommon.const import NEOX_UNIT_SCALE
from ..cdata import state_physic_arg, status_config
from logic.gcommon.const import SEX_MALE, SEX_FEMALE
SWIM_USE_MILA_ANI_IDS = [
 15, 98]
ROLE_ID_MI_LA = 15
TEST_JUMP_ANIM = True
STAND_REPLACE_PREFIX = 's_'
CROUCH_REPLACE_PREFIX = 'c_'
IDLE_RELATE_PARAMS = tuple(set(['low_body_action', 'weapon_type', 'is_shoot', 'move_action']))
MOVE_RELATE_PARAMS = tuple(set(['weapon_type']))
USE_ITEM_RELATE_PARAMS = tuple(set(['low_body_action']))
JUMP_RELATE_PARAMS = tuple(set(['weapon_type']))
WEAPON_RELATE_PARAMS = tuple(set(['move_action']))
SOURCE_NODE_TYPE = 'Source'
BLEND_NODE_TYPE = 'Blend'
SELECT_NODE_TYPE = 'Select'
DUMMY_NODE_TYPE = 'Dummy'
RUSH_TRIGGER_NAME = set(['step1'])
EIGHT_DIR_ORIGIN = 0
EIGHT_DIR_RIGHT = 1
EIGHT_DIR_UP_RIGHT = 2
EIGHT_DIR_UP_ = 3
EIGHT_DIR_UP_LEFT = 4
EIGHT_DIR_LEFT = 5
EIGHT_DIR_BOTTOM_LEFT = 6
EIGHT_DIR_BOTTOM = 7
EIGHT_DIR_BOTTOM_RIGHT = 8
IS_NEW_MODEL = True
DEFAULT_SEX = SEX_FEMALE
FRAMES_PER_SECOND = 30.0
SECONDS_PER_FRAME = 1.0 / 30.0
DELAY_KEEP_WALK_TIME = 0.3
DEFAULT_XML = 'animator_conf/hero.xml'
STATE_GENERAL_LOW_BODY = 1
STATE_STAND = 2
STATE_SQUAT = 3
STATE_CRAWL = 4
STATE_JUMP = 5
STATE_DIE = 6
STATE_PARACHUTE = 7
STATE_DOWN = 8
STATE_DRIVE = 9
STATE_PASSENGER = 10
STATE_SQUAT_HELP = 11
STATE_SWIM = 12
STATE_CLIMB = 13
STATE_SKATE = 14
STATE_ROLL = 15
STATE_ENTER_MECHA = 16
STATE_RUSH = 17
STATE_BLEND_SPACE = 18
STATE_TEST_STATE = 99
STATE_DESC = {STATE_GENERAL_LOW_BODY: 'STATE_GENERAL_LOW_BODY',
   STATE_STAND: 'STATE_STAND',
   STATE_SQUAT: 'STATE_SQUAT',
   STATE_JUMP: 'STATE_JUMP',
   STATE_DIE: 'STATE_DIE',
   STATE_PARACHUTE: 'STATE_PARACHUTE',
   STATE_DOWN: 'STATE_DOWN',
   STATE_DRIVE: 'STATE_DRIVE',
   STATE_PASSENGER: 'STATE_PASSENGER',
   STATE_SQUAT_HELP: 'STATE_SQUAT_HELP',
   STATE_SWIM: 'STATE_SWIM',
   STATE_CLIMB: 'STATE_CLIMB',
   STATE_SKATE: 'STATE_SKATE',
   STATE_ROLL: 'STATE_ROLL',
   STATE_ENTER_MECHA: 'STATE_ENTER_MECHA',
   STATE_RUSH: 'STATE_RUSH'
   }
ARMOR_STATE_CLOSE = 0
ARMOR_STATE_UNWIND = 1
ARMOR_STATE_ALREADY_OPEN = 2
STATE_TRANSIT_MIN = 100
STATE_CRAWL_TO_STAND = 103
STATE_SQUAT_TO_CRAWL = 104
STATE_STAND_TO_CRAWL = 105
STATE_STAND_TO_DOWN = 106
STATE_DOWN_TO_STAND = 107
HELP_STAND_TO_SQUAT = 108
TRANSIT_STATUS_TO_FINAL_STATUS = {STATE_CRAWL_TO_STAND: STATE_STAND,
   STATE_SQUAT_TO_CRAWL: STATE_CRAWL,
   STATE_STAND_TO_CRAWL: STATE_CRAWL,
   STATE_STAND_TO_DOWN: STATE_DOWN,
   STATE_DOWN_TO_STAND: STATE_STAND
   }
ANIM_STATE_TO_LOGIC_STATE = {STATE_STAND: status_config.ST_STAND,
   STATE_SQUAT: status_config.ST_CROUCH,
   STATE_DOWN: status_config.ST_DOWN,
   STATE_STAND_TO_DOWN: status_config.ST_DOWN,
   STATE_PARACHUTE: status_config.ST_PARACHUTE,
   STATE_SQUAT_HELP: status_config.ST_HELP,
   STATE_SWIM: status_config.ST_SWIM,
   STATE_CLIMB: status_config.ST_CLIMB,
   STATE_ROLL: status_config.ST_ROLL,
   STATE_ENTER_MECHA: status_config.ST_MECHA_BOARDING,
   STATE_RUSH: status_config.ST_RUSH,
   STATE_DOWN_TO_STAND: status_config.ST_DOWN_TRANSMIT_STAND,
   STATE_DIE: status_config.ST_DEAD,
   STATE_DRIVE: status_config.ST_MECHA_DRIVER
   }
ROLL_LEFT = 0
ROLL_RIGHT = 1
ROLL_FRONT = 2
ROLL_BACK = 3
MOVE_STATE_WALK = 0
MOVE_STATE_RUN = 1
MOVE_STATE_STAND = 2
MOVE_STATE_TURN_LEFT = 3
MOVE_STATE_TURN_RIGHT = 4
MOVE_STATE_CELEBRATE = 5
RUN_FIRST_STAGE = 0
RUN_SECOND_STAGE = 1
RUN_THIRD_STAGE = 2
STOP_STAGE_STATIC = 0
STOP_STAGE_BRAKE = 1
SWIM_ACTION_IDLE = 0
SWIM_ACTION_DIRECT_FRONT = 1
SWIM_ACTION_BACK_2_FRONT = 2
SWIM_ACTION_STAND_2_FRONT = 3
SWIM_ACTION_DIRECT_BACK = 4
SWIM_ACTION_FRONT_2_BACK = 5
SWIM_ACTION_STAND_2_BACK = 6
SWIM_ACTION_HORIZON = 7
SWIM_EVENT_IDLE = 0
SWIM_EVENT_MOVE_FRONT = 1
SWIM_EVENT_MOVE_BACK = 2
WALK_ON_WATER_EVENT_MOVE = 3
SKATE_ACTION_NONE = 0
SKATE_ACTION_BOARD = 1
SKATE_ACTION_PREPARE_MOVE = 2
SKATE_ACTION_MOVE = 3
SKATE_ACTION_BRAKE = 4
SKATE_ACTION_JUMP = 5
SKATE_ACTION_LEAVE = 6
SKATE_ACTION_TURN_LEFT = 7
SKATE_ACTION_TURN_RIGHT = 8
PICK_POSITION_LOW = 0
PICK_POSITION_HIGH = 1
WEAPON_POS_LEFT = 1
WEAPON_POS_RIGHT = 2
PUT_ON_LEFT_POS_GUN = 1
PUT_OFF_LEFT_POS_GUN = 2
PUT_ON_RIGHT_POS_GUN = 3
PUT_OFF_RIGHT_POS_GUN = 4
HAND_STATE_NONE = 0
STATE_GENERAL_UP_BODY = 1
HAND_STATE_GET_NEW_GUN = 2
HAND_STATE_ADD_BULLET = 3
HAND_STATE_FIRE = 4
HAND_STATE_PREPARE_THROW_BOMB = 7
HAND_STATE_READY_FOR_THROW_BOMB = 8
HAND_STATE_THROW_BOMB = 9
HAND_STATE_PUNCH = 10
HAND_STATE_USE_ITEM = 11
HAND_STATE_LOAD = 12
HAND_STATE_PICK = 13
HAND_STATE_CURE = 14
HAND_STATE_FIST_IDLE = 15
HAND_STATE_HITED = 16
HAND_STATE_SWITCH_GUN_MODE = 18
HAND_STATE_USE_BANDAGE = 19
HAND_STATE_TEST_SINGLE = 97
HAND_STATE_TEST_ADD = 98
HAND_STATE_TEST_FULL_BODY = 99
RELOAD_TYPE_ALL = 1
RELOAD_TYPE_ONE_FIRST = 2
RELOAD_TYPE_ONE_NEXT = 3
GUN_LOAD_BY_LEFT_HAND = 0
GUN_LOAD_BY_RIGHT_HAND = 1
WEAPON_TYPE_EMPTY_HAND = 0
WEAPON_TYPE_SHOTGUN = 1
WEAPON_TYPE_SHIELD = 2
WEAPON_TYPE_FLAMER = 3
WEAPON_TYPE_SNIPER_RIFLE = 4
WEAPON_TYPE_GRENADE = 5
WEAPON_TYPE_BAZOOKA = 6
WEAPON_TYPE_M249 = 7
WEAPON_TYPE_DOUBLE = 8
WEAPON_TYPE_FRIED_PIG = 9
WEAPON_TYPE_NORMAL = 10
WEAPON_TYPE_SHRAPNEL = 11
WEAPON_TYPE_PULSE = 12
WEAPON_TYPE_FROZEN = 13
WEAPON_TYPE_HYDRA_MISSILE = 14
WEAPON_TYPE_LMG = 15
WEAPON_TYPE_BLAST = 16
WEAPON_TYPE_M4 = 17
WEAPON_TYPE_MP5 = 18
WEAPON_TYPE_DJFD = 22
WEAPON_TYPE_SHIELD_RIFLE = 23
WEAPON_ROTATE_TYPE_LIST = [
 WEAPON_TYPE_FLAMER, WEAPON_TYPE_BAZOOKA, WEAPON_TYPE_SHRAPNEL]
WEAPON_LOAD_FROM_IDLE = 0
WEAPON_LOAD_FROM_ADD_BULLET = 1
JUMP_STATE_UP = 0
JUMP_STATE_IN_AIR = 1
JUMP_STATE_FALL_GROUND = 2
FALL_ON_GROUND_LOW_SPEED = 0
FALL_ON_GROUND_MEDIUM_SPEED = 1
FALL_ON_GROUND_HIGH_SPEED = 2
PARACHUTE_STATE_CLOSE = 0
PARACHUTE_STATE_OPENING = 1
PARACHUTE_STATE_FINISH_OPEN = 2
PARACHUTE_STATE_ON_GROUND = 3
PARACHUTE_STATE_NONE = 4
CLIMB_STATE_NONE = 0
CLIMB_STATE_CLIMB_UP = 1
CLIMB_STATE_JUMP_DOWN = 10
CLIMB_STATE_STAND_BARRIER = 11
CLIMB_STATE_ON_GROUND = 20
PICK_TYPE_NONE = 0
PICK_TYPE_STAND_EMPTY_LOW = 1
PICK_TYPE_STAND_HAVE_GUN_LOW = 2
PICK_TYPE_STAND_EMPTY_HIGH = 3
PICK_TYPE_STAND_HAVE_GUN_HIGH = 4
PICK_TYPE_STAND_MOVE_EMPTY = 5
PICK_TYPE_STAND_MOVE_HAVE_GUN = 6
PICK_TYPE_SQUAT_EMPTY = 7
PICK_TYPE_SQUAT_HAVE_GUN = 8
PICK_TYPE_HAVE_GUN_LIST = [
 PICK_TYPE_STAND_HAVE_GUN_LOW, PICK_TYPE_STAND_HAVE_GUN_HIGH, PICK_TYPE_STAND_MOVE_HAVE_GUN, PICK_TYPE_SQUAT_HAVE_GUN]
BEGIN_JUMP_UP_EVENT = 'begin_jump_up'
END_JUMP_UP_EVENT = 'end_jump_up'
BEGIN_JUMP_IN_AIR_EVENT = 'begin_jump_in_air'
BEGIN_FALL_GROUND_EVENT = 'begin_fall_ground'
END_FALL_GROUND_EVENT = 'end_fall_ground'
BEGIN_FIRE_EVENT = 'begin_fire'
BEGIN_ADD_BULLET_EVENT = 'begin_add_bullet'
END_ADD_BULLET_EVENT = 'end_add_bullet'
ROOT_BEGIN_GET_NEW_WEAPON_EVENT = 'root_begin_get_new_weapon'
BEGIN_GET_NEW_WEAPON_EVENT = 'begin_get_new_weapon'
END_GET_NEW_WEAPON_EVENT = 'end_get_new_weapon'
BEGIN_SWITCH_GUN_MODE_EVENT = 'begin_switch_gun_mode'
END_SWITCH_GUN_MODE_EVENT = 'end_switch_gun_mode'
BEGIN_PULL_RING_EVENT = 'begin_pull_ring'
END_PULL_RING_EVENT = 'end_pull_ring'
BEGIN_THROW_OUT_EVENT = 'begin_throw_out'
END_THROW_BOMB_EVENT = 'end_throw_bomb'
BEGIN_GUN_LOAD_EVENT = 'begin_load'
BEGIN_USE_ITEM_EVENT = 'begin_use_item'
BEGIN_PUNCH_EVENT = 'begin_punch'
END_FIST_IDLE_EVENT = 'end_fist_idle'
END_HITED_EVENT = 'end_hited'
END_TURN_EVENT = 'end_turn'
BEGIN_PICK_EVENT = 'begin_pick'
END_PICK_EVENT = 'end_pick'
END_LOAD_EVENT = 'end_load'
END_PARACHUTE_EVENT = 'end_parachute'
END_DIE_EVENT = 'end_die'
END_STAND_TO_HELP_EVENT = 'end_stand_to_help'
END_OPEN_PARACHUTE_EVENT = 'end_open_parachute'
END_PARACHUTE_ON_GROUND_EVENT = 'end_parachute_on_ground'
END_PARACHUTE_LEAVE_EVENT = 'end_parachute_leave'
BEGIN_CRAWL_TO_STAND_EVENT = 'begin_crawl_to_stand'
END_CRAWL_TO_STAND_EVENT = 'end_crawl_to_stand'
END_SQUAT_TO_CRAWL_EVENT = 'end_squat_to_ground'
END_STAND_TO_CRAWL_EVENT = 'end_stand_to_crawl'
END_STAND_TO_DOWN_EVENT = 'end_stand_to_down'
END_DOWN_TO_STAND_EVENT = 'end_down_to_stand'
END_CELEBRATE_EVENT = 'end_celebrate'
END_SWIM_TRANSIT_FRONT_EVENT = 'end_swim_transit_front'
END_SWIM_TRANSIT_BACK_EVENT = 'end_swim_transit_back'
BEGIN_SWIM_STATE_EVENT = 'begin_swim'
END_SWIM_STATE_EVENT = 'end_swim'
BEGIN_SWIM_MOVE_EVENT = 'begin_swim_move'
END_SWIM_MOVE_EVENT = 'end_swim_move'
BEGIN_SWIM_IDLE_EVENT = 'begin_swim_idle'
END_SWIM_IDLE_EVENT = 'end_swim_idle'
END_MOVE_EVENT = 'end_move'
BEGIN_STAND_MOVE_EVENT = 'begin_stand_move'
BEGIN_STAND_SHOOT_MOVE_EVENT = 'begin_stand_shoot_move'
BEGIN_SQUAT_MOVE_EVENT = 'begin_squat_move'
BEGIN_SQUAT_RUN_EVENT = 'begin_squat_run'
BEGIN_RUN_FIRST_STAGE_EVENT = 'begin_run_first_stage'
BEGIN_RUN_THIRD_STAGE_EVENT = 'begin_run_third_stage'
BEGIN_RUN_SECOND_STAGE_EVENT = 'begin_run_second_stage'
END_RUN_SECOND_STAGE_EVENT = 'end_run_second_stage'
BEGIN_STAND_2_RUN_STAGE_EVENT = 'begin_stand_to_run_stage'
END_STAND_2_RUN_STAGE_EVENT = 'end_stand_to_run_stage'
BEGIN_IDLE_EVENT = 'begin_idle'
BEGIN_JUMP_IDLE_EVENT = 'begin_jump_idle'
END_IDLE_EVENT = 'end_idle'
BEGIN_MOVE_BRAKE_EVENT = 'begin_move_brake'
END_MOVE_BRAKE_EVENT = 'end_move_brake'
END_SKATE_STATE_EVENT = 'end_skate_state'
BEGIN_SKATE_BOARD_EVENT = 'begin_skate_board'
END_SKATE_BOARD_EVENT = 'end_skate_board'
BEGIN_SKATE_PREPARE_MOVE_EVENT = 'begin_skate_prepare_move'
END_SKATE_PREPARE_MOVE_EVENT = 'end_skate_prepare_move'
BEGIN_SKATE_BRAKE_EVENT = 'begin_skate_brake'
END_SKATE_BRAKE_EVENT = 'end_skate_brake'
BEGIN_SKATE_LEAVE_EVENT = 'begin_skate_leave'
END_SKATE_LEAVE_EVENT = 'end_skate_leave'
BEGIN_CLIM_UP_EVENT = 'begin_climb_up'
END_CLIM_UP_EVENT = 'end_climb_up'
END_CLIM_STAND_BARRIER_EVENT = 'end_climb_stand_barrier'
END_ENTER_MECHA_EVENT = 'end_enter_mecha'
END_UNWIND_EVENT = 'end_unwind'
BEGIN_RUSH_EVENT = 'begin_rush'
END_RUSH_EVENT = 'end_rush'
STAND_TO_CRAWL_NODE_NAME = 'stand_transmit_crawl'
HAVE_GUN_STAND_TO_CRAWL_CLIP_NAME = 'shoot_stand_transmit_crawl'
EMPTY_HAND_STAND_TO_CRAWL_CLIP_NAME = 'stand_transmit_crawl_emptyhand'
STAND_NODE_NAME = 'stand'
SQUAT_NODE_NAME = 'squat'
JUMP_ROOT_NODE_NAME = 'jump.full_body'
CRAWL_NODE_NAME = 'crawl'
DIE_NODE_NAME = 'die'
PUNCH_NODE_NAME = 'punch'
PICK_NODE_NAME = 'pick'
ROLL_NODE_NAME = 'roll'
RUSH_NODE_NAME = 'rush'
FULL_BODY_NODE_NAME = 'full_body'
RUN_JUMP_NODE_NAME = 'jump.run.jump_run_on_up'
NOT_RUN_JUMP_NODE_NAME = 'jump.stand_or_walk.jump_on_up'
RUN_JUMP_IN_AIR_NODE_NAME = 'jump_run_in_air'
NOT_RUN_JUMP_IN_AIR_NODE_NAME = 'jump.stand_or_walk.jump_in_air'
DOWN_TO_DIE_CLIP_NAME = 'dying_die'
STAND_TO_DIE_CLIP_NAME = 'die'
TURN_X_FULL_BODY_NODE = 'turn_x_full_body'
GET_NEW_GUN_ROOT_NODE_NAME = 'get_new_gun'
ADD_BULLET_ROOT_NODE_NAME = 'add_bullet'
FIRE_ROOT_NODE_NAME = 'fire'
LOAD_ROOT_NODE_NAME = 'load'
SWITCH_GUN_MODE_ROOT_NODE_NAME = 'switch_gun_mode'
HIT_NODE_NAME = 'be_hited'
TURN_X_UP_BODY_NODE_NAME = 'turn_x_up_body'
TURN_X_UP_BODY_NODE_DICT = {STATE_STAND: TURN_X_UP_BODY_NODE_NAME,STATE_SQUAT: TURN_X_UP_BODY_NODE_NAME,STATE_JUMP: TURN_X_UP_BODY_NODE_NAME,STATE_SWIM: TURN_X_UP_BODY_NODE_NAME,
   STATE_SKATE: TURN_X_UP_BODY_NODE_NAME,STATE_DOWN: TURN_X_UP_BODY_NODE_NAME,STATE_STAND_TO_DOWN: TURN_X_UP_BODY_NODE_NAME
   }
TURN_Y_UP_BODY_NOD_NAME = 'turn_y_up_body'
TURN_Y_UP_BODY_NODE_DICT = {STATE_STAND: TURN_Y_UP_BODY_NOD_NAME,STATE_JUMP: TURN_Y_UP_BODY_NOD_NAME,STATE_SQUAT: TURN_Y_UP_BODY_NOD_NAME,STATE_SWIM: TURN_Y_UP_BODY_NOD_NAME,
   STATE_SKATE: TURN_Y_UP_BODY_NOD_NAME,STATE_DOWN: TURN_Y_UP_BODY_NOD_NAME,STATE_STAND_TO_DOWN: TURN_Y_UP_BODY_NOD_NAME
   }
TURN_LEFT_NODE_DICT = {STATE_STAND: 'stand.prepare.turn_left.low_body',STATE_CRAWL: 'crawl.normal.turn_left',STATE_SQUAT: 'squat.turn_left.low_body'}
TURN_BODY_NODES = (
 'turn_x_full_body', TURN_Y_UP_BODY_NOD_NAME, TURN_X_UP_BODY_NODE_NAME)
LEFT_WEAPON_TRIGGER = 'action_gun_l'
RIGHT_WEAPON_TRIGGER = 'action_gun'
SWIM_EVENT_LIST = (
 (
  ('swim_idle', ), SWIM_EVENT_IDLE),
 (
  ('swim_f', ), SWIM_EVENT_MOVE_FRONT),
 (
  ('swim_b', ), SWIM_EVENT_MOVE_BACK))
THROW_BOMB_TRIGGER = 'action_gun'
MOVE_NODE_LIST = ('stand.prepare.move', 'stand.shoot.move')
USE_ITEM_NODE_LIST = ('stand.use_item', 'squat.use_item', 'crawl.use_item')
SOUND_TYPE_WALK = 0
SOUND_TYPE_RUN = 1
SOUND_TYPE_CRAWL = 2
SOUND_TYPE_SWIM = 3
SOUND_TYPE_JUMP = 4
SOUND_TYPE_RUSH = 5
sound_name_map = {SOUND_TYPE_WALK: 'walk',
   SOUND_TYPE_RUN: 'run',
   SOUND_TYPE_CRAWL: 'crawl',
   SOUND_TYPE_SWIM: 'swim'
   }
MP_STATUS_2_EVENT = {STATE_STAND: 'E_STAND',
   STATE_SQUAT: 'E_SQUAT',
   STATE_CRAWL: 'E_GROUND'
   }
IDLE_NODES = {STATE_STAND: 'stand.idle.static',STATE_SQUAT: 'squat.idle',STATE_JUMP: 'jump.have_gun.up_body.idle',STATE_SKATE: 'skate_idle.have_gun.up_body'
   }
SOURCE_NODE_INHERIT_ATTR = 256
STAND_MODEL_OFFSET_Y = state_physic_arg.stand_offset_y * NEOX_UNIT_SCALE
MP_STATUS_2_Y_OFF = {STATE_STAND: state_physic_arg.stand_offset_y * NEOX_UNIT_SCALE,
   STATE_SQUAT: state_physic_arg.squat_offset_y * NEOX_UNIT_SCALE,
   STATE_CRAWL: state_physic_arg.crawl_offset_y * NEOX_UNIT_SCALE,
   STATE_SWIM: {15: state_physic_arg.swim_offset_y_15 * NEOX_UNIT_SCALE}}

def get_y_offset(state, role_id):
    state_physic_arg.stand_offset_y * NEOX_UNIT_SCALE
    y_off_config = MP_STATUS_2_Y_OFF.get(state, STAND_MODEL_OFFSET_Y)
    if isinstance(y_off_config, dict):
        y_off = y_off_config.get(role_id, STAND_MODEL_OFFSET_Y)
        return y_off
    return y_off_config


BONE_HEAD_NAME = 'biped head'
BONE_SPINE_NAME = 'biped spine'
BONE_SPINE1_NAME = 'biped spine1'
BONE_SPINE2_NAME = 'biped spine2'
BONE_RIGHT_HAND_NAME = 'biped r hand'
BONE_LEFT_HAND_NAME = 'biped l hand'
BONE_BIPED_NAME = 'biped'
BONE_BIPED_ROOT = 'biped root'
BONE_CHESHEN_BONE01_NAME = 'cheshen_bone01'
ENABLE_FULL_BODY_BONE = (('biped root', 1), )
ENABLE_UP_BODY_BONE = (('biped root', 0), ('biped spine', 1))
NO_LIMIT_PARAM = '*'
DYNAMIC_MASK_BONE_CLIP = {'c_emptyhand_pick': ({'param': {'move_action': MOVE_STATE_STAND},'subtree': ENABLE_FULL_BODY_BONE}, {'param': {'move_action': (MOVE_STATE_WALK, MOVE_STATE_RUN)},'subtree': ENABLE_UP_BODY_BONE}),'c_shoot_pick': ({'param': {'move_action': MOVE_STATE_STAND},'subtree': ENABLE_FULL_BODY_BONE}, {'param': {'move_action': (MOVE_STATE_WALK, MOVE_STATE_RUN)},'subtree': ENABLE_UP_BODY_BONE}),'s_low_pick_move': ({'param': {'move_action': MOVE_STATE_STAND},'subtree': ENABLE_FULL_BODY_BONE}, {'param': {'move_action': (MOVE_STATE_WALK, MOVE_STATE_RUN)},'subtree': ENABLE_UP_BODY_BONE}),'s_shoot_low_pick_move': ({'param': {'move_action': MOVE_STATE_STAND},'subtree': ENABLE_FULL_BODY_BONE}, {'param': {'move_action': (MOVE_STATE_WALK, MOVE_STATE_RUN)},'subtree': ENABLE_UP_BODY_BONE})}
SOURCE_NODES_ORDERS = {'low_body_action.blend_6': ('bl', 'fl', 'b', 'f', 'br', 'fr')
   }
SOURCE_NODE_POSITION_PARAMETERS = {8032: {'low_body_action.blend_6': {'f': (0.0, 1.0),
                                      'fl': (-0.866, 0.5),
                                      'fr': (0.866, 0.5),
                                      'b': (0.0, -1.0),
                                      'bl': (-0.866, -0.5),
                                      'br': (0.866, -0.5)
                                      }
          }
   }

def get_source_node_position_parameters(blend_node_name, parameter_position_map):
    if blend_node_name not in SOURCE_NODES_ORDERS:
        return
    ret = []
    for dir_suffix in SOURCE_NODES_ORDERS[blend_node_name]:
        ret.append(parameter_position_map[dir_suffix])

    return tuple(ret)


def check_update_position_parameters(animator, mecha_id):
    if not global_data.feature_mgr.is_support_set_animator_blend_node_children_parameter_position():
        return
    if mecha_id not in SOURCE_NODE_POSITION_PARAMETERS:
        return
    for blend_node_name, parameter_position_map in SOURCE_NODE_POSITION_PARAMETERS[mecha_id].items():
        node = animator.find(blend_node_name)
        if not node:
            continue
        node.childrenParameterPositions = get_source_node_position_parameters(blend_node_name, parameter_position_map)


NEED_CACHE_ANIMATIONS = {8009: ('idle_m', 'idle_s', 'idle_r', 'switch_fanghuibuqiang', 'switch_nachuxiandanqiang',
 'switch_shouhuixiandan', 'switch_nachudaodan', 'switch_shouhuidaodan', 'switch_nachubuqiang',
 'huoliquankai_01', 'huoliquankai_02', 'huoliquankai_idle', 'huoliquankai_03'),
   8012: ('transform', 'roll_stand'),
   8017: ('aim_idle_l', 'aim_idle_r', 'aim_l', 'aim_r', 'aim_l2r', 'aim_r2l', 'aim_b_l', 'aim_f_l',
 'aim_b_r', 'aim_f_r', 'aim_bl', 'aim_br', 'aim_fl', 'aim_fr', 'aim_switch_fl2r',
 'aim_switch_fr2l', 'aim_switch_bl2r', 'aim_switch_br2l', 'shoot_jump_l_01', 'shoot_jump_l_02',
 'shoot_jump_l_03', 'shoot_jump_r_01', 'shoot_jump_r_02', 'shoot_jump_r_03'),
   8022: ('turn_l2r', 'turn_r2l'),
   8029: ('run', 'rifle_change', 'rifle_change_b', 'rifle_change_bl', 'rifle_change_br', 'rifle_change_f',
 'rifle_change_fl', 'rifle_change_fr', 'shotgun_change', 'shotgun_change_b', 'shotgun_change_bl',
 'shotgun_load', 'shotgun_load_b', 'shotgun_load_bl', 'shotgun_load_br', 'shotgun_load_f',
 'shotgun_load_fl', 'shotgun_change_br', 'shotgun_change_f', 'shotgun_change_fl',
 'shotgun_change_fr', 'shotgun_run', 'turnleft_90', 'turnright_90', 'shotgun_shoot',
 'shotgun_shoot_b', 'shotgun_shoot_f', 'shotgun_shoot_br', 'shotgun_shoot_bl', 'shotgun_shoot_fr',
 'shotgun_shoot_fl'),
   8033: ('trans_1', 'trans_2', 'trans_move_1', 'trans_move_2', 'reload', 'reload_f', 'reload_b',
 'reload_fr', 'reload_br', 'reload_fl', 'reload_bl', 'human_vice_01', 'human_vice_02',
 'human_vice_03')
   }

def check_cache_mecha_animation(is_avatar, animator, mecha_id, model):
    if is_avatar:
        if not animator.TrySetAsyncLoad(False):
            if mecha_id in NEED_CACHE_ANIMATIONS:
                import world
                for anim_name in NEED_CACHE_ANIMATIONS[mecha_id]:
                    model.cache_animation(anim_name, world.CACHE_ANIM_ALWAYS)

    elif mecha_id in NEED_CACHE_ANIMATIONS:
        import world
        for anim_name in NEED_CACHE_ANIMATIONS[mecha_id]:
            model.cache_animation(anim_name, world.CACHE_ANIM_ALWAYS)
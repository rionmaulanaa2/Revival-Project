# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/status_config.py
_reload_all = True
ST_DEAD = 10
ST_DOWN = 11
ST_ON_DRIVE = 12
ST_ON_PASSENGER = 13
ST_STAND = 14
ST_CROUCH = 15
ST_JUMP = 16
ST_JUMP_1 = 17
ST_JUMP_2 = 18
ST_JUMP_3 = 19
ST_SHOOT = 21
ST_MOVE = 22
ST_SWITCH = 23
ST_RELOAD = 24
ST_LOAD = 25
ST_RUN = 29
ST_TURN = 30
ST_AIM = 31
ST_PICK = 32
ST_EMPTY_HAND = 33
ST_USE_ITEM = 34
ST_HELP = 35
ST_DOWN_TRANSMIT_STAND = 38
ST_SWIM = 39
ST_PARACHUTE = 42
ST_RELOAD_LOOP = 43
ST_FLY = 44
ST_CLIMB = 45
ST_SKATE = 46
ST_SKATE_MOVE = 47
ST_SKATE_BRAKE = 48
ST_DISCARD = 51
ST_ROLL = 53
ST_RIGHT_AIM = 57
ST_MECHA_BOARDING = 61
ST_MECHA_DRIVER = 62
ST_MECHA_PASSENGER = 63
ST_RUSH = 64
ST_WEAPON_ACCUMULATE = 67
ST_MECH_EJECTION = 68
ST_CELEBRATE = 69
ST_SWITCH_WP_MODE = 70
ST_FROZEN = 71
ST_CROUCH_MOVE = 72
ST_CROUCH_RUN = 73
ST_HIT = 75
ST_SUPER_JUMP = 76
ST_VEHICLE_GUNNER = 77
ST_VEHICLE_PASSENGER = 78
ST_CUSTOM_ACTIONS = 79
ST_CONTINUE_ACTION = 80
ST_PERFORMANCE_ACTION = 81
ST_CONTROLLING_SPECIAL_WEAPON = 82
MC_DEAD = 10
MC_STAND = 14
MC_JUMP_1 = 17
MC_JUMP_2 = 18
MC_JUMP_3 = 19
MC_MOVE = 22
MC_RUN = 29
MC_TURN = 30
MC_USE_ITEM = 34
MC_HELP = 35
MC_DASH = 64
MC_HIT = 75
MC_SUPER_JUMP = 76
combine_state = {ST_SKATE_MOVE: set([ST_SKATE, ST_MOVE])
   }
num_2_desc = {10: 'ST_DEAD',
   11: 'ST_DOWN',
   12: 'ST_ON_DRIVE',
   13: 'ST_ON_PASSENGER',
   14: 'ST_STAND',
   15: 'ST_CROUCH',
   16: 'ST_JUMP',
   17: 'ST_JUMP_1',
   18: 'ST_JUMP_2',
   19: 'ST_JUMP_3',
   21: 'ST_SHOOT',
   22: 'ST_MOVE',
   23: 'ST_SWITCH',
   24: 'ST_RELOAD',
   25: 'ST_LOAD',
   29: 'ST_RUN',
   30: 'ST_TURN',
   31: 'ST_AIM',
   32: 'ST_PICK',
   33: 'ST_EMPTY_HAND',
   34: 'ST_USE_ITEM',
   35: 'ST_HELP',
   38: 'ST_DOWN_TRANSMIT_STAND',
   39: 'ST_SWIM',
   42: 'ST_PARACHUTE',
   43: 'ST_RELOAD_LOOP',
   44: 'ST_FLY',
   45: 'ST_CLIMB',
   46: 'ST_SKATE',
   47: 'ST_SKATE_MOVE',
   48: 'ST_SKATE_BRAKE',
   51: 'ST_DISCARD',
   53: 'ST_ROLL',
   57: 'ST_RIGHT_AIM',
   61: 'ST_MECHA_BOARDING',
   62: 'ST_MECHA_DRIVER',
   63: 'ST_MECHA_PASSENGER',
   64: 'ST_RUSH',
   67: 'ST_WEAPON_ACCUMULATE',
   68: 'ST_MECH_EJECTION',
   69: 'ST_CELEBRATE',
   70: 'ST_SWITCH_WP_MODE',
   71: 'ST_FROZEN',
   72: 'ST_CROUCH_MOVE',
   73: 'ST_CROUCH_RUN',
   75: 'ST_HIT',
   76: 'ST_SUPER_JUMP',
   77: 'ST_VEHICLE_GUNNER',
   78: 'ST_VEHICLE_PASSENGER',
   79: 'ST_CUSTOM_ACTIONS',
   80: 'ST_CONTINUE_ACTION',
   81: 'ST_PERFORMANCE_ACTION',
   82: 'ST_CONTROLLING_SPECIAL_WEAPON'
   }
desc_2_num = {'ST_DEAD': 10,
   'ST_DOWN': 11,
   'ST_ON_DRIVE': 12,
   'ST_ON_PASSENGER': 13,
   'ST_STAND': 14,
   'ST_CROUCH': 15,
   'ST_JUMP': 16,
   'ST_JUMP_1': 17,
   'ST_JUMP_2': 18,
   'ST_JUMP_3': 19,
   'ST_SHOOT': 21,
   'ST_MOVE': 22,
   'ST_SWITCH': 23,
   'ST_RELOAD': 24,
   'ST_LOAD': 25,
   'ST_RUN': 29,
   'ST_TURN': 30,
   'ST_AIM': 31,
   'ST_PICK': 32,
   'ST_EMPTY_HAND': 33,
   'ST_USE_ITEM': 34,
   'ST_HELP': 35,
   'ST_DOWN_TRANSMIT_STAND': 38,
   'ST_SWIM': 39,
   'ST_PARACHUTE': 42,
   'ST_RELOAD_LOOP': 43,
   'ST_FLY': 44,
   'ST_CLIMB': 45,
   'ST_SKATE': 46,
   'ST_SKATE_MOVE': 47,
   'ST_SKATE_BRAKE': 48,
   'ST_DISCARD': 51,
   'ST_ROLL': 53,
   'ST_RIGHT_AIM': 57,
   'ST_MECHA_BOARDING': 61,
   'ST_MECHA_DRIVER': 62,
   'ST_MECHA_PASSENGER': 63,
   'ST_RUSH': 64,
   'ST_WEAPON_ACCUMULATE': 67,
   'ST_MECH_EJECTION': 68,
   'ST_CELEBRATE': 69,
   'ST_SWITCH_WP_MODE': 70,
   'ST_FROZEN': 71,
   'ST_CROUCH_MOVE': 72,
   'ST_CROUCH_RUN': 73,
   'ST_HIT': 75,
   'ST_SUPER_JUMP': 76,
   'ST_VEHICLE_GUNNER': 77,
   'ST_VEHICLE_PASSENGER': 78,
   'ST_CUSTOM_ACTIONS': 79,
   'ST_CONTINUE_ACTION': 80,
   'ST_PERFORMANCE_ACTION': 81,
   'ST_CONTROLLING_SPECIAL_WEAPON': 82
   }
state_duration_config = {10: 0,
   11: -1,
   12: -1,
   13: -1,
   14: -1,
   15: -1,
   16: 10,
   17: 10,
   18: 10,
   19: 10,
   21: -1,
   22: -1,
   23: 10,
   24: 0,
   25: 0,
   29: -1,
   30: 0,
   31: -1,
   32: 0,
   33: -1,
   34: 0,
   35: 6,
   38: 0,
   39: -1,
   42: -1,
   43: -1,
   44: 10,
   45: 3,
   46: -1,
   47: -1,
   48: 3,
   51: -1,
   53: 0,
   57: -1,
   61: -1,
   62: -1,
   63: -1,
   64: 0,
   67: -1,
   68: 2,
   69: -1,
   70: 3,
   71: 10,
   72: -1,
   73: -1,
   75: -1,
   76: 10,
   77: -1,
   78: -1,
   79: 10,
   80: -1,
   81: -1,
   82: -1
   }
state_clip_config = {10: 'dead_ballon',
   24: 's_flamer_reload',
   25: 's_snipe_load',
   30: 'shoot_crouch_turn_r',
   32: 's_low_pick',
   34: 's_cure',
   38: 'dying_up',
   53: 'takeweapon_roll_b',
   64: 'flash_f'
   }
from . import status_override_forbid_config
from . import status_override_cover_config
from . import status_forbid_config
from . import status_cover_config
from logic.gcommon.common_utils import status_utils
import six
for special_status, basic_status in six.iteritems(status_override_cover_config.special_2_basic_config):
    status_cover_config.data[special_status] = set(status_cover_config.data[basic_status])
    status_forbid_config.data[special_status] = set(status_forbid_config.data[basic_status])
    for new_status, old_status_list in six.iteritems(status_cover_config.data):
        if basic_status in old_status_list:
            status_cover_config.data[new_status].add(special_status)

    for new_status, old_status_list in six.iteritems(status_forbid_config.data):
        if basic_status in old_status_list:
            status_forbid_config.data[new_status].add(special_status)

for new_status, old_status_list in six.iteritems(status_override_forbid_config.get_config_sets()):
    status_forbid_config.data[new_status] = status_forbid_config.data[new_status].union(old_status_list)
    cover_status_list = status_cover_config.data[new_status]
    for one_old_status in old_status_list:
        if one_old_status in cover_status_list:
            cover_status_list.remove(one_old_status)

for new_status, old_status_list in six.iteritems(status_override_cover_config.get_config_sets()):
    status_cover_config.data[new_status] = status_cover_config.data[new_status].union(old_status_list)
    forbid_status_list = status_forbid_config.data[new_status]
    for one_old_status in old_status_list:
        if one_old_status in forbid_status_list:
            forbid_status_list.remove(one_old_status)

human_id = '10011'
behav_config = status_utils.get_behavior_config(human_id)
cover = behav_config.get_cover(human_id)
forbid = behav_config.get_forbid(human_id)
for special_status, basic_status in six.iteritems(status_override_cover_config.special_2_basic_config):
    cover[special_status] = set(cover[basic_status])
    forbid[special_status] = set(forbid[basic_status])
    for new_status, old_status_list in six.iteritems(cover):
        if basic_status in old_status_list:
            cover[new_status].add(special_status)

    for new_status, old_status_list in six.iteritems(forbid):
        if basic_status in old_status_list:
            forbid[new_status].add(special_status)

for new_status, old_status_list in six.iteritems(status_override_forbid_config.get_config_sets()):
    forbid[new_status] = forbid[new_status].union(old_status_list)
    cover_status_list = cover[new_status]
    for one_old_status in old_status_list:
        if one_old_status in cover_status_list:
            cover_status_list.remove(one_old_status)

for new_status, old_status_list in six.iteritems(status_override_cover_config.get_config_sets()):
    cover[new_status] = cover[new_status].union(old_status_list)
    forbid_status_list = forbid[new_status]
    for one_old_status in old_status_list:
        if one_old_status in forbid_status_list:
            forbid_status_list.remove(one_old_status)
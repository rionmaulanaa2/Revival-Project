# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/ai_const.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
ST_WAIT = 1
ST_PREPARE_SHOOT = 2
ST_XULI = 3
ST_SHOOTING = 4
ST_RELOAD_BULLET = 5
ST_SWITCH_WEAPON = 6
ST_PREPARE_USE_SKILL = 7
ST_MECHA_HANG_UP = 1000
MOVE_TYPE_NORMAL = 1
MOVE_TYPE_PATHING = 2
MOVE_TYPE_FAST_PATHING = 3
AI_EVT_ON_HIT = 1
AI_EVT_ON_KILL_OTHER = 2
AI_EVT_SHOOT_PLAYER = 3
AI_CALL_MECHA_SEARCH_PLAYER_RANGE = 300
AI_CALL_MECHA_WAIT_TIME_MIN = 320
AI_CALL_MECHA_WAIT_TIME_MAX = 340
AI_CALL_MECHA_FIXED_CD = 10
AI_CALL_MECHA_RANGE = 20
AI_CALL_MECHA_FIND_POS_MAX_TRY_TIMES = 6
CTRL_ACTION_MAIN = 1
CTRL_ACTION_SUB = 2
CTRL_ACTION_JUMP = 3
CTRL_ACTION_RUSH = 4
CTRL_ACTION_EXT = 5
REACH_OFFSET = NEOX_UNIT_SCALE / 2
YAW_OFFSET = 0.01
AI_CAN_ATK_TYPE_BUILDING = 1
AI_MOVE_PATH_SHOW = False
PATH_SHOW_TYPE_DETOUR = 1
PATH_SHOW_TYPE_LOGIC = 2
AI_EJECT_PARA_TYPE_LINEAR = 1
AI_EJECT_PARA_TYPE_RL = 2
AI_EJECT_PARA_TYPE_RRL = 3
from math import pi
AI_EJECT_PARA_CONFIG = {AI_EJECT_PARA_TYPE_LINEAR: (),
   AI_EJECT_PARA_TYPE_RL: ({'rad': (pi / 4, pi / 2),'radius': (10, 40)},),AI_EJECT_PARA_TYPE_RRL: ({'rad': (pi / 3, pi / 1.5),'radius': (5, 20)}, {'rad': (pi / 4, pi / 2),'radius': (12, 35)})}
AI_EJECT_PARA_SHAKE_YAW = (
 -pi / 3, pi / 3)
COLOR_RED = (255, 255, 0, 0)
COLOR_GREEN = (255, 0, 255, 0)
COLOR_BLUE = (255, 0, 0, 255)
STATE_INFO = {'CombatState': [
                 '\xe6\x88\x98\xe6\x96\x97', COLOR_RED],
   'DropState': [
               '\xe5\xbc\x80\xe5\xb1\x80\xe8\xb7\xb3\xe4\xbc\x9e', COLOR_BLUE],
   'EjectState': [
                '\xe6\x91\xa7\xe6\xaf\x81\xe8\xb7\xb3\xe4\xbc\x9e', COLOR_BLUE],
   'EscapePoisonState': [
                       '\xe8\xb7\x91\xe6\xaf\x92', COLOR_BLUE],
   'FlightState': [
                 '\xe8\x88\xaa\xe7\xba\xbf', COLOR_BLUE],
   'FollowState': [
                 '\xe8\xbf\xbd\xe5\x87\xbb', COLOR_BLUE],
   'FrozenState': [
                 '\xe5\x86\xbb\xe7\xbb\x93', COLOR_GREEN],
   'IdleState': [
               '\xe5\xbe\x85\xe6\x9c\xba', COLOR_GREEN],
   'MechaCombatState': [
                      '\xe6\x9c\xba\xe7\x94\xb2\xe6\x88\x98\xe6\x96\x97', COLOR_RED],
   'MechaState': [
                '\xe6\x9c\xba\xe7\x94\xb2\xe5\x9f\xba\xe7\xa1\x80', COLOR_GREEN],
   'PatrolState': [
                 '\xe5\xb7\xa1\xe9\x80\xbb', COLOR_BLUE],
   'PickItemState': [
                   '\xe6\x8b\xbe\xe5\x8f\x96', COLOR_GREEN],
   'RunAwayState': [
                  '\xe9\x80\x83\xe8\xb7\x91', COLOR_BLUE],
   'UseDrugState': [
                  '\xe7\x94\xa8\xe8\x8d\xaf', COLOR_GREEN]
   }
STATE_MARK_INFO = {'CombatState': 'A',
   'PatrolState': 'I',
   'FollowState': 'Z',
   'RunAwayState': 'R',
   'EscapePoisonState': 'P',
   'DropState': 'D',
   'FlightState': 'F',
   'EjectState': 'E'
   }
MOVE_MIN_HEIGHT = -25 * NEOX_UNIT_SCALE
AI_SEA_LEVEL_HEIGHT = {'bw_all06': 40 * NEOX_UNIT_SCALE,
   'kongdao': 70 * NEOX_UNIT_SCALE,
   'default': 40 * NEOX_UNIT_SCALE
   }
AI_SEA_FOOT_HEIGHT = {'bw_all06': AI_SEA_LEVEL_HEIGHT['bw_all06'] - 5 * NEOX_UNIT_SCALE,
   'kongdao': AI_SEA_LEVEL_HEIGHT['kongdao'] - 5 * NEOX_UNIT_SCALE,
   'default': AI_SEA_LEVEL_HEIGHT['default'] - 5 * NEOX_UNIT_SCALE
   }
AI_AGENT_MOVE = 1
AI_AGENT_WATER = 2
AI_MAP_LIMIT_BORDER = 1900 * NEOX_UNIT_SCALE
AI_SKATE_BOARD = 'skate_board'
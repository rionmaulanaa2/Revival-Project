# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/camera_const.py
from __future__ import absolute_import
from six.moves import range
_reload_all = True
import sys
import math3d
import math
import data.camera_state_const as camera_state_const
BASE_MODEL = '0'
FOLLOW_SYNC_NONE = 0
FOLLOW_SYNC_TARGET = 1
FOLLOW_SYNC_CAM = 2
POSTURE_STAND = '1'
POSTURE_SQUAT = '2'
POSTURE_GROUND = '3'
POSTURE_JUMP = '4'
POSTURE_KNOCK_DOWN = '5'
POSTURE_SWIM = '6'
POSTURE_CLIMB = '7'
POSTURE_RIGHT_SIDEWAYS = '10'
POSTURE_LEFT_SIDEWAYS = '11'
POSTURE_UP_SIDEWAYS = '12'
from data.camera_state_const import *
FREE_CAMERA_LIST = frozenset([PREVIEW_MODEL, FREE_MODEL, PLANE_MODE, FREE_DROP_MODE, DEBUG_MODE])
FREE_CAMERA_SLERP_LIST = [
 PREVIEW_MODEL, FREE_MODEL, PLANE_MODE]
PARACHUTE_CAMERA_LIST = frozenset([PARACHUTE_MODE, FREE_DROP_MODE])
MOVE_DIR_NUMS = 24
sys.modules[__name__].__dict__.update(dict([ ('MOVE_DIR_' + str(idx * 360 // MOVE_DIR_NUMS), idx) for idx in range(MOVE_DIR_NUMS + 1) ]))
v = math3d.vector(0, 0, 1)
DIR_VECS = [ v * math3d.matrix.make_rotation_y(math.pi * 2 * i / MOVE_DIR_NUMS) for i in range(MOVE_DIR_NUMS) ]
v = None
NORMAL_Z_RANGE = (1, 10000.0)
JET_Z_RANGE = (0.1, 290000.0)
PARACHUTE_Z_RANGE = (30.0, 290000.0)
COLL_SLERP = 1
SWITCH_SLERP = 2
CAM_ROT_INPUT_SRC_NONE = 0
CAM_ROT_INPUT_SRC_SLIDE = 2
CAM_ROT_INPUT_SRC_SENSOR = 1
DISABLE_POSTURE = 0
ENABLE_POSTURE = 1
INHERIT_POSTURE = 2
FREE_CAMERA_TYPE = set([camera_state_const.OBSERVE_FREE_MODE, camera_state_const.FREE_MODEL])
RECONNECT_HUMAN_DIR = 1
RECONNECT_CAM_DIR = 2
RECONNECT_DEFAULT_DIR = 3
HDR_TONE_FACTOR_OUTSIDE = 1.0
HDR_TONE_FACTOR_INSIDE = 2.0
HDR_TONE_FACTOR_DURATION = 2.0
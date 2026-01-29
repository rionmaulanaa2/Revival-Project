# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/trick_bullet_utils.py
from __future__ import absolute_import
from six.moves import range
import exception_hook
try:
    import cython
except:
    exception_hook.post_error('[import ERROR] 1')

from common.utils.timer import CLOCK, RELEASE
from common.framework import Functor
import world
import math3d
MAX_QUEUE_LEN = 60
REAL_BULLET_INDEX = 0
POS_QUEUE_INDEX = 1
CUR_QUEUE_LEN_INDEX = 2
QUEUE_TAIL_INDEX = 3
TIMER_INDEX = 4
REAL_BULLET_POS_DICT = {}
REAL_BULLET_TO_KEY_MAP = {}
TRICK_BULLET_COUNT_INDEX = 0
DONE_BULLET_COUNT_INDEX = 1
BULLET_SFX_LIST_INDEX = 2
BULLET_HEAD_LIST_INDEX = 3
TRICK_BULLET_DATA = {}
SCALE_DATA = {}
START_POS_INDEX = 0
START_CAMERA_FORWARD_INDEX = 1
OFFSET_VEC_LIST_INDEX = 2
OFFSET_ROTATION_LIST_INDEX = 3
OFFSET_DATA = {}
BULLET_OWNER_MAP = {}

def _init_bullet_scale(bullet_model, scale_data):
    min_scale = scale_data[0]
    bullet_model.scale = math3d.vector(min_scale, min_scale, min_scale)
    scale_data.pop(0)


def _update_bullet_scale(dt, bullet_model, scale_data):
    max_scale, duration = scale_data[0], scale_data[1]
    if duration >= 0:
        duration -= dt
        cur_scale = bullet_model.scale.x
        if duration > 0:
            new_scale = cur_scale + (max_scale - cur_scale) / duration * dt
        else:
            new_scale = max_scale
        bullet_model.scale = math3d.vector(new_scale, new_scale, new_scale)
        scale_data[1] = duration


def _record_real_bullet_pos(dt, real_bullet_key, scale_data):
    if real_bullet_key not in REAL_BULLET_POS_DICT:
        return RELEASE
    else:
        real_bullet_data = REAL_BULLET_POS_DICT[real_bullet_key]
        model, pos_queue, cur_queue_len, tail = (real_bullet_data[REAL_BULLET_INDEX], real_bullet_data[POS_QUEUE_INDEX], real_bullet_data[CUR_QUEUE_LEN_INDEX], real_bullet_data[QUEUE_TAIL_INDEX])
        if model is None or not model.valid:
            real_bullet_data[TIMER_INDEX] = None
            real_bullet_data[0] = None
            return RELEASE
        _update_bullet_scale(dt, model, scale_data)
        if cur_queue_len < MAX_QUEUE_LEN:
            pos_queue.append(model.world_position)
            real_bullet_data[CUR_QUEUE_LEN_INDEX] += 1
        else:
            pos_queue[tail] = model.world_position
        real_bullet_data[QUEUE_TAIL_INDEX] = (tail + 1) % MAX_QUEUE_LEN
        return


def begin_record_real_bullet_pos(real_bullet_key, model, scale_data, trick_bullet_count):
    unit = BULLET_OWNER_MAP[real_bullet_key][0]
    if unit.ev_g_is_avatar() or global_data.cam_lplayer and global_data.cam_lplayer.id == unit.share_data.ref_driver_id:
        cam_forward = world.get_active_scene().active_camera.rotation_matrix.forward
    else:
        cam_forward = unit.ev_g_forward()
    OFFSET_DATA[real_bullet_key] = [model.world_position, cam_forward, [ None for i in range(trick_bullet_count) ], [ None for i in range(trick_bullet_count) ]]
    REAL_BULLET_POS_DICT[real_bullet_key] = [model, list(), 0, 0, None]
    _init_bullet_scale(model, scale_data)
    _record_real_bullet_pos(0, real_bullet_key, scale_data)
    REAL_BULLET_POS_DICT[real_bullet_key][TIMER_INDEX] = global_data.game_mgr.register_logic_timer(_record_real_bullet_pos, args=(real_bullet_key, scale_data), interval=1, times=-1, timedelta=True)
    return


def _on_load_trick_bullet(real_bullet_key, index, scale_data, sfx):
    bullet_sfx_list = TRICK_BULLET_DATA[real_bullet_key][BULLET_SFX_LIST_INDEX]
    head_list = TRICK_BULLET_DATA[real_bullet_key][BULLET_HEAD_LIST_INDEX]
    bullet_sfx_list[index] = sfx
    head_list[index] = 0
    unit, weapon_pos = BULLET_OWNER_MAP[real_bullet_key][0], BULLET_OWNER_MAP[real_bullet_key][1]
    offset_data = OFFSET_DATA[real_bullet_key]
    if not world.get_active_scene():
        cam_forward = offset_data[START_CAMERA_FORWARD_INDEX]
    elif unit.is_valid():
        if unit.ev_g_is_avatar():
            cam_forward = world.get_active_scene().active_camera.rotation_matrix.forward
        else:
            cam_forward = unit.ev_g_forward()
    else:
        cam_forward = offset_data[START_CAMERA_FORWARD_INDEX]
    mat = math3d.matrix.make_rotation_between(offset_data[START_CAMERA_FORWARD_INDEX], cam_forward)
    rot = math3d.matrix_to_rotation(mat)
    offset_data[OFFSET_ROTATION_LIST_INDEX][index] = rot
    pos = None
    if unit.is_valid():
        pos = unit.ev_g_fired_pos(weapon_pos)
    if not pos:
        pos = offset_data[START_POS_INDEX]
    offset_data[OFFSET_VEC_LIST_INDEX][index] = pos - offset_data[START_POS_INDEX]
    _init_bullet_scale(sfx, scale_data)
    _update_trick_bullet_pos(0, real_bullet_key, index, scale_data)
    global_data.game_mgr.register_logic_timer(_update_trick_bullet_pos, args=(real_bullet_key, index, scale_data), interval=1, times=-1, timedelta=True)
    return


def _check_all_trick_bullet_done(real_bullet_key):
    trick_bullet_data = TRICK_BULLET_DATA[real_bullet_key]
    trick_bullet_data[DONE_BULLET_COUNT_INDEX] += 1
    if trick_bullet_data[DONE_BULLET_COUNT_INDEX] == trick_bullet_data[TRICK_BULLET_COUNT_INDEX]:
        REAL_BULLET_POS_DICT.pop(real_bullet_key)
        TRICK_BULLET_DATA.pop(real_bullet_key)
        BULLET_OWNER_MAP.pop(real_bullet_key)


def _update_trick_bullet_pos(dt, real_bullet_key, index, scale_data):
    bullet_sfx_list = TRICK_BULLET_DATA[real_bullet_key][BULLET_SFX_LIST_INDEX]
    head_list = TRICK_BULLET_DATA[real_bullet_key][BULLET_HEAD_LIST_INDEX]
    head = head_list[index]
    if head != REAL_BULLET_POS_DICT[real_bullet_key][QUEUE_TAIL_INDEX] and bullet_sfx_list[index] and bullet_sfx_list[index].valid:
        real_bullet_pos = REAL_BULLET_POS_DICT[real_bullet_key][POS_QUEUE_INDEX][head]
        _update_bullet_scale(dt, bullet_sfx_list[index], scale_data)
        offset_data = OFFSET_DATA[real_bullet_key]
        ini_vec = real_bullet_pos - offset_data[START_POS_INDEX]
        final_vec = offset_data[OFFSET_ROTATION_LIST_INDEX][index].rotate_vector(ini_vec)
        final_pos = offset_data[START_POS_INDEX] + final_vec
        final_pos += offset_data[OFFSET_VEC_LIST_INDEX][index]
        bullet_sfx_list[index].position = final_pos
        head_list[index] = (head + 1) % MAX_QUEUE_LEN
    else:
        global_data.sfx_mgr.shutdown_sfx(bullet_sfx_list[index])
        bullet_sfx_list[index] = None
        _check_all_trick_bullet_done(real_bullet_key)
        return RELEASE
    return


def _create_sfx--- This code section failed: ---

 182       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'sfx_mgr'
           6  LOAD_ATTR             2  'create_sfx_in_scene'

 183       9  LOAD_ATTR             1  'sfx_mgr'
          12  LOAD_GLOBAL           3  'Functor'
          15  LOAD_GLOBAL           4  '_on_load_trick_bullet'
          18  LOAD_FAST             1  'real_bullet_key'
          21  LOAD_FAST             2  'index'
          24  LOAD_FAST             3  'scale_data'
          27  CALL_FUNCTION_4       4 
          30  CALL_FUNCTION_257   257 
          33  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 30


def load_trick_bullet(real_bullet_key, model, trick_bullet_count, bullet_path, interval, scale_data_list, unit, weapon_pos):
    if not world.get_active_scene():
        return
    else:
        if not unit.is_valid():
            return
        str_model = str(model)
        if str_model in REAL_BULLET_TO_KEY_MAP:
            old_real_bullet_key = REAL_BULLET_TO_KEY_MAP[str_model]
            destroy_real_bullet_model(old_real_bullet_key, str_model)
        REAL_BULLET_TO_KEY_MAP[str_model] = real_bullet_key
        BULLET_OWNER_MAP[real_bullet_key] = (unit, weapon_pos)
        begin_record_real_bullet_pos(real_bullet_key, model, scale_data_list[0], trick_bullet_count)
        TRICK_BULLET_DATA[real_bullet_key] = [trick_bullet_count, 0, [ None for i in range(trick_bullet_count) ], [ 0 for i in range(trick_bullet_count) ]]
        for i in range(trick_bullet_count):
            delay_time = interval * (i + 1)
            global_data.game_mgr.register_logic_timer(_create_sfx, args=(bullet_path, real_bullet_key, i, scale_data_list[i + 1]), interval=delay_time, times=1, mode=CLOCK)

        return


def destroy_real_bullet_model(real_bullet_key, str_model):
    if real_bullet_key in REAL_BULLET_POS_DICT:
        REAL_BULLET_POS_DICT[real_bullet_key][REAL_BULLET_INDEX] = None
        str_model in REAL_BULLET_TO_KEY_MAP and REAL_BULLET_TO_KEY_MAP.pop(str_model)
    return
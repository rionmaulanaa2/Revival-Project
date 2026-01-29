# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/lobby_jump_utils.py
from __future__ import absolute_import
from six.moves import range
import world
import math3d
from logic.client.const.camera_const import POSTURE_STAND
from logic.gcommon.cdata import status_config
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as g_const
from logic.gcommon.common_const import collision_const
import collision
import math

def lobby_jump():
    if not global_data.is_inner_server:
        return
    if global_data.player and global_data.player.is_in_battle():
        return
    if not global_data.lobby_player:
        return
    if not global_data.is_pc_mode and not global_data.is_inner_server:
        return
    lo_player = global_data.lobby_player
    flag = _check_climb(lo_player)
    if flag[0]:
        _try_climb(lo_player, flag[1], flag[2], flag[3])
        global_data.lo_climb_err_code = 1
    else:
        _try_jump(lo_player)
        global_data.lo_climb_err_code = flag[1]


def can_jump(unit):
    return unit.ev_g_can_jump()


def can_climb(unit):
    if unit.ev_g_is_jump():
        return False
    if unit.ev_g_is_climb():
        return False
    return True


def _check_climb(unit):
    if not unit:
        return [False, -3]
    if not can_climb(unit):
        return [False, -2]
    player_pos = unit.ev_g_foot_position()
    if not player_pos:
        return [False, -3]
    scn = world.get_active_scene()
    model_yaw = unit.ev_g_model_yaw()
    forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
    group_climb_check = collision_const.GROUP_CLIMB_CHECK
    chect_begin = player_pos + math3d.vector(0, g_const.CLIMB_MIN_HIGHT, 0)
    check_end = chect_begin + forward_vect * g_const.CLIMB_MAX_DISTANCE
    distance = 0
    result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
    if result[0]:
        distance = (result[1] - chect_begin).length
        if abs(result[2].y) > 0.18:
            return [False, -4]
    else:
        return [
         False, -5]
    for i in range(2):
        if i == 0:
            offset = g_const.FIRST_FORWARD_OFFSET
        else:
            offset = g_const.SECOND_FORWARD_OFFSET
        forward_pos = player_pos + forward_vect * (distance + offset)
        chect_begin = forward_pos + math3d.vector(0.0, g_const.CLIMB_MAX_HIGHT, 0.0)
        check_end = forward_pos + math3d.vector(0.0, g_const.CLIMB_MIN_HIGHT, 0.0)
        height = 0
        result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
        if result[0]:
            height = result[1].y
            if abs(result[2].y) < 0.9:
                return [False, -6]
            climb_height = height - player_pos.y
            if climb_height < g_const.CLIMB_MIN_HIGHT or climb_height > g_const.CLIMB_MAX_HIGHT:
                return [False, -7]
            break
    else:
        return [
         False, -8]

    height += 0.4
    forward_pos = player_pos + forward_vect * (distance + g_const.CLIMB_BOARD_MIN_WIDTH)
    chect_begin = forward_pos + math3d.vector(0.0, g_const.CLIMB_MAX_HIGHT, 0.0)
    check_end = forward_pos + math3d.vector(0.0, g_const.CLIMB_MIN_HIGHT + g_const.CLIMB_RAY_CHECK_HEIGHT, 0.0)
    result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
    if result[0]:
        offset = height - result[1].y
        if offset < 0.01:
            climb_type = g_const.CLIMB_TO_TOP_STAND
        elif unit.ev_g_is_in_any_state((status_config.ST_RUN,)):
            climb_type = g_const.CLIMB_TO_RUN
        else:
            climb_type = g_const.CLIMB_TO_DOWN_STAND
    else:
        climb_type = g_const.CLIMB_TO_DROP
    character = unit.share_data.ref_character
    if not character:
        return [False, -9]
    if climb_type == g_const.CLIMB_TO_TOP_STAND:
        c_width = collision_const.CHARACTER_STAND_WIDTH
        c_height = collision_const.CHARACTER_STAND_HEIGHT - c_width * 2.0
        check_distance = g_const.CLIMB_BOARD_MIN_WIDTH
    else:
        c_width = collision_const.CHARACTER_CLIMB_WIDTH
        c_height = collision_const.CHARACTER_CLIMB_HEIGHT - c_width * 2.0
        check_distance = g_const.CLIMB_BOARD_MIN_WIDTH + (collision_const.CHARACTER_STAND_WIDTH - c_width) + 3.9
    c_width *= 1.1
    check_pos_y = height + c_height * 0.5 + c_width
    check_begin = math3d.vector(player_pos.x, check_pos_y, player_pos.z)
    check_end = check_begin + forward_vect * check_distance
    size = math3d.vector(c_width, c_height, 1)
    col = collision.col_object(collision.CAPSULE, size, group_climb_check, group_climb_check)
    result = scn.scene_col.sweep_intersect(col, check_begin, check_end, group_climb_check, group_climb_check, collision.INCLUDE_FILTER)
    if result:
        return [False, -10]
    if climb_type != g_const.CLIMB_TO_TOP_STAND:
        character = unit.share_data.ref_character
        if not character:
            return [False, -11]
        size = math3d.vector(collision_const.CHARACTER_STAND_WIDTH, collision_const.CHARACTER_STAND_HEIGHT - collision_const.CHARACTER_STAND_WIDTH * 2, 1)
        check_pos_y = height + size.y * 0.5 + size.x
        check_end = math3d.vector(check_end.x, check_pos_y, check_end.z)
        is_hit = unit.ev_g_static_test(character.group, character.mask, check_end)
        if is_hit:
            return [False, -11]
    if climb_height < g_const.CLIMB_RAY_CHECK_HEIGHT:
        climb_type += g_const.CLIMB_SUB_TYPY_COUNT
    climb_pos = math3d.vector(player_pos.x, height, player_pos.z) + forward_vect * (distance + g_const.CLIMB_POINT_OFFSET)
    return [
     True, climb_type, climb_pos, model_yaw]


def _try_climb(unit, climb_type, climb_pos, climb_rotation):
    if not unit:
        return
    if not can_climb(unit):
        return
    unit.send_event('E_CLIMB', climb_type, climb_pos, climb_rotation)


def _try_jump(unit):
    if not unit:
        return
    if not can_jump(unit):
        return
    unit.send_event('E_CTRL_JUMP')
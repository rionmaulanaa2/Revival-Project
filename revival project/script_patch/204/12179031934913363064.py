# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sfx_utils.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
DIS_LEVEL_0 = (10 * NEOX_UNIT_SCALE) ** 2
DIS_LEVEL_1 = (200 * NEOX_UNIT_SCALE) ** 2
DIS_RATE_0 = 1.0
DIS_RATE_1 = 4.0
DIS_F_RATE_0 = (DIS_RATE_1 - DIS_RATE_0) / (DIS_LEVEL_1 - DIS_LEVEL_0)
DIS_F_RATE_1 = DIS_RATE_0 - DIS_LEVEL_0 * DIS_F_RATE_0
FOV_LEVEL_0 = 20
FOV_LEVEL_1 = 80
FOV_RATE_0 = 0.8
FOV_RATE_1 = 1.0
FOV_F_RATE_0 = (FOV_RATE_1 - FOV_RATE_0) / (FOV_LEVEL_1 - FOV_LEVEL_0)
FOV_F_RATE_1 = FOV_RATE_0 - FOV_LEVEL_0 * FOV_F_RATE_0
DIS_RATE_HUMAN_0 = 3.0
DIS_RATE_HUMAN_1 = 20.0
DIS_F_RATE_HUMAN_0 = (DIS_RATE_HUMAN_1 - DIS_RATE_HUMAN_0) / (DIS_LEVEL_1 - DIS_LEVEL_0)
DIS_F_RATE_HUMAN_1 = DIS_RATE_HUMAN_0 - DIS_LEVEL_0 * DIS_F_RATE_0
FOV_RATE_HUMAN_0 = 0.7
FOV_F_RATE_HUMAN_0 = (FOV_RATE_1 - FOV_RATE_HUMAN_0) / (FOV_LEVEL_1 - FOV_LEVEL_0)
FOV_F_RATE_HUMAN_1 = FOV_RATE_HUMAN_0 - FOV_LEVEL_0 * FOV_F_RATE_0
DEAD_DIS_LEVEL_0 = 15 * NEOX_UNIT_SCALE
DEAD_DIS_LEVEL_1 = 80 * NEOX_UNIT_SCALE
DEAD_DIS_LEVEL_2 = 200 * NEOX_UNIT_SCALE
DEAD_DIS_RATE_0 = 1.0
DEAD_DIS_RATE_1 = 3.0
DEAD_DIS_RATE_2 = 5.0
DEAD_DIS_F_RATE_0 = (DEAD_DIS_RATE_1 - DEAD_DIS_RATE_0) / (DEAD_DIS_LEVEL_1 - DEAD_DIS_LEVEL_0)
DEAD_DIS_F_RATE_1 = DEAD_DIS_RATE_0 - DEAD_DIS_LEVEL_0 * DEAD_DIS_F_RATE_0
DEAD_DIS_F_RATE_2 = (DEAD_DIS_RATE_2 - DEAD_DIS_RATE_1) / (DEAD_DIS_LEVEL_2 - DEAD_DIS_LEVEL_1)
DEAD_FOV_RATE_0 = 0.8
DEAD_FOV_RATE_1 = 1.5
DEAD_FOV_F_RATE_0 = (DEAD_FOV_RATE_1 - DEAD_FOV_RATE_0) / (FOV_LEVEL_1 - FOV_LEVEL_0)
DEAD_FOV_F_RATE_1 = DEAD_FOV_RATE_0 - FOV_LEVEL_0 * DEAD_FOV_F_RATE_0

def get_sfx_scale_by_length_spr(length_sqr):
    f_dis = DIS_RATE_0
    if length_sqr >= DIS_LEVEL_0 and length_sqr < DIS_LEVEL_1:
        f_dis = length_sqr * DIS_F_RATE_0 + DIS_F_RATE_1
    elif length_sqr > DIS_LEVEL_1:
        f_dis = DIS_RATE_1
    f_fov = FOV_RATE_0
    fov = global_data.game_mgr.scene.active_camera.fov
    if fov >= FOV_LEVEL_0 and fov < FOV_LEVEL_1:
        f_fov = fov * FOV_F_RATE_0 + FOV_F_RATE_1
    elif fov >= FOV_LEVEL_1:
        f_fov = FOV_RATE_1
    return f_dis * f_fov


def get_sfx_scale_by_length_human_spr(length_sqr):
    f_dis = DIS_RATE_HUMAN_0
    if length_sqr >= DIS_LEVEL_0 and length_sqr < DIS_RATE_HUMAN_1:
        f_dis = length_sqr * DIS_F_RATE_HUMAN_0 + DIS_F_RATE_HUMAN_1
    elif length_sqr > DIS_RATE_HUMAN_1:
        f_dis = DIS_RATE_1
    f_fov = FOV_RATE_HUMAN_0
    fov = global_data.game_mgr.scene.active_camera.fov
    if fov >= FOV_LEVEL_0 and fov < FOV_LEVEL_1:
        f_fov = fov * FOV_F_RATE_HUMAN_0 + FOV_F_RATE_HUMAN_1
    elif fov >= FOV_LEVEL_1:
        f_fov = FOV_RATE_1
    return f_dis * f_fov


def get_dead_sfx_scale_by_length_spr(length):
    f_dis = DEAD_DIS_RATE_0
    if length >= DEAD_DIS_LEVEL_0 and length < DEAD_DIS_LEVEL_1:
        f_dis = DEAD_DIS_RATE_0 + (length - DEAD_DIS_LEVEL_0) * DEAD_DIS_F_RATE_0
    elif length >= DEAD_DIS_LEVEL_1 and length < DEAD_DIS_LEVEL_2:
        f_dis = DEAD_DIS_RATE_1 + (length - DEAD_DIS_LEVEL_1) * DEAD_DIS_F_RATE_2
    elif length > DEAD_DIS_LEVEL_2:
        f_dis = DEAD_DIS_RATE_2
    f_fov = DEAD_FOV_RATE_0
    fov = global_data.game_mgr.scene.active_camera.fov
    if fov >= FOV_LEVEL_0 and fov < FOV_LEVEL_1:
        f_fov = fov * DEAD_FOV_F_RATE_0 + DEAD_FOV_F_RATE_1
    elif fov >= FOV_LEVEL_1:
        f_fov = DEAD_FOV_RATE_1
    return f_dis * f_fov
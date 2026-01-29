# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/map_3d_utils.py
from __future__ import absolute_import
import math3d
import math
BASE_Y = 350.0
BASE_X = 0.0
BASE_Z = 600.0
ANI_START_ROT = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(-30.0 / 180 * math.pi, 0.0, 0.0)))
ANI_START_POS = math3d.vector(BASE_X, BASE_Y, BASE_Z + 100)
ANI_END_POS = math3d.vector(BASE_X, BASE_Y, BASE_Z)
END_POS = math3d.vector(BASE_X, BASE_Y, BASE_Z)
END_MAT = math3d.matrix.make_translation(BASE_X, BASE_Y, BASE_Z)
START_SCALE = math3d.vector(1.0, 1.0, 1.0)
END_SCALE = math3d.vector(1.0, 1.0, 1.0)
START_ROT = math3d.euler_to_rotation(math3d.vector(0.0 / 180 * math.pi, 0.0, 0.0))
END_ROT = math3d.euler_to_rotation(math3d.vector(-75.0 / 180 * math.pi, 0.0 / 180 * math.pi, 0.0))
START_ROT_MAT = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(0.0 / 180 * math.pi, 0.0, 0.0)))
END_ROT_MAT = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(-75.0 / 180 * math.pi, 0.0 / 180 * math.pi, 0.0)))
ROT1 = math3d.matrix.make_rotation(ANI_START_ROT.up, math.pi / 90.0)
FINAL_WORLD_MAT = math3d.matrix()
FINAL_WORLD_MAT.do_scale(math3d.vector(1, 1, 1))
FINAL_WORLD_MAT.do_rotation(END_ROT_MAT)
FINAL_WORLD_MAT.do_translate(END_POS)
FINAL_WORLD_INVERSE_MAT = math3d.matrix(FINAL_WORLD_MAT)
FINAL_WORLD_INVERSE_MAT.inverse()
MAP_3D_ROTATE_X = 1
MAP_3D_ROTATE_Z = 2
MAX_X_DEGREE = -30
MIN_X_DEGREE = -75
MIN_MAP_AND_CAM_DISTANCE = 400
MAX_MAP_AND_CAM_DISTANCE = 600

def trans_world_pos_to_3dmap_pos(pos):
    if not pos:
        return None
    else:
        return math3d.vector(pos.x / 100, 0, pos.z / 100)


def trans_3dmap_pos_to_world_pos(pos):
    if not pos:
        return None
    else:
        return math3d.vector(pos.x * 100.0, 0, pos.z * 100.0)
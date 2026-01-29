# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/const/common_const.py
from __future__ import absolute_import
import game3d
import math3d
VEC3D_UP = math3d.vector(0, 1, 0)
VEC3D_FORWARD = math3d.vector(0, 0, 1)
VEC3D_RIGHT = math3d.vector(1, 0, 0)
VEC3D_ZERO = math3d.vector(0, 0, 0)
VEC3D_TEMP = math3d.vector(0, 0, 0)
WINDOW_WIDTH, WINDOW_HEIGHT, _, _, _ = game3d.get_window_size()
ENABLE_PRELOAD_SHADER = True
SCENE_BG_PIC_MAX_RATIO = 19.0 / 9
FORCE_DELTA_TIME = 1.0 / 17.0
FORCE_DELTA_TIME_MS = 1000.0 / 17.0
LOGIN_BK_VIDEO_NAME = 'video/8002_ss.mp4'
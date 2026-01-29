# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/angle_utils.py
from __future__ import absolute_import
from math import pi, fabs
CIRCLE_ANGLE = pi * 2

def get_angle_difference(src_angle, target_angle):
    angle = fabs(target_angle - src_angle)
    larger_than_pi = angle > pi
    if larger_than_pi:
        angle = CIRCLE_ANGLE - angle
    if angle == 0:
        symbol = 0
    elif int(target_angle > src_angle) ^ int(larger_than_pi):
        symbol = 1
    else:
        symbol = -1
    return (angle, symbol)
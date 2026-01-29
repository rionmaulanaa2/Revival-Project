# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/action_utils.py
from __future__ import absolute_import

def linear_inter(x_val, min_val, max_val, x0=0, x1=1):
    return (x_val - x0) / (x1 - x0) * (max_val - min_val) + min_val


def bezier_action_helper(fly_t, start_pos, end_pos, normalized_p1=(0.04, 0.38), normalized_p2=(0.52, 0.94)):
    import cc
    control_p1_x = linear_inter(normalized_p1[0], end_pos.x, start_pos.x)
    control_p1_y = linear_inter(normalized_p1[1], end_pos.y, start_pos.y)
    control_p2_x = linear_inter(normalized_p2[0], end_pos.x, start_pos.x)
    control_p2_y = linear_inter(normalized_p2[1], end_pos.y, start_pos.y)
    control_p1 = (control_p1_x, control_p1_y)
    control_p2 = (control_p2_x, control_p2_y)
    if end_pos.x < start_pos.x:
        act = cc.BezierTo.create(fly_t, ((end_pos.x, end_pos.y), control_p2, control_p1))
    else:
        act = cc.BezierTo.create(fly_t, ((end_pos.x, end_pos.y), control_p1, control_p2))
    return act
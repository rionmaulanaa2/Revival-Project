# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rocker_utils.py
from __future__ import absolute_import

def modify_rotate_dist_by_sensitivity(sst_settings, x_delta, y_delta, pos, rocker_center, base_val=None):
    from logic.gcommon.common_const import ui_operation_const as uoc
    settings = sst_settings
    x_scale = settings[uoc.SST_IDX_RIGHT] if pos.x >= rocker_center.x else settings[uoc.SST_IDX_LEFT]
    if base_val is None:
        base_val = settings[uoc.SST_IDX_BASE]
    x_delta *= base_val * x_scale
    y_scale = settings[uoc.SST_IDX_UP] if pos.y >= rocker_center.y else settings[uoc.SST_IDX_DOWN]
    y_delta *= base_val * y_scale
    return (
     x_delta, y_delta)


def set_rocker_center_pos(w_move_pos, w_center_pos, move_node, radius):
    import math3d
    move_vec = math3d.vector2(w_move_pos.x - w_center_pos.x, w_move_pos.y - w_center_pos.y)
    move_vec_length = move_vec.length
    if move_vec_length > radius:
        move_vec = move_vec * (radius / move_vec_length)
    spawn_pt = move_node.getParent().convertToNodeSpace(w_center_pos)
    rocker_pos = math3d.vector2(spawn_pt.x, spawn_pt.y) + move_vec
    center_node_at_point(move_node, rocker_pos.x, rocker_pos.y)


def center_node_at_point(move_node, lpos_x, lpos_y):
    anchor_point = move_node.getAnchorPoint()
    size = move_node.getContentSize()
    scale = move_node.getScale()
    x_offset = (anchor_point.x - 0.5) * size.width * scale
    y_offset = (anchor_point.y - 0.5) * size.height * scale
    move_node.SetPosition(lpos_x + x_offset, lpos_y + y_offset)
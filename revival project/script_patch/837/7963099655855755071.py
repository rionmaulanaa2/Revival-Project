# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/dy_box_proto.py
from __future__ import absolute_import

def on_dy_box_static_transform(synchronizer, move_id, lst_transform_info):
    synchronizer.send_event('E_DYBOX_ON_STATIC_TRANSFORM_SYNC', move_id, lst_transform_info)


def add_breakable(synchronizer, break_id, params):
    owner = synchronizer.unit_obj.get_owner()
    if owner:
        owner.break_models(break_id, params)


def debug_add_collision(synchronizer, col_type, pos, size, matrix):
    from logic.gcommon.common_utils import matrix_utils
    import collision
    import math3d
    pos = math3d.vector(*pos)
    size = math3d.vector(*size)
    rot = matrix_utils.create_matrix_from_tuple(matrix)
    col = collision.col_object(col_type, size, 32768, 32768)
    col.position = pos
    col.rotation_matrix = rot
    synchronizer.scene.scene_col.add_object(col)


def record_break_hit_item(synchronizer, hit_item):
    owner = synchronizer.unit_obj.get_owner()
    if owner:
        owner.logic.send_event('E_RECORD_HP_BREAK_HIT_ITEM', hit_item)
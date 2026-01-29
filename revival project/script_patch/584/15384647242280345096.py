# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoneyBoxCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import collision
from logic.gcommon.common_const import battle_const as b_const

class ComMoneyboxCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'CRYSTAL_STAGE_CHANGE_FOR_COL': 'on_crystal_stage_change'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoneyboxCollision, self).init_from_dict(unit_obj, bdict)
        self.need_cover = bdict.get('need_cover')

    def _on_model_loaded(self, model, *args):
        if self.need_cover:
            cylinder_size = math3d.vector(b_const.CRYSTAL_COVER_R * 0.7, b_const.CRYSTAL_HEIGHT * 0.5, 0)
            self.col = collision.col_object(collision.CYLINDER, cylinder_size)
            offset_vec = math3d.vector(0, b_const.CRYSTAL_HEIGHT * 0.5, 0)
        else:
            self.col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
            offset_vec = math3d.vector(0, 0, 0)
        self.scene.scene_col.add_object(self.col)
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_AUTO_AIM & ~collision_const.GROUP_MECHA_BALL | collision_const.GROUP_CHARACTER_INCLUDE
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM | collision_const.GROUP_CHARACTER_INCLUDE
        self.col.position = model.world_position + offset_vec
        self.col.rotation_matrix = model.rotation_matrix
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)

    def on_crystal_stage_change(self, new_stage):
        model = self.ev_g_model()
        if not model:
            return
        if self.need_cover:
            offset_vec = math3d.vector(0, b_const.CRYSTAL_HEIGHT * 0.5, 0)
        else:
            offset_vec = math3d.vector(0, 0, 0)
        self.col.position = model.world_position + offset_vec
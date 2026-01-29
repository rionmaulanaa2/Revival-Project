# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCrystalCoverCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import collision_const
import math3d
import collision
from logic.gcommon.common_const import battle_const as b_const
from logic.gcommon.common_utils import battle_utils

class ComCrystalCoverCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'CRYSTAL_STAGE_CHANGE_FOR_COL': 'on_crystal_stage_change'
       })

    def __init__(self):
        super(ComCrystalCoverCollision, self).__init__()
        self._extra_obj = []
        self._need_extra_col = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComCrystalCoverCollision, self).init_from_dict(unit_obj, bdict)
        self._need_extra_col = bdict.get('need_extra_col', False)

    def _on_model_loaded(self, model, *args):
        self.col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        self.col.mask = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.TERRAIN_MASK
        self.col.group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.REGION_SCENE_GROUP
        self.col.position = model.world_position
        self.col.rotation_matrix = model.world_rotation_matrix
        self.scene.scene_col.add_object(self.col)
        global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
        if not self._need_extra_col:
            return
        col_position = model.world_position + math3d.vector(0, b_const.CRYSTAL_COVER_H * 0.5 * model.scale.y, 0)
        rotation_matrix = model.world_rotation_matrix
        col_sizes = battle_utils.get_crystal_cover_col_sizes((model.scale.x, model.scale.y, model.scale.z))
        for col_size in col_sizes:
            extra_col = collision.col_object(collision.BOX, col_size, collision_const.REGION_SCENE_GROUP, collision_const.REGION_SCENE_GROUP)
            self._extra_obj.append(extra_col)

        col_offsets = battle_utils.get_crystal_cover_col_offsets((model.scale.x, model.scale.y, model.scale.z))
        for idx, col_offset in enumerate(col_offsets):
            col_pos = col_offset * rotation_matrix + col_position
            self._extra_obj[idx].position = col_pos

        for idx, col_yaw in enumerate(b_const.CRYSTAL_COVER_EXTRA_COL_YAW_LIST):
            if col_yaw:
                self._extra_obj[idx].rotation_matrix = rotation_matrix * math3d.matrix.make_rotation_y(col_yaw)
            else:
                self._extra_obj[idx].rotation_matrix = rotation_matrix

        for extra_col in self._extra_obj:
            self.scene.scene_col.add_object(extra_col)

    def on_crystal_stage_change(self, new_stage):
        model = self.ev_g_model()
        if not model:
            return
        self.col.position = model.world_position
        self.col.rotation_matrix = model.world_rotation_matrix
        if not self._need_extra_col:
            return
        col_position = model.world_position + math3d.vector(0, b_const.CRYSTAL_COVER_H * 0.5 * model.scale.y, 0)
        rotation_matrix = model.world_rotation_matrix
        col_offsets = battle_utils.get_crystal_cover_col_offsets((model.scale.x, model.scale.y, model.scale.z))
        for idx, col_offset in enumerate(col_offsets):
            col_pos = col_offset * rotation_matrix + col_position
            self._extra_obj[idx].position = col_pos

        for idx, col_yaw in enumerate(b_const.CRYSTAL_COVER_EXTRA_COL_YAW_LIST):
            if col_yaw:
                self._extra_obj[idx].rotation_matrix = rotation_matrix * math3d.matrix.make_rotation_y(col_yaw)
            else:
                self._extra_obj[idx].rotation_matrix = rotation_matrix

    def destroy(self):
        super(ComCrystalCoverCollision, self).destroy()
        if self._extra_obj:
            for extra_col in self._extra_obj:
                self.scene.scene_col.remove_object(extra_col)

            self._extra_obj = []
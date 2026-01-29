# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNBombDeviceCollision.py
from __future__ import absolute_import
from .ComBuildingCollision import ComBuildingCollision
from logic.gcommon.common_const.collision_const import TERRAIN_MASK, GLASS_GROUP
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision
import math3d
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_GRENADE, GROUP_CHARACTER_INCLUDE, GROUP_STATIC_SHOOTUNIT, GROUP_MECHA_BALL

class ComNBombDeviceCollision(ComBuildingCollision):

    def _on_model_loaded(self, model):
        if not self.scene:
            return
        else:
            box = model.bounding_box
            pos = model.world_position
            scale = model.world_scale
            rot = model.world_rotation_matrix
            center = model.center
            self.offset = math3d.vector(0, -box.y - center.y, 0)
            collision_info = self.ev_g_collision_info()
            if collision_info:
                scale = collision_info.get('scale', scale)
                rot = collision_info.get('rotation', rot)
                self.offset = collision_info.get('offset', self.offset)
                self.offset = self._get_offset_by_str(self.offset, box) if type(self.offset) is str else self.offset
                custom_box = collision_info.get('custom_box', None)
                if custom_box:
                    box = math3d.vector(custom_box[0] * NEOX_UNIT_SCALE, custom_box[1] * NEOX_UNIT_SCALE, custom_box[2] * NEOX_UNIT_SCALE)
            self.col = collision.col_object(collision.CAPSULE, box * scale)
            self.col.rotation_matrix = rot
            self.col.mask = GROUP_STATIC_SHOOTUNIT | GROUP_CHARACTER_INCLUDE | GROUP_GRENADE | GROUP_MECHA_BALL
            self.col.group = GLASS_GROUP
            self.col.model_col_name = model.name
            self.scene.scene_col.add_object(self.col)
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
            target_pos = pos + center
            start = target_pos + self.offset * NEOX_UNIT_SCALE
            end = target_pos
            self.col.position = start
            self._raise_up(start, end, 30)
            return
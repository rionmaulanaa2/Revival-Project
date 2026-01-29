# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartItemAdaptiveLod.py
from __future__ import absolute_import
import six
from . import ScenePart
import math3d
import math
import collision
from logic.gcommon.common_const import collision_const
from logic.client.const.camera_const import ADAPTIVE_Z_DIST
import game3d
from logic.gcommon.const import NEOX_UNIT_SCALE
LOD_NORMAL = (
 15 * NEOX_UNIT_SCALE, 15 * NEOX_UNIT_SCALE)
LOD_FAR = (50 * NEOX_UNIT_SCALE, 50 * NEOX_UNIT_SCALE)
OBJS_PER_FRAME = 2

class PartItemAdaptiveLod(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartItemAdaptiveLod, self).__init__(scene, name, True)
        self._house_coms = []
        self._house_next = 0
        self._house_map = {}

    def on_update(self, dt):
        house_coms = self._house_coms
        if not self._house_coms:
            return
        scn_col = self.scene().scene_col
        if not scn_col:
            return
        cam_pos = self.scene().active_camera.world_position
        if self._house_next >= len(house_coms):
            self._house_next = 0
        com = house_coms[self._house_next]
        item_checked = 0
        for entity_id, model in six.iteritems(com.house_pick_detail_map):
            if com.house_obj_check_map.get(entity_id, False):
                continue
            com.house_obj_check_map[entity_id] = True
            if entity_id not in com.house_pick_obj_map or not com.house_pick_obj_map[entity_id].is_visible_in_this_frame():
                item_checked += 0.5
            else:
                result = scn_col.hit_by_ray(cam_pos, model.world_position, 0, collision_const.REGION_SCENE_GROUP, 0, collision.INEQUAL_FILTER)
                visible = not result[0]
                model.lod_config = LOD_FAR if visible else LOD_NORMAL
                item_checked += 1
            if item_checked >= OBJS_PER_FRAME:
                break

        if item_checked < OBJS_PER_FRAME:
            com.house_obj_check_map = {}
            self._house_next += 1

    def add(self, house):
        if house not in self._house_map:
            self._house_map[house] = len(self._house_coms)
            self._house_coms.append(house)

    def remove(self, house):
        if house in self._house_map:
            index = self._house_map[house]
            last = self._house_coms[-1]
            self._house_coms[index] = last
            self._house_map[last] = index
            del self._house_coms[-1]
            del self._house_map[house]
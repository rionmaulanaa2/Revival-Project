# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWaterMechaTrans.py
from __future__ import absolute_import
from .ComWater import ComWater
from .ComWaterMecha import ComWaterMecha
from logic.gcommon.common_const import water_const, scene_const, collision_const, mecha_const
import math3d
import collision

class ComWaterMechaTrans(ComWaterMecha):
    BIND_EVENT = ComWaterMecha.BIND_EVENT.copy()
    BIND_EVENT.update({'E_TRANSFORMING_TO_VEHICLE_IN_WATER': 'start_tranfroming_to_vehicle_in_water',
       'E_FORCE_REFRESH': 'force_refresh'
       })

    def __init__(self):
        super(ComWaterMechaTrans, self).__init__()
        self.force_check_diving = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComWaterMechaTrans, self).init_from_dict(unit_obj, bdict)

    def change_status(self, last_status, water_height=None, water_depth=0):
        super(ComWaterMechaTrans, self).change_status(last_status, water_height)
        self.send_event('E_CHANGE_WATER_STATUS', last_status)

    def start_tranfroming_to_vehicle_in_water(self, *args):
        self.leave_diving()

    def check_material_index(self, material_index):
        pattern = self.ev_g_pattern()
        if not pattern or pattern == mecha_const.MECHA_PATTERN_NORMAL:
            return material_index
        else:
            if material_index == scene_const.MTL_DEEP_WATER or material_index == scene_const.MTL_WATER:
                scn = self.scene
                if not scn:
                    return scene_const.MTL_SAND
                pos = self.get_pos()
                if not pos:
                    return scene_const.MTL_SAND
                p1 = pos + math3d.vector(0, 520, 0)
                p2 = pos + math3d.vector(0, -5, 0)
                if p1.y <= ComWater.DEFAULT_WATER_HEIGHT:
                    p1.y = ComWater.DEFAULT_WATER_HEIGHT + 5
                result = scn.scene_col.hit_by_ray(p1, p2, 0, collision_const.WATER_GROUP, collision_const.WATER_MASK, collision.EQUAL_FILTER)
                if not result[0]:
                    return scene_const.MTL_SAND
            return material_index

    def get_last_material_index(self):
        return self.last_material

    def _set_water_diff_height(self, diff_height):
        change = diff_height != self.water_diff
        self.water_diff = diff_height
        if change or self.force_check_diving:
            self.on_water_depth_change(diff_height)

    def on_water_depth_change(self, diff_height):
        if diff_height > water_const.H_WATER_MECHATRANS_DIVING:
            if self.diving is not True:
                self.set_diving(True)
                self.enter_diving()
        elif self.diving is not False:
            self.set_diving(False)
            self.leave_diving()

    def force_refresh(self, flag):
        if flag:
            self.set_diving(False)
        self.force_check_diving = flag
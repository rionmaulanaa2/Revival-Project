# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAIWater.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import scene_const, water_const
from logic.gcommon.cdata.status_config import ST_SWIM

class ComAIWater(UnitCom):
    BIND_EVENT = {}

    def __init__(self):
        super(ComAIWater, self).__init__()
        self.need_update = False
        self._is_robot = False
        self.is_in_deep_water = False

    def init_from_dict(self, unit_obj, bdict):
        super(ComAIWater, self).init_from_dict(unit_obj, bdict)
        self._is_robot = bool(bdict.get('is_robot', False))
        if self._is_robot:
            self.need_update = True

    def tick(self, dt):
        pos = self.ev_g_position()
        scn = self.scene
        if pos and scn:
            if pos.y > 100:
                return
            material_index = scn.get_scene_info_2d(pos.x, pos.z)
            if material_index == scene_const.MTL_DEEP_WATER:
                if not self.is_in_deep_water:
                    self.send_event('E_WATER_EVENT', water_const.WATER_DEEP_LEVEL, 0)
                    if self.ev_g_get_state(ST_SWIM):
                        self.is_in_deep_water = True
            elif self.is_in_deep_water:
                self.is_in_deep_water = False
                self.send_event('E_WATER_EVENT', water_const.WATER_NONE, 0)
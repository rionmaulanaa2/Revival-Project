# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_granbelm/ComGranbelmPortalCollision.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import collision
import math3d
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_AUTO_AIM, BUILDING_GROUP, GROUP_CAMERA_COLL
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComGranbelmPortalCollision(UnitCom):
    BIND_EVENT = {'E_ON_PORTAL_SFX_LOADED': '_on_sfx_loaded'
       }
    COL_SIZE = (4, 2)

    def __init__(self):
        super(ComGranbelmPortalCollision, self).__init__()
        self._col = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGranbelmPortalCollision, self).init_from_dict(unit_obj, bdict)

    def _on_sfx_loaded(self, pos):
        if not self.scene:
            return
        size = math3d.vector(self.COL_SIZE[0] * NEOX_UNIT_SCALE, self.COL_SIZE[1] * NEOX_UNIT_SCALE, 1)
        self._col = collision.col_object(collision.CYLINDER, size)
        self._col.position = pos
        self._col.car_undrivable = True
        self._col.is_force_callback = True
        self.send_event('E_PORTAL_COL_LOADED', self._col, self.COL_SIZE)

    def _on_trigger_callback(self, *args):
        own_obj, other_obj, flag = args

    def destroy(self):
        if self._col:
            self.scene.scene_col.remove_object(self._col)
            self._col = None
        super(ComGranbelmPortalCollision, self).destroy()
        return
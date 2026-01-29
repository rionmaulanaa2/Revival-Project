# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEShopCollision.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import collision
import math3d
from logic.gcommon.common_const.collision_const import TERRAIN_GROUP, TERRAIN_MASK

class ComPVEShopCollision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'init_col'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEShopCollision, self).init_from_dict(unit_obj, bdict)
        self.col = None
        return

    def init_col(self, pos, scale, col_info):
        col_size = math3d.vector(col_info[0], col_info[1], col_info[2]) * scale
        y_offset = col_info[3] * scale
        self.col = collision.col_object(collision.BOX, col_size, 0, 0, 0)
        self.col.group = TERRAIN_GROUP
        self.col.mask = TERRAIN_MASK
        pos.y += y_offset
        self.col.position = pos
        self.scene.scene_col.add_object(self.col)
        self.send_event('E_COL_LOADED', pos)

    def destroy(self):
        self.col and self.scene.scene_col.remove_object(self.col)
        self.col = None
        super(ComPVEShopCollision, self).destroy()
        return
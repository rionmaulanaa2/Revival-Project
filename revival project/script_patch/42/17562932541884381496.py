# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrackMissileCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
import collision
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const

class ComTrackMissileCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'G_COL_SIZE': 'get_col_size'
       })
    COL_SIZE = (2.1, 2.7, 2.1)
    COL_RADIUS = 6.8
    BIND_BONE = 'gj_1066'

    def _on_model_loaded(self, model, *args):
        self.col = collision.col_object(collision.SPHERE, math3d.vector(self.COL_RADIUS * NEOX_UNIT_SCALE, 0, 0), 0, 0, 0)
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_AUTO_AIM & ~collision_const.GROUP_MECHA_BALL
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        self.send_event('E_COL_LOADED', self.col)

    def get_col_size(self):
        return self.COL_RADIUS

    def destroy(self):
        if self.col:
            global_data.emgr.del_ignore_col_ids_event.emit(self.col.cid)
        super(ComTrackMissileCollision, self).destroy()
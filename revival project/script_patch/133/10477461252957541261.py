# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTriggerGrenadeCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import collision

class ComTriggerGrenadeCollision(ComCommonShootCollision):

    def init_from_dict(self, unit_obj, bdict):
        super(ComTriggerGrenadeCollision, self).init_from_dict(unit_obj, bdict)
        self._dead = False

    def _on_model_loaded(self, model):
        if self._dead:
            return
        self.col = collision.col_object(collision.BOX, math3d.vector(0.7 * NEOX_UNIT_SCALE, 0.9 * NEOX_UNIT_SCALE, 0.7 * NEOX_UNIT_SCALE), 0, 0, 0)
        self.scene.scene_col.add_object(self.col)
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_AUTO_AIM & ~collision_const.GROUP_MECHA_BALL
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        self.col.position = model.world_position
        self.col.rotation_matrix = model.rotation_matrix
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        global_data.emgr.add_ignore_col_ids_event.emit(self.col.cid)
        self.col.bind_sync_visible_obj(model, collision.DIRECTLY_SYNC, 1, False)

    def destroy(self):
        if self.col:
            global_data.emgr.del_ignore_col_ids_event.emit(self.col.cid)
        super(ComTriggerGrenadeCollision, self).destroy()
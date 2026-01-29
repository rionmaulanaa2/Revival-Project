# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSkillWallCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import collision
import math3d
import world
import math

class ComSkillWallCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def _on_model_loaded(self, hit_col_path, *args, **kwargs):
        model = world.model(hit_col_path, None)
        model.scale = math3d.vector(4.8, 4.8, 4.8)
        self.col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        self.col.position = self.sd.ref_pos
        self.col.rotation_matrix = self.sd.ref_rotation_matrix * math3d.matrix.make_rotation_y(math.radians(-90))
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_SHOOTUNIT
        self.col.group = collision_const.GROUP_SHOOTUNIT
        self.scene.scene_col.add_object(self.col)
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        return

    def on_is_pierced(self):
        return False
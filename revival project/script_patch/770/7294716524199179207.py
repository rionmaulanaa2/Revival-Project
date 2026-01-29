# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMeshShootCollision.py
from __future__ import absolute_import
import collision
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import HIT_PART_BODY

class ComMeshShootCollision(ComCommonShootCollision):

    def _on_model_loaded(self, model, custom_pos=None, custom_col_group=None):
        self.col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        self.scene.scene_col.add_object(self.col)
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_AUTO_AIM & ~collision_const.GROUP_MECHA_BALL | collision_const.GROUP_CHARACTER_INCLUDE
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM | collision_const.GROUP_CHARACTER_INCLUDE
        self.col.position = model.position
        self.col.rotation_matrix = model.rotation_matrix
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        return HIT_PART_BODY
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOilBottleCollision.py
from __future__ import absolute_import
import math3d
import collision
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const import building_const

class ComOilBottleCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'E_OIL_BOTTLE_ON_FIRE': 'remove_bottle_collision'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComOilBottleCollision, self).init_from_dict(unit_obj, bdict)
        self._hitable = bdict.get('hitable', False)
        self.state = bdict.get('building_state', building_const.B_OIL_BOTTLE_STATE_BOTTLE)
        self.grow_time = 0.5
        self.grow_elapsed = 0
        self.model = None
        return

    def _on_model_loaded(self, m, *args):
        if self.state == building_const.B_OIL_BOTTLE_STATE_FIRE:
            return
        self.col = self.create_bottle_collision(m)
        self.col.position = m.world_position
        self.col.rotation_matrix = m.rotation_matrix
        scn = self.scene
        scn.scene_col.add_object(self.col)
        if self._hitable:
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
            global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)
        if self.non_explosion_dis:
            global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
        self.send_event('E_COLLSION_LOADED', m, self.col)

    def create_bottle_collision(self, model):
        model.scale = math3d.vector(2.0, 2.0, 2.0)
        col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        col.mask = GROUP_SHOOTUNIT | GROUP_GRENADE | GROUP_CHARACTER_INCLUDE
        col.group = GROUP_SHOOTUNIT | GROUP_CHARACTER_INCLUDE
        self.non_explosion_dis = True
        self.model = model
        self.need_update = True
        model.scale = math3d.vector(1.0, 1.0, 1.0)
        return col

    def remove_bottle_collision(self, *args):
        if self.col:
            self.scene.scene_col.remove_object(self.col)
            global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)
            self.col = None
        return

    def _destroy_shoot_collision(self):
        self.need_update = False
        self.model = None
        if self.col:
            global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)
        super(ComOilBottleCollision, self)._destroy_shoot_collision()
        return

    def tick(self, dt):
        self.grow_elapsed += dt
        scale = 1.0 + self.grow_elapsed / self.grow_time
        if self.grow_elapsed >= self.grow_time:
            self.need_update = False
            scale = 2.0
        if self.model and self.model.valid:
            self.model.scale = math3d.vector(scale, scale, scale)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDeathDoorCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision

class ComDeathDoorCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'G_IS_WEAK_DOOR': 'is_weak_door'
       })

    def init_from_dict(self, unit_obj, bdict):
        self.npc_id = bdict.get('npc_id')
        super(ComDeathDoorCollision, self).init_from_dict(unit_obj, bdict)

    def _on_model_loaded(self, m):
        self.col = global_data.death_battle_door_col.get_door_col(self.npc_id)
        if self.col is None:
            return
        else:
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
            global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
            self.send_event('E_COLLSION_LOADED', m, self.col)
            return

    def _destroy_shoot_collision(self):
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            if self.col.cid in global_data.war_non_explosion_dis_objs:
                global_data.war_non_explosion_dis_objs.pop(self.col.cid)
            self.col = None
        return

    def on_is_pierced(self):
        return False

    def is_weak_door(self):
        return global_data.death_battle_door_col.is_weak_door(self.npc_id)
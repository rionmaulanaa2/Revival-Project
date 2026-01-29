# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBeacon8031Collision.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import collision_const
import collision
import math3d
COL_SIZE = math3d.vector(8.453705, 15.08432, 2.894531)
POSITION_OFFSET = math3d.vector(0, 17, 0)

class ComBeacon8031Collision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_DEATH': ('die', 10),
       'G_HUMAN_COL_ID': 'get_col_id'
       }
    BIND_BONE_NAME = 'bon_aile01'

    def init_from_dict(self, unit_obj, bdict):
        super(ComBeacon8031Collision, self).init_from_dict(unit_obj, bdict)
        self.owner_id = bdict.get('owner_eid', None)
        self.yaw = bdict.get('yaw', 0)
        self.col = None
        return

    def destroy(self):
        super(ComBeacon8031Collision, self).destroy()
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def on_model_loaded(self, model):
        self.col = collision.col_object(collision.BOX, COL_SIZE * model.scale, collision_const.GROUP_GRENADE | collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision_const.GROUP_DYNAMIC_SHOOTUNIT, 0, False)
        if not (global_data.mecha and global_data.mecha.id == self.owner_id):
            self.col.mask |= collision_const.GROUP_CHARACTER_INCLUDE
            self.col.group |= collision_const.GROUP_CHARACTER_INCLUDE
        self.scene.scene_col.add_object(self.col)
        self.col.position = model.position
        self.col.position += POSITION_OFFSET * model.scale.y
        self.col.rotation_matrix = math3d.matrix.make_rotation_y(self.yaw)
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)

    def get_col_id(self):
        if self.col:
            return [self.col.cid]
        return []
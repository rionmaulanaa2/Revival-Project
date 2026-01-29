# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTVMissileLauncherCollision.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
import collision
import world

class ComTVMissileLauncherCollision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'G_CHECK_ENTER_CONSOLOE_ZONE': 'check_enter_zone',
       'E_DEATH': ('die', 10),
       'G_HUMAN_COL_ID': 'get_col_id'
       }
    BIND_BONE_NAME = 'biped_tvmissile_1068_root'
    MODEL_PATH = 'character/weapons/1068_tvmissile/1068/l3.gim'

    def init_from_dict(self, unit_obj, bdict):
        super(ComTVMissileLauncherCollision, self).init_from_dict(unit_obj, bdict)
        self.col = collision.col_object(collision.MESH, world.model(self.MODEL_PATH, None), collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, 0, True)
        self.col.mask |= collision_const.GROUP_GRENADE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
        self.col.group |= collision_const.GROUP_DYNAMIC_SHOOTUNIT
        return

    def destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        super(ComTVMissileLauncherCollision, self).destroy()
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.col = None
        return

    def on_model_loaded(self, model):
        model.bind_col_obj(self.col, self.BIND_BONE_NAME)
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())

    def check_enter_zone(self, pos):
        if self.sd.ref_controller_id:
            return (False, None)
        else:
            model = self.ev_g_model()
            if model:
                dist = (model.position - pos).length
                if dist < 2 * NEOX_UNIT_SCALE:
                    return (True, dist)
            return (
             False, None)

    def die(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)

    def get_col_id(self):
        return [
         self.col.cid]
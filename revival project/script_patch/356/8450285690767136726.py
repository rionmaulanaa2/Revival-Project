# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComHandyShieldCollision.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import collision
import math3d
import world
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_MECHA_BALL
from logic.gcommon.common_const.mecha_const import HANDY_SHIELD_BONE, HANDY_SHIELD_SOCKET
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.mecha_const import DEFEND_ON, DEFEND_OFF

class ComHandyShieldCollision(UnitCom):
    BIND_EVENT = {'E_ON_LOAD_SHIELD_MODEL': 'on_load_shield_model',
       'E_SET_SHIELD_SIZE_RATIO': 'on_set_shield',
       'E_ADD_HS_COL': 'on_add',
       'E_REMOVE_HS_COL': 'on_remove'
       }

    def __init__(self):
        super(ComHandyShieldCollision, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHandyShieldCollision, self).init_from_dict(unit_obj, bdict)
        self.init_params(bdict)

    def init_params(self, bdict):
        self.mecha_id = bdict['mecha_id']
        self.col = None
        self.mecha_model = None
        self.socket_name = HANDY_SHIELD_SOCKET
        self.offset = (0, 0)
        self.X = 1.1 * NEOX_UNIT_SCALE
        self.Y = 4.0 * NEOX_UNIT_SCALE
        self.Z = 3.5 * NEOX_UNIT_SCALE
        self.is_pve = global_data.game_mode.is_pve()
        self.size_up_factor = 1.0
        return

    def on_set_shield(self, factor):
        self.size_up_factor = 2.0

    def on_load_shield_model(self, model, mecha_model, size=None, socket_name=None, offset=None):
        self.destroy_col()
        if type(size) in (tuple, list):
            self.X, self.Y, self.Z = size
            self.X *= NEOX_UNIT_SCALE * self.size_up_factor
            self.Y *= NEOX_UNIT_SCALE * self.size_up_factor
            self.Z *= NEOX_UNIT_SCALE
        if socket_name is not None:
            self.socket_name = socket_name
        if offset is not None:
            self.offset = offset
        size = math3d.vector(self.X, self.Y, self.Z)
        col = collision.col_object(collision.BOX, size, 0, 0, False)
        col.mask = GROUP_SHOOTUNIT | GROUP_GRENADE & ~GROUP_MECHA_BALL
        col.group = GROUP_SHOOTUNIT
        col.is_force_callback = True
        col.car_undrivable = True
        self.col = col
        self.send_event('E_ON_LOAD_SHIELD_COL', model, self.col)
        self.mecha_model = mecha_model
        state = self.ev_g_handy_shield_state()
        if state == DEFEND_ON:
            self.on_add()
        return

    def on_add(self, *args):
        if not self.is_pve and self.ev_g_is_avatar():
            return
        if not self.col:
            return
        self.scene.scene_col.add_object(self.col)
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        self.send_event('E_ADD_HANDY_SHIELD_COL', self.col)
        self.need_update = True

    def on_remove(self):
        if not self.is_pve and self.ev_g_is_avatar():
            return
        self.need_update = False
        if self.col:
            self.scene.scene_col.remove_object(self.col)
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.send_event('E_REMOVE_HANDY_SHIELD_COL')

    def tick(self, dt):
        if self.mecha_model:
            m = self.mecha_model().get_socket_matrix(self.socket_name, 1)
            self.col.position = m.translation + m.forward * self.offset[0] + m.up * self.offset[1]
            self.col.rotation_matrix = m.rotation

    def destroy_col(self):
        if self.col:
            self.scene.scene_col.remove_object(self.col)
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.col = None
        return

    def destroy(self):
        self.need_update = False
        self.destroy_col()
        super(ComHandyShieldCollision, self).destroy()
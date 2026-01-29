# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComLightShieldCollision.py
from __future__ import absolute_import
import math3d
import collision
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_MECHA_BALL, GROUP_CHARACTER_EXCLUDE
from common.cfg import confmgr
from common.framework import Functor
from logic.gcommon.common_const.buff_const import BUFF_ID_8008_SHIELD_CONTACT_ENABLE

class ComLightShieldCollision(ComCommonShootCollision):

    def init_from_dict(self, unit_obj, bdict):
        super(ComLightShieldCollision, self).init_from_dict(unit_obj, bdict)
        self._hitable = bdict.get('hitable', False)
        self.item_id = bdict.get('building_no')
        self.conf = confmgr.get('c_building_res', str(self.item_id))
        params = self.conf.get('ExtInfo', {})
        self.extra_scale = params.get('extra_scale', 1.0)
        self.breakthrough_size_up_factor = bdict.get('size_up_factor', 0)
        self.owner_id = bdict['owner_id']

    def _on_model_loaded(self, m):
        self.col, start, end = self.create_light_shield(m)
        self.col.position = end
        self.col.rotation_matrix = m.rotation_matrix
        scn = self.scene
        scn.scene_col.add_object(self.col)
        if self._hitable:
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        if self.non_explosion_dis:
            global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
        self.send_event('E_COLLSION_LOADED', m, self.col)

    def create_light_shield(self, model):
        model.scale = math3d.vector(15, 15, 15) * 4
        model.scale *= self.extra_scale
        model.scale *= 1 + self.breakthrough_size_up_factor
        col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        start, end = model.world_position, model.world_position
        col.mask = GROUP_SHOOTUNIT | GROUP_GRENADE & ~GROUP_MECHA_BALL
        col.group = GROUP_SHOOTUNIT
        col.is_force_callback = True
        col.car_undrivable = True
        player_mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
        if player_mecha and player_mecha.logic and self.owner_id == player_mecha.id and player_mecha.logic.ev_g_has_buff_by_id(BUFF_ID_8008_SHIELD_CONTACT_ENABLE):
            col.set_contact_callback(Functor(self.on_contact))
            col.set_notify_contact(True)
        self.non_explosion_dis = True
        self.scene.scene_col.add_object(col)
        return (
         col, start, end)

    def on_contact(self, *args):
        if len(args) == 3:
            cobj, point, normal = args
        else:
            my_obj, cobj, touch, hit_info = args
            if not touch:
                return
        start_pos = cobj.position - cobj.rotation_matrix.forward * 3 * 13.0
        end_pos = cobj.position + cobj.rotation_matrix.forward * 2 * 13.0
        result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, -1, collision.INCLUDE_FILTER, True)
        if result[0]:
            for cobj in result[1]:
                mecha_logic_list = global_data.emgr.scene_find_unit_event.emit(cobj[4].cid)
                if mecha_logic_list:
                    hittter_mecha_logic = mecha_logic_list[0]
                    if not hittter_mecha_logic:
                        return
                    hitter_id = hittter_mecha_logic.id
                    player_mecha = global_data.player.logic.ev_g_ctrl_mecha_obj()
                    if player_mecha and player_mecha.logic:
                        player_mecha.logic.send_event('E_CALL_SYNC_METHOD', 'hit_8008_breakthrough_shield', (hitter_id,))
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBuildingCollision.py
from __future__ import absolute_import
import math3d
import collision
import world
from common.utils.timer import CLOCK
from logic.gcommon.const import NEOX_UNIT_SCALE
from .ComCommonShootCollision import ComCommonShootCollision
from logic.gcommon.common_const import building_const as b_const
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_AUTO_AIM, GROUP_GRENADE, GROUP_CHARACTER_INCLUDE, GROUP_SHOOTUNIT, GROUP_CAMERA_COLL
from mobile.common.EntityManager import EntityManager
from common.cfg import confmgr

class ComBuildingCollision(ComCommonShootCollision):

    def __init__(self):
        super(ComBuildingCollision, self).__init__()
        self.special_col_dict = {b_const.B_PHOTON_TOWER: self.create_photo_tower,
           b_const.B_PHOTON_TOWER_DEATH_MODE: self.create_photo_tower,
           b_const.B_LIGHT_SHIELD: self.create_light_shield
           }
        for building_no in b_const.B_BOUNCER_LIST:
            self.special_col_dict[building_no] = self.create_special_col

        self.timer_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBuildingCollision, self).init_from_dict(unit_obj, bdict)
        self._building_no = bdict.get('building_no', None)
        self._hitable = bdict.get('hitable', False)
        self._owner_id = bdict.get('owner_id', None)
        self._destruction_timer = None
        self._building_conf = confmgr.get('c_building_res', str(self._building_no))
        return

    def destroy(self):
        super(ComBuildingCollision, self).destroy()
        if self.timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.timer_id)
            self.timer_id = None
        if self._destruction_timer:
            global_data.game_mgr.unregister_logic_timer(self._destruction_timer)
            self._destruction_timer = None
        self.special_col_dict.clear()
        return

    def _on_model_loaded(self, m):
        start, end = (None, None)
        if self._building_no in self.special_col_dict:
            handler = self.special_col_dict[self._building_no]
            self.col, start, end = handler(m)
        else:
            self.col = collision.col_object(collision.MESH, m, 0, 0, 0, True)
            start, end = m.world_position, m.world_position
            start.y -= m.bounding_box.y * 2
            self.col.mask = GROUP_GRENADE | GROUP_AUTO_AIM | self.col.mask
            self.col.group = BUILDING_GROUP | GROUP_AUTO_AIM | self.col.group
        self.col.position = end
        self.col.rotation_matrix = m.rotation_matrix
        self._raise_up(start, end)
        scn = self.scene
        scn.scene_col.add_object(self.col)
        if self._hitable:
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        if self.non_explosion_dis:
            global_data.war_non_explosion_dis_objs[self.col.cid] = self.unit_obj.id
        self.send_event('E_COLLSION_LOADED', m, self.col)
        return None

    def _raise_up(self, start, end, tick_count=20):
        self.cnt = 0

        def _raise():
            if not self or not self.is_valid():
                return
            else:
                self.cnt += 1
                pos = math3d.vector(0, 0, 0)
                u = self.cnt * 1.0 / tick_count
                if u > 1.0:
                    u = 1.0
                    global_data.game_mgr.get_logic_timer().unregister(self.timer_id)
                    self.timer_id = None
                pos.intrp(start, end, u)
                if self.col:
                    self.col.position = pos
                return

        if self.timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.timer_id)
            self.timer_id = None
        self.timer_id = global_data.game_mgr.get_logic_timer().register(func=_raise, interval=0.03, times=-1, mode=CLOCK)
        return

    def create_light_shield(self, model):
        model.scale = math3d.vector(15, 15, 15) * 4
        col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        start, end = model.world_position, model.world_position
        col.mask = GROUP_SHOOTUNIT | GROUP_GRENADE
        col.group = GROUP_SHOOTUNIT
        col.is_force_callback = True
        col.car_undrivable = True
        self.non_explosion_dis = True
        return (
         col, start, end)

    def create_special_col(self, model):
        import collision
        r = model.bounding_box.z / 2
        col = collision.col_object(collision.SPHERE, math3d.vector(r, r, r), 0, 0, 0, True)
        col.mask = GROUP_GRENADE | GROUP_AUTO_AIM
        col.group = (BUILDING_GROUP | GROUP_AUTO_AIM) & ~GROUP_CAMERA_COLL
        start, end = model.world_position, model.world_position
        offset = model.bounding_box.y
        start.y -= offset * 1.8
        end.y -= offset * 1.8
        return (
         col, start, end)

    def create_photo_tower(self, model):
        ext_info = self._building_conf.get('ExtInfo')
        scale = ext_info.get('scale', 1)
        conf_size = ext_info.get('size', [3, 45, 3])
        tower_size = math3d.vector(*conf_size) * scale
        model.scale = math3d.vector(scale, scale, scale)
        if model and model.valid:
            scene = global_data.game_mgr.scene
            start_pos = model.world_position + math3d.vector(0, 5, 0)
            end_pos = model.world_position + math3d.vector(0, tower_size.y + 2, 0)
            result = scene.scene_col.hit_by_ray(start_pos, end_pos, 0, 0, 0, collision.EXCLUDE_FILTER, True)
            if result[0]:
                self._self_destruction()
        col_obj = collision.col_object(collision.CAPSULE, tower_size, 0, 0, 0, True)
        col_obj.disable_gravity(True)
        col_obj.ignore_collision = True
        col_obj.mask = GROUP_GRENADE | GROUP_CHARACTER_INCLUDE | GROUP_SHOOTUNIT
        col_obj.group = GROUP_SHOOTUNIT | GROUP_AUTO_AIM | GROUP_CHARACTER_INCLUDE
        start, end = model.world_position, model.world_position
        end.y += tower_size.y / 2 + 2
        start.y -= tower_size.y / 2
        return (
         col_obj, start, end)

    def _self_destruction(self):
        if self._owner_id is None:
            return
        else:
            parent = EntityManager.getentity(self._owner_id)
            if parent and parent.logic:
                parent.logic.send_event('E_CALL_SYNC_METHOD', 'disable_building', (self.unit_obj.id,), True)
            return
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComVehicleCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
import time
import weakref
import world
import math3d
from logic.gutils.scene_utils import is_break_obj
from logic.gcommon.common_const import scene_const
import logic.gcommon.common_const.collision_const as collision_const
from data.constant_break_data import data as constant_break_list
from logic.gutils.scene_utils import SNOW_SCENE_BOX_MODEL_ENT_MAP
from common.utils.sfxmgr import CREATE_SRC_SIMPLE

class ComVehicleCollision(ComObjCollision):
    CHECK_TIME_CD = 0.5
    BIND_EVENT = {'E_VECHICLE_LOADED': '_on_vehicle_load'
       }

    def __init__(self):
        super(ComVehicleCollision, self).__init__()
        self.col_id = None
        self.next_check_time = time.time()
        self.vehicle = None
        self.break_obj_list = []
        self.collision_sfx = None
        self.collision_sfx_last_time = 0
        self.collision_sound_time = time.time()
        self.last_vert_speed = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComVehicleCollision, self).init_from_dict(unit_obj, bdict)
        self.collision_sfx = constant_break_list.get(1, {}).get('cResFx', None)
        return

    def on_init_complete(self):
        vehicle = self.ev_g_vehicle()
        if vehicle:
            self._on_vehicle_load(vehicle)

    def _create_col_obj(self):
        pass

    def _on_vehicle_load(self, vehicle):
        self.col_id = vehicle.cid
        self.scene.scene_col.add_interest_id(self.col_id)
        vehicle.set_notify_contact(True)
        vehicle.set_contact_callback(self.on_contact)
        self.need_update = True
        self.vehicle = vehicle

    def destroy(self):
        vehicle = self.vehicle
        if vehicle:
            vehicle.set_contact_callback(None)
        self._col_obj = None
        self.col_id = None
        self.vehicle = None
        super(ComVehicleCollision, self).destroy()
        return

    def on_contact(self, *args):
        if not self.is_valid():
            return
        else:
            if not self.unit_obj:
                return
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            if cobj.group == collision_const.WATER_GROUP and cobj.mask == collision_const.WATER_MASK:
                self.send_event('E_PLAY_DROP_WATER', point, self.last_vert_speed)
            if self.collision_sfx and cobj and cobj.group in (scene_const.COL_METAL, scene_const.COL_STONE):
                now = time.time()
                if now - self.collision_sfx_last_time > collision_const.COLLISION_SFX_INTERVAL:
                    self.collision_sfx_last_time = now

                    def create_cb(sfx):
                        global_data.sfx_mgr.set_rotation_by_normal(sfx, normal)

                    global_data.sfx_mgr.create_sfx_in_scene(self.collision_sfx, point, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            model_col_name = getattr(cobj, 'model_col_name', None)
            if model_col_name and is_break_obj(model_col_name):
                break_entity_id = SNOW_SCENE_BOX_MODEL_ENT_MAP.get(str(cobj.model_col_name), None)
                break_item_info = {'model_col_name': cobj.model_col_name,'point': point,
                   'normal': normal,
                   'power': None,
                   'break_type': collision_const.BREAK_TRIGGER_TYPE_VEHICLE_MOVE,
                   'break_entity_id': break_entity_id
                   }
                self.break_obj_list.append(break_item_info)
                return
            global_data.emgr.scene_vehicle_collision_event.emit(cobj.cid, self.unit_obj.id, point)
            vehicle = self.vehicle
            if vehicle:
                vehicle.speed = vehicle.speed * 0.8
                now = time.time()
                if now - self.collision_sound_time > 0.5:
                    self.send_event('E_VEHICLE_COLLISION_SOUND', cobj.group)
                    self.collision_sound_time = now
            return

    def tick(self, dt):
        if not self.col_id:
            return
        vehicle = self.ev_g_vehicle()
        if vehicle:
            self.last_vert_speed = vehicle.speed.y
        now = time.time()
        if now > self.next_check_time:
            global_data.emgr.scene_add_break_objs.emit(self.break_obj_list, True)
            self.break_obj_list = []
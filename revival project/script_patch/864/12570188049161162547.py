# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComVehicleMoveSyncSender.py
from __future__ import absolute_import
import math
import math3d
from ..UnitCom import UnitCom
from ...time_utility import time
from ...common_utils.matrix_utils import format_matrix_to_tuple
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.vehicle_const import SYNC_WHEELE_SCALE, VEHICLE_WHEEL_COUNT
from logic.gcommon.const import USE_FLOAT_REDUCE
import logic.gcommon.common_utils.float_reduce_util as fl_reduce
from logic.gutils.sync.TriggerPosRot import TriggerPosRot
from logic.gcommon.common_utils.math3d_utils import normal_v3d_to_tp as v3d_to_tp

class ComVehicleMoveSyncSender(UnitCom):
    BIND_EVENT = {'E_VEHICLE_SYNC_TRANSFORM': '_vehicle_syn_transform',
       'E_VEHICLE_SYNC_TRANSFORM_STOP': '_vehicle_syn_transform_stop',
       'E_VEHICLE_SET_CMP_DIS': '_vehicle_set_cmp_dis',
       'E_VEHICLE_SYNC_WATER': '_vehicle_syn_water',
       'E_VEHICLE_BROADCAST': '_vehicle_broadcast',
       'E_VEHICLE_SYNC_RB': '_on_roll_back',
       'E_VEHICLE_SYNC_TRIGGER_ENABLE': '_set_trigger_enable',
       'E_CHANGE_PATTERN': '_on_pattern_changed'
       }

    def __init__(self):
        super(ComVehicleMoveSyncSender, self).__init__(need_update=False)
        self.avatar_send_event = global_data.player.logic.send_event
        self.enable = False
        self.last_send_time = time()
        self.last_car_mat = None
        self._tg_pos_rot = TriggerPosRot()
        self._tg_pos_rot.set_callback('lin', self._on_lin_tri)
        self._tg_pos_rot.set_callback('agl', self._on_agl_tri)
        return

    def destroy(self):
        self._on_sender_destroy()
        self.need_update = False
        self.avatar_send_event = None
        super(ComVehicleMoveSyncSender, self).destroy()
        return

    def _real_syn(self):
        vid = self.unit_obj.id
        vehicle = self.ev_g_vehicle()
        wheel_trans = {}
        wheels = self.ev_g_vehicle_wheel()
        world_mat = self.last_car_mat
        self.last_send_time = time()
        self.last_car_mat = None
        if world_mat is None:
            return
        else:
            car_mat = math3d.matrix(world_mat)
            car_mat.inverse()
            if wheels:
                for wm, idx in wheels:
                    local = wm.world_transformation * car_mat
                    local *= SYNC_WHEELE_SCALE
                    wheel_trans[idx] = format_matrix_to_tuple(local)

            wheels_agl = {}
            for idx in range(VEHICLE_WHEEL_COUNT):
                radian = self.ev_g_wheel_rotation_radian(idx)
                if radian != None:
                    wheels_agl[idx] = round(radian, 2)

            lin_spd = vehicle.speed
            l_spd = (lin_spd.x, lin_spd.y, lin_spd.z)
            agl_spd = vehicle.angular_speed
            a_spd = (agl_spd.x, agl_spd.y, agl_spd.z)
            if USE_FLOAT_REDUCE:
                l_spd = fl_reduce.f3_to_i3(*l_spd)
                a_spd = fl_reduce.f3_to_i3(*a_spd)
            trans_info = {'wheel': wheel_trans,
               'wheels_agl': wheels_agl,
               'speed': lin_spd.length / NEOX_UNIT_SCALE * 3.6,
               'eg_spd': vehicle.engine_speed,
               'l_spd': l_spd,
               'a_spd': a_spd
               }
            self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_syn_transform', (vid, trans_info), True)
            return

    def _vehicle_syn_transform(self, world_mat, send_immediately=False):
        if not self.unit_obj:
            return
        if self.enable is False:
            self.need_update = True
            self.enable = True
        self.last_car_mat = world_mat
        if send_immediately:
            self._real_syn()

    def _vehicle_syn_transform_stop(self):
        vehicle_model = self.ev_g_model()
        if not vehicle_model:
            return
        self._vehicle_syn_transform(vehicle_model.world_transformation, True)
        self._on_lin_tri(time(), vehicle_model.position, math3d.vector(0, 0, 0), math3d.vector(0, 0, 0))

    def _vehicle_set_cmp_dis(self, dis=30.0):
        self._tg_pos_rot.set_lin_cmp_dis(dis)

    def tick(self, dt):
        if not self.unit_obj:
            return
        self._on_pos_rot()
        self._tg_pos_rot.tick(dt)
        now = time()
        if now - self.last_send_time > 0.2:
            self._real_syn()

    def _vehicle_syn_water(self, in_water, water_height):
        vid = self.unit_obj.id
        self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_syn_water', (vid, in_water, water_height), False)

    def _vehicle_broadcast(self, event_name, *args):
        vid = self.unit_obj.id
        self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_broadcast', (vid, event_name, args), False)

    def _on_pos_rot(self):
        vv = self.ev_g_vehicle()
        if not vv:
            return
        now = time()
        self._tg_pos_rot.input_lin(now, vv.position, vv.linear_velocity, math3d.vector(0, 0, 0))
        agl = math3d.rotation_to_euler(math3d.matrix_to_rotation(vv.rotation_matrix))
        self._tg_pos_rot.input_agl(now, agl, vv.angular_speed, math3d.vector(0, 0, 0))

    def _on_lin_tri(self, t, lin_pos, lin_vel, lin_acc):
        if math.isnan(lin_pos.x):
            return
        lin_pos = v3d_to_tp(lin_pos)
        lin_vel = v3d_to_tp(lin_vel)
        lin_acc = v3d_to_tp(lin_acc)
        vid = self.unit_obj.id
        self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_sync_lin', (vid, t, lin_pos, lin_vel, lin_acc), True)

    def _on_agl_tri(self, t, agl_v3d, agl_vel, agl_acc):
        if agl_v3d is None:
            return
        else:
            factor = 1
            agl_v3d = v3d_to_tp(agl_v3d * factor)
            agl_vel = v3d_to_tp(agl_vel * factor)
            agl_acc = v3d_to_tp(agl_acc * factor)
            vid = self.unit_obj.id
            self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_sync_agl', (vid, t, agl_v3d, agl_vel, agl_acc), True)
            return

    def _on_sender_destroy(self):
        if not self.unit_obj or not self.unit_obj._is_valid:
            return
        vv = self.ev_g_vehicle()
        if not vv:
            return
        now = time()
        self._tg_pos_rot.input_lin(now, vv.position, math3d.vector(0, 0, 0), math3d.vector(0, 0, 0))
        agl = math3d.rotation_to_euler(math3d.matrix_to_rotation(vv.rotation_matrix))
        self._tg_pos_rot.input_agl(now, agl, math3d.vector(0, 0, 0), math3d.vector(0, 0, 0))

    def _set_trigger_enable(self, enable):
        self.need_update = enable

    def _on_pattern_changed(self, pattern):
        from logic.gcommon.common_const import mecha_const as mconst
        if pattern != mconst.MECHA_PATTERN_VEHICLE:
            self._set_trigger_enable(False)

    def _on_roll_back(self, t, lin_pos, lin_agl, lin_vel, rb_id):
        vv = self.ev_g_vehicle()
        if not vv:
            return
        pos = math3d.vector(*lin_pos)
        agl = math3d.vector(*lin_agl)
        vel = math3d.vector(*lin_vel)
        vv.position = pos
        vv.speed = vel
        vv.angular_speed = agl
        vid = self.unit_obj.id
        self.avatar_send_event('E_CALL_SYNC_METHOD', 'vehicle_rb_done', (vid, rb_id), False)
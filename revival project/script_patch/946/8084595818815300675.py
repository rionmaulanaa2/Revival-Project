# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComVehicleMoveSyncReceiver.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from logic.gcommon.common_utils.matrix_utils import create_matrix_from_tuple
import logic.gcommon.time_utility as time
import math3d
from logic.gcommon.common_const.vehicle_const import SYNC_WHEELE_SCALE
from logic.gcommon.common_utils.math3d_utils import normal_tp_to_v3d as tp_to_v3d
import math
from logic.gcommon.common_const import mecha_const

class ComVehicleMoveSyncReceiver(UnitCom):
    BIND_EVENT = {'E_VEHICLE_SYNC_RC_TRANSFORM': '_vehicle_syn_rc_transform',
       'E_VEHICLE_SYNC_WATER': '_vehicle_syn_water',
       'E_VEHICLE_SYNC_LIN': ('_on_sync_lin', -999),
       'E_VEHICLE_SYNC_AGL': ('_on_sync_agl', -999),
       'E_CHANGE_PATTERN': '_on_change_pattern',
       'G_SPEED': 'on_get_speed',
       'G_GET_WALK_DIRECTION': 'get_walk_direction'
       }

    def __init__(self):
        super(ComVehicleMoveSyncReceiver, self).__init__(need_update=False)
        self.next_pos_info = None
        now = time.time()
        self.start_time = now
        self.end_time = now
        self.min_diff_time = 0.03
        self.mp_wm_pre_translation = {}
        self.mp_wm_pre_rotation = {}
        self.cur_pos_info = {}
        V3D_ZERO = math3d.vector(0, 0, 0)
        self._lin_t = 0
        self._lin_pos = None
        self._lin_vel = V3D_ZERO
        self._lin_acc = V3D_ZERO
        self._itpl_lin = V3D_ZERO
        self._agl_t = 0
        self._agl_v3d = None
        self._agl_vel = V3D_ZERO
        self._agl_acc = V3D_ZERO
        self._itpl_agl = V3D_ZERO
        return

    def _vehicle_syn_rc_transform(self, trans_info):
        winfo = {}
        wheels = trans_info['wheel']
        for idx, _tuple in six.iteritems(wheels):
            wheel_mat = create_matrix_from_tuple(_tuple)
            wheel_mat *= 1.0 / SYNC_WHEELE_SCALE
            winfo[idx] = wheel_mat

        eg_spd = trans_info.get('eg_spd', 20)
        self.next_pos_info = {'wheel': winfo
           }
        sp_info = {'eg_spd': trans_info.get('eg_spd', 0),
           'wheels_agl': trans_info['wheels_agl']
           }
        self.send_event('E_VEHICLE_ENGINE_SPEED_CHANGE', sp_info)
        m = self.ev_g_model()
        if not m:
            return
        mat = m.world_transformation
        car_mat = math3d.matrix(mat)
        car_mat.inverse()
        wheel_trans = {}
        wheels = self.ev_g_vehicle_wheel()
        if wheels:
            for wm, idx in wheels:
                wheel_trans[idx] = wm.world_transformation * car_mat
                self.mp_wm_pre_translation[idx] = wheel_trans[idx].translation
                self.mp_wm_pre_rotation[idx] = wheel_trans[idx].rotation

        self.cur_pos_info = {'wheel': wheel_trans,
           'count': 0,
           'eg_spd': eg_spd
           }
        self.need_update = True
        self.start_time = time.time()
        self.end_time = self.start_time + trans_info.get('deta_time', 0.2) + 0.5

    def _real_syn(self, trans_info, not_interpolation=False):
        return
        import math3d
        m = self.ev_g_model()
        wheels = self.ev_g_vehicle_wheel()
        wheel_info = trans_info['wheel']
        mat_0 = math3d.matrix()
        mat_0.translation = math3d.vector(0, 0, 0)
        if not_interpolation:
            for wm, idx in wheels:
                wm.world_transformation = mat_0 * wheel_info[idx] * m.world_transformation

        else:
            for wm, idx in wheels:
                if idx in wheel_info:
                    if idx in self.mp_wm_pre_translation and idx in self.mp_wm_pre_rotation:
                        mat_new = math3d.matrix(wheel_info[idx])
                        pre_trans = self.mp_wm_pre_translation[idx]
                        pre_rot = self.mp_wm_pre_rotation[idx]
                        u = 0.18 * trans_info['count']
                        mat_new.translation = pre_trans + (mat_new.translation - pre_trans) * u
                        mat_new.rotation = pre_rot + (mat_new.rotation - pre_rot) * u
                    else:
                        mat_new = wheel_info[idx]
                    wm.world_transformation = mat_new * m.world_transformation

    def tick(self, dt):
        now = time.time()
        if now - self.end_time > 0.5:
            self.need_update = False
            return
        self.itpl_lin_agl(dt)

    def _vehicle_syn_water(self, in_water, water_height):
        self.send_event('E_VEHICLE_ON_SYNC_WATER', in_water, water_height)

    def on_get_speed(self):
        if self._lin_vel:
            return self._lin_vel.length
        return 0

    def get_walk_direction(self):
        return self._lin_vel

    def _on_sync_lin(self, t, lin_pos, lin_vel, lin_acc):
        self._lin_t = t
        self._lin_pos = tp_to_v3d(lin_pos)
        self._lin_vel = tp_to_v3d(lin_vel)
        self._lin_acc = tp_to_v3d(lin_acc)
        self.end_time = t + 1.0
        m = self.ev_g_model()
        if m:
            self.need_update = True

    def _on_sync_agl(self, t, agl_v3d, agl_vel, agl_acc):
        self._agl_t = t
        self._agl_v3d = tp_to_v3d(agl_v3d)
        self._agl_vel = tp_to_v3d(agl_vel)
        self._agl_acc = tp_to_v3d(agl_acc)
        m = self.ev_g_model()
        if m:
            self.need_update = True

    def fix_2_pi(self, new_euler, old_euler):
        diff = new_euler - old_euler
        x_df = diff.x / abs(diff.x) * math.pi if abs(diff.x) > math.pi else 0
        y_df = diff.y / abs(diff.y) * math.pi if abs(diff.y) > math.pi else 0
        z_df = diff.z / abs(diff.z) * math.pi if abs(diff.z) > math.pi else 0
        v3d_diff = math3d.vector(x_df, y_df, z_df) * 2
        old_euler += v3d_diff
        return (
         new_euler, old_euler)

    def itpl_lin_agl(self, dt):
        m = self.ev_g_model()
        if not m:
            return
        pre_car_mat = m.world_transformation
        now = time.time() - 0.05
        if self._lin_t != 0 and now - self._lin_t < 2.0:
            dt = now - self._lin_t
            _sim_pos = self._lin_pos + self._lin_vel * dt
            v3d = math3d.vector(0, 0, 0)
            v3d.intrp(m.position, _sim_pos, 0.2)
            m.position = v3d
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(v3d)
            else:
                self.send_event('E_POSITION', v3d)
        if self._agl_t != 0 and now - self._agl_t < 2.0:
            dt = now - self._agl_t
            _sim_agl = self._agl_v3d + self._agl_vel * dt
            mat_rot = m.rotation_matrix
            elr = math3d.rotation_to_euler(math3d.matrix_to_rotation(mat_rot))
            elr, _sim_agl = self.fix_2_pi(elr, _sim_agl)
            v3d = math3d.vector(0, 0, 0)
            v3d.intrp(elr, _sim_agl, 0.5)
            mat_rot = math3d.rotation_to_matrix(math3d.euler_to_rotation(v3d))
            m.rotation_matrix = mat_rot
        if self.next_pos_info:
            wheel_info = self.next_pos_info['wheel']
            car_mat = pre_car_mat
            car_mat.inverse()
            wheels = self.ev_g_vehicle_wheel()
            if wheels:
                for wm, idx in wheels:
                    if idx in wheel_info:
                        if idx in self.mp_wm_pre_translation and idx in self.mp_wm_pre_rotation:
                            mat_new = math3d.matrix(wheel_info[idx])
                            pre_mat = wm.world_transformation * car_mat
                            pre_rot = math3d.matrix_to_rotation(pre_mat.rotation)
                            new_rot = math3d.matrix_to_rotation(mat_new.rotation)
                            new_rot.slerp(pre_rot, new_rot, 0.2)
                            mat_new.rotation = math3d.rotation_to_matrix(new_rot)
                            mat_new.translation = pre_mat.translation + (mat_new.translation - pre_mat.translation) * 0.5
                        else:
                            mat_new = wheel_info[idx]
                        wm.world_transformation = mat_new * m.world_transformation

    def _on_change_pattern(self, pattern):
        if pattern == mecha_const.MECHA_PATTERN_NORMAL:
            self.need_update = False
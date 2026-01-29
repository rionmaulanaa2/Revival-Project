# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComVehiclePhysics.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
import weakref
import math3d
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon.common_const import attr_const

class ComVehiclePhysics(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'G_VEHICLE': '_get_vehicle',
       'G_VEHICLE_HEIGHT': 'get_vehicle_height',
       'G_WHEEL_RADIUS': 'get_wheel_radius',
       'G_VEHICLE_CONF': '_get_vehicle_conf',
       'E_REINIT_POS_AND_ROTATION': '_reset_pos_and_rotation',
       'E_ACCELERATE': 'set_accelerate_state',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha'
       }

    def __init__(self):
        super(ComVehiclePhysics, self).__init__(False)
        self.model_ref = None
        self.vehicle = None
        self.vtype = None
        self.vehicle_conf = None
        self.phys_conf = None
        self.phys_resume = None
        self._can_accelerate = True
        self._height = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComVehiclePhysics, self).init_from_dict(unit_obj, bdict)
        pos = bdict.get('position', (0, 390, -95))
        self.init_pos = math3d.vector(*pos)
        self.agl = bdict.get('agl', None)
        if 'lin_spd' in bdict and 'agl_spd' in bdict:
            phys_resume = {}
            phys_resume['lin_spd'] = bdict['lin_spd']
            phys_resume['agl_spd'] = bdict['agl_spd']
            phys_resume['phys_owner'] = bdict['phys_owner']
            self.phys_resume = phys_resume
        return

    def _on_model_loaded(self, model):
        self.create_vehicle()

    def on_init_complete(self):
        self.create_vehicle()
        transform_id = self.unit_obj.ev_g_transform_id()
        if transform_id:
            self.vtype = str(transform_id)

    def create_vehicle(self):
        model = self.ev_g_model()
        if not model:
            return
        else:
            self.model_ref = weakref.ref(model)
            from common.cfg import confmgr
            transform_id = self.unit_obj.ev_g_transform_id()
            phys_conf = confmgr.get('vehicle_data2', str(transform_id), default=None)
            if phys_conf:
                self.vtype = str(transform_id)
                self.vehicle = self.create_vehicle_phys()
                self.send_event('E_VECHICLE_LOADED', self.vehicle)
                phys_resume = self.phys_resume
                if not phys_resume:
                    enable_phy = False
                    self.send_event('E_VEHICLE_ENABLE_PHYSICS', enable_phy)
                else:
                    lin_spd = math3d.vector(*phys_resume['lin_spd'])
                    agl_spd = math3d.vector(*phys_resume['agl_spd'])
                    phy_owner = phys_resume['phys_owner']
                    enable_phy = True if phy_owner == global_data.player.id and lin_spd.length > 0 and agl_spd.length > 0 else False
                    self.send_event('E_VEHICLE_ENABLE_PHYSICS', enable_phy, lin_spd, agl_spd)
                pattern = self.ev_g_pattern()
                is_vehicle_and_controller = pattern == mconst.MECHA_TYPE_VEHICLE and phys_resume and phys_resume['phys_owner'] == global_data.player.id
                if pattern == mconst.MECHA_TYPE_NORMAL or not is_vehicle_and_controller:
                    global_data.game_mgr.scene.scene_col.remove_object(self.vehicle)
                vnpc = self.unit_obj.get_owner()
                eid = self.unit_obj.id
                global_data.emgr.scene_add_vehicle.emit(eid, vnpc)
            return

    def get_vehicle_height(self):
        return self._height

    def get_wheel_radius(self):
        vehicle = self._get_vehicle()
        if not vehicle:
            return 0
        return vehicle.wheel_radius

    def create_vehicle_phys(self):
        import collision
        import math3d
        import world
        from logic.gcommon.const import NEOX_UNIT_SCALE
        scene = self.scene
        vconf = self._get_vehicle_conf()
        phys_conf = self._get_phys_conf()
        model = self.model_ref()
        wheel_points = vconf['wheelpoints']
        wheelsocks = vconf['wheelsocks']
        wheel_cnt = len(wheel_points)
        wheel_res = vconf['cWheelRes']
        broken_wheel_res = vconf['cWheelBreakRes']
        volume = math3d.vector(*[ int(x) for x in phys_conf['volume'].split(',') ])
        rigid_mass = phys_conf['rigid_mass']
        rigid_center = math3d.vector(*[ float(x) for x in phys_conf['rigid_center'].split(',') ])
        rigid_moi = math3d.vector(*[ float(x) for x in phys_conf['rigid_moi'].split(',') ])
        chassis_offset = math3d.vector(*[ float(x) for x in phys_conf['chassis_offset'].split(',') ])
        peak_torque = phys_conf['peak_torque']
        max_omega = phys_conf['max_omega']
        engine_moi = phys_conf['engine_moi']
        engine_full_rate = phys_conf['engine_full_rate']
        engine_zero_rate = phys_conf['engine_zero_rate']
        engine_zero_rate_disengated = phys_conf['engine_zero_rate_disengated']
        wheel_damping_rate = phys_conf['wheel_damping_rate']
        wheel_moi = phys_conf['wheel_moi']
        max_steer = phys_conf['max_steer']
        max_hand_brake_torque = phys_conf['max_hand_brake_torque']
        brake_factor = phys_conf['brake_factor']
        longitudinal_force = phys_conf['longitudinal_force']
        latstiffy = phys_conf['latstiffy']
        camber_force = phys_conf['camber_force']
        latstiffx = phys_conf['latstiffx']
        clutch_strength = phys_conf['clutch_strength']
        anti_rollbar = phys_conf['anti_rollbar']
        suspension_max_droop = phys_conf['suspension_max_droop']
        spring_strength = phys_conf['spring_strength']
        spring_damper_rate = phys_conf['spring_damper_rate']
        front_rear = phys_conf['front_rear']
        front_left_right = phys_conf['front_left_right']
        rear_left_right = phys_conf['rear_left_right']
        rear_bias = phys_conf['rear_bias']
        center_bias = phys_conf['center_bias']
        front_bias = phys_conf['front_bias']
        wheel_mass = phys_conf['wheel_mass']
        wheel_radius = phys_conf['wheel_radius']
        wheel_width = phys_conf['wheel_width']
        wheel_type = phys_conf['wheel_type']
        wheel_offset_x = phys_conf['wheel_offset_x']
        wheel_offset_y = phys_conf['wheel_offset_y']
        wheel_offset_z = phys_conf['wheel_offset_z']
        chassis_verts = [ math3d.vector(*eval(v_str)) for v_str in phys_conf['chassis_verts'].split('|') ]
        is_boat = True if phys_conf['vehicle_type'] == 2 else False
        vehicle = collision.Vehicle4W()
        vehicle.set_chassis_mass(rigid_mass)
        vehicle.set_chassis_dim(volume)
        vehicle.set_chassis_offset(chassis_offset)
        self._height = volume.y + wheel_radius
        for i in range(0, 4):
            vehicle.set_wheel_info(i, wheel_mass, wheel_radius, wheel_width)
            vehicle.set_tire_type(i, wheel_type)
            is_front_wheel = i // 2 == 0
            is_left_wheel = i % 2 == 0
            x = -wheel_offset_x if is_left_wheel else wheel_offset_x
            y = wheel_offset_y
            if is_front_wheel:
                z = wheel_offset_z if 1 else -wheel_offset_z
                vehicle.set_wheel_center_offset(i, math3d.vector(x, y, z))

        vehicle.reset_position(self.init_pos, math3d.euler_to_rotation(math3d.vector(0, 0, 0)))
        vehicle.set_chassis_verts(chassis_verts)
        vehicle.set_chasis_model(model)
        scene.scene_col.add_interest_id(vehicle.cid)
        scene.scene_col.add_object(vehicle)
        vehicle.mask = GROUP_CHARACTER_INCLUDE
        vehicle.group = GROUP_CHARACTER_INCLUDE
        if self.agl:
            agl = self.agl
            self.agl = None
            agl = math3d.vector(*agl)
            mat_rot = math3d.rotation_to_matrix(math3d.euler_to_rotation(agl))
            vehicle.reset_position(self.init_pos, mat_rot)
        vehicle.peak_torque = peak_torque
        vehicle.max_omega = max_omega
        vehicle.engine_moi = engine_moi * self._get_speed_scale()
        vehicle.engine_full_rate = engine_full_rate
        vehicle.engine_zero_rate = engine_zero_rate
        vehicle.engine_zero_rate_disengated = engine_zero_rate_disengated
        vehicle.wheel_damping_rate = wheel_damping_rate
        vehicle.wheel_moi = wheel_moi
        vehicle.max_steer = max_steer
        vehicle.max_hand_brake_torque = max_hand_brake_torque
        vehicle.longitudinal_force = longitudinal_force
        vehicle.latstiffy = latstiffy
        vehicle.latstiffx = latstiffx
        vehicle.camber_force = camber_force
        vehicle.clutch_strength = clutch_strength
        vehicle.anti_rollbar = anti_rollbar
        vehicle.suspension_max_droop = suspension_max_droop
        vehicle.spring_strength = spring_strength
        vehicle.spring_damper_rate = spring_damper_rate
        vehicle.front_rear = front_rear
        vehicle.front_left_right = front_left_right
        vehicle.rear_left_right = rear_left_right
        vehicle.rear_bias = rear_bias
        vehicle.center_bias = center_bias
        vehicle.front_bias = front_bias
        vehicle.is_boat = True
        vehicle.rigid_center = rigid_center
        vehicle.rigid_moi = rigid_moi
        global_data.v = vehicle
        return vehicle

    def set_accelerate_state(self, flag):
        if flag:
            self._accelerate()
        else:
            self._accelerate_done()

    def _accelerate(self):
        if not self.vehicle:
            return
        if self._can_accelerate:
            self._can_accelerate = False
            self.vehicle.peak_torque = self._get_phys_conf().get('acc_peak_torque', 150000)
            self.vehicle.max_omega = self._get_phys_conf().get('acc_max_omega', 1000)
            self.vehicle.engine_moi = self._get_phys_conf()['acc_engine_moi'] * self._get_speed_scale()
            self.vehicle.engine_full_rate = self._get_phys_conf()['acc_engine_full_rate']
            self.vehicle.engine_zero_rate = self._get_phys_conf()['acc_engine_zero_rate']
            self.vehicle.engine_zero_rate_disengated = self._get_phys_conf()['acc_engine_zero_rate_disengated']
            self.send_event('E_CHONGCI', True)

    def _accelerate_done(self):
        if self.vehicle:
            self._can_accelerate = True
            peak_torque = self._get_phys_conf()['peak_torque']
            max_omega = self._get_phys_conf()['max_omega']
            self.vehicle.peak_torque = peak_torque
            self.vehicle.max_omega = max_omega
            self.vehicle.engine_moi = self._get_phys_conf()['engine_moi'] * self._get_speed_scale()
            self.vehicle.engine_full_rate = self._get_phys_conf()['engine_full_rate']
            self.vehicle.engine_zero_rate = self._get_phys_conf()['engine_zero_rate']
            self.vehicle.engine_zero_rate_disengated = self._get_phys_conf()['engine_zero_rate_disengated']
            self.send_event('E_CHONGCI', False)

    def _reset_pos_and_rotation(self, pos, rot):
        if self.vehicle:
            self.vehicle.reset_position(pos, rot)

    def _get_vehicle(self):
        return self.vehicle

    def _get_vehicle_conf(self):
        from common.cfg import confmgr
        if self.vehicle_conf:
            return self.vehicle_conf
        self.vehicle_conf = confmgr.get('c_vehicle_res_config', str(self.vtype))
        return self.vehicle_conf

    def _get_phys_conf(self):
        from common.cfg import confmgr
        if self.phys_conf:
            return self.phys_conf
        self.phys_conf = confmgr.get('vehicle_data2', str(self.vtype))
        return self.phys_conf

    def destroy(self):
        if self.vehicle:
            self.scene.scene_col.remove_object(self.vehicle)
        self.vehicle = None
        super(ComVehiclePhysics, self).destroy()
        return

    def _get_speed_scale(self):
        factor = self.unit_obj.ev_g_add_attr(attr_const.ATTR_VEHICLE_SPEED_UP_FACTOR)
        if factor and 0 < factor < 1.0:
            return 1.0 - factor
        return 1.0

    def _on_join_mecha(self):
        speed_scale = self._get_speed_scale()
        config_value = self._get_phys_conf()['engine_moi']
        if speed_scale != 1.0 and self.vehicle and self.vehicle.engine_moi == config_value:
            self.vehicle.engine_moi = config_value * speed_scale

    def _on_leave_mecha(self):
        if self.vehicle:
            self.vehicle.engine_moi = self._get_phys_conf()['engine_moi']
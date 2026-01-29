# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPlane.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.time_utility import time
import math3d
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils import parachute_utils

class ComPlane(UnitCom):
    PLANE_STAGE_UNREADY = 0
    PLANE_STAGE_ON_AIR_LINE = 1
    PLANE_STAGE_AFTER_AIR_LINE = 2
    PLANE_STAGE_BEFORE_DESTROY = 3
    PLANE_STAGE_BEFORE_START = 4
    BIND_EVENT = {'G_PLANE_CUR_YAW': 'get_plane_cur_yaw',
       'G_POSITION': 'get_position',
       'G_CAN_JUMP_TO': 'can_jump_to',
       'G_CAN_JUMP_TO_3D': 'can_jump_to_in_3d_map',
       'G_JUMP_POS_VALID': 'calc_jump_pos_valid',
       'G_CNT_PLANE_RADIUS': 'get_cnt_radius',
       'G_AIRLINE_START_POS': 'get_airline_start_pos',
       'G_PLANE_DIRECTION': 'get_plane_direction',
       'G_PLANE_PREVIEW_LINE': 'get_preview_line',
       'G_PLANE_ARRIVED_END_TIMESTAMP': 'get_end_timestamp'
       }

    def __init__(self):
        super(ComPlane, self).__init__()
        self.init_attribute()

    def on_post_init_complete(self, bdict):
        super(ComPlane, self).on_post_init_complete(bdict)
        global_data.emgr.plane_create_event.emit()

    def get_position(self):
        return self._cnt_pos

    def get_plane_direction(self):
        return self._ready_forward

    def get_cnt_radius(self):
        cnt_time = time()
        return self.start_radius + (cnt_time - self._ready_timestamp) * self.radius_spd

    def get_end_timestamp(self):
        return self._end_timestamp

    def calc_airline_start_pos(self):
        airline = self._end_position - self._start_position
        distance = airline.length
        airline.normalize()
        spd = distance / (self._end_timestamp - self._ready_timestamp)
        time = self.start_radius / self.radius_spd
        reverse_distance = spd * time
        self.airline_start_pos = self._start_position - airline * reverse_distance
        airline_start_distance = (self.airline_start_pos - self._start_position).length
        self.airline_angle_half = math.atan(self.start_radius * 1.0 / airline_start_distance)

    def calc_airline_tangent_points(self):
        self.end_radius = self.start_radius + (self._end_timestamp - self._ready_timestamp) * self.radius_spd
        airline_start_distance = (self.airline_start_pos - self._start_position).length
        sin_rot_ratians = float(self.start_radius) / airline_start_distance
        sin_rot_ratians = 0.999 if sin_rot_ratians >= 1 else sin_rot_ratians
        rot_radians = math.asin(sin_rot_ratians)
        tangent_start_length = self.start_radius / math.tan(rot_radians)
        tangent_end_length = self.end_radius / math.tan(rot_radians)
        forward_dir = self._start_position - self.airline_start_pos
        forward_dir.normalize()
        m1 = math3d.matrix.make_rotation_y(rot_radians)
        m2 = math3d.matrix.make_rotation_y(-rot_radians)
        tangent_dir1 = forward_dir * m1
        tangent_dir2 = forward_dir * m2
        tangent_l1_s = tangent_dir1 * tangent_start_length + self.airline_start_pos
        tangent_l1_e = tangent_dir1 * tangent_end_length + self.airline_start_pos
        tangent_l2_s = tangent_dir2 * tangent_start_length + self.airline_start_pos
        tangent_l2_e = tangent_dir2 * tangent_end_length + self.airline_start_pos
        self._tangent_points = [
         tangent_l1_s, tangent_l1_e, tangent_l2_s, tangent_l2_e]
        global_data.emgr.draw_preview_line_event.emit(self._tangent_points)

    def calc_jump_pos_valid(self, pos):
        forward_dir = self._start_position - self.airline_start_pos
        cur_dir = pos - self.airline_start_pos
        cur_dir.y = 0
        if cur_dir.is_zero:
            return True
        else:
            airline_start_distance = (self.airline_start_pos - self._start_position).length
            sin_rot_radians = float(self.start_radius) / airline_start_distance
            sin_rot_radians = 0.99 if sin_rot_radians >= 1 else sin_rot_radians
            rot_radians = math.asin(sin_rot_radians)
            forward_dir.normalize()
            cur_dir.normalize()
            cos_radians = max(min(1.0, forward_dir.dot(cur_dir)), -1.0)
            radians = math.acos(cos_radians)
            if abs(radians) <= rot_radians:
                return True
            return False

    def get_preview_line(self):
        return self._tangent_points

    def get_airline_start_pos(self):
        return self.airline_start_pos

    def can_jump_to(self, position):
        if not self._cnt_pos:
            return False
        else:
            cnt_radius = self.get_cnt_radius()
            cmp_pos = math3d.vector(position)
            cmp_pos.y = self._cnt_pos.y
            target_cnt_vector = cmp_pos - self._cnt_pos
            if target_cnt_vector.dot(self._ready_forward) >= 0:
                return target_cnt_vector.length <= cnt_radius
            target_start_pos_vector = cmp_pos - self.airline_start_pos
            target_start_pos_vector.normalize()
            radian = math.acos(target_start_pos_vector.dot(self._ready_forward))
            print('calc radian is', radian, 'half radian', self.airline_angle_half)
            return radian < self.airline_angle_half

    def can_jump_to_in_3d_map(self, position):
        if not self._cnt_pos:
            return False
        else:
            cnt_radius = self.get_cnt_radius()
            cmp_pos = math3d.vector(position)
            cmp_pos.y = self._cnt_pos.y
            target_cnt_vector = cmp_pos - self._cnt_pos
            if target_cnt_vector.length <= cnt_radius:
                return True
            return False

    def init_attribute(self):
        self.need_update = True
        self._player_in_plane = False
        self._air_line_rad = 0
        self._start_position = None
        self._end_position = None
        self._start_timestamp = 0
        self._end_timestamp = 0
        self._ready_timestamp = 0
        self._ready_time = 0
        self._after_air_line_time = 10
        self._ready_forward = None
        self._end_forward = None
        self._rad_spd = 0
        self._on_air_line_time = 0
        self._round_center = None
        self._round_radius = 0
        self._cnt_pos = None
        self._speed = 0
        self._tangent_points = []
        self._passenger_list = []
        from common.cfg import confmgr
        parachute_conf = confmgr.get('parachute_conf').get_conf()
        self.start_radius = parachute_conf['PARACHUTE_START_RADIUS'] * NEOX_UNIT_SCALE
        self.radius_spd = parachute_conf['PARACHUTE_RADIUS_SPD'] * NEOX_UNIT_SCALE
        self.airline_start_pos = None
        self.airline_angle_half = None
        return

    def in_which_stage(self, cnt_time):
        if self._start_timestamp > cnt_time:
            return self.PLANE_STAGE_BEFORE_START
        else:
            if self._ready_timestamp > cnt_time >= self._start_timestamp:
                return self.PLANE_STAGE_UNREADY
            if self._end_timestamp > cnt_time >= self._ready_timestamp:
                return self.PLANE_STAGE_ON_AIR_LINE
            if self._end_timestamp + self._after_air_line_time > cnt_time >= self._end_timestamp:
                return self.PLANE_STAGE_AFTER_AIR_LINE
            return self.PLANE_STAGE_BEFORE_DESTROY

    def update_straight_flight_pos(self, time_gap):
        pos = self._ready_forward * self._speed * time_gap + self._start_position
        self.sync_plane_pos(pos, self._ready_forward)

    def sync_plane_pos(self, pos, direction, circle_ratio=0):
        if self._passenger_list:
            new_psgs = []
            for eid in self._passenger_list:
                entity = EntityManager.getentity(eid)
                if entity and entity.logic:
                    if entity.logic.share_data.ref_parachute_stage == parachute_utils.STAGE_PLANE:
                        entity.logic.send_event('E_FOOT_POSITION', pos)
                        if G_POS_CHANGE_MGR:
                            entity.logic.notify_pos_change(pos)
                        else:
                            entity.logic.send_event('E_POSITION', pos)
                        new_psgs.append(eid)

            self._passenger_list = new_psgs
        self._cnt_pos = pos

    def update_unready_flight_pos(self, time_gap):
        self.update_straight_flight_pos(time_gap)

    def update_extension_flight_pos(self, time_gap):
        pos = self._end_forward * (time_gap - self._on_air_line_time) * self._speed + self._end_position
        self.sync_plane_pos(pos, self._end_forward)

    def init_from_dict(self, unit_obj, bdict):
        super(ComPlane, self).init_from_dict(unit_obj, bdict)
        self.start_flight_stage(bdict)

    def start_flight_stage(self, bdict):
        self.init_air_line_data(bdict)

    def init_air_line_data(self, bdict):
        self._start_position = math3d.vector(*bdict['start_pos'])
        self._end_position = math3d.vector(*bdict['end_pos'])
        angle = bdict['angle']
        self._speed = bdict['speed']
        self._air_line_rad = angle * math.pi / 180.0
        self._start_timestamp = bdict['start_timestamp']
        self._ready_time = bdict['ready_time']
        self._ready_timestamp = self._start_timestamp + self._ready_time
        self._end_timestamp = self._start_timestamp + bdict['flight_time']
        self._on_air_line_time = self._end_timestamp - self._ready_timestamp
        self._rad_spd = self._air_line_rad / self._on_air_line_time
        self.init_straight_data(bdict)
        self.calc_airline_start_pos()
        self.calc_airline_tangent_points()

    def init_straight_data(self, bdict):
        forward_dir = self._end_position - self._start_position
        forward_dir.normalize()
        self._ready_forward = forward_dir
        self._end_forward = forward_dir

    def destroy(self):
        global_data.emgr.scene_del_airline_event.emit(self.unit_obj.id)
        super(ComPlane, self).destroy()

    def init_event(self):
        super(ComPlane, self).init_event()
        global_data.emgr.plane_set_passenger_event += self.set_passenger_list
        global_data.emgr.plane_add_passenger_event += self.add_passenger
        global_data.emgr.plane_remove_passenger_event += self.remove_passenger

    def tick(self, *args):
        cnt_time = time()
        time_gap = cnt_time - self._ready_time
        cnt_stage = self.in_which_stage(cnt_time)
        time_gap = time_gap - self._start_timestamp
        if cnt_stage == self.PLANE_STAGE_BEFORE_START:
            self.update_unready_flight_pos(0.0)
        elif cnt_stage == self.PLANE_STAGE_UNREADY:
            self.update_unready_flight_pos(time_gap)
        elif cnt_stage == self.PLANE_STAGE_ON_AIR_LINE:
            self.update_straight_flight_pos(time_gap)
        elif cnt_stage == self.PLANE_STAGE_AFTER_AIR_LINE:
            self.update_extension_flight_pos(time_gap)
        else:
            global_data.emgr.plane_destroy_event.emit()

    def set_passenger_list(self, passenger_id_list):
        self._passenger_list = list(passenger_id_list)
        if global_data.player.id in self._passenger_list:
            self._passenger_list.remove(global_data.player.id)

    def add_passenger(self, passenger_id):
        if passenger_id not in self._passenger_list:
            self._passenger_list.append(passenger_id)

    def remove_passenger(self, passenger_id):
        if passenger_id in self._passenger_list:
            self._passenger_list.remove(passenger_id)

    def get_plane_cur_yaw(self):
        return self._ready_forward.yaw
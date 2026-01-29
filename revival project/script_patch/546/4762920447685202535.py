# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComFlightCam.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.utils.timer import RELEASE, CLOCK
import world
import math3d
import math
import time
import random
MIN_DIFF_SCALE = 0.02

class ComFlightCam(UnitCom):
    BIND_EVENT = {'E_POSITION': 'update_player_position',
       'E_USE_FLIGHT_CAM': 'set_use_flight_cam',
       'E_SET_FLIGHT_BOOST_PARAM': 'init_param'
       }

    def __init__(self):
        super(ComFlightCam, self).__init__(need_update=False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlightCam, self).init_from_dict(unit_obj, bdict)
        self.scale_x = 0.0
        self.max_drift_dist = 0.0
        self.last_cam_target_pos = None
        self.need_calculate = False
        self.last_offset_stamp = 0
        self.min_radius = 5.0
        self.max_radius = 15.0
        self.radius_speed = 2.0
        self.min_angle_interval = math.pi
        self.max_angle_interval = math.pi * 5 / 2
        self.max_angle_speed = 1.0
        self.min_angle_acc = 1.0
        self.max_angle_acc = 2.0
        self.plus = 1.0
        self.initialize_camera_offset_param()
        self.is_target_pos_recovering = False
        self.start_intrp_stamp = 0
        self.drift_dir = 1
        self.cur_duration = 0
        global_data.emgr.enable_special_target_pos_logic.emit(False)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.update_player_position)
        return

    def destroy(self):
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.update_player_position)
        global_data.emgr.enable_special_target_pos_logic.emit(False)
        super(ComFlightCam, self).destroy()

    def init_param(self, *args):
        self.max_drift_dist, self.leave_recover_duration = args

    def update_player_position(self, mecha_pos):
        if self.need_calculate:
            self._update_camera_offset()
            cam = world.get_active_scene().active_camera
            cam_right = cam.rotation_matrix.right
            scale = self.scale_x
            self.last_cam_target_pos = mecha_pos + cam_right * scale * self.max_drift_dist
            cam_up = cam.rotation_matrix.up
            self.last_cam_target_pos += cam_up * self.vertical_offset
            self.last_cam_target_pos += cam_right * self.horizontal_offset
            global_data.emgr.set_target_pos_for_special_logic.emit(self.last_cam_target_pos)
        elif self.is_target_pos_recovering:
            self._interpolate_target_pos()

    def set_rocker_drag_scale(self, scale_x, scale_z, *args):
        if math.fabs(scale_x - self.scale_x) > MIN_DIFF_SCALE:
            self.scale_x = scale_x

    def set_use_flight_cam(self, flag):
        self.need_calculate = flag
        if flag:
            self.regist_event('E_CHANGE_ANIM_MOVE_DIR', self.set_rocker_drag_scale)
            self.scale_x = 0.0
            if not self.is_target_pos_recovering:
                self.last_cam_target_pos = self.ev_g_position()
                global_data.emgr.enable_special_target_pos_logic.emit(flag)
            global_data.emgr.set_target_pos_for_special_logic.emit(self.last_cam_target_pos)
            self.initialize_camera_offset_param()
        else:
            self.unregist_event('E_CHANGE_ANIM_MOVE_DIR', self.set_rocker_drag_scale)
            self.start_target_pos_recover()

    def _clamp(self, x, min_val, max_val):
        if x > max_val:
            return max_val
        if x < min_val:
            return min_val
        return x

    def _update_camera_offset(self):
        cur_offset_stamp = time.time()
        delta_time = cur_offset_stamp - self.last_offset_stamp
        self.last_offset_stamp = cur_offset_stamp
        if math.fabs(self.angle - self.last_angle) >= self.angle_interval and self.angle_speed * self.last_angle_speed <= 0:
            self.angle_interval = random.uniform(self.min_angle_interval, self.max_angle_interval)
            self.angle_acc = random.uniform(self.min_angle_acc, self.max_angle_acc)
            self.last_angle = self.angle
            self.plus *= -1
        self.angle_speed += self.angle_acc * self.plus * delta_time
        if math.fabs(self.angle_speed) > self.max_angle_speed:
            self.angle_speed = self.max_angle_speed * self.plus
        self.angle += self.angle_speed * delta_time
        self.radius += self.radius_speed * self.plus * delta_time
        self.radius = self._clamp(self.radius, self.min_radius, self.max_radius)
        self.vertical_offset = self.radius * math.sin(self.angle)
        self.horizontal_offset = self.radius * math.cos(self.angle)

    def initialize_camera_offset_param(self):
        self.vertical_offset = 0.0
        self.horizontal_offset = 0.0
        self.radius = 0.0
        self.angle = 0.0
        self.last_angle = self.angle
        self.angle_interval = 0
        self.angle_speed = 0
        self.last_angle_speed = self.angle_speed
        self.angle_acc = 1.0

    def start_target_pos_recover(self):
        self.start_intrp_stamp = time.time()
        self.cur_duration = self.leave_recover_duration * math.fabs(self.scale_x)
        self.drift_dir = 1 if self.scale_x > 0 else -1
        self.is_target_pos_recovering = True

    def _interpolate_target_pos(self):
        cur_stamp = time.time()
        duration = cur_stamp - self.start_intrp_stamp
        if duration >= self.cur_duration:
            global_data.emgr.enable_special_target_pos_logic.emit(False)
            global_data.emgr.camera_target_pos_changed_event.emit(self.ev_g_position())
            self.is_target_pos_recovering = False
            return
        cam = world.get_active_scene().active_camera
        cam_right = cam.rotation_matrix.right
        scale = 1.0 - duration / self.cur_duration
        scale *= scale
        self.last_cam_target_pos = self.ev_g_position() + cam_right * self.max_drift_dist * scale * self.drift_dir
        global_data.emgr.set_target_pos_for_special_logic.emit(self.last_cam_target_pos)
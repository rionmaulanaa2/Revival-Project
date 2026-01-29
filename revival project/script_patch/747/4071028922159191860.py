# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/GyroscopeComponent.py
from __future__ import absolute_import
from six.moves import range
import game3d
import cc
import math3d
import random
DELTA_GYRO_EPSILON = 0.01

class GyroscopeComponent(object):
    GYRO_ACT_TAG = 191030

    def __init__(self, *arg):
        self._gryo_update_cb = None
        self.delta_gyro_epsilon = DELTA_GYRO_EPSILON
        self._sensitivity = 1
        self._rotation_flag = 1
        self._update_timer = None
        return

    def set_args(self, *arg):
        self.arg = arg[0]
        self.interval = self.arg.get('interval', 0.033)
        self._gryo_update_cb = self.arg.get('gryo_update_cb', None)
        return

    def destroy(self):
        self.set_gyroscope_enable(False)
        self.stop_gyro_timer()
        self._gryo_update_cb = None
        return

    def set_gyroscope_enable(self, enable):
        self._cnt_gyro_vector = math3d.rotation(0, 0, 0, 1)
        game3d.activate_software_motion_sensor(0, False, self.interval)
        enable_res = game3d.activate_software_motion_sensor(0, enable, self.interval)
        if game3d.get_platform() == game3d.PLATFORM_WIN32 and global_data.show_ss_card_effect:
            import math
            self._use_gyroscope = True
            self._loop_index = 0
            start = math.radians(-40)
            end = math.radians(40)
            circle = 180
            step = (end - start) / circle
            self._loop_dir = 1
            self._sim_rot_y_list = [ i * step + start for i in range(circle) ]
            self._sim_rot_x_list = [ i * step + start for i in range(circle) ]
            self.get_gyro_dxdy = self.get_gyro_dxdy_pc
        else:
            self._use_gyroscope = enable and enable_res
        if enable:
            if self._use_gyroscope:
                self.stop_gyro_timer()
                self.start_gyro_timer()
        else:
            self.stop_gyro_timer()

    def start_gyro_timer(self):
        self._update_timer = global_data.game_mgr.register_logic_timer(self.update_gyro_data, 1)

    def stop_gyro_timer(self):
        if self._update_timer is not None:
            global_data.game_mgr.get_logic_timer().unregister(self._update_timer)
        self._update_timer = None
        return

    def get_gyro_dxdy(self):
        rot = math3d.rotation(*game3d.get_software_motion_sensor(0))
        raw_gyro_speed = rot
        if self._cnt_gyro_vector.x == 0 and self._cnt_gyro_vector.y == 0:
            if raw_gyro_speed.x != 0 and raw_gyro_speed.y != 0:
                self._cnt_gyro_vector = raw_gyro_speed
        new_vector = self._cnt_gyro_vector * 0.5 + raw_gyro_speed * 0.5
        self._cnt_gyro_vector = new_vector
        return (
         new_vector, raw_gyro_speed)

    def get_gyro_dxdy_pc(self):
        idx = self._loop_index
        rot_x = self._sim_rot_y_list[idx]
        rot_y = 0
        raw_gyro_speed = math3d.euler_to_rotation(math3d.vector(rot_x, rot_y, 0))
        new_vector = self._cnt_gyro_vector * 0.5 + raw_gyro_speed * 0.5
        self._cnt_gyro_vector = new_vector
        if self._loop_index >= len(self._sim_rot_y_list) - 1:
            self._loop_dir = -1
        elif self._loop_index <= 0:
            self._loop_dir = 1
        self._loop_index += self._loop_dir
        return (
         self._cnt_gyro_vector, raw_gyro_speed)

    def update_gyro_data(self):
        if not self._gryo_update_cb:
            return None
        else:
            _rotation = game3d.get_rotation()
            if _rotation == 90:
                self._rotation_flag = 1
            elif _rotation == 270:
                self._rotation_flag = -1
            new_gyro_vector, raw_gyro_vector = self.get_gyro_dxdy() if self._use_gyroscope else (None,
                                                                                                 None)
            self._gryo_update_cb(new_gyro_vector, raw_gyro_vector, self._rotation_flag)
            return None
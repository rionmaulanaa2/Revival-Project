# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CamAsymptoticFollowCom.py
from __future__ import absolute_import
from __future__ import print_function
import cython
from common.utils import timer
import math
import math3d
MODE_DIST_PERCENT = 1
MODE_LINEAR_VELOCITY = 2
from .ICamAsymptoticFollowCom import ICamAsymptoticFollowCom
import game3d
import time
DESIGNED_FRAME_RATE = 30
AVE_FRAME_COUNT = 10

class FollowState(object):

    def __init__(self):
        self._last_time = 0
        self._last_time_timer = None
        self._over_time_action = None
        return

    def set_last_time(self, last_time):
        self.unregister_last_timer()
        self._last_time_timer = global_data.game_mgr.register_logic_timer(func=lambda : self.on_over_time(), interval=last_time, times=1, mode=timer.CLOCK)

    def on_over_time(self):
        self._last_time_timer = None
        if self._over_time_action and callable(self._over_time_action):
            self._over_time_action()
        return

    def unregister_last_timer(self):
        if self._last_time_timer:
            global_data.game_mgr.unregister_logic_timer(self._last_time_timer)
            self._last_time_timer = None
        return

    def set_over_time_action(self, action_func):
        self._over_time_action = action_func

    def exit_state(self):
        self._over_time_action = None
        self.unregister_last_timer()
        return

    def get_follow_speed(self):
        return None


class LinearVelocityFollower(FollowState):

    def __init__(self, start_speed, max_speed, acceleration):
        super(LinearVelocityFollower, self).__init__()
        self._start_speed = start_speed
        self._max_speed = max_speed
        self._acceleration = acceleration
        self._speed = self._start_speed

    def set_init_state(self, start_speed, max_speed, acceleration):
        self._start_speed = start_speed
        self._max_speed = max_speed
        self._acceleration = acceleration
        self._speed = self._start_speed

    def get_move_vec(self, delta_time, move_dir, cur_pos, target_pos):
        return move_dir * delta_time * self._speed

    def get_follow_speed(self):
        return self._speed


class CamAsymptoticFollowCom(ICamAsymptoticFollowCom):

    def __init__(self):
        self._max_follow_speed_change_timer = None
        self._follow_target_pos = None
        self._default_follow_target_speed = 1.0
        self._follow_target_speed = self._default_follow_target_speed
        self._speed_recover_timer = None
        self._cur_follow_method = None
        self._frame_rate = game3d.get_frame_rate()
        self._speed_frame_ratio = float(self._frame_rate) / DESIGNED_FRAME_RATE
        self._last_camera_follow_target_pos_list = []
        self._last_camera_follow_speed_val_list = []
        self._last_camera_follow_delta_list = []
        self._camera_speed = 0
        self._cur_follow_time = 0
        self._cur_target_time = 0
        return

    def on_change_target_follow_speed(self, new_speed, last_time=10, recover_time=0.2, mode=None, extra_info=None):
        if last_time <= 0:
            log_error('follow speed last time should larger than 0')
            return
        if not mode:
            self._last_camera_follow_target_pos_list = []
            self._last_camera_follow_speed_val_list = []
            self._last_camera_follow_delta_list = []
            self._camera_speed = 0
            self._cur_follow_time = 0
            self._cur_target_time = 0
            self._unregister_recover_timer()
            if new_speed != self._default_follow_target_speed:
                self._unregister_timer()
                self._max_follow_speed_change_timer = global_data.game_mgr.register_logic_timer(func=lambda : self.recover_to_default_speed(recover_time), interval=last_time, times=1, mode=timer.CLOCK)
            self._follow_target_speed = new_speed
        elif mode == 'SPEED':
            self.on_change_target_follow_by_linear_velocity({'speed': new_speed}, last_time, recover_time)

    def get_follow_target_pos(self):
        return self._follow_target_pos

    def get_follow_target_speed(self):
        if self._cur_follow_method:
            return self._cur_follow_method.get_follow_speed()
        return self._follow_target_speed

    def recover_to_default_speed(self, time=0.1):
        self.change_follow_method(None)
        self._max_follow_speed_change_timer = None
        global_data.game_mgr.unregister_logic_timer(self._speed_recover_timer)
        if time > 0:
            time = time * self._speed_frame_ratio
            times = math.ceil(time / 0.03)
            step = (self._default_follow_target_speed - self._follow_target_speed) / times
            self._speed_recover_timer = global_data.game_mgr.register_logic_timer(func=lambda : self._gradually_recover_speed(step), interval=0.03, times=times, mode=timer.CLOCK)
        else:
            self._follow_target_speed = self._default_follow_target_speed
        return

    def _gradually_recover_speed(self, step=0.1):
        self._follow_target_speed = min(self._follow_target_speed + step, self._default_follow_target_speed)

    def init_target_pos(self, world_pos):
        self._follow_target_pos = world_pos

    def update_follow_target_pos(self, world_pos):
        if world_pos is None:
            import exception_hook
            exception_hook.post_stack('world pos should not be None, old_pos:%s' % str(self._follow_target_pos))
        self._follow_target_pos = world_pos
        return

    def get_asymptotic_follow_pos(self, cur_pos, delta_time, camera):
        ret = self._inner_get_asymptotic_follow_pos(cur_pos, delta_time, camera)
        if self._follow_target_speed < 1.0:
            if self._last_camera_follow_target_pos_list:
                last_diff = self._follow_target_pos - self._last_camera_follow_target_pos_list[-1]
                self._last_camera_follow_speed_val_list.append(last_diff.length)
            self._last_camera_follow_target_pos_list.append(self._follow_target_pos)
            self._last_camera_follow_delta_list.append(delta_time)
            if len(self._last_camera_follow_target_pos_list) > AVE_FRAME_COUNT:
                self._last_camera_follow_target_pos_list.pop(0)
                self._last_camera_follow_speed_val_list.pop(0)
                self._last_camera_follow_delta_list.pop(0)
        return ret

    def _inner_get_asymptotic_follow_pos(self, cur_pos, delta_time, camera):
        follow_target_pos = self._follow_target_pos
        if cur_pos:
            distance_vec = follow_target_pos - cur_pos
            if not self._cur_follow_method:
                speed_val_list = self._last_camera_follow_speed_val_list
                if 0.001 < self._follow_target_speed < 0.95 and speed_val_list:
                    last_pos = self._last_camera_follow_target_pos_list[-1]
                    last_move_vec = follow_target_pos - last_pos
                    ave_speed = sum(speed_val_list) / len(speed_val_list)
                    factor = 1 * (1.0 - (AVE_FRAME_COUNT - len(self._last_camera_follow_speed_val_list)) / float(AVE_FRAME_COUNT))
                    ave_speed = last_move_vec.length * (1 - factor) + ave_speed * factor
                    ave_delta = sum(self._last_camera_follow_delta_list) / len(self._last_camera_follow_delta_list)
                    move_dir = math3d.vector(distance_vec)
                    if not move_dir.is_zero:
                        move_dir.normalize()
                    ave_vec = move_dir * ave_speed
                    frame_pos_diff_in_30 = ave_vec * self._speed_frame_ratio
                    last_follow_target_pos = self._last_camera_follow_target_pos_list[-1]
                    predict_pos = frame_pos_diff_in_30 + last_follow_target_pos
                    if self._frame_rate > DESIGNED_FRAME_RATE and self._cur_target_time < 2 and self._follow_target_speed < 0.8:
                        if self._cur_follow_time >= self._cur_target_time:
                            dist_vec_between_camera_target = (follow_target_pos - cur_pos) * self._follow_target_speed
                            predict_len = (predict_pos - cur_pos).length
                            if predict_len > 0.001 and self._follow_target_speed < 0.4:
                                slow_factor = (follow_target_pos - cur_pos).length / predict_len
                            elif self._follow_target_speed > 0.6:
                                slow_factor = (self._follow_target_speed - 0.6) / 0.4 * 0.3 + 1
                            else:
                                slow_factor = 1.0
                            self._camera_speed = dist_vec_between_camera_target.length / (1.0 / DESIGNED_FRAME_RATE) * slow_factor
                            self._cur_target_time += 1.0 / DESIGNED_FRAME_RATE
                        else:
                            slow_factor = 1.0
                        self._cur_follow_time += 1.0 / self._frame_rate
                        diff_vec = move_dir * (self._camera_speed * ave_delta)
                    else:
                        dist_vec_between_camera_target = (predict_pos - cur_pos) * (1 - self._follow_target_speed)
                        camera_final_pos = follow_target_pos - dist_vec_between_camera_target
                        diff_vec = camera_final_pos - cur_pos
                    if diff_vec.length > distance_vec.length:
                        diff_vec = distance_vec
                else:
                    diff_vec = (follow_target_pos - cur_pos) * self._follow_target_speed
                if diff_vec.length <= 0:
                    return None
                return diff_vec
            else:
                if type(self._cur_follow_method) == LinearVelocityFollower:
                    move_vec = self._cur_follow_method.get_move_vec(delta_time, camera.transformation.forward, cur_pos, follow_target_pos)
                    return move_vec
                return None

        else:
            return follow_target_pos
        return None

    def destroy(self):
        self._unregister_timer()
        self._unregister_recover_timer()

    def _unregister_timer(self):
        if self._max_follow_speed_change_timer:
            global_data.game_mgr.unregister_logic_timer(self._max_follow_speed_change_timer)
            self._max_follow_speed_change_timer = None
        return

    def _unregister_recover_timer(self):
        if self._speed_recover_timer:
            global_data.game_mgr.unregister_logic_timer(self._speed_recover_timer)
            self._speed_recover_timer = None
        return

    def change_follow_method(self, new_method):
        if self._cur_follow_method is not None:
            self._cur_follow_method.exit_state()
            self._cur_follow_method = None
        self._cur_follow_method = new_method
        return

    def on_change_target_follow_by_linear_velocity(self, speed_dict, last_time=10, recover_time=0.2):
        speed = speed_dict.get('speed', 0)
        method = LinearVelocityFollower(speed, speed, 0)
        method.set_last_time(last_time)
        method.set_over_time_action(lambda : self.on_follow_method_over_time(recover_time))
        self.change_follow_method(method)

    def on_follow_method_over_time(self, recover_time):
        self.change_follow_method(None)
        self._follow_target_speed = 0
        self.recover_to_default_speed(recover_time)
        return

    def test(self):
        global_data.cam_lctarget.send_event('E_SET_CAMERA_FOLLOW_SPEED', True, 90, 2, 2, 'SPEED')
        print(global_data.game_mgr.scene.active_camera.transformation.forward)

    def on_frame_rate_changed(self):
        self._frame_rate = game3d.get_frame_rate()
        self._speed_frame_ratio = float(self._frame_rate) / DESIGNED_FRAME_RATE
        self._last_camera_follow_target_pos_list = []
        self._last_camera_follow_speed_val_list = []
        self._last_camera_follow_delta_list = []
        self._camera_speed = 0
        self._cur_follow_time = 0
        self._cur_target_time = 0
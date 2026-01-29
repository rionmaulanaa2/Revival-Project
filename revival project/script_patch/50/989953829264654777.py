# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComEnvDetect.py
from __future__ import absolute_import
from six.moves import range
import time
import math
import world
import math3d
import collision
from common.utils import timer
from ...cdata import status_config
import logic.gcommon.const as g_const
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.gcommon.common_const.animation_const as animation_const
import logic.gcommon.common_const.collision_const as collision_const

class ComEnvDetect(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_DELTA_YAW': 'on_env_change',
       'E_POSITION': 'on_env_change',
       'E_LEAVE_STATE': '_on_leave_state',
       'E_ENTER_STATE': '_on_enter_state'
       }

    def __init__(self):
        super(ComEnvDetect, self).__init__()
        self._ready = False
        self._timer = 0
        self._last_check_climb = time.time()
        self._last_check_jump = time.time()
        self._detect_time = 0.5
        self._detect_cache = {}
        self._is_env_detect_opened = False

    def init_from_dict(self, unit_obj, bdict):
        from logic.gcommon.common_const import ui_operation_const as uoc
        super(ComEnvDetect, self).init_from_dict(unit_obj, bdict)
        self._is_env_detect_opened = global_data.player.get_setting(uoc.AUTO_CLIMB)
        self.process_event(True)

    def destroy(self):
        super(ComEnvDetect, self).destroy()
        self.process_event(False)
        self.clear_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_enable_auto_climb': self.on_enable_auto_climb
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def clear_timer(self):
        if self._timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self._timer)
        self._timer = 0

    def on_enable_auto_climb(self, flag):
        self._is_env_detect_opened = flag
        self.clear_timer()
        if flag:
            self._timer = global_data.game_mgr.get_post_logic_timer().register(func=self.detect_env, interval=0.5, mode=timer.CLOCK)

    def on_load_animator_complete(self, *args):
        if not self._is_env_detect_opened:
            return
        animator = self.ev_g_animator()
        if not animator:
            return
        self._ready = True
        self.clear_timer()
        self._timer = global_data.game_mgr.get_post_logic_timer().register(func=self.detect_env, interval=0.5, mode=timer.CLOCK)

    def on_env_change(self, *args):
        if not self._is_env_detect_opened:
            return
        if not self._ready:
            return

    def draw_line(self, chect_begin, check_end, result):
        return
        if result[0]:
            pos_list = [
             chect_begin, result[1]]
        else:
            pos_list = [
             chect_begin, check_end]
        global_data.emgr.scene_draw_line_event.emit(pos_list, alive_time=3, color=65280)

    def _on_enter_state(self, state, *args):
        if not self._is_env_detect_opened:
            return
        if state == status_config.ST_RUN:
            self._detect_time = 0.1
            self.clear_timer()
            self._timer = global_data.game_mgr.get_post_logic_timer().register(func=self.detect_env, interval=self._detect_time, mode=timer.CLOCK)

    def _on_leave_state(self, state, *args):
        if not self._is_env_detect_opened:
            return
        if state == status_config.ST_RUN:
            self._detect_time = 0.5
            self.clear_timer()
            self._timer = global_data.game_mgr.get_post_logic_timer().register(func=self.detect_env, interval=self._detect_time, mode=timer.CLOCK)

    def detect_env(self):
        player = global_data.player
        if not player or not player.logic:
            return
        else:
            player_unit = player.logic
            player_pos = player_unit.ev_g_foot_position()
            if not player_pos:
                return
            scn = world.get_active_scene()
            model_yaw = player_unit.ev_g_yaw()
            key = '{}_{}_{}_{}'.format(int(model_yaw), int(player_pos.x), int(player_pos.y), int(player_pos.z))
            self._detect_cache = {}
            forward_vect = math3d.vector(math.sin(model_yaw), 0.0, math.cos(model_yaw))
            group_climb_check = collision_const.GROUP_CLIMB_CHECK
            max_detect_dis = g_const.CLIMB_MAX_DISTANCE * 0.5
            vertical_count = 9
            cur_serial_count = 0
            max_serial_count = 99
            vertical_results = []
            acc_offset = 0
            for i in range(vertical_count):
                if self._detect_time <= 0.1:
                    acc_offset += 0.01
                percent = float(i) / vertical_count + i * acc_offset
                chect_begin = player_pos + math3d.vector(0, g_const.CLIMB_MAX_HIGHT, 0) + forward_vect * (percent * max_detect_dis)
                check_end = chect_begin + math3d.vector(0, -g_const.CLIMB_MAX_HIGHT * 1.8, 0)
                result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
                vertical_results.append(result)
                if not result[0] and max_serial_count > vertical_count:
                    max_serial_count = i - 1
                elif i > 0 and max_serial_count == 99 and result[0]:
                    normal = result[2]
                    last_normal = vertical_results[i - 1][2]
                    dot = last_normal.dot(normal)
                    if dot < 0.9:
                        max_serial_count = i - 1
                self.draw_line(chect_begin, check_end, result)

            max_detect_dis *= 1 + acc_offset * (vertical_count - 1)
            horizon_results = []
            horizon_heights = [
             0.44, 0.76, 0.82, 0.88, 0.94, 1.0, 1.06, 1.12, 1.44, 1.94]
            horizon_heights = [ height * g_const.NEOX_UNIT_SCALE for height in horizon_heights ]
            for height in horizon_heights:
                chect_begin = player_pos + math3d.vector(0, height, 0)
                check_end = chect_begin + forward_vect * max_detect_dis
                result = scn.scene_col.hit_by_ray(chect_begin, check_end, 0, group_climb_check, group_climb_check, collision.INCLUDE_FILTER, False)
                horizon_results.append(result)
                self.draw_line(chect_begin, check_end, result)

            col_rets = []
            collect_types = {}
            height_type = g_const.DETECT_TYPE_VERTICAL_FREE
            height_types = [g_const.DETECT_TYPE_VERTICAL_FREE, g_const.DETECT_TYPE_VERTICAL_LOW_WALL, g_const.DETECT_TYPE_VERTICAL_MIDDLE_WALL, g_const.DETECT_TYPE_VERTICAL_HIGH_WALL]
            height_range = [0.1, 0.5, 1.45, 2.0]
            for i, ret in enumerate(horizon_results[::-1]):
                if ret[0]:
                    height = (ret[1].y - player_pos.y) / g_const.NEOX_UNIT_SCALE
                    if height > height_range[-1]:
                        _type = g_const.DETECT_TYPE_VERTICAL_HIGH_WALL
                    else:
                        for j, limit in enumerate(height_range):
                            if height < limit:
                                _type = j
                                break

                    if not collect_types:
                        height_type = _type
                    if _type not in collect_types:
                        collect_types[_type] = ret
                        col_rets.append(ret)

            rad_heights = []
            last_height = None
            distance_step = float(max_detect_dis) / vertical_count
            for ret in vertical_results[:max_serial_count + 1]:
                if not ret[0]:
                    height = -100
                else:
                    height = ret[1].y
                if last_height == None:
                    last_height = height
                    continue
                if height <= -100:
                    rad_height = -math.pi * 0.5
                else:
                    rad_height = math.atan((height - last_height) / distance_step)
                rad_heights.append(rad_height)

            count = len(rad_heights)
            if count > 0:
                rad_height = sum(rad_heights) / count
            else:
                rad_height = -99
            can_climb = True
            can_jump = True
            horizon_type = g_const.DETECT_TYPE_HORIZONTRAL_PLANE
            if rad_height < -math.pi * 0.4:
                horizon_type = g_const.DETECT_TYPE_HORIZONTRAL_CLIFF
            elif rad_height > 0.1:
                can_climb = True
                can_jump = True
                horizon_type = g_const.DETECT_TYPE_HORIZONTRAL_UPHILL
            elif rad_height < -0.1:
                horizon_type = g_const.DETECT_TYPE_HORIZONTRAL_DOWNHILL
            else:
                can_climb = True
                can_jump = True
                horizon_type = g_const.DETECT_TYPE_HORIZONTRAL_PLANE
            dot_nor = 0
            walk_direction = None
            if col_rets:
                col_ret = col_rets[0]
                pos, normal = col_ret[1], col_ret[2]
                walk_direction = self.ev_g_char_walk_direction()
                if not walk_direction:
                    walk_direction = math3d.vector(0, 0, 0)
                walk_direction.y = 0
                if not walk_direction.is_zero:
                    walk_direction.normalize()
                else:
                    walk_direction = forward_vect
                dot_nor = normal.dot(walk_direction)
            if height_type in [g_const.DETECT_TYPE_VERTICAL_MIDDLE_WALL]:
                now = time.time()
                if now - self._last_check_climb > 1 and can_climb:
                    try_silence_climb = False
                    if dot_nor < -0.9:
                        try_silence_climb = True
                    else:
                        nxt_col_ret = collect_types.get(g_const.DETECT_TYPE_VERTICAL_LOW_WALL, None)
                        if dot_nor < -0.2 and nxt_col_ret and walk_direction:
                            pos, normal = nxt_col_ret[1], nxt_col_ret[2]
                            sub_dot_nor = normal.dot(walk_direction)
                            if sub_dot_nor < -0.9:
                                try_silence_climb = True
                    if try_silence_climb:
                        move_duration = self.ev_g_get_status_duration(status_config.ST_MOVE)
                        run_duration = self.ev_g_get_status_duration(status_config.ST_RUN)
                        if move_duration > 1 or run_duration > 1:
                            self._last_check_climb = now
                            from logic.gutils.climb_utils import silence_climb
                            can_climb = silence_climb()
                            if not can_climb:
                                from logic.gutils.climb_utils import silence_jump
                                silence_jump()
            elif height_type in [g_const.DETECT_TYPE_VERTICAL_LOW_WALL]:
                now = time.time()
                if now - self._last_check_jump > 1.05 and dot_nor < -0.8 and can_jump:
                    move_duration = self.ev_g_get_status_duration(status_config.ST_MOVE)
                    run_duration = self.ev_g_get_status_duration(status_config.ST_RUN)
                    if move_duration > 0.5 or run_duration > 0.5:
                        self._last_check_jump = now
                        from logic.gutils.climb_utils import silence_jump
                        silence_jump(low=True)
            return
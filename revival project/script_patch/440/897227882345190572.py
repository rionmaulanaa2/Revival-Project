# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkerSidewaysShotAppearance.py
from __future__ import absolute_import
import math3d
from logic.client.const.camera_const import POSTURE_RIGHT_SIDEWAYS, POSTURE_LEFT_SIDEWAYS, POSTURE_UP_SIDEWAYS
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
SW_RIGHT = POSTURE_RIGHT_SIDEWAYS
SW_LEFT = POSTURE_LEFT_SIDEWAYS
SW_UP = POSTURE_UP_SIDEWAYS
HOZ_VECTOR = math3d.vector(1, 0, 1)
FORWARD_DIR = math3d.vector(0, 0, 1)
BUNKER_MIN_WIDTH = 0.6 * NEOX_UNIT_SCALE

class ComBunkerSidewaysShotAppearance(UnitCom):
    BIND_EVENT = {'G_PLAYER_SIDEWAYS_OFFSET': '_get_player_sideways_offset',
       'E_START_BUNK_SHOT_MOVE': 'start_sideways_shot_move',
       'E_STOP_BUNKER_SHOT_MOVE': 'stop_shot_move',
       'E_INTERRUPT_BUNKER_SHOT_MOVE': 'interrupt_bunker_shot_move',
       'G_IS_IN_BUNKER_SHOT_MOVE': '_get_is_in_bunker_shot_move',
       'E_DEATH': '_on_death',
       'S_LEAVE_BUNKER': 'on_leave_bunker'
       }

    def __init__(self):
        super(ComBunkerSidewaysShotAppearance, self).__init__()
        self._target_move_offset = None
        self.is_in_sideways_shot_move = False
        self._moved_offset = None
        self.init_tick_parameters()
        return

    def init_tick_parameters(self):
        self._move_start_time = 0
        self._move_start_pos = None
        self._move_tick_speed = None
        self._sideways_move_callback = None
        self._cur_sideways_timer_id = None
        self._move_tick_count = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBunkerSidewaysShotAppearance, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        self.part_cam = self.scene.get_com('PartCamera')

    def destroy(self):
        self.unregist_timer()
        self._sideways_move_callback = None
        self._cur_sideways_timer_id = None
        super(ComBunkerSidewaysShotAppearance, self).destroy()
        return

    def _get_player_sideways_offset(self):
        if self.is_in_sideways_shot_move:
            return self.ev_g_model_position() - self._move_start_pos
        else:
            return self._moved_offset

    def start_sideways_shot_move(self, sw_dir, offset, callback, cost_time=0.2):
        import time
        self._sideways_move_callback = callback
        from logic.gcommon.common_const.animation_const import FRAMES_PER_SECOND
        update_interval = 1.0 / FRAMES_PER_SECOND
        self._target_move_offset = offset
        self._move_start_time = time.time()
        self._move_start_pos = self.ev_g_model_position()
        self._move_end_pos = self._move_start_pos + self._target_move_offset
        self._moved_offset = math3d.vector(0, 0, 0)
        self._model_moved_offset = math3d.vector(0, 0, 0)
        self._move_tick_speed = self._target_move_offset * (1.0 / cost_time) * update_interval
        self._target_move_dist = self._target_move_offset.length
        self._move_tick_speed_dist = self._move_tick_speed.length
        self.is_in_sideways_shot_move = True
        self.unregist_timer()
        from common.utils.timer import LOGIC
        times = int(cost_time * FRAMES_PER_SECOND) + 2
        self._move_tick_count = times
        if sw_dir != SW_UP:
            t_id = global_data.game_mgr.register_logic_timer(self._sideways_move_tick, interval=1, times=times, mode=LOGIC)
        else:
            if self.part_cam:
                self._start_camera_height = self.part_cam.cam.world_position.y
            self.send_event('E_CTRL_STAND')
            t_id = global_data.game_mgr.register_logic_timer(self._sideways_stand_tick, interval=1, times=times, mode=LOGIC)
        if t_id:
            self._cur_sideways_timer_id = t_id

    def end_sideways_shot_move(self):
        self.is_in_sideways_shot_move = False
        self.unregist_timer()
        if callable(self._sideways_move_callback):
            self._sideways_move_callback()
        self._sideways_move_callback = None
        return

    def stop_shot_move(self):
        if self.is_in_sideways_shot_move:
            self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
        self.is_in_sideways_shot_move = False
        self.unregist_timer()
        self._sideways_move_callback = None
        return

    def on_leave_bunker(self):
        pass

    def _sideways_move_tick(self):
        real_move = self.ev_g_model_position() - self._move_start_pos
        real_move_dist = real_move.length

        def arrive_callback():
            self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
            self._moved_offset = self._model_moved_offset
            self.end_sideways_shot_move()

        self._move_tick_count -= 1
        remain_dist = self._target_move_dist - real_move_dist
        is_near_end = False
        is_end = real_move_dist >= self._target_move_dist or self._target_move_dist - real_move_dist < self._move_tick_speed_dist / 3.0 or self._move_tick_count == 0
        if not is_end:
            is_near_end = remain_dist <= self._move_tick_speed_dist / 2.3
        from logic.gcommon.common_const.animation_const import FRAMES_PER_SECOND
        if not is_end:
            if not is_near_end:
                self.send_event('E_SET_WALK_DIRECTION', self._move_tick_speed * FRAMES_PER_SECOND, arrive_callback, self._move_end_pos)
            else:
                self.send_event('E_SET_WALK_DIRECTION', self._move_tick_speed * FRAMES_PER_SECOND / 2.0)
            tick_real_move = real_move - self._model_moved_offset
            self._model_moved_offset = real_move
            self._moved_offset = self._model_moved_offset
            self.update_remain_camera_offset(tick_real_move)
        else:
            self._model_moved_offset = real_move
            self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
            arrive_callback()

    def unregist_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._cur_sideways_timer_id)

    def update_remain_camera_offset(self, tick_move):
        cur_offset = self.ev_g_bunker_camera_offset()
        self.send_event('S_BUNKER_CAMERA_OFFSET', cur_offset - tick_move)

    def _get_is_in_bunker_shot_move(self):
        return self.is_in_sideways_shot_move

    def _on_death(self, *arg):
        self.stop_shot_move()

    def _sideways_stand_tick(self):
        self._move_tick_count -= 1
        is_end = self._moved_offset.length >= self._target_move_offset.length or self._move_tick_count == 0
        if not is_end:
            if self.part_cam:
                cur_height = self.part_cam.cam.world_position.y
                height_move = cur_height - self._start_camera_height
                self.update_remain_camera_offset(math3d.vector(0, height_move, 0))
            else:
                self.update_remain_camera_offset(self._move_tick_speed)
                self._moved_offset += self._move_tick_speed
        else:
            self._moved_offset = self._target_move_offset
            self.end_sideways_shot_move()

    def interrupt_bunker_shot_move(self):
        self.stop_shot_move()
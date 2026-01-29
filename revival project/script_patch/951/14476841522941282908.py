# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComJumpLobbyBase.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import common.utils.timer as timer
import time
import world
from logic.gcommon.cdata import jump_physic_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import math3d
import math

class ComJumpLobbyBase(UnitCom):
    JUMP_STATE = ()
    BIND_EVENT = {'E_JUMP_MOVE': '_move_toward',
       'G_IS_JUMP': '_is_jump',
       'E_CLEAR_JUMP_ACC': '_clear_jump_acceleration',
       'E_MOVE_STOP': '_move_stop'
       }

    def __init__(self):
        super(ComJumpLobbyBase, self).__init__()
        self._jump_acceleration_timer_id = None
        self._jump_acceleration_start_velocity = math3d.vector(0, 0, 0)
        self._last_jump_yaw = 0
        self._last_jump_acceleration = math3d.vector(0, 0, 0)
        self._acceleration = 0
        self._forbid_horizon_acc_speed = 0
        self._max_fall_horizon_delta_speed = 0
        self._cur_speed = math3d.vector(0, 0, 0)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComJumpLobbyBase, self).init_from_dict(unit_obj, bdict)
        from logic.gcommon.cdata import speed_physic_arg
        self._acceleration = speed_physic_arg.acceleration
        self._forbid_horizon_acc_speed = jump_physic_config.fall_speed_to_jump * NEOX_UNIT_SCALE

    def reset(self):
        super(ComJumpLobbyBase, self).reset()

    def destroy(self):
        super(ComJumpLobbyBase, self).destroy()

    def _is_jump(self):
        return False

    def _move_toward(self, move_dir):
        if self.ev_g_is_jump():
            character = self.sd.ref_character
            if character and character.isJumping():
                if character.verticalVelocity >= self._forbid_horizon_acc_speed:
                    if not self._jump_acceleration_timer_id:
                        self._begin_jump_acceleration()
                    self._last_jump_acceleration = move_dir

    def _move_stop(self):
        self._clear_jump_acceleration()

    def _on_ground_finish(self):
        pass

    def _begin_jump_acceleration(self):
        rock_dir = self.ev_g_rock_move_dir()
        if rock_dir is None:
            return
        else:
            self._jump_acceleration_start_velocity = rock_dir
            self._cur_speed = self._jump_acceleration_start_velocity
            normalized_rock_dir = math3d.vector(rock_dir)
            if not normalized_rock_dir.is_zero:
                normalized_rock_dir.normalize()
            self._last_jump_acceleration = normalized_rock_dir
            self._last_jump_yaw = self.ev_g_yaw()
            if not self._jump_acceleration_timer_id:
                self._jump_acceleration_timer_id = global_data.game_mgr.register_logic_timer(self._jump_acceleration_tick, 0.1, times=-1, mode=timer.CLOCK, timedelta=True)
            return

    def _jump_acceleration_tick(self, dt, *args):
        character = self.sd.ref_character
        if not character:
            self._jump_acceleration_timer_id = None
            return timer.RELEASE
        else:
            if character.verticalVelocity < self._forbid_horizon_acc_speed:
                self._jump_acceleration_timer_id = None
                return timer.RELEASE
            total_add_speed = self._cur_speed - self._jump_acceleration_start_velocity
            if self._max_fall_horizon_delta_speed > 0 and total_add_speed.length_sqr >= self._max_fall_horizon_delta_speed * self._max_fall_horizon_delta_speed:
                self._jump_acceleration_timer_id = None
                return timer.RELEASE
            delta_speed_magnitude = self._acceleration * dt
            delta_speed = self._last_jump_acceleration * delta_speed_magnitude
            self._cur_speed = self._cur_speed + delta_speed
            if self._max_fall_horizon_delta_speed > 0:
                speed_value = self._cur_speed.length
                if speed_value > self._max_fall_horizon_delta_speed:
                    self._cur_speed.normalize()
                    self._cur_speed = self._cur_speed * self._max_fall_horizon_delta_speed
            world_move_dir = self._cur_speed * math3d.matrix.make_rotation_y(self._last_jump_yaw)
            self.send_event('E_CHARACTER_WALK', world_move_dir)
            return

    def _clear_jump_acceleration(self):
        self._jump_acceleration_start_velocity = math3d.vector(0, 0, 0)
        self._last_jump_acceleration = math3d.vector(0, 0, 0)
        self._clean_jump_acc_timer()

    def _clean_jump_acc_timer(self):
        if self._jump_acceleration_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._jump_acceleration_timer_id)
        self._jump_acceleration_timer_id = None
        return
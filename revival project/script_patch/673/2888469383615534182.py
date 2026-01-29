# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMoveForce.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import world
import math3d
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.cdata import status_config
import time
import common.utils.timer as timer
import C_file
import logic.gcommon.common_const.skill_const as kconst
import math
from logic.gutils import track_reader
track_data = [
 (
  0.0, (0, 0, 0)), (0.1, (0, 0, 3.0)), (0.2, (0, 0, 4.5))]
force_move = [
 (
  0.0, (0, 0, 0)), (0.1, (0, 0, 3.0)), (0.15, (0, 0, 4.5))]
tick_time = 0.03333

class ComMoveForce(UnitCom):
    BIND_EVENT = {'E_MOVE_FORCE': 'on_move_force_by_yaw',
       'E_MOVE_FORCE_VECT': 'on_move_force_by_vector'
       }

    def __init__(self):
        super(ComMoveForce, self).__init__()
        self._track_reader = track_reader.TrackReader()
        self._start_time = 0.0
        self._last_pos = None
        self._recoil_timer_id = None
        self._cur_time = 0.0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMoveForce, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        pass

    def destroy(self):
        super(ComMoveForce, self).destroy()

    def on_move_force_by_yaw(self, yaw=0.0, distance=30.0, track_data=track_data):
        vector = math3d.vector(-math.sin(yaw), 0.0, -math.cos(yaw))
        self.on_move_force_by_vector(vector, distance, track_data)

    def on_move_force_by_vector(self, vector, distance=30.0, track_data=force_move):
        start_pos = self.ev_g_position()
        if not start_pos:
            return
        end_pos = start_pos + vector * distance
        self._track_reader.read_track('', vector, start_pos, end_pos, track_data)
        if self._recoil_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._recoil_timer_id)
        self._cur_time = 0.0
        self._last_pos = start_pos
        self._recoil_timer_id = global_data.game_mgr.register_logic_timer(self.tick, 1, mode=timer.LOGIC)

    def tick(self):
        self._cur_time += tick_time
        track_pos, is_end = self._track_reader.get_cur_pos(self._cur_time)
        dist_dir = track_pos - self._last_pos
        dist_dir.x /= tick_time
        dist_dir.z /= tick_time
        self.send_event('E_CHARACTER_WALK_FORCE', dist_dir)
        self.send_event('E_ACTION_SYNC_VEL', dist_dir)
        self._last_pos = track_pos
        if is_end:
            global_data.game_mgr.unregister_logic_timer(self._recoil_timer_id)
            self._recoil_timer_id = None
            self.send_event('E_CHARACTER_WALK_FORCE', math3d.vector(0, 0, 0))
            self.send_event('E_ACTION_CHECK_POS', stop=True)
        return
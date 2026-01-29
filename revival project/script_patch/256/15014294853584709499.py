# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_bunker/ComBunkerSidewaysCam.py
from __future__ import absolute_import
import time
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

class ComBunkerSidewaysCam(UnitCom):
    BIND_EVENT = {'G_BUNKER_CAMERA_OFFSET': 'get_bunker_camera_offset',
       'S_BUNKER_CAMERA_OFFSET': 'set_bunker_camera_offset',
       'S_BUNKER_CAMERA_SMOOTH_OFFSET': '_set_bunker_camera_smooth_offset'
       }

    def __init__(self):
        super(ComBunkerSidewaysCam, self).__init__()
        self._is_in_bksw_cam = False
        self._cur_bksw_offset = math3d.vector(0, 0, 0)
        self._cur_bksw_offset_speed = 0
        self._cur_sideways_camera_timer_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComBunkerSidewaysCam, self).init_from_dict(unit_obj, bdict)

    def on_init_complete(self):
        self.part_cam = self.scene.get_com('PartCamera')

    def destroy(self):
        super(ComBunkerSidewaysCam, self).destroy()

    def get_bunker_camera_offset(self):
        return self._cur_bksw_offset

    def set_bunker_camera_offset(self, new_offset):
        if self._cur_bksw_offset == new_offset:
            return
        if not new_offset or new_offset and new_offset.is_zero:
            self._is_in_bksw_cam = False
            self._cur_bksw_offset = math3d.vector(0, 0, 0)
        else:
            self._is_in_bksw_cam = True
            self._cur_bksw_offset = new_offset
        global_data.emgr.set_camera_world_offset_event.emit(self._cur_bksw_offset)

    def unregist_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._cur_sideways_camera_timer_id)

    def _set_bunker_camera_smooth_offset(self, cost_time):
        target_offset = self.ev_g_bunker_camera_target_offset()
        if target_offset == self._cur_bksw_offset:
            return
        if cost_time <= 0:
            self.set_bunker_camera_offset(target_offset)
            return
        self._start_time = time.time()
        self._slerp_cost_time = cost_time
        from logic.gcommon.common_const.animation_const import FRAMES_PER_SECOND
        update_interval = 1.0 / FRAMES_PER_SECOND
        self._slerp_offset_speed = (target_offset - self._cur_bksw_offset) * (1.0 / self._slerp_cost_time) * update_interval
        self.unregist_timer()
        from common.utils.timer import LOGIC
        t_id = global_data.game_mgr.register_logic_timer(self._camera_offset_tick, interval=1, times=-1, mode=LOGIC)
        if t_id:
            self._cur_sideways_camera_timer_id = t_id

    def _camera_offset_tick(self):
        _cur_bksw_offset = self._cur_bksw_offset + self._slerp_offset_speed
        cur_time = time.time()
        is_end = cur_time - self._start_time >= self._slerp_cost_time
        if is_end:
            self.unregist_timer()
            target_offset = self.ev_g_bunker_camera_target_offset()
            self.set_bunker_camera_offset(target_offset)
        else:
            self.set_bunker_camera_offset(_cur_bksw_offset)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/system/TickLodSystem.py
from __future__ import absolute_import
from .SystemBase import SystemBase, FPS_30
from ..client.ComDataAppearance import ComDataAppearance
from ..client.ComDataLogicLod import ComDataLogicLod
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
LOD_STEP = 30 * NEOX_UNIT_SCALE

class TickLodSystem(SystemBase):

    def __init__(self):
        super(TickLodSystem, self).__init__()
        self._timer_30fps = 0
        self._calc_flag = 0

    def interested_type(self):
        return (
         ComDataAppearance, ComDataLogicLod)

    def handler_types(self):
        return []

    def tick(self, dt):
        scn = world.get_active_scene()
        self._timer_30fps += dt
        dt_30fps = 0
        if self._timer_30fps > FPS_30:
            dt_30fps = self._timer_30fps
            self._timer_30fps = 0
        if scn:
            calc_count_this_frame = max(2, len(self._element_list) / 4)
            global_max_lod = global_data.global_max_lod
            cam_pos = scn.active_camera.world_position
            for unit in self._element_list:
                model_data = unit.sd.ref_appearance
                lod_data = unit.sd.ref_logic_lod
                lod_data.dt_full_fps = dt if lod_data.need_tick else lod_data.dt_full_fps + dt
                lod_data.need_tick = lod_data.dt_full_fps >= lod_data.logic_tick_step
                lod_data.dt_30_fps = dt_30fps if lod_data.need_tick_30fps else lod_data.dt_30_fps + dt_30fps
                lod_data.need_tick_30fps = lod_data.dt_30_fps >= lod_data.logic_tick_step
                if calc_count_this_frame and lod_data.calc_flag != self._calc_flag and model_data.model:
                    lod_data.calc_flag = self._calc_flag
                    lod_level = min(int((model_data.model.position - cam_pos).length / LOD_STEP), global_max_lod)
                    lod_data.logic_tick_step = lod_level * 0.015
                    calc_count_this_frame -= 1

            if calc_count_this_frame or self._element_list[-1].sd.ref_logic_lod == self._calc_flag:
                self._calc_flag = 1 - self._calc_flag

    def add_handler(self, handler_type, handler):
        raise NotImplementedError()

    def remove_handler(self, handler_type, handler):
        raise NotImplementedError()
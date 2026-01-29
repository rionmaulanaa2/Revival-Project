# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGridManager.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import time_utility
import world
GRID_WIDTH = 5000

class CGridManager:

    def __init__(self):
        self.init_parameters()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.grid_manager = None
        return

    def init_parameters(self):
        self.grid_manager = world.gridobject_manager(GRID_WIDTH)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def add_to_grid(self, id, pos):
        self.grid_manager.add_obj(str(id), pos)

    def update_pos(self, id, pos):
        self.grid_manager.remove_obj(str(id))
        self.grid_manager.add_obj(str(id), pos)

    def del_from_grid(self, id):
        self.grid_manager.remove_obj(str(id))

    def get_grid_list(self, pos):
        grid_list = self.grid_manager.acquire_obj_list(pos)
        return grid_list

    def get_inside_occupy_zone(self, pos):
        if not pos:
            return []
        grid_list = self.get_grid_list(pos)
        insides_occupy_zone = []
        occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
        for occupy_id in grid_list:
            occupy_data = occupy_cfg.get(str(occupy_id), {})
            area = occupy_data.get('area')
            if area:
                left_bottom_pos = area[0]
                right_top_pos = area[1]
                if left_bottom_pos[0] <= pos.x <= right_top_pos[0] and left_bottom_pos[1] <= pos.z <= right_top_pos[1]:
                    insides_occupy_zone.append(occupy_id)

        return insides_occupy_zone
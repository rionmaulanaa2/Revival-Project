# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/SysMapAirlineMgr.py
from __future__ import absolute_import
import six
import six_ex
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
from logic.gcommon.const import AIRLINE_AIRSHIP
import math3d
import cc
AIRLINE_COLOR = cc.Color4F(0.5, 0.5, 0, 1)
AIRLINE_WIDTH = 3
AIRLINE_ID = 0

class SysMapAirlineMgr(ScenePartSysBase):

    def __init__(self):
        super(SysMapAirlineMgr, self).__init__()
        self.airline_map = {}
        self.init_event()

    def add_airline(self, entity_id, start_pos, end_pos):
        if entity_id in self.airline_map:
            return
        self.airline_map[entity_id] = (
         start_pos, end_pos)
        global_data.emgr.scene_airline_changed_event.emit(entity_id, self.airline_map[entity_id])

    def del_airline(self, entity_id):
        if entity_id in self.airline_map:
            del self.airline_map[entity_id]
            global_data.emgr.scene_airline_changed_event.emit(entity_id, None)
        return

    def del_airship_airline(self):
        del_ids = []
        for k, v in six.iteritems(self.airline_map):
            if v[0] == AIRLINE_AIRSHIP:
                del_ids.append(k)

        for k in del_ids:
            self.del_airline(k)

    def del_all_airline(self):
        del_ids = six_ex.keys(self.airline_map)
        for k in del_ids:
            self.del_airline(k)

    def on_ctrl_target_changed(self, target, *args):
        self.del_airship_airline()
        if target.__class__.__name__ == 'Airship':
            if target and target.logic:
                path = target.logic.ev_g_move_path()
                if not path:
                    return
                self.add_airline(target.entity_id, AIRLINE_AIRSHIP, math3d.vector(*path[0]), math3d.vector(*path[1]), True)

    def init_event(self):
        global_data.emgr.scene_add_airline_event += self.add_airline
        global_data.emgr.scene_del_airline_event += self.del_airline
        global_data.emgr.switch_control_target_event += self.on_ctrl_target_changed
        global_data.emgr.on_battle_status_changed += self.on_battle_status_changed

    def on_battle_status_changed(self, status):
        battle = global_data.battle
        if not battle:
            return
        flight_dict = battle.flight_dict
        if not flight_dict:
            return
        if status in (battle.BATTLE_STATUS_PREPARE, battle.BATTLE_STATUS_PARACHUTE):
            self.add_airline(AIRLINE_ID, math3d.vector(*flight_dict['start_pos']), math3d.vector(*flight_dict['end_pos']))
        else:
            self.del_airline(AIRLINE_ID)

    def destroy(self):
        self.del_all_airline()
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/QTELocalBattle.py
from __future__ import absolute_import
import math3d
import collision
from logic.entities.Battle import Battle
from mobile.common.EntityManager import Dynamic
from mobile.common.EntityManager import EntityManager
from data.c_guide_data import GetLocalGuideParams
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, TERRAIN_MASK, REGION_SCENE_GROUP
BARRIER_POLY = [
 math3d.vector(1, 0, 0),
 math3d.vector(0, 0, 1),
 math3d.vector(-1, 0, 0),
 math3d.vector(0, 0, -1)]

@Dynamic
class QTELocalBattle(Battle):
    TICK_INTERVAL = 1

    def __init__(self, entityid):
        super(QTELocalBattle, self).__init__(entityid)
        self._mecha_charger = None
        self._tick_total = 0
        self.area_id = None
        self.local_barriers = []
        self._min_x = None
        self._max_x = None
        self._min_z = None
        self._max_z = None
        return

    def init_from_dict(self, bdict):
        self.init_from_dict_base(bdict)

    def load_finish(self):
        scene = self.get_scene()
        scene.scene_data.update({'view_range': 2000})
        scene.modify_view_range(2000)
        self.create_barriers()
        super(QTELocalBattle, self).load_finish()

    def on_destroy(self):
        self.clear_barriers()

    def init_battle_scene(self, scene_data):
        from logic.gcommon.common_utils import parachute_utils
        parachute_stage = self._save_init_bdict.get('parachute_stage', None)
        preload_cockpit = parachute_utils.is_flying(parachute_stage)
        scene_data.update({'preload_cockpit': preload_cockpit})
        scene_data.update({'battle_need_preload_effect_cache': True})
        self.load_scene(scene_data)
        return

    def tick(self, dt):
        super(QTELocalBattle, self).tick(dt)
        self._tick_total += dt
        if self._tick_total < QTELocalBattle.TICK_INTERVAL:
            return
        self._tick_total -= QTELocalBattle.TICK_INTERVAL
        self.mecha_charger_check()

    def record_mecha_charger(self, charger_id):
        self._mecha_charger = charger_id

    def mecha_charger_check(self):
        if self._mecha_charger is None:
            return
        else:
            charger = EntityManager.getentity(self._mecha_charger)
            if not (charger and charger.logic):
                return
            charger.logic.send_event('E_LBS_CHARGER_CHECK')
            return

    def create_barriers(self):
        map_info = GetLocalGuideParams()
        barrier_pos = map_info['barrier_pos']['var_val']
        barrier_pos = math3d.vector(*barrier_pos)
        barrier_size = map_info['barrier_size']['var_val']
        barrier_range = map_info['barrier_range']['var_val']
        for _, direction in enumerate(BARRIER_POLY):
            pos = barrier_pos + direction * barrier_range * NEOX_UNIT_SCALE
            size = math3d.vector(barrier_size[0] * NEOX_UNIT_SCALE, barrier_size[1] * NEOX_UNIT_SCALE, barrier_size[2] * NEOX_UNIT_SCALE)
            barrier = collision.col_object(collision.BOX, size, 0, 0, 0, True)
            barrier.position = pos
            mask = TERRAIN_MASK
            group = REGION_SCENE_GROUP
            barrier.mask = mask
            barrier.group = group
            barrier.rotation_matrix = math3d.matrix.make_orient(direction, math3d.vector(0, 1, 0))
            global_data.game_mgr.scene.scene_col.add_object(barrier)
            self.local_barriers.append(barrier)
            pos_limit = barrier_pos + direction * (barrier_range - 3) * NEOX_UNIT_SCALE
            if self._min_x is None or self._min_x > pos_limit.x:
                self._min_x = pos_limit.x
            if self._max_x is None or self._max_x < pos_limit.x:
                self._max_x = pos_limit.x
            if self._min_z is None or self._min_z > pos_limit.z:
                self._min_z = pos_limit.z
            if self._max_z is None or self._max_z < pos_limit.z:
                self._max_z = pos_limit.z

        return

    def clear_barriers(self):
        for barrier in self.local_barriers:
            global_data.game_mgr.scene.scene_col.remove_object(barrier)

        self.local_barriers = []

    def get_barrier_range(self):
        return (
         self._min_x, self._max_x, self._min_z, self._max_z)
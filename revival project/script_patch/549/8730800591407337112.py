# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/survival/CarryManager.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from logic.client.const import game_mode_const
from common.utils import timer
from logic.comsys.battle.Death.DeathBattleUtils import pnpoly
from logic.comsys.archive import archive_key_const
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import collision_const
import game3d
import math3d
import collision
DEFAULT_RAY_LENGTH = 8 * NEOX_UNIT_SCALE

class CarryManager(Singleton):
    ALIAS_NAME = 'carry_mgr'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.ZERO_VECTOR = math3d.vector(0, 0, 0)
        self._bases = set()
        self._player_rel_pos_timer = None
        self._player_rel_info = [None, None]
        self._train_head_ids = []
        self._train_stations = {}
        self._train_carriage_ids = []
        return

    def reset(self):
        self._bases.clear()
        self._train_head_ids = []
        self._train_stations = {}
        self._train_carriage_ids = []
        if self._player_rel_pos_timer:
            global_data.game_mgr.unregister_logic_timer(self._player_rel_pos_timer)
            self._player_rel_pos_timer = None
        return

    def on_finalize(self):
        self.reset()

    def _on_battle_begin(self):
        self.reset()

    def exit_battle(self):
        self.reset()

    def enter_battle(self):
        self.reset()
        self._player_rel_pos_timer = global_data.game_mgr.register_logic_timer(self.update_player_rel_pos, 0.1, mode=timer.CLOCK)

    def update_player_rel_pos(self):
        if not global_data.player or not global_data.player.logic:
            return
        player_pos = global_data.player.logic.ev_g_position()
        if not player_pos:
            return
        self._player_rel_info = self.get_valid_relative_pos(player_pos)

    @property
    def player_rel_info(self):
        return self._player_rel_info

    def get_bases_under_pos(self, pos, ray_length=DEFAULT_RAY_LENGTH):
        if not self._bases:
            return None
        else:
            cols = set()
            ans = set()
            start = pos
            end = math3d.vector(pos.x, pos.y - DEFAULT_RAY_LENGTH, pos.z)
            start.y += 0.2 * NEOX_UNIT_SCALE
            ress = global_data.game_mgr.scene.scene_col.hit_by_ray(start, end, -1, -1, collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER, True)
            if ress and ress[0]:
                for res in ress[1]:
                    cols.add(res[4])

            if not cols:
                return False
            for ent_id in self._bases:
                ent = global_data.battle.get_entity(ent_id)
                if not ent or not ent.logic:
                    continue
                if ent.logic.ev_g_col() in cols:
                    ans.add(ent.id)

            return ans

    def get_base_under_pos(self, pos, ray_length=DEFAULT_RAY_LENGTH):
        if not self._bases:
            return None
        else:
            cols = set()
            start = math3d.vector(pos.x, pos.y, pos.z)
            end = math3d.vector(pos.x, pos.y - 15 * NEOX_UNIT_SCALE, pos.z)
            start.y += 3 * NEOX_UNIT_SCALE
            ress = global_data.game_mgr.scene.scene_col.hit_by_ray(start, end, -1, -1, collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER, True)
            if ress and ress[0]:
                for res in ress[1]:
                    cols.add(res[4].cid)

            if not cols:
                return None
            for ent_id in self._bases:
                ent = global_data.battle.get_entity(ent_id)
                if not ent or not ent.logic:
                    continue
                if ent.logic.ev_g_col_id() in cols:
                    return ent

            return None

    def get_valid_relative_pos(self, pos, ray_length=DEFAULT_RAY_LENGTH):
        under_ent = self.get_base_under_pos(pos, ray_length)
        if not under_ent:
            return (None, None)
        else:
            rel_pos = self.get_relative_pos(pos, under_ent)
            if rel_pos:
                return (under_ent.id, rel_pos)
            return (None, None)
            return None

    def get_relative_pos(self, world_pos, par_obj):
        rel_pos = self.world_to_relative(world_pos, par_obj.logic.ev_g_trans())
        if not rel_pos:
            return None
        else:
            return rel_pos

    def relative_to_world(self, rel_coor, par_trans):
        if not rel_coor or not par_trans:
            return None
        else:
            return rel_coor * par_trans

    def world_to_relative(self, world_coor, par_trans):
        if not world_coor or not par_trans:
            return None
        else:
            par_trans.inverse()
            return world_coor * par_trans

    def register_base_ent(self, ent_id):
        if ent_id not in self._bases:
            self._bases.add(ent_id)

    def unregister_base_ent(self, ent_id):
        if ent_id in self._bases:
            self._bases.remove(ent_id)

    def have_base_ent(self):
        if self._bases:
            return True
        else:
            return False

    def add_train_id(self, id):
        self._train_head_ids.append(id)

    def add_train_carriage_id(self, id):
        self._train_carriage_ids.append(id)

    def get_train_ids(self):
        return self._train_head_ids

    def add_train_station(self, id, eid):
        self._train_stations[id] = eid

    def get_train_station(self, id):
        return self._train_stations.get(id)

    def get_nearest_station_id(self, train_pos):
        if not self._train_stations:
            return
        else:
            tmp_dis = 99999
            nearest_station_id = None
            for key, val in six.iteritems(self._train_stations):
                eid, trk_dis = val
                tmp_ent = global_data.battle.get_entity(eid)
                if not tmp_ent or not tmp_ent.logic:
                    return
                tmp_station_pos = tmp_ent.logic.ev_g_position()
                vec_length = tmp_station_pos - train_pos
                if vec_length != self.ZERO_VECTOR:
                    dis = vec_length.length
                else:
                    dis = 0
                if dis < tmp_dis:
                    nearest_station_id = key
                    tmp_dis = dis

            return nearest_station_id

    def is_player_on_train(self):
        cols = []
        if not global_data.player or not global_data.player.logic:
            return (False, None)
        else:
            ctrl_target = global_data.player.logic.ev_g_control_target()
            if ctrl_target and ctrl_target.logic:
                pos = ctrl_target.logic.ev_g_position()
                start = math3d.vector(pos.x, pos.y, pos.z)
                end = math3d.vector(pos.x, pos.y - 8 * NEOX_UNIT_SCALE, pos.z)
                start.y += 0.2 * NEOX_UNIT_SCALE
                ress = global_data.game_mgr.scene.scene_col.hit_by_ray(start, end, -1, -1, collision_const.GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER, True)
                if ress and ress[0]:
                    for res in ress[1]:
                        cols.append(res[4])

            if not cols:
                return (False, None)
            for train_carriage_id in self._train_carriage_ids:
                tmp_train_carriage = global_data.battle.get_entity(train_carriage_id)
                if tmp_train_carriage and tmp_train_carriage.logic:
                    if tmp_train_carriage.logic.ev_g_col() in cols:
                        return (True, tmp_train_carriage)

            return (
             False, None)

    def get_player_rel_pos_to_train(self):
        on_train, train_carriage = self.is_player_on_train()
        if not on_train or not train_carriage or not train_carriage.logic:
            return (None, None)
        else:
            valid_pos_vec = global_data.player.logic.ev_g_position()
            rel_pos = train_carriage.logic.ev_g_relative_pos(valid_pos_vec)
            return (
             rel_pos, train_carriage.id)
            return None
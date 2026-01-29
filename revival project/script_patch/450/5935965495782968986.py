# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainStationClient.py
from __future__ import absolute_import
from logic.gcommon.common_const import battle_const
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.utility import log_debug
import world
import collision
import math3d
import game3d
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
from common.cfg import confmgr
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class ComTrainStationClient(UnitCom):
    TRAIN_STATION_MARK_IDS = [
     2035, 2036, 2037, 2038]
    BIND_EVENT = {'G_POSITION': 'get_position'
       }

    def __init__(self):
        super(ComTrainStationClient, self).__init__()
        self._station_no = None
        self._pos = None
        self._vec_pos = None
        self._x_range = None
        self._z_range = None
        self._half_idle_time = None
        self._train_station_dis = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_train_station_changed': self.on_train_station_changed,
           'on_train_pre_arrival': self.on_train_pre_arrival
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainStationClient, self).init_from_dict(unit_obj, bdict)
        self._station_no = bdict.get('station_no')
        self._pos = bdict.get('position')
        self._vec_pos = math3d.vector(*self._pos)
        self.init_mark()
        lb, rt = confmgr.get('train_node_data', str(self._station_no), 'station_range', default=[None, None])
        self._x_range = [min(lb[0], rt[0]), max(lb[0], rt[0])]
        self._z_range = [min(lb[1], rt[1]), max(lb[1], rt[1])]
        self._half_idle_time = confmgr.get('train_data', '1', 'idle_duration', default=20) / 2
        self._train_station_dis = confmgr.get('train_node_data', str(self._station_no), 'track_dis')
        global_data.carry_mgr.add_train_station(self._station_no, [self.unit_obj.id, self._train_station_dis])
        self.process_event(True)
        return

    def recreate_train_mark(self):
        train_head_ids = global_data.carry_mgr.get_train_ids()
        for train_head_id in train_head_ids:
            tmp_train_head = global_data.battle.get_entity(train_head_id)
            if tmp_train_head and tmp_train_head.logic:
                tmp_train_head.logic.send_event('E_RECREAT_MARK')

    @execute_by_mode(False, (game_mode_const.GAME_MODE_TRAIN,))
    def init_mark(self):
        if self._station_no >= len(self.TRAIN_STATION_MARK_IDS):
            return
        global_data.emgr.scene_add_client_mark.emit(self.unit_obj.id, self.TRAIN_STATION_MARK_IDS[self._station_no - 1], self._vec_pos)
        self.recreate_train_mark()

    @execute_by_mode(False, (game_mode_const.GAME_MODE_TRAIN,))
    def on_train_pre_arrival(self, train_pos):
        if not train_pos:
            return
        else:
            player_pos = global_data.player.logic.ev_g_position()
            if global_data.carry_mgr.get_nearest_station_id(train_pos) != self._station_no:
                return
            if not self.in_station_range(player_pos):
                return
            global_data.emgr.show_human_tips.emit(17283, 3, cb=None)
            return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_TRAIN,))
    def on_train_station_changed(self, train_state, train_pos):
        if not train_pos:
            return
        else:
            player_pos = global_data.player.logic.ev_g_position()
            if global_data.carry_mgr.get_nearest_station_id(train_pos) != self._station_no:
                return
            if not self.in_station_range(player_pos):
                return
            if train_state == battle_const.KD_TRAIN_START_PRE_SPEED_UP:
                global_data.emgr.show_human_tips.emit(17282, 3, cb=None)
            return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_TRAIN,))
    def try_show_hint(self, train_state, train_pos):
        if not train_pos:
            return
        else:
            player_pos = global_data.player.logic.ev_g_position()
            if global_data.carry_mgr.get_nearest_station_id(train_pos) != self._station_no:
                return
            if not self.in_station_range(player_pos):
                return
            if train_state == battle_const.KD_TRAIN_START_PRE_SPEED_UP:
                global_data.emgr.show_human_tips.emit(17282, 3, cb=None)
            return

    def destroy(self):
        super(ComTrainStationClient, self).destroy()
        self.process_event(False)

    def get_position(self):
        return self._vec_pos

    def in_station_range(self, pos):
        if not pos:
            return False
        if not self._x_range[0] <= pos.x <= self._x_range[1]:
            return False
        if not self._z_range[0] <= pos.z <= self._z_range[1]:
            return False
        return True
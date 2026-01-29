# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainClient.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import collision
import math3d
import game3d
import logic.gcommon.cdata.status_config as status_config
import weakref
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import battle_const

class ComTrainClient(UnitCom):
    BIND_EVENT = {'E_TRAIN_MOVE': 'sync_train_move',
       'E_TRAIN_START_SPEED_UP': '_on_train_change_state',
       'E_TRAIN_START_SPEED_REDUCE': '_on_train_change_state',
       'E_TRAIN_START_SPEED_MAINTAIN': '_on_train_change_state',
       'E_TRAIN_START_CHANGE': '_on_train_change_state',
       'E_TRAIN_STATE_CTRL_STATE': '_on_train_change_ctrl_state',
       'E_TRAIN_STATE_HEAL': '_on_train_heal_state_change',
       'E_TRAIN_STATE_DAMAGE': '_on_train_damage_state_change',
       'E_TRAIN_STATE_DO_SKILL': '_on_train_do_skill'
       }

    def __init__(self):
        super(ComTrainClient, self).__init__()
        self._carriage_ids = None
        self._train_no = None
        self._speed = None
        self._acc_time = None
        self._dis = None
        self._carriage_lengths = None
        self._carriage_offsets = None
        self._target_dis = None
        self._target_time = None
        self._rail_length = None
        self._do_move_action = False
        self._update_timer_id = None
        self.last_player_pos = None
        self._train_state = None
        self._train_ctrl_state = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainClient, self).init_from_dict(unit_obj, bdict)
        self._carriage_ids = bdict.get('carriage_ids')
        self._carriage_lengths = bdict.get('carriage_lengths')
        self._train_no = bdict.get('train_no')
        self._speed = bdict.get('speed', 10)
        self._acc_time = bdict.get('acc_time', 10)
        self._dis = bdict.get('dis')
        self._rail_length = bdict.get('rail_length')
        self._carriage_offsets = self.init_carriage_offset(self._carriage_lengths)
        tm = global_data.game_mgr.get_fix_logic_timer()
        self._update_timer_id = tm.register(func=self.do_move, interval=1, timedelta=True)
        self._train_state = bdict.get('client_state', battle_const.KD_TRAIN_START_SPEED_REDUCE)
        self._on_train_change_state(self._train_state)
        global_data.emgr.on_train_loaded.emit()

    def init_carriage_offset(self, carriage_lengths):
        total_offset = 0
        offsets = []
        for i in range(len(carriage_lengths)):
            if i > 0:
                total_offset += carriage_lengths[i - 1] / 2 + carriage_lengths[i] / 2
            offsets.append(total_offset)

        return offsets

    def destroy(self):
        super(ComTrainClient, self).destroy()
        if self._update_timer_id:
            tm = global_data.game_mgr.get_fix_logic_timer()
            tm.unregister(self._update_timer_id)

    def sync_train_move(self, dis, time):
        if dis == self._target_dis:
            return
        self._target_dis = dis
        self._target_time = time
        self._do_move_action = True

    def _on_train_change_state(self, state):
        self._train_state = state
        for i in range(len(self._carriage_ids)):
            tmp_carriage_id = self._carriage_ids[i]
            tmp_carriage = global_data.battle.get_entity(tmp_carriage_id)
            if not tmp_carriage or not tmp_carriage.logic:
                continue
            tmp_carriage.logic.send_event('E_CHANGE_CARRIAGE_STATE', state)

    def _on_train_change_ctrl_state(self, state):
        if not self._carriage_ids:
            return
        carriage_head = global_data.battle.get_entity(self._carriage_ids[0])
        if not carriage_head or not carriage_head.logic:
            return
        carriage_head.logic.send_event('E_CHANGE_CARRIAGE_CTRL_STATE', state)

    def _on_train_heal_state_change(self, enable, group):
        if not self._carriage_ids:
            return
        carriage_head = global_data.battle.get_entity(self._carriage_ids[0])
        if not carriage_head or not carriage_head.logic:
            return
        carriage_head.logic.send_event('E_CHANGE_CARRIAGE_HEAL', enable, group)

    def _on_train_damage_state_change(self, enable, group):
        if not self._carriage_ids:
            return
        carriage_head = global_data.battle.get_entity(self._carriage_ids[0])
        if not carriage_head or not carriage_head.logic:
            return
        carriage_head.logic.send_event('E_CHANGE_CARRIAGE_DAMAGE', enable, group)

    def _on_train_do_skill(self, skill_id):
        if not self._carriage_ids:
            return
        carriage_head = global_data.battle.get_entity(self._carriage_ids[0])
        if not carriage_head or not carriage_head.logic:
            return
        carriage_head.logic.send_event('E_TRAIN_DO_SKILL', skill_id)

    def is_reach_target_node(self, target_dis, before_dis, after_dis):
        if after_dis >= target_dis >= before_dis:
            return True
        if after_dis >= target_dis + self._rail_length >= before_dis:
            return True
        return False

    def mod_rail_length(self, length):
        return length % self._rail_length

    def test(self, delta, train_speed):
        pos = global_data.player.logic.ev_g_position()
        if self.last_player_pos:
            dis = (pos - self.last_player_pos).length
            speed = dis / delta
        self.last_player_pos = pos

    def do_move(self, delta):
        if not self._do_move_action:
            return
        else:
            self._target_dis = float(self._target_dis)
            self._dis = float(self._dis)
            dis1 = float(self._target_dis) - float(self._dis)
            dis2 = self._target_dis + self._rail_length - self._dis
            total_dis = dis2 if abs(dis1) > abs(dis2) else dis1
            total_time = self._target_time - tutil.time()
            if total_time <= 0 or abs(total_dis) > 100:
                self._dis = self._target_dis
                self._do_move_action = False
                self.do_carriage_move(0, None)
                return
            tmp_speed = total_dis / total_time
            add_dis = delta * tmp_speed
            before_dis = self._dis
            self._dis += add_dis
            if self.is_reach_target_node(self._target_dis, before_dis, self._dis):
                tmp_speed = 0
                self._dis = self._target_dis
                self._do_move_action = False
            self._dis = self.mod_rail_length(self._dis)
            self.do_carriage_move(tmp_speed, delta)
            return

    def do_carriage_move(self, tmp_speed, delta):
        if not self._carriage_ids:
            return
        for i in range(len(self._carriage_ids)):
            tmp_carriage_id = self._carriage_ids[i]
            tmp_carriage = global_data.battle.get_entity(tmp_carriage_id)
            if not tmp_carriage or not tmp_carriage.logic:
                continue
            tmp_dis = self._dis - self._carriage_offsets[i]
            tmp_carriage.logic.send_event('E_DO_CARRIAGE_MOVE', tmp_dis, tmp_speed, delta, self._dis, self._target_dis)
# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/train_proto.py
from __future__ import absolute_import
from logic.gcommon.common_const import battle_const

def train_start_speed_up(synchronizer):
    synchronizer.send_event('E_TRAIN_START_SPEED_UP', battle_const.KD_TRAIN_START_SPEED_UP)


def train_start_speed_reduce(synchronizer):
    synchronizer.send_event('E_TRAIN_START_SPEED_REDUCE', battle_const.KD_TRAIN_START_SPEED_REDUCE)


def train_start_speed_maintain(synchronizer):
    synchronizer.send_event('E_TRAIN_START_SPEED_MAINTAIN', battle_const.KD_TRAIN_START_SPEED_MAINTAIN)


def train_change_state(synchronizer, state):
    synchronizer.send_event('E_TRAIN_START_CHANGE', state)


def train_add_cargo(synchronizer, cargo_id, rel_pos, carriage_id):
    synchronizer.send_event('E_ADD_CARGO', cargo_id, rel_pos, carriage_id)


def train_remove_cargo(synchronizer, cargo_id):
    synchronizer.send_event('E_REMOVE_CARGO', cargo_id)


def train_do_skill_succeed(synchronizer, soul_id, skill_id, player_name):
    synchronizer.send_event('E_TRAIN_STATE_DO_SKILL', skill_id)
    global_data.emgr.train_use_skill_succeed.emit(soul_id, skill_id, player_name)


def train_battle_update_power(synchronizer, soul_id, power):
    if global_data.cam_lplayer and global_data.cam_lplayer.id == soul_id:
        global_data.emgr.update_train_skill_prog.emit(power)


def train_move(synchronizer, dis, time):
    synchronizer.send_event('E_TRAIN_MOVE', dis, time)


def ctrl_train_change_state(synchronizer, state):
    synchronizer.send_event('E_TRAIN_STATE_CTRL_STATE', state)


def set_train_heal(synchronizer, enable, group):
    synchronizer.send_event('E_TRAIN_STATE_HEAL', enable, group)


def set_train_damage(synchronizer, enable, group):
    synchronizer.send_event('E_TRAIN_STATE_DAMAGE', enable, group)
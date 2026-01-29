# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/building_proto.py
from __future__ import absolute_import
import math3d

def on_building_enable(synchronizer, enable):
    synchronizer.send_event('E_BUILDING_ENABLE', enable)


def on_building_hp_change(synchronizer, hp):
    synchronizer.send_event('E_BUILDING_CHANGE_HP', hp)


def on_building_done(synchronizer):
    synchronizer.send_event('E_BUILDING_DONE')


def on_building_explode(synchronizer, is_explode):
    synchronizer.send_event('E_BUILDING_EXPLODE', is_explode)


def show_disturb_circle(synchronizer, show):
    synchronizer.send_event('E_SHOW_DISTURB_CIRCLE', show)


def building_prepare_shoot(synchronizer, shoot_key, target_id):
    synchronizer.send_event('E_SENTRYGUN_PREPARE', shoot_key, target_id)


def building_begin_aim(synchronizer, shoot_key, target_id):
    synchronizer.send_event('E_SENTRYGUN_AIM', shoot_key, target_id)


def jump_from_building(synchronizer, jump_args, npc_eid, bouncer_speed):
    from mobile.common.EntityManager import EntityManager
    elasticity = EntityManager.getentity(npc_eid)
    if not elasticity:
        return
    jump_args['npc_eid'] = npc_eid
    jump_args['bouncer_speed'] = bouncer_speed
    synchronizer.send_event('E_SUPER_JUMP', jump_args)


def update_used_player(synchronizer, player_list):
    synchronizer.send_event('E_UPDATE_USED_PLAYER', player_list)


def photon_tower_charge(synchronizer, charge_target, result):
    synchronizer.send_event('E_PHOTON_TOWER_CHARGE_INFO', charge_target, result)


def photon_tower_shoot(synchronizer, target_id, charge_tree_size):
    synchronizer.send_event('E_PHOTON_TOWER_SHOOT_INFO', target_id, charge_tree_size)


def photon_begin_aim(synchronizer, target_id, aim_result):
    synchronizer.send_event('E_PHOTON_TOWER_AIM_INFO', target_id, aim_result)


def machine_moving(synchronizer, tp_next_pos, t_start, t_moving, move_index):
    synchronizer.send_event('E_MACHINE_MOVING', math3d.vector(*tp_next_pos), t_start, t_moving, move_index)


def aerospace_early_launch_time(synchronizer, delta_time):
    synchronizer.send_event('E_MACHINE_MODIF_TIME', delta_time)


def oil_bottle_on_fire(synchronizer, fighter_id):
    synchronizer.send_event('E_OIL_BOTTLE_ON_FIRE', fighter_id)


def gm_switch_move(synchronizer, timestamp):
    synchronizer.send_event('E_GM_SWITCH_MOVE', timestamp)


def gm_rescale_target(synchronizer, scl_xyz):
    synchronizer.send_event('E_GM_RESCALE_TARGET', scl_xyz)


def pick_flag_succeed(synchronizer, picker_id, picker_faction):
    synchronizer.send_event('E_PICK_FLAG_SUCCEED', picker_id, picker_faction)


def recover_flag_succeed(synchronizer, holder_id, holder_faction, recover_pos, reason, before_pos):
    synchronizer.send_event('E_RECOVER_FLAG_SUCCEED', holder_id, holder_faction, recover_pos, reason, before_pos)


def start_flag2_plant(synchronizer):
    synchronizer.send_event('E_START_FLAG_PLANT')


def stop_flag2_plant(synchronizer):
    synchronizer.send_event('E_STOP_FLAG_PLANT')


def set_flag2_plant_point(synchronizer, point, total_point):
    synchronizer.send_event('E_SET_FLAG_PLANT_POINT', point, total_point)


def player_around_crystal_change(synchronizer, player_cnt):
    synchronizer.send_event('E_PLAYER_AROUND_CRYSTAL_CHANGE', player_cnt)


def on_crystal_stage_change(synchronizer, new_stage):
    synchronizer.send_event('CRYSTAL_STAGE_CHANGE', new_stage)


def pick_egg_succeed(synchronizer, picker_id, picker_faction):
    synchronizer.send_event('E_PICK_EGG_SUCCEED', picker_id, picker_faction)


def drop_egg_succeed(synchronizer, holder_id, holder_faction, recover_pos, reason, before_pos, pass_egg):
    synchronizer.send_event('E_DROP_EGG_SUCCEED', holder_id, holder_faction, recover_pos, reason, before_pos, pass_egg)


def update_nbomb_status(synchronizer, status):
    synchronizer.send_event('E_UPDATE_NBOMB_STATUS', status)
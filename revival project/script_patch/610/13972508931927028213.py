# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/mecha_effect_optimize_info.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from logic.gcommon.common_const.ui_operation_const import MECHA_EFFECT_LEVEL_MEDIUM, MECHA_EFFECT_LEVEL_HIGH, MECHA_EFFECT_LEVEL_ULTRA
from device_compatibility import PERF_FLAG_ANDROID_LOW, PERF_FLAG_ANDROID_MED, PERF_FLAG_ANDROID_HIGH, PERF_FLAG_IOS_LOW, PERF_FLAG_IOS_MED, PERF_FLAG_IOS_HIGH, get_device_perf_flag
LOD_LEVEL_TO_MAX_MECHA_EFFECT_LEVEL_MAP = {0: MECHA_EFFECT_LEVEL_ULTRA,
   1: MECHA_EFFECT_LEVEL_ULTRA,
   2: MECHA_EFFECT_LEVEL_HIGH,
   3: MECHA_EFFECT_LEVEL_MEDIUM
   }
PERF_FLAG_TO_MAX_MECHA_EFFECT_LEVEL_MAP = {PERF_FLAG_ANDROID_LOW: MECHA_EFFECT_LEVEL_MEDIUM,
   PERF_FLAG_ANDROID_MED: MECHA_EFFECT_LEVEL_ULTRA,
   PERF_FLAG_ANDROID_HIGH: MECHA_EFFECT_LEVEL_ULTRA,
   PERF_FLAG_IOS_LOW: MECHA_EFFECT_LEVEL_MEDIUM,
   PERF_FLAG_IOS_MED: MECHA_EFFECT_LEVEL_ULTRA,
   PERF_FLAG_IOS_HIGH: MECHA_EFFECT_LEVEL_ULTRA
   }
DEVICE_PERF_MAX_MECHA_EFFECT_LEVEL = None

def calculate_mecha_effect_level(setting_mecha_effect_level, lod_level, consider_device_perf_flag=False):
    global DEVICE_PERF_MAX_MECHA_EFFECT_LEVEL
    max_mecha_effect_level = LOD_LEVEL_TO_MAX_MECHA_EFFECT_LEVEL_MAP[lod_level]
    if consider_device_perf_flag:
        if DEVICE_PERF_MAX_MECHA_EFFECT_LEVEL is None:
            DEVICE_PERF_MAX_MECHA_EFFECT_LEVEL = PERF_FLAG_TO_MAX_MECHA_EFFECT_LEVEL_MAP[get_device_perf_flag()]
        return min(setting_mecha_effect_level, max_mecha_effect_level, DEVICE_PERF_MAX_MECHA_EFFECT_LEVEL)
    else:
        return min(setting_mecha_effect_level, max_mecha_effect_level)


DEBUG_MECHA_EFFECT_LEVEL = G_CLIENT_TRUNK
DEBUG_EVENT_REGISTERED = False
MECHA_EFFECT_LEVEL_MODIFY_RECORD = {}

def record_mecha_effect_level_modify_data(mecha_id, effect_id, index, level):
    if mecha_id not in MECHA_EFFECT_LEVEL_MODIFY_RECORD:
        MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id] = {}
    if effect_id not in MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id]:
        MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id][effect_id] = {}
    MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id][effect_id][index] = level


def _print_specific_mecha_effect_level_changed_record(mecha_id):
    print('=======================================\n\xe6\x9c\xba\xe7\x94\xb2\xe7\xbc\x96\xe5\x8f\xb7\xef\xbc\x9a{}\n'.format(mecha_id))
    effect_ids = six_ex.keys(MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id])

    def my_cmp(a, b):
        return six_ex.compare(int(a), int(b))

    effect_ids.sort(key=cmp_to_key(my_cmp))
    for effect_id in effect_ids:
        effect_level_data = MECHA_EFFECT_LEVEL_MODIFY_RECORD[mecha_id][effect_id]
        print('\xe7\x89\xb9\xe6\x95\x88\xe7\xbc\x96\xe5\x8f\xb7\xef\xbc\x9a{}'.format(effect_id))
        indices = six_ex.keys(effect_level_data)
        indices.sort(key=cmp_to_key(my_cmp))
        for index in indices:
            level = effect_level_data[index]
            print('\xe7\xac\xac {} \xe8\xa1\x8c\xe7\x89\xb9\xe6\x95\x88\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\xba\xef\xbc\x9a{}'.format(index, level))

        print('')

    print('=======================================')


def print_mecha_effect_level_changed_record(mecha_id=None):
    if mecha_id and mecha_id in MECHA_EFFECT_LEVEL_MODIFY_RECORD:
        _print_specific_mecha_effect_level_changed_record(mecha_id)
    else:
        for mecha_id in six.iterkeys(MECHA_EFFECT_LEVEL_MODIFY_RECORD):
            _print_specific_mecha_effect_level_changed_record(mecha_id)


def register_mecha_effect_level_debug_event():
    global DEBUG_EVENT_REGISTERED
    if DEBUG_MECHA_EFFECT_LEVEL and not DEBUG_EVENT_REGISTERED:
        DEBUG_EVENT_REGISTERED = True
        global_data.emgr.print_mecha_effect_level_changed_data += print_mecha_effect_level_changed_record
        global_data.emgr.set_specific_mecha_effect_level += record_mecha_effect_level_modify_data


USE_LOCAL_CACHE_EFFECT_ANIM = {4108: {
        'move', 'accelerate'},
   8001: {
        'shoot'},
   8002: {
        'sword_jump_aim_fire_02', 'sword_jump_aim_fire_01', 'sword_jump_01', 'sword_jump_aim_fire_03',
        'thrust_land_l', 'thrust_land_f'},
   8003: {
        'thrust_r', 'jump_wings', 'jump_01', 'thrust_b', 'air_move', 'thrust_l', 'thrust_f'},
   8004: {
        'thrust_f_02', 'hover', 'jump_01'},
   8009: {
        'shoot_m', 'run_s', 'run_start_r'},
   8010: {
        'shoot', 'transform_shoot', 's_transform_shoot'},
   8014: {
        'shoot', 'dash_shoot',
        'slash_chase', 'dash_air_f', 'jump_01',
        'slash01', 'slash02', 'slash03', 'air_slash01', 'air_slash02', 'air_slash03', 'air_slash04'},
   8015: {
        'run_start', 'dash_start_f'},
   8016: {
        'shoot_charge_f', 'shoot_charge_fl', 'run_stop', 'shoot_charge', 'dash_end', 'dash_shoot', 'jump_03'},
   8017: {
        'ball_start01', 'ball_start02',
        'dash_l_03', 'dash_l_02', 'dash_r_03', 'dash_r_02', 'dash_b_03', 'dash_b_02', 'dash_f_03', 'dash_f_02'},
   8018: {
        'shoot_01', 'shoot_02', 'shoot_03', 'shoot_04'}
   }
IGNORE_EFFECT_WHEN_INVISIBLE_ANIM_INDEX = {8001: {
        '3', '4', '5'},
   8002: {
        '3', '4', '5', '6', '7', '8'},
   8003: {
        '11', '12'},
   8004: {
        '9', '16', '17', '18', '19'},
   8005: {
        '9', '11', '12', '13', '14', '15'},
   8006: {
        '4', '6', '7', '9', '10', '11'},
   8007: {
        '6', '10', '11', '12', '13'},
   8008: {
        '5', '6', '7'},
   8009: {
        '3', '4', '5', '6', '7', '8', '9', '11', '13', '14', '15', '16', '17', '27', '28'},
   8010: {
        '2', '3', '4', '5', '7', '8', '10', '11', '13', '15'},
   8011: {
        '4', '6', '7', '8', '9', '10', '11', '13', '25', '26', '27', '28', '29', '30', '33'},
   8012: {
        '3', '4', '5'},
   8013: {
        '1', '2', '10', '11', '12'},
   8014: {
        '4', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'},
   8015: {
        '3', '4', '9', '11', '12', '13', '14', '15', '16', '19'},
   8016: {
        '18', '19', '21', '22', '26'},
   8017: {
        '1', '2', '3', '5', '16', '100', '101'},
   8018: {
        '10', '13', '15', '17', '19', '20', '21', '22'},
   8019: {
        '9', '11', '16', '17'},
   8020: {
        '3', '4', '5', '6', '14', '16'},
   8021: {
        '5', '6'},
   8022: {
        '5', '9', '100', '101', '102', '103', '104'},
   8023: {
        '7', '8', '12'},
   8024: {
        '1', '10'},
   8025: {
        '5', '6'},
   8029: {
        '3', '4'},
   8032: {
        '16', '19'}
   }
USE_SCRIPT_TRIGGER_ANIM_NAMES = {4108: {
        'move', 'accelerate'},
   8001: {
        'shoot', 'missile_02', 'jump_01'},
   8002: {
        'thrust_land_f', 'thrust_land_b', 'thrust_land_l', 'thrust_land_r'},
   8003: {
        'shoot', 'air_shoot', 'reload', 'air_reload',
        'air_move'},
   8004: {
        'move', 'run', 'run_01', 'shoot', 'reload'},
   8005: {
        'shoot', 'transform_shoot'},
   8006: {
        'shoot', 'jump1', 'jump4', 'rush_wei_start', 'rush_wei_idle', 'rush_wei_end', 'mount'},
   8007: {
        'shoot', 'reload', 'run', 'run_start'},
   8009: {
        'shoot_m', 'shoot_s_l', 'shoot_s_r', 'shoot_r_l', 'shoot_r_r', 'huoliquankai_02',
        'run_start_m', 'run_m', 'run_stop_m',
        'huoliquankai_move', 'shouder_rocket'},
   8010: {
        'shoot', 'transform_shoot', 's_transform_shoot',
        'transform_move', 's_transform_move', 'transform_dash',
        'second_shoot02', 'transform_second_shoot02', 's_transform_second_shoot02', 'transform_dash_s_shoot02'},
   8011: {
        'j_run', 'j_run_s01', 'j_guard_idle', 'j_idle', 'j_idle_s01', 'j_guard_idle_s01', 'j_jump_01',
        'q_dasha_01', 'q_dasha_02', 'q_dashb_01', 'q_dashb_02', 'q_jump_02q_superjump_01'},
   8014: {
        'shoot', 'dash_shoot',
        'dash_lod',
        'reload', 'dash_reload',
        'jump_01'},
   8015: {
        'storm_loop', 'run', 'run_start', 'runstop'},
   8016: {
        'aim', 'aim_charge', 'move', 'run', 'shoot', 'shoot_charge', 'shoot_charge_fl', 'shoot_charge_f'},
   8017: {
        'jump01'},
   8018: {
        'run'},
   8020: {
        'trans_move'},
   8021: {
        'shoot', 'reload', 'jump_01'},
   8022: {
        'move', 'shoot', 'dash_lod'},
   8023: {
        'snipe_jump_01', 'snipe_jump_02', 'snipe_jump_03',
        'snipe_dash_start_f', 'snipe_dash_start_b', 'snipe_dash_start_l', 'snipe_dash_start_r',
        'snipe_dash_loop_f', 'snipe_dash_loop_b', 'snipe_dash_loop_l', 'snipe_dash_loop_r',
        'snipe_dash_end_f', 'snipe_dash_end_b', 'snipe_dash_end_l', 'snipe_dash_end_r',
        'akimbo_jump_01', 'akimbo_jump_02', 'akimbo_jump_03',
        'akimbo_dash_start_f', 'akimbo_dash_start_b', 'akimbo_dash_start_l', 'akimbo_dash_start_r',
        'akimbo_dash_loop_f', 'akimbo_dash_loop_b', 'akimbo_dash_loop_l', 'akimbo_dash_loop_r',
        'akimbo_dash_end_f', 'akimbo_dash_end_b', 'akimbo_dash_end_l', 'akimbo_dash_end_r',
        'akimbo_reload', 'scope_move', 'scope_reload', 'scope_load', 'snipe_load'},
   8024: {
        'dash_05', 'shoot'},
   8025: {
        'dash_01', 'dash_02', 'move', 'shoot', 'reload'},
   8026: {
        'jump_01'},
   8027: {
        'shoot', 'reload', 'jump_01'},
   8028: {
        'girl_move', 'girl_up', 'girl_down', 'girl_reload', 'girl_shoot1', 'girl_shoot2', 'rabt_dash_move',
        'rabt_shoot1', 'rabt_shoot2', 'rabt_shoot_move_1', 'rabt_shoot_move_2', 'rabt_salvo_start', 'rabt_salvo_loop',
        'rabt_salvo_firend', 'rabt_reload', 'rabt_jump_start'},
   8029: {
        'rifle_shoot', 'shotgun_shoot'},
   8031: {
        'shoot', 'reload', 'move', 'move_reaper'},
   8032: {
        'shoot', 'move', 'stomp_05', 'charge'},
   8033: {
        'air_dash', 'reload', 'shoot'},
   8034: {
        'shoot', 'boom_fireend'},
   8035: {
        'dash_fly_start', 'dash_fly_loop', 'jump1'},
   8036: {
        'dash', 'dash_air', 'shoot_cluster', 'shoot_shotgun', 'reload'},
   8037: {
        'vice_loop', 'slash_02'}
   }

def _trans_anim_name_to_effect_id(data_for_anim_name, data_for_effect_id):
    for _mecha_id, _anim_name_set in six.iteritems(data_for_anim_name):
        data_for_effect_id[_mecha_id] = effect_id_set = set()
        anim_effect_id_map = confmgr.get('mecha_skin_{}_trigger_res'.format(_mecha_id), 'anim_id', default={})
        for anim_name in _anim_name_set:
            effect_id = anim_effect_id_map.get(anim_name, None)
            if effect_id is None:
                continue
            if effect_id not in effect_id_set:
                effect_id_set.add(effect_id)

    return


USE_LOCAL_CACHE_EFFECT_ID = {}
USE_SCRIPT_TRIGGER_EFFECT_ID = {}
_trans_anim_name_to_effect_id(USE_LOCAL_CACHE_EFFECT_ANIM, USE_LOCAL_CACHE_EFFECT_ID)
_trans_anim_name_to_effect_id(USE_SCRIPT_TRIGGER_ANIM_NAMES, USE_SCRIPT_TRIGGER_EFFECT_ID)
ENGINE_TRIGGER_DATA_INITIALIZED = False

def initialize_engine_trigger_data():
    global ENGINE_TRIGGER_DATA_INITIALIZED
    if ENGINE_TRIGGER_DATA_INITIALIZED:
        return
    else:
        ENGINE_TRIGGER_DATA_INITIALIZED = True
        for mecha_id in six.iterkeys(USE_SCRIPT_TRIGGER_EFFECT_ID):
            anim_effect_conf = confmgr.get('mecha_skin_{}_trigger_res'.format(mecha_id), 'anim_effect', default={})
            for effect_id, effect_info in six.iteritems(anim_effect_conf):
                only_one_valid_part = True
                valid_part = None
                for part, part_effect_list in six.iteritems(effect_info):
                    if not part_effect_list:
                        continue
                    if valid_part:
                        only_one_valid_part = False
                        break
                    valid_part = part

                if not only_one_valid_part:
                    USE_SCRIPT_TRIGGER_EFFECT_ID[mecha_id].add(effect_id)

        for mecha_id in six.iterkeys(USE_LOCAL_CACHE_EFFECT_ID):
            USE_LOCAL_CACHE_EFFECT_ID[mecha_id] &= USE_SCRIPT_TRIGGER_EFFECT_ID.get(mecha_id, set())

        return
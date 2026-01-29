# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/newbie_stage_utils.py
from __future__ import absolute_import
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from data.newbie_stage_config import GetWeaponDamage
import copy
GUIDE_PROCESS_MODE_ONLY_INIT = 1
GUIDE_PROCESS_MODE_ONLY_DESTROY = 2
NPC_MECHA_TYPE_2_INIT_DICT = {8001: {'init_max_hp': 2700,
          'shield': 0.0,
          'last_action': [
                        None, None],
          'creator': None,
          'mecha_sfx': None,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'cur_fuel': 100.0,
          'driver_id': None,
          'suspended': False,
          'seats': ('seat_1', ),
          'broken_times': 0,
          'born_time': 1559460064.397052,
          'passenger_dict': {},'npc_id': 8001,
          'idx_pool': {1: 19},'trans_pattern': 1,
          'shoot_mode': 1,
          'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 80,'item_type': 0,'attachment': {},'item_id': 800101},2: {'item_id': 800102,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'faction_id': 1,
          'max_shield': 500.0,
          'max_hp': 2700,
          'hp': 100,
          'immobilize_value': 0,
          'mp_attr': {'head_hit': 1.2,'body_hit': 1.0,'mileage': 0,'arm_hit': 1.0,'item_num': 0,'foot_hit': 1.0},'mecha_fashion': {'0': 201800100},'mecha_robot': True,
          'auto_join': False,
          'wp_bar_last_pos': 0,
          'wp_bar_cur_gun_pos': 2,
          'rage': 0,
          'skills': {800152: {'cost_fuel': 10,'cost_fuel_type': 1,'last_cast_time': 0,'outer_shield_lasting_time': 4,'outer_shield_hp': 300,
                              'speed_up_buff_id': 397,'effect_buff_id': 396,'inc_mp': 10,'mp': 100,
                              'speed_up_lasting_time': 3,'outer_shield_buff_id': 372,'max_mp': 100},
                     800153: {'last_cast_time': 0,'cost_fuel': 20,'cost_fuel_type': 1},800151: {'last_cast_time': 0,'inc_mp': 10,'max_mp': 100,'mp': 100}},
          'missile_lock': None,
          'mecha_id': 8001,
          't_rage_last': 0,
          'wp_bar_cur_pos': 2,
          'mp_explosive': {},'shapeshift': False,
          'set_st': 'set([])',
          'position': [],'fuel_regtime': 0
          },
   8005: {'init_max_hp': 2850,
          'shield': 0.0,
          'last_action': [
                        None, None],
          'creator': 0,
          'mecha_sfx': None,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'cur_fuel': 90.0,
          'driver_id': None,
          'max_fuel_dict': {},'suspended': False,
          'seats': [
                  'seat_1'],
          'broken_times': 0,
          'born_time': 1606718910.27,
          'passenger_dict': {},'npc_id': 8005,
          'vrf_status': [
                       113, 110],
          'temporary_shield_map': {},'shoot_mode': 1,
          'weapons': {1: {'count': 1,'ibolted': 1,'ibulletnum': 20,'item_type': 0,'attachment': {},'item_id': 800501},2: {'item_id': 800502,'item_type': 0,'ibulletnum': 0,'attachment': {},'count': 1},3: {'count': 1,'ibolted': 1,'ibulletnum': 6,'item_type': 0,'attachment': {},'item_id': 800503}},'faction_id': 0,
          'next_regtime_dict': {},'max_shield': 700.0,
          'max_hp': 2850,
          'hit_flag_value': {},'cur_fuel_dict': {},'hp': 100,
          'durative_cost': {},'mp_attr': {'mileage': 0,'arm_hit': 1.0,'foot_hit': 1.0,'head_hit': 1.5,'body_hit': 1.0,'item_num': 0},'mecha_fashion': {},'mecha_robot': True,
          'auto_join': False,
          'module_buff_data': {},'max_fuel': 90.0,
          'rage': 0,
          'skills': {800552: {'cost_fuel': 30,'max_fuel': 0,'cost_fuel_type': 1,'last_cast_time': 0,'jump_distance_rate': 1,'left_cast_cnt': 1,
                              'mp_stage': 0,'inc_mp': 10,'mp': 90,'init_inc_mp': 10,'max_mp': 90,'cost_mp': 90
                              },
                     800553: {'last_cast_time': 0,'cost_fuel': 18,'max_fuel': 0,'cost_fuel_type': 1},800551: {'last_cast_time': 0,'left_cast_cnt': 1,'mp_stage': 0,'inc_mp': 10,'mp': 80,'init_inc_mp': 10,'max_mp': 80,
                              'cost_mp': 80},
                     800855: {'last_cast_time': 0,'left_cast_cnt': 1,'mp_stage': 0,'inc_mp': 10,'mp': 135,'max_distance': 6,'init_inc_mp': 10,
                              'building_id': 6025,'max_mp': 135,'cost_mp': 135}
                     },
          'missile_lock': None,
          'mecha_custom_skin': {},'mecha_id': 8005,
          't_rage_last': 0,
          'trans_pattern': 1,
          'mp_explosive': {},'shapeshift': '',
          'position': [],'fuel_regtime': 0
          },
   8501: {'init_max_hp': 1500,
          'shield': 0,
          'creator': None,
          'mecha_sfx': None,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'cur_fuel': 100.0,
          'driver_id': None,
          'seats': [
                  'seat_1'],
          'born_time': 1608256991.357,
          'passenger_dict': {},'npc_id': 8501,
          'trans_pattern': 1,
          'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 100,'item_type': 0,'attachment': {},'item_id': 8992}},'faction_id': 18,
          'max_shield': 0,
          'max_hp': 1500,
          'mp_add_attr': {},'hp': 1500,
          'mp_attr': {'mileage': 0,
                      'arm_hit': 1.0,
                      'foot_hit': 1.0,
                      'head_hit': 1.5,
                      'body_hit': 1.0,
                      'item_num': 0,
                      'human_yaw': 2.092821734640787
                      },
          'mecha_fashion': {u'0': 208200200},'mecha_robot': False,
          'auto_join': True,
          'max_fuel': 100.0,
          'skills': {850152: {'last_cast_time': 0,'cost_fuel': 12,'max_fuel': 0,'cost_fuel_type': 1},850151: {'last_cast_time': 0,'left_cast_cnt': 1,'mp_stage': 0,'inc_mp': 5,'mp': 100,'init_inc_mp': 5,'max_mp': 100,'cost_mp': 100}},'missile_lock': None,
          'mecha_custom_skin': {},'mecha_id': 8501,
          'vrf_status': [
                       113, 110],
          'mp_explosive': {},'shapeshift': 'trans',
          'position': [
                     -37.53196334838867, 809.0584716796875, 17589.298828125],
          'fuel_regtime': 0
          }
   }
NPC_BUILDING_TYPE_2_INIT_DICT = {6021: {'status': 2,
          'npc_id': 19,
          'effective': True,
          'hp': 500,
          'max_hp': 500,
          'faction_id': 0,
          'building_no': 6021,
          'birthtime': 1608291705.207,
          'position': [
                     5562.0, 183.0, 14.0],
          'rot': [
                0, 0, 0, 1],
          'owner_id': None
          }
   }
SELF_MECHA_TYPE_2_INIT_DICT = {8001: {'init_max_hp': 2550,
          'shield': 500.0,
          'last_action': [
                        None, None],
          'creator': None,
          'mecha_sfx': 203800000,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'cur_fuel': 100.0,
          'driver_id': None,
          'max_fuel_dict': {},'suspended': False,
          'seats': [
                  'seat_1'],
          'broken_times': 0,
          'born_time': 1608348947.833,
          'passenger_dict': {},'npc_id': 8001,
          'vrf_status': [
                       113, 110],
          'temporary_shield_map': {},'shoot_mode': 1,
          'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 80,'item_type': 0,'attachment': {},'item_id': 800101},2: {'item_id': 800102,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'faction_id': 1,
          'next_regtime_dict': {},'max_shield': 500.0,
          'max_hp': 2550,
          'hit_flag_value': {},'cur_fuel_dict': {},'mp_add_attr': {},'hp': 2550,
          'durative_cost': {},'mp_attr': {'mileage': 0,'arm_hit': 1.0,'foot_hit': 1.0,'head_hit': 1.2,'body_hit': 1.0,'item_num': 0},'mecha_fashion': {'0': 201800100},'mecha_robot': False,
          'auto_join': False,
          'module_buff_data': {},'max_fuel': 100.0,
          'rage': 0,
          'skills': {800151: {'last_cast_time': 0,'inc_mp': 30.0,'mp': 100.0,'left_cast_cnt': 999999},800152: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 80.0,'left_cast_cnt': 999999},800153: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 80.0,'left_cast_cnt': 999999}},'missile_lock': None,
          'mecha_custom_skin': {},'mecha_id': 8001,
          't_rage_last': 0,
          'trans_pattern': 1,
          'mp_explosive': {},'shapeshift': '',
          'position': [
                     9.5367431640625e-06, 245.43638610839844, 22.880046844482422],
          'fuel_regtime': 0
          }
   }

def get_npc_mecha_init_dict_by_type(mecha_type, creator_id, pos, hp=None, shield=None):
    init_dict = NPC_MECHA_TYPE_2_INIT_DICT.get(int(mecha_type))
    if not init_dict:
        return {}
    ret_dict = copy.deepcopy(init_dict)
    ret_dict.update({'creator': creator_id,
       'driver_id': creator_id,
       'passenger_dict': {creator_id: 'seat_1'},'position': pos
       })
    if hp:
        ret_dict.update({'hp': hp
           })
    if shield:
        ret_dict.update({'shield': shield
           })
    return ret_dict


def get_npc_mecha_trans_init_dict_by_type(mecha_type, extra_dict=None):
    init_dict = NPC_MECHA_TYPE_2_INIT_DICT.get(int(mecha_type))
    ret_dict = copy.deepcopy(init_dict)
    if extra_dict:
        ret_dict.update(extra_dict)
    return ret_dict


def get_npc_building_init_dict_by_type(building_type, extra_dict=None):
    init_dict = NPC_BUILDING_TYPE_2_INIT_DICT.get(building_type)
    ret_dict = copy.deepcopy(init_dict)
    if extra_dict:
        ret_dict.update(extra_dict)
    return ret_dict


def get_npc_robot_init_dict_by_role_type(role_type, pos, max_hp=200):
    init_dict = {'max_hp': max_hp,
       'is_robot': True,
       'char_name': 'guide_robot',
       'weapons': {},'position': pos,
       'parachute_mecha_id': 8002,
       'faction_id': 1,
       'aim_y': 1.0,
       'role_id': str(role_type)
       }
    return init_dict


def get_self_mecha_init_dict_by_type(mecha_type, extra_dict=None):
    init_dict = SELF_MECHA_TYPE_2_INIT_DICT.get(mecha_type)
    ret_dict = copy.deepcopy(init_dict)
    if extra_dict:
        ret_dict.update(extra_dict)
    return ret_dict


def propel_guide(guide_id, com_obj, force=None):
    guide_data = com_obj.get_guide_data(guide_id)
    if global_data.is_pc_mode:
        func_name = guide_data.get('PCInterface', guide_data.get('Interface', None))
    else:
        func_name = guide_data.get('Interface', None)
    if global_data.is_pc_mode:
        func_args = guide_data.get('PCArgs', guide_data.get('Args', []))
    else:
        func_args = guide_data.get('Args', [])
    func_type = guide_data.get('InterfaceType', None)
    if global_data.is_pc_mode:
        end_event = guide_data.get('PCEvent', guide_data.get('Event', None))
    else:
        end_event = guide_data.get('Event', None)
    if func_type is None or func_type == GUIDE_PROCESS_MODE_ONLY_INIT or force:
        if func_name:
            func = getattr(com_obj, func_name)
            if isinstance(func_args, (list, tuple)):
                func(guide_id, *func_args)
            else:
                func(guide_id, func_args)
        if end_event:
            if len(end_event) == 2:
                com_obj.unit_obj.regist_event(end_event[0], getattr(com_obj, end_event[1]))
            elif len(end_event) == 3:
                target_unit_obj_name = end_event[2]
                control_target = com_obj.unit_obj.ev_g_control_target()
                if not control_target or not control_target.logic:
                    return
                ct_logic_name = control_target.logic.__class__.__name__
                if target_unit_obj_name == ct_logic_name:
                    control_target.logic.regist_event(end_event[0], getattr(com_obj, end_event[1]))
    return


def propel_guide_multiple(guide_ids, com_obj, ui_list=None, force=None):
    com_obj.show_main_ui(ui_list)
    if guide_ids:
        if isinstance(guide_ids, (list, tuple)):
            for guide_id in guide_ids:
                propel_guide(guide_id, com_obj, force)

        else:
            propel_guide(guide_ids, com_obj, force)


def destroy_guide(guide_id, com_obj, force=None):
    guide_data = com_obj.get_guide_data(guide_id)
    if global_data.is_pc_mode:
        func_name = guide_data.get('PCInterface', guide_data.get('Interface', None))
    else:
        func_name = guide_data.get('Interface', None)
    if global_data.is_pc_mode:
        func_args = guide_data.get('PCArgs', guide_data.get('Args', []))
    else:
        func_args = guide_data.get('Args', [])
    func_type = guide_data.get('InterfaceType', None)
    if global_data.is_pc_mode:
        end_event = guide_data.get('PCEvent', guide_data.get('Event', None))
    else:
        end_event = guide_data.get('Event', None)
    prior_guide_id = guide_data.get('Prior', None)
    if func_type is None or func_type == GUIDE_PROCESS_MODE_ONLY_DESTROY or force:
        if func_name:
            func = getattr(com_obj, '{}_destroy'.format(func_name))
            if isinstance(func_args, (list, tuple)):
                func(guide_id, *func_args)
            else:
                func(guide_id, func_args)
        if end_event:
            com_obj.unit_obj.unregist_event(end_event[0], getattr(com_obj, end_event[1]))
        if prior_guide_id is None:
            pass
    add_finished_guide = getattr(com_obj, 'add_finished_guide')
    add_finished_guide and add_finished_guide(guide_id)
    return


def destroy_guide_multiple(guide_ids, com_obj, force=None):
    if guide_ids:
        if isinstance(guide_ids, (list, tuple)):
            for guide_id in guide_ids:
                destroy_guide(guide_id, com_obj, force)

        else:
            destroy_guide(guide_ids, com_obj, force)


def finish_guide(guide_id, com_obj):
    if com_obj.unit_obj is None:
        return
    else:
        is_finished_guide = getattr(com_obj, 'is_finished_guide')
        if is_finished_guide and is_finished_guide(guide_id):
            return
        guide_data = com_obj.get_guide_data(guide_id)
        prior_guide_id = guide_data.get('Prior', None)
        if prior_guide_id:
            prior_next_guide_ids = com_obj.get_guide_data(prior_guide_id).get('Next', None)
            destroy_guide_multiple(prior_next_guide_ids, com_obj)
        else:
            destroy_guide(guide_id, com_obj)
        next_guide_ids = guide_data.get('Next')
        if global_data.is_pc_mode and guide_data.get('Next_PC'):
            next_guide_ids = guide_data.get('Next_PC')
        next_show_main_ui = guide_data.get('NextShowMainUI')
        if global_data.is_pc_mode and guide_data.get('PCNextShowMainUI'):
            next_show_main_ui = guide_data.get('PCNextShowMainUI')
        propel_guide_multiple(next_guide_ids, com_obj, next_show_main_ui)
        if prior_guide_id:
            com_obj.extra_finish_process(guide_id)
        return


def finish_local_battle_guide(battle_type):
    from logic.gutils import task_utils
    if not global_data.player:
        return
    global_data.player.quit_new_local_battle()
    assessment_tid = task_utils.get_certificate_task_id_by_battle_type(battle_type)
    assessment_tid and global_data.player.call_server_method('finish_assessment_task', (assessment_tid,))


def save_newbie_local_battle_data(key, value):
    info = GuideSetting().local_battle_data
    info[key] = value
    GuideSetting().local_battle_data = info


def get_newbie_local_battle_type():
    info = GuideSetting().local_battle_data
    return info.get('_lbs_battle_type', -1)


def remove_newbie_local_battle_data(keys):
    info = GuideSetting().local_battle_data
    if isinstance(keys, (list, tuple)):
        for key in keys:
            if key in info:
                del info[key]

    elif keys in info:
        del info[keys]
    GuideSetting.local_battle_data = info


def get_newbie_stage_local_damage(weapon_id, is_mecha_target, part):
    info = GetWeaponDamage().get(weapon_id, None)
    if not info:
        return 0
    else:
        if is_mecha_target:
            if part == 0:
                return info['mecha_head_hit']
            else:
                return info['mecha_other_hit']

        else:
            if part == 0:
                return info['human_head_hit']
            return info['human_other_hit']
        return


def is_in_newbie_local_battle():
    from logic.gcommon.const import NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE, NEWBIE_STAGE_THIRD_BATTLE, NEWBIE_STAGE_FOURTH_BATTLE
    battle = global_data.battle
    if not battle:
        return False
    return battle.get_battle_tid() in [NEWBIE_STAGE_HUMAN_BATTLE, NEWBIE_STAGE_MECHA_BATTLE, NEWBIE_STAGE_THIRD_BATTLE, NEWBIE_STAGE_FOURTH_BATTLE]
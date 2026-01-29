# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/qte_guide_utils.py
from __future__ import absolute_import
from logic.comsys.guide_ui.GuideSetting import GuideSetting
from data.c_guide_data import get_qte_step_init_data

def get_qte_battle_data():
    aid = global_data.channel.get_prop_str('USERINFO_AID')
    return GuideSetting().local_battle_data.get(aid, {})


def get_qte_guide_init_pos_and_yaw(step_id):
    step_init_data = get_qte_step_init_data(step_id)
    position = step_init_data['pos']
    yaw = step_init_data['yaw']
    return (
     position, yaw)


def get_qte_current_step():
    info = get_qte_battle_data()
    return info.get('_lbs_step', None)


def get_qte_local_pos_and_yaw():
    saved_step_id = get_lbs_qte_guide_step()
    return get_qte_guide_init_pos_and_yaw(saved_step_id)


def is_in_qte_battle():
    info = get_qte_battle_data()
    return info.get('_lbs_in_battle', 0)


def save_qte_battle_data(key, value):
    info = get_qte_battle_data()
    info[key] = value
    aid = global_data.channel.get_prop_str('USERINFO_AID')
    data = GuideSetting().local_battle_data
    data[aid] = info
    GuideSetting().local_battle_data = data


def is_finish_qte_guide():
    info = get_qte_battle_data()
    if not info:
        return False
    else:
        if info.get('_lbs_finish_guide', None):
            return True
        return info.get('_lbs_qte_guide_finish', 0)


def set_qte_guide_finish():
    save_qte_battle_data('_lbs_qte_guide_finish', 1)


def get_qte_chosen_role_id():
    info = get_qte_battle_data()
    if not info:
        return
    else:
        role_id = info.get('_lbs_role_id', None)
        if role_id:
            return role_id
        return info.get('_lbs_qte_role_id', None)
        return


def save_qte_chosen_role_id(role_id):
    save_qte_battle_data('_lbs_qte_role_id', role_id)


FIRST_STEP_ID = 100

def get_lbs_qte_guide_step():
    info = get_qte_battle_data()
    return info.get('_lbs_qte_guide_step', FIRST_STEP_ID)


def save_lbs_qte_guide_step(step_id):
    save_qte_battle_data('_lbs_qte_guide_step', step_id)


QTE_MECHA_INIT_DICT = {8004: {'creator': None,
          'driver_id': None,
          'born_time': 0,
          'passenger_dict': {},'init_max_hp': 3201,
          'hp': 3200,
          'max_shield': 800.0,
          'shield': 800.0,
          'faction_id': 0,
          'max_fuel': 100.0,
          'max_hp': 3200,
          'mecha_robot': True,
          'position': [
                     2779, 290, 7415],
          'mp_attr': {'human_yaw': 1.7},'npc_id': 8004,
          'last_action': [
                        None, None],
          'mecha_sfx': None,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'cur_fuel': 100.0,
          'suspended': False,
          'seats': [
                  'seat_1'],
          'broken_times': 0,
          'vrf_status': [
                       113, 110],
          'shoot_mode': 1,
          'next_regtime_dict': {},'last_max_heat_state_enter_time': None,
          'shared_magazine': {'iBulletNum': 35,'pos': [1, 2],'iBulletCap': 35},'durative_cost': {},'heat_state': 0,
          'mecha_fashion': {},'auto_join': False,
          'rage': 0,
          'missile_lock': None,
          'mecha_custom_skin': {},'mecha_id': 8004,
          't_rage_last': 0,
          'trans_pattern': 1,
          'mp_explosive': {},'cur_heat': 2000,
          'fuel_regtime': 0,
          'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 35,'item_type': 0,'attachment': {},'item_id': 800401},2: {'count': 1,'iBolted': 1,'iBulletNum': 35,'item_type': 0,'attachment': {},'item_id': 800403},3: {'item_id': 800411,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'skills': {800451: {'other_damage_add_factor': 0.2,'last_cast_time': 0,'human_damage': 0,'mecha_damage': 0,'human_damage_add_factor': 0.2,
                              'buff_human': 377,'buff_mecha': 375,'attack_dis': 29},
                     800452: {'last_cast_time': 0},800453: {'last_cast_time': 0,'cost_fuel': 20,'max_fuel': 0,'cost_fuel_type': 2},800454: {'ignore_buff': [305, 322, 329, 317, 337, 328],'last_cast_time': 0,
                              'left_cast_cnt': 1,'mp_stage': 0,
                              'inc_mp': 10,
                              'mp': 100,
                              'add_buff': {347: {'extra_duration': 4,'ratio': 0.2,'no_condition': 1,'mod_buff_card_id': 1403}},'init_inc_mp': 10,
                              'max_mp': 100,
                              'cost_mp': 100
                              },
                     800455: {'last_cast_time': 0,'left_cast_cnt': 1,'mp_stage': 0,'heat_state_delay': 2,'inc_mp': 10,'mp': 100,
                              'init_inc_mp': 10,'max_mp': 100,'cost_mp': 100},
                     800456: {'last_cast_time': 0,'cost_fuel': 20,'max_fuel': 0,'cost_fuel_type': 2}}
          },
   8001: {'creator': None,
          'driver_id': None,
          'born_time': 0,
          'passenger_dict': {},'init_max_hp': 2550,
          'hp': 2550,
          'max_shield': 500.0,
          'shield': 500.0,
          'faction_id': 0,
          'max_fuel': 100.0,
          'cur_fuel': 100.0,
          'max_hp': 2550,
          'mecha_robot': False,
          'position': [
                     2779, 290, 7415],
          'mp_attr': {'mileage': 0,'arm_hit': 1.0,'foot_hit': 1.0,'head_hit': 1.2,'body_hit': 1.0,'item_num': 0},'npc_id': 8001,
          'last_action': [
                        None, None],
          'mecha_sfx': 203800000,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'max_fuel_dict': {},'suspended': False,
          'seats': [
                  'seat_1'],
          'broken_times': 0,
          'vrf_status': [
                       113, 110],
          'shoot_mode': 1,
          'weapons': {1: {'count': 1,'iBulletCap': 110,'iBolted': 1,'iBulletNum': 110,'item_type': 0,'attachment': {},'item_id': 800101},2: {'item_id': 800102,'item_type': 0,'iBulletNum': 0,'attachment': {},'count': 1}},'next_regtime_dict': {},'hit_flag_value': {},'cur_fuel_dict': {},'mp_add_attr': {},'durative_cost': {},'mecha_fashion': {'0': 201800100},'auto_join': False,
          'rage': 0,
          'skills': {800152: {'left_cast_cnt': 999999,'cost_fuel': 10,'max_fuel': 0,'cost_fuel_type': 1,'last_cast_time': 0,'outer_shield_lasting_time': 4,'outer_shield_hp': 300,'speed_up_buff_id': 397,'mp_stage': 0,'effect_buff_id': 396,'inc_mp': 10,'mp': 80,'speed_up_lasting_time': 3,'init_inc_mp': 10,'outer_shield_buff_id': 372,'max_mp': 80,'cost_mp': 80},800153: {'left_cast_cnt': 999999,'last_cast_time': 0,'cost_fuel': 20,'max_fuel': 0,'cost_fuel_type': 1},800151: {'left_cast_cnt': 999999,'last_cast_time': 0,'mp_stage': 0,'inc_mp': 10,'mp': 100,'init_inc_mp': 10,'max_mp': 100,'cost_mp': 100}},'missile_lock': None,
          'mecha_custom_skin': {},'mecha_id': 8001,
          't_rage_last': 0,
          'trans_pattern': 1,
          'mp_explosive': {},'shapeshift': '',
          'fuel_regtime': 0
          },
   8002: {'creator': None,
          'driver_id': None,
          'born_time': 0,
          'passenger_dict': {},'init_max_hp': 2200,
          'hp': 2200,
          'max_shield': 800.0,
          'shield': 800.0,
          'faction_id': 0,
          'max_fuel': 120.0,
          'cur_fuel': 120.0,
          'max_hp': 2200,
          'mecha_robot': False,
          'position': [
                     2779, 290, 7415],
          'mp_attr': {'mileage': 0,'arm_hit': 1.0,'foot_hit': 1.0,'head_hit': 1.2,'body_hit': 1.0,'item_num': 0},'mecha_id': 8002,
          'npc_id': 8002,
          'last_action': [
                        None, None],
          'mecha_sfx': None,
          'mv_state': -1,
          'share': False,
          'repair_energy': 60.0,
          'max_fuel_dict': {},'suspended': False,
          'seats': [
                  'seat_1'],
          'broken_times': 0,
          'vrf_status': [
                       113, 110],
          'temporary_shield_map': {},'shoot_mode': 1,
          'weapons': {1: {'count': 1,'iBolted': 1,'iBulletNum': 1,'item_type': 0,'attachment': {},'item_id': 800201}},'next_regtime_dict': {},'hit_flag_value': {},'cur_fuel_dict': {},'mp_add_attr': {},'durative_cost': {},'mecha_fashion': {},'auto_join': False,
          'module_buff_data': {},'rage': 0,
          'skills': {800251: {'left_cast_cnt': 9999999,'last_cast_time': 0,'add_energy': 0,'add_dmg': 10,'fSpeed': 1885,'add_dmg_stage': 3,'mp_stage': 0,'item_type': 800201,'inc_mp': 12.5,'mp': 105,'init_inc_mp': 12.5,'max_mp': 105,'cost_mp': 15},800252: {'left_cast_cnt': 9999999,'last_cast_time': 0,'left_count': 3,'continue_count': 3,'mp_stage': 0,'inc_mp': 1,'continue_time': 8,'mp': 12,'init_inc_mp': 1,'max_mp': 12,'cost_mp': 12},800253: {'left_cast_cnt': 9999999,'last_cast_time': 0,'cost_fuel': 10,'max_fuel': 0,'cost_fuel_type': 1,'mp_stage': 3,'inc_mp': 6,'mp': 30,'init_inc_mp': 6,'max_mp': 30,'cost_mp': 30},800259: {'last_cast_time': 0,'cost_fuel': 20,'max_fuel': 0,'cost_fuel_type': 1}},'missile_lock': None,
          'mecha_custom_skin': {},'t_rage_last': 0,
          'trans_pattern': 1,
          'mp_explosive': {},'shapeshift': '',
          'fuel_regtime': 0
          }
   }

def get_npc_mecha_init_dict--- This code section failed: ---

 285       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('time_utility',)
           6  IMPORT_NAME           0  'logic.gcommon'
           9  IMPORT_FROM           1  'time_utility'
          12  STORE_FAST            5  'time_utility'
          15  POP_TOP          

 286      16  LOAD_FAST             5  'time_utility'
          19  LOAD_ATTR             2  'time'
          22  CALL_FUNCTION_0       0 
          25  STORE_FAST            6  'now'

 288      28  LOAD_GLOBAL           3  'QTE_MECHA_INIT_DICT'
          31  LOAD_CONST            3  8004
          34  BINARY_SUBSCR    
          35  STORE_FAST            7  'mecha_init_dict'

 289      38  LOAD_FAST             7  'mecha_init_dict'
          41  LOAD_ATTR             4  'update'
          44  BUILD_MAP_4           4 

 290      47  BUILD_MAP_4           4 
          50  STORE_MAP        

 291      51  STORE_MAP        
          52  INPLACE_POWER    
          53  INPLACE_POWER    
          54  STORE_MAP        

 292      55  LOAD_FAST             1  'pos'
          58  LOAD_CONST            6  'position'
          61  STORE_MAP        

 293      62  LOAD_FAST             6  'now'
          65  LOAD_CONST            7  'born_time'
          68  STORE_MAP        
          69  CALL_FUNCTION_1       1 
          72  POP_TOP          

 296      73  LOAD_FAST             2  'yaw'
          76  LOAD_CONST            0  ''
          79  COMPARE_OP            9  'is-not'
          82  JUMP_IF_FALSE_OR_POP   107  'to 107'
          85  LOAD_FAST             7  'mecha_init_dict'
          88  LOAD_ATTR             4  'update'
          91  LOAD_CONST            8  'mp_attr'
          94  BUILD_MAP_1           1 
          97  LOAD_FAST             2  'yaw'
         100  LOAD_CONST            9  'human_yaw'
         103  STORE_MAP        
         104  CALL_FUNCTION_256   256 
       107_0  COME_FROM                '82'
         107  POP_TOP          

 297     108  LOAD_FAST             3  'hp'
         111  LOAD_CONST            0  ''
         114  COMPARE_OP            9  'is-not'
         117  JUMP_IF_FALSE_OR_POP   157  'to 157'
         120  LOAD_FAST             7  'mecha_init_dict'
         123  LOAD_ATTR             4  'update'
         126  BUILD_MAP_3           3 

 298     129  LOAD_FAST             3  'hp'
         132  LOAD_CONST           10  'hp'
         135  STORE_MAP        

 299     136  LOAD_FAST             3  'hp'
         139  LOAD_CONST           11  1
         142  BINARY_ADD       
         143  LOAD_CONST           12  'init_max_hp'
         146  STORE_MAP        

 300     147  LOAD_FAST             3  'hp'
         150  LOAD_CONST           13  'max_hp'
         153  STORE_MAP        
         154  CALL_FUNCTION_1       1 
       157_0  COME_FROM                '117'
         157  POP_TOP          

 302     158  LOAD_FAST             4  'shield'
         161  LOAD_CONST            0  ''
         164  COMPARE_OP            9  'is-not'
         167  JUMP_IF_FALSE_OR_POP   191  'to 191'
         170  LOAD_FAST             7  'mecha_init_dict'
         173  LOAD_ATTR             4  'update'
         176  LOAD_CONST           14  'shield'
         179  LOAD_FAST             4  'shield'
         182  LOAD_CONST           15  'max_shield'
         185  LOAD_FAST             4  'shield'
         188  CALL_FUNCTION_512   512 
       191_0  COME_FROM                '167'
         191  POP_TOP          

 303     192  LOAD_FAST             7  'mecha_init_dict'
         195  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 50


def get_summon_mecha_init_dict(mecha_type, pos, yaw):
    mecha_init_dict = QTE_MECHA_INIT_DICT[mecha_type]
    mecha_init_dict.update({'creator': global_data.player.id,
       'driver_id': global_data.player.id,
       'position': pos
       })
    mecha_init_dict['mp_attr']['human_yaw'] = yaw
    return mecha_init_dict
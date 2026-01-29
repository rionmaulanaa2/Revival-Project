# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathBattleUtils.py
from __future__ import absolute_import
import six
from six.moves import range

def pnpoly--- This code section failed: ---

   8       0  LOAD_FAST             2  'pos'
           3  UNPACK_SEQUENCE_2     2 
           6  STORE_FAST            3  'x'
           9  STORE_FAST            4  'y'

   9      12  STORE_FAST            1  'pos_lst'
          15  BINARY_SUBTRACT  
          16  STORE_FAST            5  'j'

  10      19  LOAD_GLOBAL           0  'False'
          22  STORE_FAST            6  'in_range'

  11      25  SETUP_LOOP          152  'to 180'
          28  LOAD_GLOBAL           1  'range'
          31  LOAD_FAST             0  'count'
          34  CALL_FUNCTION_1       1 
          37  GET_ITER         
          38  FOR_ITER            138  'to 179'
          41  STORE_FAST            7  'i'

  12      44  LOAD_FAST             1  'pos_lst'
          47  LOAD_FAST             7  'i'
          50  BINARY_SUBSCR    
          51  LOAD_CONST            2  ''
          54  BINARY_SUBSCR    
          55  STORE_FAST            8  'first_x'

  13      58  LOAD_FAST             1  'pos_lst'
          61  LOAD_FAST             7  'i'
          64  BINARY_SUBSCR    
          65  LOAD_CONST            1  1
          68  BINARY_SUBSCR    
          69  STORE_FAST            9  'first_y'

  14      72  LOAD_FAST             1  'pos_lst'
          75  LOAD_FAST             5  'j'
          78  BINARY_SUBSCR    
          79  LOAD_CONST            2  ''
          82  BINARY_SUBSCR    
          83  STORE_FAST           10  'second_x'

  15      86  LOAD_FAST             1  'pos_lst'
          89  LOAD_FAST             5  'j'
          92  BINARY_SUBSCR    
          93  LOAD_CONST            1  1
          96  BINARY_SUBSCR    
          97  STORE_FAST           11  'second_y'

  16     100  LOAD_FAST             7  'i'
         103  STORE_FAST            5  'j'

  17     106  LOAD_FAST             9  'first_y'
         109  LOAD_FAST             4  'y'
         112  COMPARE_OP            4  '>'
         115  LOAD_FAST            11  'second_y'
         118  LOAD_FAST             4  'y'
         121  COMPARE_OP            4  '>'
         124  COMPARE_OP            3  '!='
         127  POP_JUMP_IF_FALSE    38  'to 38'
         130  LOAD_FAST             3  'x'
         133  LOAD_FAST            10  'second_x'
         136  LOAD_FAST             8  'first_x'
         139  BINARY_SUBTRACT  
         140  LOAD_FAST             4  'y'
         143  LOAD_FAST             9  'first_y'
         146  BINARY_SUBTRACT  
         147  BINARY_MULTIPLY  
         148  LOAD_FAST            11  'second_y'
         151  LOAD_FAST             9  'first_y'
         154  BINARY_SUBTRACT  
         155  BINARY_DIVIDE    
         156  LOAD_FAST             8  'first_x'
         159  BINARY_ADD       
         160  COMPARE_OP            0  '<'
       163_0  COME_FROM                '127'
         163  POP_JUMP_IF_FALSE    38  'to 38'

  18     166  LOAD_FAST             6  'in_range'
         169  UNARY_NOT        
         170  STORE_FAST            6  'in_range'
         173  JUMP_BACK            38  'to 38'
         176  JUMP_BACK            38  'to 38'
         179  POP_BLOCK        
       180_0  COME_FROM                '25'

  19     180  LOAD_FAST             6  'in_range'
         183  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 12


def get_player_group_id():
    if global_data.player and global_data.player.logic:
        return global_data.player.logic.ev_g_group_id()


def cal_enemy_base_range(player_pos, born_data, range_data):
    _x, _y, _z, _r, _idx, _dict_info = born_data
    y_range = range_data.get('y_range')
    if not y_range:
        return False
    if player_pos.y < _y + y_range[0] or player_pos.y > _y + y_range[1]:
        return False
    pos_lst = range_data.get('pos_lst', [])
    return pnpoly(len(pos_lst), pos_lst, (player_pos.x, player_pos.z))


def check_in_death_base(player_pos, is_check_my_group):
    in_enemy_base = False
    if not player_pos:
        return in_enemy_base
    else:
        if not global_data.game_mode:
            return in_enemy_base
        if not global_data.death_battle_data:
            return in_enemy_base
        if global_data.death_battle_data.area_id is None:
            return in_enemy_base
        born_range_data = global_data.game_mode.get_cfg_data('born_range_data')
        born_cfg_data = global_data.game_mode.get_born_data()
        door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
        range_ids = born_cfg_data[global_data.death_battle_data.area_id].get('c_range_accurate')
        if not range_ids:
            range_ids = born_cfg_data[global_data.death_battle_data.area_id].get('c_range')
        door_data = born_cfg_data[global_data.death_battle_data.area_id].get('door')
        if not door_data:
            return
        for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
            is_my_group = get_player_group_id() == group_id
            if is_check_my_group != is_my_group:
                continue
            _x, _y, _z, _r, _idx, _dict_info = born_data.data
            for index, door_id in enumerate(door_data[_idx]):
                if _dict_info:
                    is_weak_door = _dict_info.get(door_id, False)
                else:
                    is_weak_door = False
                if not is_weak_door:
                    return in_enemy_base
                door_info = door_cfg_data.get(str(door_id))
                if not door_info:
                    continue

            range_data = born_range_data.get(str(range_ids[_idx]), {})
            in_enemy_base = in_enemy_base or cal_enemy_base_range(player_pos, born_data.data, range_data)
            extra_pos_id = range_data.get('extra_pos_id', [])
            for pos_id in extra_pos_id:
                range_data = born_range_data.get(str(pos_id), {})
                in_enemy_base = in_enemy_base or cal_enemy_base_range(player_pos, born_data.data, range_data)

        return in_enemy_base


def has_week_door():
    if not global_data.death_battle_data or global_data.death_battle_data.area_id is None:
        return False
    else:
        for group_id, born_data in six.iteritems(global_data.death_battle_data.born_data):
            _x, _y, _z, _r, _idx, _dict_info = born_data.data
            door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
            born_cfg_data = global_data.game_mode.get_born_data()
            door_data = born_cfg_data[global_data.death_battle_data.area_id].get('door')
            if not door_data:
                return False
            if len(door_data) <= _idx:
                return False
            for index, door_id in enumerate(door_data[_idx]):
                door_info = door_cfg_data.get(str(door_id))
                if not door_info:
                    continue
                door_id = int(door_id)
                if _dict_info:
                    is_weak_door = _dict_info.get(door_id, False)
                else:
                    is_weak_door = False
                if is_weak_door:
                    return True

        return False
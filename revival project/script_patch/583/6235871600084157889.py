# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sound_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
import logic.gcommon.const as gconst

def play_sound--- This code section failed: ---

   8       0  LOAD_GLOBAL           0  'isinstance'
           3  LOAD_GLOBAL           1  'str'
           6  BINARY_SUBSCR    
           7  LOAD_GLOBAL           1  'str'
          10  CALL_FUNCTION_2       2 
          13  POP_JUMP_IF_FALSE    59  'to 59'

   9      16  POP_JUMP_IF_FALSE     1  'to 1'
          19  BINARY_SUBSCR    
          20  LOAD_CONST            2  'nf'
          23  COMPARE_OP            2  '=='
          26  POP_JUMP_IF_FALSE    59  'to 59'

  10      29  LOAD_GLOBAL           2  'global_data'
          32  LOAD_ATTR             3  'sound_mgr'
          35  LOAD_ATTR             4  'post_event'
          38  LOAD_ATTR             3  'sound_mgr'
          41  BINARY_SUBSCR    
          42  LOAD_FAST             1  'sound_id'
          45  LOAD_FAST             2  'sound_pos'
          48  CALL_FUNCTION_3       3 
          51  POP_TOP          

  11      52  LOAD_CONST            0  ''
          55  RETURN_END_IF    
        56_0  COME_FROM                '26'
        56_1  COME_FROM                '16'
          56  JUMP_FORWARD          0  'to 59'
        59_0  COME_FROM                '56'

  12      59  SETUP_LOOP           45  'to 107'
          62  SETUP_LOOP            1  'to 66'
          65  SLICE+1          
        66_0  COME_FROM                '62'
          66  GET_ITER         
          67  FOR_ITER             36  'to 106'
          70  STORE_FAST            3  'data'

  13      73  LOAD_GLOBAL           2  'global_data'
          76  LOAD_ATTR             3  'sound_mgr'
          79  LOAD_ATTR             5  'set_switch'
          82  LOAD_FAST             3  'data'
          85  LOAD_CONST            3  ''
          88  BINARY_SUBSCR    
          89  LOAD_FAST             3  'data'
          92  LOAD_CONST            1  1
          95  BINARY_SUBSCR    
          96  LOAD_FAST             1  'sound_id'
          99  CALL_FUNCTION_3       3 
         102  POP_TOP          
         103  JUMP_BACK            67  'to 67'
         106  POP_BLOCK        
       107_0  COME_FROM                '59'

  14     107  LOAD_GLOBAL           2  'global_data'
         110  LOAD_ATTR             3  'sound_mgr'
         113  LOAD_ATTR             4  'post_event'
         116  LOAD_ATTR             3  'sound_mgr'
         119  BINARY_SUBSCR    
         120  LOAD_FAST             1  'sound_id'
         123  LOAD_FAST             2  'sound_pos'
         126  CALL_FUNCTION_3       3 
         129  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 10


def get_hitted_sound(weapon_id, hitted_type):
    type_map = {'human': 0,'mecha': 1}
    weapon_conf = confmgr.get('firearm_config', str(weapon_id), default={})
    hitted_sound_list = weapon_conf.get('cHittedSound', [])
    if not hitted_sound_list:
        return []
    index = type_map.get(hitted_type, 0)
    if index < len(hitted_sound_list):
        return hitted_sound_list[index]
    return hitted_sound_list[0]


def play_hit_sound_2d(weapon_id, is_human, is_head):
    weapon_conf = confmgr.get('firearm_config', str(weapon_id), default={})
    hit_sound_2d = weapon_conf.get('cHitSound2D', None)
    if not hit_sound_2d:
        hit_sound_2d = 'ui_hit_notice'
    group_type = 'human' if is_human else 'mecha'
    group_part = 'head' if is_head else 'body'
    global_data.sound_mgr.play_hit_sound_2d(hit_sound_2d, (('character_form', group_type), ('hit_parts', group_part)))
    return


def check_mecha_foot_nf(mecha_id):
    mecha_id = str(mecha_id)
    return mecha_id.startswith('80')
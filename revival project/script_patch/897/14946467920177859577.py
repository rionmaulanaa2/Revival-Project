# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/explosive_utils.py
from __future__ import absolute_import
_reload_all = True
from logic.gcommon.common_const.weapon_const import WP_GRENADES_GUN
throw_base_sync_keys = ('uniq_key', 'call_sync_id', 'item_itype', 'item_kind', 'last_time',
                        'use_rot_mat', 'dir', 'up', 'position', 'm_position', 'in_aim',
                        'accumulate_rate', 'mass', 'gravity', 'speed', 'skin_id',
                        'shiny_weapon_id', 'custom_params', 'sub_idx', 'pellets',
                        'fired_socket_index', 'is_first_grenade', 'col_width', 'limited_pierce_cnt')
throw_extra_sync_keys = throw_base_sync_keys + ('origin_pos', 'end', 'track', 'aim_target',
                                                'aim_pos', 'fire_cam_pitch', 'first_contact_dis',
                                                'bounces', 'limited_pierce_cnt')
explosion_base_sync_keys = ('uniq_key', 'owner_id', 'target', 'item_itype', 'item_kind',
                            'position', 'normal', 'use_rot_mat', 'dir', 'up', 'forward',
                            'cobj_group', 'cobj_mask', 'skin_id', 'shiny_weapon_id',
                            'dummy_reason', 'ignore_bomb_sfx', 'last_time', 'faction_id')

def get_sync_dict(info):
    sync_keys = throw_base_sync_keys if info.get('item_kind', 0) == WP_GRENADES_GUN else throw_extra_sync_keys
    sync_dict = {key:info[key] for key in sync_keys if key in info}
    return sync_dict


def get_explosion_sync_dict(info):
    sync_dict = {key:info[key] for key in explosion_base_sync_keys if key in info}
    if 'extra_sync_keys' in info:
        for key in info['extra_sync_keys']:
            if key in info:
                sync_dict[key] = info[key]

    return sync_dict


def transfer_attr--- This code section failed: ---

  99       0  LOAD_CONST            1  'skin_id'
           3  LOAD_FAST             0  'source_info'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    45  'to 45'

 100      12  POP_JUMP_IF_FALSE     1  'to 1'
          15  BINARY_SUBSCR    
          16  LOAD_FAST             1  'ret_info'
          19  LOAD_CONST            1  'skin_id'
          22  STORE_SUBSCR     

 101      23  LOAD_FAST             0  'source_info'
          26  LOAD_ATTR             0  'get'
          29  LOAD_CONST            2  'shiny_weapon_id'
          32  CALL_FUNCTION_1       1 
          35  LOAD_FAST             1  'ret_info'
          38  LOAD_CONST            2  'shiny_weapon_id'
          41  STORE_SUBSCR     
          42  JUMP_FORWARD          0  'to 45'
        45_0  COME_FROM                '42'

 103      45  LOAD_CONST            3  'sub_idx'
          48  LOAD_FAST             0  'source_info'
          51  COMPARE_OP            6  'in'
          54  POP_JUMP_IF_FALSE    71  'to 71'

 104      57  POP_JUMP_IF_FALSE     3  'to 3'
          60  BINARY_SUBSCR    
          61  LOAD_FAST             1  'ret_info'
          64  LOAD_CONST            3  'sub_idx'
          67  STORE_SUBSCR     
          68  JUMP_FORWARD          0  'to 71'
        71_0  COME_FROM                '68'

 106      71  LOAD_CONST            4  'extra_info'
          74  LOAD_FAST             0  'source_info'
          77  COMPARE_OP            6  'in'
          80  POP_JUMP_IF_FALSE    97  'to 97'

 107      83  POP_JUMP_IF_FALSE     4  'to 4'
          86  BINARY_SUBSCR    
          87  LOAD_FAST             1  'ret_info'
          90  LOAD_CONST            4  'extra_info'
          93  STORE_SUBSCR     
          94  JUMP_FORWARD          0  'to 97'
        97_0  COME_FROM                '94'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 12
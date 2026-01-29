# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/charm_utils.py
from __future__ import absolute_import
from logic.gutils.item_utils import get_item_rare_degree, get_lobby_item_type, get_lobby_item_is_forbid_charm
from logic.gcommon.cdata import charm_data

def show_charm_up_tips_and_update_charm_value(item_list):
    if not global_data.player:
        return
    orignal_charm_value = global_data.player.get_charm_value()
    changed_charm_value = 0
    for item_id, item_num in item_list:
        if get_lobby_item_is_forbid_charm(item_id):
            continue
        item = global_data.player.get_item_by_no(item_id)
        if not item or item.get_expire_time() != -1:
            continue
        item_type = get_lobby_item_type(item_id)
        item_degress = get_item_rare_degree(item_id)
        changed_charm_value += item_num * charm_data.get_charm(item_type, item_degress)
        global_data.player.update_charm(item_num, item_type, item_degress)

    if changed_charm_value != 0:
        show_charm_tips(orignal_charm_value, changed_charm_value)


def show_charm_tips--- This code section failed: ---

  27       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('tips_const',)
           6  IMPORT_NAME           0  'logic.client.const'
           9  IMPORT_FROM           1  'tips_const'
          12  STORE_FAST            2  'tips_const'
          15  POP_TOP          

  28      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('LobbyInfoUI',)
          22  IMPORT_NAME           2  'logic.comsys.lobby.LobbyInfoUI'
          25  IMPORT_FROM           3  'LobbyInfoUI'
          28  STORE_FAST            3  'LobbyInfoUI'
          31  POP_TOP          

  29      32  LOAD_GLOBAL           4  'global_data'
          35  LOAD_ATTR             5  'ui_mgr'
          38  LOAD_ATTR             6  'get_ui'
          41  LOAD_CONST            4  'LobbyInfoUI'
          44  CALL_FUNCTION_1       1 
          47  STORE_FAST            4  'ui_inst'

  30      50  LOAD_FAST             4  'ui_inst'
          53  POP_JUMP_IF_TRUE     66  'to 66'

  31      56  LOAD_FAST             3  'LobbyInfoUI'
          59  CALL_FUNCTION_0       0 
          62  POP_TOP          
          63  JUMP_FORWARD          0  'to 66'
        66_0  COME_FROM                '63'

  33      66  BUILD_MAP_4           4 
          69  LOAD_FAST             2  'tips_const'
          72  LOAD_ATTR             7  'LOBBY_SUB_CHARM_INFO'
          75  LOAD_CONST            5  'i_type'
          78  STORE_MAP        

  34      79  STORE_MAP        
          80  DELETE_SUBSCR    
          81  DELETE_SUBSCR    
          82  STORE_MAP        

  35      83  LOAD_FAST             0  'start_value'
          86  LOAD_FAST             1  'add_value'
          89  BINARY_ADD       
          90  LOAD_CONST            7  'show_num'
          93  STORE_MAP        

  36      94  BUILD_MAP_3           3 
          97  LOAD_CONST            8  'lab_up'
         100  LOAD_CONST            9  'node_name'
         103  STORE_MAP        

  37     104  LOAD_CONST           10  'SetString'
         107  LOAD_CONST           11  'func_name'
         110  STORE_MAP        

  38     111  LOAD_GLOBAL           8  'str'
         114  LOAD_FAST             1  'add_value'
         117  CALL_FUNCTION_1       1 
         120  BUILD_TUPLE_1         1 
         123  LOAD_CONST           12  'args'
         126  STORE_MAP        
         127  LOAD_CONST           13  'set_attr_dict'
         130  STORE_MAP        
         131  STORE_FAST            5  'msg'

  40     134  LOAD_GLOBAL           4  'global_data'
         137  LOAD_ATTR             9  'emgr'
         140  LOAD_ATTR            10  'lobby_tips_down_message_event'
         143  LOAD_ATTR            11  'emit'
         146  LOAD_FAST             5  'msg'
         149  LOAD_FAST             2  'tips_const'
         152  LOAD_ATTR            12  'LOBBY_MAIN_COMMON_INFO'
         155  CALL_FUNCTION_2       2 
         158  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 79
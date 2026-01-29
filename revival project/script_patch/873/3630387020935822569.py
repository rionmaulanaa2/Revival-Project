# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/homeland_utils.py
from __future__ import absolute_import
import json
from common import http
from logic.gcommon.common_const import homeland_const
import hashlib
from logic.gutils import micro_webservice_utils

def request_init_data():
    player = global_data.player
    if not player:
        return
    uid = player.get_visit_uid() or player.uid
    request_homeland_data({'req_type': homeland_const.HOMELAND_REQUEST_INIT_HOMEPAGE,'uid': uid})


def left_message--- This code section failed: ---

  21       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            1  'player'

  22       9  LOAD_FAST             1  'player'
          12  POP_JUMP_IF_TRUE     19  'to 19'

  23      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

  24      19  LOAD_FAST             1  'player'
          22  LOAD_ATTR             2  'get_visit_uid'
          25  CALL_FUNCTION_0       0 
          28  JUMP_IF_TRUE_OR_POP    37  'to 37'
          31  LOAD_FAST             1  'player'
          34  LOAD_ATTR             3  'uid'
        37_0  COME_FROM                '28'
          37  STORE_FAST            2  'uid'

  25      40  LOAD_FAST             1  'player'
          43  LOAD_ATTR             3  'uid'
          46  STORE_FAST            3  'sub_uid'

  26      49  LOAD_GLOBAL           4  'request_homeland_data'
          52  BUILD_MAP_4           4 
          55  LOAD_GLOBAL           5  'homeland_const'
          58  LOAD_ATTR             6  'HOMELAND_REQUEST_NEW_MESSAGE_BLOCK'
          61  LOAD_CONST            1  'req_type'
          64  STORE_MAP        
          65  LOAD_FAST             2  'uid'
          68  LOAD_CONST            2  'uid'
          71  STORE_MAP        
          72  LOAD_FAST             3  'sub_uid'
          75  LOAD_CONST            3  'sub_uid'
          78  STORE_MAP        
          79  STORE_MAP        
          80  STORE_MAP        
          81  STORE_MAP        
          82  STORE_MAP        
          83  CALL_FUNCTION_1       1 
          86  POP_TOP          

  28      87  LOAD_GLOBAL           0  'global_data'
          90  LOAD_ATTR             7  'message_data'
          93  LOAD_ATTR             8  'get_seting_inf'
          96  LOAD_CONST            5  'message_board_left_count'
          99  CALL_FUNCTION_1       1 
         102  JUMP_IF_TRUE_OR_POP   108  'to 108'
         105  BUILD_MAP_0           0 
       108_0  COME_FROM                '102'
         108  STORE_FAST            4  'left_message_count'

  29     111  LOAD_FAST             4  'left_message_count'
         114  LOAD_ATTR             9  'get'
         117  LOAD_GLOBAL          10  'int'
         120  LOAD_FAST             2  'uid'
         123  CALL_FUNCTION_1       1 
         126  LOAD_CONST            6  ''
         129  LOAD_CONST            6  ''
         132  BUILD_LIST_2          2 
         135  CALL_FUNCTION_2       2 
         138  UNPACK_SEQUENCE_2     2 
         141  STORE_FAST            5  'count'
         144  STORE_FAST            6  'day'

  30     147  LOAD_FAST             5  'count'
         150  LOAD_CONST            7  1
         153  INPLACE_ADD      
         154  STORE_FAST            5  'count'

  31     157  LOAD_CONST            6  ''
         160  LOAD_CONST            8  ('time_utility',)
         163  IMPORT_NAME          11  'logic.gcommon'
         166  IMPORT_FROM          12  'time_utility'
         169  STORE_FAST            7  'tutil'
         172  POP_TOP          

  32     173  LOAD_FAST             5  'count'
         176  LOAD_FAST             7  'tutil'
         179  LOAD_ATTR            13  'get_rela_day_no'
         182  CALL_FUNCTION_0       0 
         185  BUILD_LIST_2          2 
         188  LOAD_FAST             4  'left_message_count'
         191  LOAD_GLOBAL          10  'int'
         194  LOAD_FAST             2  'uid'
         197  CALL_FUNCTION_1       1 
         200  STORE_SUBSCR     

  33     201  LOAD_GLOBAL           0  'global_data'
         204  LOAD_ATTR             7  'message_data'
         207  LOAD_ATTR            14  'set_seting_inf'
         210  LOAD_CONST            5  'message_board_left_count'
         213  LOAD_FAST             4  'left_message_count'
         216  CALL_FUNCTION_2       2 
         219  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 79


def request_more_data_max():
    player = global_data.player
    if not player:
        return
    uid = player.get_visit_uid() or player.uid
    sub_uid = player.uid
    max_id = global_data.message_board_mgr.get_max_bid()
    request_homeland_data({'req_type': homeland_const.HOMELAND_REQUEST_PULL_MESSAGE_BODY_BY_HIGHER_LIMIT,'uid': uid,'sub_uid': sub_uid,'max_bid': max_id,'limit': 20})


def del_message(bid):
    player = global_data.player
    if not player:
        return
    uid = player.get_visit_uid() or player.uid
    request_homeland_data({'req_type': homeland_const.HOMELAND_REQUEST_DELETE_MESSAGE_BLOCK,'uid': uid,'bids': [bid]})


def reply_message--- This code section failed: ---

  55       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            2  'player'

  56       9  LOAD_FAST             2  'player'
          12  POP_JUMP_IF_TRUE     19  'to 19'

  57      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

  58      19  LOAD_FAST             2  'player'
          22  LOAD_ATTR             2  'get_visit_uid'
          25  CALL_FUNCTION_0       0 
          28  JUMP_IF_TRUE_OR_POP    37  'to 37'
          31  LOAD_FAST             2  'player'
          34  LOAD_ATTR             3  'uid'
        37_0  COME_FROM                '28'
          37  STORE_FAST            3  'uid'

  59      40  LOAD_FAST             2  'player'
          43  LOAD_ATTR             3  'uid'
          46  STORE_FAST            4  'sub_uid'

  60      49  LOAD_GLOBAL           4  'request_homeland_data'
          52  BUILD_MAP_5           5 
          55  LOAD_GLOBAL           5  'homeland_const'
          58  LOAD_ATTR             6  'HOMELAND_REQUEST_REPLAY_MESSAGE'
          61  LOAD_CONST            1  'req_type'
          64  STORE_MAP        
          65  LOAD_FAST             3  'uid'
          68  LOAD_CONST            2  'uid'
          71  STORE_MAP        
          72  STORE_MAP        
          73  PRINT_ITEM_TO    
          74  PRINT_ITEM_TO    
          75  STORE_MAP        
          76  LOAD_FAST             4  'sub_uid'
          79  LOAD_CONST            4  'sub_uid'
          82  STORE_MAP        
          83  LOAD_FAST             1  'msg'
          86  LOAD_CONST            5  'msg'
          89  STORE_MAP        
          90  CALL_FUNCTION_1       1 
          93  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 72


def del_reply--- This code section failed: ---

  63       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            2  'player'

  64       9  LOAD_FAST             2  'player'
          12  POP_JUMP_IF_TRUE     19  'to 19'

  65      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

  66      19  LOAD_FAST             2  'player'
          22  LOAD_ATTR             2  'get_visit_uid'
          25  CALL_FUNCTION_0       0 
          28  JUMP_IF_TRUE_OR_POP    37  'to 37'
          31  LOAD_FAST             2  'player'
          34  LOAD_ATTR             3  'uid'
        37_0  COME_FROM                '28'
          37  STORE_FAST            3  'uid'

  67      40  LOAD_GLOBAL           4  'request_homeland_data'
          43  BUILD_MAP_4           4 
          46  LOAD_GLOBAL           5  'homeland_const'
          49  LOAD_ATTR             6  'HOMELAND_REQUEST_DELETE_MESSAGE'
          52  LOAD_CONST            1  'req_type'
          55  STORE_MAP        
          56  LOAD_FAST             3  'uid'
          59  LOAD_CONST            2  'uid'
          62  STORE_MAP        
          63  STORE_MAP        
          64  PRINT_ITEM_TO    
          65  PRINT_ITEM_TO    
          66  STORE_MAP        
          67  LOAD_FAST             1  'mid'
          70  LOAD_CONST            4  'mid'
          73  STORE_MAP        
          74  CALL_FUNCTION_1       1 
          77  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 63


def write_intro--- This code section failed: ---

  70       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            1  'player'

  71       9  LOAD_FAST             1  'player'
          12  POP_JUMP_IF_TRUE     19  'to 19'

  72      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

  73      19  LOAD_FAST             1  'player'
          22  LOAD_ATTR             2  'get_visit_uid'
          25  CALL_FUNCTION_0       0 
          28  JUMP_IF_TRUE_OR_POP    37  'to 37'
          31  LOAD_FAST             1  'player'
          34  LOAD_ATTR             3  'uid'
        37_0  COME_FROM                '28'
          37  STORE_FAST            2  'uid'

  74      40  LOAD_GLOBAL           4  'request_homeland_data'
          43  BUILD_MAP_3           3 
          46  LOAD_GLOBAL           5  'homeland_const'
          49  LOAD_ATTR             6  'HOMELAND_REQUEST_INTRODUCE'
          52  LOAD_CONST            1  'req_type'
          55  STORE_MAP        
          56  LOAD_FAST             2  'uid'
          59  LOAD_CONST            2  'uid'
          62  STORE_MAP        
          63  STORE_MAP        
          64  PRINT_ITEM_TO    
          65  PRINT_ITEM_TO    
          66  STORE_MAP        
          67  CALL_FUNCTION_1       1 
          70  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 63


def give_like--- This code section failed: ---

  77       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'player'
           6  STORE_FAST            3  'player'

  78       9  LOAD_FAST             3  'player'
          12  POP_JUMP_IF_TRUE     19  'to 19'

  79      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

  80      19  LOAD_FAST             3  'player'
          22  LOAD_ATTR             2  'get_visit_uid'
          25  CALL_FUNCTION_0       0 
          28  JUMP_IF_TRUE_OR_POP    37  'to 37'
          31  LOAD_FAST             3  'player'
          34  LOAD_ATTR             3  'uid'
        37_0  COME_FROM                '28'
          37  STORE_FAST            4  'uid'

  81      40  LOAD_FAST             3  'player'
          43  LOAD_ATTR             3  'uid'
          46  STORE_FAST            5  'sub_uid'

  82      49  LOAD_FAST             2  'cancel'
          52  POP_JUMP_IF_TRUE    103  'to 103'

  83      55  LOAD_GLOBAL           4  'request_homeland_data'
          58  BUILD_MAP_5           5 
          61  LOAD_GLOBAL           5  'homeland_const'
          64  LOAD_ATTR             6  'HOMELAND_REQUEST_THUMB'
          67  LOAD_CONST            1  'req_type'
          70  STORE_MAP        
          71  LOAD_FAST             4  'uid'
          74  LOAD_CONST            2  'uid'
          77  STORE_MAP        
          78  LOAD_FAST             5  'sub_uid'
          81  LOAD_CONST            3  'sub_uid'
          84  STORE_MAP        
          85  STORE_MAP        
          86  STORE_MAP        
          87  STORE_MAP        
          88  STORE_MAP        
          89  LOAD_FAST             1  'mid'
          92  LOAD_CONST            5  'mid'
          95  STORE_MAP        
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          
         100  JUMP_FORWARD         45  'to 148'

  85     103  LOAD_GLOBAL           4  'request_homeland_data'
         106  BUILD_MAP_5           5 
         109  LOAD_GLOBAL           5  'homeland_const'
         112  LOAD_ATTR             7  'HOMELAND_REQUEST_CANCEL_THUMB'
         115  LOAD_CONST            1  'req_type'
         118  STORE_MAP        
         119  LOAD_FAST             4  'uid'
         122  LOAD_CONST            2  'uid'
         125  STORE_MAP        
         126  LOAD_FAST             5  'sub_uid'
         129  LOAD_CONST            3  'sub_uid'
         132  STORE_MAP        
         133  STORE_MAP        
         134  STORE_MAP        
         135  STORE_MAP        
         136  STORE_MAP        
         137  LOAD_FAST             1  'mid'
         140  LOAD_CONST            5  'mid'
         143  STORE_MAP        
         144  CALL_FUNCTION_1       1 
         147  POP_TOP          
       148_0  COME_FROM                '100'

Parse error at or near `STORE_MAP' instruction at offset 85


def show_info(info_tag):
    msg = homeland_const.HOMELAND_REPLAY_MSG.get(info_tag)
    if msg:
        global_data.game_mgr.show_tip(msg)


def homeland_callback(result, args):
    if not result:
        return
    all_data = result.get('data') or {}
    info_tag = all_data.get('info', 0)
    show_info(info_tag)
    if result.get('msg') == 'success':
        req_type = all_data.get('req_type')
        if req_type == homeland_const.HOMELAND_REQUEST_INIT_HOMEPAGE:
            data = all_data.get('data', [])
            if data:
                data = data[0]
                global_data.message_board_mgr.init_message_data(data)
            else:
                global_data.message_board_mgr.init_message_data({})
        elif req_type == homeland_const.HOMELAND_REQUEST_PULL_MESSAGE_BODY:
            pass
        elif req_type == homeland_const.HOMELAND_REQUEST_NEW_MESSAGE_BLOCK:
            request_init_data()
        elif req_type == homeland_const.HOMELAND_REQUEST_PULL_MESSAGE_BODY_BY_HIGHER_LIMIT:
            data = all_data.get('data', [])
            global_data.message_board_mgr.extend_message_data(data)


def request_homeland_data(data={}, cb=homeland_callback):
    req_type = data.get('req_type')
    if not req_type:
        return
    if req_type in homeland_const.HOMELAND_GAME_ONLY_REQUEST:
        player = global_data.player
        if player:
            player.call_server_method('homeland_req', (data,))
    else:
        micro_webservice_utils.micro_service_request('HomelandService', data, cb)
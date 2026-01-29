# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/search_salog_utils.py
from __future__ import absolute_import
from logic.gutils.salog import SALog
from logic.gcommon.common_utils.text_utils import check_review_words
import logic.gcommon.time_utility as tutil

def add_common_search_salog--- This code section failed: ---

  10       0  LOAD_GLOBAL           0  'check_review_words'
           3  LOAD_FAST             0  'search_content'
           6  CALL_FUNCTION_1       1 
           9  UNPACK_SEQUENCE_2     2 
          12  STORE_FAST            1  'review_pass'
          15  STORE_FAST            2  'msg'

  11      18  LOAD_GLOBAL           1  'global_data'
          21  LOAD_ATTR             2  'player'
          24  STORE_FAST            3  'player'

  12      27  LOAD_FAST             3  'player'
          30  POP_JUMP_IF_TRUE     37  'to 37'

  13      33  LOAD_CONST            0  ''
          36  RETURN_END_IF    
        37_0  COME_FROM                '30'

  14      37  BUILD_MAP_6           6 

  15      40  LOAD_GLOBAL           3  'tutil'
          43  LOAD_ATTR             4  'get_time'
          46  CALL_FUNCTION_0       0 
          49  LOAD_CONST            1  'time'
          52  STORE_MAP        

  16      53  LOAD_FAST             3  'player'
          56  LOAD_ATTR             5  'uid'
          59  LOAD_CONST            2  'role_id'
          62  STORE_MAP        

  17      63  LOAD_FAST             3  'player'
          66  LOAD_ATTR             6  'get_name'
          69  CALL_FUNCTION_0       0 
          72  LOAD_CONST            3  'role_name'
          75  STORE_MAP        

  18      76  LOAD_FAST             3  'player'
          79  LOAD_ATTR             7  'get_lv'
          82  CALL_FUNCTION_0       0 
          85  LOAD_CONST            4  'role_level'
          88  STORE_MAP        

  19      89  STORE_MAP        
          90  INPLACE_POWER    
          91  INPLACE_POWER    
          92  STORE_MAP        

  20      93  LOAD_FAST             1  'review_pass'
          96  LOAD_CONST            6  'result'
          99  STORE_MAP        
         100  STORE_FAST            4  'log_info'

  22     103  LOAD_FAST             3  'player'
         106  LOAD_ATTR             8  'call_server_method'
         109  LOAD_CONST            7  'client_sa_log'
         112  LOAD_CONST            5  'search'
         115  LOAD_FAST             4  'log_info'
         118  BUILD_TUPLE_2         2 
         121  CALL_FUNCTION_2       2 
         124  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 89
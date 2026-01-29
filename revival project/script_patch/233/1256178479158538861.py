# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/debug/__init__.py
from __future__ import absolute_import
from . import async_test

def is_client_debug--- This code section failed: ---

   9       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('check_file_exist',)
           6  IMPORT_NAME           0  'common.utils.path'
           9  IMPORT_FROM           1  'check_file_exist'
          12  STORE_FAST            0  'check_file_exist'
          15  POP_TOP          

  10      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  CALL_FUNCTION_1       1 
          22  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 16


def init_display_debug_msg_win():
    import C_debug
    import logoutput
    if is_client_debug():
        C_debug.show_console_window(True)
    logoutput.init()


def display_debug_msg_win(flag):
    import C_debug
    C_debug.show_console_window(flag)


def debug_get_func_info--- This code section failed: ---

  29       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'inspect'
           9  STORE_FAST            1  'inspect'

  30      12  LOAD_FAST             1  'inspect'
          15  LOAD_ATTR             1  'ismethod'
          18  LOAD_FAST             0  'f'
          21  CALL_FUNCTION_1       1 
          24  POP_JUMP_IF_TRUE     42  'to 42'
          27  LOAD_FAST             1  'inspect'
          30  LOAD_ATTR             2  'isfunction'
          33  LOAD_FAST             0  'f'
          36  CALL_FUNCTION_1       1 
        39_0  COME_FROM                '24'
          39  POP_JUMP_IF_FALSE    51  'to 51'

  32      42  LOAD_FAST             0  'f'
          45  STORE_FAST            2  'func'
          48  JUMP_FORWARD         38  'to 89'

  33      51  LOAD_GLOBAL           3  'hasattr'
          54  LOAD_GLOBAL           2  'isfunction'
          57  CALL_FUNCTION_2       2 
          60  POP_JUMP_IF_FALSE    75  'to 75'

  35      63  LOAD_FAST             0  'f'
          66  LOAD_ATTR             4  'fn'
          69  STORE_FAST            2  'func'
          72  JUMP_FORWARD         14  'to 89'

  37      75  LOAD_CONST            3  'UnsupportType: %s'
          78  LOAD_GLOBAL           5  'type'
          81  LOAD_FAST             0  'f'
          84  CALL_FUNCTION_1       1 
          87  BINARY_MODULO    
          88  RETURN_VALUE     
        89_0  COME_FROM                '72'
        89_1  COME_FROM                '48'

  38      89  SETUP_EXCEPT         25  'to 117'

  39      92  LOAD_GLOBAL           6  'str'
          95  LOAD_FAST             1  'inspect'
          98  LOAD_ATTR             7  'getfile'
         101  LOAD_FAST             2  'func'
         104  CALL_FUNCTION_1       1 
         107  CALL_FUNCTION_1       1 
         110  STORE_FAST            3  'trace'
         113  POP_BLOCK        
         114  JUMP_FORWARD         37  'to 154'
       117_0  COME_FROM                '89'

  40     117  DUP_TOP          
         118  LOAD_GLOBAL           8  'Exception'
         121  COMPARE_OP           10  'exception-match'
         124  POP_JUMP_IF_FALSE   153  'to 153'
         127  POP_TOP          
         128  STORE_FAST            4  'e'
         131  POP_TOP          

  41     132  LOAD_CONST            4  'Get trace Error:'
         135  LOAD_GLOBAL           6  'str'
         138  LOAD_FAST             4  'e'
         141  CALL_FUNCTION_1       1 
         144  BUILD_TUPLE_2         2 
         147  STORE_FAST            3  'trace'
         150  JUMP_FORWARD          1  'to 154'
         153  END_FINALLY      
       154_0  COME_FROM                '153'
       154_1  COME_FROM                '114'

  42     154  SETUP_EXCEPT         25  'to 182'

  43     157  LOAD_GLOBAL           6  'str'
         160  LOAD_FAST             1  'inspect'
         163  LOAD_ATTR             9  'getsourcelines'
         166  LOAD_FAST             2  'func'
         169  CALL_FUNCTION_1       1 
         172  CALL_FUNCTION_1       1 
         175  STORE_FAST            5  'trace_line_list'
         178  POP_BLOCK        
         179  JUMP_FORWARD         37  'to 219'
       182_0  COME_FROM                '154'

  44     182  DUP_TOP          
         183  LOAD_GLOBAL           8  'Exception'
         186  COMPARE_OP           10  'exception-match'
         189  POP_JUMP_IF_FALSE   218  'to 218'
         192  POP_TOP          
         193  STORE_FAST            4  'e'
         196  POP_TOP          

  45     197  LOAD_CONST            5  'Get line_no Error:'
         200  LOAD_GLOBAL           6  'str'
         203  LOAD_FAST             4  'e'
         206  CALL_FUNCTION_1       1 
         209  BUILD_TUPLE_2         2 
         212  STORE_FAST            5  'trace_line_list'
         215  JUMP_FORWARD          1  'to 219'
         218  END_FINALLY      
       219_0  COME_FROM                '218'
       219_1  COME_FROM                '179'

  46     219  LOAD_FAST             2  'func'
         222  LOAD_ATTR            10  '__name__'
         225  LOAD_CONST            6  ', Trace:'
         228  BINARY_ADD       
         229  LOAD_FAST             3  'trace'
         232  BINARY_ADD       
         233  LOAD_CONST            7  ',line_no:'
         236  BINARY_ADD       
         237  LOAD_GLOBAL           6  'str'
         240  LOAD_FAST             5  'trace_line_list'
         243  CALL_FUNCTION_1       1 
         246  BINARY_ADD       
         247  STORE_FAST            6  'info'

  47     250  LOAD_FAST             6  'info'
         253  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 57
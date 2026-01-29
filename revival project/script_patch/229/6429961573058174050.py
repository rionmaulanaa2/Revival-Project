# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/delay.py
from __future__ import absolute_import
from logic.gcommon import utility as util
import sys
func_2_handler = {}
handler_2_func = {}

def __raise_inner_error(_str):
    import exception_hook
    exception_hook.upload_exception(*sys.exc_info())


def __debug_call(func):
    if func not in func_2_handler:
        err = 'DELAY CALL ERROR: try to call an unexisted func, erro:%s\n' % util.debug_get_func_info(func)
        err += util.get_output_stack_str()
        __raise_inner_error(err)
        return
    h = func_2_handler[func]
    del func_2_handler[func]
    del handler_2_func[h]
    func()


def call--- This code section failed: ---

  34       0  LOAD_DEREF            0  'func'
           3  LOAD_GLOBAL           0  'func_2_handler'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    84  'to 84'

  35      12  LOAD_CONST            1  'DELAY CALL ERROR: found duplicate func, erro:%s\n'
          15  LOAD_GLOBAL           1  'util'
          18  LOAD_ATTR             2  'debug_get_func_info'
          21  LOAD_DEREF            0  'func'
          24  CALL_FUNCTION_1       1 
          27  BINARY_MODULO    
          28  STORE_FAST            3  'err'

  36      31  LOAD_FAST             3  'err'
          34  LOAD_GLOBAL           1  'util'
          37  LOAD_ATTR             3  'get_output_stack_str'
          40  CALL_FUNCTION_0       0 
          43  INPLACE_ADD      
          44  STORE_FAST            3  'err'

  37      47  LOAD_GLOBAL           4  '__raise_inner_error'
          50  LOAD_FAST             3  'err'
          53  CALL_FUNCTION_1       1 
          56  POP_TOP          

  39      57  LOAD_GLOBAL           0  'func_2_handler'
          60  LOAD_DEREF            0  'func'
          63  BINARY_SUBSCR    
          64  STORE_FAST            4  'h'

  40      67  LOAD_GLOBAL           0  'func_2_handler'
          70  LOAD_DEREF            0  'func'
          73  DELETE_SUBSCR    

  41      74  LOAD_GLOBAL           5  'handler_2_func'
          77  LOAD_FAST             4  'h'
          80  DELETE_SUBSCR    
          81  JUMP_FORWARD          0  'to 84'
        84_0  COME_FROM                '81'

  43      84  LOAD_CONST            2  ''
          87  LOAD_CONST            0  ''
          90  IMPORT_NAME           6  'game3d'
          93  STORE_FAST            5  'game3d'

  44      96  LOAD_FAST             5  'game3d'
          99  LOAD_ATTR             7  'delay_exec'
         102  LOAD_ATTR             3  'get_output_stack_str'
         105  BINARY_MULTIPLY  
         106  LOAD_CLOSURE          0  'func'
         112  LOAD_LAMBDA              '<code_object <lambda>>'
         115  MAKE_CLOSURE_0        0 
         118  LOAD_CONST            5  ''
         121  LOAD_FAST             2  'speed_scale_influenced'
         124  CALL_FUNCTION_4       4 
         127  STORE_FAST            4  'h'

  46     130  LOAD_FAST             4  'h'
         133  LOAD_GLOBAL           0  'func_2_handler'
         136  LOAD_DEREF            0  'func'
         139  STORE_SUBSCR     

  47     140  LOAD_DEREF            0  'func'
         143  LOAD_GLOBAL           5  'handler_2_func'
         146  LOAD_FAST             4  'h'
         149  STORE_SUBSCR     

  49     150  LOAD_FAST             4  'h'
         153  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_MULTIPLY' instruction at offset 105


def cancel(handler):
    if handler not in handler_2_func:
        err = 'DELAY CALL ERROR: try to remove an nonexisted func\n'
        err += util.get_output_stack_str()
        __raise_inner_error(err)
        return
    func = handler_2_func[handler]
    del func_2_handler[func]
    del handler_2_func[handler]
    import game3d
    game3d.cancel_delay_exec(handler)
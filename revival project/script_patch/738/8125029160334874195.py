# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/client_utils.py
from __future__ import absolute_import
import sys
from exception_hook import dump_exception_hook

def __post_exec(insd, func, *args, **kargs):
    insd[id(func)] = False
    func(*args, **kargs)


def post_method(func):

    def wrapper--- This code section failed: ---

  12       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'game_mgr'
           6  POP_JUMP_IF_FALSE    93  'to 93'

  13       9  POP_JUMP_IF_FALSE     1  'to 1'
          12  BINARY_SUBSCR    
          13  LOAD_ATTR             2  '__dict__'
          16  STORE_FAST            2  'insd'

  14      19  LOAD_FAST             2  'insd'
          22  LOAD_ATTR             3  'get'
          25  LOAD_GLOBAL           4  'id'
          28  LOAD_DEREF            0  'func'
          31  CALL_FUNCTION_1       1 
          34  LOAD_GLOBAL           5  'False'
          37  CALL_FUNCTION_2       2 
          40  POP_JUMP_IF_TRUE    106  'to 106'

  15      43  LOAD_GLOBAL           6  'True'
          46  LOAD_FAST             2  'insd'
          49  LOAD_GLOBAL           4  'id'
          52  LOAD_DEREF            0  'func'
          55  CALL_FUNCTION_1       1 
          58  STORE_SUBSCR     

  16      59  LOAD_GLOBAL           0  'global_data'
          62  LOAD_ATTR             1  'game_mgr'
          65  LOAD_ATTR             7  'post_exec'
          68  LOAD_GLOBAL           8  '__post_exec'
          71  LOAD_FAST             2  'insd'
          74  LOAD_DEREF            0  'func'
          77  LOAD_FAST             0  'args'
          80  LOAD_FAST             1  'kargs'
          83  CALL_FUNCTION_VAR_KW_3     3 
          86  POP_TOP          
          87  JUMP_ABSOLUTE       106  'to 106'
          90  JUMP_FORWARD         13  'to 106'

  18      93  LOAD_DEREF            0  'func'
          96  LOAD_FAST             0  'args'
          99  LOAD_FAST             1  'kargs'
         102  CALL_FUNCTION_VAR_KW_0     0 
         105  POP_TOP          
       106_0  COME_FROM                '90'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 9

    return wrapper


def post_function(func):

    def wrapper(*args, **kargs):
        if global_data.game_mgr:
            insd = func.__dict__
            if not insd.get(id(func), False):
                insd[id(func)] = True
                global_data.game_mgr.post_exec(__post_exec, insd, func, *args, **kargs)
        else:
            func(*args, **kargs)

    return wrapper


def __post_ui_exec(func, self, *args, **kargs):
    self.__dict__[id(func)] = False
    if not self.panel or self.panel.IsDestroyed():
        return
    func(self, *args, **kargs)


def post_ui_method(func):

    def wrapper(self, *args, **kargs):
        if global_data.game_mgr:
            insd = self.__dict__
            if not insd.get(id(func), False):
                insd[id(func)] = True
                global_data.game_mgr.finish_exec(__post_ui_exec, func, self, *args, **kargs)
        else:
            func(*args, **kargs)

    return wrapper


def safe_call(func):

    def wrapper(*args, **kargs):
        try:
            return func(*args, **kargs)
        except:
            dump_exception_hook(*sys.exc_info())
            return None

        return None

    return wrapper


def online_call(func):

    def wrapper(*args, **kargs):
        if not global_data.player:
            global_data.game_mgr.show_tip(258)
            return
        return func(*args, **kargs)

    return wrapper


def safe_widget(func):

    def wrapper(self, *args, **kargs):
        try:
            return func(self, *args, **kargs)
        except:
            setattr(self, func.__name__[5:], None)
            dump_exception_hook(*sys.exc_info())
            return

        return

    return wrapper
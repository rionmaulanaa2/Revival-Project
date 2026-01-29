# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/MetaUtils.py
iteritems = None

def init--- This code section failed: ---

  10       0  BUILD_MAP_0           0 
           3  STORE_FAST            0  't'

  11       6  LOAD_GLOBAL           0  'hasattr'
           9  LOAD_GLOBAL           1  'iteritems'
          12  CALL_FUNCTION_2       2 
          15  POP_JUMP_IF_FALSE    30  'to 30'

  12      18  LOAD_CONST               '<code_object iteritems>'
          21  MAKE_FUNCTION_0       0 
          24  STORE_GLOBAL          1  'iteritems'
          27  JUMP_FORWARD          9  'to 39'

  15      30  LOAD_CONST               '<code_object iteritems>'
          33  MAKE_FUNCTION_0       0 
          36  STORE_GLOBAL          1  'iteritems'
        39_0  COME_FROM                '27'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12


init()
# global iteritems ## Warning: Unused global
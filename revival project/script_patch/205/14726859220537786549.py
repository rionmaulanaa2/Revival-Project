# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/safaia_six.py
import sys
import types
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    if sys.platform.startswith('java'):
        MAXSIZE = int(2147483647)
    else:

        class X(object):

            def __len__(self):
                return 2147483648


        try:
            len(X())
        except OverflowError:
            MAXSIZE = int(2147483647)
        else:
            MAXSIZE = int(9223372036854775807)

        del X

def with_metaclass(meta, *bases):

    class metaclass(type):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

        @classmethod
        def __prepare__(cls, name, this_bases):
            return meta.__prepare__(name, bases)

    return type.__new__(metaclass, 'temporary_class', (), {})


def add_metaclass(metaclass):

    def wrapper--- This code section failed: ---

  66       0  LOAD_FAST             0  'cls'
           3  LOAD_ATTR             0  '__dict__'
           6  LOAD_ATTR             1  'copy'
           9  CALL_FUNCTION_0       0 
          12  STORE_FAST            1  'orig_vars'

  67      15  LOAD_FAST             1  'orig_vars'
          18  LOAD_ATTR             2  'get'
          21  LOAD_CONST            1  '__slots__'
          24  CALL_FUNCTION_1       1 
          27  STORE_FAST            2  'slots'

  68      30  LOAD_FAST             2  'slots'
          33  LOAD_CONST            0  ''
          36  COMPARE_OP            9  'is-not'
          39  POP_JUMP_IF_FALSE   102  'to 102'

  69      42  LOAD_GLOBAL           4  'isinstance'
          45  LOAD_FAST             2  'slots'
          48  LOAD_GLOBAL           5  'str'
          51  CALL_FUNCTION_2       2 
          54  POP_JUMP_IF_FALSE    69  'to 69'

  70      57  LOAD_FAST             2  'slots'
          60  BUILD_LIST_1          1 
          63  STORE_FAST            2  'slots'
          66  JUMP_FORWARD          0  'to 69'
        69_0  COME_FROM                '66'

  71      69  SETUP_LOOP           30  'to 102'
          72  LOAD_FAST             2  'slots'
          75  GET_ITER         
          76  FOR_ITER             19  'to 98'
          79  STORE_FAST            3  'slots_var'

  72      82  LOAD_FAST             1  'orig_vars'
          85  LOAD_ATTR             6  'pop'
          88  LOAD_FAST             3  'slots_var'
          91  CALL_FUNCTION_1       1 
          94  POP_TOP          
          95  JUMP_BACK            76  'to 76'
          98  POP_BLOCK        
        99_0  COME_FROM                '69'
          99  JUMP_FORWARD          0  'to 102'
       102_0  COME_FROM                '69'

  73     102  LOAD_FAST             1  'orig_vars'
         105  LOAD_ATTR             6  'pop'
         108  LOAD_CONST            2  '__dict__'
         111  LOAD_CONST            0  ''
         114  CALL_FUNCTION_2       2 
         117  POP_TOP          

  74     118  LOAD_FAST             1  'orig_vars'
         121  LOAD_ATTR             6  'pop'
         124  LOAD_CONST            3  '__weakref__'
         127  LOAD_CONST            0  ''
         130  CALL_FUNCTION_2       2 
         133  POP_TOP          

  75     134  LOAD_GLOBAL           7  'hasattr'
         137  LOAD_GLOBAL           4  'isinstance'
         140  CALL_FUNCTION_2       2 
         143  POP_JUMP_IF_FALSE   162  'to 162'

  76     146  LOAD_FAST             0  'cls'
         149  LOAD_ATTR             8  '__qualname__'
         152  LOAD_FAST             1  'orig_vars'
         155  LOAD_CONST            4  '__qualname__'
         158  STORE_SUBSCR     
         159  JUMP_FORWARD          0  'to 162'
       162_0  COME_FROM                '159'

  77     162  LOAD_DEREF            0  'metaclass'
         165  LOAD_FAST             0  'cls'
         168  LOAD_ATTR             9  '__name__'
         171  LOAD_FAST             0  'cls'
         174  LOAD_ATTR            10  '__bases__'
         177  LOAD_FAST             1  'orig_vars'
         180  CALL_FUNCTION_3       3 
         183  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 140

    return wrapper
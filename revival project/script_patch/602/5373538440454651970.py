# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/cython/cython_utils/init_cython.py


def init(script_dir, to_build, to_load, build_dir=None, debug=False, profile=False, assertions=True, use_default_python=True, module_filter=None):
    import sys
    import os
    this_file = os.path.abspath(__file__)
    if to_build and os.path.isfile(this_file) and (sys.platform.startswith('win') or sys.platform.startswith('linux')):
        this_dir = os.path.dirname(this_file)
        cython_dir = os.path.dirname(this_dir)
        sys.path.insert(0, cython_dir)

        def build_and_load--- This code section failed: ---

  40       0  LOAD_CONST            1  -1
           3  LOAD_CONST            2  ('DistutilsPlatformError',)
           6  IMPORT_NAME           0  'distutils.errors'
           9  IMPORT_FROM           1  'DistutilsPlatformError'
          12  STORE_FAST            1  'DistutilsPlatformError'
          15  POP_TOP          

  41      16  LOAD_CONST            1  -1
          19  LOAD_CONST            3  ('run_build', 'load_extension')
          22  IMPORT_NAME           2  'staticbuild'
          25  IMPORT_FROM           3  'run_build'
          28  STORE_FAST            2  'run_build'
          31  IMPORT_FROM           4  'load_extension'
          34  STORE_FAST            3  'load_extension'
          37  POP_TOP          

  42      38  SETUP_EXCEPT         54  'to 95'

  43      41  LOAD_CONST            4  'Building cython scripts...'
          44  PRINT_ITEM       
          45  PRINT_NEWLINE_CONT

  44      46  LOAD_FAST             2  'run_build'
          49  LOAD_ATTR             5  'build'

  45      52  LOAD_DEREF            0  'script_dir'

  46      55  LOAD_DEREF            5  'to_load'

  47      58  LOAD_DEREF            1  'debug'
          61  LOAD_CONST            6  'profile'

  48      64  LOAD_DEREF            2  'profile'
          67  LOAD_CONST            7  'static_lib'

  49      70  LOAD_GLOBAL           6  'False'
          73  LOAD_CONST            8  'assertions'

  50      76  LOAD_DEREF            3  'assertions'
          79  LOAD_CONST            9  'use_default_python'

  51      82  LOAD_DEREF            4  'use_default_python'
          85  CALL_FUNCTION_1282  1282 
          88  STORE_FAST            4  'so_path'
          91  POP_BLOCK        
          92  JUMP_FORWARD        111  'to 206'
        95_0  COME_FROM                '38'

  52      95  DUP_TOP          
          96  LOAD_FAST             1  'DistutilsPlatformError'
          99  COMPARE_OP           10  'exception-match'
         102  POP_JUMP_IF_FALSE   205  'to 205'
         105  POP_TOP          
         106  STORE_FAST            5  'ex'
         109  POP_TOP          

  56     110  LOAD_FAST             5  'ex'
         113  LOAD_ATTR             7  'message'
         116  LOAD_CONST           10  'Unable to find vcvarsall.bat'
         119  COMPARE_OP            2  '=='
         122  POP_JUMP_IF_FALSE   199  'to 199'

  57     125  LOAD_CONST           11  'Building cython scripts failed with the following exception:'
         128  PRINT_ITEM       
         129  PRINT_NEWLINE_CONT

  58     130  LOAD_CONST            1  -1
         133  LOAD_CONST            0  ''
         136  IMPORT_NAME           8  'traceback'
         139  STORE_FAST            6  'traceback'

  59     142  SETUP_LOOP           46  'to 191'
         145  LOAD_FAST             6  'traceback'
         148  LOAD_ATTR             9  'format_exception_only'
         151  LOAD_GLOBAL          10  'type'
         154  LOAD_FAST             5  'ex'
         157  CALL_FUNCTION_1       1 
         160  LOAD_FAST             5  'ex'
         163  CALL_FUNCTION_2       2 
         166  GET_ITER         
         167  FOR_ITER             20  'to 190'
         170  STORE_FAST            7  'line'

  60     173  LOAD_FAST             7  'line'
         176  LOAD_ATTR            11  'strip'
         179  LOAD_CONST           12  '\n'
         182  CALL_FUNCTION_1       1 
         185  PRINT_ITEM       
         186  PRINT_NEWLINE_CONT
         187  JUMP_BACK           167  'to 167'
         190  POP_BLOCK        
       191_0  COME_FROM                '142'

  61     191  LOAD_CONST           13  'Fallback to interpreted python.'
         194  PRINT_ITEM       
         195  PRINT_NEWLINE_CONT
         196  JUMP_ABSOLUTE       251  'to 251'

  63     199  RAISE_VARARGS_0       0 
         202  JUMP_FORWARD         46  'to 251'
         205  END_FINALLY      
       206_0  COME_FROM                '92'

  65     206  LOAD_CONST           14  'Building cython scripts succeeded.'
         209  PRINT_ITEM       
         210  PRINT_NEWLINE_CONT

  66     211  LOAD_DEREF            5  'to_load'
         214  POP_JUMP_IF_FALSE   247  'to 247'

  67     217  LOAD_CONST           15  'Loading cython scripts from %s'
         220  LOAD_FAST             4  'so_path'
         223  BINARY_MODULO    
         224  PRINT_ITEM       
         225  PRINT_NEWLINE_CONT

  68     226  LOAD_FAST             3  'load_extension'
         229  LOAD_FAST             4  'so_path'
         232  LOAD_DEREF            6  'module_filter'
         235  CALL_FUNCTION_2       2 
         238  POP_TOP          

  69     239  LOAD_CONST           16  'Loading cython scripts succeeded.'
         242  PRINT_ITEM       
         243  PRINT_NEWLINE_CONT
         244  JUMP_FORWARD          0  'to 247'
       247_0  COME_FROM                '244'

  70     247  LOAD_FAST             4  'so_path'
         250  RETURN_VALUE     
       251_0  COME_FROM                '205'

Parse error at or near `CALL_FUNCTION_1282' instruction at offset 85

        import lock_file
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        filePath = os.path.join(build_dir, 'build')
        fileLock = lock_file.FileLock(filePath)
        fileLock.acquire()
        result = build_and_load(build_dir)
        fileLock.release()
        return result
    if to_build:
        print 'Building cython scripts failed with the following error:'
        print 'Not possible to build cython scripts.'
    from .. import cython, load_essentials
    if to_load:
        try:
            print 'Loading cython scripts...'
            load_essentials.load_static_lib(module_filter)
            print 'Loading cython scripts succeeded.'
        except:
            print 'Loading cython scripts failed with the following exception:'
            import traceback
            traceback.format_exc()
            print 'Fallback to interpreted python.'

    cython_package = load_essentials.__name__.split('.')[:-1]
    del sys.modules['.'.join(cython_package)]
    del sys.modules['.'.join(cython_package + ['cython'])]
    sys.modules['cython'] = cython


class SampleModuleFilter(object):

    def filter(self, fullname):
        return True
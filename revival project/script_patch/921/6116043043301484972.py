# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/log/__init__.py
from __future__ import absolute_import
from __future__ import print_function
import sys
import logging
import traceback
import six
if six.PY2:
    import new
from common.framework import Singleton
from common.utils.time_utils import get_cur_time_str
from common.platform import is_win32

class SimpleLoger(Singleton):
    ALIAS_NAME = 'slog'

    def init(self):
        if is_win32():

            def info--- This code section failed: ---

  25       0  LOAD_GLOBAL           0  'print'
           3  LOAD_GLOBAL           1  'get_cur_time_str'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  '[INFO]'
          12  LOAD_CONST            2  'end'
          15  LOAD_CONST            3  ' '
          18  CALL_FUNCTION_259   259 
          21  POP_TOP          

  26      22  SETUP_LOOP           30  'to 55'
          25  LOAD_FAST             1  'args'
          28  GET_ITER         
          29  FOR_ITER             22  'to 54'
          32  STORE_FAST            2  'arg'

  27      35  LOAD_GLOBAL           0  'print'
          38  LOAD_FAST             2  'arg'
          41  LOAD_CONST            2  'end'
          44  LOAD_CONST            3  ' '
          47  CALL_FUNCTION_257   257 
          50  POP_TOP          
          51  JUMP_BACK            29  'to 29'
          54  POP_BLOCK        
        55_0  COME_FROM                '22'

  28      55  LOAD_GLOBAL           0  'print'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

            def debug--- This code section failed: ---

  31       0  LOAD_GLOBAL           0  'print'
           3  LOAD_GLOBAL           1  'get_cur_time_str'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  '[DEBUG]'
          12  LOAD_CONST            2  'end'
          15  LOAD_CONST            3  ' '
          18  CALL_FUNCTION_259   259 
          21  POP_TOP          

  32      22  SETUP_LOOP           30  'to 55'
          25  LOAD_FAST             1  'args'
          28  GET_ITER         
          29  FOR_ITER             22  'to 54'
          32  STORE_FAST            2  'arg'

  33      35  LOAD_GLOBAL           0  'print'
          38  LOAD_FAST             2  'arg'
          41  LOAD_CONST            2  'end'
          44  LOAD_CONST            3  ' '
          47  CALL_FUNCTION_257   257 
          50  POP_TOP          
          51  JUMP_BACK            29  'to 29'
          54  POP_BLOCK        
        55_0  COME_FROM                '22'

  34      55  LOAD_GLOBAL           0  'print'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

            def info_fmt(fmt, *args):
                print(get_cur_time_str(), '[INFO]', fmt.format(*args))

            def debug_fmt(fmt, *args):
                print(get_cur_time_str(), '[DEBUG]', fmt.format(*args))

            def info_fmtp(fmt, *args):
                print(get_cur_time_str(), '[INFO]', fmt % args)

            def debug_fmtp(fmt, *args):
                print(get_cur_time_str(), '[DEBUG]', fmt % args)

        else:

            def info(fmt, *args):
                pass

            def debug(fmt, *args):
                pass

            def info_fmt(fmt, *args):
                pass

            def debug_fmt(fmt, *args):
                pass

            def info_fmtp(fmt, *args):
                pass

            def debug_fmtp(fmt, *args):
                pass

        def error--- This code section failed: ---

  69       0  LOAD_GLOBAL           0  'print'
           3  LOAD_GLOBAL           1  'get_cur_time_str'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  '[ERROR]'
          12  LOAD_CONST            2  'end'
          15  LOAD_CONST            3  ' '
          18  CALL_FUNCTION_259   259 
          21  POP_TOP          

  70      22  SETUP_LOOP           30  'to 55'
          25  LOAD_FAST             1  'args'
          28  GET_ITER         
          29  FOR_ITER             22  'to 54'
          32  STORE_FAST            2  'arg'

  71      35  LOAD_GLOBAL           0  'print'
          38  LOAD_FAST             2  'arg'
          41  LOAD_CONST            2  'end'
          44  LOAD_CONST            3  ' '
          47  CALL_FUNCTION_257   257 
          50  POP_TOP          
          51  JUMP_BACK            29  'to 29'
          54  POP_BLOCK        
        55_0  COME_FROM                '22'

  72      55  LOAD_GLOBAL           0  'print'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

        def warning--- This code section failed: ---

  75       0  LOAD_GLOBAL           0  'print'
           3  LOAD_GLOBAL           1  'get_cur_time_str'
           6  CALL_FUNCTION_0       0 
           9  LOAD_CONST            1  '[WARNING]'
          12  LOAD_CONST            2  'end'
          15  LOAD_CONST            3  ' '
          18  CALL_FUNCTION_259   259 
          21  POP_TOP          

  76      22  SETUP_LOOP           30  'to 55'
          25  LOAD_FAST             1  'args'
          28  GET_ITER         
          29  FOR_ITER             22  'to 54'
          32  STORE_FAST            2  'arg'

  77      35  LOAD_GLOBAL           0  'print'
          38  LOAD_FAST             2  'arg'
          41  LOAD_CONST            2  'end'
          44  LOAD_CONST            3  ' '
          47  CALL_FUNCTION_257   257 
          50  POP_TOP          
          51  JUMP_BACK            29  'to 29'
          54  POP_BLOCK        
        55_0  COME_FROM                '22'

  78      55  LOAD_GLOBAL           0  'print'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

Parse error at or near `CALL_FUNCTION_259' instruction at offset 18

        def error_fmt(fmt, *args):
            print(get_cur_time_str(), '[ERROR]', fmt.format(*args))

        def warning_fmt(fmt, *args):
            print(get_cur_time_str(), '[WARNING]', fmt.format(*args))

        def error_fmtp(fmt, *args):
            print(get_cur_time_str(), '[ERROR]', fmt % args)

        def warning_fmtp(fmt, *args):
            print(get_cur_time_str(), '[WARNING]', fmt % args)

        def debug_assert(cond, fmt, *args):
            pass

        gd = global_data
        gd.set_global_data('log_info', info, True)
        gd.set_global_data('log_debug', debug, True)
        gd.set_global_data('log_error', error, True)
        gd.set_global_data('log_warning', warning, True)
        gd.set_global_data('log_warn', warning, True)
        gd.set_global_data('log_info_fmt', info_fmt, True)
        gd.set_global_data('log_debug_fmt', debug_fmt, True)
        gd.set_global_data('log_error_fmt', error_fmt, True)
        gd.set_global_data('log_warning_fmt', warning_fmt, True)
        gd.set_global_data('log_info_fmtp', info_fmtp, True)
        gd.set_global_data('log_error_fmtp', error_fmtp, True)
        gd.set_global_data('log_debug_fmtp', debug_fmtp, True)
        gd.set_global_data('log_warning_fmtp', warning_fmtp, True)
        gd.set_global_data('log_assert', debug_assert, True)

    def on_finalize(self):
        gd = global_data
        gd.del_global_data('log_info')
        gd.del_global_data('log_debug')
        gd.del_global_data('log_error')
        gd.del_global_data('log_warning')
        gd.del_global_data('log_warn')
        gd.del_global_data('log_info_fmt')
        gd.del_global_data('log_debug_fmt')
        gd.del_global_data('log_error_fmt')
        gd.del_global_data('log_warning_fmt')
        gd.del_global_data('log_info_fmtp')
        gd.del_global_data('log_error_fmtp')
        gd.del_global_data('log_debug_fmtp')
        gd.del_global_data('log_warning_fmtp')
        gd.del_global_data('log_assert')


def compact_traceback():
    t, v, tb = sys.exc_info()
    tbinfo = []
    if tb is None:
        return
    else:
        while tb:
            tbinfo.append((
             tb.tb_frame.f_code.co_filename,
             tb.tb_frame.f_code.co_name,
             str(tb.tb_lineno)))
            tb = tb.tb_next

        del tb
        pfile, function, line = tbinfo[-1]
        info = ' '.join([ '[%s|%s|%s]' % x for x in tbinfo ])
        return (
         (
          pfile, function, line), t, v, info)


def log_compact_traceback(self):
    self.error(traceback.format_exc())


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARN
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG

class LogManager(object):
    created_modules = set()
    log_level = DEBUG

    @staticmethod
    def get_logger(moduleName):
        if moduleName in LogManager.created_modules:
            return logging.getLogger(moduleName)
        logger = logging.getLogger(moduleName)
        logger.log_last_except = six.create_bound_method(log_compact_traceback, logger)
        logger.setLevel(LogManager.log_level)
        ch = logging.StreamHandler()
        ch.setLevel(LogManager.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        LogManager.created_modules.add(moduleName)
        return logger

    @staticmethod
    def set_log_level(lv):
        LogManager.log_level = lv
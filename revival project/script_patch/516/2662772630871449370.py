# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/mobilelog/LogManager.py
from __future__ import absolute_import
import sys
import logging
import traceback
import six
if six.PY2:
    import new

def compact_traceback():
    t, v, tb = sys.exc_info()
    tbinfo = []
    if tb == None:
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
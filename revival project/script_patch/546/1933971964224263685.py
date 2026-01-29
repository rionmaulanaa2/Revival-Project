# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/com_factory.py
from __future__ import absolute_import
import sys
import inspect
import six

def _get_component(com_name, com_type):
    mpath = 'logic.gcommon.component.%s.%s' % (com_type, com_name)
    mod = sys.modules.get(mpath)
    if not mod:
        mod = __import__(mpath, globals(), locals(), [com_name])
    com = getattr(mod, com_name, None)
    if com is None:
        log_error('[Component %s] Not Supported', com_name)
        return
    else:
        return com


def load_com(com_name, com_type):
    component = _get_component(com_name, com_type)
    return component()


def fill_com_type(rlist, stype, tlist):
    for com in tlist:
        rlist.append((stype, com))


def component(share=[], client=[], server=[]):

    def _component(unit):

        def _init_coms(self, bdict):
            com_types = []
            fill_com_type(com_types, 'share', share)
            fill_com_type(com_types, 'client', client)
            fill_com_type(com_types, 'server', server)
            for cpath, com in com_types:
                if isinstance(com, tuple):
                    com_type, com_state = com if 1 else (com, None)
                    if hasattr(com_state, '__call__'):
                        if not com_state(bdict):
                            continue
                    elif com_state and com_state not in bdict:
                        continue
                    if com_type.find('.') > 0:
                        com_prefix, com_type = com_type.rsplit('.', 1)
                        cpath = '%s.%s' % (cpath, com_prefix)
                    self.add_com(com_type, cpath)

            self._post_init_coms(bdict)
            return

        unit._init_coms = _init_coms
        return unit

    return _component


def DoExtendToUnit(func):
    func.__need_extend_to_unit = True
    return func


def IsExtendToUnit--- This code section failed: ---

  83       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'False'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_3       3 
          12  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9


class UnitComMetaclass(type):

    def __new__(cls, name, bases, dct):
        newcls = super(UnitComMetaclass, cls).__new__(cls, name, bases, dct)
        for name, func in inspect.getmembers(newcls):
            if (inspect.ismethod(func) or inspect.isfunction(func)) and IsExtendToUnit(func):
                continue

        return newcls
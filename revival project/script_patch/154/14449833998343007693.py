# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/SimpleEventManager.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
import cython
import types
from collections import defaultdict
from .EventStop import ESTOP
from logic.gcommon.utility import dummy_cb
from .ISimpleEventManager import ISimpleEventManager

def _fast_remove_coms_event_func(unit_obj, key):
    if not key.startswith('ev_'):
        key = 'ev_' + key.lower()
    if key in unit_obj.fast_acc_dict:
        for obj in unit_obj.fast_acc_dict[key]:
            if key in obj.__dict__:
                delattr(obj, key)

        unit_obj.fast_acc_dict[key].clear()
    if key in unit_obj.__dict__:
        del unit_obj.__dict__[key]


def old_remove_coms_event_func(self, key):
    if not key.startswith('ev_'):
        key = 'ev_' + key.lower()
    for com in six.itervalues(self._coms):
        d = com.__dict__
        if key in d:
            del d[key]
        if 'is_com_behavior' in d:
            states = d['_states']
            for state in six.itervalues(states):
                if key in state.__dict__:
                    del state.__dict__[key]

    if key in self.__dict__:
        del self.__dict__[key]


_remove_coms_event_func = _fast_remove_coms_event_func

def com_bind_event(obj, einfo):
    unit_obj = obj.unit_obj
    regist_event = unit_obj.regist_event
    for key, func_name in six.iteritems(einfo):
        priority = 0
        if type(func_name) in (tuple, list):
            func_name, priority = func_name
        func = getattr(obj, func_name, None)
        if not func:
            continue
        regist_event(key, func, priority)

    return


def com_unbind_event(obj, einfo):
    unit_obj = obj.unit_obj
    unregist_event = unit_obj.unregist_event
    for key, func_name in six.iteritems(einfo):
        if type(func_name) in (tuple, list):
            func_name, priority = func_name
        func = getattr(obj, func_name, None)
        if not func:
            continue
        unregist_event(key, func)

    return


def check_G(func):
    return func


def check_ev(func):
    return func


def default_empty():
    return None


class SimpleEventManager(ISimpleEventManager):

    def __init__(self):
        super(SimpleEventManager, self).__init__()
        self._event_dict = defaultdict(list)
        self.unit_obj = None
        self._lock = False
        return

    def get_event_func(self, event):
        event_handlers = self._event_dict[event]
        if event_handlers:
            return event_handlers[0][1]
        else:
            return None

    def lock(self, value):
        self._lock = value

    @check_G
    def emit(self, event, *args, **kwargs):
        event_handlers = self._event_dict[event]
        for priority, func in tuple(event_handlers):
            ret = func(*args, **kwargs)
            if ret is ESTOP:
                break

    def value(self, event, *args, **kwargs):
        event_handlers = self._event_dict[event]
        if event_handlers:
            return event_handlers[0][1](*args, **kwargs)
        else:
            return None

    @check_ev
    def regist_event(self, event, func, priority=0):
        el = self._event_dict[event]
        last_priority = priority
        if el:
            last_priority = el[-1][0]
        el.append((priority, func))
        if last_priority > priority:
            el.sort(key=cmp_to_key(--- This code section failed: ---

 167       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_ATTR             1  'compare'
           9  BINARY_SUBSCR    
          10  LOAD_FAST             1  'y'
          13  LOAD_CONST            1  ''
          16  BINARY_SUBSCR    
          17  CALL_FUNCTION_2       2 
          20  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
))
            if event.startswith('G_'):
                _remove_coms_event_func(self.unit_obj, event)

    @check_ev
    def unregist_event(self, event, func):
        event_handlers = self._event_dict.get(event, [])
        for event_handler in event_handlers[:]:
            if func == event_handler[1]:
                event_handlers.remove(event_handler)
                if event.startswith('G_'):
                    _remove_coms_event_func(self.unit_obj, event)

    def destroy(self):
        for key, obj_set in six.iteritems(self.unit_obj.fast_acc_dict):
            for obj in obj_set:
                obj.__dict__.pop(key, None)

            obj_set.clear()

        self._event_dict.clear()
        self._event_dict = None
        self.unit_obj = None
        return

    def tick(self):
        pass
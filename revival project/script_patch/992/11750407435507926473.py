# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/lobby_click_interval_utils.py
from __future__ import absolute_import
import time
LAST_CLICK_TIME = 0.0
CLICK_INTERVAL = 0.5

def check_click_interval(node=None):

    def method(func):

        def wrapper(*args, **kwargs):
            global LAST_CLICK_TIME
            cur_time = time.time()
            if cur_time - LAST_CLICK_TIME > CLICK_INTERVAL:
                LAST_CLICK_TIME = cur_time
                func(*args, **kwargs)

        node and node.BindMethod('OnClick', wrapper)
        return wrapper

    return method


UNIQUE_CLICK_OCCUPIED = False
LAST_TRIGGER_END_TIME = 0.0
TRIGGER_INTERVAL = 0.1

def global_unique_click(node):

    def method(func):

        def OnBegin(*args, **kwargs):
            global LAST_TRIGGER_END_TIME
            global UNIQUE_CLICK_OCCUPIED
            if UNIQUE_CLICK_OCCUPIED:
                return False
            cur_time = time.time()
            if cur_time - LAST_TRIGGER_END_TIME <= TRIGGER_INTERVAL:
                return False
            UNIQUE_CLICK_OCCUPIED = True
            return True

        node.BindMethod('OnBegin', OnBegin)

        def OnCancel(*args, **kwargs):
            global LAST_TRIGGER_END_TIME
            global UNIQUE_CLICK_OCCUPIED
            UNIQUE_CLICK_OCCUPIED = False
            LAST_TRIGGER_END_TIME = time.time()

        node.BindMethod('OnCancel', OnCancel)

        def OnEnd(*args, **kwargs):
            global LAST_TRIGGER_END_TIME
            global UNIQUE_CLICK_OCCUPIED
            UNIQUE_CLICK_OCCUPIED = False
            LAST_TRIGGER_END_TIME = time.time()

        node.BindMethod('OnEnd', OnEnd)
        node.BindMethod('OnClick', func)
        return func

    return method
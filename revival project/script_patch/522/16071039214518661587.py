# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/factory.py
from __future__ import absolute_import
import sys
import exception_hook
all_scene_part = {}
all_sub_sys = {}

def _import_part(part_type):
    global all_scene_part
    prefix = 'logic.vscene.parts'
    part_cls = _import_cls(part_type, prefix)
    if part_cls:
        all_scene_part[part_type] = part_cls
    return part_cls


def _import_sub_sys(sys_type):
    global all_sub_sys
    prefix = 'logic.vscene.part_sys'
    sys_cls = _import_cls(sys_type, prefix)
    if sys_cls:
        all_sub_sys[sys_type] = sys_cls
    return sys_cls


def _import_cls(cls_type, prefix):
    mod = __import__(prefix, globals(), locals(), [cls_type])
    mod = getattr(mod, cls_type, None)
    com = getattr(mod, cls_type, None)
    load_err = None
    if com is None:
        exception_hook.upload_exception(*sys.exc_info())
        return
    else:
        return com


def load_cls(cls_type, cls_dict, import_func):
    cls = None
    try:
        cls = cls_dict.get(cls_type, None)
        if cls is None:
            cls = import_func(cls_type)
    except:
        log_error('load wrong type of scene com', cls_type)
        exception_hook.upload_exception(*sys.exc_info())

    return cls


def load_com(scn, part_type):
    cls = load_cls(part_type, all_scene_part, _import_part)
    if cls:
        return cls(scn, part_type)
    else:
        return None
        return None


def load_sub_sys(sys_type):
    cls = load_cls(sys_type, all_sub_sys, _import_sub_sys)
    if cls:
        return cls()
    else:
        return None
        return None
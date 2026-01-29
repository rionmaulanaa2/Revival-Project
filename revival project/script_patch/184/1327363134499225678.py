# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Meta/ClassMetaManager.py
ClassMetas = {}
ExtraMetas = {}
_ClassMetaWatcher = []

def sunshine_class_meta(cls):
    RegisterClassMeta(cls())
    return cls


def sunshine_extra_meta(cls):
    UpdateClassExtraMeta(cls())
    return cls


def RegisterClassMetaWatcher(watcher):
    _ClassMetaWatcher.append(watcher)


def RegisterClassMeta(meta):
    global ClassMetas
    from .TypeMeta import BaseClassMeta
    ClassMetas[meta.className] = meta
    extraMeta = ExtraMetas.pop(meta.className, None)
    if extraMeta:
        UpdateClassExtraMeta(extraMeta)
    for watcher in _ClassMetaWatcher:
        watcher(meta.className, meta)

    return


def UpdateClassExtraMeta(extraMeta):
    meta = GetClassMeta(extraMeta.className)
    if not meta:
        ExtraMetas[extraMeta.className] = extraMeta
        return
    meta.UpdateExtraMeta(extraMeta)


def GetClassMeta(className):
    return ClassMetas.get(className)


def GetAllClassMetas():
    return ClassMetas
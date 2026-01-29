# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/reloadall.py
from __future__ import absolute_import
from . import reimport

def init_reload():
    reimport.modified()


def reload_client(path=None):
    import xupdate
    arr = reimport.modified(path)
    for m in arr:
        xupdate.update(m)

    return arr


def reload_modules(pathlist):
    import xupdate
    arr = reimport.modified_loaded(pathlist)
    for m in arr:
        xupdate.update(m)

    return arr


def ex_reload_client(modules=None):
    from common.utils import reloadex
    if modules is None:
        modules = reloadex.modified()
    reloadex.reloadex(modules)
    return


def code_hotfix(path=None):
    reload_client(path)
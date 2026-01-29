# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/__init__.py
from __future__ import absolute_import

def is_need_patch():
    import C_file
    return C_file.find_res_file('__need_patch__', '')


def is_need_patch_new():
    import C_file
    return C_file.find_res_file('__need_patch_new__', '')
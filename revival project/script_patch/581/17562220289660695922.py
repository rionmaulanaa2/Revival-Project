# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/safe_eval.py
from __future__ import absolute_import

def calc(ret_type, func_str, *args):
    import re
    if re.findall('[A-Za-z_]', func_str):
        return
    else:
        try:
            v = eval(func_str.format(*args))
            return ret_type(v)
        except:
            return

        return
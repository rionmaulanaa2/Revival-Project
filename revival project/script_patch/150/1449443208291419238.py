# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/math_utils.py
from __future__ import absolute_import
import math

def poly1d(a, b, c):
    solve_root = math.sqrt(abs(b * b - 4 * a * c))
    res1 = (-b + solve_root) / (2 * a)
    res2 = (-b - solve_root) / (2 * a)
    return (
     res1, res2)
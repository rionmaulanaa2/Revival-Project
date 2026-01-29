# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/pyfx.py
from __future__ import absolute_import
import os
import sys
import six.moves.builtins
p = '../../pyfx11'
sys.path.append(p)
six.moves.builtins.__dict__['__pyfx_path'] = p
npkimporter = sys.path_hooks.pop()
import pyfx11
import present_demo
present_demo.present_compute_shader()
sys.path_hooks.append(npkimporter)
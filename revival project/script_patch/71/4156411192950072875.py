# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/matrix_utils.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.const import USE_FLOAT_REDUCE
import logic.gcommon.common_utils.float_reduce_util as fl_reduce

def format_matrix_to_tuple(mat):
    import math3d
    ret = []
    for i in range(4):
        for j in range(4):
            ret.append(mat.get(i, j))

    if USE_FLOAT_REDUCE:
        ret = fl_reduce.f_to_i(ret)
    return tuple(ret)


def create_matrix_from_tuple(_tuple):
    import math3d
    if USE_FLOAT_REDUCE:
        _tuple = list(_tuple)
        _tuple = fl_reduce.i_to_f(_tuple)
    mat = math3d.matrix()
    mat.set_all(_tuple)
    return mat
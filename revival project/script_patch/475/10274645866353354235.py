# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/math3d_utils.py
from __future__ import absolute_import
from ..const import USE_FLOAT_REDUCE
from .float_reduce_util import REDUCE_FACTOR
import math3d

def v3d_to_tp(v3d):
    if USE_FLOAT_REDUCE:
        return (int(v3d.x * REDUCE_FACTOR), int(v3d.y * REDUCE_FACTOR), int(v3d.z * REDUCE_FACTOR))
    else:
        return (
         v3d.x, v3d.y, v3d.z)


def tp_to_v3d--- This code section failed: ---

  23       0  LOAD_GLOBAL           0  'USE_FLOAT_REDUCE'
           3  POP_JUMP_IF_FALSE    40  'to 40'

  24       6  LOAD_GLOBAL           1  'math3d'
           9  LOAD_ATTR             2  'vector'
          12  LOAD_ATTR             1  'math3d'
          15  BINARY_SUBSCR    
          16  LOAD_GLOBAL           3  'REDUCE_FACTOR'
          19  BINARY_DIVIDE    
          20  BINARY_DIVIDE    
          21  BINARY_DIVIDE    
          22  BINARY_DIVIDE    
          23  BINARY_SUBSCR    
          24  LOAD_GLOBAL           3  'REDUCE_FACTOR'
          27  BINARY_DIVIDE    
          28  BINARY_DIVIDE    
          29  PRINT_ITEM_TO    
          30  PRINT_ITEM_TO    
          31  BINARY_SUBSCR    
          32  LOAD_GLOBAL           3  'REDUCE_FACTOR'
          35  BINARY_DIVIDE    
          36  CALL_FUNCTION_3       3 
          39  RETURN_END_IF    
        40_0  COME_FROM                '3'

  26      40  LOAD_GLOBAL           1  'math3d'
          43  LOAD_ATTR             2  'vector'
          46  LOAD_FAST             0  'tp'
          49  CALL_FUNCTION_VAR_0     0 
          52  RETURN_VALUE     

Parse error at or near `BINARY_SUBSCR' instruction at offset 15


def normal_tp_to_v3d(val):
    return math3d.vector(*val)


def normal_v3d_to_tp(val):
    return (
     val.x, val.y, val.z)


def matrix_to_tp(mat):
    return (
     (
      mat.get(0, 0), mat.get(0, 1), mat.get(0, 2), mat.get(0, 3)),
     (
      mat.get(1, 0), mat.get(1, 1), mat.get(1, 2), mat.get(1, 3)),
     (
      mat.get(2, 0), mat.get(2, 1), mat.get(2, 2), mat.get(2, 3)),
     (
      mat.get(3, 0), mat.get(3, 1), mat.get(3, 2), mat.get(3, 3)))
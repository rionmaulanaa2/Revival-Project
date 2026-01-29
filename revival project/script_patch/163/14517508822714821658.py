# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/pylrc/utilities.py
from __future__ import absolute_import
from six.moves import range
from datetime import datetime

def validateTimecode(timecode):
    try:
        unpackTimecode(timecode)
        return True
    except ValueError:
        return False


def unpackTimecode--- This code section failed: ---

  20       0  LOAD_CONST            1  '.'
           3  LOAD_FAST             0  'timecode'
           6  COMPARE_OP            6  'in'
           9  POP_JUMP_IF_FALSE    30  'to 30'

  21      12  LOAD_GLOBAL           0  'datetime'
          15  LOAD_ATTR             1  'strptime'
          18  LOAD_ATTR             2  'minute'
          21  CALL_FUNCTION_2       2 
          24  STORE_FAST            1  'x'
          27  JUMP_FORWARD         15  'to 45'

  23      30  LOAD_GLOBAL           0  'datetime'
          33  LOAD_ATTR             1  'strptime'
          36  LOAD_ATTR             3  'second'
          39  CALL_FUNCTION_2       2 
          42  STORE_FAST            1  'x'
        45_0  COME_FROM                '27'

  24      45  LOAD_FAST             1  'x'
          48  LOAD_ATTR             2  'minute'
          51  STORE_FAST            2  'minutes'

  25      54  LOAD_FAST             1  'x'
          57  LOAD_ATTR             3  'second'
          60  STORE_FAST            3  'seconds'

  26      63  LOAD_GLOBAL           4  'int'
          66  LOAD_FAST             1  'x'
          69  LOAD_ATTR             5  'microsecond'
          72  LOAD_CONST            4  1000
          75  BINARY_DIVIDE    
          76  CALL_FUNCTION_1       1 
          79  STORE_FAST            4  'milliseconds'

  27      82  LOAD_FAST             2  'minutes'
          85  LOAD_FAST             3  'seconds'
          88  LOAD_FAST             4  'milliseconds'
          91  BUILD_TUPLE_3         3 
          94  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 21


def findEvenSplit(line):
    word_list = line.split(' ')
    differences = []
    for i in range(len(word_list)):
        group1 = ' '.join(word_list[0:i + 1])
        group2 = ' '.join(word_list[i + 1::])
        differences.append(abs(len(group1) - len(group2)))

    index = differences.index(min(differences))
    for i in range(len(word_list)):
        if i == index:
            group1 = ' '.join(word_list[0:i + 1])
            group2 = ' '.join(word_list[i + 1::])

    return ''.join([group1, '\n', group2]).rstrip()